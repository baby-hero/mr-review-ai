from dotenv import load_dotenv
import os

load_dotenv()

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LIMIT_CHARS = 10000

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

### Pull Request Diff:
---
{diff}
---
Respond only with a detailed review following the 7 steps above. Provide specific feedback on shortcomings, using code examples from the diff to clarify your points.
Note: Try to write the best possible summary. Ensure the review is laser-focused on problems and required improvements.
"""

REVIEW_PROMPT_TEMPLATE_V2 = """
You are a senior software engineer reviewing a GitHub Pull Request.

Please analyze the following code diff and provide feedback in the following structure:

1. **Key Changes**: Summarize the significant changes in logic, functionality, and noteworthy structure.
2. **Code Clarity**: Is the code readable and easy to understand? What improvements could be made to enhance clarity?
3. **Names and Comments**: Are function and variable names clear and accurately describe their purpose? Are comments helpful and do they explain complex parts of the code?
4. **Complexity Reduction**: Are there any complex logic or structures that could be simplified? Suggest alternative approaches if any.
5. **Potential Risks**: Are there any potential bugs, edge cases, or concurrency issues (if applicable) that need consideration?
6. **Best Practices**: Does the code adhere to best practices regarding coding style, error handling, performance, scalability, and security (if relevant)? Suggest improvements with code examples.
7. **Allow Merge Request?**: Should this Pull Request be merged? Answer: Yes / Yes with minor changes / No. Explain why.

### Pull Request Diff:
---
{diff}
---
Respond with a detailed review following the 7 steps above. Be specific, constructive, and provide examples from the code where appropriate to illustrate your points.
Note: Aim to write the best possible summary.
"""

REVIEW_PROMPT_TEMPLATE_V3 = """
You are a senior software engineer reviewing a GitHub Pull Request, focusing on identifying areas for improvement.

Please analyze the following code diff and provide feedback, primarily highlighting what could be better, in the following structure:

1. **Key Issues**: Briefly summarize the main areas of concern or necessary changes.
2. **Clarity Concerns**: Point out specific instances where code readability could be improved.
3. **Naming/Comment Issues**: Identify unclear or misleading names and areas where comments would be beneficial.
4. **Complexity Issues**: Highlight any unnecessarily complex logic or structures.
5. **Potential Bugs/Edge Cases**: Point out any potential bugs or unhandled edge cases.
6. **Best Practice Violations**: Identify instances where best practices are not followed and briefly suggest improvements.
7. **Allow Merge Request?**: Should this be merged? Answer: Yes with mandatory changes / No. Briefly explain why based on the identified issues.

### Pull Request Diff:
---
{diff}
---
Focus on constructive criticism and be specific with examples from the code to illustrate your points. Keep the feedback concise and directly address areas needing improvement.
"""

REVIEW_PROMPT_TEMPLATE_V4 = """
You are a senior software engineer conducting a critical review of a GitHub Pull Request. Your objective is to identify deficiencies, areas needing improvement, and potential risks. Focus your feedback strictly on constructive criticism to ensure the review is concise, direct, and actionable. Avoid positive affirmations.

Please analyze the following code diff and deliver your critical feedback based on these 7 points:

1.  **Key Changes & Potential Impacts**:
    * Briefly summarize only the most significant functional changes.
    * Highlight any changes that could introduce regressions, conflicts, or significantly alter existing behavior.

2.  **Code Clarity Deficiencies**:
    * Pinpoint specific sections of code that are difficult to read, understand, or follow.
    * What makes them unclear (e.g., excessive nesting, overly long methods/functions, obscure logic, "magic" numbers/strings)?
    * Suggest concrete refactoring to improve readability.

3.  **Issues with Comments and Naming**:
    * Identify unclear, misleading, inconsistent, or overly terse/verbose function, variable, and class names.
    * Point out missing comments for complex or non-obvious logic.
    * Flag comments that are outdated, incorrect, redundant (commenting the obvious), or poorly written.

4.  **Unnecessary Complexity & Simplification Failures**:
    * Identify specific logic, algorithms, or data structures that are overly complex for the problem they solve.
    * Point out convoluted control flow or excessive conditional nesting.
    * Suggest specific, simpler alternative approaches or refactoring to reduce complexity.

5.  **Bug Risks & Unhandled Scenarios**:
    * Enumerate potential bugs, logical flaws, off-by-one errors, null/undefined reference issues, or resource mismanagement (e.g., leaks).
    * Identify unhandled edge cases, error conditions, or invalid inputs.
    * If applicable, note potential race conditions or concurrency issues.
    * Highlight any new or exacerbated security vulnerabilities (e.g., XSS, SQL injection, insecure direct object references, data exposure).

6.  **Deviations from Best Practices & Standards**:
    * Identify specific instances where the code violates established software design principles (e.g., SOLID, DRY, KISS), language-specific idioms, or project-defined coding standards/style guides.
    * Point out anti-patterns, hardcoded values that should be configurable, inefficient algorithms/data structures, improper error handling, or poor testability.
    * Suggest improvements with concise code examples where critical for illustration.

7.  **Merge Decision & Mandatory Revisions**:
    * Based *strictly* on the identified issues, should this PR be merged? (Answer: Yes / Yes with minor changes / No).
    * Clearly justify your decision by referencing the critical issues found. If "No" or "Yes with minor changes," list the *minimum* mandatory changes required for approval.

### Pull Request Diff:
---
{diff}
---
Respond *only* with a critical review following the 7 steps above. Be specific, directly address shortcomings, and provide code snippets from the diff to illustrate your concerns. Ensure the review is laser-focused on problems and required improvements.
"""

SIMPLIFIED_FOLLOW_UP_REVIEW_PROMPT_TEMPLATE = """
Please review the following code change (diff-code) provided below. The user has modified the code based on your previous suggestions. Your task is to review it, identify any remaining issues (if any), and required improvements.

You previously gave feedback on the following points:
---
{previous_feedbacks}
---

### Pull Request Diff
——
{diff}
——

Finally, you must always include this section:

**Allow MR to Merge?**: Should this be merged? Answer: Yes / Yes with minor changes / No. Explain why.

Note: Try to provide the best possible summary. Ensure the review is *laser-focused* on problems and required improvements.
"""

def get_llm_review(diff, feedbacks=None, prompt_version=1):
    if feedbacks:
        prompt_final = SIMPLIFIED_FOLLOW_UP_REVIEW_PROMPT_TEMPLATE.format(diff=diff[:LIMIT_CHARS], previous_feedbacks=feedbacks[-LIMIT_CHARS:])
    else:
        match prompt_version:
            case 1:
                prompt_final = REVIEW_PROMPT_TEMPLATE_V1
            case 2:
                prompt_final = REVIEW_PROMPT_TEMPLATE_V2
            case 3:
                prompt_final = REVIEW_PROMPT_TEMPLATE_V3
    
        prompt_final = prompt_final.format(diff=diff[:LIMIT_CHARS])   # truncate if too long
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("prompt_final", prompt_final[:100])

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt_final
    )
    return response.text