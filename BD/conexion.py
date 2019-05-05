import psycopg2
import sys
import pprint

def readImage():

    archivo = ""
    try:
        archivo = open("tatuaje 3.jpg", "rb")
        img = archivo.read()
        return img

    except IOError as e:
        print ("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)

    finally:
        if archivo:
            archivo.close()

def main():

    #Conexión a la DB
    conexion = "host='localhost' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()

    try:

        #Obtiene la información y la inserta en la DB
        data = readImage()
        binary = psycopg2.Binary(data)
        objCursor.execute("INSERT INTO imagenes(imagen) VALUES (%s)", (binary,))
        obj.commit()

        #Obtiene los valores de la DB
        objCursor.execute("select * from imagenes")
        registros = objCursor.fetchall()
        pprint.pprint(registros)


    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()


main()