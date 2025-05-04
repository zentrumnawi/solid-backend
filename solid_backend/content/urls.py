from rest_framework.routers import SimpleRouter

from .views import NestedProfileEndpoint, IdListProfileEndpoint, ContentItemEndpoint

app_name = "content"
router = SimpleRouter()
router.register(r"profiles", NestedProfileEndpoint, basename="profile")
router.register(r"recursive/profiles", IdListProfileEndpoint, basename="idlist-profile")
router.register(r"contentItem", ContentItemEndpoint, basename="content-item")
urlpatterns = []
urlpatterns += router.urls
