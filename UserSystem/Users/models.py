from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from Users.manager import CustomAccountManager


def get_number(value):
    """
        This function return whether the value has digits or not
    """
    if not value.isdigit():
        raise ValidationError("Enter valid phone number")


class UserDerived(AbstractUser):
    """
     Extending the User Model by inheriting AbstractUser Class
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10, unique=True, validators=[get_number])
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    street = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=6, validators=[get_number])
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'date_of_birth']
