from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456",
    },
    "feles": {
        "username": "feles",
        "full_name": "Felipe Acosta",
        "email": "fcosta@mail.com",
        "disable": False,
        "password": "123456789",
    },
    "hgabriel": {
        "username": "hgabriel",
        "full_name": "Antoni Heinze",
        "email": "aheinze@mail.com",
        "disable": True,
        "password": "O987654321!@#",
    },
}


def search_user_db(username: str):
    if username in users_db:  # recuperando el username(usuario)
        return User_DB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticacion invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcto",
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
