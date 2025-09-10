# blueprints/api/routes.py
from flask import jsonify, request
from ui.blueprints.api import api_bp
from ui.services.db_services import (
    get_site_links, 
    delete_site_links, 
    get_site_keywords,
    get_distinct_site_names
)
from datetime import datetime

@api_bp.route('/links')
def api_get_links():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        name = request.args.get('name')
        keyword = request.args.get('keyword')
        search = request.args.get('search')
        date = request.args.get('date')

        # If no date is provided, default to the current date
        if not date:
            date = datetime.now().strftime('%Y%m%d')

        # Fetch links using the service function
        links_data = get_site_links(page=page, limit=limit, name=name, keyword=keyword, date=date, search=search)

        # Determine if there's more data to load (for infinite scroll)
        has_more = len(links_data) == limit
        
        return jsonify({
            'links': links_data,
            'has_more': has_more,
            'current_page': page
        })

    except Exception as e:
        # Log the error in a real application
        print(f"Error fetching links: {e}") 
        return jsonify({'error': str(e)}), 500

@api_bp.route('/keywords')
def api_get_keywords():
    try:
        date = request.args.get('date', datetime.now().strftime('%Y%m%d'))
        name = request.args.get('name') 
        keyword_filter = request.args.get('keyword')

        keywords_data = get_site_keywords(date=date, name=name, keyword=keyword_filter)

        return jsonify({
            'keywords': keywords_data
        })
    except Exception as e:
        print(f"Error fetching keywords: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/links/delete', methods=['POST'])
def api_delete_links():
    """
    Deletes site_links entries based on a list of IDs sent in the request body.
    Requires a POST request with a JSON body like: {"ids": [1, 5, 10]}
    """
    try:
        data = request.get_json()
        if not data or 'ids' not in data or not isinstance(data['ids'], list):
            return jsonify({'error': 'Invalid request body. Expected JSON with an "ids" array.'}), 400

        link_ids_to_delete = data['ids']
        
        if not link_ids_to_delete:
            return jsonify({'message': 'No IDs provided for deletion.'})

        # Basic validation: ensure all IDs are integers (you might add more robust checks)
        if not all(isinstance(id, int) for id in link_ids_to_delete):
            return jsonify({'error': 'All IDs must be integers.'}), 400

        delete_site_links(link_ids_to_delete)
        return jsonify({'message': f'{len(link_ids_to_delete)} links deleted successfully.'})

    except sqlite3.Error as e:
        print(f"Database error during deletion: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"Error deleting links: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/site_names')
def api_get_site_names():
    """
    Fetches distinct site names for a given date.
    Useful if the date selector is dynamic.
    """
    try:
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y%m%d')
        
        site_names_data = get_distinct_site_names(date=date)
        return jsonify({'site_names': [item['name'] for item in site_names_data]})
    except Exception as e:
        print(f"Error fetching site names: {e}")
        return jsonify({'error': str(e)}), 500