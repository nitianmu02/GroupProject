from email.policy import default
from django.db import models

class Wallpaper(models.Model):
    imgId = models.AutoField(primary_key = True, default = 1)
    imagNAME = models.CharField(max_length=200, default='')
    imagSRC = models.CharField(max_length=200, default='')
    imagTAGS = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.imagNAME

class Users(models.Model):
    username = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.username

class Rating(models.Model):
    username = models.CharField(max_length=100, default='')
    imagNAME =models.CharField(max_length=200, default='')
    rating = models.IntegerField(default=0)
    like = models.BooleanField(default=False)
    fav = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class Favorite(models.Model):
    username = models.CharField(max_length=100, default='')
    imagname = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.username

class Photos(models.Model):
    img_name = models.CharField(max_length=200, default='')
    img_src = models.CharField(max_length=200, default='')
    img_tags = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.img_name
