"""Exact relative-order inputs and competent ordinary entropy comparisons.

PSD qualification uses explicit rational unitary/congruence factors. Dense
entropy values are diagnostics, separated from the analytic certificate.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sympy as s
import numpy as np
import mpmath as mp
import json,time
from exact_controls import ROOT,channel,depolarize,trace_a,epsilon

EPS=s.Rational(1,192);MARGIN=s.Rational(869,2592)
def simple(A):return A.applyfunc(s.simplify)
def householder(values):
    v=s.Matrix(values);return s.eye(len(v))-2*v*v.T/(v.T*v)[0]
def record(A):return [[str(x)for x in row]for row in A.tolist()]
def numeric(A):return np.array(A.tolist(),dtype=complex)
def entropy_numpy(A):
    vals=np.linalg.eigvalsh(A);assert vals.min()>-5e-14
    keep=vals>0
    return float(-np.dot(vals[keep],np.log(vals[keep]))),float(vals.min())
def scalar_mp(x):
    return mp.mpf(int(s.numer(x)))/int(s.denom(x))
def entropy_mp(A):
    B=mp.matrix([[mp.mpc(scalar_mp(s.re(x)),scalar_mp(s.im(x)))for x in row]for row in A.tolist()])
    ev=mp.eighe(B,eigvals_only=True);assert min(ev)>0
    return -sum(x*mp.log(x)for x in ev)

def direct_cmi(rho,r):
    d=3*r;V=np.array([[epsilon(i,j,k)/np.sqrt(2)for i in range(3)]for j in range(3)for k in range(3)])
    lift=np.kron(V,np.eye(d));sigma=lift@rho@lift.conjugate().T
    tensor=sigma.reshape(3,3,d,3,3,d)
    q1r=np.einsum('abrcbs->arcs',tensor).reshape(3*d,3*d)
    q2r=np.einsum('abraps->brps',tensor).reshape(3*d,3*d)
    ref=np.einsum('abrabs->rs',tensor)
    marginal=np.einsum('abrpqr->abpq',tensor).reshape(9,9)
    S1,_=entropy_numpy(q1r);S2,_=entropy_numpy(q2r);SR,_=entropy_numpy(ref);Sall,_=entropy_numpy(sigma)
    swap=np.zeros((9,9))
    for i in range(3):
        for j in range(3):swap[3*i+j,3*j+i]=1
    pm=(np.eye(9)-swap)/2
    assert np.max(abs(marginal-pm/3))<2e-13
    return S1+S2-SR-Sall,float(np.max(abs(marginal-pm/3)))

def acquire(name,eigenvalues,complex_reset=False):
    begin=time.monotonic();r=len(eigenvalues);d=3*r
    Q=householder(list(range(1,r+1)));cs=list(map(s.Rational,eigenvalues))
    roots=[s.sqrt(x)for x in cs];assert all(x.is_Rational for x in roots)
    C=simple(Q*s.diag(*cs)*Q.T);Dc=simple(Q*s.diag(*roots)*Q.T);D=s.kronecker_product(s.eye(3),Dc)
    R=householder(list(range(1,d+1)))*householder([j*j+3*j+1 for j in range(1,d+1)])
    if complex_reset:
        phases=[(1,s.I,s.Rational(3,5)+s.Rational(4,5)*s.I)[j%3]for j in range(d)]
        R=s.diag(*phases)*R
    R=simple(R);assert simple(R.H*R)==s.eye(d)and Dc*Dc==C
    ws=[s.Rational(d+j+1,2*d)for j in range(d)]
    Y=simple(EPS*D*R*s.diag(*ws)*R.H*D)
    gap=simple(EPS*D*R*s.diag(*(1-w for w in ws))*R.H*D)
    assert simple(EPS*s.kronecker_product(s.eye(3),C)-Y-gap)==s.zeros(d)
    assert min(ws)>0 and max(ws)==1
    T=s.trace(Y);TC=s.trace(C);assert T>0 and TC>0
    comm=simple(Y*s.kronecker_product(s.eye(3),C)-s.kronecker_product(s.eye(3),C)*Y)
    flat=len(set(cs))==1
    if not flat:assert comm!=s.zeros(d)
    realign=s.Matrix(9,r*r,lambda i,j:Y[(i//3)*r+j//r,(i%3)*r+j%r]);osr=realign.rank();assert osr>2
    active=[j for j,c in enumerate(cs)if c>0];rank=len(active);J=Q[:,active]
    Cp=simple(J.T*C*J);Yp=simple(s.kronecker_product(s.eye(3),J.T)*Y*s.kronecker_product(s.eye(3),J))
    logical=simple(s.kronecker_product(s.eye(3),Q.T)*Y*s.kronecker_product(s.eye(3),Q))
    edges=[]
    for j in active:
        for k in active:
            if j<k and any(logical[b*r+j,c*r+k]!=0 for b in range(3)for c in range(3)):edges.append([j,k])
    assert len(edges)==rank*(rank-1)//2
    omega=s.Matrix([int(i==j)for i in range(3)for j in range(3)])
    X=s.kronecker_product(omega*omega.T,Cp)+s.kronecker_product(s.eye(3),Yp)
    NX=channel(X,rank);EX=depolarize(X,rank);normalizer=3*(TC+T)
    marginal=s.Matrix(3,3,lambda i,j:sum(X[i*3*rank+k,j*3*rank+k]for k in range(3*rank)))
    assert simple(marginal-(TC+T)*s.eye(3))==s.zeros(3)
    rho=X/normalizer;nrho=NX/normalizer;erho=EX/normalizer
    exact_seconds=time.monotonic()-begin
    start_numpy=time.monotonic();SX,vx=entropy_numpy(numeric(rho));SN,vn=entropy_numpy(numeric(nrho));SE,ve=entropy_numpy(numeric(erho))
    normalized_delta=-SX-SE+2*SN;rawdelta=float(normalizer)*normalized_delta
    numpy_seconds=time.monotonic()-start_numpy
    start_mp=time.monotonic();mp.mp.dps=65
    mp_delta=-entropy_mp(rho)-entropy_mp(erho)+2*entropy_mp(nrho)
    mp_seconds=time.monotonic()-start_mp
    assert abs(float(mp_delta)-normalized_delta)<2e-11
    bound=MARGIN*T/normalizer;assert float(mp_delta)>float(bound)
    old_exclusion=None
    if len(active)==r:
        m=min(cs);M=max(cs);kappa=M/m;old_radius=m/(512*kappa**2)
        lower_norm=T/d
        assert lower_norm>old_radius
        old_exclusion={'m':str(m),'M':str(M),'kappa':str(kappa),'old_absolute_norm_radius':str(old_radius),
                       'certified_Y_norm_lower':str(lower_norm),'norm_lower_divided_by_old_radius':str(lower_norm/old_radius),
                       'even_b_le_m_over_192_fails':bool(lower_norm>m/192)}
    direct=None
    if name=='strong_nonflat_complex':
        cmi,err=direct_cmi(numeric(rho),rank)
        assert abs(cmi-np.log(3)-normalized_delta)<5e-12
        direct={'CMI_numeric':cmi,'CMI_minus_log3_numeric':cmi-np.log(3),
                'difference_from_Delta_rho':abs(cmi-np.log(3)-normalized_delta),
                'antisymmetric_marginal_max_error':err,'full_extension_dimension':27*rank}
    data={'name':name,'r':r,'active_logical_rank':rank,'complex_reset':complex_reset,
      'C_eigenvalues':[str(x)for x in cs],'C':record(C),'C_orthogonal_factor':record(Q),
      'C_sqrt':record(Dc),'Y':record(Y),'Y_relative_unitary_factor':record(R),
      'Y_relative_eigenweights':[str(w)for w in ws],'relative_radius':str(EPS),
      'exact_relative_order_certificate':'Y=eps D R diag(w)R* D; eps(I_B tensor C)-Y=eps D R diag(1-w)R* D',
      'trace_C':str(TC),'trace_Y':str(T),'reset_probability':str(T/(TC+T)),
      'exact_Delta_lower':str(MARGIN*T),'exact_normalized_CMI_excess_lower':str(bound),
      'operator_Schmidt_rank_Y':osr,'commutes_with_I_tensor_C':comm==s.zeros(d),
      'active_C_eigenbasis_coherence_edges':edges,'prior_receiver_exclusion':old_exclusion,
      'original_source_dimension':9*r,'active_source_dimension':9*rank,
      'numeric_Delta_normalized':normalized_delta,'numeric_Delta_raw':rawdelta,
      'mp65_Delta_normalized':mp.nstr(mp_delta,60),'numeric_minimum_eigenvalues_normalized':[vx,vn,ve],
      'direct_operational_CMI_control':direct,
      'exact_input_receiver_seconds':exact_seconds,'ordinary_numpy_entropy_seconds':numpy_seconds,
      'ordinary_mp65_entropy_seconds':mp_seconds,
      'entropy_comparison_scope':'Full active-support dense eigensystems; mp agreement is not a certified matrix-entropy enclosure. Analytic receiver plus exact order factors supplies the certificate.',
      'physical_input':'Synthetic exact supplied channel; no measured/implemented device'}
    (ROOT/f'results/{name}.json').write_text(json.dumps(data,indent=2)+'\n')
    summary={k:v for k,v in data.items()if k not in ('C','C_orthogonal_factor','C_sqrt','Y','Y_relative_unitary_factor','Y_relative_eigenweights')}
    print(json.dumps(summary,indent=2),flush=True)
    return summary

def main():
    rows=[acquire('strong_nonflat_complex',[1,10000],True),acquire('very_nonflat',[1,10000,100000000]),
          acquire('flat_arbitrary_reset',[1,1,1]),acquire('singular_noncommuting',[0,1,10000])]
    (ROOT/'results/fixture_summary.json').write_text(json.dumps({'status':'PASS_EXACT_RELATIVE_ORDER_AND_DENSE_ENTROPY_CONTROLS','rows':rows},indent=2)+'\n')

if __name__=='__main__':main()
