from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import MainCategory, Subject, Question, Option, TestResult, UserAnswer

# Inline formset & Inline for Options (unchanged)
class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = 0
        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_correct', False):
                correct_count += 1
        if correct_count != 1:
            raise ValidationError("Each question must have exactly one correct answer.")

class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'subject', 'positive_marks', 'negative_marks', 'correct_answer_display']
    list_filter = ['subject', 'subject__main_category']
    search_fields = ['text', 'subject__name']
    inlines = [OptionInline]

    def correct_answer_display(self, obj):
        option = obj.correct_option()
        return option.text if option else "None"
    correct_answer_display.short_description = "Correct Answer"

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_category']
    prepopulated_fields = {'slug': ('name',)}

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'score', 'computed_rank', 'taken_at']
    list_filter = ['subject', 'taken_at']

    def computed_rank(self, obj):
        higher_count = TestResult.objects.filter(subject=obj.subject, score__gt=obj.score).count()
        return higher_count + 1
    computed_rank.short_description = "Rank"

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['test_result', 'question', 'selected_option', 'answered_at', 'display_is_correct']
    list_filter = ['question', 'selected_option']

    def display_is_correct(self, obj):
        return obj.is_correct
    display_is_correct.short_description = "Correct"

admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
