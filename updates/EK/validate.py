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

BASE = 'f12638af678bb8f3cc4039f10de78a55476a3a0c'
ORIGINAL_HEAD = '30097f1c13c65cf695e662245532a7ca619b1473'
PREFIX = 'research/2026-10-12-foundational-discovery-wave/'
MANIFEST_SHA = '8f8276ac4936eba68e365f89719096ab4ed72094dea8d11c1f68c27f6180e56a'
EXPECTED = {'N731':['F1','F2'], 'N732':['I1','I2','I3'], 'N733':['A1','A2','A3'], 'N734':['R1','R2']}
SOURCE_ONLY = ['Q8','SRC1','SRC2','M1']


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
    need(len(source_rows) == 59 and sum(x['bytes'] for x in source_rows) == 723940,
         'source coverage/extent changed')
    indexed = {x['original_relative_path']:x for x in source_rows}
    need(len(indexed) == 59 and 'MANIFEST.json' in indexed, 'source identities changed')
    p = ROOT/(PREFIX+'MANIFEST.json')
    need(sha(p.read_bytes()) == MANIFEST_SHA == indexed['MANIFEST.json']['sha256'],
         'producer manifest identity changed')
    producer = {x['path']:x['sha256'] for x in json.loads(p.read_text())['files']}
    need(len(producer) == 58 and set(producer) == set(indexed)-{'MANIFEST.json'} and
         manifest['producer_manifest']['member_hashes_checked'] == 58, 'producer coverage changed')
    scripts = 0
    for name,item in indexed.items():
        need(item['path'] == PREFIX+name and '..' not in Path(name).parts and
             not Path(name).is_absolute(), 'source path changed')
        data = (ROOT/item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'] and
             len(data.decode().splitlines()) == item['lines'], 'original bytes or extent changed')
        if name != 'MANIFEST.json':
            need(sha(data) == producer[name], 'producer member hash mismatch')
        need(data == git('show',ORIGINAL_HEAD+':'+item['path']), 'original PR bytes rewritten')
        if name.endswith('.py'):
            ast.parse(data,filename=name)
            scripts += 1
    need(scripts == 6, 'script coverage changed')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/PREFIX).rglob('*') if p.is_file()} ==
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
         'exact prompt/conversation invented from reconstructed session')
    r=trace['resources']; team=manifest['reported_team']
    need(r['worker_invocations'] == team['unique_accepted_launches'] == 20 and
         team['accepted_luna_max_launches'] == 15 and team['accepted_sol_max_launches'] == 5 and
         team['follow_up_and_retry_turn_count'] == team['peak_worker_concurrency'] == 'UNKNOWN',
         'launches, all turns or concurrency conflated')
    launches=load(PREFIX+'SPAWN_RECEIPTS.json')['agents']
    need(len(launches)==20 and sum(x['model']=='gpt-6-luna' for x in launches)==15 and
         sum(x['model']=='gpt-6.1-sol' for x in launches)==5 and
         all(x['reasoning_effort']=='max' and x['fork_turns']=='none' and
             x.get('acceptance',{}).get('task_name') for x in launches), 'accepted model receipts lost')
    need(all(v is None for v in trace['model'].values()) and
         r['reported_inference_seconds'] is None and r['reported_duration_ref_ids']==[] and
         all(v is None for v in r['usage'].values()) and r['usage_receipt_ref_ids']==[],
         'unmeasured usage/root model/concurrency inferred')
    need(r['worker_receipt_ref_ids']==['launches','execution'] and trace['matched_run_id'] is None and
         trace['advance']['verification']=='producer_reported' and
         trace['advance']['verification_receipt'] is None, 'comparative or independent verification invented')


def check_retained_gates(mapping, indexed):
    need([x['id'] for x in mapping['retained_source_only_claims']]==SOURCE_ONLY,
         'open or unaudited source-only claims dropped or made theorem cards')
    for n,phrase in [('deep/S2.md','no restriction on'),('deep/S1.md','1.67–4.69'),
                     ('deep/S5_inverse_challenge.md','certified')]:
        need(phrase in (ROOT/indexed[n]['path']).read_text(), 'source comparator/acquisition gate absent')
    need('NOT_ESTABLISHED' in next(x['status'] for x in mapping['retained_source_only_claims'] if x['id']=='M1'),
         'mission promoted')
    need(next(x['status'] for x in mapping['retained_source_only_claims'] if x['id']=='Q8').startswith('OPEN'),
         'paired mesh question promoted')


def main():
    manifest = load('updates/EK/SOURCE_MANIFEST.json'); mapping = load('updates/EK/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA' and manifest['campaign_status'] == 'NOT_ESTABLISHED' and manifest['original_pr_head_revision'] == ORIGINAL_HEAD,
         'base/source boundary or campaign outcome changed')
    indexed = check_sources(manifest); check_retained_gates(mapping,indexed)
    ledger = load(PREFIX+'CLAIMS.json')
    need(len(ledger['claims']) == 14, 'source claim ledger changed')
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
    need(sorted(covered+SOURCE_ONLY) == sorted(c['id'] for c in ledger['claims']) and proof_count == 25,
         'fourteen source claims or decisive proof ranges lost')
    need(len(trace_paths) == len(cp_paths) == 1, 'campaign costs/attempts duplicated per card')
    trace = load(next(iter(trace_paths))); validate_trace(trace,ROOT); check_trace(trace,manifest)
    cp = load(next(iter(cp_paths))); validate_record(cp,ROOT)
    need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
         'Independent repository intake' in cp['branch_purpose'], 'intake ancestry or original registration invented')
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
    print(json.dumps(dict(intake='EK',status='PASS',original_files=59,original_bytes=723940,
        producer_member_hashes_checked=58,source_ledger_claims=14,mechanism_cards=4,proof_ranges=proof_count,
        observational_campaign_traces=1,accepted_unique_worker_launches=20,peak_workers='UNKNOWN',
        record_level_intake_checkpoints=1,unchanged_earlier_scientific_routes=len(scientific),
        python_files_syntax_parsed=6,scientific_scripts_syntax_parsed_only=5,package_integrity_validator_executed=True,scientific_scripts_executed=0,
        scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
