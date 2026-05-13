"""Olympic Games API - Main application entry point."""
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, tokens, countries, athletes, sports, events
from app.seed import seed_database

Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI()
app.include_router(users.router, prefix="/v1")
app.include_router(tokens.router, prefix="/v1")
app.include_router(countries.router, prefix="/v1")
app.include_router(athletes.router, prefix="/v1")
app.include_router(sports.router, prefix="/v1")
app.include_router(events.router, prefix="/v1")


@app.get("/")
def root():
    return {"message": "Welcome to the Olympic Games API"}
