"""Compare fixed source-informed use questions; never execute archived programs."""
import argparse
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from knowledge.retrieve import Library
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--baseline-root',type=Path);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 lib=Library(root=args.baseline_root or ROOT,validate=False)
 spec=json.loads((BASE/'evaluation/PROBLEMS.json').read_bytes());rows=[]
 for case in spec['cases']:
  lanes=[]
  for method in ('lexical','content','structured','agent'):
   started=time.monotonic()
   result=lib.search(case['query'],limit=5,method=method,**(dict(available=case['available'],unavailable=case['unavailable']) if method=='agent' else {}))
   hits=result['results'];target=case['target']
   lanes.append(dict(method=method,seconds=round(time.monotonic()-started,3),exact_unit_rank=next((i for i,h in enumerate(hits,1) if h['id']==target),None),family_rank=next((i for i,h in enumerate(hits,1) if h['id']==target or 'N1126-quadratic-wave-current-and-window-cost' in lib.resolve(h['id'])['parents'] or h['id']=='N1126-quadratic-wave-current-and-window-cost'),None),results=hits))
  rows.append(dict(case=case,methods=lanes));print(case['id'],[(x['method'],x['family_rank'],x['exact_unit_rank']) for x in lanes],flush=True)
 m=json.loads((lib.root/'knowledge/current/manifest.json').read_bytes())
 args.output.write_text(json.dumps(dict(exposure=spec['exposure'],input_version=m['input_version'],scope='Ranks are relevance/navigation, not proof or compatibility. Timing excludes corpus loading/freshness startup; first neural call includes model initialization.',results=rows),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
