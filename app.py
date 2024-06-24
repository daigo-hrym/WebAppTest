from flask import Flask, request, jsonify, render_template, send_from_directory
import logging
import pyodbc
import os
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# ログ設定
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=1, encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# 環境変数から接続情報を取得
connection_string = os.getenv('DB_CONNECTION_STRING')

# デバッグ用のログを追加
if not connection_string:
    app.logger.error("接続文字列が設定されていません")
else:
    app.logger.info(f"接続文字列: {connection_string}")

port = int(os.getenv('PORT', 61234))  # 環境変数からポートを取得、デフォルトは 61234

def get_db_connection():
    if not connection_string:
        raise ValueError("接続文字列が設定されていません")
    app.logger.info(f"接続文字列: {connection_string}")
    conn = pyodbc.connect(connection_string)
    return conn

def get_member_name(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dbo.members WHERE id=?", (member_id,))
    result = cursor.fetchone()
    conn.close()
    app.logger.info(f"SQLクエリ結果: {result}")
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_member():
    member_id = request.args.get('memberId')
    if not member_id:
        return jsonify({"error": True, "message": "会員IDが提供されていません"}), 400
    
    member_name = get_member_name(member_id)
    if member_name:
        app.logger.info(f"正常終了: 会員ID {member_id} の名称は {member_name[0]} です")
        return jsonify({"error": False, "name": member_name[0]})
    else:
        app.logger.error(f"エラー: 指定されたID {member_id} は存在しません")
        return jsonify({"error": True, "message": "指定されたIDは存在しません"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)