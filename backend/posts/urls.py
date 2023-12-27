from posts.views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"post", PostViewSet, basename="post")

urlpatterns = router.urls
