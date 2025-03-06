from flask import Flask, request, jsonify
import os
import bacdive
import json
from collections import Counter

app = Flask(__name__)
client = bacdive.BacdiveClient('leolai2010@gmail.com','Kill!77358524')

interpert_dict = {
    'OX':'oxidase',
    'PYRA':'PYR',
    'GLU':'glucose',
    'H2S':'h2s',
    'MOB':'motility',
    'IND':'indole',
    'ODC':'ornithine',
    'CIT':'citrate',
    'URE':'urease',
    'NO2':'nitrate',
    'VP':'voges_proskauer',
    'LDC Lys':'lysine_decarboxylase',
    'ONPG':'beta_galactosidase',
    'MEL':'melibiose',
    'TDA Trp':'trytophan_deaminase'
}

def merge_objects(objects):
    merged = {}
    keys = {key for obj in objects for key in obj}  
    for key in keys:
        values = [obj[key] for obj in objects if key in obj]  
        most_common_value = Counter(values).most_common(1)[0][0]
        merged[key] = most_common_value
    return merged

def bacdiveid_finder(bacid):
    client.search(taxonomy=bacid)
    for strain in client.retrieve(['type strain']):
        bacdiveid = next(iter(strain))
        type_strain = strain[bacdiveid][0].get('type strain', None)
        if type_strain == 'yes':
            return bacdiveid
        
def bacdiveid_result(bacdiveid):
    data = {}
    client.search(id = bacdiveid)
    for strain in client.retrieve(['methylred-test', 'API 20E']):
        if strain[bacdiveid][0].get('methylred-test', None) == '+':
            data['methylred_result'] = 1
        else:
            data['methylred_result'] = 0
        combine_api_20e_result = merge_objects(strain[bacdiveid][1].get('API 20E', None))
        break
    for interpert in interpert_dict:
        if interpert in combine_api_20e_result:
            data[interpert_dict[interpert]] = 1 if combine_api_20e_result[interpert] == "+" else 0
    print(data)

@app.route("/", methods=['POST'])
def diver():
    if request.method == 'POST':
        data = request.get_json()
        if data and 'genus' in data and 'specie' in data:
            genus = data['genus']
            specie = data['specie']
            organism = genus + ' ' + specie
            bacdiveid = bacdiveid_finder(organism)
            response_data = bacdiveid_result(bacdiveid)
            return jsonify(response_data), 200
        else:
            return "Invalid JSON payload", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))