from django.contrib import admin

from .models import QuizAnswer, QuizQuestion
from .forms import QuizAnswerFormSet
from solid_backend.media_object.admin import ImageMediaObjectInline


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1
    formset = QuizAnswerFormSet


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]
    inlines = [QuizAnswerInline, ImageMediaObjectInline]
    related_lookup_fields = {
        "generic": [["content_type", "object_id"],],
    }

    class Media:
        js = (
            "//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
            "quiz/js/hide_columns.js",
        )


admin.site.register(QuizQuestion, QuizQuestionAdmin)


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "correct"]


admin.site.register(QuizAnswer, QuizAnswerAdmin)
