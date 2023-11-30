from flask import Blueprint

from controllers.app_controller import get_species_info, get_species_available_models, predict_species_with_model, \
    get_species_model_information, get_species, get_observations

blueprint = Blueprint('blueprint', __name__)

# Endpoint mapping to methods defined in server.controllers.app_controller
blueprint.route('/birds', methods=['GET'])(get_species)
blueprint.route('/birds/<string:species_name>', methods=['GET'])(get_species_info)
blueprint.route('/birds/<string:species_name>/models', methods=['GET'])(get_species_available_models)
blueprint.route('/birds/<string:species_name>/models/<string:model>', methods=['GET'])(get_species_model_information)
blueprint.route('/birds/<string:species_name>/observations', methods=['GET'])(get_observations)
blueprint.route('/birds/<string:species_name>/models/<string:model>/predict', methods=['GET'])(predict_species_with_model)
