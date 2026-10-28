"""Independent finite-matrix and exact-rational controls for the construction."""
import sys
sys.dont_write_bytecode=True
import itertools,json,time,math
from fractions import Fraction as Q
import numpy as np
import sympy as S
import mpmath as mp
from scipy.linalg import expm,svdvals
from block_purity_readout import (local_positive_exponential,transfers,
                                 trace_power_interval,interval_log,BASE)


def physical_spin(spin):
    m=np.arange(-spin,spin+1);d=len(m);z=np.diag(m);p=np.zeros((d,d))
    for i,a in enumerate(m[:-1]):p[i+1,i]=np.sqrt(spin*(spin+1)-a*(a+1))
    return np.kron(z,z)-(np.kron(p,p.T)+np.kron(p.T,p))/2


def apply_pair(M,gate,i,j,n,d):
    D=d**n;perm=[i,j]+[k for k in range(n)if k not in (i,j)]+[n]
    arr=M.reshape((d,)*n+(D,)).transpose(perm)
    arr=gate@arr.reshape(d*d,-1)
    return arr.reshape((d,)*n+(D,)).transpose(np.argsort(perm)).reshape(D,D)


def exact_power_controls():
    fixtures=[np.array([[.5,.25],[.125,.75]]),
        np.array([[.5,math.ldexp(1.,-500),.25],[0.,.75,.125],[.125,0.,.5]])]
    records=[]
    for T in fixtures:
        exact=S.Matrix([[S.Rational(*float(x).as_integer_ratio())for x in row]for row in T])
        for m in (1,3,7,64,128):
            lo,hi=trace_power_interval(T,m,Q(0));truth=S.trace(exact**m)
            truth=Q(int(S.numer(truth)),int(S.denom(truth)))
            assert lo<=truth<=hi
            records.append(dict(d=len(T),power=m,exact_fraction_enclosed=True,
                clipped_tiny_entry_present=bool(np.any((T>0)&(T<math.ldexp(1.,-400))))))
    return records


def source_index_control():
    beta=.75;G,_,rg=local_positive_exponential(4,beta);F,_,rf=local_positive_exponential(2,beta)
    T1,T2=transfers(G,F)
    h=physical_spin(2);I=np.eye(625)
    H0=sum(apply_pair(I,h,i,i+1,4,5)for i in range(3))
    exactG=expm(-beta*H0);exactF=expm(-beta*h)
    M=apply_pair(exactG,exactF,3,0,4,5)
    direct=float(np.sum(M*M.T)/np.trace(M)**2)
    loz,hiz=trace_power_interval(T1,1,Q(1,10**10))
    loq,hiq=trace_power_interval(T2,1,Q(1,10**10))
    lo,hi=loq/(hiz*hiz),hiq/(loz*loz)
    assert float(lo)<direct<float(hi)
    ratio=float(np.trace(T2)/np.trace(T1)**2)
    assert abs(ratio-direct)<2e-12
    mp.iv.dps=80;iv=mp.iv
    def log_fraction(q):return iv.log(iv.mpf(q.numerator)/q.denominator)
    k=rg['normalizing_binary_exponent']+rf['normalizing_binary_exponent']
    absolute1=(log_fraction(loz)+k*iv.log(2)-16*iv.mpf(3)/4,
               log_fraction(hiz)+k*iv.log(2)-16*iv.mpf(3)/4)
    absolute2=(log_fraction(loq)+2*k*iv.log(2)-32*iv.mpf(3)/4,
               log_fraction(hiq)+2*k*iv.log(2)-32*iv.mpf(3)/4)
    log1=math.log(float(np.trace(M)));log2=math.log(float(np.sum(M*M.T)))
    assert float(absolute1[0].a)<log1<float(absolute1[1].b)
    assert float(absolute2[0].a)<log2<float(absolute2[1].b)
    V=apply_pair(I,h,3,0,4,5)
    true2=float(np.trace(expm(-2*beta*(H0+V))))
    gt1=float(np.trace(apply_pair(expm(-2*beta*H0),expm(-2*beta*h),3,0,4,5)))
    alt2=float(np.sum(M*M.T))
    assert true2<=alt2<=gt1
    return dict(spin=2,n=4,full_physical_dimension=625,
                direct_density_purity=direct,closed_transfer_purity=ratio,
                difference=abs(ratio-direct),both_closed_trace_indices_verified=True,
                restored_absolute_log_trace1_interval=[float(absolute1[0].a),float(absolute1[1].b)],
                restored_absolute_log_trace2_interval=[float(absolute2[0].a),float(absolute2[1].b)],
                full_source_true_ALT2_GT1_control=[true2,alt2,gt1])


