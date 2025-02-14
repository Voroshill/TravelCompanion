from fastapi import FastAPI
from dotenv import load_dotenv

from app.places.endpoints import router as places_router

load_dotenv()

app = FastAPI()

app.include_router(places_router)


@app.get("/mainpage/")
async def root():
    pass
