#!/bin/bash

echo "Importing all 4 workflows..."
echo ""

WORKFLOWS=(
  "workflow.json"
  "veogenerate.json"
  "heygenvideo.json"
  "submagicvideo.json"
)

for file in "${WORKFLOWS[@]}"; do
  echo "Importing $file..."
  ./import.sh "$file"
  sleep 2
done

echo ""
echo "Final state:"
docker exec n8n_postgres psql -U n8n -d n8n -c "SELECT ROW_NUMBER() OVER (ORDER BY name) as no, name FROM workflow_entity ORDER BY name;" 2>&1
