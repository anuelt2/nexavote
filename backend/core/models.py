"""
core/models.py

This module defines abstract base model for resue across this project.
"""
import uuid

from django.db import models


def generate_uuid():
    """
    Generate a UUID as a string.
    
    Returns:
        str: A unique UUID string in standard format.
    """
    return str(uuid.uuid4())


class BaseUUIDModel(models.Model):
    """
    Abstract base model with UUID as primary key, and automatic timestamp
    fields for creation and update.
    
    This model provides common fields that all models in the project should have:
    - A UUID primary key for better security and scalability
    - Automatic timestamps for creation and last update
    
    Attributes:
        id (CharField): UUID primary key with maximum length of 36 characters
        created_at (DateTimeField): Timestamp when the record was created
        updated_at (DateTimeField): Timestamp when the record was last updated
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
