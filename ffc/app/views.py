from flask import Blueprint, render_template, redirect, request
import json
import requests

views = Blueprint('views', __name__)

ghg_data_api = 'http://127.0.0.1:6000/'
mass_converter_api = 'http://127.0.0.1:7000/'

# Extract following functions to unit converter API
def convert_to_kgs(mass, units):
    """Function has two parmeters: a number that is a mass quantity 
    and a string that is a unit of measurement for mass. Returns 
    the equivaent mass as measured in kilograms."""
    to_kgs = {
        'lb' : 0.453592,
        'oz' : 0.0283495,
        'mg' : 0.000001,
        'g' : 0.001,
        'kg' : 1,
        'ton (metric)' : 1000,
        'ton (us)' : 907.185,
        'ton (imperial)' : 1016.05,
        'st' : 6.35029,
    }
    return mass * to_kgs[units]

def convert_from_kgs(mass, units):
    """Function has two parmeters: a number that is a mass quantity 
    mesured in kilograms and a string that is a unit of measurement 
    for mass. Returns the equivaent mass as measured in the 
    specified units."""
    from_kgs = {
        'lb' : 2.20462,
        'oz' : 35.274,
        'mg' : 1000000,
        'g' : 1000,
        'kg' : 1,
        'ton (metric)' : 0.001,
        'ton (us)' : 0.00110231,
        'ton (imperial)' : 0.000984207,
        'st' : 0.157473,
    }
    return mass * from_kgs[units]




# Route handler for home page view
@views.route('/')
def home():
    return render_template('home.html')


# Route handler for food list page view
@views.route('/food_list')
def food_list():
    # Request ghg data from API
    response = requests.get(ghg_data_api)
    data = json.loads(response.text)

    # Extract food item names and categories from ghg data
    food_item_dictionary = {}
    for item in data.keys():
        food_item_dictionary[item] = data[item]['Category']

    return render_template(
        'food_list.html', 
        food_item_dictionary=food_item_dictionary,
        )


# Route handler for footprint calculator page view
@views.route('/footprint_calc/<item_name>')
def footprint_calc(item_name):
    return render_template('footprint_calc.html', item_name=item_name)


# Route handler for results page view
@views.route('/results', methods=['GET'])
def results():
    # Get input data from footprint calculator submit (GET request)
    item_name = request.args.get('item_name')
    mass = request.args.get('mass')
    units = request.args.get('units')

    # Request ghg data from API
    response = requests.get(ghg_data_api)
    data = json.loads(response.text)

    # Convert input mass to kgs
    # Request mass unit conversion from API
    req_params = mass +'/' + units + '/kg/'
    mc_response = requests.get(mass_converter_api + req_params)
    mass_kgs = float(json.loads(mc_response.text)['result_mass'])

    # Calculate emissions for food item
    emissions_kg = float(data[item_name]['Total']) * mass_kgs

    # Convert emissions in kg to input units
    req_params = str(emissions_kg) +'/kg/' + units + '/'
    mc_response = requests.get(mass_converter_api + req_params)
    emissions = float(json.loads(mc_response.text)['result_mass'])

    emissions = round(emissions, 2)
    
    # Use emissions result to calculate alternative food amounts
    alternatives = {}
    for item in data.keys():
        item_kgs = emissions_kg / float(data[item]['Total'])

        req_params = str(item_kgs) +'/kg/' + units + '/'
        mc_response = requests.get(mass_converter_api + req_params)
        item_emissions = float(json.loads(mc_response.text)['result_mass'])

        alternatives[item] = {}
        alternatives[item]['Amount'] = round(item_emissions, 2)
        alternatives[item]['Category'] = data[item]['Category']


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
    return render_template(
        'results.html', 
        item_name=item_name, 
        mass=mass, 
        units=units, 
        emissions=emissions, 
        alternatives=alternatives
    )


# Route handler for grocery page view
@views.route('/grocery')
def grocery():
    return render_template('grocery.html')


# Route handler for grocery page view
@views.route('/grocery_search')
def grocery_search():
    # Get input data from grocery form submit
    city = request.args.get('city')
    state = request.args.get('state')

    # Redirect to search results using map API
    api_url = 'https://maps-api-microservice.herokuapp.com/grocery?'
    map_url = api_url + 'city=' + city + '&state=' + state
    return redirect(map_url)


# Route handler for about page view
@views.route('/about')
def about():
    return render_template('about.html')
