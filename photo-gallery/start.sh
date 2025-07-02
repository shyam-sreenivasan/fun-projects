#!/bin/bash

IMAGE_DIR="$1"

./stop.sh

if [ -z "$IMAGE_DIR" ]; then
  echo "❌ Please provide image directory path."
  echo "Usage: ./start.sh /path/to/images"
  exit 1
fi

echo "🚀 Starting backend..."
cd backend
node index.js "$IMAGE_DIR" > ../server.log 2>&1 &
echo $! > ../backend.pid
cd ..

echo "🚀 Starting frontend..."
cd frontend
npm run dev > ../client.log 2>&1 &
echo $! > ../frontend.pid
cd ..

echo "✅ Both frontend and backend started."
