# 1. Importar fastApi
from fastapi import FastAPI
from routers import products, users

# 2. Intanciar fastapi
app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message":"Hola"}

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}


# Documentación Swagger UI: http://127.0.0.1:8000/docs
# Documentación Redocly: http://127.0.0.1:8000/redoc
