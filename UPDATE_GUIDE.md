# 🔄 Workflow Update Guide - No Duplicates

## Overview

These tools help you **update existing workflows without creating duplicates**:

- **update_manager.py** - Smart update manager with change detection
- **update_workflows.sh** - Simple bash updater  
- **export_workflows.sh** - Export workflows from n8n to JSON

## 📋 Workflow

### Option 1: Update via Python (Recommended)

```bash
# Interactive menu
python3 update_manager.py

# Or direct update
python3 update_manager.py --update workflow.json "Viral Content Factory"

# List workflows
python3 update_manager.py --list
```

**Features:**
- ✅ Detects changes in JSON files
- ✅ Shows which workflows have updates
- ✅ Updates in-place without duplicates
- ✅ Interactive menu for easy selection

### Option 2: Update via Bash

```bash
# Interactive selection of which workflow to update
./update_workflows.sh

# Updates one workflow at a time
# No duplicates created
```

### Option 3: Export & Sync Workflow

```bash
# Export current workflows from n8n to JSON
./export_workflows.sh

# Then update using update_manager.py
python3 update_manager.py
```

## 🔄 Complete Workflow (Step by Step)

### Step 1: Make Changes in n8n UI

1. Go to http://localhost:5678
2. Open a workflow
3. Add/modify nodes
4. **Save** the workflow

### Step 2: Export Updated Workflows

```bash
./export_workflows.sh
```

This creates JSON files in `workflow-exports/` directory with your changes.

### Step 3: Sync Back to Source

```bash
# Copy exported version back to source
cp workflow-exports/viral_content_factory.json workflow.json

# Or use the update manager
python3 update_manager.py --update workflow.json "Viral Content Factory"
```

### Step 4: Version Control (Optional)

```bash
git add workflow.json
git commit -m "Update: Added new node to Viral Content Factory"
git push
```

## 🎯 Practical Example

### Scenario: Add a new node to "Viral Content Factory"

**In n8n UI:**
1. Go to Workflows → Viral Content Factory
2. Click "+" → Add node (e.g., Filter node)
3. Configure the node
4. Click Save

**In Terminal:**
```bash
# Export the updated workflow
./export_workflows.sh

# Check if changes detected
python3 update_manager.py

# You'll see: ⭐ (has changes) next to Viral Content Factory

# Update back to JSON file
python3 update_manager.py --update workflow.json "Viral Content Factory"

# Or copy from export
cp workflow-exports/viral_content_factory.json workflow.json

# Commit
git add workflow.json
git commit -m "Add Filter node to Viral Content Factory"
```

## 🚫 How to NOT Create Duplicates

### ❌ WRONG - Do NOT do this:
```bash
# This creates a duplicate!
./import_direct.sh
```

### ✅ RIGHT - Do this instead:
```bash
# This updates existing workflow
python3 update_manager.py

# Or export and sync
./export_workflows.sh
python3 update_manager.py --update workflow.json "Workflow Name"
```

## 📊 Comparing Workflows

### Check current workflows in n8n:
```bash
python3 update_manager.py --list

# Output shows:
# id | name
# ---|---
# abc123 | Viral Content Factory
# def456 | Stage 3 - VEO B-Roll Generation
# etc...
```

### Export for comparison:
```bash
./export_workflows.sh

ls -lah workflow-exports/
# Shows all exported JSON files with timestamps
```

## 🔧 Command Reference

| Command | Purpose | Result |
|---------|---------|--------|
| `python3 update_manager.py` | Interactive menu | Choose workflow to update |
| `./update_workflows.sh` | Bash updater | Menu-based update |
| `./export_workflows.sh` | Export all workflows | Creates `workflow-exports/` |
| `python3 update_manager.py --list` | Show workflows | Lists all in n8n |
| `python3 update_manager.py --update file.json "Name"` | Direct update | Updates specific workflow |

## 📝 Workflow JSON Structure

Each workflow JSON has:
```json
{
  "id": "workflow_id_from_db",
  "name": "Workflow Name",
  "nodes": [...],
  "connections": [...],
  "createdAt": "...",
  "updatedAt": "..."
}
```

When you run `update_manager.py`, it:
1. Reads the JSON file
2. Finds workflow by name in n8n database
3. Imports/updates it in-place
4. **No duplicate created** ✅

## 🆘 Troubleshooting

### Issue: Still creating duplicates

**Problem:** Using `import_direct.sh` or `./import_workflows.sh`

**Solution:** Use `update_manager.py` instead

```bash
python3 update_manager.py
```

### Issue: Workflow updates but changes don't show

**Solution:** Refresh n8n browser tab

```
1. Go to http://localhost:5678
2. Press F5 or Ctrl+Shift+R (hard refresh)
3. Open Workflows menu again
```

### Issue: Can't find workflow by name

**Solution:** List workflows first

```bash
python3 update_manager.py --list

# Use exact name shown in output
```

## ✨ Best Practices

1. **Always export before major changes**
   ```bash
   ./export_workflows.sh
   ```

2. **Use descriptive commit messages**
   ```bash
   git commit -m "Update: Added error handling to VEO generation workflow"
   ```

3. **Keep backups of working versions**
   ```bash
   cp workflow.json workflow.backup.json
   ```

4. **Test in n8n before committing**
   - Make changes
   - Test execution
   - Export
   - Commit

5. **Use version control**
   ```bash
   git diff workflow.json  # See what changed
   git log workflow.json   # See history
   ```

## 🚀 Quick Reference

```bash
# View all workflows
python3 update_manager.py --list

# Make changes in n8n UI, then:

# Option A: Auto-update
python3 update_manager.py

# Option B: Manual export + update
./export_workflows.sh
cp workflow-exports/your_workflow.json workflow.json

# Commit changes
git add workflow.json
git commit -m "Update workflow"
```

---

**Key Point:** 
- ✅ Use `update_manager.py` to prevent duplicates
- ✅ Use `export_workflows.sh` to sync from n8n
- ❌ Never run `import_direct.sh` to update existing workflows
