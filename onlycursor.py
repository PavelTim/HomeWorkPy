# Функция, создающая структуру БД (таблицы)
def createtables(cur):
    ''' создает таблицы '''
    cur.execute("""CREATE TABLE IF NOT EXISTS client (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(50) NOT NULL,
    client_surname VARCHAR(60) NOT NULL,
    client_email VARCHAR(60) NOT NULL);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS telephon (
    id SERIAL PRIMARY KEY,
    num VARCHAR(15) NOT NULL,
    client_id INTEGER REFERENCES client(id));""")


def droptables(cur):
    ''' DROP tables client and telephon '''
    cur.execute("""DROP TABLE telephon;""")
    cur.execute("""DROP TABLE client;""")


def cleartables(cur):
    """ delete all data in tables client and telefon """
    cur.execute("""DELETE  FROM telephon;""")
    cur.execute("""DELETE  FROM client;""")


def selectall(cur):
    """ select all data in tables client and telefon """
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
def insertclient(cur, name, surname, email, number=None):
    """ client: name: str, surname: str, email: str """
    cur.execute("""INSERT INTO client(client_name, client_surname, client_email)
        VALUES (%s, %s, %s) RETURNING id;""", (name, surname, email))
    result = cur.fetchone()[0]
    if number:
        cur.execute("""INSERT INTO telephon(num, client_id)
                    VALUES (%s, %s)""", (number, result))
    return result


# Функция, позволяющая добавить телефон для существующего клиента
def insertnumber(cur, client_id, number: str):
    """ insert telephon number """
    cur.execute("""INSERT INTO telephon(num, client_id)
        VALUES
        (%s, %s) RETURNING id;""", (number, client_id))
    result = cur.fetchone()
    return result


def insertnumbers(cur, client_id, numbers: list):
    """ insertnumbers(cur, client_id, numbers: list) """
    for number in numbers:
        cur.execute("""INSERT INTO telephon(num, client_id)
            VALUES
            (%s, %s);""", (number, client_id))


# Функция, позволяющая изменить данные о клиенте
def updateclient(cur, id_client: int, name=None, surname=None, email=None):
    """ Update client Исправленная версия """
    if name:
        cur.execute("""UPDATE client
                    SET client_name = %s
                    WHERE id = %s;""", (name, id_client))
    if surname:
        cur.execute("""UPDATE client
                    SET client_surname = %s
                    WHERE id = %s;""", (surname, id_client))
    if email:
        cur.execute("""UPDATE client
                    SET client_email = %s
                    WHERE id = %s;""", (email, id_client))

    result = cur.statusmessage
    return result

# Функция, позволяющая удалить телефон для существующего клиента
def deletenumber(cur, id, number=None):
    """ DELETE telephon number """
    if number is None:
        cur.execute("""DELETE FROM telephon
            WHERE client_id = %s;""", (id,))
    else:
        cur.execute("""DELETE FROM telephon
                    WHERE client_id = %s AND num = %s;""", (id, number))
        result = cur.statusmessage
    return result


# Функция, позволяющая удалить существующего клиента
def deleteclient(cur, id: int):
    """ delete client """
    cur.execute("""DELETE FROM telephon WHERE client_id = %s;""", (id,))
    cur.execute("""DELETE FROM client WHERE id = %s;""", (id,))


# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def findclient(cur, *, name=None, surname=None, email=None, number=None):
    """ search telephon number cur: cursor, name=None, surname=None, email=None, number=None """
    cur.execute("""SELECT client.id, client_name, client_surname, client_email, num
        FROM client JOIN telephon
        ON client.id = telephon.client_id
        WHERE 
            client_email = %s OR
            num = %s OR
            client_name = %s AND client_surname = %s;""", (email, number, name, surname))
    result = cur.fetchall()
    return result