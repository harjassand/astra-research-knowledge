"""New independent checks for U39/U74; no unchanged Max endpoint is rerun.

All imports and executions use review-owned copies.  Numerical moments and
identity checks do not certify full-law TV claims; ULTRA_REVIEW.md contains
the mathematical reconstruction and exact scope.
"""
from pathlib import Path
from fractions import Fraction as F
import ast
import builtins
import hashlib
import importlib.util
import itertools
import json
import math
import runpy
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
OWN=ROOT/'owned_copies'
RNG=np.random.default_rng(7397427)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod


def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for i in range(n+1):
            for tail in compositions(n-i,k-1):yield (i,)+tail


def joint_fock_checks(d):
    # Independent dense coefficient representation, retaining every coefficient.
    # This does not import either producer's polynomial implementation.
    basis=[v for n in range(9) for v in compositions(n,2*d)]
    index={v:i for i,v in enumerate(basis)}
    nz=np.array([sum(v[d:]) for v in basis]); ng=np.array([sum(v[:d]) for v in basis])
    num=len(basis)
    maps={}
    for axis in range(2*d):
        for creation in [False,True]:
            src=[];dst=[];coef=[]
            for j,v in enumerate(basis):
                if (creation and sum(v)<8) or (not creation and v[axis]):
                    w=list(v);w[axis]+=1 if creation else -1
                    src.append(j);dst.append(index[tuple(w)])
                    coef.append(math.sqrt(v[axis]+1 if creation else v[axis]))
            maps[axis,creation]=(np.array(src),np.array(dst),np.array(coef))
    def act(arr,axis,creation=False):
        src,dst,coef=maps[axis,creation];out=np.zeros_like(arr)
        out[...,dst]=arr[...,src]*coef
        return out
    def rowdiv(M,source=False):
        return sum((act(M[:,j],j if source else d+j,True) for j in range(d)),np.zeros((d,num)))
    def div(v):
        return sum((act(v[j],d+j,True) for j in range(d)),np.zeros(num))
    def jac(v,source=False):
        return np.stack([act(v,j if source else d+j) for j in range(d)],axis=1)
    out=[]
    for n,m in [(0,0),(1,0),(0,2),(2,1),(2,2),(3,1)]:
        R=np.zeros((d,d,num));mask=(ng==n)&(nz==m)
        for i in range(d):
            for j in range(i,d):
                R[i,j,mask]=RNG.normal(size=int(mask.sum()))
                R[j,i]=R[i,j]
        R/=np.linalg.norm(R)
        dr=rowdiv(R);s=div(dr)
        u=np.stack([act(-s/((m+2)*(n+m+2)),d+i) for i in range(d)])
        dw=dr-np.stack([act(s,d+i) for i in range(d)])/(m+2)
        jw=jac(dw);B=(jw-jw.swapaxes(0,1))/(m+2)
        Dg=jac(u,True);Dz=jac(u)
        Jg=-Dg;Jz=-R-Dz.swapaxes(0,1)+B
        dive=float(np.linalg.norm(rowdiv(Jg,True)+rowdiv(Jz)-u))
        lin=Jz+Dz.swapaxes(0,1)
        syme=float(np.linalg.norm(.5*(lin+lin.swapaxes(0,1))+R))
        D2=float(np.sum(dr*dr));S2=float(s@s)
        exact=1+2*D2/(m+2)-(2/(m+2)**2+(n+m+3)/((m+2)*(n+m+2)**2))*S2
        j2=float(np.sum(Jg*Jg)+np.sum(Jz*Jz))
        du2=float(np.sum(Dg*Dg)+np.sum(Dz*Dz))
        assert max(dive,syme,abs(j2-exact))<2e-12
        assert du2<=1+1e-12 and np.sum(Dg*Dg)<=.25+1e-12 and j2<=3+1e-12
        assert not np.any(u[:,nz==0])
        out.append(dict(d=d,n=n,m=m,divergence_error=dive,symmetric_error=syme,
                        combined_norm_identity_error=abs(j2-exact),kernel_norm_squared=j2,
                        derivative_norm_squared=du2))
    return out


