import streamlit as st
from logs import get_latest_error_log
from github_fetch import get_buggy_code
from diagnose import diagnose_bug
from extract_fix import extract_fixed_code, extract_root_cause_and_explanation
from create_fix_branch import create_branch_with_fix
from open_pull_request import open_fix_pull_request
from history import init_db, add_history_entry, get_all_history
import os, difflib

init_db()

def generate_diff(original: str, fixed: str) -> str:
    """
    Compares the original buggy code against the fixed code line-by-line
    and returns a unified diff string (the same format 'git diff' uses),
    which Streamlit can render with red/green highlighting.
    """
    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        fromfile="original",
        tofile="fixed",
        lineterm="",
    )
    return "\n".join(diff)

st.set_page_config(page_title="Cloud Log Auditor", layout="wide")
st.title("Cloud Log Auditor")

st.write(
    "This agent monitors your application's error logs, diagnoses bugs "
    "using AI, and opens a pull request with a proposed fix — with your "
    "approval before anything is written to your repository."
)

col1, col2 = st.columns(2)
with col1:
    st.info(f"**Monitoring GCP project:** {os.getenv('GCP_PROJECT_ID')}")
with col2:
    st.info(f"**Target repository:** {os.getenv('GITHUB_REPO')}")

st.divider()

if st.button("Check for latest error"):
    with st.spinner("Checking Cloud Logging for errors..."):
        latest_log = get_latest_error_log()


    latest_log = get_latest_error_log()

    if latest_log is None:
        st.warning("No error logs found.")
    else:
        st.session_state["latest_log"] = latest_log
        st.success("Error found!")

if "latest_log" in st.session_state:
    st.subheader("Latest Error")
    st.code(st.session_state["latest_log"].get("stack_trace"), language="text")

if "latest_log" in st.session_state:
    if st.button("Diagnose and generate fix"):

      with st.spinner("Fetching code and diagnosing the bug..."):
        code = get_buggy_code()
        result = diagnose_bug(
            stack_trace=st.session_state["latest_log"].get("stack_trace"),
            code=code,
            filename=os.getenv("TARGET_FILE"),
        )
        fixed_code = extract_fixed_code(result)
        root_cause, explanation = extract_root_cause_and_explanation(result)

        st.session_state["fixed_code"] = fixed_code
        st.session_state["root_cause"] = root_cause
        st.session_state["explanation"] = explanation
        st.session_state["original_code"] = code

   
    if "fixed_code" in st.session_state:

        with st.sidebar:
            st.subheader("Code Diff")
            diff_text = generate_diff(
                st.session_state["original_code"],
                st.session_state["fixed_code"],
            )
            st.code(diff_text, language="diff")

        st.subheader("Diagnosis")
        st.write("**Root Cause:**", st.session_state["root_cause"])
        st.write("**Explanation:**", st.session_state["explanation"])

        st.subheader("Proposed Fix")
        st.code(st.session_state["fixed_code"], language="python")

        if st.button("Approve and create Pull Request"):

           with st.spinner("Creating branch and opening pull request..."):
            branch_name = create_branch_with_fix(
                fixed_code=st.session_state["fixed_code"],
                root_cause=st.session_state["root_cause"],
            )

            pr_url = open_fix_pull_request(
                branch_name=branch_name,
                root_cause=st.session_state["root_cause"],
                explanation=st.session_state["explanation"],
                stack_trace=st.session_state["latest_log"].get("stack_trace"),
            )

            add_history_entry(
                root_cause=st.session_state["root_cause"],
                pr_url=pr_url,
            )

            st.session_state["pr_url"] = pr_url

    if "pr_url" in st.session_state:
        st.success("Pull request created!")
        st.markdown(f"[View Pull Request]({st.session_state['pr_url']})")

st.divider()
st.subheader("History")

history = get_all_history()
if not history:
    st.write("No fixes recorded yet.")
else:
    for timestamp, root_cause, pr_url in history:
        st.write(f"**{timestamp}** — {root_cause}")