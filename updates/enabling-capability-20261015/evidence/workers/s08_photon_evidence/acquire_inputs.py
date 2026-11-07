"""Acquire or verify the immutable actual photon archive; never generates data."""
import argparse,hashlib,json,time,urllib.request
from pathlib import Path
URL='https://ndownloader.figshare.com/files/7428508'
SHA='5e94165fa89350d67be5a3b5987f20844fbb97adeb5373b513dc65146ef0944a'
SIZE=34749720
p=argparse.ArgumentParser();p.add_argument('--archive',default='/tmp/astra_premise_quantum_data.zip');a=p.parse_args()
path=Path(a.archive);start=time.perf_counter();downloaded=False
if not path.exists():
 temp=path.with_name(path.name+'.part');path.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(URL,timeout=60) as response,temp.open('wb') as output:
  while True:
   part=response.read(1024*1024)
   if not part:break
   output.write(part)
 if temp.stat().st_size!=SIZE or hashlib.sha256(temp.read_bytes()).hexdigest()!=SHA:
  raise ValueError('Input checksum mismatch; .part preserved for diagnosis')
 temp.replace(path);downloaded=True
b=path.read_bytes()
if len(b)!=SIZE or hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Existing archive checksum mismatch')
print(json.dumps(dict(url=URL,path=str(path),sha256=SHA,bytes=SIZE,downloaded_now=downloaded,elapsed_seconds=time.perf_counter()-start),indent=2))
