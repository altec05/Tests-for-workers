from django.contrib import admin
from .models import *


class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', )
    list_display_links = ('category_name',)
    search_fields = ('category_name',)
    fields = ('category_name',)


class TestQuestionInline(admin.StackedInline):
    model = Question
    show_change_link = True
    extra = 0


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class TestAdmin(admin.ModelAdmin):
    inlines = [TestQuestionInline, ]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'category', 'author', 'created_at', 'updated_at', 'visibility')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('category', 'author', 'visibility')
    readonly_fields = ('created_at', 'author', 'updated_at')
    fields = ('name', 'slug', 'category', 'author', 'created_at', 'updated_at', 'visibility')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('test', 'question_text', 'qtype', 'visibility')
    list_display_links = ('test', 'question_text')
    search_fields = ('question_text',)
    list_filter = ('test', 'visibility')
    fields = ('test', 'question_text', 'qtype', 'visibility')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    list_display_links = ('answer_text',)
    search_fields = ('answer_text',)
    list_filter = ('question',)
    fields = ('question', 'answer_text', 'is_correct')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')
    list_display_links = ('user',)
    search_fields = ()
    list_filter = ()
    fields = ('user', 'question', 'answer')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'user', 'correct', 'wrong')
    list_display_links = ('test',)
    search_fields = ()
    list_filter = ('test', 'user')
    fields = ('test', 'user', 'correct', 'wrong')


admin.site.register(TestCategory, TestCategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Result, ResultAdmin)
