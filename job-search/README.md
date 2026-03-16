# Job Search — Project Ascension

Centralized tracking system for Sloan's AI engineering job search campaign.

## Structure

**applications.csv** — Master tracker for all roles. Columns: date, company, role, status, salary_min, salary_max, url, notes.

**outreach-drafts/** — Draft messages for recruiters, hiring managers, and networking contacts. Name files by company and role (e.g., `true-anomaly-staff-outreach.md`).

**research/** — Company research notes, interview prep, and competitive intel. One file per company (e.g., `true-anomaly.md`).

## Pipeline Status Workflow

```
identified → researched → drafted → applied → screening → interview → offer → accepted/declined
```

| Status | Meaning |
|--------|---------|
| `identified` | Role found, not yet researched |
| `researched` | Company intel gathered, fit assessed |
| `drafted` | Outreach message written |
| `applied` | Outreach sent or application submitted |
| `screening` | Recruiter or hiring manager contact made |
| `interview` | Active interview process |
| `offer` | Offer received |
| `accepted` | Offer accepted — closed won |
| `declined` | Offer declined or role withdrawn — closed |

## Workflow

1. Alexandra or manual search identifies roles → add to `applications.csv` with status `identified`
2. Research the company → save to `research/<company>.md` → update status to `researched`
3. Draft outreach → save to `outreach-drafts/<company>-<role>.md` → update status to `drafted`
4. Send outreach or submit application → update status to `applied`
5. Track progress through screening, interview, offer, accepted/declined
