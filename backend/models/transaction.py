from tortoise import fields
from tortoise.models import Model


class Transaction(Model):
    id = fields.IntField(pk=True)

    trans_date_trans_time = fields.CharField(max_length=30)
    cc_num = fields.CharField(max_length=20)
    merchant = fields.CharField(max_length=100)
    category = fields.CharField(max_length=50)
    amt = fields.FloatField()

    first = fields.CharField(max_length=50)
    last = fields.CharField(max_length=50)
    gender = fields.CharField(max_length=1)

    street = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)
    state = fields.CharField(max_length=2)
    zip = fields.IntField()

    lat = fields.FloatField()
    long = fields.FloatField()
    city_pop = fields.IntField()

    job = fields.CharField(max_length=100)
    dob = fields.CharField(max_length=20)

    trans_num = fields.CharField(max_length=100)
    unix_time = fields.BigIntField()

    merch_lat = fields.FloatField()
    merch_long = fields.FloatField()

    is_fraud = fields.BooleanField()

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "transactions"

    def __str__(self):
        return f"Transaction {self.id} - {self.merchant} - Fraud: {self.is_fraud}"
