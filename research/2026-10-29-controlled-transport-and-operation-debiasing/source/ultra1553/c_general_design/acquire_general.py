"""One tall-source acquisition; numerical SDP is only a proposal.

No core22 imports/writes, no side-information sample or physical data.
All Choi identities, primal signs and global lower-bound signs are rational.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,resource,time
START=time.perf_counter()
import numpy as np
import sympy as sp
import cvxpy as cp
IMPORT_SECONDS=time.perf_counter()-START
from fisher_pencils import (source_coefficients,target_coefficients,linear_system,
    zeros,eye,encode,decode,phi,minus,pack,unpack,upper_coords,quadratic_matrix,
    ldl_positive,matvec,baseline,trace_product,min_floor_columns)
ROOT=Path(__file__).resolve().parent


def rnd(x,bits=42): return F(round(float(x)*(1<<bits)),1<<bits)


def symrows(M):return sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in row] for row in M])


def fraction(x):return F(int(x.p),int(x.q))


def positive_shift(M,bits=38):
    """Add a rational diagonal until exact LDL proves positivity."""
    d=F(1,1<<bits);trials=[]
    while True:
        T=[[x+(d if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(M)]
        ok,receipt=ldl_positive(T);trials.append({'shift':str(d),'passed':ok})
        if ok:return T,d,receipt,trials
        d*=2


def main():
    run=time.perf_counter();phase={}
    L=decode([['3/5','1/5'],['1/5','3/5'],['1/5','1/5']])
    n,ell,m=2,3,3;c=F(1,2);kappa=F(1,1000);f=m+1
    values=[F(0),F(1,2),F(1)]
    cost=[[(y-F(i))**2/n for i in range(n)] for y in values]
    source,Ar,br,specs=linear_system(L,m);e=len(source[0][1]);d=e*f
    coords=upper_coords(d);nc=len(coords);nv=nc+m*n
    C0,K0,R0=baseline(L,m,c);v0=pack(C0,K0)
    assert matvec(Ar,v0)==br
    source_record={'scope':'constructed tall positive reference; no acquired population channel',
        'L':encode(L),'budget':str(c),'entry_floor':str(kappa),'cost':encode(cost),
        'target_values':list(map(str,values)),'n':n,'ell':ell,'m':m,
        'source_order':e,'target_order':f,'Choi_order':d}
    (ROOT/'SOURCE.json').write_text(json.dumps(source_record,indent=2)+'\n')
    phase['compile_seconds']=time.perf_counter()-run
    tick=time.perf_counter()
    C=cp.Variable((d,d),symmetric=True);K=cp.Variable((m,n))
    vec=cp.hstack([C[i,j] for i,j in coords]+[K[y,i] for y in range(m) for i in range(n)])
    Afloat=np.array([[float(x) for x in row] for row in Ar]);bfloat=np.array(br,dtype=float)
    eq=(Afloat@vec==bfloat)
    # A0 is diagonal; exact formula is reused by the rational receiver.
    AA=source[0][1]
    ph0=sum(float(AA[a][a])*C[a*f:(a+1)*f,a*f:(a+1)*f] for a in range(e))
    B0=cp.diag(cp.hstack([cp.sum(K[y,:])/n for y in range(m)]+[float(c)]))
    R=B0-ph0;conR=(R>>0)
    constraints=[C>>0,conR,eq,K>=float(kappa)]
    obj=cp.sum(cp.multiply(np.array(cost,dtype=float),K))
    prob=cp.Problem(cp.Minimize(obj),constraints)
    prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_feas=1e-10,tol_gap_rel=1e-10,max_iter=250)
    phase['numerical_seconds']=time.perf_counter()-tick
    if C.value is None or K.value is None:raise RuntimeError('NO_PROPOSAL '+str(prob.status))
    proposal={'status':prob.status,'cost':float(prob.value),'K':K.value.tolist(),
        'C':C.value.tolist(),'dual_R':conR.dual_value.tolist(),'dual_equalities':eq.dual_value.tolist(),
        'seconds':phase['numerical_seconds']}
    (ROOT/'NUMERICAL_PROPOSAL.json').write_text(json.dumps(proposal,indent=2)+'\n')

    tick=time.perf_counter()
    Am=symrows(Ar)
    independent=list(Am.T.to_DM().convert_to(sp.QQ).rref()[1])
    Aind=Am[independent,:]
    pivots=list(Aind.to_DM().convert_to(sp.QQ).rref()[1])
    inv=Aind[:,pivots].inv()
    phase['projection_setup_seconds']=time.perf_counter()-tick
    tick=time.perf_counter()
    raw=pack([[rnd(x) for x in row] for row in C.value],[[rnd(x) for x in row] for row in K.value])
    trials=[]
    for b in (22,20,18,16,14,12,10,8):
        theta=F(1,1<<b);v=[(1-theta)*x+theta*y for x,y in zip(raw,v0)]
        residual=[br[h]-sum(Ar[h][j]*v[j] for j in range(nv)) for h in independent]
        delta=inv*sp.Matrix([sp.Rational(x.numerator,x.denominator) for x in residual])
        for j,x in zip(pivots,delta):v[j]+=fraction(x)
        Cr,Kr=unpack(v,d,m,n)
        Rr=minus(target_coefficients(Kr,c)[0][1],phi(Cr,AA,f))
        exact=matvec(Ar,v)==br and all(x>=kappa for row in Kr for x in row)
        oc,pc=ldl_positive(Cr);orr,pr=ldl_positive(Rr)
        trials.append({'mixing':str(theta),'equalities_and_floor':exact,'C_PD':oc,'R_PD':orr})
        if exact and oc and orr:break
    if not(exact and oc and orr):raise RuntimeError('NO_EXACT_PRIMAL '+str(trials))
    upper=sum(cost[y][i]*Kr[y][i] for y in range(m) for i in range(n))
    phase['primal_projection_and_check_seconds']=time.perf_counter()-tick

    tick=time.perf_counter()
    Yraw=[[rnd(x) for x in row] for row in conR.dual_value]
    Y,shiftY,py,tryY=positive_shift(Yraw,40)
    lam=[rnd(x) for x in eq.dual_value]
    # Lagrangian: objective + lambda*(A v-b) - Tr(Y R).
    gc=[sum(lam[h]*Ar[h][j] for h in range(len(Ar))) for j in range(nc)]
    for h,(u,vv) in enumerate(coords):
        a,p=divmod(u,f);b,q=divmod(vv,f)
        # derivative of Tr(Y Phi(A0)); A0 is diagonal here.
        if a==b:
            gc[h]+=AA[a][a]*Y[q][p]
            if u!=vv:gc[h]+=AA[a][a]*Y[p][q]
    M=quadratic_matrix(gc,d)
    Mshift,shiftC,pm,tryC=positive_shift(M,40)
    residualK=zeros(m,n)
    for y in range(m):
        for i in range(n):
            residualK[y][i]=cost[y][i]+sum(lam[h]*Ar[h][nc+y*n+i] for h in range(len(Ar)))-Y[y][y]/n
    constant=-sum(lam[h]*br[h] for h in range(len(Ar)))-c*Y[-1][-1]
    amin=min(AA[i][i] for i in range(e));traceC=(1+c)/amin
    lower=constant+min_floor_columns(residualK,kappa)-shiftC*traceC
    assert lower<=upper
    phase['dual_repair_and_check_seconds']=time.perf_counter()-tick
    certificate={'C':encode(Cr),'K':encode(Kr),'R':encode(Rr),'mixing_trials':trials,
        'primal_C_LDL':pc,'primal_R_LDL':pr,'global_upper':str(upper),
        'dual_Y':encode(Y),'dual_lambda':list(map(str,lam)),
        'dual_C_shift':str(shiftC),'dual_trace_C_bound':str(traceC),
        'dual_Y_initial_shift':str(shiftY),'dual_Y_shift_trials':tryY,'dual_C_shift_trials':tryC,
        'dual_Y_LDL':py,'dual_shifted_C_LDL':pm,'global_lower':str(lower),
        'global_gap':str(upper-lower),'projection_rank':len(pivots),
        'projection_independent_rows':independent,'projection_pivot_columns':pivots}
    (ROOT/'CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    phase['after_imports_seconds']=time.perf_counter()-run
    phase['import_seconds']=IMPORT_SECONDS
    phase['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    phase['numerical_status_is_not_a_certificate']=True
    (ROOT/'ACQUISITION_COST.json').write_text(json.dumps(phase,indent=2)+'\n')
    print(json.dumps({'status':'EXACT_PRIMAL_AND_GLOBAL_BOUND','orders':[e,f,d],
        'bounds':[float(lower),float(upper)],'gap':float(upper-lower),'costs':phase},indent=2))


if __name__=='__main__':main()
