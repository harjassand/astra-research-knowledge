#!/usr/bin/env python3
"""Read-only hash verification; does not rerun writers or alter any source."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;W=P.parent.parent
manifest=json.loads((P/'AUDIT_SHA256.json').read_text());n=0
for name,row in manifest['audit_payloads'].items():
 p=P/name;b=p.read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],p;n+=1
for binding_file in ['SOURCE_BINDINGS.json','DEPENDENCY_BINDINGS.json']:
 for name,row in json.loads((P/binding_file).read_text()).items():
  p=Path(name);p=p if p.is_absolute() else W/p;b=p.read_bytes()
  assert hashlib.sha256(b).hexdigest()==row['sha256'],p
  if 'bytes' in row:assert len(b)==row['bytes'],p
  n+=1
print('PASS read-only audit, source, and accepted-dependency bindings:',n)
