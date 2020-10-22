import jwt
import os
import logging
from random import randrange
import requests
import json
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from flask_cors import CORS
from http import HTTPStatus

# Loading Config Parameters
DB_USER = os.getenv('DB_USER', 'wys')
DB_PASS = os.getenv('DB_PASSWORD', 'rac3e/07')
DB_IP = os.getenv('DB_IP_ADDRESS', '10.2.19.195')
DB_PORT = os.getenv('DB_PORT', '3307')
DB_SCHEMA = os.getenv('DB_SCHEMA', 'wys')
APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
APP_PORT = os.getenv('APP_PORT', 5007)
PROJECTS_MODULE_HOST = os.getenv('PROJECTS_MODULE_HOST', '127.0.0.1')
PROJECTS_MODULE_PORT = os.getenv('PROJECTS_MODULE_PORT', 5000)
PROJECTS_MODULE_API = os.getenv('PROJECTS_MODULE_API', '/api/projects/')
PROJECTS_URL = f"http://{PROJECTS_MODULE_HOST}:{PROJECTS_MODULE_PORT}"
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_SCHEMA}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SWAGGER_URL = '/api/times/docs/'
API_URL = '/api/times/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "WYS API - Times Service"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

try:
    f = open('oauth-public.key', 'r')
    key: str = f.read()
    f.close()
    app.config['SECRET_KEY'] = key
except Exception as terr:
    app.logger.error(f'Can\'t read public key f{terr}')
    exit(-1)

app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)
Base = declarative_base()

class TimeCategory(db.Model):
    """
    Attributes
    ---
    id: Category id
    code: Category Internal Name
    name: Category External Name
    position: Position where this category should be in a Chart Gantt
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))
    position = db.Column(db.Integer)
    subcategories = db.relationship(
        "TimeSubcategory",
        backref="time_category",
        cascade="all, delete, delete-orphan"
    )

    def to_dict(self):
        """
        Convert object to dictionary
        """
        obj_dict ={
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "position": self.position,
            "subcategories": [sub_cat.to_dict() for sub_cat in self.subcategories]
        }
        return obj_dict

    def serialize(self):
        """
            Return object serialized to json
        """
        return jsonify(self.to_dict())


class TimeSubcategory(db.Model):
    """
        Attributes
        ---
        id: SubCategory id
        code: SubCategory Internal Name
        name: SubCategory External Name
        position: Position where this subcategory should be in a Chart Gantt
        is_milestone: True if this Subcategory is a milestone
        category_id: Category id that own this subcategory
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))
    is_milestone = db.Column(db.Boolean, nullable=False, default=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('time_category.id'), nullable=False)

    def to_dict(self):
        """
        Convert object to dictionary
        """
        obj_dict = {
        'id': self.id,
        'code': self.code,
        'name': self.name,
        'is_milestone': self.is_milestone,
        'position': self.position,
        'category_id': self.category_id
        }
        return obj_dict

    def serialize(self):
        """
            Return object serialized to json
        """
        return jsonify(self.to_dict())
db.create_all()
db.session.commit()

