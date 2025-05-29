from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from dateutil.parser import isoparse
from dateutil.relativedelta import relativedelta
from flask_cors import CORS
from datetime import datetime, timezone
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json
import re
import time

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

USERNAME = "chrisapton"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
CACHE_FILE = "contributed_repos.json"
LAST_RUN_FILE = "last_repos_run.txt"

app = Flask(__name__)
CORS(app)

# Weekly scheduler to check for updates on github
def get_last_run():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE) as f:
            return float(f.read().strip())
    return 0

def set_last_run(ts=None):
    ts = ts or time.time()
    with open(LAST_RUN_FILE, "w") as f:
        f.write(str(ts))

def weekly_repos_update():
    # Only run if it's been > 1 week since last run
    if time.time() - get_last_run() > 7 * 24 * 60 * 60:
        print("Running scheduled weekly repos update...")
        update_repos_cache()
        set_last_run()
    else:
        print("Weekly repo update: Not needed yet.")

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
    latest = commits[0]["commit"]["author"]["date"].split("T")[0]
    first = commits[-1]["commit"]["author"]["date"].split("T")[0]
    return first, latest

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}, []
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
        all_descriptions = [repo.get("description", "") for repo in data if repo.get("description")]
        return {repo["title"]: repo for repo in data}, all_descriptions

def save_cache(data_dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(data_dict.values()), f, indent=2)

def update_repos_cache():
    contributed_repos, all_descriptions = load_cache()
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
            # Check for if there's an updated last commit
            first_commit, last_commit = get_commit_dates(owner, name)

            if not first_commit:
                first_commit = pushed_at.split("T")[0]
            if not last_commit:
                last_commit = pushed_at.split("T")[0]

            if isoparse(last_commit) > isoparse(contributed_repos[name]["endDate"]):
                print("Commit update detected at:", full_name)

                if isoparse(last_commit) - isoparse(contributed_repos[name]["updatedDate"]) > relativedelta(months=6):
                    print("Full update for:", full_name)
                else: 
                    contributed_repos[full_name] = {
                        "title": contributed_repos[name]["title"],
                        "description": contributed_repos[name]["description"],
                        "github": contributed_repos[name]["github"],
                        "demoType": None,
                        "demoContent": None,
                        "startDate": contributed_repos[name]["startDate"],
                        "endDate": last_commit,
                        "ongoing": False,
                        "skills": contributed_repos[name]["skills"],
                        "updatedDate": contributed_repos[name]["updatedDate"]
                    }
                    continue
            else:
                continue

        if is_user_a_contributor(owner, name):
            first_commit, last_commit = get_commit_dates(owner, name)

            if not first_commit:
                first_commit = pushed_at.split("T")[0]
            if not last_commit:
                last_commit = pushed_at.split("T")[0]
            
            # LLM part to chatgpt to get a description and skills set up from the github link.
            client = OpenAI()

            response = client.responses.create(
                model="gpt-4.1",
                tools=[{"type": "web_search_preview"}],
                input=f"""
                Here are prior descriptions. Vary the next one so it sounds more natural.
                {all_descriptions}

                Follow this url {url} and provide a 1 to 2 sentence decription of the project as if 
                it'll go on the projects for my personal website for a student who has a masters in data science. 
                If it's difficult to provide a description then just explain what it contains. Don't say 'challenging 
                to provide a detailed description of the project' since this will be shown on my personal website.

                Provide no other output
                """
            )

            all_descriptions.append(response.output_text)

            def get_github_languages(repo_url):
                owner_repo = '/'.join(repo_url.rstrip('/').split('/')[-2:])
                api_url = f'https://api.github.com/repos/{owner_repo}/languages'
                resp = requests.get(api_url)
                if resp.status_code == 200:
                    return list(resp.json().keys())
                return []

            langs = get_github_languages(url)
            skills_response = client.responses.create(
                model="gpt-4.1",
                tools=[{"type": "web_search_preview"}],
                input=f"""
            Read the content at this URL: {url}

            and project description from {response.output_text}

            also the languages from {langs}

            Identify only the technologies, libraries, and tools that are used in the code or documentation of the project at this URL.
            Return a JSON list of relevant skills as someone would select skills for the project on linkedin. 
            If you cannot identify any technologies, libraries, or tools, return an empty list: [] but ideally we would want around 1 to 6 skills.
            Look into the code of the url and project to find the relavent skills if you can't find any within the code. 
            For big projects there should be at least 1. These skills will be listed under my project description for my website.

            Return only a JSON list (for example: ["Python", "Flask", "React"]), with no other output, text, or code blocks.
            This is so that the skills can be found using match = re.search(r"\[.*?\]", skills_response.output_text, re.DOTALL)
            """
            )

            try:
                match = re.search(r"\[.*?\]", skills_response.output_text, re.DOTALL)
                skills = json.loads(match.group(0)) if match else []
                print(skills)
            except Exception as e:
                print(f"Failed to parse skills JSON: {e}")
                skills = []

            contributed_repos[full_name] = {
                "title": name,
                "description": response.output_text.strip(),
                "github": url,
                "demoType": None,
                "demoContent": None,
                "startDate": first_commit,
                "endDate": last_commit,
                "ongoing": False,
                "skills": skills,
                "updatedDate": datetime.now(timezone.utc).strftime("%Y-%m-%d")
            }
        else:
            print(f"Skipped (not a contributor): {full_name}")

    # Save updated cache
    save_cache(contributed_repos)

# Setup scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='WeeklyReposUpdate', func=weekly_repos_update, trigger='interval', hours=1)  # Checks every hour

@app.route("/")
def home():
    return "Backend is running!"

# Route to reverse input (example route you had)
@app.route("/run-python-code", methods=["POST"])
def run_python_code():
    input_data = request.json.get("input")
    result = {"output": input_data[::-1]}  # Reverse the input string
    return jsonify(result)

@app.route('/repos')
def repos_cached():
    update_repos_cache()
    contributed_repos, _ = load_cache()
    sorted_list = sorted(
        contributed_repos.values(),
        key=lambda x: x["endDate"] or "",
        reverse=True
    )
    return jsonify(sorted_list)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)

