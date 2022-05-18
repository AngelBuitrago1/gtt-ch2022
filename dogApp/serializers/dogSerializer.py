from dogApp.models.dog import Dog
from rest_framework import serializers

# Con esta clase y sus parametros creo un serializer con la ayuda
# de Django Rest
class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ['name', 'picture', 'create_date', 
                    'is_adopted', 'id_user']  