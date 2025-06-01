from rest_framework import viewsets
from .models import MainCategory, Subject, Question, Option, TestResult
from .serializers import (
    MainCategorySerializer, 
    SubjectSerializer, 
    QuestionSerializer, 
    OptionSerializer,
    TestResultSerializer
)

class MainCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class TestResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that provides a list of test results along with the user rank
    (computed relative to other scores for the same subject).
    """
    queryset = TestResult.objects.all().order_by('-score')
    serializer_class = TestResultSerializer
