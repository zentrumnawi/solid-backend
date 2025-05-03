from rest_framework.routers import SimpleRouter

from .views import (
    # ProfileEndpoint,
    RootNodeEndpoint,
    ParentNodeEndpoint,
    ChildrenEndpoint,
    LeavesEndpoint,
    NestedProfileEndpoint,
    IdListProfileEndpoint,
    ContentItemEndpoint,
)

app_name = "content"
router = SimpleRouter()
# router.register(r"profiles", ProfileEndpoint, basename="profile")
router.register(r"root-nodes", RootNodeEndpoint, basename="rootnode")
router.register(r"leaf-nodes", LeavesEndpoint, basename="leafnodes")
router.register(r"parent-node", ParentNodeEndpoint, basename="parentnode")
router.register(r"children", ChildrenEndpoint, basename="children")
router.register(r"profiles-new", NestedProfileEndpoint, basename="profile-new")
router.register(r"recursive/profiles", IdListProfileEndpoint, basename="idlist-profile")
router.register(r"contentItem", ContentItemEndpoint, basename="content-item")
urlpatterns = []
urlpatterns += router.urls
