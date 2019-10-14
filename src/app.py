import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import src.settings
from src.config import app_config
from src.auth.controllers.user_controller import pedido_blueprint
from src.auth.controllers.shop_controller import shops_blueprint
from src.auth.controllers.order_controller import orders_blueprint
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail, AccessDeniedException, NotFoundException

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])

db = SQLAlchemy(app)

app.register_blueprint(pedido_blueprint)
app.register_blueprint(shops_blueprint)
app.register_blueprint(orders_blueprint)

@app.errorhandler(InvalidUserInformation)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 420

@app.errorhandler(NotFoundException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 404

@app.errorhandler(NotFoundEmail)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 404

@app.errorhandler(AccessDeniedException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 401

@app.route('/', methods=['GET'])
def ping():
    return jsonify({'response': 'hello world'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)


