#!/bin/bash
printf 'IAmTheMan!20040113!\n' | sudo -S apt-get update
printf 'IAmTheMan!20040113!\n' | sudo -S apt-get install -y python3.12-venv nodejs npm postgresql-16 docker.io docker-compose
