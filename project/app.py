import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

chat_history = []
database_link = ""
conn = None

def header_processing(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


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
            return header_processing(jsonify({"status": "Connected", "data": "Connected to Database Successfully!"}))

        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return header_processing(jsonify({"status": "Invalid", "data": "Database invalid or Connection Error..."}))

    return header_processing(jsonify({"status": "Invalid", "data": "No database link provided."}))


@app.route("/api/query", methods=["POST"])
def query_database():
    """Handle user input and generate a SQL query."""
    global database_link, conn

    user_input = request.json.get("user_input")
    if conn:
        sql_query = """
            SELECT team_name, rank, match_numbers
            FROM teams_data
            ORDER BY rank ASC
            LIMIT 3;
        """
        cursor = conn.cursor()
        cursor.execute(sql_query)

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
                "data": "Please connect to a valid database first!!!",
                "type": "message",
            }
        )
        return header_processing(jsonify({"data": "Please connect to a valid database first!"}))


"""
python -m waitress --host=0.0.0.0 --port=5000 app:app
"""
if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
