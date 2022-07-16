from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json


# Create your views here.


def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4+ceil((n/4)-(n//4))
    # Range = range(1, nSlides)
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allprods = [[products, Range, nSlides], [products, Range, nSlides]]
    allprods = []
    catprods = Product.objects.values('category')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        Range = range(1, nSlides)
        allprods.append([prod, Range, nSlides])
    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)


def searchmatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def productView(request, myid):
    vproduct = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': vproduct[0]})


def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return redirect('/shop/')
    return render(request, "shop/contact.html")


def about(request):
    return render(request, 'shop/about.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            print(order)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    responses = json.dumps(updates, default=str)
                return HttpResponse(responses)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def checkout(request):
        if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')

            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                           zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        return render(request, 'shop/checkout.html')
