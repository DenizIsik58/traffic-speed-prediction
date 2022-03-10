#!/bin/sh
Write-Host "Starting up docker..."
docker-compose up -d --build traffic_speec_prediction
Write-Host "Server is now up and running!"
 #>