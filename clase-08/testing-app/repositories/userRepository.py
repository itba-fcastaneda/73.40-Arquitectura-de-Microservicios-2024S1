from models import user

class UserRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self):
        return self.db.session.query(user.User).all()

    def create(self,name, email):
        new_user = user.User(name=name, email=email)
        self.db.session.add(new_user)
        self.db.session.commit()