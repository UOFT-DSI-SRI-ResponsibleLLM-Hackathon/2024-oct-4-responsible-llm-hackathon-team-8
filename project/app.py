from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store chat history
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Here, you would add logic to generate the SQL query and fetch data
        sql_query = "SELECT * FROM example_table WHERE condition"  # Placeholder for generated SQL
        data = [
            {"Product": "Example Product 1", "Price": 10, "Year": 2022},
            {"Product": "Example Product 2", "Price": 15, "Year": 2023}
        ]  # Placeholder for fetched data
        
        # Append user input and bot response to chat history
        chat_history.append({'user_input': user_input, 'sql_query': sql_query, 'data': data})

        return redirect(url_for('index'))

    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
