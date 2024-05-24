from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from django.utils import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from birthday import BirthdayField, BirthdayManager
# from management import models


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,identification_number, password, **extra_fields):
        print('__manager create user', email, )
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            identification_number=identification_number,
            **extra_fields
        )
        print('_create-----',password)
        user.set_password(password)
        print('_create-----',user)
        user.save(using=self._db)
        return user

    def create_user(self,email,identification_number, password=None, **extra_fields):
        print('manager create user',email,)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, identification_number, password, **extra_fields)

    def create_superuser(self, email,identification_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,identification_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(unique=True)
    identification_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['identification_number']

    objects = AccountManager()

class Profile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    filled = models.BooleanField(default=False)
    objects = models.Manager()
    birthday = BirthdayField(null=True, blank=True)
    birthday = BirthdayManager()
