from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Store chat history
chat_history = []
database_link = ""  # Variable to store the database link

@app.route('/', methods=['GET', 'POST'])
def index():
    global database_link

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        # Here, you would add logic to generate the SQL query and fetch data
        sql_query = "SELECT * FROM example_table WHERE condition"  # Placeholder for generated SQL
        data = [
            {"Product": "Example Product 1", "Price": 10, "Year": 2022},
            {"Product": "Example Product 2", "Price": 15, "Year": 2023}
        ]  # Placeholder for fetched data
        
        # Append user input and bot response to chat history
        chat_history.append({'user_input': user_input, 'sql_query': sql_query, 'data': data})

        return redirect(url_for('index'))

    return render_template('index.html', chat_history=chat_history, database_link=database_link)

@app.route('/set_db_link', methods=['POST'])
def set_db_link():
    global database_link
    database_link = request.form.get('db_link')

    # Set the new database link (e.g., for future use in connecting to PostgreSQL)
    if database_link:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_link
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

    return redirect(url_for('index'))


"""
python -m waitress --host=0.0.0.0 --port=5000 app:app
"""
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)