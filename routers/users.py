from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# iniciar el servidor: uvicorn users:app --reload

# Entidad users


class User(BaseModel):
    id: int
    name: str  # Lo tipamos para que nos AYUDE a saber de que tipo es.
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="Agustin", surname="Agusdev", url="https://agus.dev", age=22),
    User(id=2, name="Hernan", surname="hdev", url="https://hdev.com", age=30),
    User(id=3, name="Carlos", surname="cardev", url="https://cardev.com", age=28),
]


@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Agustin", "surname": "Agusdev", "url": "https://agus.dev", "age": 22},
        {"name": "Hernan", "surname": "hdev", "url": "https://h.dev", "age": 30},
        {"name": "Jesus", "surname": "Jesusdev", "url": "https://Jesus.dev", "age": 27},
        {"name": "Pablo", "surname": "pablodev", "url": "https://pablo.dev", "age": 29},
        {"name": "Carlos", "surname": "cdev", "url": "https://c.dev", "age": 19},
    ]


@app.get("/users")
async def users():
    return users_list


# Path


@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query


@app.get("/user/")
async def user(id: int):
    return search_user(id)


"""
Mostrar una operacion que nos permita
añadir usuarios.
"""


@app.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user


@app.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    # Si no se encontro el usuario:
    if not found:
        return {"error": "No se ha actualizado ese usario"}
    else:
        return user


@app.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha elminiado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
