from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserInfoForm
from store.models import Product , Cart, Order
from checkout.models import Transaction, PaymentMethod
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_store import settings
from django.utils.translation import gettext as _
from django_store import settings
import math
import stripe

# Create your views here.
# def make_order(request):
#     if request.method != 'POST':
#         return redirect('store.checkout')
    
#     form = UserInfoForm(request.POST)
#     if form.is_valid():
#         cart = Cart.objects.filter(session=request.session.session_key).last()
#         products = Product.objects.filter(pk__in=cart.items)

#         total = 0
#         for item in products:
#             total+=item.price
        
#         if total <= 0:
#             return redirect('store.cart')

#         order = Order.objects.create(customer=form.cleaned_data, total=total)
#         for product in products:
#             order.orderproduct_set.create(product_id=product.id, price=product.price)

#         send_order_email(order, products)

#         cart.delete()
#         return redirect('store.checkout_complete')
#     else:
#         return redirect('store.checkout')

def stripe_config(request):
    return JsonResponse(
        {
            'public_key':settings.STRIPE_PUBLISHABLE_KEY
        }
    )

def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)

    if not transaction:
        return JsonResponse({
            'message':_('Please enter valid info.')
        }, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount*100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction':transaction.id
        }
    )

    return JsonResponse({
            'client_secret': intent['client_secret']
        })

def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Paypal)

def make_transaction(request, pm):
    
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)

        total = 0
        for item in products:
            total+=item.price
        
        if total <= 0:
            return None

        return Transaction.objects.create(
            customer=form.cleaned_data,
            session=request.session.session_key,
            payment_method=pm,
            items=cart.items,
            amount=math.ceil(total)
            )

def send_order_email(order, products):
    msg_html = render_to_string('emails/order.html', {
        'order':order,
        'products':products
    })
    send_mail(subject='New Order', 
        html_message=msg_html,
        message=msg_html,
        from_email='noreply@example.com',
        recipient_list=[order.customer['email']]
    )