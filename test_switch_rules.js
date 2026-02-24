const fs = require('fs');
const wfRaw = fs.readFileSync('workflow.json', 'utf8');
const wf = JSON.parse(wfRaw);
const switchNode = wf.nodes.find(n => n.name === 'Switch Platform');
console.log(JSON.stringify(switchNode.parameters.rules, null, 2));
