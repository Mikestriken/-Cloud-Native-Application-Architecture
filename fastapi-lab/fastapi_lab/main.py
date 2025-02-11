# Invoke-RestMethod -Uri "http://127.0.0.1:8000/users/1234"
# Invoke-RestMethod -Uri "http://127.0.0.1:8000/user/" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"ID": 123,"email": "mm@", "username": "mm"}'

from typing import Dict, Any, Union
from fastapi import FastAPI, HTTPException

from fastapi_lab.user import *

app:FastAPI = FastAPI()

itemDB:Dict[int, Dict[str, Any]] = {}
userDB: Dict[int, User] = {}

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello, FastAPI World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int) -> Dict[str, Union[int, float, str]]:
    if int(item_id) in itemDB:
        return itemDB[int(item_id)]
    else:
        raise HTTPException(status_code=404, detail="ITEM NOT FOUND!")

@app.post("/items/")
def create_item(item: Dict[str, Any]) -> Dict[str, Any]:
    if ("ID" not in item):
        raise HTTPException(status_code=400, detail="Item has no 'ID'!")
        
    elif not isinstance(item["ID"], int):
        raise HTTPException(status_code=400, detail="Item's 'ID' is invalid type!")
    
    elif item["ID"] in itemDB:
        raise HTTPException(status_code=400, detail="Item's ID already exists!")
        
    itemDB[item["ID"]] = item
    
    return {"result": "Item created", "item": item}
# ==========================================================================================================
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in userDB:
        return userDB[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found!")

@app.post("/users/")
def create_user(user: Dict[str, Any]):
    if ("ID" not in user):
        raise HTTPException(status_code=400, detail="user has no 'ID'!")
        
    elif not isinstance(user["ID"], int):
        raise HTTPException(status_code=400, detail="user's 'ID' is invalid type!")
    
    elif user["ID"] in userDB:
        raise HTTPException(status_code=400, detail="user's ID already exists!")

    userDB[user["ID"]] = User(
        user["ID"],
        "" if not "email" in user else user["email"],
        "" if not "username" in user else user["username"]
    )
    # userDB[user["ID"]].email = "" if not "email" in user else user["email"]
    # userDB[user["ID"]].username = "" if not "username" in user else user["username"]
    
    return {"result": "User created", "user": user}