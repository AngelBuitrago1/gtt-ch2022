from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

# Esta clase administra como se crean los usuarios en el sistema de autenticación
# e identificar las credenciales
class UserManager(BaseUserManager):
    def create_user(self, username, password = None):
        """
        Crea y guarda un usuario con el username and password.
        """
        if not username:
            raise ValueError('Usuario debe tener un username')
        user = self.model(username = username)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Creación de la entidad User esta tiene dos clase como parametros que permiten 
# crear un modelo de usuario básico con autenticación
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField('Name', max_length = 30)
    last_name = models.CharField('Last Name', max_length = 30)
    email = models.EmailField('Email', max_length = 100)
    username = models.CharField('Username', max_length = 15, unique = True)
    password = models.CharField('Password', max_length = 256)

# Se sobreescibe el metodo save por el atributo password y su hash    
    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

# Se asocia el UserManager al modelo User
    objects = UserManager()
    USERNAME_FIELD = 'username'