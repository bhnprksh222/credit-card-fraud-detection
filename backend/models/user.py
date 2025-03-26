"""
File Name   : user.py
Author      : Bhanu Prakash Akepogu
Date        : 03/25/2025
Description : This script initializes the user model using tortoise ORM.
Version     : 1.0.0
"""

from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=200)
    firstname = fields.CharField(max_length=100)
    lastname = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "User"
