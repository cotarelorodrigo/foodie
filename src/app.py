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
import src.auth.auth_exception as auth
from flask_mail import Message

db = SQLAlchemy()
mail = Mail()
app = Flask('foodie-app')
CORS(app)

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

    @app.errorhandler(auth.InvalidUserInformation)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 420

    @app.errorhandler(auth.NotFoundException)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 404

    @app.errorhandler(auth.NotFoundEmail)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 405

    @app.errorhandler(auth.AccessDeniedException)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 401

    @app.errorhandler(auth.InvalidQueryParameters)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 400

    @app.errorhandler(auth.NotEnoughFavourPoints)
    def user_error_handler(e):
        return jsonify({"msg": e.msg}), 408
    
    return app


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)


