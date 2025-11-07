from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
from utils.gutils.bq_utils import insert_user_to_bigquery
import os

from utils.gutils.connect_to_bg import connect_bigquery

load_dotenv()

app = FastAPI()

# Allow CORS for your frontend (localhost for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expected Google Client ID
GOOGLE_CLIENT_ID = os.getenv("NEXT_PUBLIC_GOOGLE_CLIENT_ID")

class TokenPayload(BaseModel):
    token: str

@app.post("/auth/google")
async def verify_google_token(payload: TokenPayload):
    try:
        # Verify the token using Google's public keys
        idinfo = id_token.verify_oauth2_token(
            payload.token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Extract user info
        user_info = {
            "user_id": idinfo["sub"],
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
        }

        # Save user in BigQuery
        insert_user_to_bigquery(user_info)

        return {"message": "User authenticated", "user": user_info}

    except ValueError as e:
        print("❌ Token verification failed:", e)
        raise HTTPException(status_code=401, detail="Invalid Google token")