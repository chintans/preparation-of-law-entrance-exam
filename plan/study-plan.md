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
