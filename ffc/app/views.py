from flask import Blueprint, render_template, redirect, request
import json
import requests

views = Blueprint('views', __name__)

ghg_data_api = 'https://cs361-ghg-data.herokuapp.com/'
mass_converter_api = 'https://cs361-mass-unit-converter.herokuapp.com/'


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
