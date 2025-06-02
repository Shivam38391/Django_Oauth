from django.db import models
from django.conf import settings

class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="subjects"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        unique_together = (("main_category", "name"),)

    def __str__(self):
        return f"{self.name} ({self.main_category.name})"

class Question(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    positive_marks = models.FloatField(default=2.0)
    negative_marks = models.FloatField(default=-0.5)

    def __str__(self):
        return self.text

    def correct_option(self):
        """Return the option marked as correct."""
        return self.options.filter(is_correct=True).first()

class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"

# ============================
# Existing TestResult Model
# ============================
class TestResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_results"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="results"
    )
    score = models.FloatField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}: {self.score}"

# ============================
# New Model: UserAnswer
# ============================
class UserAnswer(models.Model):
    test_result = models.ForeignKey(
        TestResult, on_delete=models.CASCADE, related_name='user_answers'
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='user_answers'
    )
    selected_option = models.ForeignKey(
        Option, on_delete=models.SET_NULL, null=True, blank=True
    )
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to '{self.question.text}' by {self.test_result.user.username}"

    @property
    def is_correct(self):
        """
        Returns True if the selected option is the correct one.
        If no option was selected, returns False.
        """
        return bool(self.selected_option and self.selected_option.is_correct)
