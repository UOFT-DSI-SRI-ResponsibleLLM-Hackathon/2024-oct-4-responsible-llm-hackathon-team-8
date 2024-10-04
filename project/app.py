import psycopg2
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

chat_history = []
database_link = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global database_link

    # if any submission on index page
    if request.method == "POST":
        user_input = request.form.get("user_input")
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

        else:  # Error handling
            chat_history.append(
                {
                    "user_input": user_input,
                    "data": "Please connect to a valid database first!!!",
                    "type": "message",
                }
            )

        return redirect(url_for("index"))

    return render_template(
        "index.html", chat_history=chat_history, database_link=database_link
    )


@app.route("/set_db_link", methods=["POST"])
def set_db_link():
    global database_link
    database_link = request.form.get("db_link")

    # Set the new database link
    if database_link:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_link
        print(f"Database link set to: {database_link}")

        # Test the connection
        try:
            conn = psycopg2.connect(database_link)
            print("Connected to the database successfully!")

            # Close the connection after testing
            conn.close()
            print("Disconnected from the database.")

        except Exception as e:
            print(f"Connection failed: {str(e)}")
            print("Database invalid or Connection Error...")
            database_link = ""  # empty database link if invalid

    return redirect(url_for("index"))


# Triage function: it is used to determine which model to send the data to


# Natural langauge processing: OpenAI API call


# Query question: send the data to the Query Model
# It need to guarentee that it won't do any changes on the database.


# Submit the database URI, serve as the endpoint for Frontend


# Receive the user's conversation


# Generate chart that can satisfy frontend's format requirement


"""
python -m waitress --host=0.0.0.0 --port=5000 app:app
"""
if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
