from flask import Blueprint, request, jsonify
import pyodbc
import os

add_member_bp = Blueprint('add_member_bp', __name__)

connection_string = os.getenv('DB_CONNECTION_STRING')

def get_db_connection():
    if not connection_string:
        raise ValueError("接続文字列が設定されていません")
    return pyodbc.connect(connection_string)

@add_member_bp.route('/add', methods=['POST'])
def add_member():
    data = request.get_json()
    member_id = data.get('memberId')
    member_name = data.get('memberName')

    if not member_id or not member_name:
        return jsonify({"error": "会員IDと会員名称は必須です"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM dbo.members WHERE id=?", (member_id,))
    if cursor.fetchone()[0] > 0:
        return jsonify({"error": "既に存在している会員IDです"}), 400

    cursor.execute("INSERT INTO dbo.members (id, name) VALUES (?, ?)", (member_id, member_name))
    conn.commit()
    conn.close()

    return jsonify({"message": "会員が追加されました"}), 201