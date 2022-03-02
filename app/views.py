from flask import Blueprint, render_template, redirect, request
import json
import requests

views = Blueprint('views', __name__)

ghg_data_api = 'https://cs361-ghg-data.herokuapp.com/'
mass_converter_api = 'https://cs361-mass-unit-converter.herokuapp.com/'
routes = {
    'home' : '/',
    'foods' : '/food_list',
    'calculator' : '/footprint_calc/<item_name>',
    'results' : '/results',
    'grocery' : '/grocery',
    'map' : '/grocery_search',
    'about' : '/about',
}

def calcFoodAlternatives(data, emissions_kg, units):
    """Uses emissions result to calculate alternative food amounts"""
    alternatives = {}
    for item in data.keys():
        item_kgs = emissions_kg / float(data[item]['Total'])

        req_params = str(item_kgs) +'/kg/' + units + '/'
        mc_response = requests.get(mass_converter_api + req_params)
        item_emissions = float(json.loads(mc_response.text)['result_mass'])

        alternatives[item] = {}
        alternatives[item]['Amount'] = round(item_emissions, 2)
        alternatives[item]['Category'] = data[item]['Category']
    return alternatives

def calcEmissions(data, item_name, mass_kgs):
    """Calculates emissions for food item"""
    return float(data[item_name]['Total']) * mass_kgs

def inputUnitsToKgs(mass, units):
    """Converts input mass to kgs"""
    req_params = mass +'/' + units + '/kg/'
    mc_response = requests.get(mass_converter_api + req_params)
    return float(json.loads(mc_response.text)['result_mass'])

def kgsToInputUnits(emissions_kg, units):
    """Converts emissions in kg to input units and rounds result"""
    req_params = str(emissions_kg) +'/kg/' + units + '/'
    mc_response = requests.get(mass_converter_api + req_params)
    emissions = float(json.loads(mc_response.text)['result_mass'])
    return round(emissions, 2)

#######################################################################
# Route Handlers
#######################################################################

@views.route(routes['home'])
def home():
    return render_template('home.html')


@views.route(routes['foods'])
def food_list():
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


@views.route(routes['calculator'])
def footprint_calc(item_name):
    return render_template('footprint_calc.html', item_name=item_name)


@views.route(routes['results'], methods=['GET'])
def results():
    item_name = request.args.get('item_name')
    mass = request.args.get('mass')
    units = request.args.get('units')

    response = requests.get(ghg_data_api)
    data = json.loads(response.text)

    mass_kgs = inputUnitsToKgs(mass, units)
    emissions_kg = calcEmissions(data, item_name, mass_kgs)
    emissions = kgsToInputUnits(emissions_kg, units)
    alternatives = calcFoodAlternatives(data, emissions_kg, units)

    return render_template(
        'results.html', 
        item_name=item_name, 
        mass=mass, 
        units=units, 
        emissions=emissions, 
        alternatives=alternatives
    )


@views.route(routes['grocery'])
def grocery():
    return render_template('grocery.html')


@views.route(routes['map'])
def grocery_search():
    city = request.args.get('city')
    state = request.args.get('state')

    api_url = 'https://maps-api-microservice.herokuapp.com/grocery?'
    map_url = api_url + 'city=' + city + '&state=' + state
    return redirect(map_url)


@views.route(routes['about'])
def about():
    return render_template('about.html')