def seed():
    try:
        categories = TimeCategory.query.all()
        if len(categories) > 0:
            return

        subcat1 = TimeSubcategory(name="Busqueda", code="BUSQUEDA", position=1)
        subcat2 = TimeSubcategory(name="Negociación de Arriendo", code="NEGOCIACION ARRIENDO", position=2)
        subcat3 = TimeSubcategory(name="Firma de Contrato", code="FIRMA CONTRATO", position=3)
        subcat4 = TimeSubcategory(name="Levantamiento de Requerimientos", code="LEVANTAMIENTO REQ", position=4)
        subcat5 = TimeSubcategory(name="Diseño Preliminar", code="DISENO PRELIMINAR", position=5)
        subcat6 = TimeSubcategory(name="Aprobación Cliente", code="APROBACION CLIENTE", position=6)
        subcat7 = TimeSubcategory(name="Anteproyecto", code="ANTEPROYECTO", position=7)
        subcat8 = TimeSubcategory(name="Aprobación Cliente", code="APROBACION CLIENTE 2", position=7)
        subcat9 = TimeSubcategory(name="Proyecto Ejecutivo", code="PROYECTO EJECUTIVO", position=8)
        subcat10 = TimeSubcategory(name="Presentación Municipal", code="PRESENTACION MUNICIPAL", position=9)
        subcat11 = TimeSubcategory(name="Presentación Admin. del Edificio", code="PRES ADM EDIFICIO", position=10)
        subcat12 = TimeSubcategory(name="Licitación de obra", code="LICITACION OBRA", position=11)
        subcat13 = TimeSubcategory(name="Negociación", code="NEGOCIACION", position=12)
        subcat14 = TimeSubcategory(name="Adjudicación y firma", code="ADJUDICACION Y FIRMA", position=13)
        subcat15 = TimeSubcategory(name="Construcción", code="CONSTRUCION", position=14)
        subcat16 = TimeSubcategory(name="Logistica de Mudanza", code="LOGISTICA", position=15)
        subcat17 = TimeSubcategory(name="Mudanza", code="MUDANZA", position=16)
        subcat18 = TimeSubcategory(name="Marcha Blanca", code="MARCHA BLANCA", position=16)

        cat1 = TimeCategory(name="ARRIENDO", code="ARRIENDO")
        cat2 = TimeCategory(name="DISEÑO", code="DISEÑO")
        cat3 = TimeCategory(name="PERMISOS", code="PERMISOS")
        cat4 = TimeCategory(name="LICITACIÓN", code="LICITACIÓN")
        cat5 = TimeCategory(name="CONSTRUCCIÓN", code="CONSTRUCCIÓN")
        cat6 = TimeCategory(name="MUDANZA", code="MUDANZA")
        cat7 = TimeCategory(name="POST OCUPACIÓN", code="OCUPACIÓN")

        db.session.add(cat1)
        db.session.add(cat2)
        db.session.add(cat3)
        db.session.add(cat4)
        db.session.add(cat5)
        db.session.add(cat6)
        db.session.add(cat7)


        # Arriendo
        cat1.subcategories.append(subcat1)
        cat1.subcategories.append(subcat2)
        subcat3.is_milestone = True
        cat1.subcategories.append(subcat3)

        # Diseño
        cat2.subcategories.append(subcat4)
        cat2.subcategories.append(subcat5)
        subcat5.is_milestone = True
        cat2.subcategories.append(subcat6)
        subcat6.is_milestone = True
        cat2.subcategories.append(subcat7)
        cat2.subcategories.append(subcat8)
        cat2.subcategories.append(subcat9)

        # Permisos
        cat3.subcategories.append(subcat10)
        cat3.subcategories.append(subcat11)

        # Licitacion
        cat4.subcategories.append(subcat12)
        cat4.subcategories.append(subcat13)
        subcat14.is_milestone = True
        cat4.subcategories.append(subcat14)

        # Construcción
        cat5.subcategories.append(subcat15)

        # Mudanza
        cat6.subcategories.append(subcat16)
        subcat17.is_milestone = True
        cat6.subcategories.append(subcat17)

        # Post Ocupacion
        cat7.subcategories.append(subcat18)

        db.session.commit()


    except SQLAlchemyError as e:
        logging.error(f"{e}")
        exit()
db.create_all()
seed()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        bearer_token = request.headers.get('Authorization', None)
        try:
            token = bearer_token.split(" ")[1]
        except Exception as ierr:
            app.logger.error(ierr)
            return jsonify({'message': 'a valid bearer token is missing'}), 500

        if not token:
            app.logger.debug("token_required")
            return jsonify({'message': 'a valid token is missing'})

        app.logger.debug("Token: " + token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['RS256'], audience="1")
            user_id: int = data['user_id']
            request.environ['user_id'] = user_id
        except Exception as err:
            return jsonify({'message': 'token is invalid', 'error': err})
        except KeyError as kerr:
            return jsonify({'message': 'Can\'t find user_id in token', 'error': kerr})

        return f(*args, **kwargs)

    return decorator


