#!/usr/bin/env python3
"""Check the ED PDF intake and historical preservation, not its mathematics.

Standard-library only. Extraction identity and page mapping are pinned; this
does not re-extract equations or substitute for reading the original PDF.
"""
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

BASE = '095f9a48edd1efdcc09f5b63a86eeeb35e80bac2'
CID = 'N715-saturated-signed-entailment-odd-cycle-probability'
PDF_SHA = '14a97779bc05ac0acb38a93c95ffa1cdd533bd8cd041685c32af858aab13247c'
TEXT_SHA = '76f6151a0c260641113e893464364f51fc2b22020a7d5ef798287683351ea8b1'
PAGE_RANGES = [[8,57],[60,111],[114,164],[167,215],
               [218,270],[273,322],[325,378],[381,437]]
IMPORTS = ['external:ED_FENG_FU_GUO_LEMMA17_ROOT_FLOW',
           'external:ED_FENG_FU_GUO_LEMMA16_COMPARISON']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text())


def rows(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def check_page_map(derived, text):
    lines = text.splitlines()
    mapping = derived['page_map']
    need(len(mapping) == 8 and len(lines) == derived['lines'] == 437, 'extraction extent changed')
    need([p['pdf_page'] for p in mapping] == list(range(1,9)) and
         [p['lines'] for p in mapping] == PAGE_RANGES, 'PDF page mapping changed')
    for page in mapping:
        start, end = page['lines']
        need(lines[start-2] == '=== ORIGINAL PDF PAGE ' + str(page['pdf_page']) + ' ===' and
             end-start+1 == page['extracted_line_count'], 'page boundary or extent changed')
    need(lines[0] == 'DERIVED TEXT EXTRACTION — NOT ORIGINAL MANUSCRIPT BYTES' and
         lines[2] == 'Original PDF SHA256: ' + PDF_SHA and
         derived['original_sha256'] == PDF_SHA, 'extraction mistaken for original')


def check_status(status):
    need(status['claim_status'] == 'source_derived_unreviewed', 'scientific promotion')
    need([d['target'] for d in status['depends_on']] == IMPORTS,
         'missing imported proof obligation or invented Astra dependency')
    need(all(status[key] == [] for key in ['supersedes','invalidates','material_updates','contrasting_blockers']),
         'unsupported earlier-claim relation')
    need(status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'independent correctness or priority invented')


def check_unknown_workflow(trace):
    need(trace['mode'] == trace['context']['conversation_relation'] == trace['prompt_availability'] == 'UNKNOWN' and
         trace['prompt_ref_ids'] == [] and trace['context']['context_ref_ids'] == [] and
         trace['context']['retained_context'] is None and trace['context']['capital_access'] is None,
         'prompt or retained conversation inferred from manuscript')
    resources = trace['resources']
    need(all(v is None for v in trace['model'].values()) and
         all(v is None for v in resources['usage'].values()) and
         resources['reported_inference_seconds'] is None and resources['worker_invocations'] is None and
         all(resources[k] == [] for k in ['reported_duration_ref_ids','usage_receipt_ref_ids','worker_receipt_ref_ids']),
         'PDF timestamp or missing evidence promoted to resource telemetry')
    need(trace['matched_run_id'] is None and trace['advance']['verification'] == 'producer_reported' and
         trace['advance']['verification_receipt'] is None, 'independent reproduction or matched trial invented')


def main():
    manifest = load('updates/ED/SOURCE_MANIFEST.json')
    claim_map = load('updates/ED/CLAIMS.json')
    need(manifest['intake_base_revision'] == claim_map['base_revision'] == BASE, 'base changed')
    need(manifest['source_handling'] == 'source=DATA' and len(manifest['originals']) ==
         len(manifest['derived_extractions']) == len(claim_map['claims']) == 1, 'source coverage changed')
    original, derived = manifest['originals'][0], manifest['derived_extractions'][0]
    data = (ROOT / original['path']).read_bytes()
    need(sha(data) == original['sha256'] == PDF_SHA and len(data) == original['bytes'] == 195071 and
         original['pages'] == 8 and original['reported_duration_seconds'] is None, 'original PDF changed')
    text = (ROOT / derived['path']).read_bytes()
    need(sha(text) == derived['sha256'] == TEXT_SHA and len(text) == derived['bytes'], 'derived extraction changed')
    check_page_map(derived, text.decode())
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/ED/package').rglob('*') if p.is_file()} ==
         {original['path'], derived['path']}, 'missing/extra archived disclosure')
    ledgers = {p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
                                 'indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in [original,derived]:
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == item['source_id']]
        docs = [r for r in ledgers['web/documents.jsonl'] if r['id'] == item['source_id']]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'] and
             metadata[0]['path'] == docs[0]['path'] == item['path'], 'source metadata disagreement')
        if item is original:
            need(docs[0]['extraction'] == 'original_binary' and docs[0]['url'] == '../'+item['path'],
                 'original PDF misrendered')
        else:
            need(docs[0]['extraction'] == 'derived_pdf_layout_text' and
                 '<pre>'+html.escape(text.decode())+'</pre>' in (ROOT/('web/'+docs[0]['url'])).read_text(),
                 'derived text web route changed content')
    entry = claim_map['claims'][0]
    need(entry['id'] == CID and entry['source_sha256'] == PDF_SHA, 'claim source identity changed')
    statuses = [s for s in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if s['card_id'] == CID]
    claims = [s for s in ledgers['indexes/claims.jsonl'] if s['id'] == CID]
    catalog = [s for s in load('indexes/agent_catalog.json')['claims'] if s['id'] == CID]
    need(len(statuses) == len(claims) == len(catalog) == 1, 'claim coverage')
    status = statuses[0]
    check_status(status)
    need(status == load('frontier/cards/'+CID+'.json') and
         entry['status'] == claims[0]['status'] == status['claim_status'] and
         claims[0]['depends_on'] == IMPORTS, 'status/dependency disagreement')
    card = (ROOT/status['card_path']).read_bytes()
    need(sha(card) == status['card_sha256'] == catalog[0]['card_sha256'] and
         (ROOT/('frontier/review_cards/'+CID+'.txt')).read_bytes().endswith(card), 'card/wrapper hash mismatch')
    proof = status['proof_availability']
    need(len(proof['located_proof_sources']) == 6 and len(proof['available_evidence_sources']) == 1, 'argument coverage changed')
    for ref in proof['located_proof_sources'] + proof['available_evidence_sources']:
        need(ref['path'] == derived['path'] and ref['sha256'] == derived['sha256'] and
             ref['hash_kind'] == 'derived_utf8_bytes' and ref['original_sha256'] == PDF_SHA and
             1 <= ref['lines'][0] <= ref['lines'][1] <= derived['lines'], 'page-mapped argument ref invalid')
    graph = load('indexes/agent_graph.json')
    node_ids = {n['id'] for n in graph['nodes']}
    need(len(node_ids) == len(graph['nodes']) and all(e['from'] in node_ids and e['to'] in node_ids for e in graph['edges']), 'graph integrity')
    need(set(claims[0]['source_ids']) == {e['to'] for e in graph['edges'] if e['from'] == CID and e['kind'] == 'provenance'}, 'provenance missing')
    need(CID+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'legacy route missing')
    for topic in status['topics']:
        need(CID+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
    need(any(CID in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'review gate missing')
    trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_unknown_workflow(trace)
    cp = load(entry['checkpoint']); validate_record(cp,ROOT)
    need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [], 'checkpoint ancestry invented')
    generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
    view = 'state/branches/'+cp['branch_id']+'.txt'
    need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
    row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
    need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
    # Preserve earlier source/card/status/checkpoint/evaluation objects, ledgers,
    # dependency semantics and every old scientific navigation byte.
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)), 'historical ledger rewritten: '+path)
    for path,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old,now = json.loads(git('show',BASE+':'+path)),load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog rewritten')
    old,now = json.loads(git('show',BASE+':indexes/query_aliases.json')),load('indexes/query_aliases.json')
    need(all(now.get(k) == v for k,v in old.items()), 'historical alias changed')
    old_paths = set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    changed = set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','state/checkpoints','state/branches','evaluation','technology/records').decode().splitlines())
    need(not (changed & old_paths), 'earlier scientific/source object changed')
    outputs = json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    need(manifest['permitted_historical_navigation_changes'] == [] and
         all((ROOT/p).is_file() and sha((ROOT/p).read_bytes()) == d for p,d in scientific.items()), 'earlier scientific navigation changed')
    print(json.dumps(dict(intake='ED',status='PASS',original_pdfs=1,original_bytes=195071,
                          mapped_pdf_pages=8,proof_ranges=6,reported_check_summary_ranges=1,
                          record_level_checkpoints=1,unchanged_earlier_scientific_routes=len(scientific),
                          scientific_scripts_executed=0,independent_scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
