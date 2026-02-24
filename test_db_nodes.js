const fs = require('fs');

try {
  const rawNodes = fs.readFileSync('db_nodes.json', 'utf8').trim();
  const parsedNodes = JSON.parse(rawNodes);

  // Read workflow.json connections
  const wfRaw = fs.readFileSync('workflow.json', 'utf8');
  const wf = JSON.parse(wfRaw);
  
  // Validate connections against nodes
  const nodeNames = new Set(parsedNodes.map(n => n.name));
  
  let invalidConnections = 0;
  
  for (const sourceNode in wf.connections) {
    if (!nodeNames.has(sourceNode)) {
      console.log(`❌ Source node '${sourceNode}' in connections does not exist in nodes!`);
      invalidConnections++;
    }
    
    // Check targets
    for (const outputType in wf.connections[sourceNode]) {
      const targets = wf.connections[sourceNode][outputType];
      for (const targetArray of targets) {
        if (targetArray) {
          for (const target of targetArray) {
             if (target && target.node && !nodeNames.has(target.node)) {
                console.log(`❌ Target node '${target.node}' in connections does not exist in nodes!`);
                invalidConnections++;
             }
          }
        }
      }
    }
  }
  
  if (invalidConnections === 0) {
    console.log('✅ All connections map to valid nodes.');
  } else {
    console.log(`❌ Found ${invalidConnections} invalid connections!`);
  }

} catch (e) {
  console.log('Error parsing JSON:', e.message);
}
