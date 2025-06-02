from rest_framework import viewsets
from .models import MainCategory, Subject, Question, Option, TestResult, UserAnswer
from .serializers import (
    MainCategorySerializer, 
    SubjectSerializer, 
    QuestionSerializer, 
    OptionSerializer,
    TestResultSerializer,
    UserAnswerSerializer
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
    queryset = TestResult.objects.all().order_by('-score')
    serializer_class = TestResultSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint to submit and retrieve user answers.
    """
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
