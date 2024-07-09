from flask import Flask, render_template
from search_member import search_member_bp
from add_member import add_member_bp
from send_mail import send_mail_bp  # ★ 追加

app = Flask(__name__)
app.register_blueprint(search_member_bp)
app.register_blueprint(add_member_bp)
app.register_blueprint(send_mail_bp)  # ★ 追加

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)