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

# Source .env for dynamic credential generation
set -a
source .env
set +a

# Generate n8n credentials from .env
echo "Generating n8n credentials..."
cat <<EOF > credentials.json
[
  {
    "id": "h68hvDXg5Xigfz5P",
    "name": "Airtable Personal Access Token account",
    "type": "airtableTokenApi",
    "data": {
      "accessToken": "$AIRTABLE_API_KEY"
    }
  },
  {
    "id": "igaSdthsiO1WHIs5",
    "name": "Google Gemini(PaLM) Api account",
    "type": "googlePalmApi",
    "data": {
      "apiKey": "$GOOGLE_GEMINI_API_KEY"
    }
  }
]
EOF

# Start services
echo "Launching containers..."
docker compose up -d

# Automated Import
echo "Automating n8n setup..."
docker cp workflow.json n8n_content_factory:/tmp/workflow.json
docker cp credentials.json n8n_content_factory:/tmp/credentials.json

docker exec n8n_content_factory n8n import:credentials --input=/tmp/credentials.json || true
docker exec n8n_content_factory n8n import:workflow --input=/tmp/workflow.json --update || true

echo ""
echo "Viral Content Factory is LIVE! 🚀"
echo "------------------------------------"
echo "n8n URL:   http://localhost:5678"
echo "Status:    Workflow & Credentials pre-loaded."
echo ""
echo "Next: Create your owner account at the URL above."
echo ""
