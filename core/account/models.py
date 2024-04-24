from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User Model
    """
    email = models.EmailField(max_length=254,unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 


    Token = models.IntegerField(blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class BaseProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    cash_bank = models.IntegerField(default=0)
    
    def __str__(self)-> str:
        return self.user.email+ "//"+self.first_name+ "//" + self.last_name
    

    def full_name(self) -> str:
        return self.first_name +' '+ self.last_name
    
    class Meta:
        abstract = True

class DriverProfile(BaseProfile):
    CARS = (
        ('SAMAND','SAMAND'),
        ("PEUGEOT","PEUGEOT")
    )
    STATUS = (
        ("traveling","traveling"),
        ("No-travel","No-travel")
    )
    photo = models.ImageField()
    car = models.CharField(choices=CARS,max_length=10)
    count_trip = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS,max_length=11)



class CustomerProfile(BaseProfile):
    pass


