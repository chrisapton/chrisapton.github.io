from flask import Flask, jsonify, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
