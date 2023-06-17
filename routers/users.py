from fastapi import APIRouter, status, HTTPException
from database.models.user import User
from database.schemas.user import user_schema
from services.search_user import search_user

from database.mongodb import mongo_db

router = APIRouter(prefix="", tags="", responses="")

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if(type(search_user('name', user.name)) == User):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist!")

    user_dict = dict(user) # save user
    del user_dict['id'] # delete 'null' id to empty
    id = mongo_db.users.insert_one(user_dict).inserted_id # insert id

    new_user = user_schema(mongo_db.users.find_one({'_id': id}))

    return User(**new_user)