# SESSION.md — Project Ascension
## Date: 2026-03-31 (Day 44 of 60)
## Engineer: James Sloan | Denver, CO

---

## PLATFORM STATUS

All systems operational. Alexandra running on Claude Sonnet 4 (conversation) + Haiku 4.5 (tools/vision).

- Control Plane: Server 3 (192.168.1.10) — FastAPI :8000, nginx HTTPS :443, PostgreSQL + pgvector
- Tailscale: Server 3: 100.115.56.89, JesAir: 100.86.193.45, iPhone: 100.117.217.120, Mac mini + Cortez: connected
- Dashboard: https://192.168.1.10/dashboard (LAN) | https://100.115.56.89/dashboard (anywhere)
- PWA installed on Cortez and JesAir

---

## SERVICES (all active, Restart=always)

| Service | Function |
|---|---|
| orchestrator | Alexandra brain — Sonnet 4 conversation, Haiku vision/tools |
| alexandra-telegram | Telegram bot — text + voice in/out |
| recruiter-watcher | Gmail poll every 15min, Telegram alert on real recruiter email |
| daily_brief cron | 7am UTC morning briefing |

---

## ALEXANDRA CAPABILITIES (Day 44)

VOICE:
- Whisper tiny model (73MB, ~1.4s transcription, beam_size=1) — 3x faster than base
- ElevenLabs TTS Jane voice
- Full voice loop: dashboard mic button + Telegram voice notes
- All text chat responses also speak aloud automatically
- Click-to-start overlay on dashboard load

VISION:
- Auto-greet on load: webcam capture, Claude vision, ElevenLabs speak
- Camera button for on-demand capture
- Home layout context + device hint (Windows=Cortez=downstairs)
- Denver timezone aware for greetings

AWARENESS:
- get_live_context: time (Denver tz), weather (OpenWeatherMap), markets (stooq), headlines (NYT RSS)
- get_emails + get_calendar: direct Gmail and Google Calendar
- Daily brief at 7am
- Dynamic day counter from project_start_date (2026-02-18)

PROACTIVE:
- recruiter-watcher: 3-gate filter, fires Telegram within 15min of real recruiter email

PERSONA:
- Sonnet 4 — warm, direct, no bullets/asterisks/markdown
- Never narrates career history unprompted
- Random time-of-day vision greetings

---

## SECURITY (all clean as of 2026-03-31)

- All 7 GitHub repos scanned and clean
- git history rewritten — no raw credentials in any commit
- All secrets use os.getenv() or dotenv
- .gitignore covers .env, *.key, *.pem, google_credentials.json, google_token.json, notified_emails.json
- GitHub PAT stored in memory only — never committed to repo
- SECURITY RULE: never commit hardcoded credentials — always verify with grep before pushing

---

## KEY FILES

- Orchestrator: /home/jes/control-plane/orchestrator/app.py
- Dashboard: /home/jes/control-plane/orchestrator/ai_operator/dashboard/dashboard.py
- Tool registry: /home/jes/control-plane/orchestrator/ai_operator/tools/registry.py
- Voice: /home/jes/control-plane/voice.py — tiny model at /home/jes/models/faster-whisper-tiny
- Telegram: /home/jes/control-plane/telegram_bot.py
- Recruiter watcher: /home/jes/control-plane/recruiter_watcher.py
- Applications: /Users/jes/ai-operator/job-search/applications.csv — 57 entries
- Keys in .env on Server 3: ANTHROPIC_API_KEY, ELEVENLABS_API_KEY, OPENWEATHER_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, POSTGRES_PASSWORD

---

## JOB SEARCH

- 57 total applications (12/20/2025 through 3/28/2026)
- Week of 3/28: Lirio, Wolters Kluwer, Cohere — unemployment req met
- Go West IT: rejected 3/29/2026
- Next applications: Friday 4/4 (3 minimum)
- Per Scholas IBM AI Solutions Developer course started 3/31/2026
- Blacklist: jobleads.com

---

## TODO (priority order)

1. Job applications — Friday 4/4 (3 minimum)
2. Interview prep — Lirio and Cohere pending
3. Proactive calendar alerts — meeting in 30min triggers Telegram alert
4. Wake word / always-on listening
5. Twilio toll-free verification (SMS)

---

## NEXT SESSION PROMPT

"Paco — Day 45. 3 job applications. Then proactive calendar alerts — Alexandra warns me 30 minutes before any meeting via Telegram."

---

*Built by James Sloan · Denver, CO · 2026*
