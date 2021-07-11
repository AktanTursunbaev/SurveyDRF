from django.db import models
from django.conf import settings


class Survey(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = "survey"
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("text", "Ответ текстом"),
        ("single_choice", "Ответ с выбором одного варианта"),
        ("multiple_choice", "Ответ с выбором нескольких вариантов"),
    ]

    title = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(
        choices=QUESTION_TYPES,
        default=QUESTION_TYPES[0][0],
        max_length=15,
        null=False,
        blank=False,
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="question",
        verbose_name="Опрос",
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "question"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="choice",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    text = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = "choice"
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="survey_response",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    survey = models.ForeignKey(
        Survey,
        related_name="response",
        verbose_name="Опрос",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "survey_response"
        verbose_name = "Ответ на опрос"
        verbose_name_plural = "Ответы на опросы"


class QuestionResponse(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="response",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    survey_response = models.ForeignKey(
        SurveyResponse,
        related_name="question_response",
        verbose_name="Ответ на опрос",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "question_response"
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class QuestionTextResponse(models.Model):
    question_response = models.OneToOneField(
        QuestionResponse,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="text_response",
        verbose_name="Ответ на вопрос",
    )
    text = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = "question_text_response"
        verbose_name = "Ответ текстом"
        verbose_name_plural = "Ответы текстом"


class QuestionSingleChoiceResponse(models.Model):
    question_response = models.OneToOneField(
        QuestionResponse,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="single_choice_response",
        verbose_name="Ответ на вопрос",
    )
    choice = models.ForeignKey(
        Choice,
        related_name="response",
        verbose_name="Вариант ответа",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "question_single_choice_response"
        verbose_name = "Ответ с выбором одного варианта"
        verbose_name_plural = "Ответы с выбором одного варианта"


class QuestionMultipleChoiceResponse(models.Model):
    question_response = models.OneToOneField(
        QuestionResponse,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="multiple_choice_response",
        verbose_name="Ответ на вопрос",
    )
    choices = models.ManyToManyField(
        Choice, related_name="responses", verbose_name="Вариант ответа"
    )

    class Meta:
        db_table = "question_multiple_choice_response"
        verbose_name = "Ответ с выбором нескольких вариантов"
        verbose_name_plural = "Ответы с выбором нескольких вариантов"
