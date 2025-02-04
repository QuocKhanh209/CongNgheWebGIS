from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("du-lieu-diem", views.DiemViewSet)
router.register("du-lieu-duong", views.DuongViewSet)
router.register("du-lieu-vung", views.VungViewSet)
router.register("model-3d", views.Model3DViewSet)



urlpatterns = [
    path("", include(router.urls)),
]
