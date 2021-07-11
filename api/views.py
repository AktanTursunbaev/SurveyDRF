from rest_framework import generics, serializers, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.db.models import Q
import datetime
from api.models import Survey, SurveyResponse
from .serializers import (
    SurveySerializer,
    SurveyUpdateSerializer,
    SurveyResponseSerializer,
)


class SurveyListView(generics.ListAPIView):
    query = Q(end_date__gte=datetime.datetime.now()) & Q(
        start_date__lte=datetime.datetime.now()
    )
    queryset = Survey.objects.filter(query)
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SurveyCreateView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = SurveySerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise serializers.ValidationError
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveyUpdateSerializer
    queryset = Survey.objects.all()
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        instance = Survey.objects.get(pk=kwargs["pk"])
        serializer = SurveyUpdateSerializer(instance, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise serializers.ValidationError
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        self.patch(request, *args, **kwargs)


class SurveyResponseListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SurveyResponseSerializer

    def get_queryset(self):
        return SurveyResponse.objects.filter(user=self.request.user)


class SurveyResponseCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyResponseSerializer

    def post(self, request, *args, **kwargs):
        context = {
            "survey_id": request.data["survey"]["id"],
            "question_response": request.data["question_response"],
        }
        serializer = SurveyResponseSerializer(data=request.data, context=context)
        try:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise serializers.ValidationError
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
