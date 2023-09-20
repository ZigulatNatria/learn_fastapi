from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
import re
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


app = FastAPI(
    title='Hello world'
)


test_users = [
    {'id': 1, 'name': 'user1', 'age': 25},
    {'id': 2, 'name': 'user2', 'age': 35},
    {'id': 3, 'name': 'user3', 'age': 40},
    {'id': 4, 'name': 'user4', 'age': 50},
    {'id': 5, 'name': 'user5', 'age': 20},
]


user_group = [
    {'id': 1, 'name': 'group1', 'users': [{'id': 1}, {'id': 2}]},
    {'id': 2, 'name': 'group2', 'users': [{'id': 3}]},
    {'id': 3, 'name': 'group3', 'users': [{'id': 4}, {'id': 5}]}
]


# class PlayerItem(BaseModel):
#     name: str = Field(re.compile(r"[a-f0-9]"))
#     email: str


class User(BaseModel):
    id: int
    name: str = Query(regex='^[0-9a-f]')
    age: int = Field(ge=18)


@app.get('/user/{user_id}')
def get_user(user_id: int):
    return [user for user in test_users if user.get('id') == user_id]


@app.post('/user/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, test_users))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


@app.post('/users')
def add_user(new_user: List[User]):
    test_users.extend(new_user)
    return {'status': 200, 'data': test_users}


@app.post('/group/')
def add_user_group(group_id: int, user_id: int):
    current_group = list(filter(lambda group: group.get('id') == group_id, user_group))
    current_user = list(filter(lambda user: user.get('id') == user_id, test_users))[0]
    current_group[0]['users'].append(current_user)
    print(current_group)
    return {'status': 200, 'data': current_group}