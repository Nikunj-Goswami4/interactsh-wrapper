from flask import Blueprint, request, jsonify
from .interact_manager import start_interactsh_session, get_interactions

bp = Blueprint('api', __name__)

@bp.route('/api/getURL', methods=['GET'])
def get_url():
    user_id = request.args.get('user', 'anonymous')
    try:
        url = start_interactsh_session(user_id)
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/getInteractions', methods=['GET'])
def interactions():
    url = request.args.get('url')
    from_ts = request.args.get('from')
    to_ts = request.args.get('to')

    if not url:
        return jsonify({"error": "Missing 'url' param"}), 400

    try:
        data = get_interactions(url, from_ts, to_ts)
        return jsonify({"interactions": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
