from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

from datetime import date

place_types = (
    #actual,human_read
    ("Country","Country"),
    ("State","State"),
    ("District","District"),
    #beach
    ("Islands","Islands"),
    ("Beach resorts","Beach resorts"),
    ("Secluded beaches","Secluded beaches"),
    #Natural Areas
    ("Mountain","Mountain"),
    ("Forest","Forest"),
    ("Dessert","Dessert"),
    ("Countryside","Countryside"),

    ("Town","Town"),
    ("City","City"),
    ("Winter sport","Winter sport"),
    ("Culture and Heritage","Culture and Heritage"),
    ("Religious","Religious"),
)

#User Model Manager
class UserManager(BaseUserManager):
    def create_user(self, username,email, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not (username or email or password):
            raise ValueError('Error: The User you want to create must have an username,email and password, try again')

        user = self.model(
            username=username,
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email, username, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username=username,
            password=password,
            email=email
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class Accounts(AbstractBaseUser):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25)
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=25)
    dp = models.ImageField(upload_to="user_dp",default=None)
    verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']

    objects = UserManager()

class Places(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    place_name = models.CharField(max_length=50)
    link = models.CharField(max_length=250)
    image = models.ImageField(upload_to="place")
    subject = models.CharField(max_length=25)
    description = models.TextField(max_length=400)
    place_type = models.CharField(choices=place_types,max_length=20)

class Place_map(models.Model):
    pm_id = models.ForeignKey("Places", verbose_name=("M1_place"), on_delete=models.CASCADE,related_name='+')
    spm_id = models.ForeignKey("Places", verbose_name=("S1_place"), on_delete=models.CASCADE)

class Review(models.Model):
    p_id = models.ForeignKey('Places', on_delete=models.CASCADE)
    u_id = models.ForeignKey('Accounts', on_delete=models.CASCADE)
    r_id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=150)
    likes = models.IntegerField(default=0)
    date_uploaded = models.DateField(default=timezone.now)

class Review_pic(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    r_pic = models.ImageField(upload_to='review')

class Review_tag(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    tags = models.CharField(max_length=20)

class Review_like(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    u_id = models.ForeignKey("Accounts", verbose_name=("u_id_FK"), on_delete=models.CASCADE)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)