"""Verify source identities, script/output binding and the bounded-search inputs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent;SRC=BASE/'sources';OUT=ROOT/'outputs/external_openings_20261101'
expected={
 'certification_v1p1.pdf':'2de704db53e75e9e4b4f93a6cf295a9e42a1c280c923ec3a07495ced667a3cd6',
 'predictive_v1p0.pdf':'075456b81bb08fcbcb2621e827303f838a96a43e7a0747da98661f68c806c872',
 'noise_energy_v1p0.pdf':'da209777d7d0b8144a3cb6d31ad05b1a5d3baef4609f9519aacf606147875fb0',
 'astra_output_mode.md':'423e5f1966a61dde79b761b155adfbb13b80f6dd2fd7e43b79e47215da563e59',
 'astra_output_mode_review.md':'b606162a773d9553e5f020b56ea70cea5e2b9ad93833f91fb25a7764eed0b859',
 'astra_capture_source.md':'2913cf3bafc9251571153785642575355228e89123374f750a724d6940fb4894',
 'astra_capture_review.txt':'769d8aa029a61842cf0d599d505ce2f628a950e4cadfa35ed619f36563687200',
 'astra_amplifier_source.tex':'cfdbb6a0ca85861788d39c8843ce7533a641633c4cabab8070ac09b9d41d170d'}
for name,want in expected.items():
    p=SRC/name;raw=p.read_bytes()
    # apply_patch added one terminal LF to fetched UTF-8 source copies.
    # Remove it ONLY when doing so reproduces the exact advertised hash.
    if hashlib.sha256(raw).hexdigest()!=want and raw.endswith(b'\n') and hashlib.sha256(raw[:-1]).hexdigest()==want:
        p.write_bytes(raw[:-1]);raw=raw[:-1]
    assert hashlib.sha256(raw).hexdigest()==want,name
for record,name in (('23746737','certification_v1p1.pdf'),('23650027','predictive_v1p0.pdf'),('23629201','noise_energy_v1p0.pdf')):
    d=json.loads((SRC/(record+'.json')).read_text());entries=d['files']
    if isinstance(entries,dict):entries=list(entries['entries'].values())
    advertised=[v['checksum'].split(':',1)[1] for v in entries if v['key'].lower().endswith('.pdf')]
    assert hashlib.md5((SRC/name).read_bytes()).hexdigest() in advertised,name
bindings={'receiver_bounds.json':'receiver_frontier.py','interval_receiver_checks.json':'interval_receiver.py',
          'jc_and_causal_checks.json':'jc_and_causal_controls.py','failed_transfers.json':'failed_transfers.py',
          'resource_controls.json':'resource_controls.py'}
for output,script in bindings.items():
    d=json.loads((OUT/output).read_text())
    assert d['script_sha256']==hashlib.sha256((BASE/script).read_bytes()).hexdigest(),script
assert json.loads((OUT/'interval_receiver_checks.json').read_text())['bound_script_sha256']==hashlib.sha256((BASE/'receiver_frontier.py').read_bytes()).hexdigest()
manifest=json.loads((SRC/'astra_search_manifest.json').read_text())
assert hashlib.sha256((SRC/'astra_catalog.json').read_bytes()).hexdigest()==manifest['outputs']['knowledge/current/catalog.json']
for p in (SRC/'astra_shards').glob('*.json'):
    folder,shard=p.stem.split('_')
    assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['outputs'][f'knowledge/current/{folder}/{shard}.json'],p
result={'status':'PASS source hashes, three Zenodo MD5 identities, five script/output bindings and 13 pinned search inputs',
        'original_source_sha256':expected,'script_output_bindings':bindings,
        'scope':'identity and arithmetic provenance, not an independent scientific audit'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
