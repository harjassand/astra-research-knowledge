#!/usr/bin/env python3
"""Portable decision/lemma retrieval for either the full or static repository."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    p = ROOT / path
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def resolve(identifier, records=None):
    records = records if records is not None else rows('frontier/CURRENT_CLAIM_STATUS.jsonl')
    key = Path(identifier).stem
    exact = [r for r in records if key == r['card_id'] or identifier == r['card_path']]
    if not exact:
        exact = [r for r in records if r['card_id'].split('-', 1)[0] == key]
    if len(exact) != 1:
        raise ValueError('Unknown or ambiguous card; supply its full ID: ' + identifier)
    path = ROOT / exact[0]['card_path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != exact[0]['card_sha256']:
        raise ValueError('Missing or changed card: refresh the scoped status layer before use')
    return exact[0]


def notice(identifier):
    records = rows('frontier/CURRENT_CLAIM_STATUS.jsonl')
    if not records:
        raise ValueError('Current status layer missing; restore it before retrieving historical claims')
    row = resolve(identifier, records)
    def compact(update):
        return {k: update[k] for k in ['target', 'relation', 'source_card', 'target_component', 'whole_claim_invalidated', 'scope', 'relation_status'] if k in update}
    def material(update):
        return update.get('relation', '').startswith(('supersedes', 'invalidates', 'corrects', 'refines'))
    updates = [compact(u) for u in row.get('material_updates', []) if material(u)]
    dependency_alerts = []
    for dep in row.get('depends_on', []):
        target = dep.get('target') if isinstance(dep, dict) else dep
        key = Path(target).stem if isinstance(target, str) else ''
        known = any(target == r['card_id'] or target == r['card_path'] or key == r['card_id'].split('-', 1)[0] for r in records)
        if not known:
            if re.match(r'^N\d+(?:-|$)', key):
                raise ValueError('Missing status for declared card dependency: ' + str(target))
            continue
        dependent = resolve(target, records)
        corrections = [compact(u) for u in dependent.get('material_updates', []) if material(u)]
        if corrections:
            dependency_alerts.append({'dependency': dependent['card_id'], 'scope': dep.get('scope', 'explicit dependency') if isinstance(dep, dict) else 'explicit dependency', 'updates': corrections, 'evidence_in': 'frontier/cards/' + dependent['card_id'] + '.json'})
    return {'card_id': row['card_id'], 'reported_claim_status': row['claim_status'],
            'proof_availability': row['proof_availability'].get('classification', 'unclassified'),
            'material_updates': updates, 'dependency_alerts': dependency_alerts,
            'status_path': 'frontier/cards/' + row['card_id'] + '.json',
            'evidence_scope': 'Full hash-pinned evidence and relations in status_path; no correction is silently truncated.',
            'external_correctness': 'unverified; newer claims do not certify older ones'}


def banner(identifier):
    value = notice(identifier)
    return 'CURRENT STATUS (read before using this historical source): ' + json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n'


def document_alerts(source_id):
    """Exact catalog associations only; do not infer mathematical dependencies."""
    alerts = []
    for claim in rows('indexes/claims.jsonl'):
        if source_id in claim.get('source_ids', []):
            value = notice(claim['id'])
            if value.get('material_updates') or value.get('dependency_alerts'):
                alerts.append(value)
    return alerts


def ranked(path, query, limit):
    if limit < 0:
        raise ValueError('limit must be non-negative')
    terms = list(dict.fromkeys(re.findall(r'\w+', query.lower())))
    scored = []
    for row in rows(path):
        hay = json.dumps(row, ensure_ascii=False).lower()
        score = sum(t in hay for t in terms)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda v: (-v[0], v[1].get('id', v[1].get('gate_id', ''))))
    return [row for _, row in scored[:limit]]


def lemma_routes(query, limit=3):
    return [{'id': r['id'], 'title': r['title'], 'path': 'literature/lemmas/' + r['id'] + '.json', 'claim_ids': r.get('claim_ids', []), 'review': r.get('review', {})}
            for r in ranked('literature/LEMMA_ATLAS.jsonl', query, limit)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['status', 'notice']:
        s = sub.add_parser(name); s.add_argument('id')
    for name in ['lemmas', 'gates']:
        s = sub.add_parser(name); s.add_argument('query'); s.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()
    if args.command == 'status':
        result = resolve(args.id)
    elif args.command == 'notice':
        result = notice(args.id)
    else:
        result = ranked('literature/LEMMA_ATLAS.jsonl' if args.command == 'lemmas' else 'frontier/OPEN_PROOF_GATES.jsonl', args.query, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(str(error))
