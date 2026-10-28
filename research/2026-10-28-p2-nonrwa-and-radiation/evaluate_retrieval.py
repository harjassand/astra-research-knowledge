"""Reproducible source-informed rankings; full output retained privately,public traces bounded."""
import argparse,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from knowledge.retrieve import Library
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--baseline-root',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--full-output',type=Path,required=True);args=p.parse_args()
 lib=Library(args.baseline_root or ROOT,validate=False);spec=json.loads((BASE/'evaluation/PROBLEMS.json').read_bytes());public=[];full=[]
 for case in spec['cases']:
  rows=[];raw=[]
  target=lib.records.get(case['target']);families=set((target['parents'] or [target['id']])if target else [case['target'].split('-',1)[0]])
  for method in ('lexical','content','structured','agent'):
   started=time.monotonic();result=lib.search(case['query'],limit=5,method=method,**(dict(available=case['available'],unavailable=case['unavailable'])if method=='agent'else{}));hits=result['results']
   rank=lambda h:bool(families & set(lib.resolve(h['id'])['parents'] or[h['id']]))
   row=dict(method=method,seconds=round(time.monotonic()-started,3),exact_target_rank=next((i for i,h in enumerate(hits,1)if h['id']==case['target']),None),family_rank=next((i for i,h in enumerate(hits,1)if rank(h)),None))
   compact=[]
   for h in hits:
    item={k:v for k,v in h.items()if k in('id','title','kind','score','relevance_logit','ranking_view','ranking_text_truncated','source_match','next','packet','premise_check','notice_count','review_decisions')};compact.append(item)
   rows.append(dict(row,results=compact));raw.append(dict(row,results=hits))
  public.append(dict(case=case,methods=rows));full.append(dict(case=case,methods=raw));print(case['id'],[(m['method'],m['family_rank'],m['exact_target_rank'])for m in rows],flush=True)
 manifest=json.loads((lib.root/'knowledge/current/manifest.json').read_bytes());common=dict(exposure=spec['exposure'],input_version=manifest['input_version'],scope='All candidate identities/order and route/triage metadata retained publicly; full responses separately frozen. Timing excludes corpus loading/freshness startup; no applicability or proof decision from rank.')
 args.output.write_text(json.dumps(dict(common,results=public),ensure_ascii=False,indent=2)+'\n');args.full_output.write_text(json.dumps(dict(common,results=full),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
