#!/usr/bin/env python3
"""Independent raw-ANF check of top-digit forcing and q^6 deflation.

This checker uses chart Groebner smoothness and a truth-table transform as
independent competitors to the production Macaulay certificate and counter.
It intentionally tests only small instances that permit exhaustive counts.
"""
from pathlib import Path
import itertools,json,random,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_local_algebra_agent','work_ring_count_agent','work_chain_root'):
    sys.path.insert(0,str(ROOT/folder))
from local_algebra_acquisition import ChainRing
from field_descent import extract_anf,polynomial_value,solve,linear_apply,gf_mul,gf_pow,bits
from acquired_chain_counter import ring_polynomial
from smooth_ring_counter import projective_smooth


def brute_sum(poly,n):
    truth=np.zeros(1<<n,dtype=np.uint8)
    for m in poly: truth[m]=1
    for i in range(n):
        stride=1<<i; blocks=truth.reshape(-1,2*stride)
        blocks[:,stride:]^=blocks[:,:stride]
    return (1<<n)-2*int(truth.sum(dtype=np.uint64))


def fpoly_value(poly,x):
    out=0
    for m,c in poly.items():
        if (m&x)==m: out^=c
    return out


def gradient_data(poly,h,e,mu=1):
    d=h.bit_length()-1; m=d*e; q=1<<d
    F=ChainRing(h,1); G=F.gram(); invG=[solve(G,1<<i) for i in range(d)]
    residue=sum(((1<<d)-1)<<(i*m) for i in range(3))
    gradients=[]
    for i in range(3):
        g={}
        for k in range(d):
            top=1<<(i*m+d*(e-1)+k)
            for term in poly:
                if term&top:
                    rem=term^top
                    if rem&~residue: raise ValueError('top derivative uses nonresidue coordinate')
                    small=sum(((rem>>(j*m))&((1<<d)-1))<<(j*d) for j in range(3))
                    g[small]=g.get(small,0)^invG[k]
        gradients.append({mask:c for mask,c in g.items() if c})
    if d==1:
        # Squares and linear monomials alias over F2. No ordinary coefficient
        # separation is needed: eight exact evaluations certify the unique
        # residue zero directly.
        zeros=[x for x in range(8) if not any(fpoly_value(g,x) for g in gradients)]
        if len(zeros)!=1: raise ValueError('binary residue gradient has no unique zero')
        return [(zeros[0]>>i)&1 for i in range(3)],None
    # Solve M*x^2+B*x from its values on a binary field basis. This is
    # injective for d>=2. It is deliberately distinct from the production
    # coefficient-level fitter.
    columns=[]
    for square in (True,False):
        for k in range(d):
            column=0
            for t in range(d):
                x=gf_mul(1<<t,1<<t,h) if square else 1<<t
                column^=gf_mul(1<<k,x,h)<<(d*t)
            columns.append(column)
    M=[[0]*3 for _ in range(3)]; B=[[0]*3 for _ in range(3)]
    c=[g.get(0,0) for g in gradients]
    for i in range(3):
        for j in range(3):
            target=sum((fpoly_value(gradients[i],1<<(d*j+t))^c[i])<<(d*t) for t in range(d))
            fit=solve(columns,target)
            if fit is None: raise ValueError('linearized gradient outside degrees one/two')
            M[i][j]=fit&(q-1); B[i][j]=fit>>d
    inverse_mu=gf_pow(mu,q-2,h)
    a=[gf_mul(B[1][2],inverse_mu,h),gf_mul(B[0][2],inverse_mu,h),gf_mul(B[0][1],inverse_mu,h)]
    for i in range(3):
        for j in range(3):
            expected=0 if i==j else gf_mul(mu,a[3-i-j],h)
            if B[i][j]!=expected: raise ValueError('gradient linear part has no common center')
    def homogeneous(i,x):
        j,k=[v for v in range(3) if v!=i]
        out=gf_mul(mu,gf_mul(x[j],x[k],h),h)
        for l in range(3): out^=gf_mul(M[i][l],gf_mul(x[l],x[l],h),h)
        return out
    if any(c[i]!=homogeneous(i,a) for i in range(3)):
        raise ValueError('gradient constant is not the common-center value')
    # Verify the entire F2-quadratic function, including cross terms.
    test_masks=[0]+[1<<i for i in range(3*d)]
    test_masks +=[(1<<i)|(1<<j) for i,j in itertools.combinations(range(3*d),2)]
    for mask in test_masks:
        x=[((mask>>(i*d))&(q-1))^a[i] for i in range(3)]
        for i in range(3):
            if fpoly_value(gradients[i],mask)!=homogeneous(i,x):
                raise ValueError('fitted gradient fails its full quadratic identity')
    H={(1,1,1):mu}
    for i in range(3):
        for j in range(3):
            ex=[0]*3; ex[i]+=1; ex[j]+=2
            if M[i][j]: H[tuple(ex)]=M[i][j]
    if not projective_smooth(H,h): raise ValueError('gradient has a projective zero')
    return a,M


