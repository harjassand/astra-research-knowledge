from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent;S=A.parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(S/'AUTHOR_STAGE_FREEZE.json')=='53686515708c0a407cb76b2d748f44efc5b7b7e2e845cd859b35f934ff8f6b9b'
for name,hs in json.loads((S/'AUTHOR_STAGE_FREEZE.json').read_text())['files'].items():assert h(S/name)==hs,name
assert h(S/'EXACT_CORRECTOR_AND_STAGE_LEMMA.md')=='0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2'
files={}
for p in sorted(A.rglob('*')):
 if not p.is_file()or '__pycache__'in p.parts or p.suffix=='.pyc'or p==A/'AUDIT_SHA256.json':continue
 assert not p.is_symlink();files[str(p.relative_to(A))]={'bytes':len(p.read_bytes()),'sha256':h(p)}
m={'scope':'PASS conditional full rate2 stage and carefully stopped composition; band-exit priority and endpoint conventions govern; no initial/global consumer','source_sha256':'0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2','independent_assertions':1393,'author_code_imported':False,'files':files}
p=A/'AUDIT_SHA256.json';assert not p.exists();p.write_text(json.dumps(m,indent=2)+'\n')
for name,z in files.items():
 p=A/name;assert len(p.read_bytes())==z['bytes']and h(p)==z['sha256'],name
for name,hs in json.loads((S/'AUTHOR_STAGE_FREEZE.json').read_text())['files'].items():assert h(S/name)==hs,name
for name in ['SOURCE_BOUND_ACCEPTANCE.md','MATHEMATICAL_REVIEW.md','AUDIT_SHA256.json']:
 p=A/name;print(name,len(p.read_bytes()),h(p))
print('FINAL IMMUTABLE READBACK PASS',len(files),'audit payloads and all four original stage payloads; no further writes.')
