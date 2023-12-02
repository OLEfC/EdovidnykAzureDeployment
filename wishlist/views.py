from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from django.db import connection


# Create your views here.
@login_required(login_url='/login/')
def wishlist_view(request):
    user = request.user.id
    table = get_wishlist_table(user)
    
    # Цикл для ітерації по кортежам у списку table
   

    search_results=get_wishlist_items(find_table_names_by_idpages(get_wishlist_table(user)))
    #print(search_results)
    if search_results:
        return render(request, 'wishlist.html', {'search_results': search_results})
    
    return render(request, 'wishlist.html')


def get_wishlist_table(user_id):#пошук id товару за id користувача
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT idpage FROM edovidnyk.wishlist
            where userid=%s; 
            ''',[user_id] ,  # Повторити idpage 7 разів для всіх запитів
            )
        wishlist_table = cursor.fetchall()
    return wishlist_table


def get_wishlist_items(input_list):
    wishlist_items = []
    with connection.cursor() as cursor:
        for item in input_list:
            table = item[0]
            idpage = item[1]
            cursor.execute(
              '''
                SELECT edovidnyk.%s.model%s, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.%s.idpage
                FROM ((edovidnyk.%s
                INNER JOIN edovidnyk.producer ON edovidnyk.%s.producer = edovidnyk.producer.idproducer)
                INNER JOIN edovidnyk.idpage ON edovidnyk.%s.idpage = edovidnyk.idpage.ididPAGE)
                WHERE edovidnyk.idpage.ididPAGE = %s
                ''' % (table, table,table,table, table, table, idpage)
            )
            result = cursor.fetchall()
            wishlist_items.extend(result)
    return wishlist_items





def find_table_names_by_idpages(idpages):
    results = []

    with connection.cursor() as cursor:
        for idpage in idpages:
            cursor.execute(
                """
                SELECT 'cpu' AS table_name, idpage FROM cpu WHERE idpage = %s
                UNION
                SELECT 'gpu' AS table_name, idpage FROM gpu WHERE idpage = %s
                UNION
                SELECT 'device' AS table_name, idpage FROM device WHERE idpage = %s
                UNION
                SELECT 'networkcard' AS table_name, idpage FROM networkcard WHERE idpage = %s
                UNION
                SELECT 'rom' AS table_name, idpage FROM rom WHERE idpage = %s
                UNION
                SELECT 'ram' AS table_name, idpage FROM ram WHERE idpage = %s
                UNION
                SELECT 'screen' AS table_name, idpage FROM screen WHERE idpage = %s
                """,
                [idpage] * 7,  # Повторити idpage 7 разів для всіх запитів
            )
            result = cursor.fetchall()
            results.append(result[0] if result else None)

    return results


from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def delete_item(request, item_id):
    user = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(
            '''
            DELETE FROM edovidnyk.wishlist WHERE userid=%s AND idpage=%s;
            ''', [user, item_id]
        )
        cursor.fetchall()

    return redirect('/wishlist')


@require_POST
def delete_all(request):
    user = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(
            '''
            DELETE FROM edovidnyk.wishlist WHERE userid=%s;
            ''', [user]
        )
        cursor.fetchall()

    return redirect('/wishlist')
    