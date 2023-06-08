from django.shortcuts import render, redirect

from .models import Vendor
from users.models import User
from .forms import AddProducts
from store.models import Products, Categories, OrderItem, Order, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models import Q
from store.utils import cartData

# User = settings.AUTH_USER_MODEL
# Create your views here.

def vendor_dash(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Products.objects.all()
        try:
            vendor_u = Vendor.objects.filter(vendor_name=request.user.id).values('shop_name')[0]['shop_name']
        except IndexError:
            pass

        vendor_name = request.user.vendor
        shippingDetails = ShippingAddress.objects.all()
        unique_products = products.filter(vendor=vendor_name)
        # check orders table add the id into array => all_orders_id
        all_orders_id = []
        order_table = Order.objects.filter().values()
        for order_id in order_table:
            all_orders_id.append(order_id['id'])

        print(all_orders_id)
        # ORDERS FOR UNIQUE VENDOR
        certain_customer_orders = []

        order_items = OrderItem.objects.filter().values()
        # loop through all_orders_id and use each key to filter order items with same key => O_item
        for i in all_orders_id:
            for o_item in order_items:
                # check for similar order_no btn order table and orderItems table
                if o_item['order_id'] == i:
                    # get the vendor id......
                    product_vendor = products.filter(id=o_item['product_id']).values('vendor_id')[0]['vendor_id']

                    # append vendor id to o_item dictionary
                    o_item['vendor_identifier'] = product_vendor

                    # get the product_name ....... 
                    product_name = products.filter(id=o_item['product_id']).values('name')[0]['name']

                    # append product name to o_item dictionary
                    o_item['product_name'] = product_name

                    #get shipping details by order_id for comparing easily with order items
                    if_ship_details = shippingDetails.filter(order_id=o_item['order_id']).values()
                    # perform quick check of shipping table to see whether an order is complete
                    if str(if_ship_details) != '<QuerySet []>':
                        # if such an order exists the append the below data to o_item dict
                        o_item['customer_id'] = if_ship_details[0]['customer_id']
                        o_item['customer_phone'] = if_ship_details[0]['phone']
                        o_item['customer_address'] = if_ship_details[0]['address']
                        o_item['customer_order_date'] = if_ship_details[0]['date_added']
                    # get the status of order whether completed by the user or still in cart...
                    statuses = Order.objects.filter(id=o_item['order_id']).values_list('pending', 'complete', 'cancelled')
                
                    for status in statuses[0]:
                        if status == True:
                            i_status = statuses[0].index(status)
                            if i_status == 0:
                                o_item['status'] = 'pending'
                            elif i_status == 1:
                                o_item['status'] = 'complete'
                            if i_status == 2:
                                o_item['status'] = 'cancelled'
                    # compare data(vendor_identifier) in o_item with the logged in vendor for filtering... 
                    logged_vendor = Vendor.objects.filter(vendor_name_id=request.user).values()[0]['id']
                    if o_item['vendor_identifier'] == logged_vendor:
                        certain_customer_orders.append(o_item)
                    
            # break
        print(f"certain_customer_orders {certain_customer_orders}")
        
        context={
            "unique_products":unique_products, 
            "vendor_u":vendor_u, 
            "all_orders": certain_customer_orders,
            "cartItems":cartItems,
            }
    except Vendor.DoesNotExist:
        context={"error_v":"Please register as a vendor at <a href="">Profile</a> to access this feature","cartItems":cartItems,}

    return render(request, 'vendors/dashboard.html', context)

def my_shop(request, *args, **kwargs):
    data = cartData(request)
    cartItems = data['cartItems']
    print(args, kwargs)
    shopName = kwargs['slug']
    rev_shop = Vendor.objects.filter(shop_name=shopName).values('vendor_name_id')[0]['vendor_name_id']
    print(rev_shop, "rev")
    user = User.objects.get(id=rev_shop)
    request.session['user'] = user.id
    products = Products.objects.filter(vendor=user.vendor)

    # create a unique list of categories for vendors
    unique_categories = []
    
    for prod_category in products:
        category = prod_category.category
        
        if category not in unique_categories:
            unique_categories.append(category)
    print(unique_categories, "cats")
    
    vendor = Vendor.objects.get(vendor_name=user)
    print(products)
    
    context = {"user":request.user, "vendor":vendor, "products": products, "unique_categories": unique_categories,"cartItems":cartItems,}
    return render(request, 'vendors/vendor_shop.html', context)

def vendor_categories(request, *args, **kwargs):
    print(args, kwargs)
    data = cartData(request)
    cartItems = data['cartItems']
    
    user = User.objects.get(id=request.session.get("user"))
    vendor = Vendor.objects.get(vendor_name=user)
    print(user)
    products = Products.objects.filter(vendor=user.vendor)

    # create a unique list of categories for vendors
    unique_categories = []
    
    for prod_category in products:
        category = prod_category.category
        
        if category not in unique_categories:
            unique_categories.append(category)
    try:
        category_id = Categories.objects.filter(name=kwargs['slug']).values()[0]['id']
        print(category_id)
        new_products = products.filter(category=category_id)
    except IndexError:
        new_products = ""
    context = {"unique_categories":unique_categories,"vendor":vendor, "products": new_products,"cartItems":cartItems,}
    return render(request, "vendors/categories.html", context)


@login_required(login_url="users:site-login")
def add_product(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        if request.user.vendor:
            if request.method == 'POST':
                form = AddProducts(request.POST, request.FILES)
                if form.is_valid():
                    # print(form,"foooooooo")
                    prod = form.save(commit=False)
                    prod.vendor = request.user.vendor
                    prod.save()
                    messages.success(request,f"Product {form.cleaned_data['name']} added.")
                    # return redirect("/vendor/dashboard")
                    form = AddProducts()
                    context = {"form":form,"cartItems":cartItems,}
                    return render(request, "vendors/add_product.html", context)
                else:
                    print(form.errors)
            else:
                form = AddProducts()
            context = {"form":form,"cartItems":cartItems,}
    # else:
    except:
        print("not vendor")
        messages.success(request, "please verify to be a vendor", extra_tags="helper")
        return redirect("users:site-profile")

    
    return render(request, "vendors/add_product.html", context)

def process_vendor(request):
    # transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    vendor = Vendor.objects.get(vendor_name=request.user)
    
    vendor.shop_name=data['vendorInfo']['shop_name']
    vendor.shop_location=data['vendorInfo']['shop_location']
    vendor.id_number=data['vendorInfo']['id_number']
    vendor.dob=data['vendorInfo']['date_of_birth']
    vendor.phone=data['vendorInfo']['phone']
    
    
    
    vendor.save()


    return JsonResponse('profile saved', safe=False)
