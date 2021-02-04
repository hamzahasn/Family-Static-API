"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_members():

    # this is how you can use the Family datastructure by calling its methods
    status = 200
    try:
        members = jackson_family.get_all_members()
        response_body = members
    except: 
        response_body = {
            "status": "There was a probelm on the server. Could not fulfill request"
        }
        status = 500 


    return jsonify(response_body), status 
@app.route('/member/<int:member_id>', methods=['GET'])
def handle_get_specific_members(member_id):
    # this is how you can use the Family datastructure by calling its methods
    status = 200
    try:
        member = jackson_family.get_member(member_id)
        if member == False:
            response_body = {
                "status": "Could not find member"
            }
            status = 404
        else: 
             response_body = member
    except:
        response_body = {
      
            "status": "There was a probelm on the server. Could not fulfill request"
        }
        status = 500 


    return jsonify(response_body), status 

    

@app.route('/member', methods=['POST'])
def handle_add_specific_members():

    # this is how you can use the Family datastructure by calling its methods
    status = 200
    body = request.json
    if body is None:
        response_body = {
            "status": "Body of response is empty."
        }
        status = 400
    else:

        try:
            member = jackson_family.add_member(body)
            response_body = member
        except:
            response_body = {
                "status": "There was a problem on the server. Could not fulfill request."
            }
            status = 500

    return jsonify(response_body), status

@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    status = 200 
    if jackson_family.delete_member(member_id): 
        members = jackson_family.get_all_members()
        response_body = {
            "done": True, "members": members
        }   
        return jsonify(response_body), 200
    else:
        return "bad request", 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
