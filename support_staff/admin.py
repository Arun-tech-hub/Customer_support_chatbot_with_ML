from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/unresolved')
def unresolved():
    conn = get_db_connection()
    unresolved_queries = conn.execute('SELECT * FROM queries WHERE status = "open"').fetchall()
    conn.close()
    return render_template('unresolved.html', unresolved_queries=unresolved_queries)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
