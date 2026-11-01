"""Collective response enclosure from an acquired three-spin reference inverse.

Uniform microscopic clocks. Critical-scale equilibrium correlations. Non-Gaussian
kinetics at every site. No truncation of the target process. The reference inverse
on degree<=3 is closed exactly; floating sparse solutions are rational proposals
whose errors are bounded using an exact integer residual and an M-matrix bound.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from itertools import combinations
from fractions import Fraction as F
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu
from pathlib import Path
import json,time

def canonical(s,n):
    ss=tuple(s)
    return min(tuple(sorted((x-a)%n for x in ss)) for a in ss)

def xor(*sets):
    out=set()
    for s in sets:out.symmetric_difference_update(s)
    return sorted(out)

def corr_index(s,n):
    if not s:return 0
    assert len(s)%2==0
    d=sum(s[j+1]-s[j] for j in range(0,len(s),2))
    return min(d,n-d)

def build(n):
    if n<4:raise ValueError('n>=4')
    triples=sorted({canonical((0,a,b),n) for a,b in combinations(range(1,n),2)})
    index={s:i for i,s in enumerate(triples)}
    # e^(2J)=n -> tanhJ=(n-1)/(n+1), gamma=tanh2J=(n²-1)/(n²+1).
    den=2*(n*n+1);gamnum=n*n-1
    cols=[];rows=[];nums=[];columns=[]
    for col,s in enumerate(triples):
        tab={col:3*den}
        for i in s:
            for di in [-1,1]:
                target=xor(s,[i,(i+di)%n])
                if len(target)==3:
                    row=index[canonical(target,n)]
                    tab[row]=tab.get(row,0)-gamnum
        columns.append(tab)
        for row,value in tab.items():
            if value:rows.append(row);cols.append(col);nums.append(value)
    H=csc_matrix((np.array(nums,dtype=float)/den,(rows,cols)),shape=(len(triples),len(triples)))
    assert all(sum(tab.values())>=3*den-6*gamnum for tab in columns)
    # Every even-spin Gibbs moment has the same explicit integer denominator.
    small=[pow(n-1,k) for k in range(n+1)]
    big=[pow(n+1,k) for k in range(n+1)]
    cn=[small[d]*big[n-d]+small[n-d]*big[d] for d in range(n//2+1)]
    cden=big[n]+small[n]
    basis=[(0,)]+triples
    gm=[];gt=[]
    for s in basis:
        sm=0;st=0
        for shift in range(n):
            shifted=[(v+shift)%n for v in s]
            sm+=cn[corr_index(xor((0,),shifted),n)]
            st+=cn[corr_index(xor((n-1,0,1),shifted),n)]
        gm.append(n*sm);gt.append(n*st)
    ti=index[canonical((n-1,0,1),n)]
    assert gm[ti+1]==gt[0]
    return dict(n=n,triples=triples,index=index,H=H,columns=columns,den=den,
                gm=gm,gt=gt,cden=cden,ti=ti)

def exact_residual(problem,xnum,bits):
    dim=len(xnum);scale=1<<bits;den=problem['den']
    rn=[0]*dim;rn[problem['ti']]=den*scale
    for j,tab in enumerate(problem['columns']):
        for i,c in tab.items():rn[i]-=c*xnum[j]
    return rn

def solve(n,same=F(1),opposite=F(2),bits=100,refinements=2):
    start=time.perf_counter();p=build(n);built=time.perf_counter()
    dim=len(p['triples']);rhs=np.zeros(dim);rhs[p['ti']]=1
    lu=splu(p['H']);x=lu.solve(rhs);scale=1<<bits
    xnum=[round(float(v)*scale) for v in x]
    for _ in range(refinements):
        rn=exact_residual(p,xnum,bits)
        r=np.array([float(F(z,p['den']*scale)) for z in rn])
        dx=lu.solve(r)
        xnum=[a+round(float(v)*scale) for a,v in zip(xnum,dx)]
    rn=exact_residual(p,xnum,bits)
    res1=F(sum(abs(z) for z in rn),p['den']*scale)
    gamma=F(n*n-1,n*n+1);a0=(same+opposite)/2;a1=(same-opposite)/2
    km=a0-gamma*same;kt=a1
    gmm=F(p['gm'][0],p['cden']);gmt=F(p['gt'][0],p['cden'])
    energy=km*gmm+kt*gmt;trialscale=gmm/energy
    lower=gmm*trialscale;alpha=gmt/gmm;rt=-trialscale*kt
    # Cov(T-alpha M,F_S), common rational denominator.
    gn=[p['gt'][j+1]*p['gm'][0]-p['gt'][0]*p['gm'][j+1] for j in range(dim)]
    gd=p['cden']*p['gm'][0]
    approx=F(sum(a*b for a,b in zip(gn,xnum)),gd*scale)
    inverse_one_bound=1/(3*(1-gamma))
    err=F(max(abs(a) for a in gn),gd)*res1*inverse_one_bound
    residual_upper=rt*rt*max(approx+err,F(0))
    upper=lower+residual_upper/min(same,opposite)
    reference=gmm/(1-gamma)
    return dict(n=n,states=f'2^{n}',triple_orbits=dim,betaJ=f'0.5 log({n})',
        same=str(same),opposite=str(opposite),gamma=str(gamma),
        variance=float(gmm),dirichlet_energy=float(energy),
        lower=float(lower),upper=float(upper),relative_width=float((upper-lower)/lower),
        lower_fraction=[str(lower.numerator),str(lower.denominator)],
        upper_fraction=[str(upper.numerator),str(upper.denominator)],
        reference_response=float(reference),lower_over_reference=float(lower/reference),
        expected_diffusion_limit_ratio=float(1/opposite),
        residual_reference_norm_upper=float(residual_upper),
        reference_inverse_scalar_estimate=float(approx),
        exact_scalar_error_bound=float(err),integer_residual_one_norm=float(res1),
        scalar_proposal_relative_error_bound=float(err/abs(approx)) if approx else None,
        rational_proposal_bits=bits,refinements=refinements,
        build_seconds=built-start,total_seconds=time.perf_counter()-start,
        status='exact rational endpoint enclosure; sparse floating solve only proposes a rational vector')

if __name__=='__main__':
    out=[]
    for n in [8,16,32,64,128]:
        result=solve(n);out.append(result)
        print(n,result['triple_orbits'],result['relative_width'],result['total_seconds'],flush=True)
        Path(__file__).with_name('critical_response_results.json').write_text(json.dumps(out,indent=2)+'\n')
