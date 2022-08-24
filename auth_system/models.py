from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from uuid import uuid4
from django.db import transaction
from auth_system.email_handler import new_account


class CustomBaseManager(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        print("custom user called")
        with transaction.atomic():
            user = self.model(email=self.normalize_email(email),**kwargs)
            user.set_password(password)
            u_id = uuid4()
            user.u_id = u_id
            # self.send_custom_email(u_id,self.normalize_email(email))
            new_account(u_id,self.normalize_email(email))
            user.save(using=self._db)
            return user

    def create_superuser(self,email,password=None,**kwargs):
        print("cusomt superuer called")
        with transaction.atomic():
            user = self.model(email=self.normalize_email(email),**kwargs)
            user.set_password(password)
            user.is_staff=True
            user.is_superuser = True
            u_id = uuid4()
            user.u_id = u_id
            self.send_custom_email(u_id,self.normalize_email(email))
            user.save(using=self._db)
            return user




class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=35)
    u_id = models.UUIDField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    account_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'

    objects = CustomBaseManager()