def restrict_residue(poly,d,e,a):
    old=d*e; new=d*(e-1); result=set()
    for term in poly:
        mapped=0; survives=True
        for i in bits(term):
            component,local=divmod(i,old)
            if local<d:
                if not(a[component]>>local&1): survives=False; break
            else: mapped^=1<<(component*new+local-d)
        if survives:
            if mapped in result: result.remove(mapped)
            else: result.add(mapped)
    return result


def count_by_forcing(poly,h,e,trace=None):
    d=h.bit_length()-1; n=3*d*e; trace=[] if trace is None else trace
    if e==1:
        answer=brute_sum(poly,n); trace.append(dict(e=e,kind='field enumeration',n=n))
        return answer,trace
    a,M=gradient_data(poly,h,e)
    restricted=restrict_residue(poly,d,e,a)
    if e<=3:
        assert all(term.bit_count()<=2 for term in restricted)
        answer=brute_sum(restricted,3*d*(e-1))
        trace.append(dict(e=e,center=a,kind='quadratic restricted leaf',restricted_terms=len(restricted)))
        return answer,trace
    old=d*(e-1); new=d*(e-3); compressed=set()
    for term in restricted:
        mapped=0
        for i in bits(term):
            component,local=divmod(i,old)
            if local>=new: raise ValueError('one of the two discarded layers remains active')
            mapped^=1<<(component*new+local)
        compressed.add(mapped)
    trace.append(dict(e=e,center=a,kind='q^6 depth reduction',restricted_terms=len(restricted)))
    below,trace=count_by_forcing(compressed,h,e-3,trace)
    return (1<<(6*d))*below,trace


def run(binary_only=False):
    rng=random.Random(808218); rows=[]
    # This binary-coefficient cubic is smooth over every characteristic-two
    # extension: its gradients are YZ, Y^2+XZ, X^2+Z^2+XY.
    residue={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    cubics=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]
    cases=[(3,5,3),(3,7,3),(3,8,3)] if binary_only else [(7,2,3),(7,3,3),(7,4,3),(11,2,3)]
    for h,e,trials in cases:
        R=ChainRing(h,e); d=R.d; n=3*R.m; depth=(e+1)//3
        for trial in range(trials):
            H={ex:residue.get(ex,0)^sum(rng.randrange(1<<d)<<(d*j) for j in range(1,e)) for ex in cubics}
            H={ex:c for ex,c in H.items() if c}
            A=[rng.getrandbits(R.m) for _ in range(3)]
            ids=[i*R.m+j for i in range(3) for j in range(d*depth)]
            Q={0} if rng.randrange(2) else set()
            for i in ids:
                if rng.randrange(2): Q.add(1<<i)
            for i,j in itertools.combinations(ids,2):
                if rng.randrange(2): Q.add((1<<i)|(1<<j))
            def value(x):
                xs=[((x>>(i*R.m))&((1<<R.m)-1))^A[i] for i in range(3)]
                return R.functional(ring_polynomial(R,H,xs))^polynomial_value(Q,x)
            raw=extract_anf(value,n)
            began=time.perf_counter(); exact=brute_sum(raw,n)
            count,trace=count_by_forcing(raw,h,e)
            assert count==exact,(h,e,trial,count,exact)
            center=[a&((1<<d)-1) for a in A]
            assert trace[0]['center']==center
            at_center=sum(center[i]<<(i*R.m) for i in range(3))
            # The hidden quotient perturbation contributes only its value
            # at the full forced jet of the translated homogeneous phase.
            expected_sign=(-1)**polynomial_value(Q,sum(A[i]<<(i*R.m) for i in range(3)))
            if e%3==0: expected=expected_sign*(1<<(2*d*e))
            elif e%3==2: expected=expected_sign*(1<<(d*(2*e-1)))
            else: expected=None
            if expected is not None: assert exact==expected
            rows.append(dict(h=h,d=d,e=e,n=n,trial=trial,quotient_depth=depth,
                raw_anf=sorted(raw),translation=A,quadratic_quotient=sorted(Q),
                acquired_centers=trace,signed_count=exact,seconds=time.perf_counter()-began))
            print(json.dumps({k:rows[-1][k] for k in ('d','e','n','trial','signed_count','seconds')}),flush=True)
    out=dict(status='all exact assertions passed',cases=rows,
             methods='independent trace-dual derivative fit; chart Groebner smoothness; full Boolean truth-table transform',
             scope=('d=1 exact-eight-point residue acquisition and repeated deflation' if binary_only else
                    'd=2 mechanism edge checks and d=3 raw family checks; no initial centroid acquisition'))
    name='top_digit_binary_edge_results.json' if binary_only else 'top_digit_deflation_audit_results.json'
    Path(__file__).with_name(name).write_text(json.dumps(out,indent=2)+'\n')
    return out


if __name__=='__main__':
    result=run(binary_only='--binary-edge' in sys.argv)
    print(json.dumps(dict(status=result['status'],cases=len(result['cases']))))
