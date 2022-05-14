from dogApp.models.dog import Dog
from rest_framework import serializers


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ['name', 'picture', 'create_date', 'is_adopted']