def derivative_checks():
    mod=load('ultra_owned_derivative',OWN/'U74/derivative_factory.py')
    y=np.array([.4]);v=w=np.ones(1);N=240000
    class Oracle:
        def __init__(self,fun):self.fun=fun;self.calls=0
        def __call__(self,x):self.calls+=1;return self.fun(x)
    # g=|x| is grad(x|x|/2), legal raw C^{1,1} potential, with a weak
    # Hessian jump.  Reference uses the sign convolution, not producer code.
    records=[]
    for b in [.6,1.]:
        oracle=Oracle(lambda x:np.abs(x)+1.7)
        ans=mod.factory(oracle,y,v,w,N,RNG,b)
        nodes,weights=np.polynomial.legendre.leggauss(200)
        low=math.sqrt(1-b*b);s=low+(1-low)*(nodes+1)/2
        rho=np.sqrt(1-s*s)
        truth=(1-low)/2*float(weights@(2*np.exp(-.5*(rho*y[0]/s)**2)/math.sqrt(2*math.pi)))
        se=float(ans.std(ddof=1)/math.sqrt(N));error=float(ans.mean()-truth)
        assert oracle.calls==3 and abs(error)<5*se
        records.append(dict(kind='absolute_value_raw_C11',b=b,queries=oracle.calls,
                            mean_error=error,standard_error=se,reference=truth,
                            observed_L2=float(np.sqrt(np.mean(ans*ans))),proved_L2_upper=2*(1-low)))
    d=3;y=np.array([.3,-.4,.7]);v=np.array([.4,.2,-.5]);w=np.array([-.1,.8,.2])
    A=np.array([[.3,.1,-.02],[.1,-.2,.03],[-.02,.03,.1]])
    oracle=Oracle(lambda x:x@A.T+np.array([1.,2.,-1.]))
    raw,anti=mod.factory(oracle,y,v,w,80000,RNG,.8,True)
    # The diagnostic computes raw 3 PLUS antithetic 8 = 11 total calls.
    # Its antithetic estimator by itself has the displayed eight-call form.
    err=float(np.max(np.abs(anti)))
    assert oracle.calls==11 and err<2e-14
    records.append(dict(kind='affine_antithetic',paired_diagnostic_total_queries=oracle.calls,
                        raw_estimator_queries=3,standalone_antithetic_queries=8,
                        max_antithetic_absolute_error=err))
    return records


def five_query_checks():
    mod=load('ultra_owned_five',OWN/'U74/five_query_sampler.py')
    class Oracle:
        def __init__(self,A,c):self.A=A;self.c=c;self.rows=0
        def __call__(self,x):self.rows+=len(x);return x@self.A.T+self.c
    A=np.array([[.19,.07,-.02],[.07,-.23,.04],[-.02,.04,.12]])
    c=np.array([1.2,-.3,.7]);N=20000;d=3;a=.13;eta=.4;b=math.sqrt(1-a*a)
    seed=771311
    ref=np.random.default_rng(seed)
    G=ref.normal(size=(N,d));H=ref.normal(size=(N,d));Z=ref.normal(size=(N,d))
    ref.normal(size=(N,d));V=ref.normal(size=(N,d))
    expect=c+(b*G+a*H)@A.T+Z-.5*b*b*(Z@(A@A).T)+eta*V
    oracle=Oracle(A,c)
    actual=mod.sample(oracle,N,d,a,eta,np.random.default_rng(seed))
    patherr=float(np.max(np.abs(actual-expect)))
    cov=(1+eta*eta)*np.eye(d)+a*a*A@A+(b**4/4)*np.linalg.matrix_power(A,4)
    assert oracle.rows==5*N and patherr<2e-12
    rows=[]
    for lam,dim,aa in [(.1,1,.01),(.3,8,.01),(.01,64,1e-7)]:
        bb=math.sqrt(1-aa*aa);ee=.5;C=math.log(1+ee**-2)/math.sqrt(2)
        candidate=min(1,C*(bb**3*lam**3*math.sqrt(dim)/math.sqrt(2)+bb**4*lam**4*dim/2)
                         +math.sqrt(2)*bb**4*lam**4*dim/(8*ee*ee)+aa*lam*math.sqrt(dim)/(2*ee))
        z=lam*lam/(5*(1+ee*ee))
        ordinary=min(1,.5*math.sqrt(math.expm1(-dim/2*math.log1p(-z*z))))
        rows.append(dict(lipschitz=lam,d=dim,a=aa,candidate_sufficient_TV=candidate,
                         ordinary_five_average_sufficient_TV=ordinary))
    return dict(queries_per_execution=oracle.rows/N,affine_pathwise_error=patherr,
                exact_affine_covariance=cov.tolist(),matched_certificate_comparisons=rows)


