# SESSION.md — Project Ascension
## Date: 2026-03-30 (Day 41 of 60)
## Engineer: James Sloan | Denver, CO

---

## PLATFORM STATUS

All systems operational. Alexandra running on Claude Sonnet 4 (conversation) + Haiku 4.5 (tools/vision).

- Control Plane: Server 3 (192.168.1.10) — FastAPI :8000, PostgreSQL + pgvector, nginx HTTPS :443
- Tailscale: Server 3: 100.115.56.89, JesAir: 100.86.193.45, iPhone: 100.117.217.120, Mac mini + Cortez: connected
- Dashboard: https://192.168.1.10/dashboard (LAN) | https://100.115.56.89/dashboard (anywhere)
- PWA installed as desktop app on Cortez

---

## ALEXANDRA CAPABILITIES (Day 41 — end of day)

CORE:
- Sonnet 4 brain for conversation, Haiku for tools/vision/execution
- Dynamic day counter from project_start_date (2026-02-18)
- Warm, direct persona — no bullets, no asterisks, no markdown, 2-4 sentence responses
- Never narrates career history unprompted
- Cross-session semantic memory via pgvector

AWARENESS:
- get_live_context tool: real-time time, weather (OpenWeatherMap), markets (S&P/NASDAQ/BTC via stooq), headlines (NYT RSS)
- get_emails + get_calendar: direct Gmail and Google Calendar access
- Daily brief at 7am via cron
- Home layout context in every vision call (kitchen/dining room vs office)

INTERFACE:
- Click-to-start overlay (fixes Chrome autoplay)
- Auto-greet on load: webcam capture, describe James, speak via ElevenLabs (Jane voice)
- Random time-of-day aware vision greeting prompts — no repetition
- Voice interface: Whisper STT + ElevenLabs TTS
- Hamburger menu: Daily Brief, Today Activity (last 24h only), Agent Tasks
- Telegram bot: @alexandra_ascension_bot
- Accessible from anywhere via Tailscale

---

## KEY FILES

- Orchestrator: /home/jes/control-plane/orchestrator/app.py (Server 3)
- Dashboard: /home/jes/control-plane/orchestrator/ai_operator/dashboard/dashboard.py
- Tool registry: /home/jes/control-plane/orchestrator/ai_operator/tools/registry.py
- Voice: /home/jes/control-plane/voice.py — Jane voice ID: RILOU7YmBhvwJGDGjNmP
- Telegram: /home/jes/control-plane/telegram_bot.py
- CC poller: /Users/jes/bin/cc_poller.py (Mac mini)
- Applications: /Users/jes/ai-operator/job-search/applications.csv — 57 entries
- Weather API key: OPENWEATHER_API_KEY in /home/jes/control-plane/.env

---

## JOB SEARCH

- 57 total applications (12/20/2025 through 3/28/2026)
- Week of 3/28: Lirio, Wolters Kluwer, Cohere — unemployment req met
- Go West IT: rejected 3/29/2026
- Next applications: Friday 4/4 (3 minimum)
- Blacklist: jobleads.com

---

## TODO (priority order)

1. Proactive notifications — recruiter email triggers Telegram alert immediately
2. Telegram voice messages — send voice notes, get voice replies
3. Voice latency reduction — Whisper tiny model
4. Find NewsAPI key (stock trader app on TheBeast) for better headlines
5. Job applications — Friday 4/4
6. Interview prep — Lirio and Cohere pending
7. Twilio toll-free verification (SMS)

---

## NEXT SESSION PROMPT

"Paco — Day 42. Build proactive notifications: when a recruiter emails James, Alexandra alerts him on Telegram immediately. Then Telegram voice messages."

---

*Built by James Sloan · Denver, CO · 2026*
