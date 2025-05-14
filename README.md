# GitHub Pull Request Reviewer

## Description

**GitHub Pull Request Reviewer** is a webhook listener that responds to GitHub pull request events. It uses AI to review code changes and automatically posts a review as a comment on the pull request.

## Features

- Listens for GitHub pull request events (`opened` and `synchronize`)
- Retrieves the pull request diff
- Sends the diff to an AI model for review
- Posts the AI-generated review as a comment on the pull request

## Requirements

- Python 3.x  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Uvicorn](https://www.uvicorn.org/)  
- [Requests](https://docs.python-requests.org/)  
- [OpenAI](https://platform.openai.com/) (if used)  
- [python-dotenv](https://pypi.org/project/python-dotenv/)  
- [Google Generative AI](https://ai.google.dev/)  

## Setup

1. Clone the repository.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your credentials:

   ```env
   GITHUB_TOKEN=your_github_token
   GOOGLE_API_KEY=your_google_genai_api_key
   ```

4. Run the application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10112
   ```

## Usage

1. In your GitHub repository, go to **Settings > Webhooks** and add a new webhook:
   - **Payload URL**: `http://your-server-url/webhook`
   - **Content type**: `application/json`
   - **Events**: Select **Let me select individual events**, and check **Pull requests**

2. Whenever a pull request is **opened** or **synchronized**, the application will:
   - Receive the event
   - Fetch the pull request diff
   - Generate a review using Google Generative AI
   - Post a review comment on the pull request

## Notes

- This project uses the **Google Generative AI API** to generate reviews.
- You need to obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey) and add it to your `.env` file.
