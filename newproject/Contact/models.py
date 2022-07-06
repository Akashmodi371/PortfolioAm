from django.db import models
class contact(models.Model):
    Name=models.CharField(max_length=50)
    Email=models.EmailField()
    Mobile=models.CharField(max_length=12)
    Message=models.TextField()
    Pic=models.ImageField(blank=True, upload_to='blog_images')

    def __str__(self):
        return self.Name



# Create your models here.
