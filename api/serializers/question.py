from rest_framework import serializers
from api.models import Question, Choice
from .choice import ChoiceSerializer


class QuestionSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer(many=True)

    class Meta:
        fields = ('id', 'title', 'type', 'choice')
        read_only_fields = ('id',)
        model = Question
