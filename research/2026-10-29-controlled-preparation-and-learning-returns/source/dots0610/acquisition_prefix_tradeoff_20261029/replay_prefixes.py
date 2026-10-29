import contextlib,io,numpy as np,json,hashlib,sys
from pathlib import Path
here=Path(__file__).parent
src=Path(sys.argv[1] if len(sys.argv)>1 else 'producer-workspace/check_retained_memory_bank_v4.py')
text=src.read_text(); needle=' if step in [10000,100000,200000,1000000]:'
insert=" if step in [100,1000,10000,100000,1000000]:\n  saved_prefixes[step]={'sums':sums.copy(),'bath':bath.copy(),'lastparity':lastparity,'moments':moments.copy()}\n"
assert text.count(needle)==1;text=text.replace(needle,insert+needle)
ns={'__file__':str(src),'saved_prefixes':{}}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(text,str(src),'exec'),ns)
data={'U0':ns['Us'][0],'U1':ns['Us'][1],'O_diagnostic':ns['O'],'Jembed':ns['Jembed'],'P':ns['P']}
for n,r in ns['saved_prefixes'].items():
 for k,v in r.items():data[f'{k}_{n}']=v
np.savez(here/'prefix_bank.npz',**data)
print(json.dumps({'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'modification':'Added copy-only snapshots at declared prefixes; no changes to random calls, input/output settings, source evolution or learner counters.','prefixes':list(ns['saved_prefixes']),'last_diagnostic':ns['rows'][-1]},indent=2))
