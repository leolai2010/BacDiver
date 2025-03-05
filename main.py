from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return "Hello from Cloud Run!"
    elif request.method == 'POST':
        data = request.get_json()
        if data and 'genus' in data and 'specie' in data:
            genus_value = data['genus']
            specie_value = data['specie']
            return f"Values from Cloud Function: Genus = {genus_value}, Specie = {specie_value}"
        else:
            return "Invalid JSON payload", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))