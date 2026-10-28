"""Full input generation + exact operator + independent scalar verification.

Constructed algebraic fixtures, not samples or acquired physical models.
"""
from pathlib import Path
from fractions import Fraction as F
from random import Random
import json,time,resource,sys
START=time.monotonic()
from box_compiler import compile_box,verify_certificate,exhaustive_max,from_branch_data
OUT=Path(__file__).resolve().parent
def make_case(k,seed,kind):
    rng=Random(seed);weights=[rng.randrange(1,33) for _ in range(k)];total=sum(weights)
    P=[F(x,total) for x in weights];mid=[];ell=[];up=[];B=[]
    for i in range(k):
        m=rng.randrange(256,769)
        w=(min(m,1024-m)*9//10) if kind=='heterogeneous_width' and i%97==0 else rng.randrange(1,8)
        mid.append(F(m,1024));ell.append(F(m-w,1024));up.append(F(m+w,1024))
        B.append(F(1) if kind=='heterogeneous_width' else 1+F(rng.randrange(0,33),1024))
    Z=sum((p*m for p,m in zip(P,mid)),F(0));q=[p*m/Z for p,m in zip(P,mid)]
    lo,hi,r=from_branch_data(P,q,B,ell,up)
    return lo,hi,r,{'P':P,'q':q,'B':B,'ell':ell,'up':up}
def encode(z):
    if isinstance(z,F):return str(z)
    if isinstance(z,dict):return {k:encode(v) for k,v in z.items()}
    if isinstance(z,(tuple,list)):return [encode(v) for v in z]
    return z
rows=[]
specs=[(k,20261028+k,t) for k in [2,3,5,8,12,16] for t in ['narrow','heterogeneous_width']]
specs +=[(1024,115,'narrow'),(4096,116,'heterogeneous_width'),(10000,117,'narrow'),(100000,118,'heterogeneous_width')]
for k,seed,kind in specs:
    start=time.monotonic();lo,hi,r,branch=make_case(k,seed,kind);input_time=time.monotonic()-start
    start=time.monotonic();cert=compile_box(lo,hi,r);compile_time=time.monotonic()-start
    start=time.monotonic();verify_certificate(lo,hi,r,cert);verify_time=time.monotonic()-start
    true=None;brute_time=None
    if k<=16:
        start=time.monotonic();true=exhaustive_max(lo,hi,r);brute_time=time.monotonic()-start
        assert cert['lower']<=true<=cert['upper']
    # Ordinary global Kantorovich bound, after w_i=q_i xi_i.
    xi_lo=min(p*l/q for p,l,q in zip(branch['P'],branch['ell'],branch['q']))
    xi_hi=max(p*u/q for p,u,q in zip(branch['P'],branch['up'],branch['q']))
    kantorovich=max(branch['B'])*(xi_lo+xi_hi)**2/(4*xi_lo*xi_hi)
    row={'k':k,'seed':seed,'kind':kind,'lower':str(cert['lower']),'upper':str(cert['upper']),
         'upper_relative_to_lower_minus1':float(cert['upper']/cert['lower']-1),
         'quadratic_rounding_factor':str(cert['factor']),'display_upper':float(cert['upper']),
         'ordinary_Kantorovich':str(kantorovich),'display_Kantorovich':float(kantorovich),
         'exact_corner_max':str(true) if true is not None else None,
         'times':{'input_generation':input_time,'exact_compilation':compile_time,'linear_verification':verify_time,'exhaustive':brute_time}}
    rows.append(row);print(json.dumps({k:row[k] for k in ['k','kind','display_upper','upper_relative_to_lower_minus1','times']}),flush=True)
    if k in [16,4096,100000]:
        name=f'{k}_{kind}'
        if k!=100000:
            (OUT/f'INPUT_{name}.json').write_text(json.dumps(encode({'lo':lo,'hi':hi,'r':r,'branch':branch}),separators=(',',':'))+'\n')
        (OUT/f'CERT_{name}.json').write_text(json.dumps(encode(cert),separators=(',',':'))+'\n')
result={'status':'EXACT_FINITE_INPUT_OPERATOR_ACQUIRED','cases':rows,'module_seconds':time.monotonic()-START,
        'maxrss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'platform':sys.platform,
        'scope':'Explicit rational-box operation. No continuation enclosure acquisition, unknown-model inference, end-to-end rare-event speedup or novelty established.'}
(OUT/'OPERATOR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
