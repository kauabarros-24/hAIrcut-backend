from tortoise import models, fields

class ModelMixin:
    import uuid
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
class User(ModelMixin, models.Model):
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=200)
    phone = fields.CharField(max_length=15)

    class Meta:
        table = "users"

    def __str__(self):
        return self.email
