from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/food_list')
def food_list():
    return '<h1>Food List Placeholder</h1>'

@views.route('/footprint_calc')
def footprint_calc():
    return '<h1>Footprint Calculator Placeholder</h1>'

@views.route('/results')
def results():
    return '<h1>Results Placeholder</h1>'

@views.route('/about')
def about():
    return '<h1>About Placeholder</h1>'