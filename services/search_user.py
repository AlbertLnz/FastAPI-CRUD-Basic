from fastapi import FastAPI
from database.mongodb import mongo_db
from database.models.user import User
from database.schemas.user import user_schema

from fastapi.responses import JSONResponse

def search_user(field: str, key): # Associative List search (key can be any value)
    try:
        user = mongo_db.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return JSONResponse({'error': 'User not found'}, status_code=404) #using JSONResponse


def search_user_id(id:str, users_list:list): # searching by id 
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return JSONResponse({'error': 'User not found'}, status_code=404) #using JSONResponse