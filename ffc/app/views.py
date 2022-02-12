from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/food_list')
def food_list():
    return render_template('food_list.html')

@views.route('/footprint_calc/<item_name>')
def footprint_calc(item_name):
    return render_template('footprint_calc.html', item_name=item_name)

@views.route('/results/<item_name>/<units>/<mass>')
def results(item_name, units, mass):
    #######################################
    # Logic for:
    #   Send request to API for all ghg data
    #       (send: GET request for ghg_data)
    #       (response from API should return: ghg_data in JSON format)
    #   Send request to mass_converter API
    #       (send for all items in ghg_data: units, mass, result_units)
    #           (maybe use JSON where {"Identifier" : [units, mass, result_units]})
    #       (response from API should return: units, mass, result_units, result_mass)
    #           (maybe use JSON where {"Identifier" : [units, mass, result_units, result_mass]})
    #   Render template with results
    #######################################
    return render_template('results.html')

@views.route('/about')
def about():
    return render_template('about.html')
