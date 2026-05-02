#!/bin/bash

set -e

# Replace API URL placeholders with environment variables
if [ -n "$SKYVERN_API_URL" ]; then
    find /app/dist -name "*.js" -exec sed -i "s|__VITE_API_BASE_URL_PLACEHOLDER__|${SKYVERN_API_URL}|g" {} \;
    find /app/dist -name "*.js" -exec sed -i "s|__VITE_WSS_BASE_URL_PLACEHOLDER__|${SKYVERN_WSS_URL:-ws://skyvern:8000}|g" {} \;
    find /app/dist -name "*.js" -exec sed -i "s|__VITE_ARTIFACT_API_BASE_URL_PLACEHOLDER__|${SKYVERN_ARTIFACT_URL:-http://skyvern:8000}|g" {} \;
fi

if [ -n "$SKYVERN_API_KEY" ]; then
    find /app/dist -name "*.js" -exec sed -i "s|__SKYVERN_API_KEY_PLACEHOLDER__|${SKYVERN_API_KEY}|g" {} \;
fi

echo "Starting frontend server..."
exec node /app/localServer.js
