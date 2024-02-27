from fastapi import APIRouter
from urllib.request import urlopen
import time


admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/health")
def health():
    return {"time": str(time.time())}

@admin_router.get("/ip")
def get_ip():
    external_ip = urlopen("https://ident.me").read().decode("utf8")
    return {"external_ip": external_ip}