from django.contrib import admin
from contact.models import contact

class contactadmin(admin.ModelAdmin):
    list_display=('Name','Email','Mobile','Message')

admin.site.register(contact,contactadmin)
# Register your models here.
