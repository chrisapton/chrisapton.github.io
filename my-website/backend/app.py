from flask import Flask, jsonify, request
import os

app = Flask(__name__)


#curl -X POST https://backend-personal-website-ee5a10ef78c9.herokuapp.com/run-python-code -H "Content-Type: application/json" -d '{"input": "Hello, World!"}'
#{
#  "output": "!dlroW ,olleH"
#}
###

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/run-python-code", methods=["POST"])
def run_python_code():
    # Example: Get data from the frontend
    input_data = request.json.get("input")
    # Process data (replace this with your logic)
    result = {"output": input_data[::-1]}  # Reverse the input string
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

