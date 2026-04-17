"""Authentication API Routes

Provides user registration, login, and JWT authentication functionality.
"""

from datetime import timedelta, datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt

from ..config import get_settings
from ..db.supabase_client import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"


def _get_secret_key() -> str:
    """Read the SECRET_KEY from application settings."""
    return get_settings().app_secret_key

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# OAuth2 password scheme for extracting Bearer tokens from request headers.
# auto_error=False means no exception when token is absent — returns None
# instead, allowing anonymous access to select endpoints.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


class UserRegister(BaseModel):
    """User registration request body."""
    name: str
    email: EmailStr
    password: str
    role: str = "professor"


class UserLogin(BaseModel):
    """User login request body."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response body."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    """User response body."""
    id: str
    name: str
    email: str
    role: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the given password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload to encode (e.g. {"sub": user_id}).
        expires_delta: Optional custom expiration duration.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    """Extract and validate the JWT token from the request header.

    Designed as a FastAPI dependency. Raises 401 on invalid/expired tokens.
    Returns None when no token is provided (anonymous access).

    Args:
        token: JWT token extracted from the Authorization: Bearer xxx header.

    Returns:
        User info dict with id, name, email, role.
    """
    if token is None:
        # No token provided — allow anonymous access for public endpoints
        return None

    # Validate and decode the JWT token
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    # Look up the user in the database
    db = get_db()
    user = await db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }


async def require_professor(current_user: dict = Depends(get_current_user)) -> dict:
    """Require the current user to hold the professor role.

    Used to protect professor-only endpoints (e.g. reply approval).

    Args:
        current_user: User info obtained via get_current_user dependency.

    Returns:
        Professor user info dict.

    Raises:
        HTTPException: 401 if not logged in, 403 if not a professor.
    """
    if current_user is None:
        raise HTTPException(status_code=401, detail="Login required")
    if current_user["role"] != "professor":
        raise HTTPException(status_code=403, detail="Professor privileges required")
    return current_user


@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister):
    """Register a new user account."""
    db = get_db()

    # Check whether the email is already registered
    existing = await db.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate role value
    if user.role not in ["professor", "student"]:
        raise HTTPException(status_code=400, detail="Role must be 'professor' or 'student'")

    # Create the user record
    password_hash = get_password_hash(user.password)
    created_user = await db.create_user(
        name=user.name,
        email=user.email,
        role=user.role,
        password_hash=password_hash,
    )

    return UserResponse(
        id=created_user["id"],
        name=created_user["name"],
        email=created_user["email"],
        role=created_user["role"],
    )


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Authenticate a user and return a JWT token."""
    db = get_db()

    # Look up the user by email
    db_user = await db.get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Verify the password
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Issue a JWT token
    access_token = create_access_token(
        data={"sub": db_user["id"], "email": db_user["email"], "role": db_user["role"]}
    )

    return Token(
        access_token=access_token,
        user={
            "id": db_user["id"],
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"],
        },
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Login required")
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
    )