def dyson_controls():
    X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);J=np.array([[0.,1.],[-1.,0.]])
    rows=[]
    for beta in (.25,1.,2.):
        H=.7*Z+.3*X
        for rate in (.01,.1):
            E=rate*(.5*X+.3*J+.2*Z)
            B=expm(-beta*H/2);A=expm(beta*(-H/2+E));D=A-B
            eta=math.expm1(beta*svdvals(E)[0])
            ratios=[]
            for p in (1,2,4,np.inf):
                a,b=svdvals(D),svdvals(B)
                ratio=(a[0]/b[0])if p==np.inf else (np.sum(a**p)/np.sum(b**p))**(1/p)
                assert ratio<=eta+1e-13;ratios.append(float(ratio))
            rows.append(dict(beta=beta,rate=rate,Schatten_p=[1,2,4,'infinity'],
                             measured_relative_errors=ratios,rigorous_formula_bound=eta))
    return rows


def multiple_cut_identity():
    d=2;n=8;D=d**n;I=np.eye(D);h=physical_spin(.5);s=.25
    cuts=[3,7];H0=sum(apply_pair(I,h,i,i+1,n,d)for i in range(n-1)if i not in cuts)
    V=sum(apply_pair(I,h,i,(i+1)%n,n,d)for i in cuts)
    P=expm(-s*V/2);B=expm(-s*H0/2);A=P@B
    derivative=-V@A/2-P@H0@B/2
    global_residual=np.linalg.solve(A.T,(derivative+(H0+V)@A/2).T).T
    expected=np.zeros((D,D))
    for c in cuts:
        edge=expm(-s*apply_pair(I,h,c,(c+1)%n,n,d)/2)
        inverse=expm(s*apply_pair(I,h,c,(c+1)%n,n,d)/2)
        outside=(apply_pair(I,h,(c-1)%n,c,n,d)+
                 apply_pair(I,h,(c+1)%n,(c+2)%n,n,d))
        expected+=(outside-edge@outside@inverse)/2
    error=float(np.linalg.norm(global_residual-expected,ord=np.inf))
    assert error<2e-13
    return dict(control_spin=.5,n=n,cuts=cuts,
        global_vs_local_multiplicative_residual_infinity_difference=error,
        scope='Index/locality control only; not spin2 cold evidence.')


def run():
    start=time.monotonic()
    result=dict(status='EXACT_ARITHMETIC_AND_INDEPENDENT_FINITE_MATRIX_CONTROLS_PASS',
        exact_positive_power_controls=exact_power_controls(),
        actual_source_four_site_index_control=source_index_control(),
        noncommuting_Dyson_controls=dyson_controls(),
        disjoint_cut_locality_control=multiple_cut_identity(),
        elapsed_seconds=time.monotonic()-start,
        scope='Exact rational controls check rounding/clipped-tail propagation. Physical matrix controls independently check source trace indices and residual locality; they do not supply a target Gibbs purity.')
    (BASE/'results/INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in('exact_positive_power_controls','noncommuting_Dyson_controls')},indent=2))


if __name__=='__main__':run()
