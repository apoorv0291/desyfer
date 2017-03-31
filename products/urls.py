from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from products.views import ProductListView, ProductDetailView, OrderCartDetailView, OrderCartListView,\
    HelloPDFView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^buy/(?P<pk>\d+)/$', OrderCartDetailView.as_view(), name='product_buy'),
    url(r'^buy/(?P<pk>\d+)$', OrderCartDetailView.as_view(), name='product_buy'),
    url(r'^orders/$', OrderCartListView.as_view(), name='orders_list'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^pdf/$',HelloPDFView.as_view(), name='pdf_view'),
    url(r'^$', ProductListView.as_view(), name='products_list'),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)