#!python
# -*- coding: utf-8 -*-

import os
import inspect
import copy

import yaml
from flask import Flask, jsonify, request, abort, make_response, render_template

app = Flask(__name__)

CHILDREN = {
    u'עלמה': {'arrived': False, 'mails': [u'user@gmail.com']},
    u'אלמה': {'arrived': False, 'mails': []},
    u'עלמהה': {'arrived': False, 'mails': []},
    u'עלמה בת': {'arrived': False, 'mails': []},
    u'עלמה בן': {'arrived': False, 'mails': []},
    u'עלמה טרנס': {'arrived': False, 'mails': []},
}

config_file = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'balagan_config.yaml')
CONFIG = yaml.load(open(config_file, 'r').read())


def check_child(child):
    if not set(child.keys()) <= {'mails', 'arrived'}:
        return 'child keys must by in \{"mail", "arrived"\}: {}'.format(child.keys())

    if 'mails' not in child.keys():
        return 'child missing "mails" field'

    if type(child['mails']) is not list:
        return '"mails" type must be list: {}'.format(type(child['mails']))

    for mail in child['mails']:
        if type(mail) is not unicode:
            return '"mail" type must be unicode: {}'.format(type(mail))

    if 'arrived' not in child.keys():
        return 'child missing "arrived" field'

    if type(child['arrived']) is not bool:
        return '"arrived" type must be bool: {}'.format(type(child['arrive']))

    return True


@app.route('/balagan/api/v1.0/children', methods=['GET'])
def get_children():
    return jsonify({'children': CHILDREN})


@app.route('/balagan/api/v1.0/children/<name>', methods=['GET'])
def get_child(name):
    if name not in CHILDREN.keys():
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'child': CHILDREN[name]})


@app.route('/balagan/api/v1.0/children', methods=['POST'])
def add_child():
    print(request.json)
    if (not request.json) or ('name' not in request.json):
        abort(400)

    name = request.json['name']
    child = {'mails': request.json.get('mails', []),
             'arrived': request.json.get('arrived', False),
             }
    res = check_child(child)
    if res is not True:
        print res
        abort(400)

    CHILDREN[name] = child
    return jsonify({'child': child})


@app.route('/balagan/api/v1.0/children/<name>', methods=['PUT'])
def update_child(name):
    if name not in CHILDREN.keys():
        abort(404)
    if not request.json:
        abort(400)
    child = copy.deepcopy(CHILDREN[name])
    child.update(request.json)

    if 'name' in child.keys():
        updated_name = child.pop('name')
        if type(updated_name) is not unicode:
            abort(400)
    else:
        updated_name = name

    res = check_child(child)
    if res is not True:
        print res
        abort(400)

    CHILDREN[updated_name] = child
    if name != updated_name:
        CHILDREN.pop(name)
    return jsonify({'child': child})


@app.route('/balagan/api/v1.0/children/<name>', methods=['DELETE'])
def remove_child(name):
    if name not in CHILDREN.keys():
        abort(404)
    CHILDREN.pop(name)
    return jsonify({'result': True})


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', api_ip='http://{}:{}'.format(CONFIG['host'], CONFIG['port']))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG['port'], debug=True)
