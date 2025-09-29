import os
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

@app.route('/api/generaterandom')
def generate_random():
    return jsonify(number=random.randint(1, 10))

if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)
