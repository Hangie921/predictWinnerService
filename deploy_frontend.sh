#!/bin/bash

# 設定變數
FRONTEND_DIR="/home/walter/predictWinnerService/frontend"  # React 前端專案目錄
DEPLOY_DIR="/var/www/frontend"  # Nginx 服務的靜態檔案目錄
GIT_BRANCH="main"  # 或者你的分支名稱
NGINX_SERVICE="nginx"

echo "🚀 開始部署 React 前端..."

# 進入專案目錄
cd $FRONTEND_DIR || { echo "❌ 無法進入 $FRONTEND_DIR"; exit 1; }

# 1️⃣ 拉取最新程式碼
echo "🔄 拉取最新程式碼..."
git pull origin $GIT_BRANCH || { echo "❌ Git 拉取失敗"; exit 1; }

# 2️⃣ 安裝或更新 npm 套件
echo "📦 安裝 npm 套件..."
npm install || { echo "❌ npm 安裝失敗"; exit 1; }

# 3️⃣ 編譯 React 應用
echo "⚙️ 編譯 React 應用..."
npm run build || { echo "❌ React build 失敗"; exit 1; }

# 4️⃣ 確保部署目錄存在
echo "📂 確保部署目錄存在..."
sudo mkdir -p $DEPLOY_DIR

# 5️⃣ 移動編譯後的檔案到 `/var/www/frontend/`
echo "🚚 部署靜態檔案..."
sudo rm -rf $DEPLOY_DIR/*  # 先清空舊的檔案
sudo cp -r dist/* $DEPLOY_DIR/ || { echo "❌ 複製檔案失敗"; exit 1; }

# 6️⃣ 設定權限
echo "🔑 設定檔案權限..."
sudo chown -R www-data:www-data $DEPLOY_DIR || { echo "❌ 設定權限失敗"; exit 1; }

# 7️⃣ 重新啟動 Nginx
echo "🔄 重新啟動 Nginx..."
sudo systemctl restart $NGINX_SERVICE || { echo "❌ Nginx 重啟失敗"; exit 1; }

echo "✅ React 前端部署完成！🎉"

