from mangum import Mangum
from fastapi import FastAPI
from src.presentation.middlewares.setup_exception_handlers import setup_exception_handlers
from src.presentation.middlewares.standardize_response_middleware import standardize_response
from src.presentation.routers.auth_routes import router as auth_router

app = FastAPI()
setup_exception_handlers(app)
app.middleware("http")(standardize_response)
app.include_router(auth_router, prefix="/v1/auth")

handler = Mangum(app)
