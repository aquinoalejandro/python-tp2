from ast import parse
import csv 
import mariadb
import os


def createdb():
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS localidades")
    cursor.execute("USE localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute("CREATE TABLE provincias(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,nombre VARCHAR(255), localidad VARCHAR(255), id_provincia INT, codigo_postal INT, id_prov_mstr INT)")
    conn.commit()
    cursor.close()
    conn.close()


createdb()

def insertar():
    with open('localidades.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        provincias_list = []
        for row in csv_reader:
            provincias_list.append(row[0])
    provincias_list.remove('provincia')
    provincias_cleaned = sorted(set(provincias_list))
    
    for provincia in provincias_cleaned:
        with open((str(provincia)+'.csv'), 'w', encoding='utf8') as csv_file:
            pass

insertar()





            