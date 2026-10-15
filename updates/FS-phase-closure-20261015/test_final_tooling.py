#!/usr/bin/env python3
"""Disposable stdlib fixtures only; no real scientific source is executed."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import tempfile

HERE = Path(__file__).resolve().parent
def module(name):
    spec = importlib.util.spec_from_file_location('fixture_' + name, HERE / (name + '.py'))
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj); return obj
r = module('replay'); v = module('validate'); checks = []
def fail(label, action):
    try: action()
    except (ValueError, FileNotFoundError): checks.append(label)
    else: raise AssertionError('expected fail closed: ' + label)
def write(root, name, data):
    p = root / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); return p

with tempfile.TemporaryDirectory(prefix='fs-final-software-fixture-') as temp:
    root = Path(temp); work = root / 'work'; work.mkdir(); out = root / 'out'; out.mkdir()
    normal = b"from pathlib import Path\nimport json\nPath(__file__).with_name('normal.json').write_text(json.dumps({'status':'PASS','fixture_only':True}))\n"
    integral = b"from pathlib import Path\nimport json\nPath(__file__).with_name('integral.json').write_text(json.dumps({'N':512,'status':'inconclusive interval bound','fixture_only':True}))\n"
    write(work, 'normal.py', normal); write(work, 'integral.py', integral)
    write(work, 'normal.json', b'{"status":"STALE_COPY"}')
    originals = {'normal.py': r.digest(normal), 'integral.py': r.digest(integral)}
    specs = [('normal', 'normal.py', [], 'normal.json'), ('phase_integral512', 'integral.py', [], 'integral.json')]
    results, inconclusive = r.execute_steps(work, out, Path(sys.executable), 10, specs=specs, originals=originals)
    assert all(x['execution_check'] == 'PASS' for x in results)
    checks.append('two bounded stdlib fixture subprocesses complete')
    assert results[0]['copied_prior_result_sha256'] is not None and json.loads((out / 'results/normal.json').read_text())['status'] == 'PASS'
    checks.append('copied stale result is removed before execution')
    assert len(inconclusive) == 1 and inconclusive[0]['name'] == 'phase_integral512'
    checks.append('expected inconclusive interval is retained separately')
    packet = root / r.PREFIX
    write(packet, 'normal.py', normal); write(packet, 'integral.py', integral)
    write(packet, 'replay.py', (HERE / 'replay.py').read_bytes())
    for name in ['PUBLISHED_INPUTS.json', 'PACKET_INPUTS.json']: write(out, name, b'{}\n')
    receipt = {'status':'PASS','published_inputs_hash_unchanged':True,'changed_published_paths':[],
        'base_revision':r.BASE,'total_steps':len(results),'checks':results,'all_positivity_certified':False,
        'generator_sha256':r.sha(packet/'replay.py'),'inconclusive_results':inconclusive,
        'pinned_dependencies':[],'runtime_adapters':[],
        'published_input_manifest':{'path':'PUBLISHED_INPUTS.json','sha256':r.sha(out/'PUBLISHED_INPUTS.json')},
        'packet_input_manifest':{'path':'PACKET_INPUTS.json','sha256':r.sha(out/'PACKET_INPUTS.json')}}
    write(out, 'RECEIPT.json', r.encoded(receipt)); v.check_replay(root, out, specs)
    checks.append('scoped replay validator accepts complete fixture receipts')
    bad = dict(receipt); bad['all_positivity_certified'] = True
    write(out, 'RECEIPT.json', r.encoded(bad)); fail('all-positivity promotion rejected', lambda:v.check_replay(root,out,specs))
    write(out, 'RECEIPT.json', r.encoded(receipt)); (out/'normal.log').write_text('tampered fixture log')
    fail('fresh log hash drift rejected', lambda:v.check_replay(root,out,specs))
    alias_work = root / 'aliases'; (alias_work/'package').mkdir(parents=True)
    radial = "import subprocess\nassert head==PIN, (head,PIN)\n"
    external = "import subprocess\nassert actual==PIN\n"
    write(alias_work,'synthesis/radial_analysis/check_radial_extensions.py',radial.encode())
    write(alias_work,'synthesis/external_duality/verify_external_duality.py',external.encode())
    adapters = r.adapt_copy(alias_work, root)
    assert (alias_work/'sources').is_symlink() and (alias_work/'sources').resolve() == (alias_work/'package').resolve()
    assert len(adapters) == 3 and all(x.get('adapted_sha256') != x.get('original_sha256') for x in adapters if 'file' in x)
    checks.append('copy-only source alias and descendant adapters record changed hashes')
    source = write(root,'source.txt',b'one\ntwo\n'); ref={'path':'source.txt','sha256':v.digest(source.read_bytes()),'lines':[1,2]};v.check(root,ref)
    checks.append('exact evidence bytes and inclusive range accepted')
    fail('out-of-range evidence rejected',lambda:v.check(root,{**ref,'lines':[1,3]}))
    fail('wrong original evidence hash rejected',lambda:v.check(root,{**ref,'sha256':'f'*64}))
    write(root,'source.html',b'<pre>one\ntwo\n</pre>');v.check(root,{**ref,'path':'missing.txt','read_path':'source.html'})
    checks.append('hash-selected legacy HTML evidence recovered exactly')
    fail('repository path escape rejected',lambda:v.local(root,'../escape'))
    # Historical array/key/order checks use synthetic Git bytes, never a real Git mutation.
    baseline = {}
    for name in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','web/documents.jsonl','state/branches.tsv']:
        baseline[name]=b'fixture-old-line\n';write(root,name,baseline[name]+b'fixture-new-line\n')
    containers={'indexes/agent_catalog.json':{'schema':'fixture','claims':[]},'indexes/agent_graph.json':{'schema':'fixture','nodes':[],'edges':[]},'mechanisms/bridge_candidates.json':{'schema':'fixture','bridges':[],'rejected_transfers':[]},'web/catalog.json':[],'indexes/query_aliases.json':{'old':'alias'}}
    for name,value in containers.items():baseline[name]=v.encoded(value);write(root,name,baseline[name])
    changed=[]
    def fake_git(_root,*args):
        if args[0]=='show':return baseline[args[1].split(':',1)[1]]
        if args[0]=='ls-tree':return b'web/pages/prior.html\n'
        if args[0]=='diff':return ('\n'.join(changed)+'\n').encode() if changed else b''
        raise AssertionError(args)
    v.git=fake_git;v.check_history(root);checks.append('append-only synthetic historical prefixes accepted')
    changed.append('web/pages/prior.html');fail('historical web-page mutation rejected',lambda:v.check_history(root))
    changed.clear();write(root,'indexes/agent_catalog.json',b'{"claims":[],"schema":"fixture"}\n')
    fail('historical JSON key/format rewrite rejected',lambda:v.check_history(root))

report={'status':'PASS','scope':'Disposable integration/replay software fixtures only; no scientific verifier executed.',
    'checks':checks,'check_count':len(checks),'published_repository_modified':False,
    'replay_sha256':hashlib.sha256((HERE/'replay.py').read_bytes()).hexdigest(),
    'validate_sha256':hashlib.sha256((HERE/'validate.py').read_bytes()).hexdigest()}
(HERE/'FINAL_TOOLING_FIXTURE_RECEIPT.json').write_bytes(r.encoded(report));print(json.dumps(report,indent=2))
