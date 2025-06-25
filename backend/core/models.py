"""
core/models.py

This module defines abstract base model for resue across this project.
"""
import uuid

from django.db import models


def generate_uuid():
    """
    Function to generate uuid as string.
    """
    return str(uuid.uuid4())


class BaseUUIDModel(models.Model):
    """
    Abstract base model with UUID as primary key, and automatic timestamp
    fields for creation and update.
    """
    id = models.CharField(
            primary_key=True,
            max_length=36,
            default=generate_uuid,
            editable=False
            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
