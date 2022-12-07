from django.shortcuts import render, get_object_or_404, redirect
from ecomapp.models import Product, Category, Cart, CartItem
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def allProdCat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.all().filter(category=c_page,available="True")
    else:
        products_list = Product.objects.all().filter(available="True")

    paginator=Paginator(products_list,8)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request,"category.html", {'category':c_page,'products':products})

def allProdDet(request,c_slug,p_slug):
    try:
        product=Product.objects.get(category__slug=c_slug, slug=p_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def allProdSer(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=Product.objects.all().filter(Q(name__icontains=query))
    return render(request,'search.html',{'query':query,'products':products})


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request),
        )
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect ('shop:cart_detail')

def cart_detail(request, total=0, counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def remove_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect ('shop:cart_detail')

def delete_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect ('shop:cart_detail')



