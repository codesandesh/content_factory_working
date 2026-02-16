#!/bin/bash

# Viral Content Factory - Local Start Script
set -e

echo "Starting Viral Content Factory..."
echo "===================================="

# Check for .env file
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys."
    exit 1
fi

# Create necessary directories
echo "Creating local directories..."
mkdir -p media scripts videos logs backups/postgres

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running!"
    exit 1
fi

# Start services
echo "Launching containers..."
docker compose up -d

echo ""
echo "Workflow is ready to be imported!"
echo "------------------------------------"
echo "n8n URL:   http://localhost:5678"
echo "Username:  admin"
echo "Password:  adminpassword"
echo ""
echo "Next: Import 'workflow.json' in n8n and set up Airtable."
echo ""
