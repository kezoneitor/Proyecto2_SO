import psycopg2
import sys

def readImage(name_dir, init, end):
    # Conexión a la DB
    conexion = "host='localhost' dbname='ProyectoSO2' user='postgres' password='12345'"
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

readImage("./img/", 0, 0)