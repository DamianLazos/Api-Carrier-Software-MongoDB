# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask
from flask_pymongo import PyMongo
# ******************************OWN LIBRARIES*********************************
from extensions import mongo
from src.routes.leads import blp as LeadsBlueprint
# ***********************************CODE*************************************

def create_app():
    # Flask instance
    app = Flask(__name__)
    # app cofiguration
    app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/carrier_software_app"
    # PyMongo instance
    mongo.init_app(app)
    db = mongo.db
    try:
        db.create_collection("leads")
    except:
        pass
    # Registered Blueprints
    app.register_blueprint(LeadsBlueprint)
    return app

