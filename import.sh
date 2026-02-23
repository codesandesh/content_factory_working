#!/bin/bash

# Quick Import Workflow to n8n
# Use this to import missing workflows

set -e

N8N_CONTAINER="n8n_content_factory"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        📥 Quick Import Workflow                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if [ -z "$1" ]; then
  echo "Usage: ./import.sh <workflow_file> [workflow_name]"
  echo ""
  echo "Examples:"
  echo "  ./import.sh workflow.json"
  echo "  ./import.sh veogenerate.json"
  echo ""
  echo "Available workflows:"
  ls -1 *.json 2>/dev/null | grep -v credentials
  exit 1
fi

WORKFLOW_FILE="$1"

if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "❌ File not found: $WORKFLOW_FILE"
  exit 1
fi

echo "Importing: $WORKFLOW_FILE"
docker cp "$WORKFLOW_FILE" "$N8N_CONTAINER:/tmp/$WORKFLOW_FILE" > /dev/null 2>&1
RESULT=$(docker exec $N8N_CONTAINER n8n import:workflow --input="/tmp/$WORKFLOW_FILE" 2>&1)

if echo "$RESULT" | grep -q "successfully imported"; then
  echo "✅ Successfully imported!"
  
  sleep 2
  
  echo ""
  echo "Current workflows in n8n:"
  docker exec n8n_postgres psql -U n8n -d n8n -c "SELECT name FROM workflow_entity ORDER BY name;" 2>&1
else
  echo "⚠️ Result: $RESULT"
fi
