import glob
import json
import mysql.connector

conexion = mysql.connector.connect(
    user='rob',
    password='12345',
    database='casas')
cursor = conexion.cursor()

files = glob.glob('*.json')

tipo = {'venta': 1, 'renta': 2}
origen = {'informador': 1}

def existe_municipio(casa):
    select = 'SELECT * from municipio WHERE nombre = %s'
    cursor.execute(select, (casa['ubicacion'],))

    rows = cursor.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False
def insertar_municipio(casa):
    insert = 'INSERT INTO municipio(nombre) VALUES(%s)'
    cursor.execute(insert, (casa['ubicacion'],))
    conexion.commit()
    return cursor.lastrowid
def existe_colonia(casa):
    select = 'SELECT * from colonia WHERE nombre = %s'
    cursor.execute(select, (casa['colonia'],))

    rows = cursor.fetchall()
    if len(rows) > 0:
        for colonia in rows:
            if colonia[2] == get_id_municipio(casa['ubicacion']):
                return True
        return False
    else:
        return False
def insertar_colonia(casa, id_muni):
    insert = 'INSERT INTO colonia(nombre, id_municipio) VALUES(%s, %s)'
    cursor.execute(insert, (casa['colonia'], id_muni))
    conexion.commit()
    return cursor.lastrowid

def existe_fecha(file):
    select = 'SELECT * from fecha WHERE fecha = %s'
    cursor.execute(select, (file[:-5],))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False
def insertar_fecha(file):
    insert = 'INSERT INTO fecha(fecha) VALUES(%s)'
    cursor.execute(insert, (file[:-5],))
    return cursor.lastrowid

def insertar_imagen(url, id_casa):
    insert = 'INSERT INTO imagen(ubicacion, id_bienraiz) VALUES (%s, %s)'
    cursor.execute(insert, (url, id_casa))
    conexion.commit()

def insertar_bienraiz(casa, id_colonia, id_fecha):
    insert = 'INSERT INTO bienraiz(titulo, ' \
             'precio, m2, m2_2, rooms, baths, cars, ' \
             'descripcion, id_tipo,' \
             'id_origen, id_colonia, id_fecha ) ' \
             'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(insert, (casa['titulo'],
                            casa['precio'][1:],
                            casa['m2'],
                            casa['m2_2'],
                            casa['recamaras'],
                            casa['wc'],
                            casa['cars'],
                            casa['descripcion'],
                            1,
                            1,
                            id_colonia,
                            id_fecha))
    conexion.commit()
    id_casa = cursor.lastrowid
    for img in casa['imgs']:
        insertar_imagen(img, id_casa)


def get_id_colonia(colonia, municipio):
    select = 'SELECT * from colonia WHERE nombre = %s'
    cursor.execute(select, (colonia,))

    rows = cursor.fetchall()
    for colonia in rows:
        if colonia[2] == get_id_municipio(municipio):
            return colonia[0]
def get_id_fecha(fecha):
    select = 'SELECT id from fecha WHERE fecha = %s'
    cursor.execute(select, (fecha,))
    rows = cursor.fetchall()
    return rows[0][0]
def get_id_municipio(municipio):
    select = 'SELECT id from municipio WHERE nombre = %s'
    cursor.execute(select, (municipio,))

    rows = cursor.fetchall()
    return rows[0][0]

for file in files:
    with open(file, encoding='utf-8') as f:
        casas = json.load(f)
        for casa in casas:
            id_muni = 0
            id_col = 0
            id_fecha = 0
            if not existe_municipio(casa):
                id_muni = insertar_municipio(casa)
            else:
                id_muni = get_id_municipio(casa['ubicacion'])
            if not existe_colonia(casa):
                id_col = insertar_colonia(casa, id_muni)
            else:
                id_col = get_id_colonia(casa['colonia'],
                                        casa['ubicacion'])
            if not existe_fecha(file):
                id_fecha = insertar_fecha(file)
            else:
                id_fecha = get_id_fecha(file[:-5])

            insertar_bienraiz(casa, id_col, id_fecha)