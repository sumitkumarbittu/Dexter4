import os
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)