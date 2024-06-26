#!/bin/bash

# 環境変数の確認
echo "PORT before setting: $PORT" >> /home/LogFiles/startup.log
echo "DB_CONNECTION_STRING before setting: $DB_CONNECTION_STRING" >> /home/LogFiles/startup.log

# ★ 環境変数の設定（明示的に設定）
export PATH=$PATH:/home/.local/bin

# ★ DB_CONNECTION_STRING を明示的に設定
export DB_CONNECTION_STRING='Driver={ODBC Driver 17 for SQL Server};Server=tcp:webapptest-sqlserver.database.windows.net,1433;Database=mydatabase;Uid=NormalUser1;Pwd=WebAppServerTestP@SS_1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
export PORT=61234

# 環境変数の確認
echo "PORT after setting: $PORT" >> /home/LogFiles/startup.log
echo "DB_CONNECTION_STRING after setting: $DB_CONNECTION_STRING" >> /home/LogFiles/startup.log

# リポジトリのディレクトリに移動
cd /home/site/wwwroot

# gunicornの起動コマンド
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug app:app