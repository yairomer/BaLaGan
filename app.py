#!python
# -*- coding: utf-8 -*-

import os
import inspect
import copy

import yaml
from flask import Flask, jsonify, request, abort, make_response, render_template

app = Flask(__name__)


DEFAULT_IMAGE_URL = u'https://s-media-cache-ak0.pinimg.com/originals/b3/ac/66/b3ac66a299b5496846ffa50eac790d49.png'

CONFIG_FILE = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'balagan_config.yaml')
CONFIG_DEFAULT_FILE = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'defaults/balagan_config.yaml')
if os.path.isfile(CONFIG_FILE):
    CONFIG = yaml.load(open(CONFIG_FILE, 'r').read())
else:
    CONFIG = yaml.load(open(CONFIG_DEFAULT_FILE, 'r').read())

CHILDREN_FILE = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'children.yaml')
CHILDREN_DEFAULT_FILE = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), 'defaults/children.yaml')
if os.path.isfile(CHILDREN_FILE):
    CHILDREN = yaml.load(open(CHILDREN_FILE, 'r').read()) or {}
else:
    CHILDREN = yaml.load(open(CHILDREN_DEFAULT_FILE, 'r').read()) or {}


def check_child(child):
    if not set(child.keys()) <= {'mails', 'image_url', 'arrived'}:
        return 'child keys must by in \{"mail", "arrived"\}: {}'.format(child.keys())

    if 'mails' not in child.keys():
        return 'child missing "mails" field'

    if type(child['mails']) is not list:
        return '"mails" type must be list: {}'.format(type(child['mails']))

    for mail in child['mails']:
        if type(mail) is not unicode:
            return '"mail" type must be unicode: {}'.format(type(mail))

    if 'image_url' not in child.keys():
        return 'child missing "image_url" field'

    if type(child['image_url']) is not unicode:
        return '"image_url" type must be unicode: {}'.format(type(child['image_url']))

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
    if (not request.json) or ('name' not in request.json):
        abort(400)

    name = request.json['name']
    child = {'mails': request.json.get('mails', []),
             'image_url': request.json.get('arrived', DEFAULT_IMAGE_URL),
             'arrived': request.json.get('arrived', False),
             }
    res = check_child(child)
    if res is not True:
        print res
        abort(400)

    CHILDREN[name] = child
    open(CHILDREN_FILE, 'w').write(yaml.dump(CHILDREN))
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
    open(CHILDREN_FILE, 'w').write(yaml.dump(CHILDREN))
    return jsonify({'child': child})


@app.route('/balagan/api/v1.0/children/<name>', methods=['DELETE'])
def remove_child(name):
    if name not in CHILDREN.keys():
        abort(404)
    CHILDREN.pop(name)
    open(CHILDREN_FILE, 'w').write(yaml.dump(CHILDREN))
    return jsonify({'result': True})


@app.route('/balagan/api/v1.0/children/actions', methods=['POST'])
def actions():
    if (not request.json) or ('type' not in request.json):
        abort(400)

    global CHILDREN

    if request.json['type'] == 'reset_arrived':
        for child in CHILDREN.itervalues():
            child['arrived'] = False

    elif request.json['type'] == 'reset':
        CHILDREN = yaml.load(open(CHILDREN_DEFAULT_FILE, 'r').read()) or {}
        open(CHILDREN_FILE, 'w').write(yaml.dump(CHILDREN))

    else:
        abort(400)

    return jsonify({})


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/manage/')
@app.route('/manage/index')
def manage():
    return render_template('manage.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG['port'], debug=True)
