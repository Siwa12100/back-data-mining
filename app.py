from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    file = request.files['file']
    delimiter = request.form.get('delimiter', ",")
    print(f"Delimiter reçu : {repr(delimiter)}")
    
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    try:
        decoded = file.stream.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(decoded), delimiter=delimiter)
        data_json = df.to_dict(orient='records')
        
        data_json = df.to_dict(orient='records')
        return jsonify({'data': data_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)