import os
import random
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Database Connection using internal URL ---
def get_db_connection():
    DATABASE_URL = os.environ.get("PGINTERNALURL")  # Internal URL on Render
    return psycopg2.connect(DATABASE_URL)


# --- Function to fetch feedback records ---
def get_all_feedback():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, comment FROM feedback ORDER BY id ASC")
        rows = cur.fetchall()  # Fetch all records
        cur.close()
        conn.close()
        # Convert to list of dicts for JSON response
        feedback_list = [
            {"id": row[0], "name": row[1], "age": row[2], "comment": row[3]}
            for row in rows
        ]
        return feedback_list
    except Exception as e:
        print("Error fetching feedback:", e)
        return []


# --- API Calls ---

# Random Number API
@app.route('/api/generaterandom')
def generate_random():
    return jsonify(number=random.randint(1, 10))


# Sum API
@app.route('/api/sum')
def get_sum():
    try:
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
        return jsonify(result=a + b)
    except Exception:
        return jsonify(error="Invalid input"), 400


# Feedback API
@app.route('/api/feedback', methods=["POST"])
def feedback():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    comment = data.get("comment", "")

    if not name or not age:
        return jsonify(error="Name and Age are required"), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, name TEXT, age INT, comment TEXT)"
        )
        cur.execute(
            "INSERT INTO feedback (name, age, comment) VALUES (%s, %s, %s)",
            (name, age, comment),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message="Feedback saved successfully ✅")
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/api/displayfeedback', methods=["GET"])
def fetch_feedback():
    feedback_list = get_all_feedback()
    return jsonify(feedback_list)


if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)