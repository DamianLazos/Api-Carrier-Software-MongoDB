# ******************************PYTHON LIBRARIES******************************
from bson.objectid import ObjectId
# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
import pandas
# ******************************OWN LIBRARIES*********************************
from extensions import mongo
# ***********************************CODE*************************************

blp = Blueprint("leads", __name__, description="All leads functionalities")

@blp.route("/leads")
class LeadsView(MethodView):
    def post(self):
        '''This endpoint takes an .xlsx file
        and turns the data into dictionaries
        in orden to save the information into
        mongo's collection.'''
        file = request.files['file']
        data_excel = pandas.read_excel(file, "Company Information", header=0)
        data = data_excel.to_dict("records")
        mongo.db.leads.insert_many(data)

        return "Success!"

    def delete(self):
        '''This endpoint delete all the data
        stored into a mongo's collection.
        NOTE
        Be careful with the use of this
        endpoint due to the information
        won't be recovered.'''
        mongo.db.leads.delete_many({})
        return "Info deleted"

@blp.route("/lead/<string:lead_id>")
class LeadsIDView(MethodView):
    def put(self, lead_id):
        '''This endpoint updates a
        selected lead from a mongo's
        collection according to its _id'''
        new_info = request.json
        mongo.db.leads.update_one({"_id": ObjectId(lead_id)}, {"$set": new_info})

        return "Success"

    def delete(self, lead_id):
        '''This endpoint deletes a
        selected lead from a mongo's
        collection according to its _id'''
        mongo.db.leads.delete_one({"_id": ObjectId(lead_id)})
        return "Success"


