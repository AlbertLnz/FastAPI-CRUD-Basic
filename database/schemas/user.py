def user_schema(user)->dict:
    return{
        'id': str(user['_id']),
        'name': user['name'],
        'surname': user['surname'],
        'languages': user['languages'],
        'age': user['age'],
    }

def list_all_user_schema(users)->list:
    return [list_all_user_schema(user) for user in users]