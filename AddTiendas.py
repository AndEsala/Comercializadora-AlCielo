""" 
Leer archivo Tiendas.csv y agregar tiendas a la base de datos. 
- La base de datos está hechah en MySQL.
- La tabla se llama tiendas.
- La base de datos se llama comercializadora.
- La tabla tiendas tiene los siguientes campos:
    - cod_tienda: INT
    - nombre: VARCHAR(60)
    - codigo_postal: LONG
    - latitud: FLOAT
    - longitud: FLOAT
    - superficie_m2: FLOAT
    - empleados: INT
    - alquiler_base: FLOAT
    - alquiler_ano_contrato: INT
"""

import pandas as pd
import mysql.connector as mysql

# Leer archivo Tiendas.csv
df = pd.read_csv('Tiendas.csv', sep = ';')

# Corregir Formato
def limpiarFormatoMoneda(valor):
    if isinstance(valor, str):
        valor = valor.replace(",", "").replace(".", "").replace("$ ", "")

        if valor.isnumeric():
            return int(valor)
    
    return valor

# Aplicar función limpiarFormatoMoneda a la columna AlquilerBase
df['AlquilerBase'] = df['AlquilerBase'].apply(limpiarFormatoMoneda)

try:
    # Conexión a la base de datos
    conn = mysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'comercializadora')
    cursor = conn.cursor()
    insertQuery = "INSERT INTO tiendas (cod_tienda, nombre, codigo_postal, superficie_m2, empleados, alquiler_base, alquiler_ano_contrato) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    # Agregar tiendas a la base de datos
    for _, row in df.iterrows():
        cursor.execute(insertQuery, ((row['Codigo']), row['NombreTienda'], row['CodigoPostal'], row['m2_superficie'], row['Empleados'], row['AlquilerBase'], row['AlquilerAnoContrato']))
    
    conn.commit()
except Exception as e:
    print(f'Error: {e}')
finally:
    cursor.close()
    conn.close()