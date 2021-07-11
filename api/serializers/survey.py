from rest_framework import serializers
from api.models import Survey, Question, Choice
from .question import QuestionSerializer


def validate_question_data(question_data):
    for i in question_data:
        if i["type"] != "text" and len(i["choice"]) < 2:
            raise serializers.ValidationError
        elif i["type"] == "text":
            if i["choice"]:
                raise serializers.ValidationError


def save_choice_data(choice_data, question):
    for j in choice_data:
        text = j["text"]
        Choice.objects.create(text=text, question=question)


def save_question_data(question_data, survey):
    for i in question_data:
        title = i["title"]
        type = i["type"]
        question_instance = Question.objects.create(
            title=title, type=type, survey=survey
        )
        if type != "text":
            save_choice_data(i["choice"], question_instance)


class SurveySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = (
            "id",
            "title",
            "start_date",
            "end_date",
            "description",
            "question",
        )
        depth = 2
        read_only_fields = ("id",)

    def create(self, validated_data):
        question_data = validated_data.pop("question")
        validate_question_data(question_data)
        survey_instance = Survey.objects.create(**validated_data)
        save_question_data(question_data, survey_instance)
        validated_data["question"] = question_data
        return validated_data


class SurveyUpdateSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ("title", "start_date", "end_date", "description", "question")
        read_only_fields = ("id", "start_date")

    def update(self, instance, validated_data):
        question_data = validated_data.pop("question")
        validate_question_data(question_data)
        Question.objects.filter(survey=instance).delete()
        save_question_data(question_data, instance)
        instance.title = validated_data.get("title", instance.title)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        validated_data["question"] = question_data
        return validated_data
