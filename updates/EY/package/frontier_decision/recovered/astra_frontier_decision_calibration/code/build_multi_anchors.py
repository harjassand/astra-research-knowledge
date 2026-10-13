from multi_solver import run
from multi_certificate import round_file
from fast_algebra import basis
from pathlib import Path
import sys,time,json,resource
root=Path(sys.argv[1]);root.mkdir(exist_ok=True,parents=True);start=time.perf_counter();fw=basis(8,1);gw=basis(8,0);results=[]
for V in [0.,.5,1.,1.5,2.75,3.]:
 name=root/('V'+str(V).replace('.','p'));a=run(fw,gw,name,3,V=V)
 b=round_file(str(name)+'.npz',str(name)+'_exact',34)
 results.append(dict(V=V,solver_seconds=a['total_seconds'],verify_seconds=b['verification_seconds']))
(root/'benchmark.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start,records=results,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
