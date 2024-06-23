from flask.cli import FlaskGroup

from src import create_app, db 
from src.api.models.users import User 
from src.api.models.zones import Zone


app = create_app()  # new
cli = FlaskGroup(create_app=create_app) 


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(username="fede", email="fede@gmail.com", password="password1234"))
    db.session.add(User(username="martin", email="martin@gmail.com", password="password1234"))
    db.session.add(User(username="nacho", email="nacho@gmail.com", password="password1234"))
    db.session.add(Zone(name="Belgrano"))
    db.session.add(Zone(name="San Isidro"))
    db.session.commit()


if __name__ == "__main__":
    cli()
