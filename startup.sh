#!/bin/sh

# 必要な環境変数をエクスポート
export PORT=${PORT:-5000}

# gunicornの起動コマンド
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app
