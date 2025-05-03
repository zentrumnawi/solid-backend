from rest_framework.routers import SimpleRouter

from .views import (
    ProfileEndpoint,
    RootNodeEndpoint,
    ParentNodeEndpoint,
    ChildrenEndpoint,
    LeavesEndpoint,
)

app_name = "content"
router = SimpleRouter()
router.register(r"profiles", ProfileEndpoint, basename="profile")
router.register(r"root-nodes", RootNodeEndpoint, basename="rootnode")
router.register(r"leaf-nodes", LeavesEndpoint, basename="leafnodes")
router.register(r"parent-node", ParentNodeEndpoint, basename="parentnode")
router.register(r"children", ChildrenEndpoint, basename="children")
urlpatterns = []
urlpatterns += router.urls
