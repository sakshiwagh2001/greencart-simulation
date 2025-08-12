# backend/app.py

from flask import Flask
from config import Config
from flask_cors import CORS
from models import db,Manager
from routes import routes_bp
from load_data import load_csv_data

app = Flask(__name__)
app.config.from_object(Config)  # हे config.py मधील Config class वाचून सर्व सेटिंग्ज apply करतो

CORS(app, supports_credentials=True)  # session cookie साठी supports_credentials=True महत्वाचे आहे

db.init_app(app)


def create_default_manager():
    # Check if manager already exists
    if not Manager.query.filter_by(username="admin").first():
        manager = Manager(username="admin")
        manager.set_password("admin123")  # strong password ठेवा
        db.session.add(manager)
        db.session.commit()
        print("Default manager user created.")
    else:
        print("Manager user already exists.")
        
with app.app_context():
    db.create_all()
    create_default_manager()
    load_csv_data(app)

app.register_blueprint(routes_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True)
    
