from rest_framework.routers import SimpleRouter

from .views import QuizAnswerEndpoint, QuizQuestionEndpoint

app_name = "quiz"
router = SimpleRouter()
router.register(r"quizquestions", QuizQuestionEndpoint)
router.register(r"quizanswers", QuizAnswerEndpoint)
urlpatterns = []
urlpatterns += router.urls
