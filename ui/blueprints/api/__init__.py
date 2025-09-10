from flask import Blueprint

# API 관련 엔드포인트를 위한 Blueprint 인스턴스 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')

# api 블루프린트에 속한 라우트(routes.py)를 임포트하여 등록합니다.
from ui.blueprints.api import routes