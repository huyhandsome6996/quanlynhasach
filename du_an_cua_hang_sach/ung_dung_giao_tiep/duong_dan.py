from django.urls import path
from . import xu_ly_yeu_cau
urlpatterns = [path('', xu_ly_yeu_cau.trang_chu, name='trang_chu'),
path('danh-sach', xu_ly_yeu_cau.lay_danh_sach, name='lay_danh_sach'), 
path('them-san-pham', xu_ly_yeu_cau.them_san_pham, name='them_san_pham'), 
path('xoa-san-pham', xu_ly_yeu_cau.xoa_san_pham, name='xoa_san_pham'), 
path('tim-kiem', xu_ly_yeu_cau.tim_kiem_san_pham, name='tim_kiem_san_pham'),
 path('sap-xep', xu_ly_yeu_cau.sap_xep_danh_sach, name='sap_xep_danh_sach')]