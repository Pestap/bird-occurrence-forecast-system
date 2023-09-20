from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello():
    return 'HELLO'


@app.route('/api/birds/<specie_name>', methods=['GET'])
def get_specie_info(specie_name):
    """
    Handle fetching specified specie information
    """
    return specie_name


@app.route('/api/birds/<specie_name>/models', methods=['GET'])
def get_specie_available_models(specie_name):
    """
    Handle fetching available models
    """
    return specie_name +"_models"


@app.route('/api/birds/<specie_name>/models/<model>', methods=['GET'])
def get_specie_model_information(specie_name, model):
    """
    Handle fetching specified model information for specie
    """
    return specie_name + "_" + model


@app.route("/api/birds/<specie_name>/models/<model>/predict", methods=['GET'])
def predict_specie_with_model(specie_name, model):
    """
    Predict specie occurrence using specified model
    """
    return specie_name + "_" + model +"_prediction"


if __name__ == '__main__':
    app.run(debug=True)


