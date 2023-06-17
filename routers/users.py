from fastapi import APIRouter, status, HTTPException
from database.models.user import User
from database.schemas.user import user_schema
from services.search_user import search_user

from database.mongodb import mongo_db
from bson import ObjectId

router = APIRouter(prefix="/users", tags="", responses="")

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED) # using status class
async def user(user: User):
    if(type(search_user('name', user.name)) == User):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist!") #using HTTPException

    user_dict = dict(user) # save user
    del user_dict['id'] # delete id field!
    id = mongo_db.users.insert_one(user_dict).inserted_id # insert id

    new_user = user_schema(mongo_db.users.find_one({'_id': id}))

    return User(**new_user)

@router.get('/', response_model=User, status_code=status.HTTP_200_OK)
async def user(id: str):
    return search_user('_id', ObjectId(id))

@router.put('/', response_model=User, status_code=status.HTTP_200_OK)
async def user(user: user):

    user_dict = dict(user)
    del user_dict['id']

    try:
        mongo_db.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in DB!")

    return search_user('_id', ObjectId(user.id))
