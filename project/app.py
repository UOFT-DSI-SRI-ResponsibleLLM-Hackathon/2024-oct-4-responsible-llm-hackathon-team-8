import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain_openai import ChatOpenAI
import os

app = Flask(__name__)
CORS(app)

chat_history = []
database_link = ""
conn = None

os.environ['OPENAI_API_KEY'] = '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'
llm = ChatOpenAI(temperature=0.8, model_name='gpt-4o')


def header_processing(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


import re
def check_sql_query(sql_query):    
    pattern = r"```sql\s*([\s\S]*?)```"
    match = re.search(pattern, sql_query.content)
    if match:
        return match.group(1).strip()  # Return the content inside the triple single quotes
    else:
        return False
    

def get_table_attributes(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT datname FROM pg_database;")
    databases = cursor.fetchall()

    # Execute a query to list all tables in the current database
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)

    # Fetch the results
    tables = cursor.fetchall()

    if tables:
        table_name = tables[0] # HARDCODE TO FETCH THE FIRST TABLE -> FUTURE WORK NEEDED!!!
        table_name = table_name[0]
    else:
        return None, None

    # Fetch the column names
    cursor.execute(f"SELECT * FROM {table_name};")
    colnames = [desc[0] for desc in cursor.description]

    return table_name, colnames

def langchain_generate_sql(text, features, table_name):
    """Generate a SQL query using Langchain given natural language input and database schema."""
    prompt = f"Given a table named {table_name}, all its columns are: {features}, write a SQL query that fulfills this request: {text}."
    try:
        result = llm.invoke(prompt)
        return result
    except Exception as e:
        print(f"Langchain SQL generation failed: {str(e)}")
        return False
    

@app.route("/api/chat_history", methods=["GET"])
def get_chat_history():
    """Retrieve the chat history."""
    return header_processing(jsonify(chat_history))


@app.route("/api/set_db_link", methods=["POST"])
def set_db_link():
    """Set the database connection link."""
    global database_link, conn
    db_link = request.json.get("db_link")

    if db_link:
        # reset connection and database
        if conn:
            conn.close()
        conn = None
        database_link = ""

        app.config["SQLALCHEMY_DATABASE_URI"] = db_link
        print(f"Database link set to: {db_link}")

        # Test the connection
        try:
            conn = psycopg2.connect(db_link)
            print("Connected to the database successfully!")

            database_link = db_link  # Set the database link if connection is successful
            return header_processing(jsonify({"status": "Connected", "message": "Connected to Database Successfully!"}))

        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return header_processing(jsonify({"status": "Invalid", "message": "Database invalid or Connection Error..."}))

    return header_processing(jsonify({"status": "Invalid", "message": "No database link provided."}))


@app.route("/api/query", methods=["POST"])
def query_database():
    """Handle user input and generate a SQL query."""
    global database_link, conn

    user_input = request.json.get("user_input")
    if conn:
        table_name, colnames = get_table_attributes(conn)
        sql_query = langchain_generate_sql(user_input, colnames, table_name)
        response = sql_query.content
        
        sql_query = check_sql_query(sql_query)

        cursor = conn.cursor()
        if sql_query:
            try:
                cursor.execute(sql_query)
            except:
                chat_history.append(
                    {
                        "user_input": user_input,
                        "sql_query": sql_query,
                        "data": None,
                        "type": "query", 
                    }
                )
                return header_processing(jsonify({"user_input": user_input, "sql_query": sql_query, "data": None}))
        else:
            chat_history.append(
                {
                    "user_input": user_input,
                    "message": response,
                    "type": "message", 
                }
            )
            return header_processing(jsonify({"message": response}))

        # zip rows and features
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in data]

        chat_history.append(
            {
                "user_input": user_input,
                "sql_query": sql_query,
                "data": result,
                "type": "query",
            }
        )
        return header_processing(jsonify({"user_input": user_input, "sql_query": sql_query, "data": result}))
    else:  # Error handling
        chat_history.append(
            {
                "user_input": user_input,
                "message": "Please connect to a valid database first!!!",
                "type": "message",
            }
        )
        return header_processing(jsonify({"message": "Please connect to a valid database first!"}))

@app.route("/api/sqlexec", methods=["POST"])
def sql_execute():
    """Handle user input and execute a SQL query."""
    global database_link, conn

    sql_query = request.json.get("sql_query_input")
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)

        # zip rows and features
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in data]

        return header_processing(jsonify({"data": result}))
    else:  # Error handling
        return header_processing(jsonify({"message": "Please connect to a valid database first!"}))


"""
gunicorn --bind 0.0.0.0:5000 app:app
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

