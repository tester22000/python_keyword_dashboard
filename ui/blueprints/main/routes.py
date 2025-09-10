from flask import render_template, request, jsonify
from ui.blueprints.main import main_bp
from ui.services.db_services import get_distinct_site_names, get_site_keywords, get_site_links
from datetime import datetime

@main_bp.route('/')
def index():
    return render_template(
        'index.html',
    )