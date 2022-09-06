from tortoise.models import Model
from tortoise import fields


class Job(Model):
    # El campo de la llave primaria se crea automáticamente
    # id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()

    def __str__(self):
        return self.name
