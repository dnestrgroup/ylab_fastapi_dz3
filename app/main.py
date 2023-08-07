from fastapi import FastAPI

from app.router import setup_routes

app = FastAPI()
setup_routes(app=app)
