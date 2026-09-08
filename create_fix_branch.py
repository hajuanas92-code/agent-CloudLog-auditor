import os
from datetime import datetime
from dotenv import load_dotenv
from github import Github

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
TARGET_FILE = os.getenv("TARGET_FILE")


def create_branch_with_fix(fixed_code: str, root_cause: str = ""):
    """
    Creates a new branch off the repo's default branch, commits the
    fixed code to the target file on that branch, and returns the
    branch name so it can be used to open a PR next.
    """
    client = Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)

    default_branch = repo.default_branch
    base_ref = repo.get_branch(default_branch)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_branch_name = f"fix/bug-py-auto-fix-{timestamp}"

    repo.create_git_ref(
        ref=f"refs/heads/{new_branch_name}",
        sha=base_ref.commit.sha,
    )

    file_data = repo.get_contents(TARGET_FILE, ref=default_branch)

    repo.update_file(
        path=TARGET_FILE,
        message=f"Auto-fix: {root_cause[:60]}" if root_cause else "Auto-fix applied by Cloud Log Auditor",
        content=fixed_code,
        sha=file_data.sha,
        branch=new_branch_name,
    )

    return new_branch_name


if __name__ == "__main__":
    from logs import get_latest_error_log
    from github_fetch import get_buggy_code
    from diagnose import diagnose_bug
    from extract_fix import extract_fixed_code

    latest_log = get_latest_error_log()
    code = get_buggy_code()
    result = diagnose_bug(
        stack_trace=latest_log.get("stack_trace"),
        code=code,
        filename=TARGET_FILE,
    )
    fixed_code = extract_fixed_code(result)

    branch_name = create_branch_with_fix(fixed_code)
    print("Created branch:", branch_name)