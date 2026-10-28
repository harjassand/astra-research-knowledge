from pathlib import Path
import json,sys,time
from knowledge.retrieve import Library
here=Path(__file__).resolve().parent
cases=json.loads((here/'evaluation/PROBLEMS.json').read_bytes())
library=Library()
rows=[]
for case in cases['cases']:
    methods=[]
    for method in ('content','structured','agent'):
        start=time.monotonic()
        hits=library.search(case['query'],limit=5,method=method)
        methods.append(dict(method=method,elapsed_seconds=time.monotonic()-start,
                            results=hits['results'] if isinstance(hits,dict) else hits,
                            response_metadata={k:v for k,v in hits.items()if k!='results'} if isinstance(hits,dict) else {}))
    rows.append(dict(case=case,methods=methods))
out=dict(exposure=cases['exposure'],input_version=library.manifest['input_version'],results=rows)
(here/'evaluation'/sys.argv[1]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print([(r['case']['id'],[(m['method'],[h['id']for h in m['results']])for m in r['methods']])for r in rows])
