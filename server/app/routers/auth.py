from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from ..schemas import UserRegister, UserLogin, Token, TokenData
from ..services import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
async def register(user: UserRegister):
    existing_user = user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_service.create_user(user.email, user.password)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    authenticated_user = user_service.authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    access_token = auth_service.create_access_token(data={"user_id": authenticated_user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

def verify_access_token(token: str, credentials_exception):
    """Verify access token and return token data"""
    user_id = auth_service.verify_access_token(token)
    if user_id is None:
        raise credentials_exception
    return TokenData(id=user_id)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token_data = verify_access_token(token, credentials_exception)
    user = user_service.get_user_by_id(token_data.id)
    
    if user is None:
        raise credentials_exception
    
    return user