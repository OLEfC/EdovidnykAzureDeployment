from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from django.db import connection

# Create your views here.
def get_compare_table(user_id):#пошук id товару за id користувача
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT idpage FROM edovidnyk.compare
            where userid=%s; 
            ''',[user_id] ,  # Повторити idpage 7 разів для всіх запитів
            )
        compare_table = cursor.fetchall()
    return compare_table



def find_table_names_by_idpages(idpages):#пошук таблиць за всіма товарами
    results = []

    with connection.cursor() as cursor:
        for idpage in idpages:
            cursor.execute(
                """
                SELECT 'cpu' AS table_name, idpage FROM cpu WHERE idpage = %s
                UNION
                SELECT 'gpu' AS table_name, idpage FROM gpu WHERE idpage = %s
                UNION
                SELECT 'laptop' AS table_name, idpage FROM laptop WHERE idpage = %s
                UNION
                SELECT 'pc' AS table_name, idpage FROM pc WHERE idpage = %s
                UNION
                SELECT 'networkcard' AS table_name, idpage FROM networkcard WHERE idpage = %s
                UNION
                SELECT 'rom' AS table_name, idpage FROM rom WHERE idpage = %s
                UNION
                SELECT 'ram' AS table_name, idpage FROM ram WHERE idpage = %s
                UNION
                SELECT 'screen' AS table_name, idpage FROM screen WHERE idpage = %s
                """,
                [idpage] * 8,  # Повторити idpage 7 разів для всіх запитів
            )
            result = cursor.fetchall()
            results.append(result[0] if result else None)

    return results
    
def get_unique_table_names(results):
    unique_tables = set()
    for result in results:
        if result:
            unique_tables.add(result[0])
    return list(unique_tables)


def get_compare_items(input_list):
    compare_items = {}

    with connection.cursor() as cursor:
        for item in input_list:
            table = item[0]
            idpage = item[1]

            cursor.execute(
                '''
                SELECT *
                FROM ((edovidnyk.%s
                INNER JOIN edovidnyk.producer ON edovidnyk.%s.producer = edovidnyk.producer.idproducer)
                INNER JOIN edovidnyk.idpage ON edovidnyk.%s.idpage = edovidnyk.idpage.ididPAGE)
                WHERE edovidnyk.idpage.ididPAGE = %s
                ''' % (table, table, table, idpage)
            )

            result = cursor.fetchall()

            if table not in compare_items:
                compare_items[table] = []

            compare_items[table].extend(result)

    return compare_items


from django.shortcuts import render

@login_required(login_url='/login/')
def compare_view(request):
    user = request.user.id
    tables = find_table_names_by_idpages(get_compare_table(user))
    
    # Цикл для ітерації по кортежам у списку table
    table = get_unique_table_names(tables)
    search_results = get_compare_items(tables)
    print(tables)
    
    context = {'search_results': search_results, 'table_list': table}

    print(context)
    
    return render(request, 'compare.html', context)

from django.shortcuts import redirect

def delete_table(request, table_type):

    user = request.user.id
    tables = find_table_names_by_idpages(get_compare_table(user))
    
    # Цикл для ітерації по кортежам у списку table
 
    print(tables)

    index=[]
    for tab in tables:
        if tab[0]==table_type:
            index.append(tab[1])
    print(index)

    with connection.cursor() as cursor:
        for i in index:
            cursor.execute(
                '''
                DELETE FROM edovidnyk.compare WHERE userid=%s AND idpage=%s;
                ''', [user,i]
            )
            cursor.fetchall()

    return redirect('/compare')
    # Отримайте потрібний об'єкт або виконайте видалення з бази даних
    # Наприклад, можна використовувати модель, якщо ви працюєте з базою даних Django ORM

    # Тут буде ваш код для видалення
    # Наприклад:
    # if table_type == 'gpu':
    #     MyModel.objects.filter(type='gpu').delete()
    # elif table_type == 'cpu':
    #     MyModel.objects.filter(type='cpu').delete()
    # і так далі

   

