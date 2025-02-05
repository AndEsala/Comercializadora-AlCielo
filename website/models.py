from database import db

class Tienda(db.Model):
    __tablename__ = 'tiendas'
    cod_tienda = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(60), nullable = False)
    codigo_postal = db.Column(db.String(10), nullable = False)
    latitud = db.Column(db.Numeric(10, 6), nullable = False)
    longitud = db.Column(db.Numeric(10, 6), nullable = False)
    superficie_m2 = db.Column(db.Float, nullable = False)
    empleados = db.Column(db.Integer, nullable = False)
    alquiler_base = db.Column(db.Float, nullable = False)
    alquiler_ano_contrato = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            'cod_tienda': self.cod_tienda,
            'nombre': self.nombre,
            'codigo_postal': self.codigo_postal,
            'latitud': float(self.latitud),
            'longitud': float(self.longitud),
            'superficie_m2': float(self.superficie_m2),
            'empleados': self.empleados,
            'alquiler_base': float(self.alquiler_base),
            'alquiler_ano_contrato': self.alquiler_ano_contrato
        }
    
class Producto(db.Model):
    __tablename__ = 'productos'
    cod_producto = db.Column(db.String, primary_key = True)
    nombre = db.Column(db.String(60), nullable = False)
    subfamilia = db.Column(db.String(60), nullable = False)

    def to_dict(self):
        return {
            'cod_producto': self.cod_producto,
            'nombre': self.nombre,
            'subfamilia': self.subfamilia
        }
    
class Venta(db.Model):
    __tablename__ = 'ventas'
    id_venta = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date, nullable = True, default = db.func.current_date())
    cod_producto = db.Column(db.String, db.ForeignKey('productos.cod_producto'), nullable = False)
    producto = db.relationship('Producto', backref = db.backref('ventas', lazy = True))
    cantidad = db.Column(db.Integer, nullable = False)
    valor_unitario = db.Column(db.Float, nullable = False)
    cod_tienda = db.Column(db.Integer, db.ForeignKey('tiendas.cod_tienda'), nullable = False)
    tienda = db.relationship('Tienda', backref = db.backref('ventas', lazy = True))

    def to_dict(self):
        return {
            'id_venta': self.id_venta,
            'ticket': self.ticket,
            'fecha': str(self.fecha),
            'linea': self.linea,
            'producto': self.producto.to_dict(),
            'cantidad': self.cantidad,
            'valor_unitario': float(self.valor_unitario),
            'tienda': self.tienda.to_dict()
        }