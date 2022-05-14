from rest_framework import serializers
from dogApp.models.user import User
from dogApp.models.dog import Dog
from dogApp.serializers.dogSerializer import DogSerializer

class UserSerializer(serializers.ModelSerializer):
    dog = DogSerializer()
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'email', 'username', 'password', 'dog']

# Crea un usuario con su perro asociado
    def create(self, validated_data):
        accountData = validated_data.pop('dog')
        userInstance = User.objects.create(**validated_data)
        Dog.objects.create(user=userInstance, **accountData)
        return userInstance

# Muestra las dos entidades gracias al método get del ORM
    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        dog = Dog.objects.get(user=obj.id)
        return {
                'id': user.id,
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'dog': {
                        'id': dog.id,
                        'picture': dog.picture,
                        'create_date': dog.create_date,
                        'is_adopted': dog.is_adopted
                }
        }