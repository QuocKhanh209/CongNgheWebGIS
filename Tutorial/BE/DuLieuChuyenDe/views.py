from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
from . import models, serializers
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
import re
# Create your views here.

class DiemViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangDiem.objects.all()
    serializer_class = serializers.DiemSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path=r"search")
    def search(self, request):
        query = Q()
        name = request.query_params.get("name")
        mode_filter = True if request.query_params.get("filter_mode") == "1" else False
        if name:
            query &= (
                Q(name__iregex=r"\y%s\y" % re.escape(name))
                if mode_filter
                else Q(name__icontains=name.lower())
            )
        queryset = self.get_queryset().filter(query)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class DuongViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangDuong.objects.all()
    serializer_class = serializers.DuongSerializer

    @action(methods=["GET"], detail=False, url_path=r"search")
    def search(self, request):
        query = Q()
        name = request.query_params.get("name")
        mode_filter = True if request.query_params.get("filter_mode") == "1" else False
        if name:
            query &= (
                Q(name__iregex=r"\y%s\y" % re.escape(name))
                if mode_filter
                else Q(name__icontains=name.lower())
            )
        queryset = self.get_queryset().filter(query)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class VungViewSet(viewsets.ModelViewSet):
    queryset = models.DuLieuDangVung.objects.all()
    serializer_class = serializers.VungSerializer

    @action(methods=["GET"], detail=False, url_path=r"search")
    def search(self, request):
        query = Q()
        name = request.query_params.get("name")
        mode_filter = True if request.query_params.get("filter_mode") == "1" else False
        if name:
            query &= (
                Q(name__iregex=r"\y%s\y" % re.escape(name))
                if mode_filter
                else Q(name__icontains=name.lower())
            )
        queryset = self.get_queryset().filter(query)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

