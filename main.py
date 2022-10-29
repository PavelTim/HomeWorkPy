import psycopg2
from psycopg2 import Error

import onlycursor
from onlycursor import (createtables, deleteclient, deletenumber,
                        droptables, findclient, insertclient, insertnumber,
                        insertnumbers, selectall, updateclient)

def main():
    ''' В функции передается только курсор '''

    # password = 'Введите свой пароль'
    password = input('Введите пароль для clientbase:')
    try:
        conn = psycopg2.connect(database='clientbase', user='postgres', password=password)
        # psycopg2.connect

        with conn:
            with conn.cursor() as cur:
                droptables(cur)
                createtables(cur)

                print('id вносимых клиентов:')
                a1 = insertclient(cur, "myname", "mysurname", "email@aaa.aa")
                print(a1)
                a2 = insertclient(cur, 'name1', 'surname2', 'email2', '89167777777')
                print(a2)
                a3 = insertclient(cur, 'name2', 'surname3', 'email3')
                print(a3)
                a4 = insertclient(cur, 'name2', 'surname3', 'email4')
                print(a4)
                a5 = insertclient(cur, 'name2', 'surname4', 'email5')
                print(a5)

        with conn:
            with conn.cursor() as cur:
                # Функция, позволяющая добавить телефон для существующего клиента
                insertnumber(cur, a1, '55555555555')

                insertnumbers(cur, a3, ['81111111111', '82222222222', '83333333333', '55555555555'])

                # Функция, позволяющая изменить данные о клиенте
                print('\n Вносим изменения в клиента 5:')
                a = updateclient(cur, a5, email='email55')
                print('updateclient result:', a)

                print('\n Вносим клиента для удаления по имени "deletedname":')
                delclient_id = insertclient(cur, 'deletedname', 'deletednamesurname', 'deletednameemail', '888888888888')
                print('id deletedname:', delclient_id)

        with conn:
            with conn.cursor() as cur:
                result = selectall(cur)
                print('\n Вся таблица с телефонами:')
                print(*result, sep='\n')

        print('--Здесь удаляем клиента--\т')
        with conn:
            with conn.cursor() as cur:
                # Функция, позволяющая удалить телефон для существующего клиента
                deletenumber(cur, a3, number='83333333333')

                # Функция, позволяющая удалить существующего клиента
                deleteclient(cur, delclient_id)

        with conn:
            with conn.cursor() as cur:
                result = selectall(cur)
                print('\n Вся таблица с телефонами после удаления:')
                print(*result, sep='\n')

        with conn:
            with conn.cursor() as cur:
                print('\n ---------------------------------------------------')
                print('Поиск')
                # Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
                result = findclient(cur, number='55555555555')
                print('Запрос number=55555555555:')
                print(*result, sep='\n')
                result = findclient(cur, email='email2')
                print('Запрос email=email2:')
                print(*result, sep='\n')
                result = findclient(cur, name='name2', surname='surname3')
                print('Запрос name=name2, surname=surname3:')
                print(*result, sep='\n')

    except (Exception, Error) as error:
        print("Ошибка пр  работе с PostgreSQL", error)
    finally:
        if conn:
            # cur.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    main()
    # print(dir(onlycursor))
