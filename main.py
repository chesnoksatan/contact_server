from flask import Flask, request, jsonify, abort
import json
from os import path
import uuid

app = Flask(__name__)

file = path.expanduser('~') + '/contacts.json'

mode = 'r+' if path.exists(file) else 'w'
with open(file, mode) as file_object:
    if mode == 'r+':
        contacts = json.load(file_object)
    else:
        contacts = {}
        file_object.write("[]")

@app.route('/contacts', methods=['GET'])
def get_contacts():
    uuids = [ list(id.keys())[0] for id in contacts ]
    print(uuids)
    return jsonify({'contacts': contacts})

@app.route('/contact/<id>/name', methods=['GET'])
def get_contact_name(id):
    for contact in contacts:
        if id in contact:
            return jsonify({'contact': contact[id]["name"]})
    
    abort(400)

@app.route('/contact/<id>/full_info', methods=['GET'])
def get_full_info(id):
    for contact in contacts:
        if id in contact:
            return jsonify({'contact': contact[id]})
    
    abort(400)

@app.route('/create_contact', methods=['POST'])
def add_contact():
    if not request.json:
        abort(400)

    id = uuid.uuid4().__str__()
    contacts.append({id: request.json})
    save_contacts()
    return jsonify({'contact': id}), 201

@app.route('/contact/<id>/update', methods=['POST'])
def update_contact(id):
    if not request.json or 'field' not in request.json:
        abort(400)
    
    print(contacts)

    for contact in contacts:
        if id in contact:
            contact[id][request.json["field"]] = request.json["value"]
            save_contacts()
            return jsonify({'contact': contact[id]}), 201

    abort(400)

def save_contacts():
    with open(file, 'w') as file_object:
        json.dump(contacts, file_object)

if __name__ == '__main__':
    app.run(debug=True)
