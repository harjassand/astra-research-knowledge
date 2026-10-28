"""Closed entangled-block purity readout with positive-arithmetic enclosures.

This reads the actual b4/ell1 Gibbs-block amplitude ansatz, not the unknown
uniform-chain Gibbs state. All local physical states and every closed-transfer
mode are included. See the proof for the IEEE arithmetic model and the
separate target-Gibbs residual obligation.
"""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as Q
import itertools,math,json,time
import numpy as np
import mpmath as mp
from scipy.sparse import csr_matrix
from seam_residual import BASE
U=Q(1,2**53)
TAU=math.ldexp(1.,-400)


def gamma(k):
    return k*U/(1-k*U)


def binary(value):
    return Q.from_float(float(value))


def upward(value,bits=100):
    return Q((value.numerator*2**bits+value.denominator-1)//value.denominator,2**bits)


def power2(k):
    return Q(2**k) if k>=0 else Q(1,2**(-k))


def positive_dot(A,B):
    """Explicit float64 products/additions; no BLAS sign/cancellation premise."""
    assert A.shape[1]==B.shape[0] and np.min(A)>=0 and np.min(B)>=0
    out=np.zeros((A.shape[0],B.shape[1]),dtype=np.float64)
    scratch=np.empty_like(out)
    for k in range(A.shape[1]):
        np.multiply(A[:,k:k+1],B[k:k+1,:],out=scratch)
        np.add(out,scratch,out=out)
    return out


def positive_sparse_dot(B,A):
    out=np.zeros_like(A);scratch=np.empty(A.shape[1])
    for row in range(B.shape[0]):
        for k in range(B.indptr[row],B.indptr[row+1]):
            np.multiply(B.data[k],A[B.indices[k],:],out=scratch)
            np.add(out[row,:],scratch,out=out[row,:])
    return out


def positive_generator(n):
    states=list(itertools.product(range(-2,3),repeat=n));lookup={q:i for i,q in enumerate(states)}
    rows=[];cols=[];values=[]
    sqrt6=math.sqrt(6)
    # This validates a rational relative enclosure of the only irrational
    # positive bond entry used in B=4(n-1)I-H_M.
    eb=Q(1,2**50)
    assert (binary(sqrt6)/(1+eb))**2<6<(binary(sqrt6)/(1-eb))**2
    root_upper=binary(sqrt6)/(1-eb)
    for a,b in itertools.product(range(-2,3),repeat=2):
        row=Q(4-a*b)
        for sign in (-1,1):
            if -2<=a+sign<=2 and -2<=b-sign<=2:
                square=(6-a*(a+sign))*(6-b*(b-sign))//4
                row+={4:Q(2),6:root_upper,9:Q(3)}[square]
        assert row<=10
    for col,q in enumerate(states):
        rows.append(col);cols.append(col);values.append(4*(n-1)-sum(q[i]*q[i+1]for i in range(n-1)))
        for i in range(n-1):
            a,b=q[i],q[i+1]
            for sign in (-1,1):
                if -2<=a+sign<=2 and -2<=b-sign<=2:
                    p=list(q);p[i]+=sign;p[i+1]-=sign
                    square=(6-a*(a+sign))*(6-b*(b-sign))//4
                    value={4:2.,6:sqrt6,9:3.}[square]
                    rows.append(lookup[tuple(p)]);cols.append(col);values.append(value)
    B=csr_matrix((values,(rows,cols)),shape=(5**n,5**n))
    masses=np.array([sum(q)for q in states])
    return B,masses,eb


def rescale(M):
    largest=float(np.max(M));assert largest>0 and math.isfinite(largest)
    k=math.frexp(largest)[1]
    out=np.ldexp(M,-k)
    assert np.count_nonzero(out)==np.count_nonzero(M)
    if np.any(out>0):assert out[out>0].min()>=np.finfo(float).tiny
    return out,k


def local_positive_exponential(n,beta,K=80):
    B,masses,eb=positive_generator(n);d=len(masses);scale=0
    while beta*10*(n-1)/2**scale>2:scale+=1
    step=beta/2**scale
    assert binary(step)==binary(beta)/2**scale
    P=np.eye(d);term=np.eye(d)
    row_nnz=int(np.max(np.diff(B.indptr)))
    for k in range(1,K+1):
        nz=term[term>0]
        if len(nz):assert float(nz.min())*2*step/k>np.finfo(float).tiny
        term=(step/k)*positive_sparse_dot(B,term);P+=term
    positive=P[P>0];assert len(positive)>0
    assert np.array_equal(P>0,masses[:,None]==masses[None,:])
    theta=(1+eb)**K*(1+gamma(2*row_nnz+3))**K*(1+gamma(K))-1
    # exp(x)<=8 for0<=x<=2. The fixed positive-tail estimate is exact rational.
    tail=Q(8*2**(K+1),math.factorial(K+1))
    assert Q(7)+Q(4,15)/(1-Q(1,3))<8
    theta+=(1+theta)*tail/binary(positive.min())
    theta=upward(theta)
    P,normalizer=rescale(P)
    for _ in range(scale):
        assert float(P[P>0].min())**2>np.finfo(float).tiny
        P=positive_dot(P,P);P,k=rescale(P);normalizer=2*normalizer+k
        theta=upward((1+theta)**2*(1+gamma(2*d))-1)
    return P,theta,dict(n=n,scale_squarings=scale,Taylor_degree=K,
        exact_relative_error_upper=str(theta),relative_error_upper=float(theta),
        normalizing_binary_exponent=normalizer,
        minimum_positive_entry=float(P[P>0].min()),
        full_physical_dimension=d,omitted_sectors=0)


def transfers(G,F):
    C=25
    assert float(G[G>0].min())**2*float(F[F>0].min())**2>np.finfo(float).tiny
    R=np.array([F.reshape(5,5,5,5)[a,:,b,:]for a in range(5)for b in range(5)])
    tensor=G.reshape(5,C,5,5,C,5)
    B1=np.zeros((5,5,5,5))
    for c in range(C):B1+=tensor[:,c,:,:,c,:]
    temp=positive_dot(R.reshape(25,25),B1.transpose(2,0,1,3).reshape(25,25))
    T1=temp.reshape(25,5,5).transpose(0,2,1).reshape(25,25)
    flat=tensor.transpose(0,2,3,5,1,4).reshape(625,C*C)
    second=flat.reshape(625,C,C).transpose(0,2,1).reshape(625,C*C)
    B2=positive_dot(flat,second.T).reshape((5,)*8)
    first=positive_dot(R.reshape(25,25),B2.transpose(2,4,0,1,3,5,6,7).reshape(25,-1))
    first=first.reshape(25,5,5,5,5,5,5)
    second=positive_dot(R.reshape(25,25),first.transpose(5,1,0,2,3,4,6).reshape(25,-1))
    T2=second.reshape(25,25,5,5,5,5).transpose(1,0,3,4,5,2).reshape(625,625)
    assert T1.min()>=0 and T2.min()>=0
    return T1,T2


class PositivePower:
    def __init__(self,M,exponent=0,lower=Q(1),upper=Q(1),absolute=Q(0)):
        self.M=M;self.exponent=exponent;self.lower=lower;self.upper=upper;self.absolute=absolute

    @classmethod
    def from_matrix(cls,M):
        out,k=rescale(M);out[out<TAU]=0
        return cls(out,k,absolute=binary(TAU))

    def multiply(self,other):
        d=len(self.M);assert d==len(other.M)
        # Clipping makes every nonzero product normal; dropped entries are
        # retained in an absolute error term, rather than uncounted modes.
        raw=positive_dot(self.M,other.M);out,k=rescale(raw);out[out<TAU]=0
        g=gamma(2*d)
        low=self.lower*other.lower/(1+g)
        high=self.upper*other.upper/(1-g)
        absolute=Q(d)*(self.upper*binary(self.M.max())*other.absolute+
                      other.upper*binary(other.M.max())*self.absolute+
                      self.absolute*other.absolute)*power2(-k)+high*binary(TAU)
        return PositivePower(out,self.exponent+other.exponent+k,low,high,absolute)


def trace_power_interval(T,m,input_theta):
    base=PositivePower.from_matrix(T);value=PositivePower(np.eye(len(T)))
    exponent=m
    while exponent:
        if exponent&1:value=value.multiply(base)
        exponent//=2
        if exponent:base=base.multiply(base)
    point=binary(np.trace(value.M));d=len(T);g=gamma(d)
    low=(value.lower*point/(1+g)-d*value.absolute)*power2(value.exponent)
    high=(value.upper*point/(1-g)+d*value.absolute)*power2(value.exponent)
    assert low>0
    # Local tensor enclosures are relative to the true positive tensor.
    low/=((1+input_theta)**m);high/=((1-input_theta)**m)
    assert low<=high
    return low,high


def interval_log(low,high):
    mp.iv.dps=80
    # Rebuild from exact numerator/denominator interval arithmetic, paying
    # the conversion itself instead of treating a rounded mpf as exact.
    a=mp.iv.mpf(low.numerator)/low.denominator
    b=mp.iv.mpf(high.numerator)/high.denominator
    return (math.nextafter(float(mp.iv.log(a).a),-math.inf),
            math.nextafter(float(mp.iv.log(b).b),math.inf))


def run():
    start=time.monotonic();rows=[]
    for beta in (.75,1.5,3.):
        G,tg,recordG=local_positive_exponential(4,beta)
        F,tf,recordF=local_positive_exponential(2,beta)
        T1,T2=transfers(G,F)
        arithmetic=gamma(4000)
        t1=upward((1+tg)*(1+tf)*(1+arithmetic)-1)
        t2=upward((1+tg)**2*(1+tf)**2*(1+arithmetic)-1)
        assert t1<1 and t2<1
        for n in (256,512):
            m=n//4;zlo,zhi=trace_power_interval(T1,m,t1);qlo,qhi=trace_power_interval(T2,m,t2)
            lo,hi=qlo/(zhi*zhi),qhi/(zlo*zlo)
            loglo,loghi=interval_log(lo,hi)
            row=dict(n=n,beta=beta,block_size=4,collar=1,
                normalized_ansatz_log_purity_lower=loglo,normalized_ansatz_log_purity_upper=loghi,
                log_width_upper=math.nextafter(loghi-loglo,math.inf),
                full_periodic_transfer_dimensions=[25,625],
                local_block_certificate=recordG,local_cut_certificate=recordF,
                target_Gibbs_purity_acquired=False)
            rows.append(row);print(n,beta,'ANSATZ logpurity',loglo,loghi,flush=True)
    result=dict(status='POSITIVE_ARITHMETIC_ENCLOSURES_FOR_ACTUAL_ENTANGLED_BLOCK_ANSATZ_READOUT',
        rows=rows,elapsed_seconds=time.monotonic()-start,
        arithmetic_model='IEEE754 binary64 round-to-nearest normal products; gamma bounds use conservative2d operation counts. Exact rational scalar enclosures and clipped-entry absolute tails are retained.',
        omitted_states_or_transfer_modes=0,
        warning='These are certified ansatz purities. The local target-Gibbs residual budget is not met; these values must not be called acquired uniform-Heisenberg purities.')
    (BASE/'results/BLOCK_PURITY_READOUT.json').write_text(json.dumps(result,indent=2)+'\n')
    print('elapsed',result['elapsed_seconds'])


if __name__=='__main__':run()
