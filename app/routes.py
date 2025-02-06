from flask import Blueprint, jsonify, request
from app.controllers import  add_user,get_all_nom

api = Blueprint('PaySphereAPI', __name__)

@api.route('/')
def home():
    return "Hello, API Flask fonctionne !"

@api.route('/test',methods=['GET'])
def test():
    test = get_all_nom()
    return jsonify([{"nom": u.nom, "prenom": u.prenom} for u in test])

@api.route('/users', methods=['GET'])
def users():
    pass
    #users = get_all_users()
    #return jsonify([{"id": u.id, "name": u.name} for u in users])

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    user = add_user(data['name'])
    return jsonify({"id": user.id, "name": user.name}), 201
