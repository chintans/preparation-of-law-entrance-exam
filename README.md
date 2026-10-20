# Law Entrance Preparation — Chintan Shah

This repo is the long-term memory for a daily coaching session run by Claude at **9:30 AM IST**.
Each session teaches one concept, gives a short test, grades it, and records progress here. Next
day's session reads this repo to decide what to teach.

Target: **3-year LLB** (graduate entry). The plan also covers the 5-year CLAT/AILET papers because they come first, carry no
upper age limit, and train the same skills (reading, reasoning, legal principle application,
current affairs).

## Exams tracked

| Exam | Programme | Exam date | Status | Registration |
|---|---|---|---|---|
| CLAT 2027 (UG) | 5-yr BA LLB, NLUs | **6 Dec 2026**, 2–4 PM | Confirmed | Closes **31 Oct 2026** |
| AILET 2027 (UG) | 5-yr BA LLB, NLU Delhi | **13 Dec 2026**, 2–4 PM | Confirmed | Closes **10 Nov 2026** |
| CUET PG 2027 — LLB paper | 3-yr LLB, DU & others | **Mar 2027** window (LLB paper day TBA) | Tentative | Expected Dec 2026 |
| NLSAT-LLB 2027 | 3-yr LLB (Hons), NLSIU | **25 Apr 2027** | Announced | Form ~Nov 2026, closes ~23 Mar 2027 |
| ~~LSAT India~~ | — | — | **Discontinued by LSAC after May 2024** | — |

Full details and sources: [`exams/`](exams/). The live date tracker is
[`exams/calendar.md`](exams/calendar.md); sessions re-verify it every Monday.

## Layout

| Path | What it holds |
|---|---|
| `CLAUDE.md` | Instructions every session follows (the session protocol) |
| `exams/*.md` | One file per exam: pattern, syllabus, marking, dates, sources |
| `exams/calendar.md` | Date tracker with verification status |
| `syllabus/topic-map.md` | Unified topic list (IDs) mapped to exams and weightage |
| `plan/study-plan.md` | Phases, focus allocation rules, session length rules |
| `progress/state.json` | Machine-readable mastery, streak, review queue, test history |
| `progress/log.md` | One line per session |
| `progress/readiness.md` | Latest readiness report (RAG per exam and section) |
| `sessions/YYYY-MM-DD.md` | Each day's lesson, test, your answers and the grading |
| `research/` | Notes carried forward: current-affairs log, cut-offs, sources |

## How a day works

1. 9:30 AM — the session builds today's lesson and test and notifies you (push + email).
2. You open it, read the 5–10 minute lesson and reply with answers, e.g. `1B 2D 3A 4C 5B`.
3. Claude grades, explains every miss, updates mastery and readiness, and commits here.
4. Some days, unannounced, it's a **surprise test** instead: a timed mixed paper in real exam
   format, followed by a readiness verdict.
