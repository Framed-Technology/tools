from api import create_api
import uvicorn

api = create_api()

if __name__ == "__main__":
    uvicorn.run("index:api", reload=True, workers=2)
