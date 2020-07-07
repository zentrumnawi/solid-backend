from rest_framework.routers import SimpleRouter

from .views import PhotographEndpoint

app_name = "photograph"
router = SimpleRouter()
router.register(r"photographs", PhotographEndpoint)
urlpatterns = []
urlpatterns += router.urls
