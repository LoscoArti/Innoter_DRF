from pages.views import FeedViewSet, PageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"page", PageViewSet, basename="pages")
router.register(r"feed", FeedViewSet, basename="feed")

urlpatterns = router.urls
