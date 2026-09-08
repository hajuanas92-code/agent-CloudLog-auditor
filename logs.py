import os
from dotenv import load_dotenv
import google.cloud.logging
from google.cloud.logging_v2 import DESCENDING

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")

client = google.cloud.logging.Client(project=PROJECT_ID)


def get_latest_error_log():
    filter_str = 'logName="projects/%s/logs/buggy-app" AND severity="ERROR"' % PROJECT_ID

    entries = client.list_entries(
        filter_=filter_str,
        order_by=DESCENDING,
        max_results=1,
    )

    for entry in entries:
        return entry.payload  # this will be the dict you logged: message, stack_trace, file

    return None

def main():
    latest = get_latest_error_log()

    if latest is None:
        print("No error logs found.")
        return

    print("Latest error entry found:")
    print("Message:", latest.get("message"))
    print("Stack trace:")
    print(latest.get("stack_trace"))

if __name__ == "__main__":
  main()
