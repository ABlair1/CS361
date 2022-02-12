from flask import Blueprint, render_template, request
import json

views = Blueprint('views', __name__)

# Route handler for home page view
@views.route('/')
def home():
    return render_template('home.html')

# Route handler for food list page view
@views.route('/food_list')
def food_list():
    # TEMPORARY: Remove the following when implementing the request to the API
    with open('../ghg_data_server/ghg_data.json', 'r') as data_file:
        data = json.load(data_file)
    # END TEMPORARY

    # KEEP: Reuse somehow in implementation below???
    food_item_dictionary = {}
    for item in data.keys():
        food_item_dictionary[item] = data[item]['Category']
    # END KEEP

    #######################################
    # Logic for:
    #   Send request to API for all ghg data
    #       (send: GET request for ghg_data)
    #       (response from API should return: ghg_data in JSON format)
    #   Render food list from items listed in ghg_data
    #       (each should be rendered as a link that routes to '/footprint_calc/<item_name>')
    #######################################
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
    input_data = {}
    input_data['item_name'] = request.args.get('item_name')
    input_data['mass'] = request.args.get('mass')
    input_data['units'] = request.args.get('units')

    # 
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
    return render_template('results.html', input_data=input_data)

# Route handler for about page view
@views.route('/about')
def about():
    return render_template('about.html')
