# API Reference - Content Factory

This guide covers the key API configurations used in the workflow.

## Google Veo 3
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/veo-3:generateVideo`
- **Method:** `POST`
- **Headers:** 
  - `Authorization: Bearer {{GOOGLE_API_KEY}}`
  - `x-goog-user-project: {{GOOGLE_PROJECT_ID}}`

## OpenAI GPT-4o
- **Endpoint:** `https://api.openai.com/v1/chat/completions`
- **Model:** `gpt-4o`

## ElevenLabs
- **Endpoint:** `https://api.elevenlabs.io/v1/text-to-speech/{{VOICE_ID}}`
- **Config:** Uses `eleven_multilingual_v2`

## Airtable
- **Endpoint:** `https://api.airtable.com/v0/{{BASE_ID}}`
- **Required Tables:**
  1. `Inspiration_Sources`
  2. `Viral_Content_Database`
  3. `Script_Library`
  4. `Video_Production_Queue`
