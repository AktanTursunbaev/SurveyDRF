from rest_framework import serializers
from api.models import Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text')
        read_only_fields = ('id',)
        model = Choice
