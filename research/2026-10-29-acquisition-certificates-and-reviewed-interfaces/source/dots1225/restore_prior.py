"""Restore exact unchanged dependencies from the prior immutable local ZIP.
Usage: python restore_prior.py /path/Astra_Research_20261029_1015_UTC.zip
No network, execution, or overwrite of different bytes.
"""
import pathlib,json,hashlib,sys,zipfile
root=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit(__doc__)
a=pathlib.Path(sys.argv[1]);expected='c5576cae243cbf23e60a2111c25023e76f1ce085cdbf2e2ce8e4ca36997e13d8'
assert hashlib.sha256(a.read_bytes()).hexdigest()==expected,'Prior archive hash mismatch'
with zipfile.ZipFile(a) as z:
 for row in json.loads((root/'PRIOR_DEPENDENCIES.json').read_text()):
  assert row['prior']['archive']=='Astra_Research_20261029_1015_UTC.zip'
  b=z.read(row['prior']['path']);assert hashlib.sha256(b).hexdigest()==row['sha256']
  p=(root/row['path']).resolve();assert p.is_relative_to(root)
  if p.exists():assert p.read_bytes()==b;continue
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('Verified prior dependencies restored; original archive unchanged.')
