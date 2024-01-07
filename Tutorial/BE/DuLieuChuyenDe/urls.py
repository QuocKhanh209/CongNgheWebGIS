from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("du-lieu-diem", views.DiemViewSet)
router.register("du-lieu-duong", views.DuongViewSet)
router.register("du-lieu-vung", views.VungViewSet)

urlpatterns = [
    path("", include(router.urls)),
]