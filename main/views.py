from django.shortcuts import render
from django.db import connection  # Імпортуйте об'єкт підключення
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
def get_popular_items(input_list):
    popular_items = []
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
            popular_items.extend(result)
    return popular_items
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



@csrf_exempt
def main(request):

    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT * FROM popular ORDER BY clickrate DESC LIMIT 5;
            """
            
        )
        result = cursor.fetchall()
        input_list=[]

        for r in result:
            tempList=[find_table_names_by_idpages(r[1])[0],r[1]]
            input_list.append(tempList)

        popular_results=get_popular_items(input_list)
        print(popular_results)
    return render(request, 'main.html', {'popular_results': popular_results})



        

            

            
        
        #print(result)

@csrf_exempt
def search(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', '')
       

        # Ваш SQL-запит для пошуку в базі даних MySQL
        query = f'''
            SELECT edovidnyk.gpu.modelgpu, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.gpu.idpage
            FROM ((edovidnyk.gpu
            INNER JOIN edovidnyk.producer ON edovidnyk.gpu.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.gpu.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.gpu.modelgpu LIKE %s

            UNION
            SELECT edovidnyk.cpu.modelcpu, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.cpu.idpage
            FROM ((edovidnyk.cpu
            INNER JOIN edovidnyk.producer ON edovidnyk.cpu.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.cpu.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.cpu.modelcpu LIKE %s


            UNION
            SELECT edovidnyk.networkcard.modelnetworkcard, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.networkcard.idpage
            FROM ((edovidnyk.networkcard
            INNER JOIN edovidnyk.producer ON edovidnyk.networkcard.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.networkcard.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.networkcard.modelnetworkcard LIKE %s

             UNION
            SELECT edovidnyk.ram.modelram, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.ram.idpage
            FROM ((edovidnyk.ram
            INNER JOIN edovidnyk.producer ON edovidnyk.ram.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.ram.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.ram.modelram LIKE %s

            UNION
            SELECT edovidnyk.rom.modelrom, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.rom.idpage
            FROM ((edovidnyk.rom
            INNER JOIN edovidnyk.producer ON edovidnyk.rom.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.rom.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.rom.modelrom LIKE %s
       
            UNION
            SELECT edovidnyk.screen.modelscreen, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.screen.idpage
            FROM ((edovidnyk.screen
            INNER JOIN edovidnyk.producer ON edovidnyk.screen.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.screen.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.screen.modelscreen LIKE %s
            
            UNION
            SELECT edovidnyk.laptop.modellaptop, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.laptop.idpage
            FROM ((edovidnyk.laptop
            INNER JOIN edovidnyk.producer ON edovidnyk.laptop.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.laptop.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.laptop.modellaptop LIKE %s

           


            UNION
            SELECT edovidnyk.pc.modelpc, edovidnyk.producer.name, edovidnyk.idpage.mainphoto,edovidnyk.pc.idpage
            FROM ((edovidnyk.pc
            INNER JOIN edovidnyk.producer ON edovidnyk.pc.producer = edovidnyk.producer.idproducer)
            INNER JOIN edovidnyk.idpage ON edovidnyk.pc.idpage = edovidnyk.idpage.ididPAGE)
            WHERE edovidnyk.producer.name LIKE %s OR edovidnyk.pc.modelpc LIKE %s
            
            
            '''
        with connection.cursor() as cursor:
            cursor.execute(query, [f'%{search_query}%'] * 16)
            search_results = cursor.fetchall()
        #if search_results:#щоб повернути іф перенеси блок редер в нього 


        #print(search_results)
            # Повернути результати пошуку в шаблон, де ви їх 
        return render(request, 'search_results.html', {'search_results': search_results})
        
        
    else:
        return HttpResponse('This page is only accessible via POST request')


