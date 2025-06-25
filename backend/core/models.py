import uuid

from django.db import models


def generate_uuid():
    """
    Function to generate uuid.
    """
    return str(uuid.uuid4())


class BaseUUIDModel(models.Model):
    """
    Model to implement uuid for ids in models.
    All models to inherit from this base model.
    """
    id = models.CharField(
            primary_key=True,
            max_length=36,
            default=generate_uuid,
            editable=False
            )

    class Meta:
        abstract = True
