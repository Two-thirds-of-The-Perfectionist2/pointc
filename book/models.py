from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .tasks import send_activation_code
# Create your models here

class UserManager(BaseUserManager):
    use_in_migrations = True


    def _create(self, email, password, **kwargs):
        assert email, 'Email is required'

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        send_activation_code.delay(user.email, user.activation_code)

        return user
    
    
    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)
    

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self._create(email, password, **kwargs)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)
    cover = models.ImageField(upload_to='profile_picture')
    is_worker = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def create_activation_code(self):
        from django.utils.crypto import get_random_string


        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOASDFGHJKLZXCVBNM234567890')
        self.activation_code = code
        self.save()
