from tkinter import Image
from django.contrib import admin
from .models import Blog,Images


# admin.site.register(Blog)
@admin.register(Blog)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','author','title','created_on')


# admin.site.register(Images)
@admin.register(Images)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','blogtitle','image')