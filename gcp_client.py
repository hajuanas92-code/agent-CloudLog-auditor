import os
import json
import google.cloud.logging
from google.oauth2 import service_account


def get_logging_client():
    """
    Creates a Cloud Logging client that works in two environments:
    1. Locally — using the GOOGLE_APPLICATION_CREDENTIALS file path (gcp-key.json)
    2. On Streamlit Cloud — using credentials pasted into st.secrets, since
       there's no actual file there, only the JSON content as a secret.
    """
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            credentials_dict = dict(st.secrets["gcp_service_account"])
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            project_id = credentials_dict.get("project_id")
            return google.cloud.logging.Client(
                credentials=credentials, project=project_id
            )
    except (ImportError, FileNotFoundError, KeyError):
        pass

    # Fallback: local development, using GOOGLE_APPLICATION_CREDENTIALS file
    return google.cloud.logging.Client()