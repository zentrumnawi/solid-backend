from rest_framework.routers import SimpleRouter

from .views import NestedProfileEndpoint, IdListProfileEndpoint

app_name = "content"
router = SimpleRouter()
router.register(r"profiles", NestedProfileEndpoint, basename="profile")
router.register(r"recursive/profiles", IdListProfileEndpoint, basename="idlist-profile")
urlpatterns = []
urlpatterns += router.urls
