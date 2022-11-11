from distutils.command.clean import clean
from unicodedata import name
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from json import dumps
import datetime
from django.contrib.auth.decorators import login_required
from .utils import cookieCart, cartData, productDet, guestOrder
#import requests
#from request.auth import HTTPBasicAuth
from django.conf import settings

User = settings.AUTH_USER_MODEL



# Create your views here.
#def index(request):
#    
#    context = {}
#    return render(request, 'store/index.html', context)
#    shipping = ShippingAdress()


def about(request):   
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'title':'about','cartItems':cartItems}
    return render(request, 'store/about.html', context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {'title':'contactus','cartItems':cartItems}
    return render(request, 'store/contacts.html', context)


def brandNames(request, *args, **kwargs):
    data = cartData(request)
    cartItems = data['cartItems']
    brand_name = kwargs['slug']
    print(brand_name)

    products = Featuredproduct.objects.filter(name__contains=brand_name)
    # get category id
    category_id = BrandCategories.objects.get(name=brand_name)
    miniBrand_Categories = BrandMiniCategories.objects.filter(brand_categories=category_id)
    
    context = {'products':products, 'cartItems':cartItems,'title':brand_name,'miniBrand_Categories':miniBrand_Categories,}
    return render(request, 'store/all_brands.html', context)


def processImages(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    product_name = data['productname']['prod_name']
    print(f"clicked prod::{product_name}")
    
    request.session["product_name"] = product_name
    return JsonResponse('image processed', safe=False)



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
        
    products = Featuredproduct.objects.all()
    product_db = productDet(request,products)

    #getting a complete order_id
    complete_order = Order.objects.filter(complete=True)
    vendor_id = ''
    
    #check if user is a vendor
    try:
        if request.user.vendor:
            print(" vendor")
    except AttributeError:
        print(f"not vendor user is {request.user}")

        

    for order in complete_order: 
        #getting the order items with the complete order_id 
        Orderitem_list = OrderItem.objects.filter(order_id=order)

        print(Orderitem_list)
        # print(Featuredproduct.objects.filter(name=Orderitem_list[0])[0].id)
        print(order)

        #checking the vendor for each product in the complete order query to alert them of a sale
        for i in Orderitem_list.values():
            prod_id = Featuredproduct.objects.filter(id=i["product_id"])

            print(f"{Vendor.objects.filter(featuredproduct__id=i['product_id'])} ### {prod_id}")
        
    Common_brands = BrandCategories.objects.all()
    prod_category = products.filter().values('id','name','category_id')
    clean_prod_category = []
    for i in prod_category:
        category_name = BrandCategories.objects.filter(id=i['category_id']).values('name')[0]['name']
        i['category_id'] = category_name
        clean_prod_category.append(i)
    print(product_db['search_db'])
    
    context = {
        'products':products,
        'clean_prod_category':dumps(clean_prod_category),
        "each_product_db":product_db['each_product_db'],
        'search_db':product_db['search_db'], 
        'cartItems':cartItems,
        'title':'store',
        'Common_brands':Common_brands,
        }
    return render(request, 'store/store.html', context)

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems,'title':'cart',}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems,'title':'checkout',}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('product:', productId)
    
    
    customer = request.user.customer
    product = Featuredproduct.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, productId=productId)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    
    return JsonResponse('item added', safe=False)



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        
        

    else:
        customer, order = guestOrder(request,data)
        

    total = float(data['shipping']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
        order.pending = False
        order.cancelled = False
    order.save()

    ShippingAddress.objects.create(
    customer=customer,
    order=order,
    address=data['shipping']['address'],
    phone=data['shipping']['phone'],
    state=data['shipping']['address'],
    zipcode=data['shipping']['postalcode'],
    mpesacode=data['userPayData']['payphone'],
    
    )


    return JsonResponse('payment complete', safe=False)








