from os import environ
from dotenv import load_dotenv

load_dotenv()

CLIENT_DOMAIN = environ.get("CLIENT_DOMAIN", "http://localhost:WXYZ")

CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
]
