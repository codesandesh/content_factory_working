import json

def generate():
    workflow = {
        "name": "NC Campaign - Smart Crawl + Nepali Post Generator (Airtable)",
        "nodes": [
            {
                "parameters": {},
                "id": "node-001",
                "name": "Manual Trigger",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [100, 400]
            },
            {
                "parameters": {
                    "rule": {
                        "interval": [
                            {
                                "field": "hours",
                                "hoursInterval": 6
                            }
                        ]
                    }
                },
                "id": "node-002",
                "name": "Schedule (Every 6hrs)",
                "type": "n8n-nodes-base.scheduleTrigger",
                "typeVersion": 1,
                "position": [100, 560]
            },
            {
                "parameters": {
                    "operation": "search",
                    "base": {
                        "__rl": True,
                        "mode": "id",
                        "value": "={{ $env.CONGRESS_AIRTABLE_BASE_ID }}"
                    },
                    "table": {
                        "__rl": True,
                        "mode": "name",
                        "value": "={{ $env.CONGRESS_AT_TABLE_SOURCES }}"
                    },
                    "filterByFormula": "{Status}='Pending'",
                    "options": {}
                },
                "id": "node-003",
                "name": "Read Sources Table",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 2,
                "position": [360, 400],
                "credentials": {
                    "airtableTokenApi": {
                        "id": "Uas1HNt2b74zrNBP",
                        "name": "Airtable Personal Access Token account"
                    }
                }
            },
            {
                "parameters": {
                    "batchSize": 3,
                    "options": {}
                },
                "id": "node-004",
                "name": "Process 3 at a Time",
                "type": "n8n-nodes-base.splitInBatches",
                "typeVersion": 1,
                "position": [600, 400]
            },
            {
                "parameters": {
                    "conditions": {
                        "boolean": [],
                        "dateTime": [],
                        "number": [],
                        "string": [
                            {
                                "value1": "={{ $json.fields['Type'] }}",
                                "value2": "URL"
                            }
                        ]
                    }
                },
                "id": "node-005",
                "name": "URL or Keyword?",
                "type": "n8n-nodes-base.if",
                "typeVersion": 1,
                "position": [840, 400]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://api.firecrawl.dev/v1/scrape",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            { "name": "Authorization", "value": "=Bearer {{ $env.FIRECRAWL_API_KEY }}" },
                            { "name": "Content-Type", "value": "application/json" }
                        ]
                    },
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "{\n  \"url\": \"{{ $json.fields.Source }}\",\n  \"formats\": [\"markdown\"],\n  \"onlyMainContent\": true,\n  \"excludeTags\": [\"nav\", \"footer\", \"ads\", \"script\", \"style\"],\n  \"waitFor\": 2000\n}"
                },
                "id": "node-006",
                "name": "Scrape Direct URL",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [1080, 260]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://api.tavily.com/search",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            { "name": "Content-Type", "value": "application/json" }
                        ]
                    },
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "{\n  \"api_key\": \"{{ $env.TAVILY_API_KEY }}\",\n  \"query\": \"{{ $json.fields.Source }} Nepali Congress Nepal sarkaar kaam\",\n  \"search_depth\": \"advanced\",\n  \"max_results\": 5,\n  \"include_domains\": [\"kathmandupost.com\", \"setopati.com\", \"thehimalayantimes.com\", \"onlinekhabar.com\", \"ratopati.com\", \"nepal.gov.np\", \"mof.gov.np\"]\n}"
                },
                "id": "node-007",
                "name": "Keyword Web Search",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [1080, 540]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://api.firecrawl.dev/v1/scrape",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            { "name": "Authorization", "value": "=Bearer {{ $env.FIRECRAWL_API_KEY }}" },
                            { "name": "Content-Type", "value": "application/json" }
                        ]
                    },
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "{\n  \"url\": \"{{ $json.results[0].url }}\",\n  \"formats\": [\"markdown\"],\n  \"onlyMainContent\": true,\n  \"excludeTags\": [\"nav\", \"footer\", \"ads\", \"script\", \"style\"],\n  \"waitFor\": 2000\n}"
                },
                "id": "node-008",
                "name": "Scrape Top Result URL",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [1320, 540]
            },
            {
                "parameters": {
                    "jsCode": "const item = $input.item.json;\nconst batchItem = $('Process 3 at a Time').item.json;\nconst fields = batchItem.fields || batchItem;\n\nlet markdown = '';\nlet sourceUrl = '';\n\nif (item.data && item.data.markdown) {\n  markdown = item.data.markdown;\n  sourceUrl = item.data.metadata?.sourceURL || item.data.metadata?.url || 'Unknown URL';\n} else if (item.markdown) {\n  markdown = item.markdown;\n  sourceUrl = item.metadata?.sourceURL || 'Unknown URL';\n}\n\nmarkdown = (markdown || '').replace(/\\n{3,}/g, '\\n\\n').replace(/#{4,}/g, '###').trim().substring(0, 8000);\n\nreturn [{\n  json: {\n    source_type: 'scraped',\n    original_type: fields['Type'] || 'Unknown',\n    original_source: fields['Source'] || 'Unknown',\n    category: fields['Category'] || 'General',\n    airtable_record_id: batchItem.id || batchItem.recordID || (batchItem.fields ? batchItem.id : ''),\n    source_url: sourceUrl,\n    raw_content: markdown,\n    char_count: markdown.length\n  }\n}];"
                },
                "id": "node-009",
                "name": "Normalize Scraped Content",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [1560, 400]
            },
            {
                "parameters": {
                    "conditions": {
                        "boolean": [],
                        "dateTime": [],
                        "number": [
                            {
                                "value1": "={{ $json.char_count }}",
                                "value2": 200,
                                "operation": "largerEqual"
                            }
                        ],
                        "string": []
                    }
                },
                "id": "node-010",
                "name": "Enough Content?",
                "type": "n8n-nodes-base.if",
                "typeVersion": 1,
                "position": [1800, 400]
            },
            {
                "parameters": {
                    "promptType": "define",
                    "text": "=You are a STRICT content filter for a political campaign focused ONLY on POSITIVE achievements.\n\nCategory: {{ $json.category }}\nSource URL: {{ $json.source_url }}\n\nScraped Content:\n{{ $json.raw_content }}\n\n---\nYour task: EXTRACT only POSITIVE, CONSTRUCTIVE content from this article.\n\n✅ INCLUDE only:\n- Roads, bridges, highways built or inaugurated\n- Schools, hospitals, health posts constructed\n- Electricity projects, hydropower, solar completed\n- Water supply, irrigation projects delivered\n- Digital/IT initiatives launched\n- Social welfare programs (scholarships, pensions, insurance)\n- Foreign investment brought in\n- Trade agreements signed\n- Disaster relief distributed\n- Poverty reduction statistics\n- Women/youth empowerment programs\n- Agricultural support programs\n- Any COMPLETED government work with measurable impact\n\n❌ STRICTLY EXCLUDE (output NOTHING about):\n- Corruption, scams, embezzlement\n- Arrests, charges, court cases\n- Party conflicts, fights, splits\n- Protests, strikes, bandhs\n- Criticism of any party or leader\n- Promises not yet fulfilled\n- Any negative news\n- Deaths, accidents, disasters\n- Allegations or accusations of any kind\n\nIf the content contains NO positive/development work at all, respond with exactly: NO_POSITIVE_CONTENT\n\nOtherwise, list 4-6 specific POSITIVE facts with:\n- What was done\n- Where (district/province)\n- When (year BS or AD)\n- Who benefited (how many people / which communities)\n- Any numbers/statistics\n\nFormat as numbered list. Be specific and factual only."
                },
                "id": "node-011",
                "name": "Gemini - Filter Positive Only",
                "type": "@n8n/n8n-nodes-langchain.chainLlm",
                "typeVersion": 1.7,
                "position": [2040, 300]
            },
            {
                "parameters": {
                    "options": {}
                },
                "id": "node-gemini-model",
                "name": "Gemini Model",
                "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
                "typeVersion": 1,
                "position": [2040, 460],
                "credentials": {
                    "googlePalmApi": {
                        "id": "vbhLIH8I52VXHFtc",
                        "name": "Google Gemini(PaLM) Api account"
                    }
                }
            },
            {
                "parameters": {
                    "conditions": {
                        "boolean": [],
                        "dateTime": [],
                        "number": [],
                        "string": [
                            {
                                "value1": "={{ $json.text }}",
                                "value2": "NO_POSITIVE_CONTENT",
                                "operation": "contains"
                            }
                        ]
                    }
                },
                "id": "node-012",
                "name": "No Positive Content?",
                "type": "n8n-nodes-base.if",
                "typeVersion": 1,
                "position": [2280, 300]
            },
            {
                "parameters": {
                    "promptType": "define",
                    "text": "=तपाईं नेपाली भाषामा सामाजिक सञ्जालका लागि सकारात्मक र प्रेरणादायी पोस्ट लेख्ने विशेषज्ञ हुनुहुन्छ।\n\nश्रेणी: {{ $('Normalize Scraped Content').item.json.category }}\n स्रोत: {{ $('Normalize Scraped Content').item.json.source_url }}\n\nसकारात्मक तथ्यहरू:\n{{ $('Gemini - Filter Positive Only').item.json.text }}\n\n---\nमाथिका तथ्यहरूको आधारमा नेपालीमा १० फरक-फरक सामाजिक सञ्जाल पोस्ट बनाउनुहोस्।\n\n✅ आवश्यक नियमहरू:\n- सम्पूर्ण पोस्ट नेपाली भाषामा (देवनागरी लिपि)\n- प्रत्येक पोस्ट २०-३५० शब्द\n- वास्तविक तथ्य, तारिख, नाम र संख्या उल्लेख गर्नुहोस्\n- सकारात्मक, उत्साहवर्धक र गर्वान्वित स्वरमा लेख्नुहोस्\n- जनताले गर्व गर्न सकून् यस्तो भावना राख्नुहोस्\n\n❌ यी कुरा लेख्नु हुँदैन:\n- भ्रष्टाचार, घोटाला वा नकारात्मक कुरा\n- कुनै पनि दल वा नेताको आलोचना\n- अपूर्ण वाचाहरू\n- कुनै पनि नकारात्मक शब्द\n\n📝 पोस्टका प्रकारहरू (प्रत्येक २ वटा):\n१. 🏗️ विकास कथा - के बन्यो, कहाँ बन्यो, कसलाई फाइदा भयो\n२. 📊 तथ्याङ्क - संख्या र उपलब्धि देखाउने\n३. 👥 मानवीय कथा - आम जनताको जीवन कसरी सुधारियो\n४. 🌟 गर्व पल - \"हाम्रो देश अगाडि बढ्दैछ\" भावना\n५. 📢 जागरण - \"यो कुरा सबैले जान्नुपर्छ\" प्रकारको\n\n📌 अन्त्यमा थप्नुहोस्:\n- सम्बन्धित इमोजी\n- ह्यासट्यागहरू: #नेपालको_विकास #नेपालीकाँग्रेस #परिवर्तन_देखिँदैछ #हाम्रो_उपलब्धि #जनताको_सरकार\n- \"यो पोस्ट सेयर गर्नुहोस् 🇳🇵\" भनेर सकाउनुहोस्\n\nढाँचा:\n---पोस्ट १---\n[Content]\n...पोस्ट १० सम्म"
                },
                "id": "node-013",
                "name": "Gemini - Write 10 Nepali Posts",
                "type": "@n8n/n8n-nodes-langchain.chainLlm",
                "typeVersion": 1.7,
                "position": [2520, 200]
            },
            {
                "parameters": {
                    "jsCode": "const rawOutput = $input.item.json.text;\nconst normalizedData = $('Normalize Scraped Content').item.json;\nconst facts = $('Gemini - Filter Positive Only').item.json.text;\n\n// Matches '---पोस्ट [Digit]---' with support for Devanagari digits\nconst postRegex = /---\s*पोस्ट\s*[\\d१२३४५६७८९०]+\s*---([\\s\\S]*?)(?=---\s*पोस्ट\s*[\\d१२३४५६७८९०]+\s*---|$)/g;\nconst posts = [];\nlet match;\nlet postNumber = 0;\n\nwhile ((match = postRegex.exec(rawOutput)) !== null) {\n  const postText = match[1].trim();\n  if (postText.length > 20) {\n    postNumber++;\n    const wordCount = postText.split(/\\s+/).length;\n    let platform = 'Facebook';\n    if (wordCount < 80) platform = 'X (Twitter)';\n    else if (wordCount < 150) platform = 'Instagram';\n\n    posts.push({\n      'Post Number': postNumber,\n      'Category': normalizedData.category,\n      'Nepali Post': postText,\n      'Platform': platform,\n      'Word Count': wordCount,\n      'Source URL': normalizedData.source_url,\n      'Original Source': normalizedData.original_source,\n      'Airtable Record ID': normalizedData.airtable_record_id,\n      'Facts Used': facts.substring(0, 400) + '...',\n      'Generated Date': new Date().toISOString().split('T')[0],\n      'Review Status': 'Pending Review',\n      'Approved': false\n    });\n  }\n}\n\nif (posts.length === 0) {\n  return [{ json: { error: 'No posts parsed', rawOutput: rawOutput.substring(0, 500) } }];\n}\n\nreturn posts.map(p => ({ json: p }));"
                },
                "id": "node-014",
                "name": "Parse Posts",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [2760, 200]
            },
            {
                "parameters": {
                    "operation": "create",
                    "base": {
                        "__rl": True,
                        "mode": "id",
                        "value": "={{ $env.CONGRESS_AIRTABLE_BASE_ID }}"
                    },
                    "table": {
                        "__rl": True,
                        "mode": "name",
                        "value": "={{ $env.CONGRESS_AT_TABLE_GENERATED_POSTS }}"
                    },
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "Post Number": "={{ $json['Post Number'] }}",
                            "Category": "={{ $json['Category'] }}",
                            "Nepali Post": "={{ $json['Nepali Post'] }}",
                            "Platform": "={{ $json['Platform'] }}",
                            "Word Count": "={{ $json['Word Count'] }}",
                            "Source URL": "={{ $json['Source URL'] }}",
                            "Original Source": "={{ $json['Original Source'] }}",
                            "Facts Used": "={{ $json['Facts Used'] }}",
                            "Generated Date": "={{ $json['Generated Date'] }}",
                            "Review Status": "={{ $json['Review Status'] }}",
                            "Approved": "={{ $json['Approved'] }}"
                        }
                    },
                    "options": {
                        "typecast": True
                    }
                },
                "id": "node-015",
                "name": "Save Posts to Airtable",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 2.1,
                "position": [3000, 200],
                "credentials": {
                    "airtableTokenApi": {
                        "id": "Uas1HNt2b74zrNBP",
                        "name": "Airtable Personal Access Token account"
                    }
                }
            },
            {
                "parameters": {
                    "operation": "update",
                    "base": {
                        "__rl": True,
                        "mode": "id",
                        "value": "={{ $env.CONGRESS_AIRTABLE_BASE_ID }}"
                    },
                    "table": {
                        "__rl": True,
                        "mode": "name",
                        "value": "={{ $env.CONGRESS_AT_TABLE_SOURCES }}"
                    },
                    "id": "={{ $('Normalize Scraped Content').item.json.airtable_record_id }}",
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "Status": "Done",
                            "Last Run": "={{ $now.format('yyyy-MM-dd HH:mm') }}"
                        }
                    }
                },
                "id": "node-016",
                "name": "Mark Source as Done",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 2.1,
                "position": [3240, 200],
                "credentials": {
                    "airtableTokenApi": {
                        "id": "Uas1HNt2b74zrNBP",
                        "name": "Airtable Personal Access Token account"
                    }
                }
            },
            {
                "parameters": {
                    "jsCode": "const item = $('Process 3 at a Time').item.json;\nconst fields = item.fields || item;\nreturn [{ json: { skipped: true, source: fields['Source'] || 'Unknown', reason: 'No positive content found', timestamp: new Date().toISOString() } }];"
                },
                "id": "node-017",
                "name": "Log: No Positive Content",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [2520, 420]
            },
            {
                "parameters": {
                    "operation": "update",
                    "base": {
                        "__rl": True,
                        "mode": "id",
                        "value": "={{ $env.CONGRESS_AIRTABLE_BASE_ID }}"
                    },
                    "table": {
                        "__rl": True,
                        "mode": "name",
                        "value": "={{ $env.CONGRESS_AT_TABLE_SOURCES }}"
                    },
                    "id": "={{ $('Normalize Scraped Content').item.json.airtable_record_id }}",
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "Status": "Skipped - No positive content",
                            "Last Run": "={{ $now.format('yyyy-MM-dd HH:mm') }}"
                        }
                    }
                },
                "id": "node-018",
                "name": "Mark Skipped in Airtable",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 2.1,
                "position": [2760, 420],
                "credentials": {
                    "airtableTokenApi": {
                        "id": "Uas1HNt2b74zrNBP",
                        "name": "Airtable Personal Access Token account"
                    }
                }
            },
            {
                "parameters": {
                    "jsCode": "const item = $('Process 3 at a Time').item.json;\nconst fields = item.fields || item;\nreturn [{ json: { skipped: true, source: fields['Source'] || 'Unknown', reason: 'Content too short', timestamp: new Date().toISOString() } }];"
                },
                "id": "node-019",
                "name": "Log: Content Too Short",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [2040, 520]
            },
            {
                "parameters": {
                    "operation": "update",
                    "base": {
                        "__rl": True,
                        "mode": "id",
                        "value": "={{ $env.CONGRESS_AIRTABLE_BASE_ID }}"
                    },
                    "table": {
                        "__rl": True,
                        "mode": "name",
                        "value": "={{ $env.CONGRESS_AT_TABLE_SOURCES }}"
                    },
                    "id": "={{ $('Normalize Scraped Content').item.json.airtable_record_id }}",
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "Status": "Skipped - Content too short",
                            "Last Run": "={{ $now.format('yyyy-MM-dd HH:mm') }}"
                        }
                    }
                },
                "id": "node-020",
                "name": "Mark Too Short in Airtable",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 2.1,
                "position": [2280, 520],
                "credentials": {
                    "airtableTokenApi": {
                        "id": "Uas1HNt2b74zrNBP",
                        "name": "Airtable Personal Access Token account"
                    }
                }
            }
        ],
        "connections": {
            "Manual Trigger": { "main": [[{ "node": "Read Sources Table", "type": "main", "index": 0 }]] },
            "Schedule (Every 6hrs)": { "main": [[{ "node": "Read Sources Table", "type": "main", "index": 0 }]] },
            "Read Sources Table": { "main": [[{ "node": "Process 3 at a Time", "type": "main", "index": 0 }]] },
            "Process 3 at a Time": { "main": [[{ "node": "URL or Keyword?", "type": "main", "index": 0 }]] },
            "URL or Keyword?": { "main": [[{ "node": "Scrape Direct URL", "type": "main", "index": 0 }], [{ "node": "Keyword Web Search", "type": "main", "index": 0 }]] },
            "Scrape Direct URL": { "main": [[{ "node": "Normalize Scraped Content", "type": "main", "index": 0 }]] },
            "Keyword Web Search": { "main": [[{ "node": "Scrape Top Result URL", "type": "main", "index": 0 }]] },
            "Scrape Top Result URL": { "main": [[{ "node": "Normalize Scraped Content", "type": "main", "index": 0 }]] },
            "Normalize Scraped Content": { "main": [[{ "node": "Enough Content?", "type": "main", "index": 0 }]] },
            "Enough Content?": { "main": [[{ "node": "Gemini - Filter Positive Only", "type": "main", "index": 0 }], [{ "node": "Log: Content Too Short", "type": "main", "index": 0 }]] },
            "Gemini Model": { "ai_languageModel": [[{ "node": "Gemini - Filter Positive Only", "type": "ai_languageModel", "index": 0 }, { "node": "Gemini - Write 10 Nepali Posts", "type": "ai_languageModel", "index": 0 }]] },
            "Gemini - Filter Positive Only": { "main": [[{ "node": "No Positive Content?", "type": "main", "index": 0 }]] },
            "No Positive Content?": { "main": [[{ "node": "Log: No Positive Content", "type": "main", "index": 0 }], [{ "node": "Gemini - Write 10 Nepali Posts", "type": "main", "index": 0 }]] },
            "Gemini - Write 10 Nepali Posts": { "main": [[{ "node": "Parse Posts", "type": "main", "index": 0 }]] },
            "Parse Posts": { "main": [[{ "node": "Save Posts to Airtable", "type": "main", "index": 0 }]] },
            "Save Posts to Airtable": { "main": [[{ "node": "Mark Source as Done", "type": "main", "index": 0 }]] },
            "Mark Source as Done": { "main": [[{ "node": "Process 3 at a Time", "type": "main", "index": 0 }]] },
            "Log: No Positive Content": { "main": [[{ "node": "Mark Skipped in Airtable", "type": "main", "index": 0 }]] },
            "Mark Skipped in Airtable": { "main": [[{ "node": "Process 3 at a Time", "type": "main", "index": 0 }]] },
            "Log: Content Too Short": { "main": [[{ "node": "Mark Too Short in Airtable", "type": "main", "index": 0 }]] },
            "Mark Too Short in Airtable": { "main": [[{ "node": "Process 3 at a Time", "type": "main", "index": 0 }]] }
        },
        "settings": {
            "executionOrder": "v1"
        },
        "id": "lb2vdmT1LIdOlBIP"
    }
    
    with open('nepali_congress.json', 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    print("Workflow generated successfully!")

if __name__ == "__main__":
    generate()
