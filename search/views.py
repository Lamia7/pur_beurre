from django.shortcuts import render
from django.db.models import Count

from .forms import MainSearchForm
from .models import Product, Category


def home(request):
    main_search_form = MainSearchForm()  # instanciate form
    context = {
        "main_search_form": main_search_form,  # key: variables we access from template
    }
    return render(request, 'search/home.html', context)


def products(request):
    if request.method == "POST":
        # get the value of name="" from template
        product_search = request.POST['product_search']
        # products = query made to DB
        # query: max 6 pdcts where name contains value of product_search normalized as in feed_db.py
        products = Product.objects.all().filter(
            name__contains=product_search.strip().lower().capitalize())[:6]
        context = {
            # title in HTML will contain value of product_search
            'title': product_search,
            'products': products,
        }
        # send context to products.html template and render this template
        return render(request, "search/products.html", context)


def product(request, product_id):
    # try:
    product = Product.objects.get(pk=product_id)
    context = {'product': product}
    # except Product.DoesNotExist:
    return render(request, 'search/product.html', context)


def substitutes(request, product_id):

    # Find product searched by user with id
    product_query = Product.objects.get(pk=product_id)

    # Find categories of the searched_product
    product_query_cat = Category.objects.filter(product__id=product_query.id)

    # Find max 9 substitutes with better nutriscore and at least 3 categories in common
    substitutes = Product.objects.filter(categories__in=product_query_cat).annotate(nb_cat=Count(
        "categories")).filter(nb_cat__gte=3).filter(nutriscore__lt=product_query.nutriscore).order_by("nutriscore")[:9]

    context = {
        'product': product_query,
        'substitutes': substitutes
    }

    return render(request, 'search/substitutes.html', context)
