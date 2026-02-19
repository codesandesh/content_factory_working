import json

# The new aggregation code that converts the array to a single formatted text block
NEW_AGGREGATION_CODE = """// Filter Stage 2 - Aggregate ALL posts into a single formatted text block
const allItems = $input.all();
const viralPosts = [];

for (const item of allItems) {
  const fields = item.json.fields || {};
  const status = fields.Status || item.json.Status || item.json.status || fields.status || '';
  
  if (status.toString().trim() === "Generate Script") {
    viralPosts.push({
      Post_ID: item.json.id || fields.Post_ID || item.json.Post_ID || item.id || '',
      Content: fields.Content || item.json.Content || item.json.content || '',
      Shares_Awards: fields.Shares_Awards || item.json.Shares_Awards || fields.Engagement_Rate || item.json.engagement_rate || 0,
      Viral_Score: fields.Viral_Score || item.json.Viral_Score || 0,
      Narrative_Hook: fields.Narrative_Hook || item.json.Narrative_Hook || item.json.narrative_hook || '',
      Visual_Theme: fields.Visual_Theme || item.json.Visual_Theme || item.json.visual_theme || '',
      Core_Story: fields.Core_Story || item.json.Core_Story || item.json.core_story || '',
      Platform: fields.Platform || item.json.Platform || item.json.platform || '',
      Status: status
    });
  }
}

// Convert array to a single formatted text block (like Make's Text Aggregator)
const textBlock = viralPosts.map((post, index) => {
  return `===
POST ${index + 1}:
Post_ID: ${post.Post_ID}
Content: ${post.Content}
Shares_Awards: ${post.Shares_Awards}
Viral_Score: ${post.Viral_Score}
Narrative_Hook: ${post.Narrative_Hook}
Visual_Theme: ${post.Visual_Theme}
Core_Story: ${post.Core_Story}
Platform: ${post.Platform}`;
}).join('\\n\\n');

// Return a single item with the formatted text block
return [{ json: { all_viral_content: textBlock, post_count: viralPosts.length } }];"""

TARGET_NODE_ID = '6e952e2a-741f-4d21-8b4c-6cac129c76a8'

with open('/home/sandesh-neupane/n8n/workflow.json', 'r') as f:
    workflow = json.load(f)

updated = False
for node in workflow.get('nodes', []):
    if node.get('id') == TARGET_NODE_ID:
        node['parameters']['jsCode'] = NEW_AGGREGATION_CODE
        updated = True
        print(f"✅ Updated node: {node.get('name')}")
        break

if not updated:
    print("❌ Node not found!")
else:
    with open('/home/sandesh-neupane/n8n/workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    print("✅ workflow.json saved successfully!")
