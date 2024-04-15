from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.crypto import get_random_string

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self,email,password,**extra):
        email = self.normalize_email(email)
        user = self.model(email=email,**extra)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,email,password,**extra):
        user = self._create_user(email,password,**extra)
        user.create_activation_code()
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra):
        extra.setdefault('is_active',True)
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra)
    


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code