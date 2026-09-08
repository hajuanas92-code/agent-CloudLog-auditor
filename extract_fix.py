import re

def extract_fixed_code(groq_response: str) -> str:
    """
    Finds the 'FIXED CODE:' section, then extracts only the content
    inside the first markdown code fence found within it — ignoring
    any stray formatting (**, ---, etc.) Groq adds around the fence.
    """
    section_pattern = r"FIXED CODE:\s*(.*?)\s*EXPLANATION OF FIX:"
    section_match = re.search(section_pattern, groq_response, re.DOTALL)

    if not section_match:
        return None

    section_text = section_match.group(1)

    # Now find the actual ```...``` fenced block inside that section
    fence_pattern = r"```[a-zA-Z]*\n(.*?)```"
    fence_match = re.search(fence_pattern, section_text, re.DOTALL)

    if fence_match:
        return fence_match.group(1).strip()

    # Fallback: no fence found, just return the raw section, cleaned up
    return section_text.strip().strip("*-").strip()

def extract_root_cause_and_explanation(groq_response: str):
    """
    Pulls out the ROOT CAUSE and EXPLANATION OF FIX sections from
    Groq's structured response, separately from the code block.
    """
    root_cause_match = re.search(
        r"ROOT CAUSE:\s*(.*?)\s*FIXED CODE:", groq_response, re.DOTALL
    )
    explanation_match = re.search(
        r"EXPLANATION OF FIX:\s*(.*)", groq_response, re.DOTALL
    )

    root_cause = root_cause_match.group(1).strip() if root_cause_match else "Unknown"
    explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."

    return root_cause, explanation

if __name__ == "__main__":
    from logs import get_latest_error_log
    from github_fetch import get_buggy_code
    from diagnose import diagnose_bug
    import os

    latest_log = get_latest_error_log()
    code = get_buggy_code()

    result = diagnose_bug(
        stack_trace=latest_log.get("stack_trace"),
        code=code,
        filename=os.getenv("TARGET_FILE"),
    )

    fixed_code = extract_fixed_code(result)
    print("Extracted fixed code:")
    print(fixed_code)