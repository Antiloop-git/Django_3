from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache

from django.views.decorators.cache import cache_page



def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
        #return Basket.objects.select_related('user')
    else:
        return []


def get_hot_product():
    # products = Product.objects.all()
    # products = Product.objects.select_related().all()
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products



@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'продукты'
    category = ''
    products = ''

    categories = ProductCategory.objects.all()
    basket = get_basket(request.user)
    # basket = Basket.objects.select_related('user')

    if pk is not None:
        if pk == 0:
            # products = Product.objects.all().order_by('price')
            products = get_products_orederd_by_price()

            category = {
                'pk': 0,
                'name': 'все'
            }
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            # products = Product.objects.filter(category_id__pk=pk).order_by('price')
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'title': title,
        'categories': categories,
        'category': category,
        'products': products_paginator,
        'basket': basket,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products_list.html', context=context)


def product(request, pk):
    title = 'продукты'
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'categories': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/product.html', context)

def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter().select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter().select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter().order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter().order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk).order_by('price')
