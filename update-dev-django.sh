#!/bin/bash
echo "[START]"

echo "---stopping django---"
docker compose -f docker-compose.yml -f docker-compose.dev.yml stop django

echo "---removing container and image---"
docker compose -f docker-compose.yml -f docker-compose.dev.yml down --rmi all

echo "---restarting django---"
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

echo "[END]"