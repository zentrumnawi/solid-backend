from rest_framework.routers import SimpleRouter

from .views import ProfileEndpoint

app_name = "content"
router = SimpleRouter()
router.register(r"profiles", ProfileEndpoint, basename="profile")
urlpatterns = []
urlpatterns += router.urls
