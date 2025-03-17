from fastapi import APIRouter, Response, Request
from src.application.use_cases.auth.sign_up_use_case import SignUpUseCase
from src.application.use_cases.auth.sign_in_use_case import SignInUseCase
from src.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from src.infrastructure.adapters.gateways.cognito_auth_gateway import CognitoAuthGateway

router = APIRouter()
auth_gateway = CognitoAuthGateway()


@router.post("/register")
async def register(data: dict):
    use_case = SignUpUseCase(auth_gateway)
    return use_case.execute(data["email"], data["password"])


@router.post("/login")
async def login(data: dict, response: Response):
    use_case = SignInUseCase(auth_gateway)
    auth_result = use_case.execute(data["email"], data["password"])

    if "error" in auth_result:
        return {"error": auth_result.get("error")}

    response.set_cookie(key="access_token",
                        value=auth_result.get("access_token"),
                        httponly=True,
                        secure=True,
                        samesite="Lax")
    response.set_cookie(key="refresh_token",
                        value=auth_result.get("refresh_token"),
                        httponly=True,
                        secure=True,
                        samesite="Lax")
    return {"message": "Login exitoso"}


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")

    if not refresh_token:
        return {"error": "No refresh token found"}

    if not access_token:
        return {"error": "No access token found"}

    use_case = RefreshTokenUseCase(auth_gateway)
    auth_result = use_case.execute(refresh_token, access_token)

    if "error" in auth_result:
        return {"error": auth_result["error"]}

    response.set_cookie(key="access_token", value=auth_result["access_token"], httponly=True, secure=True, samesite="Lax")
    return {"message": "Token actualizado"}
