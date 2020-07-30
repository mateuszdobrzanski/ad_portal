from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, ProductImage, Category
from django.db.models import Count
# for complex search
from django.db.models import Q
from django.shortcuts import get_object_or_404


def product_list(request, category_slug=None):
    category = None

    # retrieve all products and categories
    products = Product.objects.all()

    # in bracket we count the offers and we use 'total_products' var to display no. product in each categories
    categories = Category.objects.annotate(total_products=Count('product'))

    # get category and show products filtered by returned category
    if category_slug:
        # category = Category.objects.get(slug=category_slug)
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # search
    search_query = request.GET.get('q')
    if search_query:
        # print(search_query)
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(condition__icontains=search_query) |
            # bellow, we have relationship between Product model and Brand model,
            # to search 'brand' in field with relationship we should use at first primary model field (brand in Product)
            # and next, we use second model's field (brand_name) in secondary model (Brand)
            Q(brand__brand_name__icontains=search_query)
        )

    # show 2 products per page
    paginator = Paginator(products, 2)
    page = request.GET.get('page')

    products = paginator.get_page(page)
    template = 'Product/product_list.html'
    context = {
        'product_list': products,
        'category_list': categories,
        'category': category,
    }

    return render(request, template, context)


def product_detail(request, product_slug):
    # when we use slug field instead of using "id" we use "slug=" and slug tag
    # product = Product.objects.get(slug=product_slug)
    product = get_object_or_404(Product, slug=product_slug)
    # filter all product images using id
    product_images = ProductImage.objects.filter(product=product)

    print(product.category.slug)

    template = 'Product/product_detail.html'
    context = {'product_detail': product,
               'product_images': product_images}

    return render(request, template, context)


def home(request):
    return render(request,
                  'home.html')
