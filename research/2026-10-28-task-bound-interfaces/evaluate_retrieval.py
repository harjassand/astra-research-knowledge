"""Fixed, source-informed use problems outside implementation fixtures."""
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from knowledge.retrieve import Library
BASE=Path(__file__).resolve().parent

def main():
 lib=Library(validate=False)
 spec=json.loads((BASE/'evaluation/FRESH_PROBLEMS.json').read_bytes())
 rows=[]
 for case in spec['cases']:
  methods=[]
  for method in ('lexical','content','structured','agent'):
   started=time.monotonic();result=lib.search(case['query'],method=method,limit=5)
   # Retain full returned candidates, failed routes and all qualification data.
   methods.append(dict(method=method,seconds=round(time.monotonic()-started,3),results=result['results']))
  from collections import defaultdict
  scores=defaultdict(float)
  for lane in ('structured','content'):
   for rank,hit in enumerate(lib.search(case['query'],method=lane,limit=8)['results'],1):scores[hit['id']]+=1/(60+rank)
  portable_ids=sorted(scores,key=lambda identifier:(-scores[identifier],identifier))[:5]
  rows.append(dict(case=case,methods=methods,portable_production_rrf_ids=portable_ids))
  print(case['id'],[(m['method'],[x['id'] for x in m['results']]) for m in methods],flush=True)
 manifest=json.loads((ROOT/'knowledge/current/manifest.json').read_bytes())
 output=dict(exposure=spec['exposure'],development_disclosure='F03 exposed a source-qualification ambiguity during development. Its question was not retuned; the adapter was clarified. This is a source-informed development comparison, not a blind or untouched held-out experiment.',input_version=manifest['input_version'],results=rows)
 (BASE/'evaluation/FRESH_CURRENT_RESULTS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
