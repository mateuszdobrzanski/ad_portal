from django.shortcuts import render
from .models import Product


def product_list(request):
    # retrieve all products
    products = Product.objects.all()
    # get in console our query list (list of objects from db)
    # print(products)

    template = 'Product/product_list.html'

    context = {'product_list': products}

    return render(request, template, context)


def product_detail(request, product_slug):
    # when we use slug field instead of using "id" we use "slug=" and slug tag
    product = Product.objects.get(slug=product_slug)
    template = 'Product/product_detail.html'
    context = {'product_detail': product}

    return render(request, template, context)


def redirect(request):
    return render(request,
                  'base.html')
