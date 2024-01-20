import pytest
from common import JsonReader
from sentiment import MastodonPostman
from pathlib import Path
import requests

def test_return_messages():
    secrets_path = Path("keys/secrets.json")
    secrets_data = JsonReader(secrets_path).read_json()

    # Access the client secret
    client_id = secrets_data["client_id"]
    client_secret = secrets_data["client_secret"]
    access_token = secrets_data["access_token"]
    api_base_url = secrets_data["api_base_url"]

    # Make the GET request
    response = requests.get(api_base_url)
    assert response.status_code == 200

    mastodon = MastodonPostman(client_id,client_secret,access_token,api_base_url)
    data = mastodon.return_messages("caturday")
    # Check if the response contains messages
    assert len(data)>0