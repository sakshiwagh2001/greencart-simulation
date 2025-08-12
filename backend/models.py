from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shift_hours = db.Column(db.Integer)
    past_week_hours = db.Column(db.String(50))  # 6|8|7|...
    
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance_km = db.Column(db.Float)
    traffic_level = db.Column(db.String(50))
    base_time_min = db.Column(db.Integer)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_rs = db.Column(db.Float)
    route_id = db.Column(db.Integer, db.ForeignKey("route.id"))
    delivery_time = db.Column(db.String(10))


