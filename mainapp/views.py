from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return  same_products



def products(request, pk=None, page=1):
    print(pk)
    title = 'продукты'
    category = ''
    products = ''

    categories = ProductCategory.objects.all()
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {
                'pk': 0,
                'name': 'все'
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category_id__pk=pk).order_by('price')

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
    title = 'страница продута'
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