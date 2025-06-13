import base64
from datetime import datetime
import logging
import os
from flask import Flask, request, jsonify
import pandas as pd
import io
from src.exceptions import *
from src.functions.clear_uploads import clear_uploads_folder

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# À supprimer en Prod
clear_uploads_folder()

@app.errorhandler(Exception)
def handle_exception(error):
    logging.critical(error, exc_info=True)

    if isinstance(error, APIException):
        response = jsonify(message=error.message, description=error.description)
        return response, error.code

    return jsonify(message="server-error", description='Internal server error'), 500

@app.route('/version', methods=['GET'])
def version():
    return jsonify({'version': 'Dat\'API-1.0.0'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if not request.is_json:
        raise BadRequestJSONException()
    
    content  = request.get_json(force=True, silent=True)

    if not content:
        raise EmptyRequestException()

    file_name = content['file_name']
    if not file_name or not isinstance(file_name, str):
        raise EmptyDataProvidedException("file_name")

    delimiter = content['delimiter']
    if not delimiter or not isinstance(delimiter, str):
        raise EmptyDataProvidedException("delimiter")

    file = content['file_data']
    if not file or not isinstance(file, str):
        raise EmptyDataProvidedException("file_data")
    
    try:
        decoded_bytes = base64.b64decode(file)
    except Exception:
        raise InvalidBase64DataException()
    
    try:
        decoded_str = decoded_bytes.decode('utf-8')
        df = pd.read_csv(io.StringIO(decoded_str), delimiter=delimiter)
    except Exception:
        raise InvalidCSVException()
    
    upload_dir = './src/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{file_name}.csv"
    filepath = os.path.join(upload_dir, filename)

    df.to_csv(filepath, index=False)

    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True)