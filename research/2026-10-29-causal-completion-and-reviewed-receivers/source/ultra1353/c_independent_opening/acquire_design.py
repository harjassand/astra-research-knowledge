"""One arbitrary-alphabet design and rational primal/dual qualification.

CVXPY/CLARABEL only proposes. Exact rational checks qualify the budget and
the global utility interval. All construction, solving, repair and checking
costs are retained. No input/side-information sampler or physical data.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import resource
import time

START = time.perf_counter()
import numpy as np
import sympy as sp
import cvxpy as cp
from scipy.optimize import linprog
IMPORT_SECONDS = time.perf_counter()-START
ROOT = Path(__file__).resolve().parent


def mat(rows):
    return sp.Matrix([[sp.Rational(F(x).numerator,F(x).denominator) for x in r] for r in rows])


def encode(M):
    return [[str(x) for x in row] for row in M.tolist()]


def fp(M):
    return np.array(M.tolist(),dtype=float)


def round_matrix(M, bits=38):
    den = 1 << bits
    return sp.Matrix([[sp.Rational(round(float(x)*den),den) for x in row] for row in M])


def ldl_positive(M):
    """Exact rational positive definiteness; no eigenvalue sign is trusted."""
    assert M == M.T
    n = M.rows
    L = sp.eye(n)
    d = []
    for j in range(n):
        dj = M[j,j]-sum(L[j,k]**2*d[k] for k in range(j))
        if dj <= 0:
            return False, j
        d.append(dj)
        for i in range(j+1,n):
            L[i,j] = (M[i,j]-sum(L[i,k]*L[j,k]*d[k] for k in range(j)))/dj
    return True, min(d)


def invariants(L):
    n = L.rows
    p = n-1
    R = L.inv()[:p,:]
    H = []
    for i in range(n):
        e = sp.eye(n)[:p,i]
        h = sum((L[y,i]*R[:,y]*R[:,y].T for y in range(n)),sp.zeros(p))-e*e.T
        assert ldl_positive(h)[0]
        H.append(h)
    return H, [h.inv() for h in H]


def block(K, aa, Hinv, i, c):
    m,n = K.shape
    q,p = m-1,n-1
    D = K[:q,:p]-K[:q,n-1]*sp.ones(1,p)
    x = K[:q,i]
    t = 1-c
    M = sp.zeros(m+n)
    M[:q,:q] = c*sp.diag(*x)
    M[:q,q:q+p] = D
    M[q:q+p,:q] = D.T
    M[q:q+p,q:q+p] = Hinv[i]
    M[:q,q+p] = c*x
    M[q+p,:q] = c*x.T
    M[q+p,q+p] = c
    M[:q,q+p+1] = aa-t*x
    M[q+p+1,:q] = (aa-t*x).T
    M[q+p+1,q+p+1] = t
    return M


def certificate_blocks(K, aa, H, c):
    m,n = K.shape
    q,p = m-1,n-1
    D = K[:q,:p]-K[:q,n-1]*sp.ones(1,p)
    t=1-c
    return [c*sp.diag(*K[:q,i])-D*H[i]*D.T
            -c*K[:q,i]*K[:q,i].T
            -(aa-t*K[:q,i])*(aa-t*K[:q,i]).T/t for i in range(n)]


def trace_product(A,B):
    return sum(A[i,j]*B[j,i] for i in range(A.rows) for j in range(A.cols))


def main():
    start=time.perf_counter()
    n,m=12,7
    q,p=m-1,n-1
    c=sp.Rational(1,2)
    kappa=sp.Rational(1,1000)
    L=sp.ones(n)*sp.Rational(1,10*n)
    for j in range(n):
        L[j,j]+=sp.Rational(3,5)
        L[(j+1)%n,j]+=sp.Rational(1,5)
        L[(j+2)%n,j]+=sp.Rational(1,10)
    assert all(sum(L[:,j])==1 for j in range(n)) and L.det()!=0
    prior=[sp.Rational(2*(i+1),n*(n+1)) for i in range(n)]
    C=sp.Matrix(m,n,lambda y,i:prior[i]*(sp.Rational(i,n-1)-sp.Rational(y,m-1))**2)
    prep=time.perf_counter()
    H,Hinv=invariants(L)
    Hseconds=time.perf_counter()-prep
    K=cp.Variable((m,n));aa=cp.Variable(q)
    dd=K[:q,:p]-cp.reshape(K[:q,n-1],(q,1),order='C')@np.ones((1,p))
    t=float(1-c)
    constraints=[cp.sum(K,axis=0)==1,K>=float(kappa),aa>=-2,aa<=2]
    psd=[]
    for i in range(n):
        xx=cp.reshape(K[:q,i],(q,1),order='C')
        av=cp.reshape(aa,(q,1),order='C')
        M=cp.bmat([[float(c)*cp.diag(K[:q,i]),dd,float(c)*xx,av-t*xx],
                   [dd.T,fp(Hinv[i]),np.zeros((p,1)),np.zeros((p,1))],
                   [float(c)*xx.T,np.zeros((1,p)),np.array([[float(c)]]),np.zeros((1,1))],
                   [(av-t*xx).T,np.zeros((1,p)),np.zeros((1,1)),np.array([[t]])]])
        con=(M>>0);constraints.append(con);psd.append(con)
    problem=cp.Problem(cp.Minimize(cp.sum(cp.multiply(fp(C),K))),constraints)
    tick=time.perf_counter()
    problem.solve(solver='CLARABEL',tol_gap_abs=2e-10,tol_feas=2e-10,
                  tol_gap_rel=2e-10,max_iter=250)
    solve_seconds=time.perf_counter()-tick
    if K.value is None or aa.value is None:
        raise RuntimeError('NO_PROPOSAL: '+str(problem.status))
    proposal={'status':problem.status,'value':float(problem.value),
              'K':K.value.tolist(),'a':aa.value.tolist(),
              'dual_blocks':[con.dual_value.tolist() for con in psd]}
    (ROOT/'NUMERICAL_PROPOSAL.json').write_text(json.dumps(proposal,indent=2)+'\n')
    tick=time.perf_counter()
    rawK=round_matrix(K.value)
    for j in range(n):
        rawK[m-1,j]=1-sum(rawK[y,j] for y in range(m-1))
    rawA=round_matrix([[x] for x in aa.value])
    K0=sp.ones(m,n)/m
    A0=sp.ones(q,1)*(1-c)/m
    # Preserve even failed rational repairs; one solved numerical target only.
    repairs=[]
    for bits in (24,22,20,18,16,14,12):
        theta=sp.Rational(1,2**bits)
        Kr=(1-theta)*rawK+theta*K0
        ar=(1-theta)*rawA+theta*A0
        coeff=certificate_blocks(Kr,ar,H,c)
        passed=all(x>=kappa for x in Kr) and all(abs(x)<=2 for x in ar)
        pivots=[]
        if passed:
            for b in coeff:
                ok,pivot=ldl_positive(b)
                if not ok:
                    passed=False;break
                pivots.append(str(pivot))
        repairs.append({'uniform_mixing_theta':str(theta),'passed':bool(passed)})
        if passed:break
    if not passed:
        raise RuntimeError('NO_CERTIFIED_PRIMAL; failures preserved in proposal')
    primal_seconds=time.perf_counter()-tick
    ub=sum(C[y,i]*Kr[y,i] for y in range(m) for i in range(n))

    # The full PSD dual is only a suggestion. Rational diagonal repairs and
    # the explicit affine-box lower bound make a source-independent certificate.
    tick=time.perf_counter()
    dual=[];dual_repairs=[]
    for i,con in enumerate(psd):
        yy=(con.dual_value+con.dual_value.T)/2
        Y=round_matrix(yy,bits=34)
        for bits in (32,30,28,26,24,22,20):
            shift=sp.Rational(1,2**bits)
            candidate=Y+shift*sp.eye(m+n)
            ok,pivot=ldl_positive(candidate)
            dual_repairs.append({'i':i,'shift':str(shift),'passed':bool(ok)})
            if ok:
                dual.append(candidate);break
        else:raise RuntimeError('NO_CERTIFIED_DUAL')
    residual=C.copy();b=sp.zeros(q,1);constant=sp.Rational(0)
    for i,Y in enumerate(dual):
        alpha=q+p;beta=alpha+1
        constant-=trace_product(Y[q:q+p,q:q+p],Hinv[i])+c*Y[alpha,alpha]+(1-c)*Y[beta,beta]
        for h in range(q):
            residual[h,i]-=c*Y[h,h]+2*c*Y[h,alpha]-2*(1-c)*Y[h,beta]
            b[h]-=2*Y[h,beta]
            for j in range(p):
                residual[h,j]-=2*Y[h,q+j]
                residual[h,n-1]+=2*Y[h,q+j]
    lb=constant-2*sum(abs(x) for x in b)
    for i in range(n):
        lb+=kappa*sum(residual[:,i])+(1-m*kappa)*min(residual[:,i])
    assert lb<=ub
    dual_seconds=time.perf_counter()-tick

    # Strong ordinary sufficient family with the same X,L,C,c. Its relaxed
    # optimum (no positivity floor) is an exact analytic lower bound on every
    # such family member. This is NOT called the strongest ordinary algorithm.
    tick=time.perf_counter()
    losses=C*L.T
    postchoices=[min(range(m),key=lambda y:losses[y,z]) for z in range(n)]
    constant_choice=min(range(m),key=lambda y:sum(C[y,:]))
    ordinary_opt=c*sum(losses[postchoices[z],z] for z in range(n))
    ordinary_opt+=(1-c)*sum(C[constant_choice,:])
    ordinary_seconds=time.perf_counter()-tick
    # Also give the ordinary sufficient family the SAME entry-floor contract.
    # The relaxed exact value above remains visible even if it is smaller than
    # the new design. A hoped-for comparison sign is never an admission test.
    tick=time.perf_counter()
    count=m*n+m
    ob=np.concatenate([float(c)*fp(losses).ravel(),
                       float(1-c)*fp(C).sum(axis=1)])
    amap=np.zeros((m*n,count))
    for y in range(m):
        for i in range(n):
            for z in range(n):amap[y*n+i,y*n+z]=float(c*L[z,i])
            amap[y*n+i,m*n+y]=float(1-c)
    eq=np.zeros((n+1,count));rhs=np.ones(n+1)
    for z in range(n):
        for y in range(m):eq[z,y*n+z]=1
    eq[n,m*n:]=1
    lp=linprog(ob,A_ub=-amap,b_ub=-float(kappa)*np.ones(m*n),
               A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    if not lp.success:raise RuntimeError('ORDINARY_LP_NO_PROPOSAL')
    # Any nonnegative floor multiplier gives an exact LP lower certificate;
    # each P column and r is minimized on its entire simplex analytically.
    multipliers=round_matrix(np.maximum(0,-lp.ineqlin.marginals).reshape((m,n)),bits=34)
    cc=C-multipliers
    lp_lower=kappa*sum(multipliers)+c*sum(min((cc*L.T)[:,z]) for z in range(n))
    lp_lower+=(1-c)*min(sum(cc[y,:]) for y in range(m))
    P=round_matrix(np.maximum(0,lp.x[:m*n]).reshape((m,n)))
    rr=round_matrix([[max(0,x)] for x in lp.x[m*n:]])
    for z in range(n):P[:,z]=P[:,z]/sum(P[:,z])
    rr=rr/sum(rr)
    for bits in (24,22,20,18,16):
        theta_lp=sp.Rational(1,2**bits)
        Pr=(1-theta_lp)*P+theta_lp*sp.ones(m,n)/m
        rrr=(1-theta_lp)*rr+theta_lp*sp.ones(m,1)/m
        Kordinary=c*Pr*L+(1-c)*rrr*sp.ones(1,n)
        if all(x>=kappa for x in Kordinary):break
    else:raise RuntimeError('ORDINARY_LP_PRIMAL_NOT_QUALIFIED')
    lp_upper=sum(C[y,i]*Kordinary[y,i] for y in range(m) for i in range(n))
    assert lp_lower<=lp_upper
    floor_lp_seconds=time.perf_counter()-tick
    source={'n':n,'m':m,'budget':str(c),'entry_floor':str(kappa),'center_box':2,
            'reference_L':encode(L),'cost_C':encode(C),'prior':[str(x) for x in prior],
            'source_scope':'explicit rational software design input, not empirical data',
            'raw_classical_X_access_to_apply_K':'REQUIRED, not inferred from an L record'}
    (ROOT/'SOURCE.json').write_text(json.dumps(source,indent=2)+'\n')
    certificate={'status':'EXACT_RATIONAL_PRIMAL_DUAL_DESIGN',
                 'release_K':encode(Kr),'center_a':encode(ar),'primal_B_pivots':pivots,
                 'dual_Y':[encode(y) for y in dual],
                 'cost_interval_exact':[str(lb),str(ub)],'cost_interval_display':[float(lb),float(ub)],
                 'global_optimality_gap':float(ub-lb),
                 'ordinary_sufficient_family_exact_optimum':str(ordinary_opt),
                 'ordinary_sufficient_family_display':float(ordinary_opt),
                 'ordinary_over_new_cost_ratio':float(ordinary_opt/ub),
                 'ordinary_relaxed_family_beaten':bool(ub<ordinary_opt),
                 'ordinary_SAME_FLOOR_family_interval':[str(lp_lower),str(lp_upper)],
                 'ordinary_SAME_FLOOR_family_display':[float(lp_lower),float(lp_upper)],
                 'ordinary_SAME_FLOOR_family_beaten':bool(ub<lp_lower),
                 'ordinary_SAME_FLOOR_P':encode(Pr),'ordinary_SAME_FLOOR_r':encode(rrr),
                 'ordinary_SAME_FLOOR_dual':encode(multipliers),
                 'ordinary_postprocess_choices':postchoices,
                 'ordinary_constant_choice':constant_choice,
                 'ordinary_is_strongest_possible_algorithm':False,
                 'source_aware_convex_oracle_may_match':True,
                 'primal_repairs':repairs,'dual_repairs':dual_repairs,
                 'costs_seconds':{'imports':IMPORT_SECONDS,'exact_H_acquisition':Hseconds,
                                  'numerical_solve':solve_seconds,'primal_round_and_check':primal_seconds,
                                  'dual_round_and_lower_bound':dual_seconds,
                                  'ordinary_exact_family':ordinary_seconds,
                                  'ordinary_same_floor_LP':floor_lp_seconds,
                                  'after_imports_total':time.perf_counter()-start},
                 'initial_attempt_runtime':'NOT_SERIALIZED; initial failure and source retained in development/',
                 'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'no_reference_state_search_or_sampler':True,
                 'solver':{'cvxpy':cp.__version__,'proposal_status':problem.status},
                 'native_randomized_release_implemented':False}
    (ROOT/'CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({k:v for k,v in certificate.items() if k not in
         ('release_K','center_a','dual_Y','primal_B_pivots','cost_interval_exact',
          'ordinary_sufficient_family_exact_optimum')},indent=2))


if __name__=='__main__':main()
