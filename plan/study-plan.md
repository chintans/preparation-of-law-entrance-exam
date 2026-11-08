# Study plan

## Phases

| Phase | Dates | Primary target | Emphasis |
|---|---|---|---|
| 1. Sprint | 21 Oct – 13 Dec 2026 | CLAT (6 Dec), AILET (13 Dec) | Legal principle application, critical reasoning, long RC, current affairs of the past year, CLAT quant/DI; AILET grammar and analytical puzzles in the last two weeks |
| 2. CUET build | 14 Dec 2026 – CUET paper day (Mar 2027) | CUET PG LLB | Computer basics, arithmetic, analytical reasoning, static GK, grammar; weekly NLSAT writing keeps going |
| 3. NLSAT finish | CUET paper day – 25 Apr 2027 | NLSAT-LLB | Part B legal answers and essays (3×/week), 500-word RC, current affairs refresh, Part A full mocks |

Skills carry across: work done in Phase 1 on reading, reasoning and legal application is most
of NLSAT Part A.

## Daily focus allocation

Each session, compute a focus weight for every exam still ahead:

```
weight(exam) = priority(exam) / max(days_to_exam, 7)
priority: CLAT 1.0, AILET 1.0, CUET 1.2, NLSAT 1.5   (3-year LLB targets weighted up)
```

Normalise the weights to shares. Pick today's exam with probability equal to its share
(use a random draw), then pick the topic within it:

1. If any topic in `review_queue` is due today or overdue → review it (spaced repetition).
2. Else the topic with the highest `exam_weight × (100 − mastery)` among that exam's topics.
3. Never the same topic three sessions running unless it is a review.

## Session length

Every session also opens with the 5-minute Current-Affairs Brief (below), on top of these lengths.

| Days to the nearest exam | Length | Format |
|---|---|---|
| > 60 | 15 min | ~8 min lesson, 5-question test |
| 22–60 | 20 min | ~8 min lesson, 8-question test (passage-based where the exam is) |
| 8–21 | 25 min | short lesson, 10-question test in exam format, timed |
| 2–7 | 30 min | revision of weakest areas + mixed mini-mock |
| 1 (day before) | 15 min | light revision, strategy and exam-day checklist, no new topics |
| Exam day | none | morning good-luck note with the 3 key reminders |

## Writing practice (NLSAT Part B)

- From 1 Dec 2026: one writing task every Sunday (legal problem or essay, alternating).
- From the day after the CUET paper: three per week (Mon/Wed/Fri), graded on a rubric.

## Surprise tests

- Base chance per session: 10%. Rises to 20% within 30 days of an exam and 30% within 10 days.
- Never two in a row; at least one in every 10 sessions (force one if 9 have passed without).
- Not on the day before an exam.
- Format: timed, mixed sections in the target exam's real pattern and marking, 15–20 questions
  (20–25 min). Ends with a full readiness report.

## Current-affairs brief (added 1 Nov 2026 at Chintan's request — CA was 0/5 on the Day-7 surprise test)

Every session except exam day opens with a **Current-Affairs Brief** of **6 items** (~5 min read, untimed).

- **Item format (2–3 lines each):** what happened, with the date → why it matters → the **static hook**
  examiners attach to it (constitutional article, statute and section, body and HQ, who heads it, the number/rank) →
  one-line "likely question".
- **Mix per brief:** 2 legal/judicial (LEG-NEW) · 1 polity/constitutional (GK-POL) · 1 national/economy/schemes
  (GK-CA/GK-ECO) · 1 international/summits/reports & indices (GK-CA) · 1 appointments/awards/sports/science (GK-CA).
- **Two streams:** 3 items from the **backfill** month at `ca.backfill_cursor` in `state.json`, 3 items from the
  **last 14 days**. Backfill runs month by month through the exam window; advance the cursor once that month has
  had ~6–8 items across briefs (about every 2–3 sessions).
  - Phase 1 (to 13 Dec 2026): window **Nov 2025 → Nov 2026** (CLAT/AILET). Cursor must reach the current month by ~30 Nov.
  - Phase 2/3: window **Apr 2026 → Mar 2027** (CUET/NLSAT); add 1 static-GK item (GK-STA) per brief for CUET.
- **Accuracy:** every item verified by web search (prefer PIB, official sites, SC/HC judgments, reputable dailies); cite
  in the session file; log in `research/current-affairs.md` as `(brief)`; never repeat an item already briefed unless
  it has a new development.
