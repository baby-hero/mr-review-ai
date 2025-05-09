#  pip install fastapi uvicorn requests openai python-dotenv google-generativeai

from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from ai_tools.gemini import get_mr_review

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    event = request.headers.get('X-GitHub-Event')
    payload = await request.json()

    if event == "pull_request" and payload["action"] in ["opened", "synchronize"]:
        pr = payload["pull_request"]
        repo = payload["repository"]
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        pr_number = pr["number"]

        # Get the PR diff
        diff_url = pr["diff_url"]
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        diff = requests.get(diff_url, headers=headers).text

        # Send to AI
        review_text = get_mr_review(diff)

        # Post review to GitHub
        comment_url = f"https://api.github.com/repos/{owner}/{repo_name}/issues/{pr_number}/comments"
        requests.post(comment_url,
                      headers={"Authorization": f"token {GITHUB_TOKEN}"},
                      json={"body": review_text})

        return {"message": "Review posted"}

    return {"message": "Event ignored"}
