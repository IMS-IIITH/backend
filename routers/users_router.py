from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ldap_utils import authenticate_user
from utils import create_access_token, check_current_user, get_current_user
from ims_api_utils import get_user_roles

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# User Login Endpoint
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    access_token_ims_app: str = Depends(check_current_user),
):
    if access_token_ims_app:
        response.delete_cookie("access_token_ims_app")

    auth_success, user_data = authenticate_user(form_data.username, form_data.password)
    if not auth_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"set-cookie": ""},
        )

    email = user_data["mail"][0].decode()
    username = user_data["uid"][0].decode()

    # Create Access Token and Set Cookie
    new_access_token = create_access_token(data={"username": username, "email": email})
    response.set_cookie(
        key="access_token_ims_app", value=new_access_token, httponly=True
    )

    return {"message": "Logged In Successfully"}


# User Logout
@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(response: Response, current_user=Depends(check_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not Logged In!")
    response.delete_cookie("access_token_ims_app")
    return {"message": "Logged Out Successfully"}


# Get Current User Endpoint
@router.get("/details", status_code=status.HTTP_200_OK)
async def read_users_me(user_data=Depends(get_current_user)):
    email = user_data["email"]

    role_data = get_user_roles(email)
    return {**user_data, **role_data}
