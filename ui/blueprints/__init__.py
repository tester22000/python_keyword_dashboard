from flask import Blueprint

# 메인 웹 페이지를 위한 Blueprint
main_bp = Blueprint('main', __name__, template_folder='templates')

# API 엔드포인트를 위한 Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

from . import main, api