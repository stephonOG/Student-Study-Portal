from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)