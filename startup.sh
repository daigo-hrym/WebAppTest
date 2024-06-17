#!/bin/sh

# 環境変数の確認
echo "PORT before setting: $PORT" >> /home/LogFiles/startup.log

# 必要な環境変数をエクスポート
export PATH=$PATH:/home/.local/bin

# gunicornの起動コマンド
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug app:app