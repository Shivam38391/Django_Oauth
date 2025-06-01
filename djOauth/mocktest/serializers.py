from rest_framework import serializers
from .models import Subject, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    # Nest options: each question will include all its options.
    options = OptionSerializer(many=True, read_only=True)
    # Custom field to show the correct option separately.
    correct_option = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'correct_option']

    def get_correct_option(self, obj):
        option = obj.correct_option()  # method defined on your model
        return OptionSerializer(option).data if option else None

class SubjectSerializer(serializers.ModelSerializer):
    # Nest questions so that each subject returns its questions (with options)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'questions']
