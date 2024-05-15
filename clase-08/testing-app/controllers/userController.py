from flask import jsonify, request
from services import userService

class UserController:
    def __init__(self, userService: userService.UserService) -> None:
        self.userService = userService

    def get_users(self):
        users = self.userService.get_users()
        usuarios_json = [{'name': user.name, 'email': user.email} for user in users]
        return jsonify(usuarios_json)
    
    def create_user(self):
        datos_usuario = request.get_json()
        name = datos_usuario.get('name')
        email = datos_usuario.get('email')
        self.userService.create_user(name, email)
        return jsonify({'mensaje': 'Usuario creado exitosamente'})
