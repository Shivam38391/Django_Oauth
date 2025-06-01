
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
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Subject, Question, Option

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

class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 4  # Adjust based on how many extra options you wish to display

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'subject', 'correct_answer_display']
    list_filter = ['subject']
    inlines = [OptionInline]

    def correct_answer_display(self, obj):
        option = obj.correct_option()
        return option.text if option else "None"
    correct_answer_display.short_description = "Correct Answer"

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)
