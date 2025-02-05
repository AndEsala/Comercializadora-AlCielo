# Proyecto: Comercializadora de Productos
## Autor: Andrés Felipe Esala Muñoz
## Fecha: 05-02-2025
## Descripción: Prueba técnica para practicante en la empresa Al Cielo

# Instalaciones Necesarias
- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/stable/installation/#install-flask)
- [MySQL](https://www.mysql.com/downloads/)

# Dependencias y/o Librerías
- [Pandas](https://pandas.pydata.org)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [MySQL-Connector](https://dev.mysql.com/doc/connector-python/en/)
- [Plotly](https://plotly.com/python/)

# Automatización
## AddProductos.py
Este archivo permite agregar productos a la base de datos. Para ello, es necesario contar con un archivo de nombre `Producto.xlsx` con la siguiente estructura:

| CodProducto | NbrProducto | Subfamilia |
|-------------|-------------|------------|

Una vez se cuenta con el archivo, se debe ejecutar el archivo utilizando el comando:
~~~bash
python AddProductos.py
~~~

## AddTiendas.py
Este archivo permite agregar tiendas a la base de datos. Para ello, es necesario contar con un archivo de nombre `Tiendas.csv` con la siguiente estructura:

| Codigo| NombreTienda | CodigoPostal | Latitud | Longitud | m2_superficie | Empleados | AlquilerBase | AlquilerAnoContrato |
|-------|--------------|--------------|---------|----------|---------------|-----------|--------------|---------------------|

Una vez se cuenta con el archivo, se debe ejecutar el archivo utilizando el comando:
~~~bash
python AddTiendas.py
~~~

## RegistrarVentas.py
Este archivo permite registrar ventas en la base de datos. Para ello, es necesario contar con un archivo de nombre `Ventas.xslx` con la siguiente estructura:

| Ticket | Fecha | Linea | CodProducto | Cantidad | ValorUnitario | CodTienda|
|--------|-------|-------|-------------|----------|---------------|----------|

Una vez se cuenta con el archivo, se debe ejecutar el archivo utilizando el comando:
~~~bash
python RegistrarVentas.py
~~~

# Sitio Web
## Base de Datos
Para el correcto funcionamiento de la base de datos, se debe crear una base de datos con el nombr de `comercializadora` e importar el archivo `comercializadora.sql` que se encuentra en la raíz de la carpeta.

## Ejecución
Para ejecutar el sitio web, se debe ejecutar el archivo `aplication.py` utilizando los siguientes comandos:
~~~bash
cd website
.venv\Scripts\activate
flask --app aplication run
~~~