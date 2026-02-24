const fs = require('fs');

const raw = fs.readFileSync('workflow.json', 'utf8');
const wf = JSON.parse(raw);

// 1. Remove Switch node
wf.nodes = wf.nodes.filter(n => n.name !== 'Switch Platform');

// 2. Add back the IF nodes
const ifNodes = [
  { platform: 'linkedin', id: 'node-s3-if-linkedin', name: 'IF LinkedIn', y: 1808 },
  { platform: 'facebook', id: 'node-s3-if-facebook', name: 'IF Facebook', y: 1312 },
  { platform: 'twitter/x', id: 'node-s3-if-twitter', name: 'IF Twitter/X', y: 1632 },
  { platform: 'reddit', id: 'node-s3-if-reddit', name: 'IF Reddit', y: 1456 }
];

ifNodes.forEach(nodeDef => {
  wf.nodes.push({
    "parameters": {
      "conditions": {
        "pass": "and",
        "options": {},
        "rules": [
          {
            "value1": "={{ $json._targetPlatform }}",
            "condition": "equals",
            "value2": nodeDef.platform
          }
        ]
      },
      "options": {}
    },
    "id": nodeDef.id,
    "name": nodeDef.name,
    "type": "n8n-nodes-base.if",
    "typeVersion": 2,
    "position": [900, nodeDef.y]
  });
});

// 3. Fix Connections
// Remove old Merge node, as it was causing issues with connections and isn't strictly necessary since HTTP requests are end nodes anyway.
wf.nodes = wf.nodes.filter(n => n.name !== 'Merge All Posts' && n.name !== 'Log Published Posts');
delete wf.connections['Merge All Posts'];
delete wf.connections['Log Published Posts'];

if (wf.connections["DEBUG: Before Switch"]) {
  wf.connections["DEBUG: Before Switch"]["main"] = [
    [
      { "node": "IF LinkedIn", "type": "main", "index": 0 },
      { "node": "IF Facebook", "type": "main", "index": 0 },
      { "node": "IF Twitter/X", "type": "main", "index": 0 },
      { "node": "IF Reddit", "type": "main", "index": 0 }
    ]
  ];
}

delete wf.connections['Switch Platform'];

wf.connections["IF LinkedIn"] = { "main": [ [ { "node": "Post to LinkedIn", "type": "main", "index": 0 } ] ] };
wf.connections["IF Facebook"] = { "main": [ [ { "node": "Post to Facebook", "type": "main", "index": 0 } ] ] };
wf.connections["IF Twitter/X"] = { "main": [ [ { "node": "Post to Twitter/X", "type": "main", "index": 0 } ] ] };
wf.connections["IF Reddit"] = { "main": [ [ { "node": "Post to Reddit", "type": "main", "index": 0 } ] ] };

delete wf.connections['Post to LinkedIn'];
delete wf.connections['Post to Facebook'];
delete wf.connections['Post to Twitter/X'];
delete wf.connections['Post to Reddit'];

fs.writeFileSync('workflow.json', JSON.stringify(wf, null, 2));
console.log('Fixed workflow for n8n UI rendering');
