#!/bin/bash

echo "🛑 Stopping backend..."
if [ -f backend.pid ]; then
  kill $(cat backend.pid) && echo "✅ Backend stopped." || echo "⚠️ Backend already stopped or PID invalid."
  rm backend.pid
else
  echo "⚠️ No backend.pid found."
fi

echo "🛑 Stopping frontend..."
if [ -f frontend.pid ]; then
  kill $(cat frontend.pid) && echo "✅ Frontend stopped." || echo "⚠️ Frontend already stopped or PID invalid."
  rm frontend.pid
else
  echo "⚠️ No frontend.pid found."
fi

