from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "chrisapton"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
CACHE_FILE = "contributed_repos.json"

app = Flask(__name__)
CORS(app)
# Sample project data
projects_data = sorted([
    {
        "title": "Personal Website",
        "description": "A personal website to showcase my work. The frontend is in React and the backend is using Flask hosted on Heroku.",
        "github": "https://github.com/chrisapton/chrisapton.github.io",
        "demoType": "link",  # Can be "link", "image", "code", or "script"
        "demoContent": "https://chrisapton.github.io/",  # URL for the demo link
        "startDate": "2025-01-01",
        "endDate": "2025-01-10",
        "ongoing": False,
        "skills": ["React", "HTML", "CSS", "JavaScript", "Flask"]
    },
    {
        "title": "Round Robin Website",
        "description": "Designed and edited a responsive website for a local retail store to improve user experience and showcase products. Performed updates as requested from the owner, including content changes, UI refinements, and SEO optimizations to enhance online visibility. Changed where the website was hosted, reducing costs by 100%.",
        "github": "https://github.com/chrisapton/round_robin",
        "demoType": "link",  
        "demoContent": "https://roundrobinstore.com/", 
        "startDate": "2024-10-01",
        "endDate": "2024-10-30", 
        "ongoing": False,
        "skills": ["HTML", "CSS", "JavaScript"]
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
        "description": "Led the development of an XGBoost model with tuned hyperparameters, leveraging Cross-Validation to predict heart disease. Preprocessed data to improve model performance: Removed outliers and feature engineering. Developed in R. Optimized the model using Randomized Search for hyperparameter tuning achieving a 90% validation accuracy.",
        "github": "https://github.com/chrisapton/Heart-Disease-Prediction",
        "demoType": None,
        "demoContent": None,  
        "startDate": "2022-06-01",
        "endDate": "2022-08-01",
        "ongoing": False,
        "skills": ["R", "Machine Learning", "XGBoost"]
    },
    {
        "title": "Casca Project",
        "description": "This project processes financial documents (e.g., bank statements) to evaluate loan eligibility using OpenAI's GPT-4 model (gpt-4o). The workflow includes converting PDF files into images, organizing them into folders, and analyzing the data using GPT-4 along with a custom text prompt.",
        "github": "https://github.com/chrisapton/CascaProject",
        "demoType": None,
        "demoContent": None,  
        "startDate": "2025-01-13",
        "endDate": "2025-01-14",
        "ongoing": False,
        "skills": ["Python", "OpenAI GPT Models", "Natural Language Processing (NLP)", "pdf2image", "OpenCV", "Prompt Engineering", "Pandas", "Git", "Financial Analysis"]
    },
    {
    "title": "SetupForge",
    "description": "SetupForge is a Windows desktop application built with C++ and wxWidgets that automates software installation and system configuration tasks. It allows users to create, edit, and execute custom installation scripts that can run executable files, move files, create directories, manage environment variables, edit the registry, and map network drives. The application features a user-friendly graphical interface for seamless configuration.",
    "github": "https://github.com/JoeCool16/SetupForge",
    "demoType": "link",
    "demoContent": "https://github.com/JoeCool16/SetupForge/releases/download/v1.0/SetupForge.exe",  
    "startDate": "2025-01-10",
    "endDate": "2025-01-21",
    "ongoing": False,
    "skills": [
        "C++", 
        "wxWidgets", 
        "Windows API", 
        "Batch Scripting", 
        "File System Management", 
        "Registry Editing", 
        "Environment Variable Management", 
        "Git", 
        "Software Deployment"
    ]
}
], key=lambda project: (
    not project["ongoing"],  # Ongoing projects first
    project["endDate"] if project["endDate"] else "9999-12-31"  # Sort by endDate
), reverse=True)  # Newest projects first

def format_date(date_str):
    if not date_str:  # Handle None dates
        return None
    date_obj = datetime.strptime(date_str, "%Y-%m-%d") 
    return date_obj.strftime("%Y-%m-%dT00:00:00Z") 

for project in projects_data:
    project["startDate"] = format_date(project["startDate"])  
    project["endDate"] = format_date(project["endDate"])  



@app.route("/")
def home():
    return "Backend is running!"

# Route to reverse input (example route you had)
@app.route("/run-python-code", methods=["POST"])
def run_python_code():
    input_data = request.json.get("input")
    result = {"output": input_data[::-1]}  # Reverse the input string
    return jsonify(result)

def fetch_starred_repos():
    url = f"https://api.github.com/users/{USERNAME}/starred?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("GitHub API Error:", response.status_code, response.text)
        return []  # fallback to avoid crash
    return [repo for repo in response.json() if not repo.get("private")]

def fetch_owned_public_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?type=owner&per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("GitHub API Error:", response.status_code, response.text)
        return []  # fallback to avoid crash
    
    return [repo for repo in response.json() if not repo.get("private")]

def is_user_a_contributor(owner, name):
    if owner.lower() == USERNAME.lower():
        return True
    url = f"https://api.github.com/repos/{owner}/{name}/contributors"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return False
    contributors = response.json()
    return any(user["login"].lower() == USERNAME.lower() for user in contributors)

def get_commit_dates(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"author": USERNAME, "per_page": 100}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return None, None
    commits = response.json()
    if not commits:
        return None, None
    latest = commits[0]["commit"]["author"]["date"]
    first = commits[-1]["commit"]["author"]["date"]
    return first, latest

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return {repo["title"]: repo for repo in json.load(f)}

def save_cache(data_dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(data_dict.values()), f, indent=2)


@app.route('/repos')
def repos_complete():
    contributed_repos = load_cache()

    starred = fetch_starred_repos()
    owned = fetch_owned_public_repos()
    all_repos = starred + owned

    seen = set()

    for repo in all_repos:
        owner = repo["owner"]["login"]
        name = repo["name"]
        full_name = f"{owner}/{name}"
        url = repo["html_url"]
        pushed_at = repo.get("pushed_at")

        if full_name in seen:
            continue
        seen.add(full_name)

        # Skip if already cached
        if name in contributed_repos:
            continue

        if is_user_a_contributor(owner, name):
            first_commit, last_commit = get_commit_dates(owner, name)

            if not first_commit:
                first_commit = pushed_at
            if not last_commit:
                last_commit = pushed_at
            
            # LLM part to chatgpt to get a description and skills set up from the github link.
            # <TODO>

            contributed_repos[full_name] = {
                "title": name,
                "description": "",
                "github": url,
                "demoType": None,
                "demoContent": None,
                "startDate": first_commit,
                "endDate": pushed_at,
                "ongoing": False,
                "skills": []
            }
        else:
            print(f"Skipped (not a contributor): {full_name}")

    # Save updated cache
    save_cache(contributed_repos)

    # Return sorted list
    sorted_list = sorted(
        contributed_repos.values(),
        key=lambda x: x["endDate"] or "",
        reverse=True
    )

    return jsonify(sorted_list)

# New route to serve project data
@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(projects_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)

