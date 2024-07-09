from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

send_mail_bp = Blueprint('send_mail_bp', __name__)

@send_mail_bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    member_id = data.get('memberId')
    member_name = data.get('memberName')

    if not member_id or not member_name:
        return jsonify({"error": "会員IDと会員名称は必須です"}), 400

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "hirayamadaigo5@gmail.com"  # ★ Gmailアカウント
    password = os.getenv('GMAIL_APP_PASSWORD')  # ★ Appパスワードを環境変数から取得
    receiver_email = "hirayamadaigo3@example.com"  # ★ 受信者のメールアドレス

    # メールの内容を設定
    message = MIMEMultipart("alternative")
    message["Subject"] = "新規会員追加のお知らせ"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"会員ID: {member_id}\n会員名称: {member_name} が追加されました。"
    part = MIMEText(text, "plain")
    message.attach(part)

    # Gmailサーバーに接続してメールを送信
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("メールが送信されました")
        return jsonify({"message": "メールが送信されました"}), 200
    except Exception as e:
        print(f"メール送信中にエラーが発生しました: {e}")
        return jsonify({"error": str(e)}), 500