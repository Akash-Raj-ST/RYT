from django.db import models

place_types = (
    ("places","Places"),
    ("hilly","Hilly"),
    ("beach","Beach"),
    ("Religious","Religious"),
    ("resort","Resort"),
)

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25)
    user_name = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    dp = models.ImageField(upload_to="user_dp",default=None)


class Places(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    place_name = models.CharField(max_length=50)
    link = models.CharField(max_length=250)
    image = models.ImageField(upload_to="place")
    subject = models.CharField(max_length=50)
    place_type = models.CharField(choices=place_types,max_length=20)

class Place_map(models.Model):
    pm_id = models.ForeignKey("Places", verbose_name=("M1_place"), on_delete=models.CASCADE,related_name='+')
    spm_id = models.ForeignKey("Places", verbose_name=("S1_place"), on_delete=models.CASCADE)

class Review(models.Model):
    p_id = models.ForeignKey('Places', on_delete=models.CASCADE)
    u_id = models.ForeignKey('User', on_delete=models.CASCADE)
    r_id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=150)
    likes = models.IntegerField(default=0)

class Review_pic(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    r_pic = models.ImageField(upload_to='review')

class Review_tag(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    tags = models.CharField(max_length=20)

class Review_like(models.Model):
    r_id = models.ForeignKey("Review", verbose_name=("r_id_FK"), on_delete=models.CASCADE)
    u_id = models.ForeignKey("User", verbose_name=("u_id_FK"), on_delete=models.CASCADE)