from typing import Dict
from mangum import Mangum
from fastapi import FastAPI
from src.presentation.routers.auth_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)

handler = Mangum(app)
