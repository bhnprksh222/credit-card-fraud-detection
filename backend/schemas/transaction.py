from models.transaction import Transaction
from tortoise.contrib.pydantic import pydantic_model_creator

TransactionOut = pydantic_model_creator(Transaction, name="TransactionOut")
