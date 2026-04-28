from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    user = fields.ForeignKeyField("models.User", related_name="categories", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "categories"
        unique_together = (("name", "user"),)


class Transaction(Model):
    id = fields.IntField(pk=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    description = fields.CharField(max_length=255)
    type = fields.CharField(max_length=7)  # "income" or "expense"
    date = fields.DateField()
    user = fields.ForeignKeyField("models.User", related_name="transactions", on_delete=fields.CASCADE)
    category = fields.ForeignKeyField("models.Category", related_name="transactions", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "transactions"
