from flask import Blueprint

from server.controllers.app_controller import get_specie_info, get_specie_available_models, predict_specie_with_model, \
    get_specie_model_information

blueprint = Blueprint('blueprint', __name__)

# Endpoint mapping to methods defined in server.controllers.app_controller
blueprint.route('/birds/<string:specie_name>', methods=['GET'])(get_specie_info)
blueprint.route('/birds/<string:specie_name>/models', methods=['GET'])(get_specie_available_models)
blueprint.route('/birds/<string:specie_name>/models/<string:model>', methods=['GET'])(get_specie_model_information)
blueprint.route('/birds/<string:specie_name>/models/<string:model>/predict', methods=['GET'])(predict_specie_with_model)
