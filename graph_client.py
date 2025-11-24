"""
graph_client.py

Microsoft Graph client using client credentials loaded from config.json.
"""

import json
import os
from typing import Dict, Any, List, Optional

import requests
from msal import ConfidentialClientApplication

# -------------------------
# Load configuration
# -------------------------

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(
        f"config.json not found. Expected at: {CONFIG_PATH}"
    )

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

TENANT_ID = config.get("tenant_id")
CLIENT_ID = config.get("client_id")
CLIENT_SECRET = config.get("client_secret")
GRAPH_API_URL = config.get("graph_api_url", "https://graph.microsoft.com/v1.0")
TENANT_DOMAIN = config.get("tenant_domain")  # optional

# Validate required fields
missing = [k for k in ["tenant_id", "client_id", "client_secret"] if not config.get(k)]
if missing:
    raise RuntimeError(f"Missing required configuration fields in config.json: {missing}")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

# -------------------------
# Authentication helpers
# -------------------------

def _get_access_token() -> str:
    """
    Authenticate with Azure AD using client credentials from config.json.
    """
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in result:
        raise RuntimeError(
            f"Failed to acquire token: {result.get('error')} - {result.get('error_description')}"
        )

    return result["access_token"]


def _get_headers() -> Dict[str, str]:
    token = _get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

# -------------------------
# Graph request wrappers
# -------------------------

def graph_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{GRAPH_API_URL}{endpoint}"
    headers = _get_headers()
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def graph_post(endpoint: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{GRAPH_API_URL}{endpoint}"
    headers = _get_headers()
    response = requests.post(url, headers=headers, json=json_body)
    response.raise_for_status()
    return response.json()


def graph_delete(endpoint: str) -> None:
    url = f"{GRAPH_API_URL}{endpoint}"
    headers = _get_headers()
    response = requests.delete(url, headers=headers)

    if response.status_code not in (204, 202):
        response.raise_for_status()

# -------------------------
# User helper functions
# -------------------------

def list_users(top: int = 10) -> List[Dict[str, Any]]:
    data = graph_get("/users", params={"$top": top})
    return data.get("value", [])


def search_users(query: str, top: int = 10) -> List[Dict[str, Any]]:
    filter_query = f"startswith(displayName,'{query}') or startswith(mail,'{query}')"
    data = graph_get("/users", params={"$filter": filter_query, "$top": top})
    return data.get("value", [])


def create_user(display_name: str, username: str, password: str) -> Dict[str, Any]:
    """
    Create a user using config.json's tenant_domain if present.
    """
    if not TENANT_DOMAIN:
        raise RuntimeError("tenant_domain missing in config.json")

    upn = f"{username}@{TENANT_DOMAIN}"

    body = {
        "accountEnabled": True,
        "displayName": display_name,
        "mailNickname": username,
        "userPrincipalName": upn,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": password
        }
    }

    return graph_post("/users", body)


def delete_user(user_identifier: str) -> None:
    graph_delete(f"/users/{user_identifier}")
