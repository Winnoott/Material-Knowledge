from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure upload folder exists
upload_folder = app.config.get('UPLOAD_FOLDER', os.path.join(app.instance_path, 'uploads'))
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Inisialisasi SQLAlchemy
db = SQLAlchemy(app)

# Inisialisasi Flask-Migrate
migrate = Migrate(app, db)

# Import models dan routes setelah db diinisialisasi
from app import models, routes
