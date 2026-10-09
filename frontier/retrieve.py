#!/usr/bin/env python3
"""Portable decision/lemma retrieval for either the full or static repository."""
import argparse
import hashlib
import json
import re
import subprocess
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
    updates = [compact(u) for u in row.get('material_updates', [])]
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
        corrections = [compact(u) for u in dependent.get('material_updates', [])]
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


def route_id(identifier):
    return identifier.split('-', 1)[0] if re.match(r'^[NL]\d+(?:-|$)', identifier) else identifier


def access_manifest():
    """Fail closed on stale generated evidence without needing the private snapshot."""
    path = ROOT / 'agent/access_manifest.json'
    if not path.is_file():
        raise ValueError('Public access views absent; run frontier/build_access.py build')
    manifest = json.loads(path.read_text())
    for name, expected in manifest['inputs'].items():
        target = ROOT / name
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError('Public access inputs changed: ' + name + '; regenerate with frontier/build_access.py build')
    return manifest


def view(identifier, kind='dossiers', manifest=None):
    manifest = access_manifest() if manifest is None else manifest
    row = resolve(identifier)
    path = 'frontier/' + kind + '/' + route_id(row['card_id']) + ('.txt' if kind == 'dossiers' else '.json')
    data = (ROOT / path).read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest['outputs'].get(path):
        raise ValueError('Changed generated view: ' + path)
    return data


def task_routes(query, limit):
    """Lexical metadata lookup, with explicit scoped blocker routes; no applicability inference."""
    if limit < 0:
        raise ValueError('limit must be non-negative')
    aliases = json.loads((ROOT / 'indexes/query_aliases.json').read_text())
    terms = set(re.findall(r'\w+', query.lower()))
    records = rows('indexes/claims.jsonl')
    scored = []
    for row in records:
        title = row['title'].lower()
        hay = title + ' ' + aliases.get(row['id'], '').lower()
        words = set(re.findall(r'\w+', hay))
        score = 3 * sum(t in set(re.findall(r'\w+', title)) for t in terms) + sum(t in words for t in terms)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda x: (-x[0], x[1]['id']))
    routes = []
    for _, row in scored[:limit]:
        status = resolve(row['id'])
        routes.append({'id': row['id'], 'title': row['title'], 'status': status['claim_status'],
                       'dossier': 'frontier/dossiers/' + route_id(row['id']) + '.txt',
                       'material_notice_count': len(status['material_updates']),
                       'contrasting_blockers': status['contrasting_blockers']})
    return {'policy': 'Lexical routing only. Read the dossier, paired interfaces and decisive proof before composing claims.', 'routes': routes}


def changes(since):
    if not re.fullmatch(r'[0-9a-f]{40}', since):
        raise ValueError('--since requires a full saved Git commit ID')
    def previous(path):
        process = subprocess.run(['git', 'show', since + ':' + path], cwd=ROOT, capture_output=True, text=True)
        if process.returncode:
            raise ValueError('Saved revision lacks required ledger: ' + path)
        return [json.loads(line) for line in process.stdout.splitlines() if line.strip()]
    output = {'since': since, 'policy': 'Compare authoritative scoped records, not blanket regenerated-file diffs; changed does not mean superseded.'}
    for path, key, label in [('frontier/CURRENT_CLAIM_STATUS.jsonl', 'card_id', 'cards'),
                             ('frontier/OPEN_PROOF_GATES.jsonl', 'gate_id', 'gates')]:
        before = {r[key]: r for r in previous(path)}
        after = {r[key]: r for r in rows(path)}
        output[label] = {'added': sorted(after.keys() - before.keys()), 'removed': sorted(before.keys() - after.keys()),
                         'changed': sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}
    result = subprocess.run(['git', 'diff', '--name-only', since, '--', 'state/checkpoints', 'agent/SEMANTIC_NOTICES.jsonl', 'mechanisms/bridge_candidates.json'], cwd=ROOT, capture_output=True, text=True, check=True)
    output['handoffs_or_semantic_records'] = result.stdout.splitlines()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['status', 'notice']:
        s = sub.add_parser(name); s.add_argument('id')
    for name in ['lemmas', 'gates']:
        s = sub.add_parser(name); s.add_argument('query'); s.add_argument('--limit', type=int, default=5)
    s = sub.add_parser('routes'); s.add_argument('query'); s.add_argument('--limit', type=int, default=5)
    for name in ['dossier', 'connections']:
        s = sub.add_parser(name); s.add_argument('id')
    s = sub.add_parser('packet'); s.add_argument('ids', nargs='+'); s.add_argument('--max-bytes', type=int, default=32768)
    s = sub.add_parser('changes'); s.add_argument('--since', required=True)
    args = parser.parse_args()
    if args.command == 'status':
        result = resolve(args.id)
    elif args.command == 'notice':
        result = notice(args.id)
    elif args.command == 'routes':
        result = task_routes(args.query, args.limit)
    elif args.command == 'changes':
        result = changes(args.since)
    elif args.command in ['dossier', 'connections']:
        data = view(args.id, 'dossiers' if args.command == 'dossier' else 'connections')
        print(data.decode(), end='')
        return
    elif args.command == 'packet':
        manifest = access_manifest()
        identifiers = list(dict.fromkeys(resolve(i)['card_id'] for i in args.ids))
        data = b'\n'.join(view(i, manifest=manifest) for i in identifiers)
        if args.max_bytes < 1 or len(data) > args.max_bytes:
            raise ValueError('Complete packet requires ' + str(len(data)) + ' UTF-8 bytes; select fewer results or raise --max-bytes. No card, correction or proof locator was truncated.')
        print(data.decode(), end='')
        return
    else:
        result = ranked('literature/LEMMA_ATLAS.jsonl' if args.command == 'lemmas' else 'frontier/OPEN_PROOF_GATES.jsonl', args.query, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
