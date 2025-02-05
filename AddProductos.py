""" 
Leer archivo Productos.xlsx y agregar productos a la base de datos. 
- La base de datos está hechah en MySQL.
- La tabla se llama productos.
- La base de datos se llama comercializadora.
- La tabla productos tiene los siguientes campos:
    - cod_producto: Varchar(10)
    - nombre: VARCHAR(60)
    - subfamilia: INT
"""

import pandas as pd
import mysql.connector as mysql

# Leer archivo Productos.xlsx
df = pd.read_excel('Productos.xlsx')

try: 
    # Conexión a la base de datos
    conn = mysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'comercializadora')
    cursor = conn.cursor()
    insertQuery = "INSERT INTO productos (cod_producto, nombre, subfamilia) VALUES (%s, %s, %s);"

    # Agregar productos a la base de datos
    for _, row in df.iterrows():
        cursor.execute(insertQuery, (row['CodProducto'], row['NbrProducto'], row['Subfamilia']))
        
    conn.commit()
    print('Productos agregados a la base de datos.')
except Exception as e:
    print(f'Error: {e}')
finally:
    cursor.close()
    conn.close()