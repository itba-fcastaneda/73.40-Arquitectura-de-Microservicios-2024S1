import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from controllers.userController import UserController
from repositories.userRepository import UserRepository
from services.userService import UserService
from controllers.pingController import PingController

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('FLASK_ENV') == 'testing':
    print("AMBIENTE APP: TESTING")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://testing:testing@db_test:3306/testing'
else:
    print("AMBIENTE APP: DEVELOPMENT")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://testing:testing@db:3306/development'

database = SQLAlchemy(app)
userRepository = UserRepository(database)
userService = UserService(userRepository)
userController = UserController(userService)

pingController = PingController()

userBP = Blueprint('users', __name__)
userBP.route('/users', methods=['GET'])(userController.get_users)
userBP.route('/users', methods=['POST'])(userController.create_user)

pingBP = Blueprint("ping", __name__)
pingBP.route("/ping", methods=['GET'])(pingController.ping)

app.register_blueprint(userBP)
app.register_blueprint(pingBP)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)