"""Algebra/continuum checks, not measurements or a fitted aging explanation.

Exact Fraction checks: TN signs, memory-matrix rank, signed cross-response,
thermodynamic quadratic residual energy, clock-response gauge, and failure
of a generic coherent-ISF product formula. Numerical quadrature: a specified
finite-core Poisson displacement field and endpoint-vs-dose predictions.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import json
import math
import time
import numpy as np

HERE=Path(__file__).resolve().parent


def rank(matrix):
    a=[list(row) for row in matrix]
    r=0
    if not a:
        return 0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        lead=a[r][col]
        a[r]=[v/lead for v in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                c=a[i][col]
                a[i]=[u-c*v for u,v in zip(a[i],a[r])]
        r+=1
        if r==len(a):
            break
    return r


def determinant(matrix):
    a=[list(row) for row in matrix]
    ans=F(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:
            return F(0)
        if p!=j:
            ans=-ans;a[j],a[p]=a[p],a[j]
        lead=a[j][j];ans*=lead
        for i in range(j+1,len(a)):
            c=a[i][j]/lead
            for k in range(j+1,len(a)):
                a[i][k]-=c*a[j][k]
    return ans


def spectrum_checks():
    records=[];principal_checks=0
    for modes in range(1,8):
        q=[F(j+1,modes+2) for j in range(modes)]
        weights=[F(1,modes)]*modes
        def r(n):return sum(w*x**n for w,x in zip(weights,q))
        n=modes+1
        kernel=[[r(i+j)-r(i)*r(j) for j in range(1,n+1)]
                for i in range(1,n+1)]
        for i in range(1,n+1):
            for j in range(1,n+1):
                gram=sum(w*(x**i-r(i))*(x**j-r(j)) for w,x in zip(weights,q))
                assert kernel[i-1][j-1]==gram
        actual_rank=rank(kernel)
        assert actual_rank==modes-1
        # Exhaust all principal minors in a bounded submatrix. General PSD
        # is proved by the exact covariance identity, not these fixtures.
        bound=min(n,5)
        for size in range(1,bound+1):
            for indices in combinations(range(bound),size):
                assert determinant([[kernel[i][j] for j in indices] for i in indices])>=0
                principal_checks+=1
        records.append({'visible_rates':modes,'sampled_material_lags':n,
                        'exact_memory_matrix_rank':actual_rank})
    # A monotone positive CROSS-response need not have positive spectral
    # weights. R(t)=(6 z-z²)/5, z=2^-t, is positive and decreasing, but
    # K(1,1)<0. It embeds in a passive two-channel susceptibility: mode
    # coupling vectors (1,6),(1,-1) have PSD outer products; their cross
    # weights are +6,-1 and sum to5.
    r=lambda n:F(6,5)*F(1,2)**n-F(1,5)*F(1,4)**n
    cross_k=r(2)-r(1)**2
    assert cross_k<0
    assert all(0<r(n+1)<r(n)<=1 for n in range(20))
    passive_modes=[[[F(1),F(6)],[F(6),F(36)]],
                   [[F(1),F(-1)],[F(-1),F(1)]]]
    assert all(determinant(m)==0 and m[0][0]>0 for m in passive_modes)
    return {'positive_spectra':records,'principal_minors_checked':principal_checks,
            'passive_signed_cross_response_K11':str(cross_k),
            'signed_cross_response_scope':'Monotone positive cross-kernel can violate PSD without violating common clock or passivity.'}


def kovacs_and_energy_checks():
    q=[F(1,2),F(1,4),F(3,4)];w=[F(1,5),F(3,10),F(1,2)]
    r=lambda n:sum(a*b**n for a,b in zip(w,q))
    checks=0
    for u in range(1,5):
        delta1=F(-1,10);delta2=-delta1*r(u)
        for v in range(1,5):
            k=r(u+v)-r(u)*r(v)
            # k_eq=dXeq/dT, delta=T_after−T_before.
            departure=-(delta1*r(u+v)+delta2*r(v))
            assert departure/(-delta1)==k
            assert k==r(v+u)-r(v)*r(u)
            checks+=1
        for anchor in [r(u),F(1,3),F(2,3)]:
            residual=[delta1*(x**u-anchor) for x in q]
            energy=sum(a*x*x for a,x in zip(w,residual))/2
            formula=delta1**2*(r(2*u)-2*anchor*r(u)+anchor**2)/2
            variance_formula=delta1**2*(r(2*u)-r(u)**2+(r(u)-anchor)**2)/2
            assert energy==formula==variance_formula
            checks+=1
    # Same initial and final T: rescale the first jump for each material wait.
    net=F(-1,100)
    for u in range(1,5):
        d1=net/(1-r(u));d2=-net*r(u)/(1-r(u))
        assert d1+d2==net and d1*r(u)+d2==0
    ra=lambda n:(F(1,2)**n+F(1,4)**n)/2
    rb=lambda n:(F(1,2)**n+3*F(1,4)**n)/4
    u,v=1,3
    kba=lambda u,v:rb(u+v)-ra(u)*rb(v)
    antisym=kba(u,v)-kba(v,u)
    predicted=ra(v)*rb(u)-ra(u)*rb(v)
    assert antisym==predicted and antisym!=0
    return {'exact_step_sign_reciprocity_energy_checks':checks,
            'cross_anchor_antisymmetry':str(antisym),
            'cross_anchor_scope':'Nonzero cross-anchor asymmetry is compatible with a common clock and distinct frozen kernels.'}


def gauge_and_coherent_checks():
    tangent=[F(2),F(3),F(5)];response=[F(7),F(11),F(13)];shift=F(4,3)
    moved=[r-v*shift for r,v in zip(response,tangent)]
    wedges=[]
    for i,j in combinations(range(3),2):
        old=tangent[i]*response[j]-tangent[j]*response[i]
        new=tangent[i]*moved[j]-tangent[j]*moved[i]
        assert old==new
        wedges.append(str(old))
    # Exact coherent counterexample: two particles with cos(q r12)=1/2,
    # iid displacement signs. q*z_s=pi/3, q*z_t=2pi/3. Then
    # phi(q Delta z)=1/2 but the normalized coherent amplitude is1/3.
    cosine_r=F(1,2);phi_s=F(1,2);phi_t=F(-1,2);phi_delta=F(1,2)
    s_s=2+2*cosine_r*phi_s**2
    s_t=2+2*cosine_r*phi_t**2
    cross=2*phi_delta+2*cosine_r*phi_s*phi_t
    assert s_s==s_t
    coherent=cross/s_s
    assert coherent==F(1,3) and coherent!=phi_delta
    # Exact endpoint return still recovers the entire scattering amplitude,
    # regardless of the failed generic product formula.
    echo_cross=2+2*cosine_r*phi_s**2
    assert echo_cross/s_s==1
    return {'gauge_invariant_wedges':wedges,'coherent_normalized_correlation':str(coherent),
            'incorrect_generic_phi_delta':str(phi_delta),'exact_return_correlation':'1',
            'scope':'A coherent-scattering algebra counterexample, not a two-particle material model.'}


def collective_gaussian_exponents():
    # Independent check of root COLLECTIVE_OBSERVATION_GATE Eq1 and Eq3.
    # Q is a rational Gram matrix, hence a valid Gaussian covariance of
    # the scalar q-projected field. Validate every repeated-index term.
    vectors=[(F(1),F(0)),(F(1,3),F(2,3)),(F(-1,2),F(1,4))]
    q=[[sum(a*b for a,b in zip(u,v)) for v in vectors] for u in vectors]
    z1,z2=F(2,3),F(-1,2)
    pair_checks=0;four_checks=0
    for j in range(3):
        for k in range(3):
            variance=z1*z1*q[j][j]+z2*z2*q[k][k]-2*z1*z2*q[j][k]
            direct=sum((z1*a-z2*b)**2 for a,b in zip(vectors[j],vectors[k]))
            assert variance==direct and variance>=0
            pair_checks+=1
    from itertools import product
    c=(1,-1,1,-1);h=(z1,z1,z2,z2)
    for indices in product(range(3),repeat=4):
        variance=sum(F(c[a]*c[b])*h[a]*h[b]*q[indices[a]][indices[b]]
                     for a in range(4) for b in range(4))
        direct=sum(sum(F(c[a])*h[a]*vectors[indices[a]][d] for a in range(4))**2
                   for d in range(2))
        assert variance==direct and variance>=0
        four_checks+=1
    # Proxy lifting gate: mean strain B misses a zero-mean mode e=(1,-1)
    # that is visible to A, so no finite ||Ae||<=k||Be|| bound is possible.
    b=[[F(1),F(1)]];a=[[F(1),F(-1)]];e=[F(1),F(-1)]
    assert sum(x*y for x,y in zip(b[0],e))==0
    assert sum(x*y for x,y in zip(a[0],e))!=0
    assert rank(b+a)>rank(b)
    return {'exact_pair_variances':pair_checks,'exact_four_index_variances':four_checks,
            'scalar_mean_lifting_gate':'Fails on a zero-mean heterogeneous strain mode',
            'scope':'Conditional Gaussian observation algebra; no material-field identification or automatic Siegert.'}


def one_minus_sinc(x):
    x=np.asarray(x)
    x2=x*x
    series=x2*(1/6-x2*(1/120-x2*(1/5040-x2/362880)))
    return np.where(np.abs(x)<0.05,series,1-np.sinc(x/np.pi))


def finite_core_checks():
    # a=rho=1. hard core excludes r<a; a regular filled core changes the
    # small-argument coefficient but not analyticity or the scaling warning.
    points,weights=np.polynomial.legendre.leggauss(768)
    x=(points+1)/2;weights=weights/2
    def exponent(b):
        return float(4*np.pi*np.dot(weights,one_minus_sinc(b*x*x)/(x**4)))
    records=[]
    constant=8*math.pi*math.sqrt(2*math.pi)/15
    for b in [1e-3,1e-2,0.1,1,10,100,1000]:
        actual=exponent(b)
        quadratic=2*math.pi*b*b/3
        fractional=constant*b**1.5
        if b<=1:
            assert quadratic*(1-b*b/100)-1e-10<=actual<=quadratic+1e-10
        if b>=10:
            # Exact bounds from |sinc x|<=1/x in the tail integral.
            center=fractional-4*math.pi/3
            tolerance=4*math.pi/(5*b)
            assert center-tolerance-1e-6<=actual<=center+tolerance+1e-6
        local=(math.log(exponent(b*1.01))-math.log(exponent(b/1.01)))/(2*math.log(1.01))
        records.append({'dimensionless_b_over_a2':b,'exponent':actual,
                        'small_b_quadratic':quadratic,'intermediate_fractional':fractional,
                        'local_log_slope':local})
    # Same total variation2: open0→2, closed0→1→0. Calibrate forward0→1.
    q=0.7;forward=exponent(q)
    endpoint_open=math.exp(-exponent(2*q));endpoint_closed=1.0
    fixed_event_dose_open=fixed_event_dose_closed=math.exp(-2*forward)
    assert endpoint_closed>fixed_event_dose_closed
    return {'quadrature_records':records,
            'endpoint_model':{'open':endpoint_open,'closed':endpoint_closed},
            'matched_total_variation_event_dose_model':{'open':fixed_event_dose_open,'closed':fixed_event_dose_closed},
            'scope':'Specified hard-core Poisson field and two explicit kinematic alternatives. Not a fitted metallic-glass explanation or a formal quadrature certificate.'}


def main():
    started=time.perf_counter()
    result={'memory_kernel':spectrum_checks(),'kovacs_energy':kovacs_and_energy_checks(),
            'gauge_coherent':gauge_and_coherent_checks(),
            'collective_gaussian':collective_gaussian_exponents(),
            'finite_core_echo':finite_core_checks(),
            'status':'all assertions passed'}
    result['runtime_seconds']=time.perf_counter()-started
    (HERE/'aging_structural_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'exact_spectra':len(result['memory_kernel']['positive_spectra']),
                      'principal_minors':result['memory_kernel']['principal_minors_checked'],
                      'signed_cross_K11':result['memory_kernel']['passive_signed_cross_response_K11'],
                      'coherent_correlation':result['gauge_coherent']['coherent_normalized_correlation'],
                      'finite_core_log_slopes':[r['local_log_slope'] for r in result['finite_core_echo']['quadrature_records']],
                      'runtime_seconds':result['runtime_seconds']}))


if __name__=='__main__':
    main()
