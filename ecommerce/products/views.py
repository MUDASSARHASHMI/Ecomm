from django.shortcuts import render
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product

class ProductDetailView(DetailView):
    model = Product

class ProductListView(ListView):
    model = Product
    queryset = Product.object.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        return context
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.object.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) 

            )
        return qs
