"""Independent algebra/acquisition diagnostics for the two frozen packets.

No diagnostic below certifies a general full-law TV assertion.  The affine TV
calculation is exact up to scalar floating evaluation; the other law claims are
reviewed mathematically in REVIEW.md.  Copied producer code is imported only for
checks explicitly marked implementation checks.
"""
from pathlib import Path
import importlib.util
import itertools
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(8491337)


def load_copy(name, rel):
    import sys
    spec = importlib.util.spec_from_file_location(name, HERE / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def scalar_inverse():
    records = []
    max_equation_error = 0.
    max_critical_ratio = 0.
    for kap in [.2, .5, .8]:
        a = math.sqrt(1-kap*kap)
        for n in [0, 1, 4, 12, 28, 48]:
            T = np.diag(a * (np.arange(n+1)+2.))
            for j in range(1, n+1):
                T[j, j-1] = kap*math.sqrt((n-j+1)*j)
            coeff = np.array([(-kap/a)**j * math.sqrt(math.comb(n,j)) /
                              (a*(j+1)*(j+2)) for j in range(n+1)])
            err = np.max(np.abs(T @ coeff - np.eye(n+1)[0]))
            # Relative error is relevant for the exponentially large columns.
            max_equation_error = max(max_equation_error,
                                     err / max(1., np.max(np.abs(T @ np.diag(coeff)))))
            critical = np.linalg.solve(T, np.diag(a**(n-np.arange(n+1))))
            op = np.linalg.svd(critical, compute_uv=False)[0]
            max_critical_ratio = max(max_critical_ratio, op*2*a)
            lower = a**(-n-1)/(n+2)**2
            assert np.linalg.norm(coeff) >= lower*(1-1e-12)
            assert op <= (1+1e-10)/(2*a)
            records.append(dict(kappa=kap, degree=n, inverse_column_norm=float(np.linalg.norm(coeff)),
                                stated_lower=lower, critical_smoothed_operator_norm=float(op)))
    return dict(max_relative_recurrence_error=max_equation_error,
                max_critical_operator_norm_over_1_over_2a=max_critical_ratio, sectors=records)


def mehler_geometry():
    gram_error = 0.
    min_contraction = 1.
    min_reserve = 1.
    for kap in [.05, .3, .7, .95]:
        a = math.sqrt(1-kap*kap)
        for q in np.r_[np.geomspace(1e-7,.1,31), np.linspace(.1,.9,31),
                       1-np.geomspace(1e-7,.1,31)]:
            gram = np.array([
                [a, -kap*(1-q), kap*q*math.sqrt((1-q)/(1+q)), kap*math.sqrt(2*q/(1+q))],
                [0., q, math.sqrt((1-q)*(1+q)), 0.],
                [0., math.sqrt(2*q*(1-q)), -math.sqrt(2)*q*math.sqrt(q/(1+q)), math.sqrt((1-q)/(1+q))]
            ])
            gram_error = max(gram_error, float(np.max(np.abs(gram@gram.T-np.eye(3)))))
            B = np.array([[a,0.],[-kap*(1-q),q]])
            min_contraction = min(min_contraction, float(np.linalg.eigvalsh(np.eye(2)-B.T@B)[0]))
            rem = np.eye(2)-B@B.T-np.diag([kap*kap*q/2,q*(1-q)/2])
            min_reserve = min(min_reserve, float(np.linalg.eigvalsh(rem)[0]))
    assert gram_error < 2e-14 and min_contraction > -2e-14 and min_reserve > -2e-14
    return dict(gram_identity_max_error=gram_error,
                minimum_I_minus_BT_B_eigenvalue=min_contraction,
                minimum_derivative_reserve_eigenvalue=min_reserve)


def vector_inverse(d):
    # Independent finite Fock-space reconstruction, using a full matrix solve
    # for the resolvent, rather than the producer's recursive polynomial code.
    kap = .63
    a = math.sqrt(1-kap*kap)
    dim = 2*d
    basis = [v for v in itertools.product(range(6), repeat=dim) if sum(v)<=5]
    ix = {v:i for i,v in enumerate(basis)}
    num = len(basis)
    degz = np.array([sum(v[d:]) for v in basis])
    degg = np.array([sum(v[:d]) for v in basis])
    small = np.flatnonzero(degz+degg<=3)
    def action(f, axis, creation=False):
        out = np.zeros_like(f)
        for j,v in enumerate(basis):
            k = v[axis]
            if (creation and sum(v)<5) or (not creation and k):
                w = list(v); w[axis] += 1 if creation else -1
                out[ix[tuple(w)]] += math.sqrt(k+1 if creation else k)*f[j]
        return out
    def C(f):
        return sum((action(action(f,i), d+i, True) for i in range(d)), np.zeros_like(f))
    def div_matrix(M):
        return np.array([sum((action(M[i,j],d+j,True) for j in range(d)), np.zeros(num)) for i in range(d)])
    def D(u, source=False):
        return np.array([[action(u[i],j if source else d+j) for j in range(d)] for i in range(d)])
    def sym(M):
        return .5*(M+M.swapaxes(0,1))
    eye = np.eye(num)[:,small]
    transfer = C(eye)
    T = (a*(degz[:,None]+2)*eye+kap*transfer)[small]
    R = np.zeros((d,d,num))
    for i in range(d):
        for j in range(i,d):
            R[i,j,small] = RNG.normal(size=len(small)) / math.sqrt(len(small))
            R[j,i] = R[i,j]
    forcing = R*a**degg
    J0 = np.zeros_like(R)
    rhs = -forcing[:,:,small].reshape(d*d,-1).T
    sol = np.linalg.solve(T,rhs).T.reshape(d,d,-1)
    J0[:,:,small] = sol
    u = div_matrix(J0)
    du = D(u)
    dgu = D(u,True)
    F = forcing+sym(kap*dgu.swapaxes(0,1)+a*du.swapaxes(0,1)+a*J0)
    Q = np.zeros_like(R)
    for m in range(4):
        Fm = F*(degz==m)
        w = div_matrix(Fm)
        dw = D(w)
        Q += -Fm+(dw-dw.swapaxes(0,1))/(m+2)
    J = J0+Q/a
    lhs = sym(kap*dgu.swapaxes(0,1)+a*du.swapaxes(0,1)+a*J)
    eq = float(np.linalg.norm(lhs+forcing))
    diverr = float(np.linalg.norm(div_matrix(J)-u))
    centering = float(np.linalg.norm(u[:,degz==0]))
    assert max(eq,diverr,centering)<2e-12
    return dict(d=d, forcing_degree=3, equation_error=eq, divergence_error=diverr,
                conditional_centering_error=centering, J_norm=float(np.linalg.norm(J)),
                correction_norm=float(np.linalg.norm(u)), R_norm=float(np.linalg.norm(R)))


# A noncommuting, smooth conservative field with a fully analytic covariance.
A = np.array([[.18,.07,-.03],[.07,-.12,.02],[-.03,.02,.26]])
W = np.array([[1.,2.,-1.],[-2.,1.,2.]])
W /= np.linalg.norm(W,axis=1)[:,None]
COEFF = np.array([.27,.19])
P = np.einsum('ri,rj->rij',W,W)
L = float(np.linalg.norm(A,2)+COEFF.sum())


def field(x):
    return x@A.T+(np.sin(x@W.T)*COEFF)@W


def cosprod(mu1, mu2, n11, n22, n12, r, s):
    dot = float(W[r]@W[s])
    return .5*(math.exp(-.5*(n11+n22+2*n12*dot))*math.cos(mu1+mu2)+
                math.exp(-.5*(n11+n22-2*n12*dot))*math.cos(mu1-mu2))


def hessian_product_mean(m1,m2,n11,n22,n12):
    ans = A@A
    for r in range(2):
        ans += COEFF[r]*math.exp(-n11/2)*math.cos(float(W[r]@m1))*(P[r]@A)
        ans += COEFF[r]*math.exp(-n22/2)*math.cos(float(W[r]@m2))*(A@P[r])
    for r in range(2):
        for s in range(2):
            cp=cosprod(float(W[r]@m1),float(W[s]@m2),n11,n22,n12,r,s)
            ans += COEFF[r]*COEFF[s]*cp*(P[r]@P[s])
    return .5*(ans+ans.T)


def analytic_covariance():
    ans = A@A
    for r in range(2):
        ans += COEFF[r]*math.exp(-.5)*(A@P[r]+P[r]@A)
    for r in range(2):
        for s in range(2):
            dot=float(W[r]@W[s])
            es=math.exp(-1)*math.sinh(dot)
            ans += COEFF[r]*COEFF[s]*es*np.outer(W[r],W[s])
    return .5*(ans+ans.T)


def preimage_acquisition():
    # Entirely independent implementation, in a noncommuting 3D field.
    kap,b,beta=.45,.6,.65
    a=math.sqrt(1-kap*kap)
    delta2=(1-beta)*(1-b*b)/2
    delta=math.sqrt(delta2)
    y=np.array([.2,.4,-.3]); v=np.array([.5,-.8,.4])
    count=180000
    def target(order):
        nodes,weights=np.polynomial.legendre.leggauss(order)
        val=np.zeros((3,3))
        for t,w in zip((nodes+1)*b/2,weights/2):
            N=np.diag([1-t*t,1-b*b])-(kap*kap/(a*a))*np.outer([t,b],[t,b])
            val += w*hessian_product_mean(t*y/a,b*y/a,N[0,0],N[1,1],N[0,1])
        return b*b*val-kap*kap*np.eye(3)
    truth=target(56)
    quad_error=float(np.max(np.abs(truth-target(96))))
    seeds=RNG.normal(size=(count,3))
    t=b*(1+seeds[:,0]/np.linalg.norm(seeds,axis=1))/2
    n11=1-t*t/(a*a); n22=1-b*b/(a*a); n12=-kap*kap*t*b/(a*a)
    c11=n11-delta2; c22=n22-delta2
    Z1=RNG.normal(size=(count,3)); Z2=RNG.normal(size=(count,3))
    C1=np.sqrt(c11)[:,None]*Z1
    C2=(n12/np.sqrt(c11))[:,None]*Z1+np.sqrt(c22-n12*n12/c11)[:,None]*Z2
    center1=t[:,None]*y/a+C1; center2=b*y/a+C2
    swap=RNG.normal(size=count)>0
    first=np.where(swap[:,None],center1,center2)
    second=np.where(swap[:,None],center2,center1)
    calls=0
    def heat(center,vec):
        nonlocal calls
        norm=np.linalg.norm(vec,axis=1)
        unit=np.divide(vec,norm[:,None],out=np.zeros_like(vec),where=norm[:,None]!=0)
        z=RNG.normal(size=vec.shape)
        z-=np.sum(z*unit,axis=1)[:,None]*unit
        radius=delta*np.linalg.norm(RNG.normal(size=(count,3)),axis=1)
        base=center+delta*z
        calls+=2
        return norm[:,None]*(field(base+radius[:,None]*unit)-field(base-radius[:,None]*unit))/(2*radius[:,None])
    out=b*b*heat(second,heat(first,np.broadcast_to(v,(count,3)).copy()))-kap*kap*v
    se=out.std(axis=0,ddof=1)/math.sqrt(count)
    standardized=np.abs(out.mean(axis=0)-truth@v)/se
    ratio=float(np.max(np.linalg.norm(out,axis=1))/((b*b*L*L+kap*kap)*np.linalg.norm(v)))
    restore=max(float(np.max(np.abs(n11+kap*kap*t*t/(a*a)-(1-t*t)))),
                float(np.max(np.abs(n12+kap*kap*t*b/(a*a)))))
    assert quad_error<1e-12 and standardized.max()<5 and ratio<=1+1e-12 and calls==4
    return dict(samples=count, queries_per_execution=calls, quadrature_stability_error=quad_error,
                conditional_mean_errors=(out.mean(axis=0)-truth@v).tolist(),
                conditional_mean_standardized_errors=standardized.tolist(),
                largest_norm_over_pathwise_bound=ratio, restored_covariance_error=restore,
                kappa=kap,b=b,beta=beta, covariance_budget=(kap*kap/(a*a))*2*b*b/(1-b*b),
                supplied_starting_mean_acquired=False)


def covariance_acquisition(mod):
    exact=analytic_covariance()
    means=np.zeros((3,3)); se=np.zeros((3,3)); norms=[]; caps=[]
    count=90000
    for i in range(3):
        vec=np.zeros((count,3)); vec[:,i]=1
        oracle=mod.QueryOracle(field)
        ans=mod.covariance_action(oracle,vec,RNG)
        means[:,i]=ans.mean(axis=0)
        se[:,i]=ans.std(axis=0,ddof=1)/math.sqrt(count)
        norms.append(float(np.linalg.norm(ans,axis=1).max()/(L*L)))
        caps.append(oracle.queries_per_execution)
    zscores=np.abs(means-exact)/se
    assert max(caps)==min(caps)==4 and zscores.max()<5 and max(norms)<=1+1e-12
    return dict(samples_per_column=count, exact_covariance=exact.tolist(),
                matrix_mean_error=(means-exact).tolist(), standardized_errors=zscores.tolist(),
                largest_norm_over_pathwise_bound=max(norms), query_caps=caps)


def conditional_residual_correction():
    mod=load_copy('learning_l31_owned','owned_copies/L31/residual_action.py')
    kap=.5; a=math.sqrt(1-kap*kap)
    # Residual e_2(G)+.3 e_1(G)e_1(Z)+.2 e_2(Z), not a constant
    # matrix.  This independently checks the source/noise score and sign.
    T=np.diag(a*(np.arange(3)+2.))
    for j in range(1,3):
        T[j,j-1]=kap*math.sqrt((3-j)*j)
    coeff=np.array([1.,.3,.2])
    J=np.linalg.solve(T,-coeff*a**(2-np.arange(3)))
    def hermite(n,x):
        if n==0:return np.ones_like(x)
        if n==1:return x
        h0=np.ones_like(x);h1=x.copy()
        for m in range(1,n):
            h0,h1=h1,(x*h1-math.sqrt(m)*h0)/math.sqrt(m+1)
        return h1
    def residual(yg,yz,v):
        val=hermite(2,yg)+.3*yg*yz+.2*hermite(2,yz)
        return val*v
    count=420000
    means=[]
    for g,z in [(.7,-.5),(-.4,1.2)]:
        G=np.full((count,1),g); Z=np.full((count,1),z)
        out,_=mod.correction(G,Z,kap,residual,RNG)
        truth=sum(math.sqrt(j+1)*J[j]*hermite(2-j,np.array(g))*hermite(j+1,np.array(z)) for j in range(3))
        se=float(out.std(ddof=1)/math.sqrt(count))
        err=float(out.mean()-truth)
        assert abs(err)<5*se
        means.append(dict(G=g,Z=z,mean_error=err,standard_error=se,exact_mean=float(truth)))
    G=RNG.normal(size=(count,1)); Z=RNG.normal(size=(count,1))
    out,_=mod.correction(G,Z,kap,residual,RNG)
    energy=float(np.mean(out*out)); truth=math.pi**2/(8*a*a)*float(coeff@coeff)
    energy_se=float(np.std(out*out,ddof=1)/math.sqrt(count))
    assert abs(energy-truth)<5*energy_se
    return dict(samples=count,polynomial_conditional_mean_checks=means,
                empirical_energy=energy,exact_energy=truth,energy_standard_error=energy_se)


def second_and_schedules(mod):
    errs=[]; caps=[]; min_reserve=1.
    for n in [1,2,7]:
        S=analytic_covariance(); tau=.4; eta=.3; sigma=math.hypot(tau,eta)
        M=tau*np.eye(3)-S/(2*tau*n)-S@S/(8*tau**3*n*n)
        Q=np.linalg.matrix_power(S,3)/(8*tau**4*n**3)+np.linalg.matrix_power(S,4)/(64*tau**6*n**4)
        errs.append(float(np.max(np.abs(S/n+M@M+eta*eta*np.eye(3)-sigma*sigma*np.eye(3)-Q))))
        for t in np.linspace(0,1,31):
            C=sigma*sigma*np.eye(3)-t*S/n+Q
            min_reserve=min(min_reserve,float(np.linalg.eigvalsh(C)[0]-eta*eta))
    affine=np.array([[.2,.1,0.],[.1,-.4,.08],[0.,.08,.5]])
    for strat in [False,True]:
        q=mod.QueryOracle(lambda x:x@affine.T+np.array([2.,-.3,.8]))
        mod.corrected_sampler(q,3,2,20,3,1.,RNG,strat)
        caps.append((q.queries_per_execution,3+4*2))
        q=mod.QueryOracle(lambda x:x@affine.T+np.array([2.,-.3,.8]))
        mod.second_corrected_sampler(q,3,2,2,20,3,1.,RNG,strat)
        caps.append((q.queries_per_execution,3+4*2+8*2))
    schedule_max=0.
    for d in [1,17,1024,10**6]:
        for epsilon in [.6,.1,.005]:
            for ratio in [.2,1.,3.]:
                n,k=mod.explicit_schedule(d,epsilon,ratio,1.)
                schedule_max=max(schedule_max,mod.safe_bound(d,n,k,ratio,1.)/epsilon)
    assert max(errs)<2e-14 and min_reserve>-2e-14 and all(x==y for x,y in caps) and schedule_max<=1+1e-12
    return dict(second_polynomial_max_error=max(errs), minimum_interpolation_reserve_slack=min_reserve,
                observed_and_required_query_caps=caps, max_schedule_bound_over_requested_epsilon=schedule_max)


def time_variance_and_matrix_geometry():
    v=(1-math.exp(-2))/2
    cstar=math.exp(-2)*(math.sinh(2)-2)/48
    iid=math.exp(-2)-1/8-3*math.exp(-4)/8
    rows=[]
    for k in [1,2,8,32,128]:
        nodes,weights=np.polynomial.legendre.leggauss(20)
        var=0.
        for j in range(k):
            t=(j+(nodes+1)/2)/k
            vals=np.exp(-1)*np.cosh(t)
            mean=float(weights@vals/2)
            var+=float(weights@((vals-mean)**2)/2)/k**2
        exact=math.exp(-2)*((.5+math.sinh(2)/4)/k-k*(math.cosh(1/k)-1)-math.sinh(2)/2*math.tanh(1/(2*k)))
        assert abs(var-exact)<3e-14
        assert var<=v*v/(12*k**3)*(1+1e-12)
        rows.append(dict(k=k,variance=var,closed_formula=exact,k_cubed_variance=k**3*var,
                         independent_over_stratified=(iid/k)/var))
    def M(t):
        out=A@A
        for r in range(2):
            out+=COEFF[r]*math.exp(-.5)*(A@P[r]+P[r]@A)
        for r in range(2):
            for s in range(2):
                out+=COEFF[r]*COEFF[s]*math.exp(-1)*math.cosh(t*float(W[r]@W[s]))*(P[r]@P[s])
        return .5*(out+out.T)
    grid=np.linspace(0,1,101)
    mineig=min(float(np.linalg.eigvalsh(M(u)-M(t))[0]) for t,u in zip(grid[:-1],grid[1:]))
    nodes,weights=np.polynomial.legendre.leggauss(48)
    integral=sum((w*M(t) for t,w in zip((nodes+1)/2,weights/2)),np.zeros((3,3)))
    cov_error=float(np.max(np.abs(integral-analytic_covariance())))
    strat_errors=[]
    for k in [1,4,16]:
        times=(np.arange(k)+RNG.uniform(size=k))/k
        val=sum((M(t) for t in times),np.zeros((3,3)))/k
        strat_errors.append(float(np.linalg.norm(val-integral,2)/(L*L/k)))
    assert mineig>-1e-14 and cov_error<1e-13 and max(strat_errors)<=1+1e-12
    return dict(c_star=cstar,iid_q_variance=iid,sine_variances=rows,
                minimum_monotone_matrix_increment_eigenvalue=mineig,
                covariance_integral_error=cov_error,
                stratified_matrix_error_over_pathwise_bound=strat_errors)


def affine_full_tv(mod):
    # Even-dimensional chi-square CDF uses a finite Poisson-tail expression.
    def cdf_chi2_even(x,d):
        if x<=0: return 0.
        logs=np.array([j*math.log(x/2)-math.lgamma(j+1) for j in range(d//2)])
        m=float(logs.max())
        log_survival=-x/2+m+math.log(float(np.exp(logs-m).sum()))
        return -math.expm1(min(0.,log_survival))
    rows=[]
    for d in [2,16,128]:
        alpha=.8; n=7; k=2; tau=1/math.sqrt(2)
        var=1+alpha**4/(4*tau*tau*n*n)
        threshold=d*math.log(var)/(1-1/var)
        tv=cdf_chi2_even(threshold,d)-cdf_chi2_even(threshold/var,d)
        bound=mod.safe_bound(d,n,k,alpha,1.)
        assert 0<=tv<=bound+1e-12
        rows.append(dict(d=d,variance=var,analytic_full_TV=tv,proved_general_bound=bound))
    return rows


def main():
    start=time.monotonic()
    mod=load_copy('learning_l68_owned','owned_copies/L68/covariance_sampler.py')
    out={
        'seed':8491337,
        'scalar_inverse':scalar_inverse(),
        'mehler_geometry':mehler_geometry(),
        'vector_inverse':[vector_inverse(d) for d in [1,2,3]],
        'four_query_preimage_noncommuting':preimage_acquisition(),
        'four_query_covariance_noncommuting':covariance_acquisition(mod),
        'conditional_residual_correction':conditional_residual_correction(),
        'second_correction_and_caps':second_and_schedules(mod),
        'time_stratification':time_variance_and_matrix_geometry(),
        'affine_analytic_full_TV':affine_full_tv(mod),
        'diagnostics_are_not_general_full_law_proofs':True,
    }
    out['execution_seconds']=time.monotonic()-start
    (HERE/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
