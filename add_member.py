import os
import logging
from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'add_member.log')
handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=1, encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

connection_string = os.getenv('DB_CONNECTION_STRING')

def get_db_connection():
    if not connection_string:
        app.logger.error(f"接続文字列が設定されていません: {connection_string}")
        raise ValueError("接続文字列が設定されていません")

    conn_str = connection_string

    try:
        conn = pyodbc.connect(conn_str)
        app.logger.info(f"DB接続成功 - connection_string: {connection_string}")
        return conn
    except Exception as e:
        app.logger.error(f"DB接続失敗 - connection_string: {connection_string}, error: {e}")
        raise

@app.route('/add', methods=['POST'])
def add_member():
    data = request.get_json()
    member_id = data.get('memberId')
    member_name = data.get('memberName')

    if not member_id or not member_name:
        return jsonify({"error": True, "message": "会員IDと会員名称は必須です"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(1) FROM dbo.members WHERE id=?", (member_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": True, "message": "既に存在している会員IDです"}), 400

        cursor.execute("INSERT INTO dbo.members (id, name) VALUES (?, ?)", (member_id, member_name))
        conn.commit()
        conn.close()
        return jsonify({"error": False, "memberId": member_id, "memberName": member_name}), 200
    except Exception as e:
        app.logger.error(f"DB操作失敗: {e}")
        return jsonify({"error": True, "message": "データベースエラー"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)