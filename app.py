from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
db = SQLAlchemy()
# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estacionamiento.db'
db.init_app(app)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(7), unique=True, nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    # Relación uno a muchos: Un vehículo puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='vehiculo', lazy=True)

class Espacio(db.Model):
    __tablename__ = 'espacios'
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(100), nullable=False)
    ocupado = db.Column(db.Boolean, default=False, nullable=False)
    # Relación uno a muchos: Un espacio puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='espacio', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora_entrada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_hora_salida = db.Column(db.DateTime, nullable=True)
    total_pagar = db.Column(db.Float, nullable=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)

@app.route('/vehiculos', methods=['GET'])
def obtener_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([{'id': vehiculo.id, 'placa': vehiculo.placa, 'marca': vehiculo.marca, 'modelo': vehiculo.modelo, 'color': vehiculo.color} for vehiculo in vehiculos])

@app.route('/vehiculos', methods=['POST'])
def crear_vehiculo():
    if not request.json or not 'placa' in request.json:
        abort(400)
    vehiculo = Vehiculo(placa=request.json['placa'], marca=request.json['marca'], modelo=request.json['modelo'], color=request.json['color'])
    db.session.add(vehiculo)
    db.session.commit()
    return jsonify({'id': vehiculo.id, 'placa': vehiculo.placa, 'marca': vehiculo.marca, 'modelo': vehiculo.modelo, 'color': vehiculo.color}), 201

@app.route('/vehiculos/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify({'id': vehiculo.id, 'placa': vehiculo.placa, 'marca': vehiculo.marca, 'modelo': vehiculo.modelo, 'color': vehiculo.color})

@app.route('/vehiculos/<int:id>', methods=['PUT'])
def actualizar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    if not request.json:
        abort(400)
    vehiculo.placa = request.json.get('placa', vehiculo.placa)
    vehiculo.marca = request.json.get('marca', vehiculo.marca)
    vehiculo.modelo = request.json.get('modelo', vehiculo.modelo)
    vehiculo.color = request.json.get('color', vehiculo.color)
    db.session.commit()
    return jsonify({'id': vehiculo.id, 'placa': vehiculo.placa, 'marca': vehiculo.marca, 'modelo': vehiculo.modelo, 'color': vehiculo.color})

@app.route('/vehiculos/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/espacios', methods=['GET'])
def obtener_espacios():
    espacios = Espacio.query.all()
    return jsonify([{'id': espacio.id, 'ubicacion': espacio.ubicacion, 'ocupado': espacio.ocupado} for espacio in espacios])

@app.route('/espacios', methods=['POST'])
def crear_espacio():
    if not request.json or not 'ubicacion' in request.json:
        abort(400)
    espacio = Espacio(ubicacion=request.json['ubicacion'], ocupado=request.json.get('ocupado', False))
    db.session.add(espacio)
    db.session.commit()
    return jsonify({'id': espacio.id, 'ubicacion': espacio.ubicacion, 'ocupado': espacio.ocupado}), 201

@app.route('/espacios/<int:id>', methods=['GET'])
def obtener_espacio(id):
    espacio = Espacio.query.get_or_404(id)
    return jsonify({'id': espacio.id, 'ubicacion': espacio.ubicacion, 'ocupado': espacio.ocupado})

@app.route('/espacios/<int:id>', methods=['PUT'])
def actualizar_espacio(id):
    espacio = Espacio.query.get_or_404(id)
    if not request.json:
        abort(400)
    espacio.ubicacion = request.json.get('ubicacion', espacio.ubicacion)
    espacio.ocupado = request.json.get('ocupado', espacio.ocupado)
    db.session.commit()
    return jsonify({'id': espacio.id, 'ubicacion': espacio.ubicacion, 'ocupado': espacio.ocupado})

@app.route('/espacios/<int:id>', methods=['DELETE'])
def eliminar_espacio(id):
    espacio = Espacio.query.get_or_404(id)
    db.session.delete(espacio)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/tickets', methods=['GET'])
def obtener_tickets():
    tickets = Ticket.query.all()
    return jsonify([{'id': ticket.id, 'fecha_hora_entrada': ticket.fecha_hora_entrada, 'fecha_hora_salida': ticket.fecha_hora_salida, 'total_pagar': ticket.total_pagar, 'vehiculo_id': ticket.vehiculo_id, 'espacio_id': ticket.espacio_id} for ticket in tickets])

@app.route('/tickets', methods=['POST'])
def crear_ticket():
    if not request.json or not 'vehiculo_id' in request.json or not 'espacio_id' in request.json:
        abort(400)
    ticket = Ticket(fecha_hora_entrada=request.json.get('fecha_hora_entrada', datetime.utcnow()), fecha_hora_salida=request.json.get('fecha_hora_salida'), total_pagar=request.json.get('total_pagar'), vehiculo_id=request.json['vehiculo_id'], espacio_id=request.json['espacio_id'])
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'id': ticket.id, 'fecha_hora_entrada': ticket.fecha_hora_entrada, 'fecha_hora_salida': ticket.fecha_hora_salida, 'total_pagar': ticket.total_pagar, 'vehiculo_id': ticket.vehiculo_id, 'espacio_id': ticket.espacio_id}), 201

@app.route('/tickets/<int:id>', methods=['GET'])
def obtener_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    return jsonify({'id': ticket.id, 'fecha_hora_entrada': ticket.fecha_hora_entrada, 'fecha_hora_salida': ticket.fecha_hora_salida, 'total_pagar': ticket.total_pagar, 'vehiculo_id': ticket.vehiculo_id, 'espacio_id': ticket.espacio_id})

@app.route('/tickets/<int:id>', methods=['PUT'])
def actualizar_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if not request.json:
        abort(400)
    ticket.fecha_hora_entrada = request.json.get('fecha_hora_entrada', ticket.fecha_hora_entrada)
    ticket.fecha_hora_salida = request.json.get('fecha_hora_salida', ticket.fecha_hora_salida)
    ticket.total_pagar = request.json.get('total_pagar', ticket.total_pagar)
    ticket.vehiculo_id = request.json.get('vehiculo_id', ticket.vehiculo_id)
    ticket.espacio_id = request.json.get('espacio_id', ticket.espacio_id)
    db.session.commit()
    return jsonify({'id': ticket.id, 'fecha_hora_entrada': ticket.fecha_hora_entrada, 'fecha_hora_salida': ticket.fecha_hora_salida, 'total_pagar': ticket.total_pagar, 'vehiculo_id': ticket.vehiculo_id, 'espacio_id': ticket.espacio_id})

@app.route('/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'result': True})
