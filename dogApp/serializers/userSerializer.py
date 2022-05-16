from rest_framework import serializers
from dogApp.models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'email', 'username', 'password']

# Crea un usuario con su perro asociado
    def create(self, validated_data):
        userInstance = User.objects.create(**validated_data)
        return userInstance

# Muestra las dos entidades gracias al método get del ORM
    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        return {
                'id': user.id,
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username
        }