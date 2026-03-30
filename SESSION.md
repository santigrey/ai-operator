# SESSION.md â Project Ascension
## Date: 2026-03-30 (Day 41 of 60)
## Engineer: James Sloan | Denver, CO

---

## PLATFORM STATUS

All systems operational. Alexandra running on Claude Haiku 4.5.

- Control Plane: Server 3 (192.168.1.10) â FastAPI :8000, PostgreSQL + pgvector, MCP server :8001, nginx HTTPS :443
- Inference Plane: TheBeast (192.168.1.152) â Ollama, Tesla T4 GPU
- Operator Layer: JesAir, Mac mini, Cortez

### Tailscale Network
- Server 3: 100.115.56.89
- JesAir: 100.86.193.45
- iPhone: 100.117.217.120
- Mac mini + Cortez: pending sign-in
- Dashboard accessible from anywhere: https://100.115.56.89/dashboard

---

## WHAT ALEXANDRA CAN DO

- Wakes up daily at 7am, reads real Gmail + Google Calendar, generates daily brief
- Executes approved tasks autonomously via CC polling loop
- Learns from approve/reject decisions (feedback loop â user_profile)
- Cross-session semantic memory via pgvector
- Real-time web research via web_fetch + DuckDuckGo
- Multi-turn chat with session isolation
- Voice interface: mic â Whisper STT â Claude â ElevenLabs TTS â audio playback
- Accessible from anywhere via Tailscale (https://100.115.56.89/dashboard)
- Telegram bot: @alexandra_ascension_bot
- Email + SMS notifications (Twilio toll-free verification pending)
- Direct Gmail (get_emails) and Calendar (get_calendar) tools in agent registry

---

## KEY FILES

- Orchestrator: /home/jes/control-plane/orchestrator/ (Server 3)
- MCP server: /home/jes/control-plane/mcp_server.py (Server 3)
- Daily brief: /home/jes/control-plane/daily_brief.py (Server 3)
- Voice: /home/jes/control-plane/voice.py (Server 3)
- Telegram bot: /home/jes/control-plane/telegram_bot.py (Server 3)
- Google credentials: /home/jes/control-plane/google_credentials.json (Server 3)
- CC poller: /Users/jes/bin/cc_poller.py (Mac mini) â launchd com.ascension.cc-poller
- Applications log: /Users/jes/ai-operator/job-search/applications.csv (Mac mini)
- SESSION.md: github.com/santigrey/ai-operator

---

## JOB SEARCH STATUS

- 57 total applications logged (12/20/2025 through 3/28/2026)
- Week of 3/28: Lirio â, Wolters Kluwer â, Cohere â (3 minimum met)
- Go West IT: rejected 3/29/2026
- Resume v2: JamesSloan_AIEngineer_Resume_v2.pdf (iCloud Drive)
- Blacklist: jobleads.com
- Target: mid-level AI/ML Platform Engineer, $120-160k, fully remote

---

## TODO (priority order)

1. Image recognition â webcam â Claude vision API
2. Telegram voice messages â send voice notes, get voice replies
3. Voice latency reduction â Whisper tiny model
4. 3 more job applications this week (week of 3/29)
5. Interview prep â Lirio and Cohere responses pending
6. Mac mini + Cortez Tailscale sign-in
7. Twilio toll-free verification (SMS)

---

## NEXT SESSION PROMPT

"Paco â Day 41. Image recognition: add webcam capture to the dashboard so Alexandra can see me. Then 3 job applications."

---


### Day 41
- Image recognition live: 📷 camera button on dashboard
- Alexandra sees user via webcam → Claude vision API → responds in character as Alexandra
- Correctly described James: appearance, workspace, burgundy curtains, shelving, homelab space
- Anthropic API key rotated — new key live in .env on Server 3
- /vision/analyze endpoint uses Alexandra persona system prompt
- Tailscale complete: Server 3, JesAir, Mac mini, iPhone, Cortez all connected
- Dashboard accessible from anywhere: https://100.115.56.89/dashboard

### TODO (priority order)
1. Telegram voice messages — send voice notes, get voice replies
2. Voice latency reduction — Whisper tiny model
3. 3 more job applications this week (week of 3/30)
4. Interview prep — Lirio and Cohere responses pending
5. Twilio toll-free verification (SMS)

### NEXT SESSION PROMPT
"Paco — Day 42. Build Telegram voice: send voice notes to Alexandra, get voice replies. Then 3 job applications."
*Built by James Sloan Â· Denver, CO Â· 2026*
