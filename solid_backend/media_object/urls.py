from rest_framework.routers import SimpleRouter

from .views import MediaObjectEndpoint

app_name = "photograph"
router = SimpleRouter()
router.register(r"media_objects", MediaObjectEndpoint)
urlpatterns = []
urlpatterns += router.urls
