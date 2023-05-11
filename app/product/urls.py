from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

app_name = "product"

router = DefaultRouter()
router.register("", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
