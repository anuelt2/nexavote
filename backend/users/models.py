"""
users/models.py

This module defines a custom User model that uses email as the unique
identifier for authentication instead of the default username. It also
provides a custom UserManager with methods to create regular users and
superusers.

The model extends Django's AbstractUser.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from core.models import BaseUUIDModel
from election_events.models import ElectionEvent


class UserManager(BaseUserManager):
    """
    Custom manager for the custom User model with email as unique identifier.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseUUIDModel):
    """
    Custom User model extending from AbstractUser that uses email as the
    unique identifier instead of username.
    """
    ROLE_CHOICES = [
            ('voter', 'Voter'),
            ('staff', 'Staff'),
            ('admin', 'Admin'),
            ]

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(
            max_length=10,
            choices=ROLE_CHOICES,
            default='voter',
            )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Return string representation with user email.
        """
        return self.email


class VoterProfile(BaseUUIDModel):
    """
    VoterProfile model linking a user with a unique UUID voter ID.
    """
    user = models.OneToOneField(
            'users.User',
            on_delete=models.CASCADE,
            related_name='voterprofile',
            )
    election_event = models.ForeignKey(
        ElectionEvent,
        on_delete=models.CASCADE,
        related_name='voter_profiles'
    )

    def __str__(self):
        """
        Return string representation with user email and voter ID.
        """
        return f'{self.user.email} - Voter ID: {self.id}'
