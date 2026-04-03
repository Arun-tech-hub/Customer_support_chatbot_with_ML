from flask import Flask, request, jsonify, render_template
import sqlite3
from model import load_model, search_db

app = Flask(__name__)

# Load the model and vectorizer
vectorizer, model = load_model()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

# Home route (renders the chat interface)
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot API route (handles customer queries)
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('query')
    
    # Search for a matching solution
    solution = search_db(user_input)
    
    if solution:
        return jsonify({"response": solution})
    else:
        # If no solution is found, store the query for support staff intervention
        conn = get_db_connection()
        conn.execute('INSERT INTO queries (customer_query, status) VALUES (?, ?)',
                     (user_input, 'open'))
        conn.commit()
        conn.close()
        return jsonify({"response": "Our support staff will get back to you soon."})

# Support staff panel to view unresolved queries
@app.route('/unresolved', methods=['GET', 'POST'])
def unresolved():
    conn = get_db_connection()
    unresolved_queries = conn.execute('SELECT * FROM queries WHERE status = ?', ('open',)).fetchall()
    
    if request.method == 'POST':
        # Staff resolving a query
        query_id = request.form.get('query_id')
        response = request.form.get('response')
        
        # Update the query in the DB
        conn.execute('UPDATE queries SET support_response = ?, status = ? WHERE id = ?',
                     (response, 'closed', query_id))
        
        # Optionally add this new Q&A to the solutions table for future use
        query = conn.execute('SELECT customer_query FROM queries WHERE id = ?', (query_id,)).fetchone()['customer_query']
        conn.execute('INSERT INTO solutions (question, answer) VALUES (?, ?)', (query, response))
        conn.commit()

    unresolved_queries = conn.execute('SELECT * FROM queries WHERE status = ?', ('open',)).fetchall()
    conn.close()
    
    return render_template('unresolved.html', unresolved_queries=unresolved_queries)

if __name__ == "__main__":
    app.run(debug=True)
