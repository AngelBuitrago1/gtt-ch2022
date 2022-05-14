from django.db import models
from .user import User

# Se crea la entidad Dog esta no necesita autenticación
class Dog(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Name dog', max_length = 30)
    picture = models.CharField('Picture Dog', max_length = 100)
    create_date = models.DateTimeField()
    is_adopted = models.BooleanField(default = False)    
    id_user = models.ForeignKey(User, related_name ='dog', on_delete = models.CASCADE)