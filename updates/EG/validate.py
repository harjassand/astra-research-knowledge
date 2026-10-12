#!/usr/bin/env python3
"""Deterministic campaign intake checks; no scientific script execution."""
import ast
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views

BASE = '5fc72a144d77c31b400efc0768afd7833c702362'
PREFIX = 'updates/EG/package/frontier_campaign/'
MANIFEST_SHA = '0c3ca9947fb3a28e3ad5a03c02657e19e98a5f97d16ae665956fff09b4e67473'
EXPECTED = {
    'N720': ['thermal_work','thermal_transduction'],
    'N721': ['hidden_channel_queries','cross_flux_sampler'],
    'N722': ['gaussian_mean_factory'],
    'N723': ['prestressed_separator'],
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads((ROOT/path).read_text())


def rows(path):
    return [json.loads(l) for l in (ROOT/path).read_text().splitlines() if l.strip()]


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def check_sources(manifest):
    source_rows = manifest['originals']
    need(len(source_rows) == 28 and sum(x['bytes'] for x in source_rows) == 228520,
         'source coverage/extent changed')
    indexed = {x['original_relative_path']:x for x in source_rows}
    need(len(indexed) == 28 and 'MANIFEST.sha256' in indexed, 'source identities changed')
    p = ROOT/(PREFIX+'MANIFEST.sha256')
    need(sha(p.read_bytes()) == MANIFEST_SHA == indexed['MANIFEST.sha256']['sha256'],
         'producer manifest identity changed')
    producer = dict((l.split('  ',1)[1],l.split('  ',1)[0]) for l in p.read_text().splitlines())
    need(len(producer) == 27 and set(producer) == set(indexed)-{'MANIFEST.sha256'} and
         manifest['producer_manifest']['member_hashes_checked'] == 27, 'producer coverage changed')
    scripts = 0
    for name,item in indexed.items():
        need(item['path'] == PREFIX+name and '..' not in Path(name).parts and
             not Path(name).is_absolute(), 'source path changed')
        data = (ROOT/item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'] and
             len(data.decode().splitlines()) == item['lines'], 'original bytes or extent changed')
        if name != 'MANIFEST.sha256':
            need(sha(data) == producer[name], 'producer member hash mismatch')
        if name.endswith('.py'):
            ast.parse(data,filename=name)
            scripts += 1
    need(scripts == 5, 'script coverage changed')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EG/package').rglob('*') if p.is_file()} ==
         {x['path'] for x in indexed.values()}, 'extra or missing archived disclosure')
    return indexed


