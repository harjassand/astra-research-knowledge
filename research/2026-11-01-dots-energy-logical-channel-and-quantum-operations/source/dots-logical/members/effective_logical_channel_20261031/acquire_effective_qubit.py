#!/usr/bin/env python3
"""Exact rational acquisition of a CP effective qubit channel; not gate synthesis.
Known uniform zero-field open Glauber chain, H0=X, localized A=Z, time1.
All classical input/certificate/model promises are explicit; no source samples.
"""
from fractions import Fraction as F
from math import isqrt,gcd
import json,time,argparse,sys
sys.set_int_max_str_digits(0) # exact rational certificate serialization, not floating JSON arithmetic
from pathlib import Path
import sympy as sp

def rat(x):
    if isinstance(x,bool): raise ValueError('boolean is not a rational input')
    return F(x)
def pair(x): x=F(x);return [x.numerator,x.denominator]
def sr(x):x=F(x);return sp.Rational(x.numerator,x.denominator)
def cpentry(z):
    z=sp.expand_complex(z);a,b=sp.re(z),sp.im(z)
    if not a.is_Rational or not b.is_Rational:raise ValueError('nonrational entry')
    return [int(a.p),int(a.q),int(b.p),int(b.q)]
def encoded(M):return [[cpentry(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def decoded(a):
    if not isinstance(a,list) or len(a)!=4 or any(not isinstance(row,list) or len(row)!=4 for row in a):raise ValueError('matrix shape')
    for row in a:
        for z in row:
            if not isinstance(z,list) or len(z)!=4 or any(type(v)!=int for v in z) or z[1]<=0 or z[3]<=0 or gcd(abs(z[0]),z[1])!=1 or gcd(abs(z[2]),z[3])!=1:raise ValueError('invalid exact complex rational')
    return sp.Matrix([[sp.Rational(z[0],z[1])+sp.I*sp.Rational(z[2],z[3]) for z in row] for row in a])
def readpair(x):
    if not isinstance(x,list) or len(x)!=2 or any(type(v)!=int for v in x) or x[1]<=0 or gcd(abs(x[0]),x[1])!=1:raise ValueError('invalid rational pair')
    return F(*x)
def thomas(lower,diag,upper,rhs):
    n=len(diag);d=list(diag);v=list(rhs)
    for i in range(1,n):
        if d[i-1]==0:raise ValueError('zero pivot')
        f=lower[i-1]/d[i-1];d[i]-=f*upper[i-1];v[i]-=f*v[i-1]
    x=[F(0)]*n;x[-1]=v[-1]/d[-1]
    for i in range(n-2,-1,-1):x[i]=(v[i]-upper[i]*x[i+1])/d[i]
    return x

def covariance_entry(n,site,t):
    if n==1:return F(1)
    lower=[];upper=[]
    for i in range(n):
        left=t if i else F(0);right=t if i+1<n else F(0)
        # tanh addition/subtraction simplifies to these exact coefficients.
        den=1-left*left*right*right
        a=left*(1-right*right)/den;b=right*(1-left*left)/den
        if i:lower.append(-a)
        if i+1<n:upper.append(-b)
    rhs=[t**abs(i-site) for i in range(n)]
    return thomas(lower,[F(1)]*n,upper,rhs)[site]

def choi(E):
    return sp.Matrix(4,4,lambda a,b:E[(a%2)+2*(b%2),(a//2)+2*(b//2)])
def ptrout(J):return sp.Matrix(2,2,lambda i,j:sum(J[2*i+a,2*j+a] for a in range(2)))
def exact_ldl(J):
    L=sp.eye(4);ds=[]
    for j in range(4):
        dj=sp.simplify(J[j,j]-sum(L[j,k]*sp.conjugate(L[j,k])*ds[k] for k in range(j)))
        if not dj.is_Rational or dj<=0:raise ValueError('PSD repair has nonpositive exact pivot')
        ds.append(dj)
        for i in range(j+1,4):L[i,j]=sp.simplify((J[i,j]-sum(L[i,k]*sp.conjugate(L[j,k])*ds[k] for k in range(j)))/dj)
    assert L*sp.diag(*ds)*L.conjugate().T==J
    return L,ds

def acquire_cp(dcoef,epsnum):
    D=sr(dcoef);epsnum=rat(epsnum);delta=epsnum/9
    X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1);I2=sp.eye(2);I4=sp.eye(4)
    G=-sp.I*(sp.kronecker_product(I2,X)-sp.kronecker_product(X.T,I2))+2*D*(sp.kronecker_product(Z,Z)-I4)
    C=2+4*dcoef;N=1;s=0
    while N<4*C:N*=2;s+=1
    K=0
    while F(2,4**(K+1))>delta/(4*N):K+=1
    E=I4;term=I4
    for k in range(1,K+1):
        term=term*G/(N*k);E=E+term
    for _ in range(s):E=E*E
    J=choi(E);assert J==J.conjugate().T and ptrout(J)==I2
    eta=2*sr(delta)
    Jcp=(J+eta*I4)/(1+2*eta)
    assert ptrout(Jcp)==I2
    L,ds=exact_ldl(Jcp)
    return dict(delta_raw=pair(delta),generator_cb_upper=pair(C),scaling_power=s,Taylor_degree=K,
      local_Taylor_error_upper=pair(F(2,4**(K+1))),squaring_error_upper=pair(delta/2),
      CP_channel_error_upper=pair(9*delta),
      choi=encoded(Jcp),ldl_unit_lower=encoded(L),ldl_positive_diagonal=[pair(F(x)) for x in ds],
      Kraus_convention='K_j[a,i]=sqrt(d_j)*L[2*i+a,j]; exact algebraic entries; sum K_j^dagger K_j=I.',
      scope='Exact rational CP/TP channel and algebraic Kraus representation; no quantum gate backend.')

def acquire(n,site,q,lam,epsilon):
    if type(n)!=int or n<1 or type(site)!=int or not 0<=site<n:raise ValueError('invalid chain/site')
    q=rat(q);lam=rat(lam);epsilon=rat(epsilon)
    if q<=0 or lam<=0 or not 0<epsilon<1:raise ValueError('invalid positive inputs')
    t=(q-1)/(q+1)
    if abs(t)>F(1,40):raise ValueError('uniform weak-bond certificate failed')
    kappa=F(19,20);r=1-kappa
    U=8/kappa+16/kappa**2;W=24/kappa**2+16/kappa**3
    root=isqrt(lam.numerator//lam.denominator)
    model=F(2) if root==0 else min(F(2),U/root+W/lam)
    epscoef=epsilon/4;epsnum=epsilon/8 # reserve epsilon/8 for optional actual gate synthesis
    if model>epsilon/2:return dict(status='ABORT',reason='effective-model certificate exceeds assigned budget',model_error_upper=pair(model))
    R=0
    while True:
        left=max(0,site-R);right=min(n-1,site+R)
        whole=left==0 and right==n-1
        coeffchannel=F(0) if whole else 8*r**(R+1)/kappa
        if coeffchannel<=epscoef:break
        R+=1
    localn=right-left+1;D=covariance_entry(localn,site-left,t)
    if D<=0:raise ValueError('nonpositive effective covariance')
    cp=acquire_cp(D,epsnum)
    total=model+coeffchannel+epsnum
    assert total<=epsilon
    return dict(status='PASS',known_program=dict(n=n,site=site,uniform_Boltzmann_ratio=pair(q),tanh_bond=pair(t),clock_rate=pair(lam)),
      task='Entire logical qubit/reference, no controls in this executable fixture; bath discarded; arbitrary initial source correlations under the proved invariant algebra.',
      kappa=pair(kappa),epsilon=pair(epsilon),radius=R,local_sites=[left,right],coefficient=D.__str__(),coefficient_rational=pair(D),
      model_error_upper=pair(model),local_coefficient_channel_error_upper=pair(coeffchannel),numerical_channel_error_upper=pair(epsnum),total_error_upper=pair(total),reserved_gate_error=pair(epsilon/8),combined_error_upper=pair(total+epsilon/8),
      channel=cp,scope='Known uniform mechanism, not learned data; exact CP certificate, no gate implementation or source-output guarantee.')

def verify_channel(record):
    """Checks ONLY exact CP/TP representation, not source law or approximation."""
    try:
        c=record['channel'];J=decoded(c['choi']);L=decoded(c['ldl_unit_lower'])
        raw=c['ldl_positive_diagonal']
        if not isinstance(raw,list) or len(raw)!=4:return False
        ds=[sr(readpair(x)) for x in raw]
        if any(x<=0 for x in ds) or any(L[i,i]!=1 for i in range(4)) or any(L[i,j]!=0 for i in range(4) for j in range(i+1,4)):return False
        return bool(J==J.conjugate().T and ptrout(J)==sp.eye(2) and L*sp.diag(*ds)*L.conjugate().T==J)
    except (KeyError,ValueError,TypeError,ZeroDivisionError,IndexError):return False

def strict_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(strict_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b

def verify_record(record):
    """Recompute the known-program certificate; this does not verify a physical model."""
    try:
        if not isinstance(record,dict) or record.get('status')!='PASS':return False
        z=record['known_program']
        rebuilt=acquire(z['n'],z['site'],readpair(z['uniform_Boltzmann_ratio']),readpair(z['clock_rate']),readpair(record['epsilon']))
        return strict_equal(rebuilt,record) and verify_channel(record)
    except (KeyError,ValueError,TypeError,ZeroDivisionError,IndexError):return False

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=16);ap.add_argument('--site',type=int,default=8);ap.add_argument('--q',default='21/20');ap.add_argument('--lambda',dest='lam',default='100000000');ap.add_argument('--epsilon',default='1/100');ap.add_argument('--output',default='effective_logical_channel_20261031/effective_qubit_certificate.json');a=ap.parse_args()
    start=time.perf_counter();out=acquire(a.n,a.site,a.q,a.lam,a.epsilon);elapsed=time.perf_counter()-start
    if out['status']=='PASS':assert verify_channel(out)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'seconds',round(elapsed,4),'radius',out.get('radius'),'bytes',Path(a.output).stat().st_size)
if __name__=='__main__':main()
