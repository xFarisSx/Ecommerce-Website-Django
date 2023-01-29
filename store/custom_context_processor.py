from store.models import Category

def store_website(request):
    categories = Category.objects.order_by('order')
    return {
        'categories':categories
    }

