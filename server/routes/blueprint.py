from flask import Blueprint

from server.controllers.app_controller import get_specie_info, get_specie_available_models, predict_specie_with_model, \
    get_specie_model_information

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/birds/<specie_name>', methods=['GET'])(get_specie_info)
blueprint.route('/birds/<specie_name>/models', methods=['GET'])(get_specie_available_models)
blueprint.route('/birds/<specie_name>/models/<model>', methods=['GET'])(get_specie_model_information)
blueprint.route('/birds/<specie_name>/models/<model>/predict', methods=['GET'])(predict_specie_with_model)
