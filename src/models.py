from tortoise import fields, models
from src.utils import UUIDModel

class User(models.Model, UUIDModel):
    name = fields.CharField(max_length=100)
    email = fields.EmailField(max_lenght=100)
    password = fields.Charfield(max_lenght=200)
    phone = fields.Charfield(max_lenght=15)
    
    