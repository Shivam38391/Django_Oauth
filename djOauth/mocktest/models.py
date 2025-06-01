from django.db import models

# Create your models here.



class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='questions'
    )
    text = models.TextField()

    def __str__(self):
        return self.text

    def correct_option(self):
        return self.options.filter(is_correct=True).first()


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options'
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"
