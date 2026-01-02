# Deployment & Setup Guide

## 1. Prerequisites
- Docker & Docker Compose installed on Oracle VPS.
- Supabase Project (`nvxnhphlzsqwlivjkfmg`):
  - URL: `https://nvxnhphlzsqwlivjkfmg.supabase.co`
  - Run the SQL in [schema.sql](file:///c:/Users/Lusa/.gemini/antigravity/playground/electric-meteoroid/schema.sql) in your Supabase SQL Editor.
- Hugging Face API Token.

## 2. Initial Setup
1. Clone this repository to your VPS.
2. Create a `.env` file with the following:
   ```env
   N8N_HOST=your-vps-ip
   HF_TOKEN=your-huggingface-token
   SUPABASE_URL=https://nvxnhphlzsqwlivjkfmg.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   ```
4. Prepare your Google Sheet:
   - Tab named `Videos` with headers: `Video_ID`, `Title`, `Status`.
   - Tab named `Health` with headers: `Timestamp`, `Status`, `Disk`, `RAM`.
   - Tab named `Weekly_Stats` (optional).

## 3. Launching
Run the following command:
```bash
docker-compose up -d --build
```

## 4. n8n Configuration
1. Access n8n at `http://your-vps-ip:5678`.
2. Import `shorts_creator.json` and `error_handler.json`.
3. Activate the workflows.

## 5. Usage
Add YouTube Video IDs to your Google Sheet, and the agent will process them sequentially every 4 hours (configurable in n8n).