@app.route("/api/times/spec", methods=['GET'])
@token_required
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "WYS Layout API Service"
    swag['tags'] = [{
        "name": "Times",
        "description": "Methods to configure layouts"
    }]
    return jsonify(swag)


@app.route('/api/times', methods=['POST'])
@token_required
def get_times():
    """
        Get Weeks to Move
        ---
        consumes:
        - "application/json"
        tags:
        - Times
        produces:
        - application/json
        required:
            - adm_agility
            - client_agility
            - mun_agility
            - construction_mod
            - constructions_times
            - procurement_process
            - demolitions
            - m2
        parameters:
        - in: body
          name: body
          properties:
            adm_agility:
                type: string
                description:  Building Administration Agility
                enum: [low, normal, high]
            client_agility:
                type: string
                description:  Client Agility
                enum: [low, normal, high]
            mun_agility:
                type: string
                description:  Municipality Agility
                enum: [low, normal, high]
            construction_mod:
                type: string
                description:  Construction Mode
                enum: [const_adm, turnkey, general_contractor]
            constructions_times:
                type: string
                description:  Construction Mode
                enum: [daytime, nightime, free]
            procurement_process:
                type: string
                description:  Construction Mode
                enum: [direct, bidding]
            demolitions:
                type: boolean
                description: Demolitions needed
            m2:
                type: number
                format: float
        responses:
            200:
                description: Return weeks
            400:
                description: Data or missing field in body.
            404:
                description: Data object not found.
            500:
                description: Internal server error.
    """

    req_params = {'adm_agility', 'client_agility', 'mun_agility', 'construction_mod',
                  'constructions_times', 'procurement_process', 'demolitions', 'm2'}

    for param in req_params:
        if param not in request.json.keys():
            return f"{param} isn't in body", 400

    return jsonify({'weeks': randrange(3, 50, 1)})

@app.route('/api/times/detailed', methods=['POST'])
@token_required
def get_times_detailed():
    """
        Get Weeks to Move
        ---
        consumes:
        - "application/json"
        tags:
        - Times
        produces:
        - application/json
        required:
            - adm_agility
            - client_agility
            - mun_agility
            - construction_mod
            - constructions_times
            - procurement_process
            - demolitions
            - m2
        parameters:
        - in: body
          name: body
          properties:
            adm_agility:
                type: string
                description:  Building Administration Agility
                enum: [low, normal, high]
            client_agility:
                type: string
                description:  Client Agility
                enum: [low, normal, high]
            mun_agility:
                type: string
                description:  Municipality Agility
                enum: [low, normal, high]
            construction_mod:
                type: string
                description:  Construction Mode
                enum: [const_adm, turnkey, general_contractor]
            constructions_times:
                type: string
                description:  Construction Mode
                enum: [daytime, nightime, free]
            procurement_process:
                type: string
                description:  Construction Mode
                enum: [direct, bidding]
            demolitions:
                type: boolean
                description: Demolitions needed
            m2:
                type: number
                format: float
        responses:
            200:
                description: Return weeks
            400:
                description: Data or missing field in body.
            404:
                description: Data object not found.
            500:
                description: Internal server error.
    """
    req_params = {'adm_agility', 'client_agility', 'mun_agility', 'construction_mod',
                  'constructions_times', 'procurement_process', 'demolitions', 'm2'}

    for param in req_params:
        if param not in request.json.keys():
            return f"{param} isn't in body", 400

    categories= TimeCategory.query.all()
    categories_dict = [category.to_dict() for category in categories]

    for category in categories_dict:
        for sub_cat in category['subcategories']:
            if sub_cat['is_milestone']:
                sub_cat["weeks"] = 0
                continue
            sub_cat["weeks"] = randrange(3, 8, 1)

    return jsonify(categories_dict)


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
