from flask import Flask, request, jsonify, render_template, send_from_directory
import logging
import pymssql
import os
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# ログ設定
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=1, encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levellevelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# 簡易ログファイル
simple_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simple_app.log')
with open(simple_log_path, 'w') as f:
    f.write('簡易ログファイルの作成に成功しました。\n')

# テストログを追加
app.logger.debug("ログ設定が完了しました。")

# ハードコーディングされた接続文字列
connection_string = "Server=tcp:webapptest-sqlserver.database.windows.net,1433;Initial Catalog=mydatabase;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;Authentication='Active Directory Default'"

port = int(os.getenv('PORT', 61234))
app.logger.debug(f"アプリケーションはポート {port} で実行されます。")

def get_db_connection():
    try:
        conn = pymssql.connect(connection_string)
        app.logger.info("DB接続成功")
        return conn
    except Exception as e:
        app.logger.error(f"DB接続失敗: {e}")
        raise

def get_member_name(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM dbo.members WHERE id=%s", (member_id,))
        result = cursor.fetchone()
        conn.close()
        app.logger.info(f"SQLクエリ結果: {result}")
        return result
    except Exception as e:
        app.logger.error(f"DB操作失敗: {e}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_member():
    member_id = request.args.get('memberId')
    app.logger.info(f"画面から受け取った会員ID: {member_id}")
    app.logger.info(f"使用する接続情報: {connection_string}")

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