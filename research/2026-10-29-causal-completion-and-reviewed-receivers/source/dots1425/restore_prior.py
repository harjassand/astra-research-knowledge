"""Restore exact prior scientific assets. Supply one or more local immutable ZIPs.
Usage: python restore_prior.py /path/Astra_Research_20261029_1225_UTC.zip [...]
No network access or overwriting different bytes. Missing archives are reported.
"""
import pathlib,json,hashlib,sys,zipfile
root=pathlib.Path(__file__).resolve().parent
expected={'Astra_Research_20261029_1225_UTC.zip':'18ca30c0d293555508e7d3b315c3cd58d097ebe5d258512a476ff7080e48266b','Astra_Research_20261029_1015_UTC.zip':'c5576cae243cbf23e60a2111c25023e76f1ce085cdbf2e2ce8e4ca36997e13d8','Astra_Research_20261029_0209_UTC.zip':'aa1df0f2581c7343f0234f6ca415a5bacdc82be1ccb6ccba1a3a3b17cc52cd67'}
archives={}
for arg in sys.argv[1:]:
 p=pathlib.Path(arg);assert p.name in expected,'Unknown archive';assert hashlib.sha256(p.read_bytes()).hexdigest()==expected[p.name],'Archive checksum mismatch';archives[p.name]=p
rows=json.loads((root/'PRIOR_DEPENDENCIES.json').read_text());missing=set();count=0
for row in rows:
 name=row['prior']['archive']
 if name not in archives:missing.add(name);continue
 with zipfile.ZipFile(archives[name]) as z:b=z.read(row['prior']['path'])
 assert hashlib.sha256(b).hexdigest()==row['sha256'];p=(root/row['path']).resolve();assert p.is_relative_to(root)
 if p.exists():assert p.read_bytes()==b
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 count+=1
print('Verified dependencies restored:',count)
if missing:print('Still required:',', '.join(sorted(missing)));sys.exit(1)
