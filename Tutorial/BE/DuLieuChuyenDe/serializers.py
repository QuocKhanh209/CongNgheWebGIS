from rest_framework import serializers as serializers
from rest_framework_gis import serializers as serializers_gis
from . import models

class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        if self.serializer is not None and not issubclass(
            self.serializer, serializers.Serializer
        ):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)

#Dữ liệu dạng điểm
class DiemSerializer(serializers_gis.GeoFeatureModelSerializer):
    class Meta:
        model = models.DuLieuDangDiem
        fields = "__all__"
        geo_field = "geom"
        read_only_fields = ["id"]

    def create(self, validated_data):
        newIns = models.DuLieuDangDiem.objects.create(**validated_data)
        return newIns
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

#Dữ liệu dạng đường    
class DuongSerializer(serializers_gis.GeoFeatureModelSerializer):
    class Meta:
        model = models.DuLieuDangDuong
        fields = "__all__"
        geo_field = "geom"
        read_only_fields = ["id"]

    def create(self, validated_data):
        newIns = models.DuLieuDangDuong.objects.create(**validated_data)
        return newIns


#Dữ liệu dạng vùng    
class VungSerializer(serializers_gis.GeoFeatureModelSerializer):
    class Meta:
        model = models.DuLieuDangVung
        fields = "__all__"
        geo_field = "geom"
        read_only_fields = ["id"]

    def create(self, validated_data):
        newIns = models.DuLieuDangVung.objects.create(**validated_data)
        return newIns
    
class Model3DSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model3D
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        newIns = models.Model3D.objects.create(**validated_data)
        return newIns
