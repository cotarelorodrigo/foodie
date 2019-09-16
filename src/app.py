import os
import settings
from config import app_config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from user_route import pedido_blueprint

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])
db = SQLAlchemy(app)

app.register_blueprint(pedido_blueprint)

@app.route('/', methods=['GET'])
def ping():
    return jsonify({'response': 'hello world'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)


