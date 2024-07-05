from flask import Blueprint, request, jsonify
import pyodbc
import os

search_member_bp = Blueprint('search_member_bp', __name__)

connection_string = os.getenv('DB_CONNECTION_STRING')

def get_db_connection():
    if not connection_string:
        raise ValueError("接続文字列が設定されていません")
    return pyodbc.connect(connection_string)

@search_member_bp.route('/search', methods=['GET'])
def search_member():
    member_id = request.args.get('memberId')
    if not member_id:
        return jsonify({"error": "会員IDが提供されていません"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dbo.members WHERE id=?", (member_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"name": result[0]})
    else:
        return jsonify({"error": "指定されたIDは存在しません"}), 404