def check_status(status):
    need(status['claim_status'] == 'source_derived_unreviewed', 'scientific promotion')
    need(all(status[k] == [] for k in ['depends_on','supersedes','invalidates','material_updates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need(status['validation']['external_correctness'] == 'UNKNOWN', 'external correctness invented')


def check_trace(trace, manifest):
    need(trace['mode'] == 'source_intensive_multi_agent' and trace['status'] == 'completed' and
         trace['context']['conversation_relation'] == trace['prompt_availability'] == 'UNKNOWN' and
         trace['prompt_ref_ids'] == [] and trace['context']['retained_context'] is None,
         'initiating prompt/conversation or mission success inferred')
    resources = trace['resources']; team = manifest['reported_team']
    need(resources['worker_invocations'] == team['dispatched_turns'] == 8 and
         resources['usage']['parallel_workers'] == team['peak_worker_concurrency'] == 4 and
         team['unique_workers'] == 4 and team['root_excluded_from_peak'] is True and
         team['child_workers_spawned'] == 0, 'unique workers, turns or peak conflated')
    need([(w['requested_model'],w['requested_reasoning'],w['dispatched_turns'])
          for w in team['accepted_requested_configurations']] ==
         [('gpt-6.1-sol','max',2),('gpt-6.1-sol','max',2),
          ('gpt-6-luna','max',2),('gpt-6-luna','max',2)], 'requested configurations changed')
    need(all(v is None for v in trace['model'].values()) and
         resources['reported_inference_seconds'] is None and
         resources['reported_duration_ref_ids'] == [] and
         all(v is None for k,v in resources['usage'].items() if k != 'parallel_workers'),
         'clock span/requested models promoted to actual inference telemetry')
    need(resources['worker_receipt_ref_ids'] == resources['usage_receipt_ref_ids'] == ['ledger'] and
         manifest['observed_clock']['elapsed_seconds'] == 2201, 'worker receipt or clock provenance lost')
    need(trace['matched_run_id'] is None and trace['advance']['verification'] == 'producer_reported' and
         trace['advance']['verification_receipt'] is None and
         trace['advance']['scientific_status'].startswith('NOT_ACHIEVED;'), 'mission or independent verification promoted')


def check_correction(indexed):
    text = (ROOT/indexed['scientific_obstruction/OBSTRUCTION.md']['path']).read_text()
    need(text.splitlines()[2].startswith('> **Correction') and
         'The bold verdict immediately below is the historical verdict retained verbatim' in text and
         'external-fixture premise and verdict are superseded' in text,
         'historical scout correction authority lost')
    corrected = (ROOT/indexed['scientific_obstruction/PRESTRESS_TRANSFER.md']['path']).read_text()
    need('**Decision: reject' in corrected and 'retained shape-memory-alloy' in corrected,
         'final retained-ring correction missing')


def main():
    manifest = load('updates/EG/SOURCE_MANIFEST.json'); mapping = load('updates/EG/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA' and manifest['campaign_status'] == 'NOT_ACHIEVED',
         'base/source boundary or campaign outcome changed')
    indexed = check_sources(manifest); check_correction(indexed)
    ledger = load(PREFIX+'CLAIM_LEDGER.json')
    need(ledger['campaign_status'] == 'NOT_ACHIEVED' and len(ledger['claims']) == 6, 'source claim ledger changed')
    ledgers = {p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
                                  'indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in indexed.values():
        metadata = [x for x in ledgers['indexes/source_metadata.jsonl'] if x.get('source_id') == item['source_id']]
        docs = [x for x in ledgers['web/documents.jsonl'] if x['id'] == item['source_id']]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'] and
             metadata[0]['path'] == docs[0]['path'] == item['path'], 'source metadata mismatch')
        need('<pre>'+html.escape((ROOT/item['path']).read_text())+'</pre>' in
             (ROOT/('web/'+docs[0]['url'])).read_text(), 'source web mirror changed')
    need(len(mapping['claims']) == 4, 'mechanism scope count changed')
    trace_paths = set(); cp_paths = set(); proof_count = 0; covered = []
    for entry in mapping['claims']:
        cid = entry['id']; route = cid.split('-',1)[0]
        need(entry['source_ledger_claim_ids'] == EXPECTED[route], 'source claim scope mapping changed')
        primary = next(x for x in indexed.values() if x['path'] == entry['source_path'])
        need(entry['source_sha256'] == primary['sha256'] and entry['source_id'] == primary['source_id'],
             'claim source pointer disagreement')
        covered += entry['source_ledger_claim_ids']; trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
        statuses = [s for s in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if s['card_id'] == cid]
        claims = [s for s in ledgers['indexes/claims.jsonl'] if s['id'] == cid]
        catalogs = [s for s in load('indexes/agent_catalog.json')['claims'] if s['id'] == cid]
        need(len(statuses) == len(claims) == len(catalogs) == 1, 'claim coverage')
        status = statuses[0]; check_status(status)
        need(status == load('frontier/cards/'+cid+'.json') and entry['status'] == claims[0]['status'] ==
             status['claim_status'] and claims[0]['depends_on'] == claims[0]['scoped_dependencies'] == [], 'claim agreement')
        card = (ROOT/status['card_path']).read_bytes()
        need(sha(card) == status['card_sha256'] == catalogs[0]['card_sha256'] and
             (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card), 'card/wrapper disagreement')
        proofs = status['proof_availability']['located_proof_sources']; proof_count += len(proofs)
        for r in proofs+status['proof_availability']['available_evidence_sources']:
            item = next(x for x in indexed.values() if x['path'] == r['path'])
            need(r['sha256'] == item['sha256'] and 1<=r['lines'][0]<=r['lines'][1]<=item['lines'], 'proof/source range invalid')
        need(cid+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'legacy route missing')
        for topic in status['topics']:
            need(cid+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
        need(any(cid in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'next gate missing')
    need(sorted(covered) == sorted(c['id'] for c in ledger['claims']) and proof_count == 18,
         'six source claims or proof ranges lost')
    need(len(trace_paths) == len(cp_paths) == 1, 'campaign costs/attempts duplicated per card')
    trace = load(next(iter(trace_paths))); validate_trace(trace,ROOT); check_trace(trace,manifest)
    cp = load(next(iter(cp_paths))); validate_record(cp,ROOT)
    need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [], 'intake ancestry invented')
    generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
    view = 'state/branches/'+cp['branch_id']+'.txt'
    need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
    row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
    need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)), 'historical ledger rewritten')
    for path,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old,now = json.loads(git('show',BASE+':'+path)),load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog rewritten')
    graph = load('indexes/agent_graph.json'); node_ids = {n['id'] for n in graph['nodes']}
    need(len(node_ids) == len(graph['nodes']) and
         all(e['from'] in node_ids and e['to'] in node_ids for e in graph['edges']), 'graph integrity')
    for entry in mapping['claims']:
        claim = next(c for c in ledgers['indexes/claims.jsonl'] if c['id'] == entry['id'])
        need(set(claim['source_ids']) == {e['to'] for e in graph['edges']
             if e['from'] == entry['id'] and e['kind'] == 'provenance'}, 'claim provenance missing')
    old_aliases = json.loads(git('show',BASE+':indexes/query_aliases.json'))
    current_aliases = load('indexes/query_aliases.json')
    need(all(current_aliases.get(k) == v for k,v in old_aliases.items()),
         'earlier alias changed')
    old_paths = set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    changed = set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','state/checkpoints',
                      'state/branches','evaluation','technology/records').decode().splitlines())
    need(not changed & old_paths, 'earlier scientific/source/checkpoint/evaluation object changed')
    outputs = json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    need(manifest['permitted_historical_navigation_changes'] == [] and
         all((ROOT/p).is_file() and sha((ROOT/p).read_bytes()) == d for p,d in scientific.items()),
         'earlier scientific navigation changed')
    print(json.dumps(dict(intake='EG',status='PASS',original_files=28,original_bytes=228520,
        producer_member_hashes_checked=27,source_ledger_claims=6,mechanism_cards=4,proof_ranges=18,
        observational_campaign_traces=1,reported_unique_workers=4,reported_worker_turns=8,reported_peak_workers=4,
        record_level_checkpoints=1,unchanged_earlier_scientific_routes=len(scientific),
        scientific_scripts_syntax_parsed_only=5,scientific_scripts_executed=0,scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
