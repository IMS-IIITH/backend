#!/usr/bin/env bash

docker compose -f docker-compose.prod.yml up --build -d
echo "Docker Built"

~/proxy-container.sh -c backend-backend-1 -d ims-app.iiit.ac.in -p 80
echo "Nginx Proxy Configured"