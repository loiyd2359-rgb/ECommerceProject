from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from orders.models import OrderItem
from .models import Product, Category

def product_list_view(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


def recommended_products_view(request):
    if request.user.is_authenticated:
        purchased_categories = OrderItem.objects.filter(
            order__user=request.user
        ).values_list('product__category', flat=True).distinct()

        purchased_products = OrderItem.objects.filter(
            order__user=request.user
        ).values_list('product_id', flat=True)

        if purchased_categories:
            recommended = Product.objects.filter(
                category__in=purchased_categories
            ).exclude(id__in=purchased_products)[:6]
        else:
            recommended = Product.objects.annotate(
                order_count=Count('orderitem')
            ).order_by('-order_count')[:6]
    else:
        recommended = Product.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:6]

    return render(request, 'products/recommended.html', {'products': recommended})