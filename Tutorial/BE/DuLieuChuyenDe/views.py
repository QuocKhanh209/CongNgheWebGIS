from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
from . import models, serializers

# Create your views here.

class DiemViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangDiem.objects.all()
    serializer_class = serializers.DiemSerializer

class DuongViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangDuong.objects.all()
    serializer_class = serializers.DuongSerializer

class VungViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangVung.objects.all()
    serializer_class = serializers.VungSerializer
