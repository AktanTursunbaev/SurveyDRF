from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Survey, SurveyResponse, Question, QuestionResponse, Choice
from api.models import (
    QuestionTextResponse,
    QuestionSingleChoiceResponse,
    QuestionMultipleChoiceResponse,
)
from .survey import SurveySerializer
from .question_response import QuestionTextResponseSerializer
from .question_response import QuestionSingleChoiceResponseSerializer
from .question_response import QuestionMultipleChoiceResponseSerializer
from .question_response import QuestionResponseSerializer
from .question import QuestionSerializer


def validate_question_response(question_response, survey):
    survey_questions = list(Question.objects.filter(survey=survey))
    question_response_questions = [
        Question.objects.get(pk=i["question"]["id"]) for i in question_response
    ]
    if survey_questions != question_response_questions:
        raise serializers.ValidationError


def create_text_response(question_response, text):
    QuestionTextResponse.objects.create(question_response=question_response, text=text)


def create_single_choice_response(question_response, choice_id):
    choice = Choice.objects.get(pk=choice_id)
    QuestionSingleChoiceResponse.objects.create(
        question_response=question_response, choice=choice
    )


def create_multiple_choice_response(question_response, choices):
    question_multiple_choice_response = QuestionMultipleChoiceResponse.objects.create(
        question_response=question_response
    )
    choices = [Choice.objects.get(pk=i["id"]) for i in choices]
    for choice in choices:
        question_multiple_choice_response.choices.add(choice)


def create_question_responses(question_responses, survey_response):
    for question_response in question_responses:
        question_instance = Question.objects.get(pk=question_response["question"]["id"])
        question_response_instance = QuestionResponse.objects.create(
            question=question_instance, survey_response=survey_response
        )
        if question_instance.type == "text":
            create_text_response(
                question_response_instance,
                question_response["text_response"]["text"],
            )
        elif question_instance.type == "single_choice":
            create_single_choice_response(
                question_response_instance,
                question_response["single_choice_response"]["choice"]["id"],
            )
        elif question_instance.type == "multiple_choice":
            create_multiple_choice_response(
                question_response_instance,
                question_response["multiple_choice_response"]["choices"],
            )


class SurveyResponseSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()
    question_response = QuestionResponseSerializer(many=True)

    class Meta:
        model = SurveyResponse
        fields = ("user", "survey", "question_response")
        read_only_fields = ("user",)

    def create(self, validated_data):
        survey = validated_data.pop("survey")
        survey_instance = Survey.objects.get(pk=self.context["survey_id"])
        user = validated_data.pop("user")
        if not user.is_anonymous:
            survey_response_instance = SurveyResponse.objects.create(
                user=user, survey=survey_instance
            )
        else:
            survey_response_instance = SurveyResponse.objects.create(
                survey=survey_instance
            )
        validate_question_response(self.context["question_response"], survey_instance)
        create_question_responses(
            self.context["question_response"], survey_response_instance
        )
        validated_data["survey"] = survey
        return validated_data
