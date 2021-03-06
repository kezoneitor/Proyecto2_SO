import psycopg2
import sys

local = 'localhost'

def readFile(uri):
    archivo = ""
    try:
        archivo = open(uri, "rb")
        img = archivo.read()
        return img

    except IOError as e:
        print("Error readFile: %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if archivo:
            archivo.close()

def writeImage(name_dir, id):
    #Conexión a la DB
    conexion = "host='"+local+"' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()
    img = readFile(name_dir+id)
    try:
        #Obtiene la información y la inserta en la DB
        binary = psycopg2.Binary(img)
        objCursor.execute("INSERT INTO imagenes(imagen, id) VALUES (%s, %s)", (binary, id))
        obj.commit()

    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error writeImage: %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()

def readImage(name_dir, init, end):
    # Conexión a la DB
    conexion = "host='"+local+"' dbname='ProyectoSO2' user='postgres' password='12345'"
    obj = psycopg2.connect(conexion)
    objCursor = obj.cursor()

    try:
        # Obtiene los valores de la DB
        objCursor.execute("SELECT * FROM imagenes ORDER BY id", (end, init))
        list_img = []
        for r in objCursor.fetchall():
            open(name_dir+r[1], 'wb').write(bytes(r[0]))
            list_img.append([name_dir,r[1]])
        return list_img

    except psycopg2.DatabaseError as e:
        if obj:
            obj.rollback()

        print('Error readImage: %s' % e)
        sys.exit(1)

    finally:
        if obj:
            obj.close()
            objCursor.close()

def sizeRegisters():
    # Conexión a la DB
    conexion = "host='"+local+"' dbname='ProyectoSO2' user='postgres' password='12345'"
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