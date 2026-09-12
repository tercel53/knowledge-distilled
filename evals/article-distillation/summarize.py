#!/usr/bin/env python3
"""Validate and summarize independently judged, paired skill evaluations."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

DIMENSIONS = ('fidelity', 'reasoning', 'language', 'structure', 'visual', 'usability')


def summarize(rows, grouped=True):
    if not isinstance(rows, list) or not rows:
        raise ValueError('expected a nonempty array of judgments')
    seen, wins = set(), Counter()
    values = {v: defaultdict(list) for v in ('baseline', 'candidate')}
    blockers = Counter()
    regressions = []
    for row in rows:
        case = row['case_id']
        run = row['run']
        if not isinstance(case, str) or not case.strip() or type(run) is not int or run < 1:
            raise ValueError('invalid case_id or run')
        scope = row['scope']
        if row['split'] not in ('development', 'holdout'):
            raise ValueError('invalid split')
        key = (case, run, scope)
        if key in seen or scope not in ('plan', 'html'):
            raise ValueError('duplicate judgment or invalid scope')
        seen.add(key)
        mapping = row['mapping']
        if set(mapping) != {'A', 'B'} or set(mapping.values()) != {'baseline', 'candidate'}:
            raise ValueError('mapping must bijectively map A/B to baseline/candidate')
        winner = row['winner']
        if winner not in ('A', 'B', 'tie', 'inconclusive') or not isinstance(row['reason'], str) or not row['reason'].strip():
            raise ValueError('invalid winner or empty reason')
        scores = row['scores']
        if set(scores) != {'A', 'B'}:
            raise ValueError('both score sheets required')
        for label, sheet in scores.items():
            version = mapping[label]
            for field in ('evidence', 'blockers'):
                if not isinstance(sheet[field], list) or any(not isinstance(s, str) or not s.strip() for s in sheet[field]):
                    raise ValueError('evidence and blockers must contain nonempty strings')
            if not sheet['evidence']:
                raise ValueError('scoring evidence is required')
            for dimension in DIMENSIONS:
                value = sheet[dimension]
                if value is not None and (type(value) is not int or not 0 <= value <= 3):
                    raise ValueError('scores must be 0..3 or null')
                if scope == 'plan' and dimension in ('visual', 'usability') and value is not None:
                    raise ValueError('planning cannot receive rendered visual/usability scores')
                if value is None and dimension in DIMENSIONS[:4] and winner != 'inconclusive':
                    raise ValueError('missing core score requires inconclusive verdict')
                if scope == 'html' and value is None and winner != 'inconclusive':
                    raise ValueError('unverified HTML dimension requires inconclusive verdict')
            blockers[version] += len(sheet['blockers'])
        wins[mapping.get(winner, winner)] += 1
        if winner == 'inconclusive':
            continue
        by_version = {mapping[k]: v for k, v in scores.items()}
        for dimension in DIMENSIONS:
            old, new = (by_version[v][dimension] for v in ('baseline', 'candidate'))
            if (old is None) != (new is None):
                raise ValueError('paired dimensions must have equal coverage')
            if old is None:
                continue
            values['baseline'][dimension].append(old)
            values['candidate'][dimension].append(new)
            if new < old:
                regressions.append({'case_id': case, 'run': run, 'scope': scope, 'split': row['split'], 'dimension': dimension, 'baseline': old, 'candidate': new})
    result = {
        'pairs': len(rows), 'verdicts': dict(wins), 'blockers': dict(blockers),
        'dimensions': {d: {v: {'mean': round(sum(values[v][d]) / len(values[v][d]), 3) if values[v][d] else None, 'n': len(values[v][d])} for v in values} for d in DIMENSIONS},
        'regressions': regressions,
        'note': 'Descriptive only; inconclusive pairs excluded from means. No automatic claim of overall improvement.'
    }
    if grouped:
        result['groups'] = {
            f'{scope}/{split}': summarize([r for r in rows if r['scope'] == scope and r['split'] == split], grouped=False)
            for scope, split in sorted({(r['scope'], r['split']) for r in rows})
        }
        result['cases'] = {
            case: {'pairs': sum(r['case_id'] == case for r in rows), 'runs': sorted({r['run'] for r in rows if r['case_id'] == case})}
            for case in sorted({r['case_id'] for r in rows})
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('judgments', type=Path)
    args = parser.parse_args()
    try:
        result = summarize(json.loads(args.judgments.read_text(encoding='utf-8')))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f'Invalid evaluation: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
