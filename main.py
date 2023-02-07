from fastapi import FastAPI
from routers import products, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

# Recursos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# iniciar el servidor: uvicorn main:app --reload


@app.get("/")
async def root():  # Siempre que se lo llama al servidor usamos: async
    return "Hello World!"


@app.get("/url")
async def url():
    return {"url_curso": "https://agusdev.com/python"}
