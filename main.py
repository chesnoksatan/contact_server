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
        contacts = []
        file_object.write("[]")


@app.route('/contacts', methods=['GET'])
def get_contacts():
    uuids = [ contact["id"] for contact in contacts ]
    return jsonify({'contacts': uuids})


@app.route('/contact/<id>/name', methods=['GET'])
def get_contact_name(id):
    contacts_filtrated = list(filter(lambda contact: contact["id"] == id, contacts))
    
    if len(contacts_filtrated) == 0: abort(400)
    else: return jsonify({'contact': contacts_filtrated[0]["name"]})


@app.route('/contact/<id>/full_info', methods=['GET'])
def get_full_info(id):
    contacts_filtrated = list(filter(lambda contact: contact["id"] == id, contacts))

    if len(contacts_filtrated) == 0: abort(400)
    else: return jsonify({'contact': contacts_filtrated[0]})


@app.route('/create_contact', methods=['POST'])
def add_contact():
    if not request.json:
        abort(400)

    id = uuid.uuid4().__str__()
    contact = request.json
    contact["id"] = id
    contacts.append(contact)

    save_contacts()
    return jsonify({'contact': id}), 201


@app.route('/contact/<id>/update', methods=['POST'])
def update_contact(id):
    if not request.json:
        abort(400)

    contacts_filtrated = list(filter(lambda contact: contact["id"] == id, contacts))

    if len(contacts_filtrated) == 0: abort(400)
    else:
        contacts.remove(contacts_filtrated[0])
        contact = request.json
        contact["id"] = id
        contacts.append(contact)

        save_contacts()
        return jsonify({'contact': contact})


def save_contacts():
    with open(file, 'w') as file_object:
        json.dump(contacts, file_object)

if __name__ == '__main__':
    app.run(debug=True)
