from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product

from django.views.decorators.cache import cache_page


@cache_page(3600)
def index(request):
    basket = []
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket = Basket.objects.select_related().all()

    title = 'geekshop'
    products = Product.objects.all()[:4]

    context = {
        'products': products,
        'some_name': 'hello',
        'title': title,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    return render(request, 'geekshop/contact.html')
