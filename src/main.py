from fastapi import FastAPI
import scraper as _scraper

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to this Rewe® API"}

@app.get("/offers")
async def offers(searchTerm: str):
    return _scraper.offers(searchTerm)