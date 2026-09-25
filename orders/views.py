from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect('view_cart')

    order = Order.objects.create(user=request.user)

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.product.price
        )

    cart.items.all().delete()

    return redirect('order_history')


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})