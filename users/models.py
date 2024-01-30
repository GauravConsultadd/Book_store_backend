from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

class UserRole(models.TextChoices):
        ADMIN = 'Admin','Administrator'
        BUYER = 'Buyer', 'Buyer'
        SELLER = 'Seller','Salesman'

# custom user manager
class CustomUserManager(BaseUserManager):
    # create buyer
    def create_buyer(self,username, email, password, **extra_fields):
       
        if not username:
            raise ValueError("Username is required")
       
        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        if password is None:
            raise ValueError("Password is required")
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user 
    
    def create_seller(self,username, email, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
       
        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        if password is None:
            raise ValueError("Password is required")
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.role=UserRole.SELLER
        user.save()

        return user

    # create super user 
    def create_superuser(self,username, email, password, **extra_fields):
       
        if not username:
            raise ValueError("Username is required")
       
        if not email:
            raise ValueError("Email address is required")
       
        user = self.model(
            username=username,
            email=email
        )
       
        user.is_superuser = True
        user.is_staff = True
        
        if password is None:
            raise ValueError("Password is required")
        
        user.set_password(password)
        user.role=UserRole.ADMIN
        user.save()
        return user 
    
# user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    role=models.CharField(max_length=20,choices=UserRole.choices,default=UserRole.BUYER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
