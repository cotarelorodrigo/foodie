import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import src.settings
from src.config import app_config
from src.auth.controllers.user_controller import pedido_blueprint
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])

db = SQLAlchemy(app)

app.register_blueprint(pedido_blueprint)

@app.errorhandler(InvalidUserInformation)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 420

@app.errorhandler(InvalidUserInformation)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 420

@app.errorhandler(NotFoundEmail)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 404

@app.route('/', methods=['GET'])
def ping():
    return jsonify({'response': 'hello world'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)


