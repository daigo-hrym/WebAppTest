from flask import Flask, request, jsonify
import logging
import pyodbc

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

# データベース接続設定
server = 'myserver.database.windows.net'
database = 'mydatabase'
username = 'adminuser'
password = 'password123'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# データベース接続の確立
def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

def get_member_name(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dbo.members WHERE id=?", (member_id,))
    result = cursor.fetchone()
    conn.close()
    return result

@app.route('/search', methods=['GET'])
def search_member():
    member_id = request.args.get('memberId')
    if not member_id:
        return jsonify({"error": True, "message": "会員IDが提供されていません"}), 400
    
    member_name = get_member_name(member_id)
    if member_name:
        logging.info(f"正常終了: 会員ID {member_id} の名称は {member_name[0]} です")
        return jsonify({"error": False, "name": member_name[0]})
    else:
        logging.error(f"エラー: 指定されたID {member_id} は存在しません")
        return jsonify({"error": True, "message": "指定されたIDは存在しません"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
