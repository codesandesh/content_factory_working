# Complete n8n Workflow: Reddit → Viral Content → Multi-Platform Scripts
**Status**: ✅ Production Ready | Last Updated: Now

---

## Overview

This is a comprehensive two-stage pipeline that:
1. **Stage 1**: Scrapes Reddit for AI/ML/tech news → analyzes with Gemini → stores viral content
2. **Stage 2**: Takes viral content → generates thought leadership scripts for 3 platforms → stores in Script Library

**Execution**: 
- Stage 1 runs every 12 hours (automatic) + manual trigger
- Stage 2 runs every 6 hours (automatic) + manual trigger

---

## Stage 1: Content Discovery (11 nodes)

### Flow
reddit-urls → apify-scraper → filter-posts → remove-empty → gemini-analyze → parse-results → filter-relevant → airtable-store

### Nodes

| # | Node | Purpose | Config |
|---|------|---------|--------|
| 1 | Manual Trigger | User-initiated Stage 1 | Click to run |
| 2 | Schedule Trigger | Auto run every 12h | cron: 0 */12 * * * |
| 3 | Generate Reddit URLs | Build 44 URLs (22 subreddits × 2 feeds) | JavaScript: hot + top/day feeds |
| 4 | Fetch Reddit via Apify | Call Reddit scraper API | POST to apify, maxItems=100 |
| 5 | Parse Reddit Posts | **Filter dataType='post' only** (skip comments), min 50 upvotes | JavaScript, skip comments |
| 6 | Remove Empty Items | Validation filter | JavaScript |
| 7 | Gemini Analyze News Post | Score viral potential (0-100) | Analyzes title, upvotes, comments |
| 8 | Gemini Model | Google Gemini API config | LLM: chat-bison-001 |
| 9 | Parse Gemini Results | Extract JSON from LLM response | JavaScript JSON parsing |
| 10 | Filter Relevant News Only | Keep only: (is_ai_ml_tech OR news_relevance≥50) AND viral_score≥30 | JavaScript filtering |
| 11 | Store in Viral Content DB | Write 22 fields to Airtable | Airtable: creates rows |

### Output (Viral Content DB)
**22 fields**:
- Name, Post_ID, Platform, Post_URL, Content
- Engagement_Score, Likes, Comments, Shares_Awards
- Viral_Score, Hook_Pattern, Content_Structure
- Emotional_Triggers, Viral_Elements, Script_Framework
- Status, Created_Date, Script_Library
- Engagement_Rate, Followers, Saves, Shares, Impressions, Clicks, Views

---

## Stage 2: Script Generation (13 nodes + 3 parallel prompts)

### Flow
viral-db → filter-unprocessed → **[linkedin | twitter | facebook]** → gemini → parse-scripts → remove-empty → airtable-store

### Nodes

| # | Node | Purpose | Platform |
|---|------|---------|----------|
| 1 | Manual Trigger (Stage 2) | User-initiated Stage 2 | N/A |
| 2 | Schedule Trigger (6h) | Auto run every 6 hours | N/A |
| 3 | Read Viral Content DB | Fetch all records from Viral DB | N/A |
| 4 | Filter Unprocessed Posts | Get max 10 Status='Analyzed' posts with no Script Library records | N/A |
| **5a** | **Gemini Generate Social Scripts** | **Generate LinkedIn thought leadership script** | **LinkedIn** |
| **5b** | **Gemini Generate Script - Twitter/X** | **Generate Twitter/X thought leadership script** | **Twitter/X** |
| **5c** | **Gemini Generate Script - Facebook** | **Generate Facebook thought leadership script** | **Facebook** |
| 6 | Gemini Model (Stage 2) | Google Gemini API config (shared by all 3 platforms) | N/A |
| 7 | Parse Gemini Scripts | Consolidate 3 platform outputs into individual records | N/A |
| 8 | Remove Empty Scripts | Validation filter | N/A |
| 9 | Store in Script Library | Write all scripts to Airtable Script Library | N/A |

### Prompt Details (All 3 Platforms)

**Author**: Ujjwal Roy
- CEO of ScaleBuild AI & Seethos AI
- Chairs IEEE Young Professionals
- Founding President, World AI Alliance
- Former Intel/Micron/IBM engineer, Wall Street finance background
- Age 32

**Exact Prompt** (identical for all 3 platforms, only platform name changes):

**Tone & Voice**:
- Direct, no fluff, hands-on CEO perspective
- Conversational, punchy, like a real human (not AI-generated)
- Opinionated but grounded
- Natural sentence rhythms, occasional imperfect phrasing

