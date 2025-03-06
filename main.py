from flask import Flask, request
import os
import bacdive
import json

app = Flask(__name__)

def bacdiveid_finder(bacid):
    client = bacdive.BacdiveClient('leolai2010@gmail.com','Kill!77358524')
    client.search(taxonomy=bacid)
    for strain in client.retrieve(['type strain']):
        bacdiveid = next(iter(strain))
        type_strain = strain[bacdiveid][0].get('type strain', None)
        if type_strain == 'yes':
            return bacdiveid
        
@app.route("/", methods=['POST'])
def diver():
    if request.method == 'POST':
        data = request.get_json()
        if data and 'genus' in data and 'specie' in data:
            genus = data['genus']
            specie = data['specie']
            organism = genus + ' ' + specie
            bacdiveid = bacdiveid_finder(organism)
            return f"Values from Cloud Function: {bacdiveid}"
        else:
            return "Invalid JSON payload", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))