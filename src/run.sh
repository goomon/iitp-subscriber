#!/bin/bash

#docker pull postgres:latest
docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 --rm --name postgres -d postgres
sleep 5
#docker stop postgres

python main.py