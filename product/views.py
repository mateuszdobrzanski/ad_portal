from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, ProductImage


def product_list(request):
    # retrieve all products
    products = Product.objects.all()
    # get in console our query list (list of objects from db)
    # print(products)

    template = 'Product/product_list.html'

    # show 2 products per page
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {'product_list': products}

    return render(request, template, context)


def product_detail(request, product_slug):
    # when we use slug field instead of using "id" we use "slug=" and slug tag
    product = Product.objects.get(slug=product_slug)
    # filter all product images using id
    product_images = ProductImage.objects.filter(product=product)

    template = 'Product/product_detail.html'
    context = {'product_detail': product,
               'product_images': product_images}

    return render(request, template, context)


def redirect(request):
    return render(request,
                  'base.html')
