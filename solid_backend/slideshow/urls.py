from rest_framework.routers import SimpleRouter

from .views import SlideshowEndpoint, SlideshowImageEndpoint, SlideshowPageEndpoint, CategoryEndpoint

app_name = "slideshow"
router = SimpleRouter()
router.register(r"slideshows", SlideshowEndpoint)
router.register(r"slideshowpages", SlideshowPageEndpoint)
router.register(r"slideshowimages", SlideshowImageEndpoint)
router.register(r"categories", CategoryEndpoint)
urlpatterns = []
urlpatterns += router.urls
