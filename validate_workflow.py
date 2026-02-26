import json
import sys

def validate_n8n_workflow(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Syntax Error: {e}")
        return
    except Exception as e:
        print(f"❌ Read Error: {e}")
        return

    nodes = workflow.get('nodes', [])
    node_names = {node['name'] for node in nodes}
    node_ids = {node['id'] for node in nodes}
    
    print(f"✅ JSON is valid. Found {len(nodes)} nodes.")
    
    connections = workflow.get('connections', {})
    errors = []
    
    # Check if all source nodes in connections exist
    for source_node_name in connections:
        if source_node_name not in node_names:
            errors.append(f"Connection error: Source node '{source_node_name}' does not exist in 'nodes' array.")
            
        # Check if all target nodes in connections exist
        for connection_type in connections[source_node_name]:
            for connection_list in connections[source_node_name][connection_type]:
                for target_info in connection_list:
                    target_node_name = target_info.get('node')
                    if target_node_name not in node_names:
                        errors.append(f"Connection error: Target node '{target_node_name}' (from '{source_node_name}') does not exist in 'nodes' array.")

    # Check for duplicate node names or IDs (n8n requires unique names)
    seen_names = set()
    for node in nodes:
        name = node['name']
        if name in seen_names:
            errors.append(f"Validation error: Duplicate node name '{name}' found.")
        seen_names.add(name)

    if errors:
        print("\n".join(errors))
    else:
        print("✅ No connection errors or duplicate names found.")

if __name__ == "__main__":
    validate_n8n_workflow('nepali_congress.json')
