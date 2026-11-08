#!/usr/bin/env python3
"""Export progress data for the progress dashboard artifact.

Usage:  python3 tools/dashboard_data.py --today YYYY-MM-DD [--out dashboard/progress.json]

Reads progress/state.json and syllabus/topic-map.md; writes one JSON file with five tables
(summary, tests, topics, sections, reading). The dashboard's five datasets all read this file.
Readiness figures follow CLAUDE.md section D (last 40 graded questions per section, surprise ×2,
projected = acc − 0.25 × (1 − acc), coverage = topics with weight ≥ 2 and ≥ 5 attempts).
"""
import argparse, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = dt.date(2026, 10, 20)  # Day 1

SECTIONS = {
    'CLAT': {'English': ['ENG-RC', 'ENG-VOC'], 'Current Affairs': ['GK-CA', 'LEG-NEW', 'GK-POL', 'GK-ECO'],
             'Legal': ['LEG-PRIN', 'LEG-TORT', 'LEG-CONT', 'LEG-CRIM', 'LEG-CONST', 'LEG-OTH', 'LEG-MAX'],
             'Logical': ['LR-CR', 'LR-ARG'], 'Quant': ['QT-ARITH', 'QT-DI']},
    'AILET': {'English': ['ENG-RC', 'ENG-VOC', 'ENG-GRM'], 'CA & GK': ['GK-CA', 'GK-STA', 'GK-POL', 'LEG-NEW'],
              'Reasoning': ['LR-CR', 'LR-ARG', 'LR-ANA', 'LEG-PRIN', 'LEG-TORT', 'LEG-CONT', 'LEG-CRIM']},
    'CUET': {'Language': ['ENG-RC', 'ENG-GRM', 'ENG-VOC', 'HIN'], 'GK': ['GK-STA', 'GK-POL', 'GK-ECO', 'GK-CA', 'LEG-NEW'],
             'Computer': ['COMP'], 'Aptitude': ['QT-ARITH', 'QT-GEO', 'QT-DI'], 'Reasoning': ['LR-ANA', 'LR-ARG']},
    'NLSAT': {'English': ['ENG-RC'], 'CA/GK': ['GK-CA', 'LEG-NEW', 'GK-POL'], 'Reasoning': ['LR-CR', 'LR-ARG', 'LEG-PRIN'],
              'Part B': ['WRIT-LEGAL', 'WRIT-ESSAY']},
}
SHARE = {'CLAT': {'English': .20, 'Current Affairs': .25, 'Legal': .25, 'Logical': .20, 'Quant': .10}}


def topic_map():
    tm = {}
    for line in (ROOT / 'syllabus/topic-map.md').read_text().splitlines():
        c = [x.strip() for x in line.split('|')]
        if len(c) > 8 and c[1][:3] in ('ENG', 'HIN', 'GK-', 'LEG', 'LR-', 'QT-', 'COM', 'WRI'):
            tm[c[1]] = {'name': c[2], **dict(zip(['CLAT', 'AILET', 'CUET', 'NLSAT'], c[4:8]))}
    return tm


def rag(p):
    return 'Green' if p >= .65 else 'Amber' if p >= .45 else 'Red'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    ap.add_argument('--out', default=str(ROOT / 'dashboard/progress.json'))
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)
    s = json.loads((ROOT / 'progress/state.json').read_text())
    tm = topic_map()

    tests = sorted(s['tests'], key=lambda t: (t.get('graded_on') or t['date'], t['date']))
    test_rows = []
    for t in sorted(s['tests'], key=lambda t: t['date']):
        mx = t.get('max') or 0
        q = t.get('questions') or 0
        mins = t.get('minutes')
        test_rows.append({
            'date': t['date'], 'day': (dt.date.fromisoformat(t['date']) - START).days + 1,
            'exam': t['exam'], 'topic': t['topic'], 'type': t['type'],
            'net': t['net'], 'max': mx, 'net_pct': round(t['net'] / mx, 4) if mx else None,
            'questions': q, 'minutes': mins,
            'sec_per_q': round(mins * 60 / q) if mins and q else None,
            'on_time': (t.get('graded_on') or t['date']) == t['date'],
        })

    sec_rows = []
    for ex, secs in SECTIONS.items():
        for name, tops in secs.items():
            n = nw = cw = 0.0
            for t in reversed(tests):
                for tp, (cr, at) in t['per_topic'].items():
                    if tp in tops and n < 40 and at:
                        take = min(at, 40 - n); k = cr * take / at
                        m = 2 if t.get('surprise') else 1
                        n += take; nw += take * m; cw += k * m
            acc = cw / nw if nw else None
            proj = acc - 0.25 * (1 - acc) if acc is not None else None
            cov = [tp for tp in tops if tm.get(tp, {}).get(ex, '–') in ('2', '3')]
            ok = [tp for tp in cov if s['topics'][tp]['attempts'] >= 5]
            enough = bool(cov) and len(ok) / len(cov) >= .5
            sec_rows.append({
                'exam': ex, 'section': name, 'graded': round(n), 'accuracy': round(acc, 4) if acc is not None else None,
                'projected': round(proj, 4) if proj is not None else None,
                'coverage': f'{len(ok)}/{len(cov)}', 'coverage_pct': round(len(ok) / len(cov), 4) if cov else 0,
                'status': (rag(proj) if enough else 'Insufficient data') if proj is not None else 'Untested',
                'share': SHARE.get(ex, {}).get(name),
            })

    topic_rows = []
    for tp, v in s['topics'].items():
        topic_rows.append({
            'topic': tp, 'name': tm.get(tp, {}).get('name', tp), 'clat_weight': tm.get(tp, {}).get('CLAT', '–'),
            'mastery': v['mastery'] if v['attempts'] else None, 'attempts': v['attempts'], 'correct': v['correct'],
            'next_review': v.get('next_review'),
            'due': bool(v.get('next_review')) and v['next_review'] <= a.today,
        })

    reading = [{**r, 'over_target_pct': round(r['seconds'] / (r['words'] / r['target_wpm'] * 60) - 1, 4)}
               for r in s['reading']['log']]

    summary = {'as_of': a.today, 'day': (today - START).days + 1, 'streak': s['streak'],
               'sessions_graded': len(s['tests']), 'reading_level': s['reading']['level'],
               'target_wpm': {1: 180, 2: 210, 3: 240, 4: 270, 5: 300}[s['reading']['level']]}
    for ex, e in s['exams'].items():
        summary[f'days_{ex.lower()}'] = (dt.date.fromisoformat(e['date']) - today).days
        summary[f'level_{ex.lower()}'] = s['readiness'][ex]['level'].split(' (')[0]
    clat = [r for r in sec_rows if r['exam'] == 'CLAT']
    summary['clat_indicative'] = round(sum(r['projected'] * r['share'] for r in clat), 4)

    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'summary': [summary], 'tests': test_rows, 'topics': topic_rows,
                               'sections': sec_rows, 'reading': reading}, indent=1, ensure_ascii=False) + '\n')
    print(f'wrote {out}: {len(test_rows)} tests, {len(topic_rows)} topics, {len(sec_rows)} sections, {len(reading)} drills')


if __name__ == '__main__':
    main()
