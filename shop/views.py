from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from shop.forms import AddQuantityForm
from .scraping import scraping, ScrapingError
from django.views.generic import ListView, DeleteView
from .models import Order, OrderItem, Product

# Create your views here.

def fill_database(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping()
        except ScrapingError as err:
            print(str(err))
            return render(request, "shop/fill_products.html", {"message" : str(err)})
        
    return render(request, "shop/fill_products.html", {"message" : None}) 


class ProductsListView(ListView):
    model = Product
    template_name = 'shop/shop.html'

@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                # product = Product.objects.get(pk=pk)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('shop:cart_view')
        else:
            pass
    return redirect('shop:shop')


@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('shop:cart_view')

    # Проверка доступа
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs
    

@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    cart = Order.get_cart(request.user)
    cart.make_order()
    return redirect('shop:shop')


def cart_pnumber(request):
    return render(request, "shop/cart_pnumber.html")