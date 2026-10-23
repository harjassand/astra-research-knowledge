"""Retrieve the exact scientific input, or verify/reuse an already supplied copy.
No credential required. Streams to a temporary file; rejects wrong bytes/hash.
"""
from pathlib import Path
import argparse,hashlib,json,os,time,urllib.request
ROOT=Path(__file__).resolve().parents[1]
URL='https://zenodo.org/records/13350497/files/WesselsSatija2023.h5ad?download=1'
SHA='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732';SIZE=219393529
def identity(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for block in iter(lambda:f.read(2**20),b''):h.update(block);n+=len(block)
 return n,h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--existing',type=Path);ap.add_argument('--destination',type=Path,default=ROOT/'common/Astra_PostB3_Empirical_Probe_20261021/data/WesselsSatija2023.h5ad');a=ap.parse_args();t=time.perf_counter()
 if a.existing:
  n,h=identity(a.existing)
  if(n,h)!=(SIZE,SHA):raise ValueError('existing input identity mismatch')
  print(json.dumps({'action':'verified existing; no download or copy','input':str(a.existing.resolve()),'bytes':n,'sha256':h,'wall_s':time.perf_counter()-t}));return
 p=a.destination
 if p.exists():
  if identity(p)!=(SIZE,SHA):raise ValueError('existing destination identity mismatch; will not overwrite')
  print(json.dumps({'action':'reused exact input','path':str(p.resolve())}));return
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.partial')
 try:
  with urllib.request.urlopen(URL,timeout=120) as r,tmp.open('xb') as f:
   while True:
    b=r.read(2**20)
    if not b:break
    f.write(b)
  n,h=identity(tmp)
  if(n,h)!=(SIZE,SHA):raise ValueError(f'input identity mismatch:{n},{h};partial preserved')
  os.replace(tmp,p)
 except Exception:raise
 print(json.dumps({'action':'downloaded and verified','url':URL,'path':str(p.resolve()),'bytes':n,'sha256':h,'wall_s':time.perf_counter()-t}))
if __name__=='__main__':main()