def noncommuting_conditional_correction():
    mod=load('ultra_owned_five_conditional',OWN/'U74/five_query_sampler.py')
    A=np.array([[.16,.04,-.01],[.04,-.18,.03],[-.01,.03,.09]])
    W=np.array([[1.,2.,-1.],[-2.,1.,2.]])
    W/=np.linalg.norm(W,axis=1)[:,None]
    P=np.einsum('ri,rj->rij',W,W);beta=np.array([.11,.17])
    a=.35;b=math.sqrt(1-a*a)
    G=np.array([.4,-.7,.1]);Z=np.array([.2,.5,-.4])
    def product_mean(t,rho):
        m1=rho*t*G;m2=b*t*G
        n1=1-rho*rho*t*t;n2=1-b*b*t*t;cross=rho*b*(1-t*t)
        M=A@A
        for j in range(2):
            M+=beta[j]*math.exp(-n1/2)*math.cos(float(W[j]@m1))*(P[j]@A)
            M+=beta[j]*math.exp(-n2/2)*math.cos(float(W[j]@m2))*(A@P[j])
        for j,k in itertools.product(range(2),repeat=2):
            dot=float(W[j]@W[k]);mu1=float(W[j]@m1);mu2=float(W[k]@m2)
            cp=.5*(math.exp(-.5*(n1+n2+2*cross*dot))*math.cos(mu1+mu2)
                   +math.exp(-.5*(n1+n2-2*cross*dot))*math.cos(mu1-mu2))
            M+=beta[j]*beta[k]*cp*(P[j]@P[k])
        return .5*(M+M.T)
    def reference(order):
        nodes,weights=np.polynomial.legendre.leggauss(order)
        ans=np.zeros((3,3))
        for t,wt in zip((nodes+1)/2,weights/2):
            for rho,wr in zip(b*(nodes+1)/2,weights/2):
                ans+=b*b*t*wt*wr*product_mean(t,rho)
        return -ans@Z
    truth=reference(24);quaderr=float(np.max(np.abs(truth-reference(40))))
    N=220000;gg=np.broadcast_to(G,(N,3));zz=np.broadcast_to(Z,(N,3))
    t=np.sqrt(RNG.uniform(size=N));center=t[:,None]*gg+np.sqrt(1-t*t)[:,None]*RNG.normal(size=(N,3))
    class Oracle:
        def __init__(self):self.rows=0
        def __call__(self,x):
            self.rows+=len(x)
            return x@A.T+(np.sin(x@W.T)*beta)@W+np.array([.7,-.2,.3])
    oracle=Oracle();u=-.5*mod.gamma_action(oracle,center,zz,a,b,RNG)
    se=u.std(axis=0,ddof=1)/math.sqrt(N);error=u.mean(axis=0)-truth
    assert quaderr<2e-13 and np.max(np.abs(error)/se)<5 and oracle.rows==4*N
    return dict(samples=N,queries_per_correction=oracle.rows/N,
                independently_integrated_conditional_mean=truth.tolist(),
                conditional_mean_error=error.tolist(),standardized_error=(error/se).tolist(),
                reference_quadrature_stability=quaderr)


