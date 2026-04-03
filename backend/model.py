from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import sqlite3

# Load the model and vectorizer
def load_model():
    with open('model/chatbot_model.pkl', 'rb') as f:
        vectorizer, model = pickle.load(f)
    return vectorizer, model

# Search for a similar query in the DB
def search_db(customer_query):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM solutions")
    solutions = cursor.fetchall()
    conn.close()

    # Return the first matching solution or None if not found
    for question, answer in solutions:
        if question in customer_query:
            return answer
    return None
