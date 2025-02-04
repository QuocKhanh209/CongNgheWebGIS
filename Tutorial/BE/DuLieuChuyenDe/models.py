from django.contrib.gis.db import models

# Dữ liệu dạng điểm
class DuLieuDangDiem(models.Model):
    class Meta:
        verbose_name = "Dữ liệu dạng điểm"
        default_permissions = ()
        permissions = [
            ("view_Diem", "Xem"),
            ("add_Diem", "Thêm"),
            ("change_Diem", "Sửa"),
            ("delete_Diem", "Xoá"),
        ]
    id = models.AutoField(primary_key=True, verbose_name="Mã điểm")
    name = models.CharField(max_length=100 ,verbose_name="Tên điểm")
    geom = models.PointField(verbose_name="Vị trí", srid=4326, null=True)

#Dữ liệu dạng đường
class DuLieuDangDuong(models.Model):
    class Meta:
        verbose_name = "Dữ liệu dạng đường"
        default_permissions = ()
        permissions = [
            ("view_Duong", "Xem"),
            ("add_Duong", "Thêm"),
            ("change_Duong", "Sửa"),
            ("delete_Duong", "Xoá"),
        ]
    id = models.AutoField(primary_key=True, verbose_name="Mã đường")
    name = models.CharField(max_length=100 ,verbose_name="Tên đường")
    geom = models.LineStringField(verbose_name="Vị trí", srid=4326, null=True)


#Dữ liệu dạng vùng
class DuLieuDangVung(models.Model):
    class Meta:
        verbose_name = "Dữ liệu dạng vùng"
        default_permissions = ()
        permissions = [
            ("view_Vung", "Xem"),
            ("add_Vung", "Thêm"),
            ("change_Vung", "Sửa"),
            ("delete_Vung", "Xoá"),
        ]
    id = models.AutoField(primary_key=True, verbose_name="Mã vùng")
    name = models.CharField(max_length=100 ,verbose_name="Tên vùng")
    geom = models.PolygonField(verbose_name="Vị trí", srid=4326, null=True)

class Model3D(models.Model):
    class Meta:
        verbose_name = "Dữ liệu 3D"
        default_permissions = ()
        permissions = [
            ("view_Model3D", "Xem"),
            ("add_Model3D", "Thêm"),
            ("change_Model3D", "Sửa"),
            ("delete_Model3D", "Xoá"),
        ]
    id = models.AutoField(primary_key=True, verbose_name="Mã model")
    name = models.CharField(max_length=100, verbose_name="Tên model")
    file = models.FileField(upload_to="models/", verbose_name="Đường dẫn file")