from django.http import JsonResponse, HttpResponse
from main.models import Products, Cart
from django.views.decorators.csrf import csrf_exempt
import ast


def get_price(item_id):
        product_queryset = list(Products.objects.filter(pk=item_id))[0]
        product_price = getattr(product_queryset, "price")
        return product_price

def show_cart(request):
    cart_queryset = list(Cart.objects.all().values("id", "price", "quantity"))
    cart_dict = {}
    for item in cart_queryset:
        cart_dict[item['id']] = {'price' : item['price'], 'quantity' : item['quantity']}
    print(cart_dict)
    return JsonResponse(cart_dict)


@csrf_exempt
def change_cart(request):
    byte_req = request.body               #Смотрим тело запроса.
    dict_req = byte_req.decode("UTF-8")   #Конвертируем байты в строку UTF-8.
    data = ast.literal_eval(dict_req)     #Переводим строку в словарь, считывая синтаксис.
    try:
        item_id = data["id"]
        quantity = data["quantity"]
    except KeyError:                      #Не позволяем добавить товар с неполными или неверными параметрами.
        return HttpResponse(status=500)
    if quantity > 0:
        add_item(item_id, quantity)
    elif quantity < 0:
        remove_item(item_id, abs(quantity))
    elif quantity == 0:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def add_item(id, quantity):
    if Cart.objects.filter(pk=id).count() > 0:    #Проверяем, добавлена ли эта позиция в корзину.
        new_quantity = int(getattr(list(Cart.objects.filter(pk=id))[0], "quantity")) + quantity
        Cart.objects.update(quantity=new_quantity)
    else:
        item_price = get_price(id)
        Cart.objects.create(id = Products.objects.get(id=id), price = item_price, quantity = quantity)

def remove_item(id, quantity):
    if Cart.objects.filter(pk=id).count() > 0:    #Проверяем, добавлена ли эта позиция в корзину.
        new_quantity = int(getattr(list(Cart.objects.filter(pk=id))[0], "quantity")) - quantity
        if new_quantity <= 0:
            Cart.objects.filter(id=id).delete()
        else:
            Cart.objects.update(quantity=new_quantity)