import psycopg2
from psycopg2 import Error


# Функция, создающая структуру БД (таблицы)
def createtables(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS client (
        id SERIAL PRIMARY KEY,
        client_name VARCHAR(50) NOT NULL,
        client_surname VARCHAR(60) NOT NULL,
        client_email VARCHAR(60) NOT NULL);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS telephon (
        id SERIAL PRIMARY KEY,
        num VARCHAR(15) NOT NULL,
        client_id INTEGER REFERENCES client(id));""")
        conn.commit()


def droptables(conn):
    ''' DROP tables client and telephon '''
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE telephon;""")
        cur.execute("""DROP TABLE client;""")
        conn.commit()


def cleartables(conn):
    """ delete all data in tables client and telefon """
    with conn.cursor() as cur:
        cur.execute("""DELETE  FROM telephon;""")
        cur.execute("""DELETE  FROM client;""")
        conn.commit()

def selectall(conn):
    """ select all data in tables client and telefon """
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                            client.id, 
                            client.client_name, 
                            client.client_surname,
                            client.client_email,
                            telephon.num
                        FROM client LEFT JOIN telephon
                                ON client.id = telephon.client_id
                        ORDER BY client.id;""")
        result = cur.fetchall()
    return result


# Функция, позволяющая добавить нового клиента
def insertclient(conn, name, surname, email, number=None):
    """ client: name: str, surname: str, email: str """
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO client(client_name, client_surname, client_email)
            VALUES (%s, %s, %s) RETURNING id;""", (name, surname, email))
        conn.commit()
        result = cur.fetchone()[0]
        if number:
            cur.execute("""INSERT INTO telephon(num, client_id)
                        VALUES (%s, %s)""", (number, result))
    return result


# Функция, позволяющая добавить телефон для существующего клиента
def insertnumber(conn, client_id, number: str):
    """ insert telephon number """
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO telephon(num, client_id)
            VALUES
            (%s, %s) RETURNING id;""", (number, client_id))
        conn.commit()
        result = cur.fetchone()
    return result


def insertnumbers(conn, client_id, numbers: list):
    """ insertnumbers(conn, client_id, numbers: list) """
    with conn.cursor() as cur:
        for number in numbers:
            cur.execute("""INSERT INTO telephon(num, client_id)
                VALUES
                (%s, %s);""", (number, client_id))
        conn.commit()

# Функция, позволяющая изменить данные о клиенте
def updateclient(conn, id_client: int, name=None, surname=None, email=None):
    """ Update client """
    with conn.cursor() as cur:
        cur.execute("""SELECT client_name, client_surname, client_email FROM client
        WHERE id = %s """, (id_client,))
        result = cur.fetchone()
        print('updateclient result:', result)
        if name is None:
            name = result[0]
        if surname is None:
            surname = result[1]
        if email is None:
            email = result[2]

        cur.execute("""UPDATE client
            SET client_name = %s, client_surname = %s, client_email = %s
            WHERE id = %s;""", (name, surname, email, id_client))
        conn.commit()
        result = cur.statusmessage
    return result


# Функция, позволяющая удалить телефон для существующего клиента
def deletenumber(conn, id, number=None):
    """ DELETE telephon number """
    with conn.cursor() as cur:
        if number is None:
            cur.execute("""DELETE FROM telephon
                WHERE client_id = %s;""", (id,))
        else:
            cur.execute("""DELETE FROM telephon
                        WHERE client_id = %s AND num = %s;""", (id, number))
        conn.commit()
        result = cur.statusmessage
    return result


# Функция, позволяющая удалить существующего клиента
def deleteclient(conn, id: int):
    """ delete client """
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM telephon WHERE client_id = %s;""", (id,))
        cur.execute("""DELETE FROM client WHERE id = %s;""", (id,))
        conn.commit()


# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def findclient(conn, *, name=None, surname=None, email=None, number=None):
    """ search telephon number cur: cursor, name=None, surname=None, email=None, number=None """
    with conn.cursor() as cur:
        cur.execute("""SELECT client.id, client_name, client_surname, client_email, num
            FROM client JOIN telephon
            ON client.id = telephon.client_id
            WHERE 
                client_email = %s OR
                num = %s OR
                client_name = %s AND client_surname = %s;""", (email, number, name, surname))
        result = cur.fetchall()
    return result

if __name__ == '__main__':
    # password = 'Введите свой пароль'
    password = input('Введите пароль для clientbase:')
    try:
        conn = psycopg2.connect(database='clientbase', user='postgres', password=password)

        droptables(conn)
        createtables(conn)

        print('id вносимых клиентов:')
        a1 = insertclient(conn, "myname", "mysurname", "email@aaa.aa")
        print(a1)
        a2 = insertclient(conn, 'name1', 'surname2', 'email2', '89167777777')
        print(a2)
        a3 = insertclient(conn, 'name2', 'surname3', 'email3')
        print(a3)
        a4 = insertclient(conn, 'name2', 'surname3', 'email4')
        print(a4)
        a5 = insertclient(conn, 'name2', 'surname4', 'email5')
        print(a5)
        # cleartables(conn):

        # Функция, позволяющая добавить телефон для существующего клиента
        insertnumber(conn, a1, '55555555555')

        insertnumbers(conn, a3, ['81111111111', '82222222222', '83333333333', '55555555555'])

        # Функция, позволяющая изменить данные о клиенте
        print('\n Вносим изменения в клиента 5:')
        a = updateclient(conn, a5, email='email55')
        print('updateclient result:', a)

        print('\n Вносим клиента для удаления по имени "deletedname":')
        delclient_id = insertclient(conn, 'deletedname', 'deletednamesurname', 'deletednameemail', '888888888888')
        print('id deletedname:', delclient_id)

        result = selectall(conn)
        print('\n Вся таблица с телефонами:')
        print(*result, sep='\n')

        # Функция, позволяющая удалить телефон для существующего клиента
        deletenumber(conn, a3, number='83333333333')

        # Функция, позволяющая удалить существующего клиента
        deleteclient(conn, delclient_id)

        result = selectall(conn)
        print('\n Вся таблица с телефонами после удаления:')
        print(*result, sep='\n')

        print('\n ---------------------------------------------------')
        print('Поиск')
        # Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
        result = findclient(conn, number='55555555555')
        print('Запрос number=55555555555:')
        print(*result, sep='\n')
        result = findclient(conn, email='email2')
        print('Запрос email=email2:')
        print(*result, sep='\n')
        result = findclient(conn, name='name2', surname='surname3')
        print('Запрос name=name2, surname=surname3:')
        print(*result, sep='\n')

    except (Exception, Error) as error:
        print("Ошибка пр  работе с PostgreSQL", error)
    finally:
        if conn:
            # cur.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")