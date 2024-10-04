import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

chat_history = []
database_link = ""


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
    global database_link
    db_link = request.json.get("db_link")

    if db_link:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_link
        print(f"Database link set to: {db_link}")

        # Test the connection
        try:
            conn = psycopg2.connect(db_link)
            print("Connected to the database successfully!")

            # Close the connection after testing
            conn.close()
            print("Disconnected from the database.")

            database_link = db_link  # Set the database link if connection is successful
            return header_processing(jsonify({"status": "Connected", "data": "Database link set and connected successfully!"}))

        except Exception as e:
            print(f"Connection failed: {str(e)}")
            print("Database invalid or Connection Error...")
            database_link = ""  # Reset database link if invalid
            return header_processing(jsonify({"status": "Invalid", "data": "Invalid database or cannot be connected."}))

    return header_processing(jsonify({"status": "Invalid", "data": "No database link provided."}))


@app.route("/api/query", methods=["POST"])
def query_database():
    """Handle user input and generate a SQL query."""
    global database_link

    user_input = request.json.get("user_input")
    if database_link:
        sql_query = "SELECT * FROM example_table WHERE condition"  # Placeholder for generated SQL
        data = [
            {"Product": "Example Product 1", "Price": 10, "Year": 2022},
            {"Product": "Example Product 2", "Price": 15, "Year": 2023},
        ]

        # Append user input and bot response to chat history
        chat_history.append(
            {
                "user_input": user_input,
                "sql_query": sql_query,
                "data": data,
                "type": "query",
            }
        )
        return header_processing(jsonify({"user_input": user_input, "sql_query": sql_query, "data": data}))
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
