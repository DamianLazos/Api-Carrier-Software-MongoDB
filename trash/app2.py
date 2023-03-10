# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask, request
import pandas
from pymongo import MongoClient
# ******************************OWN LIBRARIES*********************************

# ***********************************CODE*************************************
app = Flask(__name__)

@app.route('/upload_csv', methods=["POST"])
def upload_csv():
    file = request.files['file']
    client = MongoClient('mongodb://localhost:27017/')
    db = client['carrier_software']
    collection = db['leads']
    file_csv = pandas.read_csv(file)
    data = file_csv.to_dict('records')
    collection.insert_many(data)
    return "Success!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)