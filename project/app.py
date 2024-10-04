from flask import Flask, render_template, request
import waitress

app = Flask(__name__)

# Home route serving index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user input and display results
@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    
    # Mock SQL query generation (replace this with actual text-to-SQL logic)
    sql_query = f"SELECT * FROM products WHERE year = 2023;"
    
    # Mock data to display (replace this with actual data from SQL execution)
    data = [
        {"Product": "Laptop", "Price": 1000, "Year": 2023},
        {"Product": "Smartphone", "Price": 700, "Year": 2023},
        {"Product": "Tablet", "Price": 500, "Year": 2023}
    ]
    
    return render_template('index.html', sql_query=sql_query, data=data)

# python -m waitress --host=0.0.0.0 --port=5000 app:app
if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=5000)
