# Restart-Docker.ps1 - Script to rebuild and restart Docker containers

Write-Host "🔄 Stopping containers..." -ForegroundColor Cyan
docker-compose down

Write-Host "🏗️ Rebuilding containers..." -ForegroundColor Yellow
docker-compose build

Write-Host "🚀 Starting containers..." -ForegroundColor Green
docker-compose up

# Add the following line if you want to run in detached mode instead
# docker-compose up -d; Write-Host "✅ Containers started in background. Use 'docker-compose logs -f' to view logs." -ForegroundColor Green