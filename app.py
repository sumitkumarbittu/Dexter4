import os
import random
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Database Connection ---
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )


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


if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)