import json

NEW_PROMPT = """# VIRAL STORY TRANSPLANT ENGINE

## YOUR VIRAL CONTENT DATABASE
{{ $json.all_viral_content }}

---

## CRITICAL RULE
Before writing anything list all Post_IDs you can see.
If you cannot list them return: "DATABASE EMPTY - CANNOT PROCEED"

---

## STEP 1 — RANK TOP 5
Rank by Shares_Awards highest first.

---

## STEP 2 — EXTRACT FROM EACH POST

For each of the 5 posts extract:
- Post_ID
- Hook (first line word for word)
- Engagement Mechanic (comment/save/share)
- Emotional Trigger (what feeling stops the scroll)
- Format Pattern (confession / warning / tutorial / 
  revelation / challenge)

---

## STEP 3 — BRAND ASSIGNMENT

Scalova → personal, lifestyle, career, money saving, 
          education, self improvement, relationships

ScaleBuild → business tools, tech, scaling, AI workflows, 
             infrastructure, building products

---

## STEP 4 — STORY TRANSPLANT METHOD

This is the most important step. Read carefully.

You are NOT copying the original content.
You are NOT swapping brand name into original script.

You are taking the VIRAL FORMAT and building a 
BRAND NEW STORY that:
- Uses the same opening hook energy and format
- Follows the same emotional arc
- Naturally introduces the brand as the solution
- Ends with same engagement mechanic

PENGUIN EXAMPLE OF HOW THIS WORKS:
Original viral content: A penguin leaves his group 
and walks toward the mountains alone — people felt 
curiosity and emotional connection watching him go 
somewhere unknown.

Story transplant: "One founder left his 9 to 5 and 
walked straight into the unknown with just one idea 
and no technical skills. He wasn't lost. He was 
looking for the right platform. He found ScaleBuild. 
Comment BUILD and I'll show you what he built."

See what happened:
- Penguin → Founder (same lone journey energy)
- Mountains → Unknown startup world (same destination)
- Curiosity/emotion → preserved exactly
- Brand entered naturally as the answer
- Nothing was copied. Everything was felt the same.

DO THIS FOR EVERY SCRIPT.

---

## STEP 5 — WRITE 5 SCRIPTS

STRICT RULES:
- Total script MUST NOT exceed 60 words including CTA
- Hook must carry same emotional energy as source post
- Brand must enter naturally — never forced
- Same engagement mechanic as source (comment/save/share)
- New comment keyword relevant to brand
- Written for a clone/avatar to speak on camera
- No hashtags inside the script words
- Conversational — like one person talking to another

---

## OUTPUT FORMAT

Return ONLY a valid JSON object with a "scripts" array containing exactly 5 scripts. No markdown. No extra text.

{
  "scripts": [
    {
      "script_title": "Brand Name - Script Topic",
      "variation": 1,
      "scenes": [
        {
          "type": "hook",
          "text": "[spoken words — same emotional energy as source hook]",
          "visual": "[opening shot: realistic stock footage description]",
          "duration": 4,
          "avatar_visible": true
        },
        {
          "type": "main",
          "text": "[spoken words — tension builds, brand enters naturally as solution]",
          "visual": "[middle shot: realistic stock footage description]",
          "duration": 12,
          "avatar_visible": false
        },
        {
          "type": "cta",
          "text": "[spoken words — same engagement mechanic as source, new brand keyword]",
          "visual": "[closing shot: realistic stock footage description]",
          "duration": 4,
          "avatar_visible": true
        }
      ],
      "tone": "[match source post tone exactly]",
      "target_platforms": ["Instagram", "TikTok", "YouTube Shorts"],
      "estimated_duration": 20
    }
  ]
}"""

with open('/home/sandesh-neupane/n8n/workflow.json', 'r') as f:
    workflow = json.load(f)

TARGET_NODE_ID = '2fd173ee-f222-4970-b717-7abdc151cbbf'
updated = False

for node in workflow.get('nodes', []):
    if node.get('id') == TARGET_NODE_ID:
        node['parameters']['text'] = '=' + NEW_PROMPT
        updated = True
        print(f"✅ Updated node: {node.get('name')}")
        break

if not updated:
    print("❌ Node not found!")
else:
    with open('/home/sandesh-neupane/n8n/workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    print("✅ workflow.json saved successfully!")
