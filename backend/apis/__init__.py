from flask import Blueprint
from flask_restplus import Api

from .epitope import api as epitope_api

enable_doc = True

api_blueprint = Blueprint('api', __name__)

if enable_doc:
    api = Api(title='ViruSurf API', version='1.0', description='TODO', )
else:
    api = Api(title='ViruSurf API', version='1.0', description='TODO', doc=False)


api.init_app(api_blueprint, add_specs=enable_doc)

api.add_namespace(epitope_api)
