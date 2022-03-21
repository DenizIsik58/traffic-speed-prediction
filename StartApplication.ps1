#!/bin/sh
Write-Host "Starting up docker..."
docker run --name testdb -e POSTGRES_USER=postgres  -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=testdb -p 5432:5432 -d postgres
docker-compose up -d --build
Write-Host "Server is now up and running!"
 #>