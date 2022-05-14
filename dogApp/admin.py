from django.contrib import admin
from .models.user import User
from .models.dog import Dog

# Register your models here.
admin.site.register(User)
admin.site.register(Dog)