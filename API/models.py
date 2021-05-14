from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
import jwt
from django.conf import settings

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self,email,name,password,**other_fields):
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        return self.create_user(email,name,password,**other_fields)

class NewUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(gettext_lazy('email address'),unique=True)
    name=models.CharField(max_length=150)
    start_date=models.DateTimeField(default=timezone.now)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects= CustomAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Advisor(models.Model):
    name=models.CharField(max_length=200)
    photo=models.TextField()


class Booking(models.Model):
    user=models.ForeignKey(NewUser,related_name='booking_user',on_delete=models.CASCADE)
    advisor=models.ForeignKey(Advisor,related_name='advisor',on_delete=models.CASCADE)
    date=models.CharField(max_length=200)





