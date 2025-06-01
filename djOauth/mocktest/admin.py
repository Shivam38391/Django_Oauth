
# # Register your models here.
# from django.contrib import admin
# from django.forms.models import BaseInlineFormSet
# from django.core.exceptions import ValidationError
# from .models import Subject, Question, Option

# class OptionInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         correct_count = 0
#         for form in self.forms:
#             # Skip forms marked for deletion
#             if form.cleaned_data.get('DELETE', False):
#                 continue
#             if form.cleaned_data.get('is_correct', False):
#                 correct_count += 1
#         if correct_count != 1:
#             raise ValidationError("Each question must have exactly one correct answer.")

# class OptionInline(admin.TabularInline):
#     model = Option
#     formset = OptionInlineFormSet
#     extra = 4  # Number of extra option fields to show

# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['text', 'subject' , ""]
#     list_filter = ['subject']
#     inlines = [OptionInline]

# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Subject, SubjectAdmin)
# admin.site.register(Question, QuestionAdmin)


from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import MainCategory, Subject, Question, Option, TestResult

# Inline formset to enforce that each question must have exactly one correct option.
class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = 0
        for form in self.forms:
            # Skip forms marked for deletion
            if form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_correct', False):
                correct_count += 1
        if correct_count != 1:
            raise ValidationError("Each question must have exactly one correct answer.")

# Inline editing of options inside a question.
class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 4  # Adjust the number of extra blank options as needed.

# Admin for the Question model.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'subject', 'positive_marks', 'negative_marks', 'correct_answer_display']
    # list_filter = ['subject',]
    
    list_filter = ['subject', 'subject__main_category']
    search_fields = ['text', 'subject__name']
    inlines = [OptionInline]

    def correct_answer_display(self, obj):
        """
        Displays the text for the correct option.
        """
        option = obj.correct_option()
        return option.text if option else "None"
    correct_answer_display.short_description = "Correct Answer"

# Admin for the Subject model.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_category']
    prepopulated_fields = {'slug': ('name',)}

# Admin for the MainCategory model.
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

# Admin for the TestResult model.
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'score', 'computed_rank', 'taken_at']
    list_filter = ['subject', 'taken_at']

    def computed_rank(self, obj):
        """
        Computes the rank by counting how many other results in the same subject
        have a higher score. Rank 1 means top scorer.
        """
        higher_count = TestResult.objects.filter(subject=obj.subject, score__gt=obj.score).count()
        return higher_count + 1
    computed_rank.short_description = "Rank"

# Registering all models with the admin site.
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)

