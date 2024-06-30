from flask import Blueprint, render_template
from datetime import datetime
from .fuelwatch_api import *
import json
main = Blueprint('main', __name__)

# relative path to save into the templates folder so "render_template" can be used
path = 'fuelwatch_v2/templates/'
filenames = ["format1.json", "fuel_data.json"]

@main.route('/<string:filename>')
def index(filename):
    json_data = {}
    
    try:
        filename = path + filename
        with open(filename) as list_file:
            json_data = json.load(list_file)
        
        json_data["last_updated"] = str(datetime.now().strftime('%Y-%m-%d %H:%M'))

        return json.dumps(json_data)
    except:
        return "JSON file missing =("




@main.route('/fetch')
def fetch():
    days = ["today", "tomorrow"]
    fuelwatch = FuelWatch()
    for day in days:
        fuelwatch.day = day
        for fuel_type in product_map:
            fuelwatch.product = fuel_type

            if fuelwatch.query():
                fuelwatch.format1
                path_filename = path + filenames[0]
                fuelwatch.write_json(fuelwatch.json_format1, path_filename)

                fuelwatch.format2
                path_filename = path + filenames[1]
                fuelwatch.write_json(fuelwatch.json_format2, path_filename)


    return render_template(filenames[1])

@main.route('/list')
def list():
    json_object = {}
    try:
        filename = path + filenames[0]
        object = open(filename)
        json_object = json.load(object)
    except:
        print("oh noes")

    

    return render_template('list.html', json_object=json_object)