**Structure (STRICT)**:
- Max 2 paragraphs (2-4 sentences each)
- 50-100 words hard ceiling
- Strong hook opening (sharp observation, not question)
- Close with perspective/prediction/question

**Formatting**:
- ❌ NO em-dashes, NO ellipses, NO hashtags, NO lists
- ✅ Raw thought leadership only

**Forbidden Phrases** (20+ AI-generated patterns to avoid)
- "Let's dive in", "Here's the thing", "In today's landscape"
- Generic buzzwords: revolutionary, game-changing, paradigm shift
- Third person, filler, corporate formality

**Output Format** (per platform):
```json
{
  "Script_Title": "[Platform] - [Topic]",
  "Hook": "Sharp opening statement",
  "Main_Content": "2 paragraphs, 50-100 words",
  "CTA": "Perspective or question",
  "Target_Platforms": "[Platform]",
  "Tone": "Direct, [platform-specific adjectives]",
  "Hashtags": ""
}
```

**Platform Variations**:
- **LinkedIn**: Professional, strategic, insider perspective
- **Twitter/X**: Contrarian angle, punchy, direct
- **Facebook**: Accessible, hands-on founder perspective

### Output (Script Library)
**13 fields per script**:
- Name, Source_Content_ID, Script_Title
- Hook, Main_Content, CTA
- Visual_Cues, Tone, Hashtags
- Estimated_Duration, Target_Platforms
- Status, Created_Date

**Rate Limiting**: Max 10 posts per Stage 2 run to avoid API limits

---

## Subreddit Sources (22 total)

**Core AI & ML**: AINews, artificial, MachineLearning, LocalLLaMA, OpenAI, ChatGPT, deeplearning, StableDiffusion, mlops, LanguageTechnology

**Tech News**: technology, technews, tech, hardware, programming, compsci

**Broader**: Futurology, startups, datascience, singularity

**Feeds per subreddit**: hot + top/day (44 URLs total)

---

## Data Flow Summary

```
Reddit Posts (100 max)
    ↓
[Filter: dataType='post', upvotes≥50]
    ↓
[Gemini: Analyze viral/relevance]
    ↓
[Filter: viral_score≥30 AND (is_ai_ml_tech OR news_relevance≥50)]
    ↓
Viral Content DB (scored posts)
    ↓
[Get unprocessed: max 10 posts]
    ↓
[Gemini (3 parallel): Generate scripts for LinkedIn/Twitter/Facebook]
    ↓
Script Library (3 scripts per content item)
```

---

## Environment Variables Required

```bash
APIFY_API_TOKEN=<your-apify-token>
AIRTABLE_BASE_ID=<your-base-id>
AT_TABLE_VIRAL_DB=<table-name>
AT_TABLE_SCRIPT_LIBRARY=<table-name>
```

---

## Configuration Files

- **workflow.json**: Complete two-stage pipeline (production-ready)
- **Airtable**: 2 tables (Viral Content DB + Script Library) with proper schema
- **n8n**: Credentials for Google Gemini API + Airtable API

---

## Execution Instructions

### Manual Trigger
1. In n8n UI, open this workflow
2. Click "Manual Trigger" button for Stage 1 (scrape Reddit)
3. Wait ~2-3 minutes for Stage 1 to complete
4. Click "Manual Trigger (Stage 2)" for script generation
5. Wait ~1-2 minutes for Stage 2 to complete
6. Check Airtable tables for results

### Automatic Triggers
- Stage 1: Every 12 hours (4 AM, 4 PM)
- Stage 2: Every 6 hours (12 AM, 6 AM, 12 PM, 6 PM)

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "Unknown field name" | Airtable schema mismatch | Verify 22 fields in Viral Content DB match mapping |
| No posts found | Comments included in filter | Verify `dataType !== 'post'` in node 5 |
| Gemini timeout | API rate limit | Reduce maxItems from 100 or increase timeout |
| "No scripts generated" | Gemini JSON parsing failed | Check Gemini response format matches expected schema |
| Low script quality | Ujjwal voice guidelines not followed | Review prompt for buzzwords, em-dashes, AI-generated phrases |

---

## Next Steps

1. ✅ Deploy workflow to n8n instance
2. ✅ Test Stage 1 (1-2 runs)
3. ✅ Verify Viral Content DB population
4. ✅ Test Stage 2 (script generation)
5. ✅ Verify Script Library quality
6. ✅ Set schedules to auto-run

---

**Created**: Auto-generated from workflow.json
**Last Modified**: Now
**Version**: 2.0 (3-platform parallel execution)
