from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from core.models import BaseUUIDModel


class UserManager(BaseUserManager):
    """
    """
    def create_user(self, email, password=None, **extra_fields):
        """
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
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        """
        return self.email


class VoterProfile(BaseUUIDModel):
    """
    Voter profile model linking a user with a unique UUID voter ID.
    """
    user = models.OneToOneField(
            'users.User',
            on_delete=models.CASCADE,
            related_name='voterprofile',
            )

    def __str__(self):
        """
        Return string representaiton with user email and voter ID.
        """
        return f'{self.user.email} - Voter ID: {self.id}'
