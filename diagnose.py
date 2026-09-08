import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def diagnose_bug(stack_trace: str, code: str, filename: str):
    """
    Sends the error's stack trace + the actual source code to Groq,
    asking it to explain the root cause and propose a corrected
    version of the full file.
    """
    prompt = f"""You are a senior software engineer reviewing a production error.

Here is the stack trace from the crash:
{stack_trace}

Here is the full current content of the file that caused it ({filename}):
{code}

Please respond in exactly this format:

ROOT CAUSE:
<a short, clear explanation of why this error happened>

FIXED CODE:
<the complete corrected version of the file, with the bug fixed>

EXPLANATION OF FIX:
<a short explanation of what you changed and why>
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from logs import get_latest_error_log
    from github_fetch import get_buggy_code

    latest_log = get_latest_error_log()
    code = get_buggy_code()

    result = diagnose_bug(
        stack_trace=latest_log.get("stack_trace"),
        code=code,
        filename=os.getenv("TARGET_FILE"),
    )

    print(result)