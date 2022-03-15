from django.urls import  path
from rest_framework.routers import SimpleRouter

from .views import QuizAnswerEndpoint, QuizQuestionEndpoint, QuizMetaDataEndpoint, QuizSessionEndpoint

app_name = "quiz"
router = SimpleRouter()
router.register(r"quizquestions", QuizQuestionEndpoint)
router.register(r"quizanswers", QuizAnswerEndpoint)
urlpatterns = [
    path("quizmeta", QuizMetaDataEndpoint.as_view()),
    path("quizsession", QuizSessionEndpoint.as_view())
]
urlpatterns += router.urls
