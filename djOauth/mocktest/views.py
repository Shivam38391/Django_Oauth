from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets
from .models import Subject, Question, Option
from .serializers import SubjectSerializer, QuestionSerializer, OptionSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subjects to be viewed.
    Each subject includes its nested questions and options.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view questions individually 
    (with their respective options and a separate correct option field).
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list all the options (if needed).
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
