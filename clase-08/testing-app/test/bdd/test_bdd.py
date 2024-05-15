import mysql.connector
import os

def verifyUserTable():
    print("BDD")
    connection = None

    try:
        if os.environ.get('FLASK_ENV') == 'testing':
            print("AMBIENTE PRUEBA BDD: TESTING")
            connection = mysql.connector.connect(
                host="db_test",
                port=3306,
                user="testing",
                password="testing",
                database="testing"
            )
        else:
            print("AMBIENTE PRUEBA BDD: DEVELOMPENT")
            connection = mysql.connector.connect(
                host="db",
                user="testing",
                password="testing",
                database="development"
            )

        cursor = connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'user'")
        userTable = cursor.fetchone()

        if userTable:
            print("Tabla user OK")
            assert(True)
        else:
            print("No se encontro la tabla User")
            assert(False)

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if connection:
            connection.close()

verifyUserTable()