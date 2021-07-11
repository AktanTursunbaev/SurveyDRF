from rest_framework import serializers
from api.models import QuestionResponse
from api.models import (
    QuestionTextResponse,
    QuestionSingleChoiceResponse,
    QuestionMultipleChoiceResponse,
)
from .question import QuestionSerializer
from .choice import ChoiceSerializer


class QuestionTextResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTextResponse
        fields = ("text",)


class QuestionSingleChoiceResponseSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer()

    class Meta:
        model = QuestionSingleChoiceResponse
        fields = ("choice",)


class QuestionMultipleChoiceResponseSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = QuestionSingleChoiceResponse
        fields = ("choices",)


class QuestionResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    text_response = QuestionTextResponseSerializer(required=False, allow_null=True)
    single_choice_response = QuestionSingleChoiceResponseSerializer(
        required=False, allow_null=True
    )
    multiple_choice_response = QuestionMultipleChoiceResponseSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = QuestionResponse
        fields = (
            "question",
            "text_response",
            "single_choice_response",
            "multiple_choice_response",
        )
