#!/usr/bin/env python3
"""Check exact supplied/selected payload bytes in Git index or a revision.

This checks repository integrity, never scientific truth.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path

PREFIX='updates/FX-global-completion-axis-20261015/'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--revision',default='INDEX');p.add_argument('--output',type=Path);a=p.parse_args()
 root=Path(__file__).resolve().parents[2]
 original=json.loads((root/PREFIX/'SOURCE_MANIFEST.json').read_bytes())
 freeze=json.loads((root/PREFIX/'SELECTED_FREEZE.v0001.json').read_bytes())
 refs=original['files']+freeze['files']
 refs += [{'path':PREFIX+'SOURCE_MANIFEST.json','sha256':hashlib.sha256((root/PREFIX/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()}, {'path':PREFIX+'SELECTED_FREEZE.v0001.json','sha256':hashlib.sha256((root/PREFIX/'SELECTED_FREEZE.v0001.json').read_bytes()).hexdigest()}]
 names=[(':'+x['path']) if a.revision=='INDEX' else a.revision+':'+x['path'] for x in refs]
 raw=subprocess.check_output(['git','-C',str(root),'cat-file','--batch'],input=('\n'.join(names)+'\n').encode());offset=0;checked=[]
 for item in refs:
  end=raw.index(b'\n',offset);head=raw[offset:end].split();offset=end+1
  assert len(head)==3 and head[1]==b'blob',(item['path'],head)
  n=int(head[2]);blob=raw[offset:offset+n];offset+=n+1
  assert raw[offset-1:offset]==b'\n'
  h=hashlib.sha256(blob).hexdigest();assert h==item['sha256'],item['path']
  if 'bytes' in item:assert len(blob)==item['bytes'],item['path']
  checked.append({'path':item['path'],'sha256':h,'bytes':n})
 assert offset==len(raw)
 out={'schema':'astra.fx-git-payload-check.v1','revision':a.revision,'status':'PASS','supplied_original_files':len(original['files']),'selected_derived_files':len(freeze['files']),'manifest_files':2,'checked_files':len(checked),'payloads':checked,'scope':'Git blob SHA256/byte identity only; no mathematical, novelty or physical validation.'}
 data=json.dumps(out,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(data)
 print(json.dumps({k:v for k,v in out.items() if k!='payloads'}))
if __name__=='__main__':main()
