"""Counted low-energy trace enclosures using a verified rank lift.

The scalar arithmetic is directed mpmath interval arithmetic. Matrix product
error bounds assume IEEE binary64 round-to-nearest real operations, including
correctly rounded FMA, with at most 8*d+8 operations in a complex dot product.
No correctness property of the eigensolver or Cholesky routine is presumed:
their returned arrays are checked by residuals. This is an ordinary validated
linear-algebra construction, not a new gap criterion or polynomial spin-count
algorithm. The matrices and their dimension remain explicit.
"""
from __future__ import annotations
import pathlib,sys,json,math,time,argparse,gc
from functools import lru_cache
import spin_chain as sc
import numpy as np
from scipy.linalg import cholesky,solve_triangular
from scipy.sparse.linalg import eigsh
import mpmath as mp
mp.iv.dps=60
iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent
U=iv.mpf(2)**-53

def upper(q):return math.nextafter(float(q.b),math.inf)
def lower(q):return math.nextafter(float(q.a),-math.inf)
def gamma(k):
    x=k*U;assert upper(x)<.01
    return x/(1-x)

def nf(a):
    """Upper Frobenius norm of an array of exact stored binary numbers."""
    x=np.asarray(a)
    s=float(np.sum(x.real*x.real+x.imag*x.imag,dtype=np.float64))
    return upper(iv.sqrt((iv.mpf(s)+iv.mpf('1e-280'))/(1-gamma(4*x.size+16))))


@lru_cache(None)
def coefficient_error(n,m,twist,k,r,t):
    # Validate the actual coefficient expression used by spin_chain.py against
    # exp(-i*(2*pi*k-pi*twist*M)*t/n)/sqrt(r), independently of np.exp accuracy.
    phi=-(2*iv.pi*k-iv.pi*twist*m)*t/n
    re=iv.cos(phi)/iv.sqrt(r);im=iv.sin(phi)/iv.sqrt(r)
    tau=np.exp(1j*(2*np.pi*k-np.pi*twist*m)/n)
    z=tau**(-t)/np.sqrt(r)
    err=upper(iv.sqrt((re-z.real)**2+(im-z.imag)**2))
    assert err<1e-14
    return err


def input_error(n,m,twist,k):
    # All possible translation orbit lengths; overcoverage is harmless.
    for r in range(1,n+1):
        if n%r or k*r%n:continue
        for t in range(r):coefficient_error(n,m,twist,k,r,t)
    e=iv.mpf('1e-14')*iv.sqrt(n)
    # H=H0+sqrt(6)*H1, max 2n irrational entries per row. sqrt(6)'s
    # actual stored approximation is also enclosed independently.
    s=iv.sqrt(6)-np.sqrt(6.0);sqrt_error=upper(iv.sqrt(s*s))
    bound=6*n*(2*e+e*e)+(2*n*sqrt_error)*(1+e)**2
    # COO products, duplicate summation, and Hermitian symmetrization.
    bound+=gamma(32+8*n*(2*n+1))*10*n*(1+e)**2
    assert upper(bound)<1e-9
    return 1e-9  # deliberately conservative, independent of observed spectra


def check_block(h,n,m,twist,k,cut,head_count):
    d=h.shape[0];dh=input_error(n,m,twist,k);start=time.monotonic()
    if head_count:
        if head_count>=d-1:
            # Small blocks are handled by a full basis; dense eigh is merely
            # a producer of candidate vectors, not a premise.
            from scipy.linalg import eigh
            theta,q=eigh(h.toarray(),check_finite=False);head_count=d
        else:
            theta,q=eigsh(h,k=head_count,which='SA',tol=2e-13,ncv=min(d,max(4*head_count+8,35)))
            order=np.argsort(theta);theta,q=theta[order],q[:,order]
        qnorm=nf(q);theta_norm=max(abs(float(theta[0])),abs(float(theta[-1])))
        gram=q.conj().T@q-np.eye(head_count)
        delta=iv.mpf(nf(gram))+gamma(8*d+8)*qnorm*qnorm+gamma(4)*(qnorm*qnorm+iv.sqrt(head_count))
        assert upper(delta)<.01
        residual=h@q-q*theta[None,:]
        r=iv.mpf(nf(residual))+gamma(8*d+8)*nf(h.data)*qnorm+gamma(8)*(nf(h.data)*qnorm+theta_norm*qnorm)+dh*qnorm
        polar_change=1/iv.sqrt(1-delta)-1
        e=r/iv.sqrt(1-delta)+2*iv.sqrt(1+delta)*theta_norm*polar_change
        eta=2*e
        assert upper(iv.mpf(float(theta[-1]))+eta)<cut or head_count==d
        del residual,gram
    else:
        theta=np.empty(0);q=np.empty((d,0),complex);qnorm=0.;eta=iv.mpf(0)

    alpha=max(1.,cut-float(theta[0])+1.) if head_count else 0.
    a=h.toarray();a[np.diag_indices(d)]-=cut
    if head_count:a+=alpha*(q@q.conj().T)
    af=nf(a)
    din=iv.mpf(dh)+alpha*gamma(8*head_count+16)*qnorm*qnorm+gamma(12)*(nf(h.data)+abs(cut)*iv.sqrt(d)+alpha*qnorm*qnorm)
    ell=cholesky(a,lower=True,check_finite=False)
    ln=nf(ell)
    product=ell@ell.conj().T
    fact_resid=nf(a-product)
    ef=iv.mpf(fact_resid)+gamma(8*d+8)*ln*ln+gamma(4)*(af+ln*ln)
    del product,a
    x=solve_triangular(ell,np.eye(d,dtype=complex),lower=True,check_finite=False)
    xn=nf(x)
    inverse_residual=np.eye(d,dtype=complex)-ell@x
    rho=iv.mpf(nf(inverse_residual))+gamma(8*d+8)*ln*xn+gamma(4)*(iv.sqrt(d)+ln*xn)
    assert upper(rho)<1
    b=iv.mpf(xn)/(1-rho)
    margin=1/(b*b)-ef-din
    assert lower(margin)>0, (n,m,twist,k,lower(margin))
    # Rank at most K of alpha QQ*: positivity proves at most K eigenvalues
    # below cut. Polar-isometry Ritz bounds prove at least K below cut.
    # Weyl with Htilde=Qbar diag(theta) Qbar* + Pperp H Pperp then pairs all
    # K eigenvalues with theta to accuracy eta. The rest are >=cut.
    row={'dimension':d,'head_count':head_count,'cut':cut,'alpha':alpha,'input_matrix_error_upper':dh,'gram_error_upper':upper(delta) if head_count else 0.,'head_eigenvalue_error_upper':upper(eta),'theta':theta.tolist(),'positive_lift_margin_lower':lower(margin),'factor_residual_bound_upper':upper(ef),'inverse_residual_bound_upper':upper(rho),'seconds':time.monotonic()-start}
    del x,inverse_residual,ell,q;gc.collect();return row


