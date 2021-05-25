from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Creating a Custom User Model Extending AbstractUser
        It is a new User model that inherit from AbstractUser.
        I am ok with how Django handles the authentication process
        I wouldn’t change anything on it. Yet, I want to add some extra
        information directly in the User model, without having to create
        an extra class.
    """
    picture = models.ImageField(upload_to='Images/', default='Default/placeholder.jpg')

