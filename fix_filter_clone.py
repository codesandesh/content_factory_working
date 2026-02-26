import json

with open('/home/sandesh-neupane/n8n/workflow.json', 'r') as f:
    wf = json.load(f)

for node in wf['nodes']:
    name = node.get('name')
    if name == 'Filter Unprocessed Posts':
        node['parameters']['jsCode'] = r"""// Filter out posts that already have scripts linked in the Script Library
const viralContent = $items("Read Viral Content DB").map(item => item.json);

let scriptLibrary = [];
try {
  scriptLibrary = $items("Read Script Library").map(item => item.json);
} catch(e) {
  console.log('Script library empty or unreadable');
}

if (!viralContent || viralContent.length === 0) {
  return []; 
}

const existingIds = new Set(
  scriptLibrary
    .filter(script => script.Source_Content_ID && script.Source_Content_ID !== "")
    .map(script => script.Source_Content_ID)
);

console.log(`Checking ${viralContent.length} posts against ${existingIds.size} existing scripts...`);
const unprocessed = viralContent.filter(post => !existingIds.has(post.id));
console.log(`Found ${unprocessed.length} completely new posts to process.`);

const results = [];
for (let i = 0; i < unprocessed.length; i++) {
  const post = unprocessed[i];
  // Deep clone the post object so we can add new properties without hitting read-only errors
  const clonedPost = JSON.parse(JSON.stringify(post));
  clonedPost._sourceId = clonedPost.id;
  
  results.push({
    json: clonedPost,
    pairedItem: { item: i }
  });
}

return results;
"""

with open('/home/sandesh-neupane/n8n/workflow.json', 'w') as f:
    json.dump(wf, f, indent=2)

print('✅ Fixed Filter Unprocessed Posts node read-only error.')
