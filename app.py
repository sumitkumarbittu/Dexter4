import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello from Render!"}

if __name__ == "__main__":
    # Render provides a PORT env variable
    port = int(os.environ.get("PORT", 5001))  # defaults to 5001 if running locally
    app.run(host="0.0.0.0", port=port)
