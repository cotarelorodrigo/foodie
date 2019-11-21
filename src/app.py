import os
from flask import Flask, jsonify
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import src.settings
from src.config import app_config
from src.auth.controllers.user_controller import user_blueprint
from src.auth.controllers.admin_controller import admins_blueprint
from src.auth.controllers.shop_controller import shops_blueprint
from src.auth.controllers.order_controller import orders_blueprint
from src.auth.controllers.register_controller import register_blueprint
from src.auth.controllers.login_controller import login_blueprint
from src.auth.controllers.direc_controller import direc_blueprint
from src.auth.controllers.delivery_controller import delivery_blueprint
from src.auth.controllers.products_controller import products_blueprint
import src.auth.auth_exception as auth_exception
from flask_mail import Message
import firebase_admin
from firebase_admin import credentials
import logging

db = SQLAlchemy()
mail = Mail()
app = Flask('foodie-app')
CORS(app)

fb_config = {
    "type":os.environ.get("FIREBASE_ADMIN_TYPE"),
    "project_id":os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key":os.environ.get("FIREBASE_PRIVATE_KEY"),
    "client_email":os.environ.get("FIREBASE_CLIENT_EMAIL")
}
try:
    default_app = firebase_admin.initialize_app(credentials.Certificate({
        "project_id":os.environ.get("FIREBASE_PROJECT_ID"),
        "type":os.environ.get("FIREBASE_ADMIN_TYPE"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "token_uri": "https://oauth2.googleapis.com/token"

    }))
    logging.info("Connected to firebase app")
except ValueError as err:
    logging.error("Unable to connect")
    logging.error("Client email:"+fb_config["client_email"])
    logging.error("Private key"+fb_config["private_key"])
    logging.error(err)

def send_email(msg_info):
    with app.app_context():
        msg = Message(msg_info["tittle"], recipients=msg_info["recipients"])
        msg.body = msg_info["body"]
        mail.send(msg)

def create_app():
    app.config.from_object(app_config[os.getenv('APP_SETTINGS')])
    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(shops_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)
    #app.register_blueprint(direc_blueprint)
    app.register_blueprint(admins_blueprint)
    app.register_blueprint(delivery_blueprint)
    app.register_blueprint(products_blueprint)

    @app.errorhandler(auth_exception.InvalidUserInformation)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 420

    @app.errorhandler(auth_exception.NotFoundException)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 404

    @app.errorhandler(auth_exception.NotFoundEmail)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 405

    @app.errorhandler(auth_exception.AccessDeniedException)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 401

    @app.errorhandler(auth_exception.InvalidQueryParameters)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 400

    @app.errorhandler(auth_exception.NotEnoughFavourPoints)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 408
    
    return app


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)


