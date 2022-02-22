from django.contrib import admin

from .models import QuizAnswer, QuizQuestion
from .forms import QuizAnswerForm


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1
    form = QuizAnswerForm


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]
    inlines = [QuizAnswerInline]

    class Media:
        js = (
            "//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
            "quiz/js/hide_columns.js",
        )


admin.site.register(QuizQuestion, QuizQuestionAdmin)


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "correct"]


admin.site.register(QuizAnswer, QuizAnswerAdmin)
