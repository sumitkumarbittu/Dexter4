import os
from flask import Flask

app = Flask(__name__)

# function to generate a random number between 1 and 10
def rand10():
    return random.randint(1, 10)

# API endpoint
@app.route('/api/generaterandom')
def generate_random():
    number = rand10()
    return jsonify(random_number=number)

if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)
