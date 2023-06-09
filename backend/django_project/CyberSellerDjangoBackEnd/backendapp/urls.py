from django.urls import path, re_path
from . import views
from django.views.static import serve
from CyberSellerDjangoBackEnd.settings import IMG_UPLOAD

urlpatterns = [
	path('', views.index, name='index'),
	path(r'signup', views.signup, name='signup'),
	path(r'login', views.login, name='login'),
	path(r'addGoods', views.addGoods, name='addGoods'),
	re_path(r'^img/(?P<path>.*)$', serve, {
		'document_root': IMG_UPLOAD
	}),
	path(r'mainRecommendGoods', views.mainRecommendGoods, name='mainRecommendGoods'),
	path(r'updateShopCart', views.updateShopCart, name='updateShopCart'),
	path(r'getGood', views.getGood, name='getGood'),
	path(r'searchShopCart', views.searchShopCart, name='searchShopCart'),
	path(r'updateStar', views.updateStar, name='updateStar'),
	path(r'getSixPictures', views.getSixPictures, name='getSixPictures'),
	path(r'updateRepo', views.updateRepo, name='updateRepo'),
	path(r'getSellGoods', views.getSellGoods, name='getSellGoods'),
	path(r'goodsRecommendGoods', views.goodsRecommendGoods, name='goodsRecommendGoods'),
	path(r'getStarGoods', views.getStarGoods, name='getStarGoods'),
	path(r'deleteGood', views.deleteGood, name='deleteGood'),
	path(r'analyseExcel', views.analyseExcel, name='analyseExcel'),
	path(r'analyseShopCart', views.analyseShopCart, name='analyseShopCart'),
	path(r'addAddress', views.addAddress, name='addAddress'),
	path(r'addSale', views.addSale, name='addSale'),
	path(r'addSaleGood', views.addSaleGood, name='addSaleGood'),
	path(r'analyseSale', views.analyseSale, name='analyseSale'),
	path(r'getGoodDetail', views.getGoodDetail, name='getGoodDetail'),
	path(r'getAddress', views.getAddress, name='getAddress'),
	path(r'deleteAddress', views.deleteAddress, name='deleteAddress'),
	path(r'updateDefaultAddress', views.updateDefaultAddress, name='updateDefaultAddress'),
	path(r'analyseLike', views.analyseLike, name='analyseLike'),
	path(r'updateShopCartNum', views.updateShopCartNum, name='updateShopCartNum'),
	path(r'analyseOrder', views.analyseOrder, name='analyseOrder'),
	path(r'checked', views.checked, name='checked'),
	path(r'getSale', views.getSale, name='getSale'),
]
