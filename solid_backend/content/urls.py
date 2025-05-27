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
    AllNodesFlatEndpoint,
    FlatProfilesEndpoint,
    AncestorsEndpoint,
)

app_name = "content"
router = SimpleRouter()
# router.register(r"profiles", ProfileEndpoint, basename="profile")
router.register(r"root-nodes", RootNodeEndpoint, basename="rootnode")
router.register(r"leaf-nodes", LeavesEndpoint, basename="leafnodes")
router.register(r"parent-node", ParentNodeEndpoint, basename="parentnode")
router.register(r"children", ChildrenEndpoint, basename="children")
router.register(r"profiles", NestedProfileEndpoint, basename="profile-new")
router.register(r"recursive/profiles", IdListProfileEndpoint, basename="idlist-profile")
router.register(r"contentItem", ContentItemEndpoint, basename="content-item")
router.register(r"all-nodes-flat", AllNodesFlatEndpoint, basename="all-nodes-flat")
router.register(r"flat-profiles", FlatProfilesEndpoint, basename="flat-profiles")
router.register(r"ancestors", AncestorsEndpoint, basename="ancestors")
urlpatterns = []
urlpatterns += router.urls
