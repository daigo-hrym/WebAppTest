from flask import Blueprint, request, jsonify
import pyodbc
import os
import requests
import logging

# ロガー設定
log_file_path = '/home/site/wwwroot/app.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', handlers=[
    logging.FileHandler(log_file_path),
    logging.StreamHandler()
])

logger = logging.getLogger(__name__)

add_member_bp = Blueprint('add_member_bp', __name__)

connection_string = os.getenv('DB_CONNECTION_STRING')
send_mail_url = os.getenv('SEND_MAIL_URL')  # 環境変数からメール送信APIのURLを取得

def get_db_connection():
    if not connection_string:
        raise ValueError("接続文字列が設定されていません")
    return pyodbc.connect(connection_string)

@add_member_bp.route('/add', methods=['POST'])
def add_member():
    logger.debug("Received request to add member")
    data = request.get_json()
    member_id = data.get('memberId')
    member_name = data.get('memberName')

    if not member_id or not member_name:
        logger.error("会員IDと会員名称は必須です")
        return jsonify({"error": "会員IDと会員名称は必須です"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM dbo.members WHERE id=?", (member_id,))
    if cursor.fetchone()[0] > 0:
        logger.warning("既に存在している会員IDです: %s", member_id)
        return jsonify({"error": "既に存在している会員IDです"}), 400

    cursor.execute("INSERT INTO dbo.members (id, name) VALUES (?, ?)", (member_id, member_name))
    conn.commit()
    conn.close()
    logger.info("会員が追加されました: ID=%s, 名前=%s", member_id, member_name)

    # メール送信APIを呼び出し
    try:
        logger.debug("Sending request to send_mail API: %s", send_mail_url)
        response = requests.post(
            send_mail_url,
            json={"memberId": member_id, "memberName": member_name}
        )
        response.raise_for_status()
        logger.info("メール送信API呼び出し成功: %s", response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error("メール送信API呼び出し失敗: %s", e)
        return jsonify({"error": f"メール送信中にエラーが発生しました: {e}"}), 500

    return jsonify({"message": "会員が追加されました"}), 201