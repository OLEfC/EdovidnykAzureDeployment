from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse


from django.db import connection

def find_table_names_by_idpages(idpage):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT 'cpu' AS table_name, idpage FROM cpu WHERE idpage = %s
            UNION
            SELECT 'gpu' AS table_name, idpage FROM gpu WHERE idpage = %s
            UNION
            SELECT 'pc' AS table_name, idpage FROM pc WHERE idpage = %s
             UNION
            SELECT 'laptop' AS table_name, idpage FROM laptop WHERE idpage = %s
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
        results=result[0] if result else None

    return results

def parse_data(table,idpage):
    with connection.cursor() as cursor:
        
        # Перевірка наявності idpage в таблиці popular
        cursor.execute("SELECT * FROM popular WHERE idpage = %s", (idpage,))
        result = cursor.fetchone()
        
        # Якщо idpage вже існує в таблиці popular
        if result:
            # Збільшуємо значення clickrate на одиницю
            cursor.execute("UPDATE popular SET clickrate = clickrate + 1 WHERE idpage = %s", (idpage,))
        else:
            # Якщо idpage не існує в таблиці popular, додаємо новий запис з clickrate = 1
            cursor.execute("INSERT INTO popular (idpage, clickrate) VALUES (%s, 1)", (idpage,))
      
        cursor.execute(
                '''SELECT * ,producer.name,idpage.mainphoto 
        FROM(( edovidnyk.%s

        INNER JOIN producer ON edovidnyk.%s.producer = producer.idproducer)
        INNER JOIN edovidnyk.idpage ON edovidnyk.%s.idpage = edovidnyk.idpage.ididPAGE)
        WHERE edovidnyk.%s.idpage = %s;'''% (table,table,table,table, idpage)
        )
        result = cursor.fetchall()
        return result
    

def parse_data_pc(table,idpage):
    with connection.cursor() as cursor:
        
        # Перевірка наявності idpage в таблиці popular
        cursor.execute("SELECT * FROM popular WHERE idpage = %s", (idpage,))
        result = cursor.fetchone()
        
        # Якщо idpage вже існує в таблиці popular
        if result:
            # Збільшуємо значення clickrate на одиницю
            cursor.execute("UPDATE popular SET clickrate = clickrate + 1 WHERE idpage = %s", (idpage,))
        else:
            # Якщо idpage не існує в таблиці popular, додаємо новий запис з clickrate = 1
            cursor.execute("INSERT INTO popular (idpage, clickrate) VALUES (%s, 1)", (idpage,))
      
        cursor.execute(
            '''SELECT *, producer.name AS producer_name, idpage.mainphoto
                FROM edovidnyk.%s
                INNER JOIN producer ON edovidnyk.%s.producer = producer.idproducer
                INNER JOIN edovidnyk.idpage ON edovidnyk.%s.idpage = edovidnyk.idpage.ididPAGE
                INNER JOIN producer AS cpuProducer ON edovidnyk.%s.cpuProducer = cpuProducer.idproducer
                INNER JOIN producer AS gpuProducer ON edovidnyk.%s.gpuProducer = gpuProducer.idproducer
                WHERE edovidnyk.%s.idpage = %s;'''% (table,table,table,table,table, table,idpage)
        )
        result = cursor.fetchall()
        return result
    

def searchimages(idpage):
     with connection.cursor() as cursor:
        
      
        cursor.execute(
                '''
            select photo from product_images
            where idproduct_images=%s;
            '''% ( idpage)
        )
        result = cursor.fetchall()
        print(len(result))
        return result


def product_detail(request, product_id):
    table = find_table_names_by_idpages(product_id)[0]
    print(table)
    
    if table is None:
        return(HttpResponse("404"))
    else:
        image=searchimages(product_id)
        search_results=parse_data(table,product_id)
        if table=='cpu':
            return render(request, 'cpuitem.html', {'search_results': search_results,'image_results':image})
            
        elif table=='gpu':
            return render(request, 'gpuitem.html', {'search_results': search_results,'image_results':image})

            
        elif table=='pc':
            return render(request, 'pcitem.html', {'search_results':  parse_data_pc(table,product_id),'image_results':image})
        
        elif table=='laptop':
            return render(request, 'laptopitem.html', {'search_results': parse_data_pc(table,product_id),'image_results':image})

            
        elif table=='networkcard':
            return render(request, 'networkcarditem.html', {'search_results': search_results,'image_results':image})

           
        elif table=='rom':
            return render(request, 'romitem.html', {'search_results': search_results,'image_results':image})

           
        elif table=='ram':
            return render(request, 'ramitem.html', {'search_results': search_results,'image_results':image})

            
        elif table=='screen':
            return render(request, 'screen.html', {'search_results': search_results,'image_results':image})
    
        print(parse_data(table,product_id))
        return(HttpResponse(parse_data(table,product_id)))


    #return render(request, 'product_detail.html', {'product': product})

# Create your views here.



  

@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(
                '''
                INSERT INTO `edovidnyk`.`wishlist` (`userid`, `idpage`)
                SELECT %s, %s FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1 FROM `edovidnyk`.`wishlist`
                    WHERE `userid` = %s AND `idpage` = %s
                );

            '''% (user, product_id,user, product_id) 
        )
        result = cursor.fetchall()
        print(len(result))

    return(product_detail(request, product_id))


@login_required(login_url='/login/')
def add_to_compare(request, product_id):
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(
                '''
                INSERT INTO `edovidnyk`.`compare` (`userid`, `idpage`)
                SELECT %s, %s FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1 FROM `edovidnyk`.`compare`
                    WHERE `userid` = %s AND `idpage` = %s
                );

            '''% (user, product_id,user, product_id) 
        )
        result = cursor.fetchall()
        print(len(result))

    return(product_detail(request, product_id))



     
