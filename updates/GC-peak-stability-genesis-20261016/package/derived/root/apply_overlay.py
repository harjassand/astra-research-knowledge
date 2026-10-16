#!/usr/bin/env python3
"""Apply a reviewed create-only overlay and append deltas after exact pin checks."""
from pathlib import Path
import argparse,hashlib,json,subprocess
h=lambda b:hashlib.sha256(b).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--stage',type=Path,required=True);a.add_argument('--receipt',type=Path,required=True);args=a.parse_args();w=args.repo.resolve();stage=args.stage.resolve();p=json.loads((stage/'PLAN.json').read_text())
 assert not args.receipt.exists()
 head=subprocess.check_output(['git','-C',str(w),'rev-parse','HEAD'],text=True).strip();assert head==p['pins']['expected_branch_head']
 assert not subprocess.check_output(['git','-C',str(w),'status','--porcelain'],text=True).strip()
 for name,dig in p['staged_files'].items():assert h((stage/name).read_bytes())==dig,name
 for name,dig in p['base_registry_sha256'].items():assert h((w/name).read_bytes())==dig,name
 writes={}
 for f in (stage/'overlay').rglob('*'):
  if f.is_file():
   rel=str(f.relative_to(stage/'overlay'));assert not (w/rel).exists(),rel;writes[rel]=f.read_bytes()
 for f in (stage/'additions').rglob('*'):
  if not f.is_file():continue
  rel=str(f.relative_to(stage/'additions'));old=(w/rel).read_bytes();delta=f.read_bytes()
  if f.suffix=='.jsonl':
   assert old.endswith(b'\n');writes[rel]=old+delta
  else:
   obj=json.loads(old);d=json.loads(delta)
   if isinstance(obj,list):assert isinstance(d,list);obj.extend(d)
   elif rel=='indexes/query_aliases.json':
    assert not (obj.keys()&d.keys());obj.update(d)
   else:
    for key,values in d.items():assert isinstance(obj[key],list) and isinstance(values,list);obj[key].extend(values)
   # Keep historical insertion order and format; never sort old registry keys.
   writes[rel]=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
 for rel,b in writes.items():
  q=(w/rel).resolve();assert q.is_relative_to(w);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 for rel,b in writes.items():assert (w/rel).read_bytes()==b
 args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps({'status':'APPLIED_REVIEWED_OVERLAY','head_before':head,'stage_plan_sha256':h((stage/'PLAN.json').read_bytes()),'files_written':{rel:h(b) for rel,b in writes.items()},'boundary':'Git/source/registry integrity only; scientific statuses unchanged.'},indent=2)+'\n')
 print(json.dumps({'files_written':len(writes),'receipt':str(args.receipt)}))
if __name__=='__main__':main()
