from django.db import models
from django.conf import settings

class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def __str__(self):
        return self.name
class Subject(models.Model):
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name="subjects",
        null=True,  # Allow null for now
        blank=True
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        unique_together = (("main_category", "name"),)

    def __str__(self):
        return f"{self.name} ({self.main_category.name if self.main_category else 'No Category'})"


class Question(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    # Marking scheme: +2 for correct answer, -0.5 for an incorrect answer by default.
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

# -------------------------------
# New Model for Test Results
# -------------------------------
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
        return f"{self.user.username} - {self.subject.name} : {self.score}"
