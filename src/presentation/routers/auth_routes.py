from fastapi import APIRouter, Response, Request, HTTPException

from src.application.use_cases.auth.authorizer_use_case import AuthorizerUseCase
from src.application.use_cases.auth.resend_confirmation_code_use_case import ResendConfirmationCodeUseCase
from src.application.use_cases.auth.sign_up_use_case import SignUpUseCase
from src.application.use_cases.auth.sign_in_use_case import SignInUseCase
from src.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from src.infrastructure.adapters.gateways.cognito_auth_gateway import CognitoAuthGateway
from src.presentation.dtos.auth.resend_confirmation_code_dto import ResendConfirmationCodeDTO
from src.presentation.dtos.auth.sign_in_dto import SignInDTO
from src.presentation.dtos.auth.sign_up_dto import SignUpDTO

router = APIRouter()
auth_gateway = CognitoAuthGateway()


@router.post("/register")
async def register(request: SignUpDTO):
    use_case = SignUpUseCase(auth_gateway)
    return use_case.execute(request.email, request.password)


@router.post("/login")
async def login(request: SignInDTO, response: Response):
    use_case = SignInUseCase(auth_gateway)
    auth_result = use_case.execute(request.email, request.password)

    response.set_cookie(key="access_token",
                        value=auth_result.get("access_token"),
                        httponly=True,
                        secure=True,
                        samesite="lax")

    response.set_cookie(key="refresh_token",
                        value=auth_result.get("refresh_token"),
                        httponly=True,
                        secure=True,
                        samesite="lax")
    return {"message": "Login exitoso"}


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")

    if not refresh_token:
        raise HTTPException(status_code=403, detail="No refresh token found")

    if not access_token:
        raise HTTPException(status_code=403, detail="No access token found")

    use_case = RefreshTokenUseCase(auth_gateway)
    auth_result = use_case.execute(refresh_token, access_token)

    response.set_cookie(key="access_token",
                        value=auth_result.get("access_token"),
                        httponly=True,
                        secure=True,
                        samesite="lax")

    return {"message": "Token actualizado"}


@router.post("/confirm")
async def confirm(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Token not found")
    return {"message": "Usuario confirmado"}


@router.get("/authorizer")
async def refresh(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Token not found")

    use_case = AuthorizerUseCase(auth_gateway)

    return use_case.execute(token=access_token)


@router.post("/resend-confirmation-code")
async def resend_confirmation_code(request: ResendConfirmationCodeDTO, response: Response):
    use_case = ResendConfirmationCodeUseCase(auth_gateway)
    auth_result = use_case.execute(request.email)
    return auth_result
