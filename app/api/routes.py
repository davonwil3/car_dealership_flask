from flask import Flask, jsonify, request
from models import Car, db, User
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import Blueprint, render_template, redirect, url_for, flash, request
from functools import wraps
from flask_login import login_required
from flask import flash
from flask_login import current_user
from helpers import token_required

site = Blueprint("site", __name__, template_folder="../site/site_templates")


# FOR INSOMNIA TESTING #############################################################

# GET all cars

@site.route('/getcars', methods=['GET'])
def getcars():
    cars = Car.query.all()
    response = jsonify([car.serialize() for car in cars])
    return response

# POST add a new car

@site.route('/addnewcar', methods=['POST'])
def addnewcar():
    new_car = Car(
        make=request.json['make'],
        model=request.json['model'],
        year=request.json['year'],
        color=request.json['color'],
        price=request.json['price']
    )
    db.session.add(new_car)
    db.session.commit()

    return jsonify({ "message": "Car added successfully" }), 200

# GET car by id

@site.route('/getcarbyid', methods=['GET'])
def getcarbyid():
    car_id = request.json['car_id']
    car = Car.query.get_or_404(car_id)
    return jsonify({
        'car_id': car.car_id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'color': car.color,
        'price': car.price
    })

# PUT update an existing car

@site.route('/updatecars', methods=['PUT'])
def updatecars():
    car_id = request.json['car_id']
    car = Car.query.get(car_id)
    if car:
        car.make = request.json.get('make', car.make)
        car.model = request.json.get('model', car.model)
        car.year = request.json.get('year', car.year)
        car.color = request.json.get('color', car.color)
        car.price = request.json.get('price', car.price)
        db.session.commit()
        
        return jsonify({ "message": "Car updated successfully" }), 200
    else:
        return jsonify({"message": "Car not found"}), 404

# DELETE a car
@site.route('/deletecars', methods=['DELETE'])
def deletecars():
    car_id = request.json['car_id']
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200




######################################################################################

# GET all cars

@site.route('/getallcars', methods=['GET'])
@login_required
def getallcars():
    cars = Car.query.all()
    return render_template('getallcars.html', cars=cars)

# POST add a new car

@site.route('/addcar', methods=['GET'])
@login_required
def addcar():
    return render_template('addcar.html')

@site.route('/addcars', methods=['POST'])
@login_required
def addcars():
    new_car = Car(
        make=request.form['make'],
        model=request.form['model'],
        year=request.form['year'],
        color=request.form['color'],
        price=request.form['price']
    )
    db.session.add(new_car)
    db.session.commit()
    flash('Car has been added successfully!')
    return redirect(url_for('site.addcar'))

# GET car by id

@site.route('/getcar/<int:car_id>', methods=['GET'])
@login_required
def getcar(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify({
        'car_id': car.car_id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'color': car.color,
        'price': car.price
    })
    

# PUT update an existing car
@site.route('/update')
@login_required
def update():
    cars = Car.query.all()
    return render_template('update.html', cars=cars)

@site.route('/updatecar/<int:car_id>', methods=['PUT'])
@login_required
def updatecar(car_id):
    car = Car.query.get(car_id)
    if car:
        car.make = request.json.get('make', car.make)
        car.model = request.json.get('model', car.model)
        car.year = request.json.get('year', car.year)
        car.color = request.json.get('color', car.color)
        car.price = request.json.get('price', car.price)
        db.session.commit()
        
        return jsonify({ "message": "Car updated successfully" }), 200
    else:
        return jsonify({"message": "Car not found"}), 404

# DELETE a car
@site.route('/deletecar/<int:car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    print(car_id, 'car_id')
    car = Car.query.get_or_404(car_id)
    print(car)
    db.session.delete(car)
    db.session.commit()
    print("Car deleted")
    return redirect(url_for('site.delete_page'))

@site.route('/deletepage')
@login_required
def deletepage():
    cars = Car.query.all()
    return render_template('deletepage.html', cars=cars)

# Get User Profile
@site.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)
