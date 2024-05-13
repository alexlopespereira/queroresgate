import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_USER = os.getenv('GITHUB_USER')

def create_issue(issue_title, issue_body):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "title": issue_title,
        "body": issue_body
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response.ok


