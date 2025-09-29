from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from settings import settings


security = HTTPBearer()



def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), app_id: str = Header(...)):
    token = credentials.credentials
    response = requests.post(settings.AUTHENTICATION_SERVICE_URL, json={"token": token, "app_id": app_id})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()["sub"]