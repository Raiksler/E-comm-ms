from django.http import JsonResponse, HttpResponse
from main.models import Products
from django.views.decorators.csrf import csrf_exempt
import ast

# Create your views here.

def get_items(request):
    items_queryset = list(Products.objects.all().values('product', 'price'))
    items_dict = {}
    for item in items_queryset:
        items_dict[item['product']] = item['price']
    return JsonResponse(items_dict)

@csrf_exempt                              #CSRF токен игнорируется, учитывая условие тз.
def new_item(request):
    byte_req = request.body
    dict_req = byte_req.decode("UTF-8")   #Конвертируем байты в строку UTF-8.
    data = ast.literal_eval(dict_req)     #Переводим строку в словарь, считывая синтаксис.
    new_product = data["product"]
    new_price = data["price"]
    Products.objects.create(product=new_product, price=new_price)   #Обновляем бд.
    return HttpResponse(status=200)