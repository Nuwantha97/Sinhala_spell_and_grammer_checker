from fastapi import FastAPI, Response
from app.api.v1.endpoints.ai_inference import router as api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return Response(status_code=200,)