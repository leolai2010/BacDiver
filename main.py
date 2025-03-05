from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return "Hello from Cloud Run!"
    elif request.method == 'POST':
        data = request.get_json()
        if data and 'column4' in data and 'column5' in data:
            column4_value = data['column4']
            column5_value = data['column5']
            return f"Values from Cloud Function: Column 4 = {column4_value}, Column 5 = {column5_value}"
        else:
            return "Invalid JSON payload", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))