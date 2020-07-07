from django.contrib import admin

from solid_backend.utility.forms import HasImgForm

from .models import QuizAnswer, QuizQuestion


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer


class QuizQuestionAdmin(admin.ModelAdmin):
    form = HasImgForm
    list_display = ["id", "text"]
    inlines = [
        QuizAnswerInline,
    ]


admin.site.register(QuizQuestion, QuizQuestionAdmin)


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "correct"]


admin.site.register(QuizAnswer, QuizAnswerAdmin)
