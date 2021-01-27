from django.contrib import admin

from .models import QuizAnswer, QuizQuestion


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]
    inlines = [QuizAnswerInline]


admin.site.register(QuizQuestion, QuizQuestionAdmin)


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "correct"]


admin.site.register(QuizAnswer, QuizAnswerAdmin)
