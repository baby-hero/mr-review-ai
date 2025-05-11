from dotenv import load_dotenv
import os

load_dotenv()

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

REVIEW_PROMPT_TEMPLATE_V1 = """
You are a senior software engineer reviewing a GitHub Pull Request.

Please analyze the following code diff and give feedback in the following structure:

1. **Key Changes**: Summarize what changed.
2. **Code Clarity**: Is the code readable? What could be improved?
3. **Comments and Naming**: Are function and variable names clear and descriptive?
4. **Complexity Reduction**: Are there complex logic or structures that could be simplified?
5. **Bug Risks**: Any potential bugs or edge cases?
6. **Best Practices**: Are best practices followed? Suggest improvements with code.
7. **Allow MR to Merge?**: Should this be merged? Answer: Yes / Yes with minor changes / No. Explain why.

Code Diff:
---
{diff}
---
Respond only with a detailed review following the 7 steps above. Be specific, constructive, and provide examples from the code where appropriate to illustrate your points.
Note: Try to write the best possible summary
"""

def get_mr_review(diff):
    prompt_final = REVIEW_PROMPT_TEMPLATE_V1.format(diff=diff[:10000])  # truncate if too long

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt_final
    )
    return response.text