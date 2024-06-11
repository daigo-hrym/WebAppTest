#!/bin/sh

# 環境変数の確認
echo "PORT before setting: $PORT" >> /home/LogFiles/startup.log

# 必要な環境変数をエクスポート
export PATH=$PATH:/home/.local/bin

# 環境変数を 61234 に強制的に設定
export PORT=61234
echo "PORT after setting to 61234: $PORT" >> /home/LogFiles/startup.log

# gunicornの起動コマンド
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app