from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
from uuid import uuid4
from src.presentation.dtos.response_dto import SuccessResponse, ErrorResponse

app = FastAPI()


@app.middleware("http")
async def standardize_response(request: Request, call_next):
    response = await call_next(request)
    body_parts = []
    async for chunk in response.body_iterator:
        body_parts.append(chunk)
    body = b''.join(body_parts)
    if 200 <= response.status_code < 300:
        data = json.loads(body.decode())
        standardized_response = SuccessResponse(data=data)
        return JSONResponse(content=standardized_response.dict(), status_code=response.status_code)
    else:

        error_data = json.loads(body.decode())
        error_details = error_data.get("detail", "No detail provided")

        error_response = ErrorResponse(
            error="An error occurred",
            details={"info": error_details},
            responseId=str(uuid4())
        )
        return JSONResponse(content=error_response.dict(), status_code=response.status_code)

