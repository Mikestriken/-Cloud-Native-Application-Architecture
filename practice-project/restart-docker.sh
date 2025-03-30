#!/bin/bash

# restart-docker.sh - Script to rebuild and restart Docker containers

# Set script to exit on error
set -e

echo "🔄 Stopping containers..."
docker-compose down

echo "🏗️ Rebuilding containers..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up

# Add the following line if you want to run in detached mode instead
# docker-compose up -d && echo "✅ Containers started in background. Use 'docker-compose logs -f' to view logs."