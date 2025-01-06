from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# Sample project data
projects_data = [
    {
        "title": "Personal Website",
        "description": "A personal website to showcase my work.",
        "github": "https://github.com/chrisapton/chrisapton.github.io",
        "demoType": "link",  # Can be "link", "image", "code", or "script"
        "demoContent": "https://chrisapton.github.io/",  # URL for the demo link
        "startDate": "2025-01-01",
        "endDate": "2025-01-10",
        "ongoing": False,
        "skills": ["React", "HTML", "CSS", "JavaScript", "Heroku"]
    },
    {
        "title": "CalHacks 10.0: KnowBotics",
        "description": "Developed a homework helper bot powered by a Large Language Model (LLM) designed to provide personalized help by analyzing lecture slides, PDFs, and homework assignments, offering customized support for students’ academic tasks.",
        "github": "https://github.com/chrisapton/CalHackss",
        "demoType": None,  
        "demoContent": None,
        "startDate": "2023-10-01",
        "endDate": "2023-10-31", 
        "ongoing": False,
        "skills": ["Python", "OpenAI API", "LlamaIndex", "Reflex", "Natural Language Processing"]
    },
    {
        "title": "Heart Disease Prediction",
        "description": "Led the development of an XGBoost model with tuned hyperparameters, leveraging Cross-Validation to predict heart disease. Preprocessed data to improve model performance: Removed outliers and feature engineering. Developed in R. Optimized the model using Randomized Search for hyperparameter tuning achieving a 90% validation accuracy",
        "github": "https://github.com/chrisapton/Heart-Disease-Prediction",
        "demoType": None,
        "demoContent": None,  
        "startDate": "2022-06-01",
        "endDate": "2022-08-01",
        "ongoing": False,
        "skills": ["R", "Machine Learning", "XGBoost"]
    }
]


@app.route("/")
def home():
    return "Backend is running!"

# Route to reverse input (example route you had)
@app.route("/run-python-code", methods=["POST"])
def run_python_code():
    input_data = request.json.get("input")
    result = {"output": input_data[::-1]}  # Reverse the input string
    return jsonify(result)

# New route to serve project data
@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(projects_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

