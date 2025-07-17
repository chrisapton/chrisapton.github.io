from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS
from github_repo_updater import update_repos_cache, load_cache
from linkedin_updater import update_linkedin, load_linkedin_cache
import os
import time

app = Flask(__name__)
CORS(app)

LAST_RUN_FILE = "last_repos_run.txt"

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
        update_linkedin()
        set_last_run()
    else:
        print("Weekly repo update: Not needed yet.")

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
    # debugging 
    contributed_repos, _ = load_cache()
    sorted_list = sorted(
        contributed_repos.values(),
        key=lambda x: x["endDate"] or "",
        reverse=True
    )
    return jsonify(sorted_list)

@app.route('/repos/forced')
def repos_forced():
    update_repos_cache()
    contributed_repos, _ = load_cache()
    sorted_list = sorted(
        contributed_repos.values(),
        key=lambda x: x["endDate"] or "",
        reverse=True
    )
    return jsonify(sorted_list)

@app.route('/linkedin/forced')
def linkedin_forced():
    update_linkedin()
    return "Linkedin updated"

@app.route('/linkedin/about')
def linkedin_cached_about():
    data = load_linkedin_cache("about")
    return jsonify(data)

@app.route('/linkedin/experience')
def linkedin_cached_experience():
    data = load_linkedin_cache("experience")
    return jsonify(data)

@app.route('/linkedin/education')
def linkedin_cached_education():
    data = load_linkedin_cache("education")
    return jsonify(data)

@app.route('/linkedin/certifications')
def linkedin_cached_certifications():
    data = load_linkedin_cache("certifications")
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)

