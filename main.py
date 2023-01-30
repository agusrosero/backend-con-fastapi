from fastapi import FastAPI
from routers import products

app = FastAPI()

# Routers
app.include_router(products.router)

# iniciar el servidor: uvicorn main:app --reload


@app.get("/")
async def root():  # Siempre que se lo llama al servidor usamos: async
    return "Hello World!"


@app.get("/url")
async def url():
    return {"url_curso": "https://agusdev.com/python"}
