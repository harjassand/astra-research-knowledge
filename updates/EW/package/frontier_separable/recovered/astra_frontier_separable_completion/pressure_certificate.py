"""Exact rational infinite-domain Hodge certificate. All tails are summed.
Target is energy of b=delta_(0,1)-delta_(1,0), NOT full transport D.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from pressure_basis import *
from pathlib import Path
import argparse,platform,resource,sys,json
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING

def fracstr(x): return f'{x.numerator}/{x.denominator}'

def outward(x,places,up):
    with localcontext() as ctx:
        ctx.prec=100; ctx.rounding=ROUND_CEILING if up else ROUND_FLOOR
        v=Decimal(x.numerator)/Decimal(x.denominator)
        return str(v.quantize(Decimal(1).scaleb(-places)))

def bilinear(x,M,y):
    return sum((xi*sum((a*yj for a,yj in zip(row,y) if yj),F(0)) for xi,row in zip(x,M) if xi),F(0))

def certify(L,K,denom_bits=52,witness=None):
    start=time.perf_counter()
    if witness is None:
        rec,x,y=run(L,K); den=2**denom_bits
        xr=[F(int(round(float(a)*den)),den) for a in x]
        yr=[F(int(round(float(a)*den)),den) for a in y]
    else:
        rec=None; xr=list(map(F,witness['potential_coefficients']));yr=list(map(F,witness['cycle_coefficients']))
    G,H,rhs,vb,pp,cp=make_gram(*matrices(build_unis(L,K),True),exact=True)
    if len(xr)!=len(pp) or len(yr)!=len(cp): raise ValueError('Wrong witness dimensions')
    lo=2*sum(a*b for a,b in zip(rhs,xr))-bilinear(xr,G,xr)
    hi=1+2*sum(a*b for a,b in zip(vb,yr))+bilinear(yr,H,yr)
    gap=hi-lo
    assert 0<=lo<=hi<=1
    unis=build_unis(L,K)
    def einner(a,b):
        return sum(c*C*ip(u,U)*ip(v,V) for c,u,v in a for C,U,V in b)
    def forward(s):
        a,q=s
        return [(F(1),(a-1,q))] if a else ([(q,s)] if q else [])
    def sh(s): return (s[0]+1,s[1])
    def gradient(ij):
        out=[[],[],[]]
        for c,i,j in terms(ij,True):
            u,v=unis[i],unis[j]
            out[0].append((F(c),u,v));out[1].append((F(c),u,v))
            for cf,U in forward(u):
                out[0].append((-c*cf,U,v));out[2].append((-c*cf,U,v))
            for cf,V in forward(v):
                out[1].append((-c*cf,u,V));out[2].append((c*cf,u,V))
        return out
    def face(ij,t):
        out=[[],[],[]]
        for c,i,j in terms(ij,False):
            u,v=unis[i],unis[j]
            out[0].append((F(c),u,sh(v) if t else v))
            out[1].append((F(-c),sh(u) if t else u,v))
            out[2].append((F(-c),u,v))
        return out
    crosschecks=0
    for a in sorted(set([0,len(pp)//3,2*len(pp)//3,len(pp)-1])):
        gd=gradient(pp[a])
        for b in sorted(set([0,1,len(cp)//3,len(cp)//2,len(cp)-1])):
            fc=face(*cp[b]); assert sum(einner(fc[e],gd[e]) for e in range(3))==0;crosschecks+=1
    # Direct whole-residual contraction, independent of assembled Gram matrices.
    grad=[[],[],[]];flow=[[],[],[(F(1),geo(0),geo(0))]]
    for a,c in zip(pp,xr):
        if c:
            for e,part in enumerate(gradient(a)):
                grad[e].extend((c*v,u,w) for v,u,w in part)
    for (a,t),c in zip(cp,yr):
        if c:
            for e,part in enumerate(face(a,t)):
                flow[e].extend((c*v,u,w) for v,u,w in part)
    def collect(part):
        from collections import defaultdict
        r=defaultdict(F)
        for c,u,v in part:r[u,v]+=c
        return [(c,u,v) for (u,v),c in r.items() if c]
    residual=[collect(flow[e]+[(-c,u,v) for c,u,v in grad[e]]) for e in range(3)]
    residual_norm=sum(einner(r,r) for r in residual)
    assert residual_norm==gap
    record=dict(status='exact rational infinite-domain variational enclosure; no external review',L=L,K=K,
       lower=fracstr(lo),upper=fracstr(hi),width=fracstr(gap),outward_lower=outward(lo,14,False),
       outward_upper=outward(hi,14,True),width_float=float(gap),potential_variables=len(xr),cycle_variables=len(yr),
       residual_atoms=sum(map(len,residual)),max_pole=str(max(q for a,q in unis)),
       total_seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       exact_crosschecks=crosschecks,whole_residual_identity=True,denominator_bits=denom_bits,
       discovery=rec,Python=sys.version,platform=platform.platform(),
       scope='Unit-source Hodge projection energy, not the full interacting transport coefficient')
    witness=dict(L=L,K=K,denominator_bits=denom_bits,
        potential_coefficients=[fracstr(c) for c in xr],cycle_coefficients=[fracstr(c) for c in yr])
    return record,witness

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--L',type=int,default=10);ap.add_argument('--K',type=int,default=6)
    ap.add_argument('--verify',type=str);args=ap.parse_args()
    saved=json.loads(Path(args.verify).read_text()) if args.verify else None
    L,K=(saved['L'],saved['K']) if saved else (args.L,args.K)
    result,witness=certify(L,K,witness=saved)
    stem=f'pressure_L{L}K{K}'
    if not saved:
        Path(stem+'_certificate.json').write_text(json.dumps(result,indent=2))
        Path(stem+'_witness.json').write_text(json.dumps(witness,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in('lower','upper','width')},indent=2))
