# SESSION.md — Project Ascension
## Date: 2026-03-30 (Day 43 of 60)
## Engineer: James Sloan | Denver, CO

---

## PLATFORM STATUS

All systems operational.

- Control Plane: Server 3 (192.168.1.10) — FastAPI :8000, nginx HTTPS :443, PostgreSQL + pgvector
- Tailscale: Server 3: 100.115.56.89, JesAir: 100.86.193.45, iPhone: 100.117.217.120, Mac mini + Cortez: connected
- Dashboard: https://192.168.1.10/dashboard (LAN) | https://100.115.56.89/dashboard (anywhere)
- PWA installed on Cortez

---

## SERVICES (all active, Restart=always)

| Service | Function |
|---|---|
| orchestrator | Alexandra brain, chat, voice, vision — Sonnet 4 conversation |
| alexandra-telegram | Telegram bot — text + voice in/out |
| recruiter-watcher | Gmail poll every 15min, Telegram alert on real recruiter email |
| daily_brief cron | 7am UTC morning briefing |

---

## ALEXANDRA CAPABILITIES (Day 43)

VOICE:
- Dashboard: mic button, Whisper STT, ElevenLabs TTS (Jane voice)
- Telegram: send voice note → transcribe → think → reply with voice message
- Click-to-start overlay unlocks Chrome autoplay on dashboard load
- Auto-greet: webcam capture + describe James + speak on load

AWARENESS:
- get_live_context: real-time time, weather (OpenWeatherMap), markets (stooq), headlines (NYT RSS)
- get_emails + get_calendar: direct Gmail and Google Calendar
- Daily brief at 7am
- Home layout context in vision — kitchen/dining room vs office
- Device-aware (Windows = Cortez = downstairs)

PROACTIVE:
- recruiter-watcher: real 3-gate filter — domain blacklist + no-reply filter + keyword match
- Fires Telegram notification within 15min of real recruiter email
- TELEGRAM_CHAT_ID: 8751426822

PERSONA:
- Sonnet 4 brain — warm, direct, no bullets/asterisks/markdown
- Dynamic day counter from project_start_date (2026-02-18)
- Random time-of-day vision greetings — no repetition
- Never narrates career history unprompted

---

## KEY FILES

- Orchestrator: /home/jes/control-plane/orchestrator/app.py
- Dashboard: /home/jes/control-plane/orchestrator/ai_operator/dashboard/dashboard.py
- Tool registry: /home/jes/control-plane/orchestrator/ai_operator/tools/registry.py
- Voice: /home/jes/control-plane/voice.py — Jane voice ID: RILOU7YmBhvwJGDGjNmP
- Telegram bot: /home/jes/control-plane/telegram_bot.py
- Recruiter watcher: /home/jes/control-plane/recruiter_watcher.py
- Applications: /Users/jes/ai-operator/job-search/applications.csv — 57 entries
- Keys in .env: ANTHROPIC_API_KEY, ELEVENLABS_API_KEY, OPENWEATHER_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

---

## JOB SEARCH

- 57 total applications (12/20/2025 through 3/28/2026)
- Week of 3/28: Lirio, Wolters Kluwer, Cohere — unemployment req met
- Go West IT: rejected 3/29/2026
- Next applications: Friday 4/4 (3 minimum)
- Blacklist: jobleads.com

---

## TODO (priority order)

1. Voice latency reduction — Whisper tiny model
2. Find NewsAPI key on TheBeast for better headlines
3. Job applications — Friday 4/4 (3 minimum)
4. Interview prep — Lirio and Cohere pending
5. Twilio toll-free verification (SMS)
6. Wake word / always-on listening

---

## NEXT SESSION PROMPT

"Paco — Day 44. Reduce voice latency — swap Whisper base for tiny model. Then job applications."

---

*Built by James Sloan · Denver, CO · 2026*
