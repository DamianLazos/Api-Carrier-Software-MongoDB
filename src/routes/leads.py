# ******************************PYTHON LIBRARIES******************************
from bson.objectid import ObjectId
# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
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

        # Here we receive the client's posted file.
        file = request.files['file']
        # Here we test if the file received is a valid .xlsx, if not a 415 http error and a message is returned.
        try:
            data_excel = pandas.read_excel(file, "Company Information", header=0)
        except:
            return {"message": "The file sent is not a .xlsx type"}, 415
        # Here we turn every .xlsx file information row into a dictionary.
        data = data_excel.to_dict("records")
        # Here we store the result dictionaries into a MongoDB database and collection.
        mongo.db.leads.insert_many(data)
        # Here we return a success confirmation message.
        return {"message": "Data processed and stored successfully."}

    def delete(self):
        '''This endpoint delete all the data
        stored into a mongo's collection.
        NOTE
        Be careful with the use of this
        endpoint due to the information
        won't be recovered.'''

        # Here we delete every document contained into a MongoDB lead's collection.
        mongo.db.leads.delete_many({})
        # Here we return a success confirmation message.
        return {"message": "All the collection's documents has been deleted successfully."}

@blp.route("/lead/<string:lead_id>")
class LeadsIDView(MethodView):
    def put(self, lead_id):
        '''This endpoint updates a
        selected lead from a mongo's
        collection according to its _id'''

        # Here we take the client's putted json object with the new information to update.
        new_info = request.json
        # Here we try to fetch a lead document(bson) into a MongoDB lead's collection by the specified _id to update it, if not we return a 404 http error with a message.
        try:
            mongo.db.leads.update_one({"_id": ObjectId(lead_id)}, {"$set": new_info})
        except:
            return {"message": "The _id specified could not been found."}, 404
        # Here we return a success confirmation message.
        return {"message": "The lead specified has been updated successfully."}

    def delete(self, lead_id):
        '''This endpoint deletes a
        selected lead from a mongo's
        collection according to its _id'''

        # Here we try to fetch a MongoDB's collection lead to delete it, if not we return a 404 http error with a message.
        try:
            mongo.db.leads.delete_one({"_id": ObjectId(lead_id)})
        except:
            return {"message": "The _id specified could not been found."}, 404
        # Here we return a success confirmation message.
        return "Success"