def count_replays():
    folder=OWN/'U39'
    paths=['exact_certificate.py','learner.py','residual_validation.py']
    for p in paths:
        tree=ast.parse((folder/p).read_text())
        imports=[n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        imports += [q.name for n in ast.walk(tree) if isinstance(n,ast.Import) for q in n.names]
        assert all('plant' not in p for p in imports)
    outputs=['rational_certificate.json','residual_certificate.json']
    before={p:hashlib.sha256((folder/p).read_bytes()).hexdigest() for p in outputs}
    orig_import=builtins.__import__
    def guarded(name,*args,**kwargs):
        if name=='plant' or name.startswith('plant.'):
            raise RuntimeError('private plant forbidden in count-only replay')
        return orig_import(name,*args,**kwargs)
    builtins.__import__=guarded
    try:
        for p in paths:runpy.run_path(str(folder/p),run_name='__main__')
    finally:builtins.__import__=orig_import
    after={p:hashlib.sha256((folder/p).read_bytes()).hexdigest() for p in outputs}
    assert before==after
    data=json.loads((folder/'counts.json').read_text())
    resets=sum(t['shots'] for t in data['tables'])
    interventions=sum(t['shots']*len(t['actions']) for t in data['tables'])
    assert resets==7000000 and interventions==14000000
    second=json.loads((folder/'residual_counts.json').read_text())
    total_resets=resets+sum(t['shots'] for t in second['tables'])
    total_calls=interventions+sum(t['shots']*len(t['actions']) for t in second['tables'])
    assert total_resets==10500000 and total_calls==21000000
    exact=json.loads((folder/'rational_certificate.json').read_text())
    chosen=exact['selected']
    assert chosen['local_tv']['rational']=='4121523/210355000'
    return dict(private_plant_import_blocked=True,exact_outputs_byte_identical=True,
                primary_resets=resets,primary_native_interventions=interventions,
                both_datasets_total_resets=total_resets,both_datasets_total_interventions=total_calls,
                local_tv=chosen['local_tv'],one_macro_tv=chosen['one_macro_tv'],two_macro_tv=chosen['two_macro_tv'])


def interval_and_clock_challenges():
    # Independently compare the support-function formula to every box-simplex
    # vertex, including dimensions different from the fixture.
    max_error=0.
    for dim in [3,4,5]:
        for _ in range(15):
            p=RNG.dirichlet(np.ones(dim));radius=RNG.uniform(.001,.08,size=dim)
            low=np.maximum(0,p-radius);high=np.minimum(1,p+radius)
            support=0.
            for mask in itertools.product([False,True],repeat=dim):
                B=np.array(mask)
                support=max(support,min(high[B].sum(),1-low[~B].sum())-p[B].sum())
            vertex=0.
            for free in range(dim):
                others=[i for i in range(dim) if i!=free]
                for flags in itertools.product([0,1],repeat=dim-1):
                    q=np.zeros(dim)
                    for i,f in zip(others,flags):q[i]=high[i] if f else low[i]
                    q[free]=1-q.sum()
                    if low[free]-1e-14<=q[free]<=high[free]+1e-14:
                        vertex=max(vertex,.5*float(np.abs(q-p).sum()))
            max_error=max(max_error,abs(support-vertex))
    # Exact one-state process attains each clock/reuse bound.
    clocks=[]
    for delta,t,M in [(F(2,5),F(1,50),1),(F(1,3),F(2,7),3)]:
        gamma=1-delta;agree=delta/(delta+gamma*t)
        fail=gamma*t/(delta+gamma*t)
        assert agree+fail==1
        # Finite partial geometric sum plus exact tail = full agreement.
        r=gamma*(1-t);partial=delta*(1-r**100)/(1-r)
        tail=delta*r**100/(1-r)
        assert partial+tail==agree
        clocks.append(dict(delta=str(delta),t=str(t),M=M,one_failure=str(fail),
                           full_joint_failure=str(1-agree**M)))
    assert max_error<2e-14
    return dict(box_simplex_vertex_max_error=max_error,exact_clock_sharpness=clocks)


def overcomplete_challenge():
    fixture=json.loads((OWN/'U39/overcomplete_fixture.json').read_text())
    arr=lambda x:np.array([[float(F(v)) for v in row] for row in x])
    V=arr(fixture['V']);L=arr(fixture['right_inverse_L'])
    lam=float(F(fixture['lambda']));C=np.array([[1,0,0],[0,0,lam],[0,-lam,0]])
    K=arr(fixture['K_rotation'])
    # Translate to legal normalized preparation coordinates, independently.
    B=np.array([[1,1,1],[0,lam,0],[1,0,-lam*lam]])
    Vp=np.linalg.solve(B,V);Lp=L@B;Cp=np.linalg.solve(B,C@B)
    assert np.max(np.abs(np.ones(3)@Vp-np.ones(4)))<1e-13
    assert np.max(np.abs(Vp@Lp-np.eye(3)))<1e-13
    largest=0.;smallest=1.
    for _ in range(100):
        E=RNG.normal(size=(4,4));E-=E.mean(axis=0)
        E*=.001/np.max(np.abs(E))
        Kh=K+E
        residual=Cp@Vp-Vp@Kh
        corrected=Kh+Lp@residual
        bound=np.abs(Lp)@np.abs(residual)
        largest=max(largest,float(np.max(np.abs(Vp@corrected-Cp@Vp))))
        smallest=min(smallest,float(np.min(Kh-bound)))
        assert np.max(np.abs(corrected-Kh)-bound)<1e-13
        assert np.max(np.abs(corrected.sum(axis=0)-1))<1e-13
    assert largest<2e-13 and smallest>0
    return dict(legal_core_determinant=float(np.linalg.det(B)),
                exact_three_state_trace_square=str(1-2*F(13,20)**2),
                three_state_necessary_lower='1/3',nonzero_residual_trials=100,
                maximum_intertwining_error=largest,minimum_certified_positive_margin=smallest)


def main():
    result=dict(seed=7397427,
                joint_gauge=[row for d in [1,2,3] for row in joint_fock_checks(d)],
                raw_resolvent_derivative=derivative_checks(),
                five_query=five_query_checks(),
                noncommuting_joint_source_correction=noncommuting_conditional_correction(),
                count_replays=count_replays(),
                interval_clock=interval_and_clock_challenges(),
                overcomplete=overcomplete_challenge(),
                diagnostics_are_not_general_TV_certificates=True)
    (ROOT/'ultra_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
