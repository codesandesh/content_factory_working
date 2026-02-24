const fs = require('fs');

const raw = fs.readFileSync('workflow.json', 'utf8');
const wf = JSON.parse(raw);

wf.nodes.forEach(node => {
  if (node.type === 'n8n-nodes-base.if') {
    // Determine target platform based on node name
    let platform = '';
    if (node.name.includes('LinkedIn')) platform = 'linkedin';
    if (node.name.includes('Facebook')) platform = 'facebook';
    if (node.name.includes('Twitter')) platform = 'twitter/x';
    if (node.name.includes('Reddit')) platform = 'reddit';
    
    if (platform) {
      node.parameters = {
        "conditions": {
          "boolean": [],
          "dateTime": [],
          "number": [],
          "string": [
            {
              "value1": "={{ $json._targetPlatform }}",
              "value2": platform
            }
          ]
        }
      };
      
      // Alternatively, newer v2 structure:
      // node.parameters.conditions = {
      //   options: {},
      //   conditions: [
      //     { id: '123', leftValue: "={{ $json._targetPlatform }}", rightValue: platform, operator: { type: "string", operation: "equals" } }
      //   ],
      //   combinator: "and"
      // };
      
      // Wait, let's use typeVersion 1 structure, it is the safest and supported by all versions.
      node.typeVersion = 1;
    }
  }
});

fs.writeFileSync('workflow.json', JSON.stringify(wf, null, 2));
console.log('Fixed IF node syntax for n8n');
