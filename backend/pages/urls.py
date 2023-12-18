from django.urls import path

from .views import PageCreateView, PageRetrieveUpdateDestroyView

urlpatterns = [
    path("pages/", PageCreateView.as_view(), name="page-create"),
    path(
        "pages/<uuid:pk>/",
        PageRetrieveUpdateDestroyView.as_view(),
        name="page-update-delete",
    ),
]
