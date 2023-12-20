from pages.views import PageViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r"pages", PageViewSet, basename="pages")

urlpatterns = router.urls
