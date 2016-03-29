from django.conf.urls import url, patterns
from django.contrib import admin
from .views import CategoryListView



urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category'),
]