import csv
import mariadb


# CreO la base de datos localidades
def createdb():
    conn = mariadb.connect(user="root", password="root", host="localhost")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS localidades")
    cursor.execute("USE localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute(
        "CREATE TABLE provincias(provincia VARCHAR(255), id INT, localidad VARCHAR(255), cp INT, id_prov_mstr INT)"
    )

        #leo datos e inserto los datos en la tabla 
    with open("localidades.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Saltar la primera fila si contiene los nombres de las columnas
        for row in csv_reader:
            # Verificar cada valor en la fila
            row = [value if value != '' else '0' for value in row]  # Reemplaza '' por '0'
            sql = "INSERT INTO provincias (provincia, id, localidad, cp, id_prov_mstr) VALUES  (%s, %s, %s, %s, %s)"
            cursor.execute(sql, row)
    conn.commit()

    return conn, cursor

# Traigo el cursor para usarlo en otras partes del codigo
conn, cursor = createdb()


def crearArchivos():
    with open("localidades.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        provincias_list = []
        for row in csv_reader:
            provincias_list.append(row[0])
    provincias_list.remove("provincia")
    provincias_cleaned = sorted(set(provincias_list))

    for provincia in provincias_cleaned:
        sql = "SELECT * FROM provincias WHERE provincia = '%s';"
        cursor.execute(sql % provincia)

        # Obtener el resultado de la consulta
        datos = cursor.fetchall()
        print(provincia, datos)

        with open((str(provincia) + ".csv"), "w", encoding="utf8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(datos)

#Funcion para ejecutar el programa
def main():
    createdb()
    crearArchivos()
    conn.close()

#Ejecutamos la funcion
main()

