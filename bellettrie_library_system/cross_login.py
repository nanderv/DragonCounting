import string
import time
import datetime

import jwt
from django.conf import settings
import random

import sys


class MemberData:
    def __init__(self, name, id, perm_level):
        self.name = name
        self.id = id
        self.perm_level= perm_level


def my_encrypt(member: MemberData) -> str:
    data = {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2), 'name': member.name, 'id': member.id, 'perms':member.perm_level}
    print(data)
    return jwt.encode(data, settings.CROSS_LOGIN_KEY, algorithm="HS256")


def my_decrypt(data: str) -> MemberData:
    data = jwt.decode(data, settings.CROSS_LOGIN_KEY,algorithms=["HS256"])
    return MemberData(data.get('name'), data.get('id'), data.get('perms'))