- **Recall questions:** every normal session's test adds **2 standalone CA recall questions** from briefs ≥ 3 days old
  (prefer items never tested; on Sundays, **5**), tagged GK-CA / LEG-NEW / GK-POL / GK-ECO. Mark logged items `(tested)`.
  Today's brief is never tested the same day.
- **Day before an exam:** the brief becomes a top-15 "most likely to be asked" recap. **Exam day:** none.

## Daily Constitution Capsule (added 8 Nov 2026 at Chintan's request — GK-POL 0/7; "I am weak at Constitution")

Every session except exam day carries a **Constitution Capsule** in the learning section, **in addition to** the day's
main lesson (whatever exam or topic the draw picks). Units and their must-know core: `syllabus/constitution-track.md`;
next unit = `constitution.cursor` in `state.json`.

- **Where:** right after the main lesson (normal sessions). On surprise-test days it comes after the CA brief and before
  the clock starts. Day before an exam: a "top-10 Articles and numbers" recap of units done. Exam day: none.
- **Length:** ~4 minutes. **Format** (no tables — tables were read, not learned, on Day 15):
  1. **5 numbered flash facts** from the unit — each one line: *Article → what it does → the number/case examiners ask*.
  2. **Say-it drill:** the 5 Article numbers listed alone; he covers the facts and says what each does before checking.
  3. **One landmark case** in two lines (name, year, bench size if famous, holding).
  4. **The trap** examiners set on this unit (the twin Article, the wrong number, the absolute word).
- **Tests:** every test (normal and surprise) adds **2 Constitution questions** on top of the usual count and the CA recall
  items: **1 on today's capsule** and **1 spaced-recall item from an earlier capsule** (prefer `weak_units`; on the first
  capsule day, use unit 1 facts already missed). Standalone, 4 options, tagged GK-POL or LEG-CONST (per the unit's tag in the
  track file). On surprise tests both are drawn from earlier capsules only. Mark them *(Constitution)* in the test.
- **Advancing:** move `constitution.cursor` on by one unit each session. If the previous session was **missed**, repeat its
  unit once (set `repeat_pending`), then move on. When grading, add a unit to `constitution.weak_units` if its capsule
  question was wrong; remove it after two later correct answers on that unit.
- **Main lesson overlap:** if the draw picks GK-POL or LEG-CONST as the day's topic, the main lesson goes deeper (worked
  examples, passage-based items) on a unit already taught or the current one; the capsule still runs as normal.
- **Session length:** the capsule adds ~4 min reading and ~2 min of questions to the times in "Session length".

## Reading speed (added 1 Nov 2026 — Day-7 pace was ~2 min/question against CLAT's 1)

**Goal for CLAT/AILET:** read a ~450-word passage in about 1:40 (≈ 270 wpm) and answer its questions at ~40 s each,
so a passage set takes ≈ 5 minutes (120 questions in 120 minutes).

- **The ⏱ passage.** In every normal session one passage (the English/RC passage if there is one, otherwise the
  longest) is marked ⏱ with its **word count** and **target reading time** for his current level. He times the read
  only (start reading → finish reading, before the questions) and replies with `R m:ss`. All other passages show their
  word count too.
- **Levels** (`reading.level` in `state.json`; start at 1):

  | Level | Target wpm | 450-word passage |
  |---|---|---|
  | 1 | 180 | 2:30 |
  | 2 | 210 | 2:10 |
  | 3 | 240 | 1:50 |
  | 4 | 270 | 1:40 (CLAT pace) |
  | 5 | 300 | 1:30 (buffer) |

  **Up a level** after two drills in a row at or under target with ≥ 75% accuracy on that passage's questions.
  **Hold** if accuracy on the passage is < 60% (speed never at the cost of comprehension) — say so plainly.
  **Down a level** after three drills in a row more than 25% over target.
- **Technique ladder** — one technique per week, named in the ⏱ header so he practises it deliberately; earlier ones stay on:
  1. *Stems first* — read only the question stems (not options) in ~15 s, then the passage.
  2. *Paragraph map* — after each paragraph, a 3–5-word label in the margin; answer from the map, return only to locate.
  3. *No regression* — never re-read mid-passage; move a pen under the line at a steady pace.
  4. *Chunking* — take in 3–4-word phrases, not single words; stop sounding out each word.
  5. *60-second rule* — any question not cracked in 60 s gets a mark and a skip; come back at the end.
- **Whole-test pace.** Every test states its time budget (60 s/question for CLAT/AILET legal and reasoning). He sends
  start and end times; grading reports seconds per question against the budget.
- **Weekly check (Sunday):** report the wpm trend from `reading.log` and the level in the readiness refresh.

