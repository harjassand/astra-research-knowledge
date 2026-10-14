#!/usr/bin/env python3
"""Discovery search allowing independently optimized positive strip widths.

Continuous minimization is floating discovery only. Any returned cycle is
reconstructed with rational widths and exact Fraction arithmetic before it is
reported as a mathematical candidate.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, sys
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import add,scale,mul,cos,sin,meanprod,poly_terms,edge_coeffs,edge_value,r,s,p,q

def energy(n,m,lam=Q(1,10)):
    a=add(scale(cos(n),p),scale(cos(m),q)); c=add(scale(sin(n),p),scale(sin(m),q))
    b=add(scale(sin(n),-n*r),scale(sin(m),-m*s)); d=add(scale(cos(n),n*r),scale(cos(m),m*s))
    u=add(mul(a,a),mul(c,c)); v=add(mul(b,b),mul(d,d)); w=add(mul(a,b),mul(c,d)); det=add(mul(a,d),scale(mul(b,c),-1))
    F=meanprod(u,u)+meanprod(v,v)+4*meanprod(w,w)+(Q(7,2)-lam)*meanprod(det,det)-Q(29,10)*meanprod(det,add(u,v))
    return poly_terms(F)

def optimum(terms,a,b):
    co=edge_coeffs(terms,a,b)
    if all(v==0 for v in co[2:]):
        # A stationary profile has W(tau)=c0*tau+c1, so its infimum is
        # c1 at tau->0 when c0>0; a positive rational width is restored
        # during exact cycle reconstruction.
        tau=1e-12 if co[0]>0 else 1.0
        return co,tau,float(co[1])+float(co[0])*tau
    c0,c1,c2,c3,c4=map(float,co)
    # W'(tau) has the sign of this quartic. Rank-one convexity makes W
    # convex, so its positive stationary root is its global minimum.
    def g(t): return c0*t**4-c2*t**2-2*c3*t-3*c4
    lo=hi=1.0
    for _ in range(100):
        if g(lo)<=0: break
        lo*=0.5
    for _ in range(100):
        if g(hi)>=0: break
        hi*=2
    if g(lo)>0 or g(hi)<0:
        raise RuntimeError(f'could not bracket timing root: {co}, g={g(lo),g(hi)}')
    tau=brentq(g,lo,hi,xtol=5e-15,rtol=1e-14)
    value=c0*tau+c1+c2/tau+c3/tau**2+c4/tau**3
    return co,tau,value

def run(n,m,low=Q(0),high=Q(2),step=Q(1,4),lam=Q(1,10)):
    axis=[]; t=Q(low)
    while t<=high: axis.append(t);t+=step
    V=[(x,y) for x in axis for y in axis]; terms=energy(n,m,lam)
    edges={}; count=0
    finite_potential=None
    if low==0 and high==2 and step==Q(1,4):
        path=ROOT/f'exact_cycle_search_{lam.numerator}_{lam.denominator}.json'
        recorded=json.loads(path.read_text()) if path.exists() else []
        match=next((x for x in recorded if x['carriers']==[n,m] and x['profile_box']==['0','2']),None)
        if match and 'potential' in match:
            finite_potential=[float(Q(v)) for v in match['potential']]
    finite_slacks=[]
    for i,a in enumerate(V):
        for j,b in enumerate(V):
            co,tau,val=optimum(terms,a,b)
            edges[i,j]=(val,tau,co); count+=1
            if finite_potential is not None:
                finite_slacks.append((val+finite_potential[i]-finite_potential[j],i,j,tau))
    d=[0.0]*len(V); pred=[None]*len(V); changed=None
    for it in range(len(V)):
        changed=None
        for (i,j),(val,tau,co) in edges.items():
            cand=d[i]+val
            if cand<d[j]-1e-9:
                d[j]=cand;pred[j]=(i,tau,co,val);changed=j
        if changed is None: break
    if changed is None:
        out={'kind':'NO_NUMERICAL_NEGATIVE_CYCLE','passes':it+1,
             'minimum_relaxed_slack':min(v+d[i]-d[j] for (i,j),(v,*_) in edges.items())}
    else:
        v=changed
        for _ in V: v=pred[v][0]
        start=v; rev=[]
        while True:
            i,tau,co,val=pred[v];rev.append((i,v,tau,co,val));v=i
            if v==start: break
            assert len(rev)<=len(V)+1
        cyc=list(reversed(rev))
        exact=None; exact_edges=None
        for den in [10**4,10**5,10**6,10**7,10**8]:
            recon=[]; total=Q(0)
            for i,j,tau,co,_ in cyc:
                h=Q(tau).limit_denominator(den)
                if h<=0: h=Q(1,10**9)
                cost=edge_value(co,h)
                recon.append((i,j,h,cost));total+=cost
            if total<0: exact,exact_edges=total,recon;break
        out={'kind':'NEGATIVE_NUMERICAL_CYCLE', 'passes':len(V),
             'numerical_weight':sum(e[4] for e in cyc),
             'rational_reconstruction_exact_weight':str(exact) if exact is not None else None,
             'rational_cycle':[[i,j,str(h),str(cost)] for i,j,h,cost in exact_edges] if exact_edges else None}
    extra={}
    if finite_slacks:
        slack,i,j,tau=min(finite_slacks)
        extra={'finite_width_potential_min_continuous_slack_approx':slack,
               'continuous_violation_edges_approx':sum(v[0]<-1e-8 for v in finite_slacks),
               'worst_continuous_width_edge_approx':{'from':list(map(str,V[i])),'to':list(map(str,V[j])),'tau':tau}}
    return {'carriers':[n,m], 'profile_box':[str(low),str(high)],'step':str(step),
            'vertex_count':len(V),'directed_pair_count':count,
            'continuous_width_scope':'per-edge infimum located numerically; exact only if rational cycle reconstruction succeeds',**extra,**out}

if __name__=='__main__':
    results=[]
    lam=Q(sys.argv[1]) if len(sys.argv)>1 else Q(1,10)
    for n,m,lo,hi,st in [(1,-1,Q(0),Q(2),Q(1,4)),(1,3,Q(0),Q(2),Q(1,4)),
                         (1,-3,Q(0),Q(2),Q(1,4)),(3,-1,Q(0),Q(2),Q(1,4)),
                         (1,-1,Q(-2),Q(2),Q(1,2)),(1,3,Q(-2),Q(2),Q(1,2)),
                         (1,-3,Q(-2),Q(2),Q(1,2))]:
        result=run(n,m,lo,hi,st,lam);results.append(result)
        print(json.dumps(result,indent=2),flush=True)
    out=ROOT/f'continuous_timing_search_{lam.numerator}_{lam.denominator}.json'
    out.write_text(json.dumps(results,indent=2)+'\n')
    if lam==Q(1,10): (ROOT/'continuous_timing_search.json').write_text(json.dumps(results,indent=2)+'\n')
