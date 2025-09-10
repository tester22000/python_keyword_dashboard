import os
from flask import Flask

from ui.blueprints.main.routes import main_bp
from ui.blueprints.api.routes import api_bp

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app