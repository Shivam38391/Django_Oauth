from rest_framework import serializers
from .models import MainCategory, Subject, Question, Option, TestResult

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    correct_option = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 
            'text', 
            'positive_marks', 
            'negative_marks', 
            'options', 
            'correct_option'
        ]

    def get_correct_option(self, obj):
        option = obj.correct_option()  #define in modals.py file
        return OptionSerializer(option).data if option else None

class SubjectSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'questions']

class MainCategorySerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'slug', 'subjects']

class TestResultSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()  # Returns the username via __str__ of the user model.
    subject = serializers.StringRelatedField()  # Returns subject name.

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'subject', 'score', 'taken_at', 'rank']

    def get_rank(self, obj):
        """
        Computes the rank of this TestResult among all results for the same subject.
        It counts how many results in this subject have a higher score.
        """
        higher_count = TestResult.objects.filter(subject=obj.subject, score__gt=obj.score).count()
        return higher_count + 1
