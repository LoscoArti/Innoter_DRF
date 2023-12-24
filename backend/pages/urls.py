from pages.views import PageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"page", PageViewSet, basename="pages")

urlpatterns = router.urls
