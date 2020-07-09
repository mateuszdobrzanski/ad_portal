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


def product_detail(request, id):
    product = Product.objects.get(id=id)
    template = 'Product/product_detail.html'
    context = {'product_detail': product}

    return render(request, template, context)
