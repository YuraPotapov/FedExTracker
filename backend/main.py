from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from datetime import datetime, timedelta
import os

app = FastAPI()

# in a real project, I would use saving and reading from the database
access_token = None
expires_at = None


async def get_access_token() -> str:
    global access_token, expires_at

    if access_token and expires_at and expires_at > datetime.now():
        return access_token

    # Obtain the required credentials from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if client_id is None or client_secret is None:
        raise HTTPException(status_code=500, detail="Client credentials not found")

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    # Construct the request payload
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # Make a POST request to the authorization URL
    async with AsyncClient() as client:
        response = await client.post("https://apis-sandbox.fedex.com/oauth/token", data=payload, headers=headers)

    # Check the response status
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve access token")

    # Parse the response JSON and extract the access token/expires
    response_json = response.json()
    access_token = response_json.get("access_token")
    expires_in_sec = response_json.get("expires_in")

    if access_token is None or expires_in_sec is None:
        raise HTTPException(status_code=500, detail="Access token not found")

    expires_at = datetime.now() + timedelta(seconds=expires_in_sec)

    return access_token


@app.get("/track/{tracking_number}")
async def track_package(tracking_number: str):
    # Retrieve the access token
    access_token = await get_access_token()

    # Add the access token to the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-locale": "en_US",
    }
    url = "https://apis-sandbox.fedex.com/track/v1/"
    payload = {
        "includeDetailedScans": True,
        "trackingInfo": [
            {
                "trackingNumberInfo":
                    {
                        "trackingNumber": tracking_number
                    }
            }
        ],
    }
    # Make API call to FedEx
    async with AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)

    # Check the response status
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve tracking information")

    return response.json()