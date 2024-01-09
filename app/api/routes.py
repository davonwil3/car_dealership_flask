from flask import Flask, jsonify, request
from models import Car, db, User
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import Blueprint, render_template, redirect, url_for, flash, request
from functools import wraps
from flask_login import login_required
from flask import flash



site = Blueprint("site", __name__, template_folder="../site/site_templates")




# GET all cars

@site.route('/getallcars', methods=['GET'])
@login_required
def getallcars():
    cars = Car.query.all()
    return render_template('getallcars.html', cars=cars)

# GET single car by ID
"""
@app.route('/profile/search', methods=['GET'])
@token_required
def search(car_id):
    car = Car.query.get(car_id)
    if car:
        return jsonify(car.to_dict())
    else:
        return jsonify({"message": "Car not found"}), 404

# POST create a new car
"""
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
    flash('Car has been added successfully!', 'success')
    return redirect(url_for('site.addcar'))

# PUT update an existing car

@site.route('/updatecar', methods=['PUT'])
@login_required
def update_car(car_id):
    car = Car.query.get(car_id)
    if car:
        car.make = request.json.get('make', car.make)
        car.model = request.json.get('model', car.model)
        car.year = request.json.get('year', car.year)
        car.color = request.json.get('color', car.color)
        car.price = request.json.get('price', car.price)
        db.session.commit()
        return 
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



