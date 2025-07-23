from unicodedata import category

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from apps.models import Product, Category
class TestTemplateView(TemplateView):
    template_name='apps/base/product_detail.html'



class HomeTemplateView(ListView):
    queryset = Product.objects.select_related('badge').order_by('-created_at')  # To‘g‘ri yozilishi
    template_name = 'apps/home.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['featured_categories'] = Category.objects.filter(featured=True)
        context['parent_categories'] = Category.objects.filter(level=0)
        return context

class CategoryDetailView(DetailView):
    queryset=Category.objects.all()
    template_name='apps/category-list.html'
    slug_url_kwarg = 'slug'

def get_context_data(self,**kwargs):
    context=super().get_context_data(**kwargs)
    category=self.get_object(self.get_queryset())
    tree_id=category.tree_id
    context['products']=Product.objects.filter(category__tree_id=tree_id)
    context['featured_categories']=Product.objects.filter(featured=True)
    context['parent_categories']=Product.objects.filter(level=0)
    context['sub_categories']=Product.objects.filter(tree_id=tree_id ,level=1)
    return context


