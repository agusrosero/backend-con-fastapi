from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "b76b59e38481bfda5e4ae1b964e40b6e4c47e670418d6e8e4a2358879cfbb9cf"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class User_DB(User):
    password: str


# Array de diferentes usuarios
users_db = {
    "Herdev": {
        "username": "Herdev",
        "full_name": "Hernan Rosero",
        "email": "asd@mail.com",
        "disable": False,
        "password": "$2y$10$s0oR923MoM3UEYhaMIcFXORIhm.V.1uSWIBDWy4XDKO54.rGPqQYu",
    },
    "feles": {
        "username": "feles",
        "full_name": "Felipe Acosta",
        "email": "fcosta@mail.com",
        "disable": False,
        "password": "$2y$10$l8ArWJRhLrYr/HIKrxxII.hzWi5AhM1JfGZCUzy5EuhIjnu4JHWEq",
    },
    "hgabriel": {
        "username": "hgabriel",
        "full_name": "Antoni Heinze",
        "email": "aheinze@mail.com",
        "disable": True,
        "password": "$2y$10$trAYzqTDj7.KMyHqgcpAbOTMqvQLhHMdo5SP4gaFa47qJ2axVm43q",
    },
}


def search_user_db(username: str):
    if username in users_db:  # recuperando el username(usuario)
        return User_DB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcto",
        )

    acces_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
