#!/bin/bash

# 環境変数の確認
echo "PORT before setting: $PORT" >> /home/LogFiles/startup.log
echo "DB_CONNECTION_STRING before setting: $DB_CONNECTION_STRING" >> /home/LogFiles/startup.log

# ★ 必要な環境変数をエクスポート
export PATH=$PATH:/home/.local/bin

# ★ 環境変数の設定（確実にエクスポートされるように）
export PORT=61234
export DB_CONNECTION_STRING="$DB_CONNECTION_STRING"

# 環境変数の確認
echo "PORT after setting: $PORT" >> /home/LogFiles/startup.log
echo "DB_CONNECTION_STRING after setting: $DB_CONNECTION_STRING" >> /home/LogFiles/startup.log

# リポジトリのディレクトリに移動
cd /home/site/wwwroot

# gunicornの起動コマンド
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug app:app