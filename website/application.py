import pandas as pd
import plotly.express as px
from database import init_db, db
from sqlalchemy import create_engine, desc
from flask import Flask, render_template, redirect, url_for, request
from models import Tienda, Producto, Venta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/comercializadora'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

@app.route('/', methods = ['GET'])
def hello_world():
    dfTiendas = getDataTiendas()
    dfProductos = getDataProductos()

    """ dfTendencia["total_ventas"] = pd.to_numeric(dfTendencia["total_ventas"]) """

    figTiendas = px.bar(dfTiendas, x = 'tienda', y = 'ingresos', title = 'Tiendas con Mayores Ingresos')
    figProductos = px.bar(dfProductos, x = 'producto', y = 'cantidad_vendida', title = 'Productos Más Vendidos')
    """ figTendencia = px.line(dfTendencia, x = 'mes', y = 'total_ventas', title = 'Tendencia de Ventas Mensuales')
    figTendencia.update_layout(xaxis_title = 'Mes', yaxis_title = 'Total Ventas', xaxis = dict(tickmode = "linear")) """

    graphTiendas = figTiendas.to_html(full_html = False)
    graphProductos = figProductos.to_html(full_html = False)
    """ graphTendencia = figTendencia.to_html(full_html = False) """

    return render_template('dashboard.html', graphTiendas = graphTiendas, graphProductos = graphProductos)

@app.route('/ventas', methods = ['GET'])
def ventas():
    ventas = Venta.query.order_by(desc(Venta.fecha)).limit(50).all()
    tiendas = Tienda.query.all()
    productos = Producto.query.all()
    return render_template('ventas.html', ventas = ventas, tiendas = tiendas, productos = productos)

@app.route('/tiendas', methods = ['GET'])
def tiendas():
    tiendas = Tienda.query.all()
    return render_template('tiendas.html', tiendas = tiendas)

@app.route('/productos', methods = ['GET'])
def productos():
    productos = Producto.query.order_by(desc(Producto.cod_producto)).limit(50).all()
    return render_template('productos.html', productos = productos)

@app.route('/ventas', methods = ['POST'])
def add_venta():
    cod_producto = request.form['producto']
    cantidad = request.form['cantidad']
    valor_unitario = request.form['valor_unitario']
    cod_tienda = request.form['tienda']

    # Validar que la cantidad sea un número entero
    try:
        cantidad = int(cantidad)
    except:
        return redirect(url_for('ventas'))
    
    # Validar que el valor unitario sea un número decimal
    try:
        valor_unitario = float(valor_unitario)
    except:
        return redirect(url_for('ventas'))
    
    # Validar que el producto y la tienda existan
    producto = Producto.query.filter_by(cod_producto = cod_producto).first()
    tienda = Tienda.query.filter_by(cod_tienda = cod_tienda).first()

    if producto is None or tienda is None:
        return redirect(url_for('ventas'))

    venta = Venta(cod_producto = cod_producto, cantidad = cantidad, valor_unitario = valor_unitario, cod_tienda = cod_tienda)
    db.session.add(venta)
    db.session.commit()

    return redirect(url_for('ventas'))

def getDataTiendas():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/comercializadora')

    # Consulta para obtener los ingresos de cada tienda
    dfTiendas = pd.read_sql_query(""" 
        SELECT t.nombre AS tienda, SUM(v.cantidad * v.valor_unitario) AS ingresos
        FROM ventas v
        JOIN tiendas t ON v.cod_tienda = t.cod_tienda
        GROUP BY t.nombre ORDER BY ingresos DESC
    """, con = engine)

    engine.dispose()
    return dfTiendas

def getDataProductos():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/comercializadora')

    # Consulta para obtener los Productos más Vendidos
    dfProductos = pd.read_sql_query(""" 
        SELECT p.nombre AS producto, SUM(v.cantidad) AS cantidad_vendida
        FROM ventas v
        JOIN productos p ON v.cod_producto = p.cod_producto
        GROUP BY p.nombre ORDER BY cantidad_vendida DESC
    """, con = engine)

    engine.dispose()
    return dfProductos

def getDataTendencia():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/comercializadora')

    # Consulta para obtener una Tendencia de Ventas Mensuales
    dfTendencia = pd.read_sql_query(""" 
        SELECT DATE_FORMAT(fecha, '%Y-%m') AS mes FROM ventas GROUP BY mes ORDER BY mes
    """, con = engine)

    engine.dispose()
    return dfTendencia

if __name__ == '__main__':
    app.run(debug = True)