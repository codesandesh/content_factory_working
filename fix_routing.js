const fs = require('fs');
const wf = JSON.parse(fs.readFileSync('workflow.json', 'utf8'));

// 1. Remove the old IF nodes
const oldIfs = ['IF LinkedIn', 'IF Facebook', 'IF Twitter/X', 'IF Reddit'];
wf.nodes = wf.nodes.filter(n => !oldIfs.includes(n.name));

// 2. Add the Switch node
wf.nodes.push({
  "parameters": {
    "rules": {
      "rules": [
        { "output": 0, "operator": "equal", "value1": "={{ $json._targetPlatform }}", "value2": "linkedin" },
        { "output": 1, "operator": "equal", "value1": "={{ $json._targetPlatform }}", "value2": "facebook" },
        { "output": 2, "operator": "equal", "value1": "={{ $json._targetPlatform }}", "value2": "twitter/x" },
        { "output": 3, "operator": "equal", "value1": "={{ $json._targetPlatform }}", "value2": "reddit" }
      ]
    },
    "fallbackOutput": "none"
  },
  "id": "node-s3-switch",
  "name": "Switch Platform",
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3,
  "position": [900, 1500]
});

// 3. Update Connections
// Remove old connections from DEBUG to the IFs
if (wf.connections["DEBUG: Before Switch"]) {
  wf.connections["DEBUG: Before Switch"]["main"] = [
    [ { "node": "Switch Platform", "type": "main", "index": 0 } ]
  ];
}

// Remove old connections from IFs to target nodes
oldIfs.forEach(o => {
  if (wf.connections[o]) delete wf.connections[o];
});

// Add connections from Switch Platform to the target API nodes
wf.connections["Switch Platform"] = {
  "main": [
    [ { "node": "Post to LinkedIn", "type": "main", "index": 0 } ],
    [ { "node": "Post to Facebook", "type": "main", "index": 0 } ],
    [ { "node": "Post to Twitter/X", "type": "main", "index": 0 } ],
    [ { "node": "Post to Reddit", "type": "main", "index": 0 } ]
  ]
};

// Also fix the trailing space in Target_Platforms column name in Airtable nodes
const storeNode = wf.nodes.find(n => n.name === 'Store in Script Library');
if (storeNode && storeNode.parameters && storeNode.parameters.columns && storeNode.parameters.columns.value) {
   if (storeNode.parameters.columns.value['Target_Platforms ']) {
       storeNode.parameters.columns.value['Target_Platforms'] = storeNode.parameters.columns.value['Target_Platforms '];
       delete storeNode.parameters.columns.value['Target_Platforms '];
   }
}

const filterNode = wf.nodes.find(n => n.name === 'Filter Approved Status');
if (filterNode && filterNode.parameters && filterNode.parameters.jsCode) {
   filterNode.parameters.jsCode = filterNode.parameters.jsCode.replace(/item\.json\['Target_Platforms '\\]/g, "item.json['Target_Platforms']");
}

fs.writeFileSync('workflow.json', JSON.stringify(wf, null, 2));
console.log('Fixed routing and Target_Platforms mapping');
