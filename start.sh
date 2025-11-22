#!/bin/bash
# Smart start script: prefer Docker, fallback to local venv

set -e
echo "🌱 VIVARIUM ZERO - Starting..."

cd "$(dirname "$0")"

# Ensure .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
fi

if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
    echo "🐳 Docker detected. Starting with docker-compose..."
    docker-compose up --build -d
    echo "⏳ Waiting for backend..." && sleep 3
else
    echo "🧪 Docker not available. Starting locally via venv..."
    cd backend
    if [ ! -d venv ]; then
        echo "📦 Creating virtualenv..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -U pip
        pip install -r requirements.txt || true
    else
        source venv/bin/activate
    fi
    echo "🚀 Launching uvicorn..."
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload >/tmp/vivarium_uvicorn.log 2>&1 &
fi

echo "🌐 Open: http://localhost:8000"
echo "📊 Health: http://localhost:8000/api/health"
echo "📄 Logs (local): tail -f /tmp/vivarium_uvicorn.log"
