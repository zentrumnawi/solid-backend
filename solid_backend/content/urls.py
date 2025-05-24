from rest_framework.routers import SimpleRouter

from .views import (
    ProfileEndpoint,
    ProfileSearchEndpoint,
)

app_name = "content"
router = SimpleRouter()
router.register(r"profiles", ProfileEndpoint, basename="profile")
router.register(r"profile-search", ProfileSearchEndpoint, basename="profile-search")
urlpatterns = []
urlpatterns += router.urls
