"""Acquire a local relative-order certificate, rather than assume an inverse.

The local four-site nested commutator is evaluated exactly in Q(sqrt(6)).
A numerical positive vector is only a producer for a rational weighted row
bound. The final norm certificate checks every entry and ratio exactly.
This yields an all-ring single-Strang-slice residual comparison. It does not
compress or contract the cold long-ring tensor network.
"""
import json, pathlib, math
from fractions import Fraction as F
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as sla
import mpmath as mp

ROOT=pathlib.Path(__file__).resolve().parent
mp.iv.dps=80; iv=mp.iv
SLO=F(2449489742783178098,10**18)
SHI=F(2449489742783178099,10**18)
assert SLO*SLO<6<SHI*SHI

def pair(n,i,j):
    # Independent weight-basis construction; h=h0+sqrt(6)h1.
    dim=5**n;rows=[[],[]];cols=[[],[]];vals=[[],[]]
    for k,word in enumerate(np.ndindex(*(5,)*n)):
        mi,mj=word[i]-2,word[j]-2
        if mi*mj: rows[0].append(k);cols[0].append(k);vals[0].append(mi*mj)
        for di,dj in [(1,-1),(-1,1)]:
            if not(0<=word[i]+di<5 and 0<=word[j]+dj<5):continue
            w=list(word);w[i]+=di;w[j]+=dj
            row=0
            for x in w:row=5*row+x
            # S+ matrix squares4,6,6,4. The bond coefficient is sqrt(ab)/2.
            ab=(6-mi*(mi+di))*(6-mj*(mj+dj));v=math.isqrt(ab)
            if v*v==ab:t=0;value=v//2;assert v%2==0
            else:t=1;value=1;assert ab==24
            rows[t].append(row);cols[t].append(k);vals[t].append(value)
    return tuple(ss.csr_matrix((np.array(vals[t],dtype=np.int64),(rows[t],cols[t])),shape=(dim,dim))for t in [0,1])

def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]@b[0]+6*(a[1]@b[1]),a[0]@b[1]+a[1]@b[0]
def comm(a,b):
    ab=mul(a,b);ba=mul(b,a)
    return ab[0]-ba[0],ab[1]-ba[1]

def abs_upper(a,b):
    x=a+b*SLO;y=a+b*SHI
    return max(abs(x),abs(y))

def acquire_norm():
    a=add(pair(4,0,1),pair(4,2,3));b=pair(4,1,2)
    c=comm(a,comm(a,b))
    assert all((x-x.T).nnz==0 for x in c)
    # Exact support is the union; integer matrix products are far below int64.
    support=(abs(c[0])+abs(c[1])).tocoo()
    c0=c[0].tocsr();c1=c[1].tocsr()
    entries=[(int(i),int(j),int(c0[i,j]),int(c1[i,j]))for i,j in zip(support.row,support.col)]
    absnum=ss.csr_matrix(([float(abs_upper(a,b))for _,_,a,b in entries],(support.row,support.col)),shape=c0.shape)
    numerical_rho=float(sla.eigsh(absnum,k=1,which='LA',return_eigenvectors=False)[0])
    # Produce a positive rational weight. No eigensolver claim is used below.
    candidate=sla.spsolve((numerical_rho+1)*ss.eye(625,format='csr')-absnum,np.ones(625))
    assert np.all(candidate>0)
    weights=[max(1,int(round(float(x)*10**12)))for x in candidate]
    sums=[F(0)for _ in weights];plain=[F(0)for _ in weights]
    for i,j,a,b in entries:
        u=abs_upper(a,b);sums[i]+=u*weights[j];plain[i]+=u
    ratios=[x/w for x,w in zip(sums,weights)]
    maximum=max(ratios);bound=math.ceil(maximum)
    assert all(x<=bound*w for x,w in zip(sums,weights))
    # Matrix C is symmetric, so the weighted Schur test bounds its 2-norm.
    record={'status':'EXACT_RATIONAL_WEIGHTED_SCHUR_CERTIFICATE',
            'matrix':'[h01+h23,[h01+h23,h12]]','dimension':625,
            'nonzero_entries':len(entries),'sqrt6_lower':str(SLO),'sqrt6_upper':str(SHI),
            'weights':weights,'weighted_norm_upper_rational':str(maximum),
            'used_norm_upper_integer':bound,'plain_row_bound_upper':math.nextafter(float(max(plain)),math.inf),
            'numeric_abs_matrix_radius_producer':numerical_rho,
            'local_coefficient_global_logZ_error':'M*n*beta*delta^2*exp(25*delta)/16',
            'scope':'All even periodic rings n>=4. No ground-state gap, Gibbs inverse, spectral completeness, or tensor truncation premise.'}
    (ROOT/'data/local_commutator_certificate.json').write_text(json.dumps(record,indent=2))
    np.savez(ROOT/'data/local_commutator_exact.npz',row=np.array([x[0]for x in entries],dtype=np.int64),col=np.array([x[1]for x in entries],dtype=np.int64),c0=np.array([x[2]for x in entries],dtype=np.int64),c1=np.array([x[3]for x in entries],dtype=np.int64))
    return record

def lo(x):return math.nextafter(float(x.a),-math.inf)
def hi(x):return math.nextafter(float(x.b),math.inf)
def error(n,beta,steps,M):
    b=iv.mpf(beta);d=b/steps
    return M*n*b*d*d*iv.exp(25*d)/16
def steps(n,beta,M,tolerance='0.001'):
    tol=iv.mpf(tolerance);left=0;right=max(1,int(beta))
    while hi(error(n,beta,right,M))>=lo(tol):left=right;right*=2
    while right-left>1:
        mid=(right+left)//2
        if hi(error(n,beta,mid,M))<lo(tol):right=mid
        else:left=mid
    return {'n':n,'beta':beta,'time_slices':right,'logZ_error_upper':hi(error(n,beta,right,M)),
            'exact_pair_gate_reflection_positive_rank':25,
            'history_dimension':'25^'+str(right),'usable_compressed_contraction':False}

def run():
    (ROOT/'data').mkdir(exist_ok=True);record=acquire_norm();M=record['used_norm_upper_integer']
    # Exact known highest-energy product vector in the ACTUAL uniform model.
    # Rescaling its tiny Gibbs weight can defeat relative order while leaving
    # every p>=2 Schatten norm and the purities arbitrarily little changed.
    n=128;b=iv.mpf(64)
    log_hs=-4*b*n-iv.mpf(n)/2*iv.log(5)
    result={'status':'LOCAL_ORDER_ACQUISITION_SUCCEEDS_WITHOUT_COMPRESSION',
            'local_nested_commutator_norm_upper':M,
            'seed_budgets':[steps(n,b,M)for n,b in [(128,64),(256,96),(512,128)]],
            'uniform_ferromagnetic_tail_example':{
                'n':n,'beta':64,'energy':4*n,'extra_decay_rate':16,
                'relative_HS_error_log10_upper':hi(log_hs/iv.log(10)),
                'all_p_ge_2_relative_error_log10_upper':hi(-4*b*n/iv.log(10)),
                'unavoidable_log_relative_order_error':1024,
                'limitation':'This constructs a mathematical accuracy boundary. It does not acquire the unknown Gibbs operator.'},
            'missing_operation':'A compressed uniform-chain representation with an acquired sufficient residual/tail bound and evaluated long-ring traces.'}
    (ROOT/'data/relative_order_bridge.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result

if __name__=='__main__':run()
