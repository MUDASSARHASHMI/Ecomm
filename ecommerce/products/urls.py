from django.conf.urls import url, patterns
from django.contrib import admin
from .views import ProductDetailView, ProductListView



urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
]