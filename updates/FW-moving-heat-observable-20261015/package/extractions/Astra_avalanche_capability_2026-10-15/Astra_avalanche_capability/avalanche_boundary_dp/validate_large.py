import pathlib,subprocess,random,mpmath as mp,json,time,numpy as np
from boundary_dp import mean_quad
b=pathlib.Path(__file__).parent
(b/'exp_probe.cpp').write_text('#define main certificate_main\n#include "large_certificate.cpp"\n#undef main\nint main(){while(std::cin){U l=readU();if(!std::cin)break;I a=exwide(l,l);std::cout<<a.l<<" "<<a.h<<"\\n";}}\n')
subprocess.run(['g++','-O3','-std=c++17',str(b/'exp_probe.cpp'),'-o',str(b/'exp_probe')],check=True)
M=1<<60;random.seed(1234);xs=[0,1,M//2,M,M*16-1,M*16,M*64-1,M*64]+[random.randrange(M*70) for _ in range(3000)]
r=subprocess.run([str(b/'exp_probe')],input=''.join(str(x)+'\n' for x in xs),capture_output=True,text=True,check=True)
mp.mp.dps=100
for x,row in zip(xs,r.stdout.splitlines()):
 l,h=map(int,row.split());v=mp.exp(-mp.mpf(x)/M);assert mp.mpf(l)/M<=v<=mp.mpf(h)/M,(x,l,h,v)
res={'exp_tests':len(xs),'exp_precision':100,'mean_comparisons':[]}
for n,kind in [(100,'moderate'),(400,'moderate'),(100,'author'),(400,'author')]:
 s=np.sort(np.random.RandomState(0).rand(n));F=n*(.175 if kind=='moderate' else .125);T=.15 if kind=='moderate' else .05
 t=time.perf_counter();q=mean_quad(s,F,T);cert=json.loads((b/f'large_result_{n}_{kind}.json').read_text());assert cert['lower']<=q['mean']<=cert['upper'];res['mean_comparisons'].append(dict(n=n,kind=kind,reference=q,reference_seconds=time.perf_counter()-t))
(b/'large_validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
