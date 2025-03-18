#!/bin/bash

# 設定變數
APP_DIR="/home/walter/predictWinnerService/backend"
VENV_DIR="$APP_DIR/venv"
GIT_BRANCH="main"  # 或者你的分支名稱
GUNICORN_SERVICE="gunicorn"
NGINX_SERVICE="nginx"

echo "🚀 開始部署 Django 更新..."

# 進入專案目錄
cd $APP_DIR || { echo "❌ 無法進入 $APP_DIR"; exit 1; }

# 1️⃣ 拉取最新程式碼
echo "🔄 拉取最新程式碼..."
git pull origin $GIT_BRANCH || { echo "❌ Git 拉取失敗"; exit 1; }

# 2️⃣ 啟用虛擬環境
echo "🐍 啟動虛擬環境..."
source $VENV_DIR/bin/activate || { echo "❌ 無法啟動虛擬環境"; exit 1; }

# 3️⃣ 更新 Python 套件（如果有變更）
echo "📦 更新 Python 套件..."
pip install -r requirements.txt || { echo "❌ 套件安裝失敗"; exit 1; }

# 4️⃣ 執行資料庫遷移（如果有變更）
echo "🛠 執行資料庫遷移..."
python manage.py migrate || { echo "❌ 資料庫遷移失敗"; exit 1; }

# 5️⃣ 收集靜態檔案
#echo "📁 收集靜態檔案..."
# python manage.py collectstatic --noinput || { echo "❌ 收集靜態檔案失敗"; exit 1; }

# 6️⃣ 重新啟動 Gunicorn
echo "🔄 重新啟動 Gunicorn..."
sudo systemctl restart $GUNICORN_SERVICE || { echo "❌ Gunicorn 重啟失敗"; exit 1; }

# 7️⃣ 重新啟動 Nginx
echo "🔄 重新啟動 Nginx..."
sudo systemctl restart $NGINX_SERVICE || { echo "❌ Nginx 重啟失敗"; exit 1; }

echo "✅ Django 部署完成！🎉"

