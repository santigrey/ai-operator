# SESSION.md — Project Ascension
## Date: 2026-03-30 (Day 41 of 60)
## Engineer: James Sloan | Denver, CO

---

## PLATFORM STATUS

All systems operational. Alexandra running on Claude Haiku 4.5.

- Control Plane: Server 3 (192.168.1.10) — FastAPI :8000, PostgreSQL + pgvector, nginx HTTPS :443
- Inference Plane: TheBeast (192.168.1.152) — Ollama, Tesla T4 GPU
- Operator Layer: JesAir, Mac mini, Cortez
- Tailscale: all nodes connected — Server 3: 100.115.56.89, JesAir: 100.86.193.45, iPhone: 100.117.217.120, Mac mini: connected, Cortez: connected
- Dashboard: https://192.168.1.10/dashboard (LAN) or https://100.115.56.89/dashboard (anywhere)
- PWA installed as desktop app on Cortez

---

## WHAT ALEXANDRA CAN DO (Day 41)

- Auto-greets on dashboard load: captures webcam, describes scene, speaks via ElevenLabs (Jane voice)
- Click-to-start overlay unlocks Chrome autoplay restriction
- Voice interface: mic button, Whisper STT, ElevenLabs TTS (Jane voice)
- Webcam vision: 📷 button or auto on load, Claude vision API, Alexandra persona
- Home layout context injected into every vision call — knows kitchen/dining room vs office
- Device hint (Windows = Cortez = downstairs) passed to vision endpoint
- Reads real Gmail and Calendar via get_emails and get_calendar tools
- Daily brief at 7am via cron
- Cross-session semantic memory via pgvector
- Telegram bot: @alexandra_ascension_bot — text commands, /status, /brief, /tasks
- Multi-turn chat with session isolation, context trim at 20 messages
- New persona: warm, direct, conversational, no bullets or headers, 2-4 sentence responses
- Day counter dynamic — calculated from project_start_date (2026-02-18) in user_profile
- Hamburger menu — Daily Brief, Recent Runs, Agent Tasks in slide-in panel
- "Project Ascension" subtitle removed from top bar

---

## KEY FILES

- Orchestrator: /home/jes/control-plane/orchestrator/app.py (Server 3) — main app
- Dashboard: /home/jes/control-plane/orchestrator/ai_operator/dashboard/dashboard.py (Server 3)
- Voice: /home/jes/control-plane/voice.py (Server 3) — Jane voice ID: RILOU7YmBhvwJGDGjNmP
- Telegram bot: /home/jes/control-plane/telegram_bot.py (Server 3)
- CC poller: /Users/jes/bin/cc_poller.py (Mac mini)
- Applications log: /Users/jes/ai-operator/job-search/applications.csv (Mac mini) — 57 entries

---

## JOB SEARCH STATUS

- 57 total applications (12/20/2025 through 3/28/2026)
- Week of 3/28: Lirio, Wolters Kluwer, Cohere — unemployment requirement met
- Go West IT: rejected 3/29/2026
- Next applications: Friday 4/4
- Blacklist: jobleads.com
- Target: mid-level AI/ML Platform Engineer, $120-160k, fully remote

---

## TODO (priority order)

1. Telegram voice messages — send voice notes, get voice replies
2. Voice latency reduction — Whisper tiny model
3. Proactive notifications — recruiter email triggers Telegram alert
4. Job applications — Friday 4/4 (3 minimum)
5. Interview prep — Lirio and Cohere responses pending
6. Twilio toll-free verification (SMS)

---

## NEXT SESSION PROMPT

"Paco — Day 42. Build Telegram voice: send voice notes to Alexandra, get voice replies back."

---

*Built by James Sloan · Denver, CO · 2026*
