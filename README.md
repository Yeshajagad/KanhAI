# KanhAI
Krishna AI Agent is a multi-agent AI system designed to provide compassionate, culturally grounded mental health support based on the teachings of the Bhagavad Gita. It combines ancient wisdom with modern AI architecture to deliver personalized guidance, emotional understanding, and actionable clarity to users.

---

## Features

* Multi-Agent Pipeline

  * Analyzer – Detects topic and emotion
  * Verse Finder (MCP Tool) – Retrieves relevant Gita verses
  * Krishna AI – Generates wise, compassionate responses
  * Action Suggester – Provides next-step recommendations
* MCP tools for verse retrieval and memory
* Session memory using SQLite
* Modern UI/UX with dark mode
* Real-time chat with smooth loading states
* Observability with logs and metrics

---

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Runs at: [http://localhost:8000](http://localhost:8000)

### Frontend

Already deployed (React build).
For local development:

```bash
cd frontend
npm install
npm run dev
```

Runs at: [http://localhost:8000](http://localhost:5173)

---

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Configuration
│   ├── database.py             # SQLite storage
│   ├── agents/                 # All 4 agents
│   │   ├── analyzer.py
│   │   ├── verse_finder.py
│   │   ├── krishna_ai.py
│   │   └── action_suggester.py
│   ├── tools/                  # MCP tools
│   │   ├── gita_mcp_tool.py
│   │   └── memory_tool.py
│   └── utils/                  # Utilities
│       ├── logger.py           # Observability
│       └── session_manager.py  # State management
└── frontend/
    └── src/
        └── App.jsx             # React UI
```

---
### Sequential Agent Flow

1. **User sends message** → Backend receives request
2. **Agent 1 (Analyzer)** → Detects topic (fear/duty/confusion) & emotion
3. **Agent 2 (Verse Finder)** → Uses MCP to find relevant Gita verse
4. **Agent 3 (Krishna AI)** → Generates wise response with verse
5. **Agent 4 (Action Suggester)** → Creates follow-up suggestions
6. **Memory Tool** → Saves interaction to database
7. **Response sent** → User receives Krishna's guidance

___
## How It Works

1. User sends a message
2. Analyzer agent detects topic, context, and emotion
3. Verse Finder uses MCP to retrieve a relevant Bhagavad Gita verse
4. Krishna AI generates a calm, wise response using the verse
5. Action Suggester recommends practical next steps
6. Memory tool saves the interaction in SQLite
7. Frontend displays the full message, verse card, and suggestions

Example:
User: “I’m confused about my career.”

* Analyzer detects confusion
* Verse Finder retrieves BG 2.47
* Krishna AI responds with guidance
* Suggester provides actionable steps

---

## API Endpoints

```
POST   /chat            – Send a message
GET    /session/{id}    – Get session info
GET    /history/{id}    – Get chat history
DELETE /session/{id}    – Clear session
GET    /metrics         – System metrics
```

---

## UI Preview

KanhAI in DarkMode 
<img width="1710" height="946" alt="Screenshot 2025-11-28 at 10 56 59 PM" src="https://github.com/user-attachments/assets/8662f518-bced-4e6f-b1bd-deb93c952dcc" />

<img width="3420" height="1892" alt="image" src="https://github.com/user-attachments/assets/fe85d56e-c13a-4367-9c54-c7d4ec5cc4b4" />

KanhAI in LightMode 
<img width="1710" height="946" alt="Screenshot 2025-11-28 at 10 56 49 PM" src="https://github.com/user-attachments/assets/c86f9eec-818c-4c38-9f98-598438f19a4a" />

<img width="1710" height="946" alt="Screenshot 2025-11-28 at 10 57 45 PM" src="https://github.com/user-attachments/assets/cb48d200-fc86-4781-980a-7fb88204a232" />


---

## Tech Stack

Backend: FastAPI, SQLite, Pydantic, Uvicorn
Frontend: React, Tailwind CSS, Lucide Icons
AI System: Multi-agent architecture with MCP tools

---

## Observability

* Logs all agent activity
* Tracks sessions, messages, and MCP usage

---

## Security

* SQLite storage
* No sensitive data logged
* Environment variables stored in `.env`

---

## Deployment

### Backend (Railway or Render)

```
pip install -r requirements.txt
python main.py
```

### Frontend (Vercel or Netlify)

```
vercel deploy
```

or

```
netlify deploy
```

---
Made with ❤️ for Krishna Lovers...
