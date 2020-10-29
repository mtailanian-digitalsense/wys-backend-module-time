import jwt
import os
import logging
from random import randrange
from constant import SubCategoryConstants, CategoryConstants
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
        obj_dict = {
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

        subcat1 = TimeSubcategory(name="Busqueda",
                                  code=SubCategoryConstants.BUSQUEDA, position=1)
        subcat2 = TimeSubcategory(name="Negociación de Arriendo",
                                  code=SubCategoryConstants.NEGOCIACION_ARRIENDO, position=2)
        subcat3 = TimeSubcategory(name="Firma de Contrato",
                                  code=SubCategoryConstants.FIRMA_CONTRATO, position=3)
        subcat4 = TimeSubcategory(name="Levantamiento de Requerimientos",
                                  code=SubCategoryConstants.LEVANTAMIENTO_REQ, position=4)
        subcat5 = TimeSubcategory(name="Diseño Preliminar",
                                  code=SubCategoryConstants.DISENO_PRELIMINAR, position=5)
        subcat6 = TimeSubcategory(name="Aprobación Cliente",
                                  code=SubCategoryConstants.APROBACION_CLIENTE, position=6)
        subcat7 = TimeSubcategory(name="Anteproyecto",
                                  code=SubCategoryConstants.ANTEPROYECTO, position=7)
        subcat8 = TimeSubcategory(name="Aprobación Cliente",
                                  code=SubCategoryConstants.APROBACION_CLIENTE_2, position=8)
        subcat9 = TimeSubcategory(name="Proyecto Ejecutivo",
                                  code=SubCategoryConstants.PROYECTO_EJECUTIVO, position=9)
        subcat10 = TimeSubcategory(name="Presentación Municipal",
                                   code=SubCategoryConstants.PRESENTACION_MUNICIPAL, position=10)
        subcat11 = TimeSubcategory(name="Presentación Admin. del Edificio",
                                   code=SubCategoryConstants.PRES_ADM_EDIFICIO, position=11)
        subcat12 = TimeSubcategory(name="Licitación de obra",
                                   code=SubCategoryConstants.LICITACION_OBRA, position=12)
        subcat13 = TimeSubcategory(name="Negociación",
                                   code=SubCategoryConstants.NEGOCIACION, position=13)
        subcat14 = TimeSubcategory(name="Adjudicación y firma",
                                   code=SubCategoryConstants.ADJUDICACION_Y_FIRMA, position=14)
        subcat15 = TimeSubcategory(name="Construcción",
                                   code=SubCategoryConstants.CONSTRUCION, position=15)
        subcat16 = TimeSubcategory(name="Logistica de Mudanza",
                                   code=SubCategoryConstants.LOGISTICA, position=16)
        subcat17 = TimeSubcategory(name="Mudanza",
                                   code=SubCategoryConstants.MUDANZA, position=17)
        subcat18 = TimeSubcategory(name="Marcha Blanca", position=18,
                                   code=SubCategoryConstants.MARCHA_BLANCA)

        cat1 = TimeCategory(name="ARRIENDO",
                            code=CategoryConstants.ARRIENDO,
                            position=1)
        cat2 = TimeCategory(name="DISEÑO",
                            code=CategoryConstants.DISENO,
                            position=2)
        cat3 = TimeCategory(name="PERMISOS",
                            code=CategoryConstants.PERMISOS,
                            position=3)
        cat4 = TimeCategory(name="LICITACIÓN",
                            code=CategoryConstants.LICITACION,
                            position=4)
        cat5 = TimeCategory(name="CONSTRUCCIÓN",
                            code=CategoryConstants.CONSTRUCCION,
                            position=5)
        cat6 = TimeCategory(name="MUDANZA",
                            code=CategoryConstants.MUDANZA,
                            position=6)
        cat7 = TimeCategory(name="POST OCUPACIÓN",
                            code=CategoryConstants.OCUPACION,
                            position=7)

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


def generate_dict(dict_values: dict, category_code: str):
    category: TimeCategory = TimeCategory.query \
        .filter(TimeCategory.code == category_code) \
        .first()

    if category is None:
        return {}

    # Build Dictionary
    category_dict = category.to_dict()
    sub_cat: dict
    for sub_cat in category_dict["subcategories"]:
        sub_cat_code = sub_cat['code']
        if sub_cat_code not in dict_values:
            logging.warning(f'{sub_cat_code} is not a valid subcategory code')
            sub_cat['weeks'] = 0
        else:
            sub_cat['weeks'] = dict_values[sub_cat_code]
    return category_dict


def calc_arriendo():
    """
    Calc Arriendo Weeks
    return: Category dict corresponding to "Arriendo"
    """

    # Build dict with weeks by subcategories
    dict_values = {SubCategoryConstants.BUSQUEDA: 2,
                   SubCategoryConstants.NEGOCIACION_ARRIENDO: 1,
                   SubCategoryConstants.FIRMA_CONTRATO: 0
                   }

    return generate_dict(dict_values, CategoryConstants.ARRIENDO)


def calc_proyecto_ejecutivo(m2):
    if m2 <= 300:
        return 4
    elif 300 < m2 <= 600:
        return 4
    elif 600 < m2 <= 800:
        return 5
    elif 800 < m2 <= 1200:
        return 5
    elif 1200 < m2 <= 1500:
        return 6
    elif 1500 < m2 <= 2000:
        return 6
    elif 2000 < m2 <= 2500:
        return 7
    elif 2500 < m2 <= 3500:
        return 7
    else:
        return 8


def calc_diseno(client_aprov: int, m2: float):
    """
    Calc diseno category
    return: dict with durations.
    """
    # Build dict with subcategories durations in weeks
    dict_values = {
        SubCategoryConstants.LEVANTAMIENTO_REQ: 1,
        SubCategoryConstants.DISENO_PRELIMINAR: 4 + client_aprov,
        SubCategoryConstants.APROBACION_CLIENTE: 0,
        SubCategoryConstants.ANTEPROYECTO: 4 + client_aprov,
        SubCategoryConstants.APROBACION_CLIENTE_2: 0,
        SubCategoryConstants.PROYECTO_EJECUTIVO: calc_proyecto_ejecutivo(m2)
    }

    return generate_dict(dict_values, CategoryConstants.DISENO)


def calc_weeks_per_m2_construccion(m2: int):
    if m2 <= 300:
        return 8
    elif 300 < m2 <= 600:
        return 9
    elif 600 < m2 <= 800:
        return 11
    elif 800 < m2 <= 1200:
        return 13
    elif 1200 < m2 <= 1500:
        return 15
    elif 1500 < m2 <= 2000:
        return 17
    elif 2000 < m2 <= 2500:
        return 21
    elif 2500 < m2 <= 3500:
        return 24
    else:
        return 26


def calc_permisos(municipality_agility: int, building_agility: int):
    """
    Calc permisos category
    return: dict with durations
    """
    dict_values = {
        SubCategoryConstants.PRESENTACION_MUNICIPAL: municipality_agility,
        SubCategoryConstants.PRES_ADM_EDIFICIO: building_agility
    }
    return generate_dict(dict_values, CategoryConstants.PERMISOS)


def calc_licitacion(isDirect: bool):
    """
    Calc licitacion category
    return: dict with durations
    """
    dict_values = {
        SubCategoryConstants.LICITACION_OBRA: 0 if isDirect else 4,
        SubCategoryConstants.NEGOCIACION: 0 if isDirect else 2,
        SubCategoryConstants.ADJUDICACION_Y_FIRMA: 0
    }
    return generate_dict(dict_values, CategoryConstants.LICITACION)


def calc_construccion(m2: int, shift: str, demolition_required: bool, construction_mod: str):
    # Mapping Weeks
    shift_map = {
        'daytime': 1,
        'nightime': 1.3,
        'free': 1
    }

    construction_mod_map = {
        'const_adm': 1.2,
        'turnkey': 1,
        'general_contractor': 1.2
    }
    weeks = {}

    # Weeks per m2

    weeks['m2'] = calc_weeks_per_m2_construccion(m2)

    # Shift Mode
    if shift not in shift_map:
        logging.warning(f'{shift} isn\'t a valid shift mode')
        weeks['shift'] = 1
    else:
        weeks['shift'] = shift_map[shift]

    # Demolition required
    weeks['demolition'] = 3 if demolition_required else 0

    # Construction Mode
    if construction_mod not in construction_mod_map:
        logging.warning(f'{construction_mod} isn\'t a valid procurement ')
        weeks['const_mod'] = 1
    else:
        weeks['const_mod'] = construction_mod_map[construction_mod]

    total_weeks = (weeks['m2'] * weeks['shift'] * weeks['const_mod']) + weeks['demolition']

    dict_values = {
        SubCategoryConstants.CONSTRUCION: total_weeks
    }

    return generate_dict(dict_values, CategoryConstants.CONSTRUCCION)


def calc_mudanza():
    dict_values = {
        SubCategoryConstants.MUDANZA: 0,
        SubCategoryConstants.LOGISTICA: 2
    }
    return generate_dict(dict_values, CategoryConstants.MUDANZA)


def calc_marcha_blanca(m2: int):
    weeks = 0
    if m2 <= 1000:
        weeks = 2
    elif 1000 < m2 <= 3500:
        weeks = 3
    else:
        weeks = 4

    dict_values = {
        SubCategoryConstants.MARCHA_BLANCA: weeks
    }

    return generate_dict(dict_values, CategoryConstants.OCUPACION)


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

    # Create weeks sum

    # Calc Rent Category

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

    categories = TimeCategory.query.all()
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
