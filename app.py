from flask import Flask,jsonify,redirect,url_for,render_template
from flask import request
from function import clean_phone_number,clean_data,clean_kata
from sql import create_db


from flask import Flask, jsonify, request
from flask import render_template, redirect, url_for
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd
import re
import sqlite3

import pandas as pd
###Flask kredensial
app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

########swagerr
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                    config=swagger_config)


@swag_from("docs/nomor_hp.yml", methods=['POST'])
@app.route('/nomor_hp', methods=['POST'])
def input_kata():
    variable_kata = request.form.get('kata')
    
    json_response = {
        'status_code': 200,
        'description': "Kata telah di cleansing",
        'data': clean_kata(variable_kata)
    }
    
    return jsonify(json_response)

@swag_from("docs/upload_data.yml", methods=['POST'])
@app.route('/upload_data', methods=['POST'])
def upload_data():
    df = request.files['df']

    # Process the data
    cleaned_data = clean_data(df)
    create_db(cleaned_data)

    # Return a JSON response
    return jsonify({
        'status_code': 200,
        'description': "file yang sudah diproses",
        'data': cleaned_data
    })



### running api
if  __name__ == "__main__":
    app.run()