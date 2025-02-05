""" 
Leer archivo Ventas.xlsx y registrar las ventas a la base de datos. 
- El archivo contiene una hoja por cada trimestre del año.
- La base de datos está hecha en MySQL.
- La tabla se llama ventas.
- La base de datos se llama comercializadora.
- La tabla ventas tiene los siguientes campos:
    - id_venta: INT (autoincremental)
    - ticket: VARCHAR(20)
    - fecha: DATE
    - linea: LONG
    - cod_producto: INT (clave foránea, referencia a la tabla productos. Es necesario validar si el producto existe en la tabla productos)
    - cantidad: INT
    - valor_unitario: FLOAT
    - cod_tienda: INT (clave foránea, referencia a la tabla tiendas. Es necesario validar si la tienda existe en la tabla tiendas)
"""

import pandas as pd
import mysql.connector as mysql

# Leer archivo Ventas.xlsx
xls = pd.ExcelFile('Ventas.xlsx')

try:
    # Conexión a la base de datos
    conn = mysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'comercializadora')
    cursor = conn.cursor()
    insertQuery = "INSERT INTO ventas (ticket, fecha, linea, cod_producto, cantidad, valor_unitario, cod_tienda) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    # Agregar ventas a la base de datos
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name = sheet)

        for _, row in df.iterrows():
            # Validar si el producto existe en la tabla productos
            cursor.execute(f"SELECT * FROM productos WHERE cod_producto = {row['CodProducto']}")
            if cursor.fetchone() is None:
                print(f'Producto {row["CodProducto"]} no existe en la tabla productos.')
                continue

            # Validar si la tienda existe en la tabla tiendas
            cursor.execute(f"SELECT * FROM tiendas WHERE cod_tienda = {row['CodTienda']}")
            if cursor.fetchone() is None:
                print(f'Tienda {row["CodTienda"]} no existe en la tabla tiendas.')
                continue
            
            fecha = row['Fecha'].to_pydatetime().strftime('%Y-%m-%d')
            cursor.execute(insertQuery, (row['Ticket'], fecha, row['Linea'], row['CodProducto'], row['Cantidad'], row['ValorUnitario'], row['CodTienda']))

    conn.commit()
    print('Ventas registradas en la base de datos.')
except Exception as e:
    print(f'Error: {e}')
finally:
    cursor.close()
    conn.close()