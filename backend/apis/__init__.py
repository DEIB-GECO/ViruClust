from flask import Blueprint
from flask_restplus import Api

from .ufl import api as ufl
from .private import api as private
from .analyze_file import api as analyze_file
from .analyze_file_example import api as analyze_file_example

enable_doc = True

api_blueprint = Blueprint('api', __name__)

if enable_doc:
    api = Api(title='UFL API', version='1.0', description='TODO', )
else:
    api = Api(title='UFL API', version='1.0', description='TODO', doc=False)


api.init_app(api_blueprint, add_specs=enable_doc)

api.add_namespace(ufl)
api.add_namespace(private)
api.add_namespace(analyze_file)
api.add_namespace(analyze_file_example)
