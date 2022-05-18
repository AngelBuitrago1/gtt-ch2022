from rest_framework import serializers
from dogApp.models.user import User

# Con esta clase y sus parametros creo un serializer 
# con la ayuda de Django Rest
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'email',
                    'username', 'password']

# Crea un usuario validando los campos solicitados en 
# la subclase META
    def create(self, validated_data):
        userInstance = User.objects.create(**validated_data)
        return userInstance

# Muestra la entidad gracias al método get del ORM
    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        return {
                'id': user.id,
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username
        }