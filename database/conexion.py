import psycopg2
import sys
import pprint

def readImage():
    # Conexión a la DB
    conexion = "host='localhost' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()

    try:
        # Obtiene los valores de la DB
        objCursor.execute("select * from imagenes")
        registros = objCursor.fetchone()
        pprint.pprint(registros[0])

    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()

def writeImage(img, id):

    #Conexión a la DB
    conexion = "host='localhost' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()

    try:

        #Obtiene la información y la inserta en la DB
        #data = readImage()
        binary = psycopg2.Binary(img)
        objCursor.execute("INSERT INTO imagenes(imagen, id) VALUES (%s, %s)", (binary, id))
        obj.commit()

    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()

def sizeRegisters():
    # Conexión a la DB
    conexion = "host='localhost' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()

    try:
        # Obtiene los valores de la DB
        objCursor.execute("select count(id) from imagenes")
        registros = objCursor.fetchone()
        return registros[0]

    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()