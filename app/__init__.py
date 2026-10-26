from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    UPLOAD_PATH = Path(app.root_path) / 'static' / 'files'
    UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    return app