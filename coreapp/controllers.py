import jwt
from datetime import datetime
from todob.settings import DB
from .constants import collections
from credentials import SECRET_KEY, ALGO
from .utils import create_new_sequential_id

users_collection = DB[collections.get("users")]
todos_collection = DB[collections.get("todos")]


def get_user_by_mobile(mobile):
    """
    get user by mobile number
    :param mobile: mobile number of user
    :return: user object
    """
    user = users_collection.find_one({"mobile": mobile}, {"_id": 0, "created_at": 0, "updated_at": 0, "password": 0})
    return user


def create_user(full_name, mobile, password):
    """
    create a new user
    :param full_name: full name of user
    :param mobile: number of user
    :param password: password
    :return: user object
    """
    id = create_new_sequential_id(users_collection)
    payload = {"password": password}
    encrypted_password = jwt.encode(payload, SECRET_KEY, ALGO)
    users_collection.insert_one({
        "id": id,
        "full_name": full_name,
        "mobile": mobile,
        "password": encrypted_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    user = users_collection.find_one(
        {
            "mobile": mobile, "password": password
        },
        {
            "_id": 0, "createdAt": 0, "updated_at": 0, "password": 0
        }
    )
    return user


def get_user_by_mobile_and_password(mobile, password):
    """
    get user object
    :param mobile: number of user
    :param password: password
    :return: user object
    """
    payload = {"password": password}
    password = jwt.encode(payload, SECRET_KEY, ALGO)
    user = users_collection.find_one({"mobile": mobile, "password": password}, {"_id": 0, "created_at": 0, "updated_at": 0, "password": 0})
    return user


def get_all_todo(user_id):
    """
    get all todo of a particular user bu user_id
    :param user_id: id of user
    :return: user list of todo objects
    """
    todos = list(todos_collection.find({"user_id": user_id}, {"_id": 0}).sort("updated_at", -1))
    return todos


def create_new_todo(user_id, body):
    """
    create a new todo
    :param user_id: id of user
    :param body: content of todo
    :return: todo object
    """
    id = create_new_sequential_id(todos_collection)
    todo = todos_collection.insert_one({
        "id": id,
        "body": body,
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    data = {
        "id": id,
        "user_id": user_id,
        "body": body,
    }
    return data


def update_todo(id, user_id, body):
    """
    update a todo
    :param id: id of todo
    :param user_id: id of user
    :param body: content of todo
    :return: todo object
    """
    todos_collection.update_one(
        {"user_id": user_id, "id": id},
        {"$set": {"body": body}}
    )
    todo = todos_collection.find_one({"id": id}, {"_id": 0})
    return todo

def get_auth_user(user_id):
    """
    get a user object by user_id
    :param user_id: id of user
    :return: user object
    """
    user = users_collection.find_one({"id": user_id}, {"_id": 0, "password":0})
    return user








