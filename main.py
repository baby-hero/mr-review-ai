from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from ai_tools.gemini import get_llm_review
from utils import github_util
from utils import file_util
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    try:
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

            file_name = f"{repo_name}-{pr_number}"
            feedback = file_util.get_data(file_name)
            # Send to AI
            review_text = get_llm_review(diff, feedback)
            if review_text:
                if feedback:
                    data_file = f"NEXT Round Review:\n {review_text}\n"
                else:
                    data_file = f"FIRST Round Review:\n {review_text}\n"
                file_util.save_data(data_file, file_name)

            # Post review to GitHub
            result = github_util.post_comment_to_pr(owner, repo_name, pr_number, review_text)
            if result.status_code >= 200 and result.status_code < 300:
                return {"message": "Review posted"}
            else:
                return {"message": f"Failed to post review: {result.text}"}

        return {"message": "Event ignored"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}
