from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=10000)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now_add=True)
    # image=models.ImageField(upload_to="img",default=None)

    def __str__(self):
        return self.title

class Images(models.Model):
    blogtitle = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img",default="None")
    def __str__(self):
        return self.blogtitle.title