def run(n,twist,beta='12',shift='4.76124816',tail='0.00001',output=None):
    start=time.monotonic();betaq=iv.mpf(beta);aq=iv.mpf(shift)
    # One common cutoff makes the TOTAL tail <=tail, before matrix uncertainty.
    cq=-aq*n+iv.log(iv.mpf(5)**n/iv.mpf(tail))/betaq
    cut=upper(cq)
    diagnostic=json.loads((ROOT/f'data/spin2_n{n}_p{twist}.json').read_text())
    bykey={(r['magnetization'],r.get('momentum',None)):r for r in diagnostic['sectors']}
    result={'n':n,'twist':twist,'beta':beta,'shift':shift,'requested_tail_upper':tail,'cut':cut,'status':'RUNNING','blocks':[],'arithmetic_contract':__doc__}
    trace=iv.mpf(0);tail_sum=iv.mpf(0)
    for m in range(2*n+1):
        for k,h in sc.momentum_blocks(n,m,twist):
            if not h.shape[0]:continue
            # Ordinary spectra select the candidate K only. Missing a level
            # makes the positive-lift verification fail instead of silently
            # making the thermal tail smaller.
            rec=bykey.get((m,k))
            if rec is None:
                from scipy.linalg import eigvalsh
                e=eigvalsh(h.toarray(),check_finite=False)
            else:e=np.array(rec['values'])
            count=int(np.sum(e<cut))
            row=check_block(h,n,m,twist,k,cut,count);row['magnetization']=m;row['momentum']=k;mult=1 if m==0 else 2;row['multiplicity']=mult
            eta=iv.mpf(row['head_eigenvalue_error_upper'])
            head=iv.mpf(0)
            for t in row['theta']:head+=iv.exp(-betaq*(iv.mpf(t)+iv.mpf([-1,1])*eta+aq*n))
            tailpart=(row['dimension']-row['head_count'])*iv.exp(-betaq*(iv.mpf(cut)+aq*n))
            trace+=mult*(head+iv.mpf([0,upper(tailpart)]));tail_sum+=mult*tailpart
            result['blocks'].append(row);result['trace_lower']=lower(trace);result['trace_upper']=upper(trace);result['tail_upper']=upper(tail_sum)
            if output:pathlib.Path(output).write_text(json.dumps(result,indent=2))
            if k==0:print('certified',n,twist,'M',m,'K',count,'margin',row['positive_lift_margin_lower'],'elapsed',time.monotonic()-start,flush=True)
    assert sum(r['dimension']*r['multiplicity']for r in result['blocks'])==5**n
    result['status']='DIRECTED_SCALAR_ENCLOSURE_UNDER_DECLARED_IEEE_MATRIX_MODEL';result['seconds']=time.monotonic()-start
    if output:pathlib.Path(output).write_text(json.dumps(result,indent=2))
    print('TRACE',n,twist,result['trace_lower'],result['trace_upper'],'tail',result['tail_upper'],'seconds',result['seconds'],flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('twist',type=int);ap.add_argument('--beta',default='12');ap.add_argument('--shift',default='4.76124816');ap.add_argument('--tail',default='0.00001');ap.add_argument('--output',required=True);a=ap.parse_args();run(a.n,a.twist,a.beta,a.shift,a.tail,a.output)
