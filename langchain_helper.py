from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate

from few_shots import few_shots

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()  # take environment variables from .env (especially openai api key)


def get_few_shot_db_chain():
    db_user = os.getenv("DB_USER", "root")  # Gets from .env file or defaults to "root"
    db_password = os.getenv("DB_PASSWORD", "")  # Gets from .env file or defaults to empty
    db_host = os.getenv("DB_HOST", "localhost")  # Gets from .env file or defaults to localhost
    db_port = os.getenv("DB_PORT", "3306")  # Gets from .env file or defaults to 3306
    db_name = os.getenv("DB_NAME", "atliq_tshirts")  # Gets from .env file or defaults to atliq_tshirts

    # URL encode the password to handle special characters like @
    encoded_password = quote_plus(db_password)
    
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}",
                              sample_rows_in_table_info=3)
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
import re

from few_shots import few_shots

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()  # take environment variables from .env (especially openai api key)


def get_few_shot_db_chain():
    db_user = os.getenv("DB_USER", "root")  # Gets from .env file or defaults to "root"
    db_password = os.getenv("DB_PASSWORD", "")  # Gets from .env file or defaults to empty
    db_host = os.getenv("DB_HOST", "localhost")  # Gets from .env file or defaults to localhost
    db_port = os.getenv("DB_PORT", "3306")  # Gets from .env file or defaults to 3306
    db_name = os.getenv("DB_NAME", "atliq_tshirts")  # Gets from .env file or defaults to atliq_tshirts

    # URL encode the password to handle special characters like @
    encoded_password = quote_plus(db_password)
    
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}",
                              sample_rows_in_table_info=3)
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

    # Temporarily skip the embeddings to isolate the error
    # embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # to_vectorize = [" ".join([str(v) for v in example.values()]) for example in few_shots]
    # vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    # example_selector = SemanticSimilarityExampleSelector(
    #     vectorstore=vectorstore,
    #     k=2,
    # )
    
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    
    Use the following format:
    
    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here
    
    Here are some examples:
    
    Question: How many t-shirts do we have left for Nike in XS size and white color?
    SQLQuery: SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'
    SQLResult: Result of the SQL query
    Answer: 91
    
    Question: How much is the total price of the inventory for all S-size t-shirts?
    SQLQuery: SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'
    SQLResult: Result of the SQL query
    Answer: 22292
    
    No pre-amble.
    """

    # Create a simple prompt template
    simple_prompt = PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=mysql_prompt + "\n\nDatabase tables:\n{table_info}\n\nQuestion: {input}\n"
    )
    
    return db, llm, simple_prompt


def get_sql_chain_response(question):
    """
    Get response from the SQL chain with proper error handling and SQL extraction
    """
    try:
        db, llm, simple_prompt = get_few_shot_db_chain()
        
        # Get database schema info
        table_info = db.get_table_info()
        
        # Create the prompt
        prompt = simple_prompt.format(input=question, table_info=table_info, top_k=5)
        
        # Get LLM response
        llm_response = llm.invoke(prompt)
        
        # Extract SQL query from the response
        sql_match = re.search(r'SQLQuery:\s*(.*?)(?:\n|$)', llm_response, re.IGNORECASE)
        
        if sql_match:
            sql_query = sql_match.group(1).strip()
            
            # Execute the SQL query
            try:
                sql_result = db.run(sql_query)
                
                # Convert result to string if it's not already
                if isinstance(sql_result, (list, tuple)):
                    sql_result_str = str(sql_result)
                else:
                    sql_result_str = str(sql_result)
                
                # Generate final answer
                final_prompt = f"""
                Question: {question}
                SQLQuery: {sql_query}
                SQLResult: {sql_result_str}
                
                Based on the SQL result above, provide a clear and concise answer to the question:
                """
                
                final_answer = llm.invoke(final_prompt)
                return final_answer
                
            except Exception as sql_error:
                return f"Error executing SQL query: {sql_error}\nQuery: {sql_query}"
                
        else:
            return f"Could not extract SQL query from LLM response: {llm_response}"
            
    except Exception as e:
        return f"Error in SQL chain: {e}"

