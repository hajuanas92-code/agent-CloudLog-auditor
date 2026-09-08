import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
TARGET_FILE = os.getenv("TARGET_FILE")


def get_buggy_code():
    """
    Connects to GitHub using the token, opens the configured repo,
    and fetches the raw text content of the configured target file.
    """
    client = Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)

    file_content = repo.get_contents(TARGET_FILE)
    code = file_content.decoded_content.decode("utf-8")

    return code

if __name__ == "__main__":
    code = get_buggy_code()
    print("Fetched code from GitHub:")
    print(code)