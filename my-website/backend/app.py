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
        "title": "Task Manager App",
        "description": "A task management tool with drag-and-drop functionality.",
        "github": "https://github.com/username/task-manager",
        "demoType": "code",  # Indicates code snippets or instructions to run
        "demoContent": "npm start in the terminal to run the app locally",  # Instructions
        "startDate": "2023-06-01",
        "endDate": "2023-10-05",
        "ongoing": False,
        "skills": ["React", "Django", "PostgreSQL"]
    },
    {
        "title": "Blog Platform",
        "description": "An ongoing project for a personal blog platform.",
        "github": "https://github.com/username/blog-platform",
        "demoType": "image",  # Indicates an image demo
        "demoContent": "https://via.placeholder.com/300x200.png?text=Blog+Platform",  # URL to an image
        "startDate": "2023-08-01",
        "endDate": None,
        "ongoing": True,
        "skills": ["Node.js", "MongoDB", "Express"]
    },
    {
        "title": "Heart Disease Prediction",
        "description": "A machine learning project to predict heart disease using Python.",
        "github": "https://github.com/username/heart-disease-prediction",
        "demoType": "script",  # Indicates running a Python script
        "demoContent": "python predict_heart_disease.py --input sample_data.csv",  # CLI command
        "startDate": "2022-06-01",
        "endDate": "2022-08-01",
        "ongoing": False,
        "skills": ["Python", "Machine Learning", "XGBoost"]
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

