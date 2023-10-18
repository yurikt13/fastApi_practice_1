from fastapi import APIRouter, HTTPException
# HTTPException para una excepción
from pydantic import BaseModel

router = APIRouter()

# Definir entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
            User(id=1, name="Yuri", surname="yuta", age=19),
            User(id=2, name="Valentina", surname="valen", age=15),
            User(id=3, name="Daniela", surname="dani",age=25)
        ]

# No hacerlo así con json
@router.get("/usersjson")
async def usersjson():
    return [
        {"id":1, "name" : "Yuri", "surname": "yuta", "age": 19},
        {"id":2, "name" : "Valentina", "surname": "valen", "age": 15},
        {"id":3, "name" : "Daniela", "surname": "dani", "age": 25}
        ]

# Hacerlo así con la clase
@router.get("/users")
async def users():
    return users_list

# Llamada mediante parámetros por path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Llamada mediante parámetros por query
@router.get("/user/")
async def user(id: int, name: str):
    return search_user(id)
# ejemplo: http://127.0.0.1:8000/user/?id=1&name=Yuri


@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail = "El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):

    found = False #variable para controlar si he actualizado el usuario o no

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        return {"message": "No se ha eliminado el usuario"}
    else: 
        return {"message": "Se ha eliminado el usuario"}

# Función q busca el usuario según id
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": f"El usuario con id {id} no existe"}
    
