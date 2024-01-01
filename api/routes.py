from flask import Flask, jsonify, request
from models import Car, db, User
from flask_sqlalchemy import SQLAlchemy

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            user = User.query.filter_by(token=token).first()
            if not user:
                raise RuntimeError('Token is invalid!')
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

# GET all cars
@app.route('/cars', methods=['GET'])
@token_required
def get_all_cars():
    return jsonify([car.to_dict() for car in Car.query.all()])

# GET single car by ID
@app.route('/cars/<int:car_id>', methods=['GET'])
@token_required
def get_car(car_id):
    car = Car.query.get(car_id)
    if car:
        return jsonify(car.to_dict())
    else:
        return jsonify({"message": "Car not found"}), 404

# POST create a new car
@app.route('/cars', methods=['POST'])
@token_required
def create_car():
    new_car = Car(
        make=request.json['make'],
        model=request.json['model'],
        year=request.json['year'],
        color=request.json['color'],
        price=request.json['price'],
        user_token = User.query.first().token
        
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify(new_car.to_dict()), 201

# PUT update an existing car
@app.route('/cars/<int:car_id>', methods=['PUT'])
@token_required
def update_car(car_id):
    car = Car.query.get(car_id)
    if car:
        car.make = request.json.get('make', car.make)
        car.model = request.json.get('model', car.model)
        car.year = request.json.get('year', car.year)
        car.color = request.json.get('color', car.color)
        car.price = request.json.get('price', car.price)
        db.session.commit()
        return jsonify(car.to_dict())
    else:
        return jsonify({"message": "Car not found"}), 404

# DELETE a car
@app.route('/cars/<int:car_id>', methods=['DELETE'])
@token_required
def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({"message": "Car deleted"})
    else:
        return jsonify({"message": "Car not found"}), 404

