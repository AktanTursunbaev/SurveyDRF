from django.urls import path
from .views import SurveyListView, SurveyCreateView, SurveyDetailView
from .views import SurveyResponseCreateView, SurveyResponseListView

app_name = "api"

urlpatterns = [
    path("survey/list", SurveyListView.as_view(), name="surveys"),
    path("survey/create", SurveyCreateView.as_view(), name="create_survey"),
    path("survey/update/<int:pk>/", SurveyDetailView.as_view(), name="update_survey"),
    path(
        "survey/response/create",
        SurveyResponseCreateView.as_view(),
        name="create_survey_response",
    ),
    path(
        "survey/response/list",
        SurveyResponseListView.as_view(),
        name="survey_responses",
    ),
]
