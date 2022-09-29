from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    param = request.GET.get('sort')
    if param == 'name':
        phone_objects = Phone.objects.order_by('name')
    elif param == 'min_price':
        phone_objects = Phone.objects.order_by('price')
    elif param == 'max_price':
        phone_objects = Phone.objects.order_by('price').reverse()
    else:
        phone_objects = Phone.objects.all()

    context = {
        'phones': phone_objects
     }

    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_object = Phone.objects.filter(slug=slug)[0]
    context = {
        'phone': phone_object
     }

    return render(request, template, context)
