# Tees: Talk to a Database

An end-to-end **LLM-powered Natural Language to SQL system** that allows users to interact with a MySQL database using plain English.

Tees is a T-shirt store whose inventory, sales, and discount data is stored in a MySQL database. Instead of writing SQL queries manually, a store manager can ask questions in natural language, and the system uses **Google Gemini + LangChain** to generate and execute the appropriate SQL query and return the result.

## 🚀 Project Overview

The system follows this workflow:

**Natural Language Question → LLM → SQL Query → MySQL Database → Result**

For example:

> "How many white Adidas T-shirts do we have left in stock?"

The system understands the question, generates the corresponding SQL query, executes it against the MySQL database, and displays the result through an interactive Streamlit interface.

---

## ✨ Features

- **Natural Language to SQL**  
  Converts plain-English questions into executable SQL queries.

- **Few-Shot Learning**  
  Uses carefully designed examples to improve SQL generation and query accuracy.

- **LLM-Powered Query Generation**  
  Uses Google Gemini through LangChain to understand user questions and generate SQL.

- **MySQL Integration**  
  Executes generated queries directly against the T-shirt store database.

- **Error Handling**  
  Handles SQL parsing and database execution errors with fallback mechanisms.

- **Interactive Web Interface**  
  Provides a simple and user-friendly Streamlit interface for querying the database.

- **Real-Time Results**  
  Retrieves results directly from the connected MySQL database.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| LLM | Google Gemini 1.5 Flash |
| LLM Framework | LangChain |
| Database | MySQL 8.0 |
| Database Connector | PyMySQL |
| UI | Streamlit |
| Programming Language | Python 3.11+ |
| Query Generation | Few-Shot Learning |

---

## 🏪 Database

The project simulates a T-shirt store called **Tees** that sells products from brands such as:

- Adidas
- Nike
- Van Heusen
- Levi's

The database contains information related to:

- Product inventory
- T-shirt brands
- Colors
- Sizes
- Pricing
- Sales
- Discounts

---

## 📂 Project Structure

```text
4_sqldb_tshirts/
│
├── database/
│   └── db_creation_atliq_t_shirts.sql
│
├── few_shots.py
├── langchain_helper.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── t_shirt_sales_llm.ipynb
