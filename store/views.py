from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Slider, Category

# Create your views here.
def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return render(
        request, 'index.html',
        {
            'products':products,
            'slides':slides
        }
    )

def product(request, pid):
    product = Product.objects.get(pk=pid)
    return render(
        request, 'product.html',
        {
            'product':product
        }
    )

def category(request, cid=None):
    cat = None

    query = request.GET.get('query')
    cid = request.GET.get('category', cid)

    where = {}

    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid
    if query:
        where['name__icontains'] = query

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'category.html',
        {
            'page_obj':page_obj,
            'category':cat
        }
    )

def cart(request):
    return render(
        request, 'cart.html'
    )

def checkout(request):
    return render(
        request, 'checkout.html'
    )

def checkout_complete(request):
    return render(
        request, 'checkout-complete.html'
    )