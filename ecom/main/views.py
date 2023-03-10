from django.http import JsonResponse, HttpResponse
from main.models import Products
from django.views.decorators.csrf import csrf_exempt
import ast


def filtered_by_name(item_list, query):
    if query == None:
        return
    return list(filter(lambda x: query in x[1], item_list))

def filtered_by_price(item_list, price):
    if price == None:
        return
    return list(filter(lambda x: int(price) == x[2], item_list))


def sorted_by_name(item_list, is_reversed):
    item_list = sorted(item_list, key=lambda x: x[1], reverse=is_reversed)
    return item_list


def sorted_by_price(item_list, is_reversed):
    item_list = sorted(item_list, key=lambda x: x[2], reverse=is_reversed)
    return item_list


def get_items(request):
    if request.GET.get('sorted_by_name') != None and request.GET.get('sorted_by_price') != None: #Если одновременно применена сортировка по цене и имени - возвращаем 500.
        return HttpResponse(status=500)

    items_queryset = list(Products.objects.all().values('id', 'product', 'price'))                    #Достаем данные о товарах и ценах из бд.
    response = list()
    for item in items_queryset:
        response.append((item['id'], item['product'], item['price']))

    if request.GET.get('filtered_by_name') != None:                         #Проверяем, запрошена ли фильтрация по имени.
        query = request.GET.get('filtered_by_name')
        response = filtered_by_name(item_list=response, query=query)

    if request.GET.get('sorted_by_name') == "a-z":                          #Проверяем, запрошена ли сортировка по имени и в каком порядке.
        response = sorted_by_name(item_list=response, is_reversed=False)
    elif request.GET.get('sorted_by_name') == "z-a":
        response = sorted_by_name(item_list=response, is_reversed=True)

    if request.GET.get('sorted_by_price') == "up":                        #Проверяем, запрошена ли сортировка по цене и в каком порядке.
        response = sorted_by_price(item_list=response, is_reversed=False)
    elif request.GET.get('sorted_by_price') == "down":
        response = sorted_by_price(item_list=response, is_reversed=True)

    if request.GET.get('filtered_by_price') != None:
        price = request.GET.get('filtered_by_price')
        response = filtered_by_price(item_list=response, price=price)

    #Ниже проверка на наличие как минимум одного query параметра.

    if request.GET.get('filtered_by_name') != None or request.GET.get('sorted_by_name') != None or request.GET.get('sorted_by_price') != None or request.GET.get('filtered_by_price') != None:
        response_dict = {}
        i = 0
        for item in response:
            response_dict[i] = {"product_id" : item[0], "product_name": item[1]}
            i+=1
        return JsonResponse(response_dict)

    #Если запрос не содержит query параметров, возвращаем список всех товаров и цен на них.

    items_queryset = list(Products.objects.all().values('id', 'product', 'price'))
    items_dict = {}
    for item in items_queryset:
        items_dict[item['id']] = {"product_name" : item["product"], "price" : item['price']}
    return JsonResponse(items_dict)


@csrf_exempt                              #CSRF токен игнорируется, учитывая условие тз.
def new_item(request):
    byte_req = request.body               #Смотрим тело запроса.
    dict_req = byte_req.decode("UTF-8")   #Конвертируем байты в строку UTF-8.
    data = ast.literal_eval(dict_req)     #Переводим строку в словарь, считывая синтаксис.
    try:
        new_product = data["product"]
        new_price = data["price"]
        new_details = data["details"]
    except KeyError:                      #Не позволяем добавить товар с неполными параметрами.
        return HttpResponse(status=500)

    if Products.objects.filter(product=new_product).count() > 0:    #Не позволяем добавлять уже имеющиеся товары.
        return HttpResponse(status=500)

    Products.objects.create(product=new_product, price=new_price, details=new_details)   #Обновляем бд.
    return HttpResponse(status=200)

def get_details(request):
    target_product = request.GET.get("id")
    if target_product != None:
        product_queryset = list(Products.objects.filter(pk=target_product))[0]
        product_id = getattr(product_queryset, "id")
        product_name = getattr(product_queryset, "product")
        product_price = getattr(product_queryset, "price")
        product_details = getattr(product_queryset, "details")
        product_dict = {"info" : {'id' : product_id, "name" : product_name, "price" : product_price, "details" : product_details}}
        return JsonResponse(product_dict)