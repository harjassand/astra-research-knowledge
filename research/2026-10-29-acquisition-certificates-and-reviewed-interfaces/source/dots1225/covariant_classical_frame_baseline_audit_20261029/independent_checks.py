"""Independent algebra/finite-grid checks; not a hardware or diamond-SDP run."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import factorial, comb, pi
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent


def rotation(q):
    w, x, y, z = q
    n = sum(t*t for t in q)
    return [[(w*w+x*x-y*y-z*z)/n, 2*(x*y-w*z)/n, 2*(x*z+w*y)/n],
            [2*(x*y+w*z)/n, (w*w-x*x+y*y-z*z)/n, 2*(y*z-w*x)/n],
            [2*(x*z-w*y)/n, 2*(y*z+w*x)/n, (w*w-x*x-y*y+z*z)/n]]


def exact_variance():
    cases = []
    for q0 in [(1,0,0,0), (1,2,3,4), (2,-1,3,1), (0,1,1,0)]:
        R = rotation([F(q) for q in q0])
        vec = sum(R, [])
        assert sum(v*v for v in vec) == 3
        for eta in [F(0), F(1,100), F(1,10), F(1,2), F(99,100), F(1)]:
            alpha, g = 1/(8+eta), (1-eta)/(8+eta)
            sig = [[alpha*int(i==j)-g*vec[i]*vec[j]/3 for j in range(9)] for i in range(9)]
            assert sum(sig[i][i] for i in range(9)) == 1
            variance = sum(sig[i][i]*(1-sig[i][i]) for i in range(9))
            for i in range(9):
                for j in range(i+1,9):
                    pp = (sig[i][i]+sig[j][j]+2*sig[i][j])/2
                    pm = (sig[i][i]+sig[j][j]-2*sig[i][j])/2
                    assert 0 <= pp <= 1 and 0 <= pm <= 1 and pp+pm <= 1
                    assert (pp-pm)/2 == sig[i][j]
                    variance += 2*((pp+pm)/4-sig[i][j]**2)
            purity = sum(t*t for row in sig for t in row)
            assert purity == (8+eta*eta)/(8+eta)**2
            assert variance == 5-purity
            assert variance <= F(44,9) < F(81,4)
            cases.append({'quaternion_integers':q0, 'eta':str(eta), 'exact_m_times_tomography_mse':str(variance)})
    assert (F(128,3)+128)*F(81,4)/8 == 432
    assert F(128)*F(44,9)/8 == F(704,9)
    assert F(704,9)*45 == 3520
    return {'rational_state_cases':len(cases), 'exact_mse_identity':'(5-Tr(sigma^2))/m',
            'submitted_halfdiamond_constant':432, 'optional_improved_halfdiamond_constant':'704/9',
            'optional_N_record_constant':3520, 'cases':cases}


def perturbation_checks():
    rng = np.random.default_rng(867015)
    good = bad = 0
    worst_good_ratio = 0.0
    worst_pointwise_ratio = 0.0
    for eta in [0, .01, .1, .7, .999]:
        alpha, g = 1/(8+eta), (1-eta)/(8+eta)
        for level in [.01, .10, .249, .25, .251, .5, 1, 3]:
            for _ in range(20):
                R = np.array(rotation(rng.normal(size=4)))
                c = R.ravel()/np.sqrt(3)
                sig = alpha*np.eye(9)-g*np.outer(c,c)
                Z = rng.normal(size=(9,9)); Z = (Z+Z.T)/2
                Z *= level*g/np.linalg.norm(Z,2)
                E = np.linalg.norm(Z,2)
                vals, vv = np.linalg.eigh(sig+Z)
                v = vv[:,0]
                aligned = v*np.sign(np.dot(v,c))
                sine = np.sqrt(max(0,1-np.dot(v,c)**2))
                M = np.sqrt(3)*v.reshape(3,3)
                if np.linalg.det(M)<0: M=-M
                u, _, vh = np.linalg.svd(M)
                estimate = u@np.diag([1,1,np.linalg.det(u@vh)])@vh
                error = np.linalg.norm(estimate-R,'fro')**2
                assert error <= 8+1e-12
                assert error <= 128*(E/g)**2+3e-9
                worst_pointwise_ratio = max(worst_pointwise_ratio,error/(128*(E/g)**2))
                if level <= .25:
                    good += 1
                    assert sine <= E/(g-E)+2e-8
                    assert np.linalg.det(np.sqrt(3)*aligned.reshape(3,3))>0
                    assert error <= (128/3)*(E/g)**2+3e-9
                    worst_good_ratio=max(worst_good_ratio,error/((128/3)*(E/g)**2))
                else: bad += 1
    return {'seed':867015,'good_event_cases':good,'bad_event_cases':bad,
            'maximum_good_bound_ratio':worst_good_ratio,
            'maximum_pointwise_128_bound_ratio':worst_pointwise_ratio}


def grid(L):
    zz, ww = np.polynomial.legendre.leggauss(L+1)
    K=2*L+1
    matrices=[]; weights=[]
    for alpha in np.arange(K)*2*pi/K:
        ca,sa=np.cos(alpha),np.sin(alpha)
        for gamma in np.arange(K)*2*pi/K:
            cg,sg=np.cos(gamma),np.sin(gamma)
            for z,w in zip(zz,ww):
                t=np.sqrt(1-z*z)
                matrices.append([[ca*z*cg-sa*sg,-ca*z*sg-sa*cg,ca*t],
                                 [sa*z*cg+ca*sg,-sa*z*sg+ca*cg,sa*t],
                                 [-t*cg,t*sg,z]])
                weights.append(w/(2*K*K))
    return np.array(matrices),np.array(weights)


# Euler-polynomial variables: ca,sa,cg,sg,z,sqrt(1-z^2).
ZERO=(0,)*6
def mono(coef,*indices):
    ex=[0]*6
    for i in indices: ex[i]+=1
    return {tuple(ex):F(coef)}
def plus(a,b):
    out=defaultdict(F,a)
    for k,v in b.items():out[k]+=v
    return dict(out)
def mul(a,b):
    out=defaultdict(F)
    for u,v in a.items():
        for w,z in b.items():out[tuple(x+y for x,y in zip(u,w))]+=v*z
    return dict(out)
ENTRIES=[plus(mono(1,0,4,2),mono(-1,1,3)),plus(mono(-1,0,4,3),mono(-1,1,2)),mono(1,0,5),
         plus(mono(1,1,4,2),mono(1,0,3)),plus(mono(-1,1,4,3),mono(1,0,2)),mono(1,1,5),
         mono(-1,5,2),mono(1,5,3),mono(1,4)]
def circle_moment(p,q):
    if p%2 or q%2:return F(0)
    a,b=p//2,q//2
    return F(factorial(2*a)*factorial(2*b),4**(a+b)*factorial(a)*factorial(b)*factorial(a+b))
def haar_integral(poly):
    total=F(0)
    for (ca,sa,cg,sg,z,t),coef in poly.items():
        az=circle_moment(ca,sa)*circle_moment(cg,sg)
        if not az or z%2:continue
        # After both azimuthal averages, all surviving beta-sine exponents
        # are even. Thus the remaining integral is a rational polynomial.
        assert t%2==0
        beta=sum((F((-1)**j*comb(t//2,j),z+2*j+1) for j in range(t//2+1)),F(0))
        total+=coef*az*beta
    return total


def exhaustive_quadrature_check():
    L=5; mats,w=grid(L); flat=mats.reshape(len(mats),9)
    assert np.all(w>0) and abs(sum(w)-1)<2e-14
    cache={():{ZERO:F(1)}}
    count=0; worst=0.0; nonzero=0
    for degree in range(L+1):
        for indices in combinations_with_replacement(range(9),degree):
            if indices:cache[indices]=mul(cache[indices[:-1]],ENTRIES[indices[-1]])
            exact=haar_integral(cache[indices])
            approx=float(w@np.prod(flat[:,indices],axis=1)) if indices else float(sum(w))
            residual=abs(approx-float(exact))
            assert residual<5e-14
            count+=1; worst=max(worst,residual); nonzero+=int(exact!=0)
    assert count==comb(14,5)
    # Independent exact third-moment witness used by operational twirl test.
    trace=plus(plus(ENTRIES[0],ENTRIES[4]),ENTRIES[8])
    assert haar_integral(mul(mul(trace,trace),trace))==1
    return {'max_degree':L,'quadrature_nodes':len(w),'all_entry_monomials_tested':count,
            'nonzero_exact_moments':nonzero,'exact_reference':'Separate rational Euler integrals, not a higher quadrature',
            'maximum_absolute_residual':worst,'exact_integral_trace_R_cubed':'1'}


def operational_covariance_check():
    # N=1 finite binary estimator: measure Pc_I; output I on yes and a pi
    # z-rotation on no. It is deliberately not a good estimator. It exposes
    # the actual probability-times-output degree3 and gives nonzero kappa.
    A,w=grid(3); B=A; eta=.1; alpha=1/(8+eta); g=(1-eta)/(8+eta)
    Fz=np.diag([-1.,-1.,1.]); expected_kappa=-4*g/81
    residuals=[]; identity_residuals=[]
    for q in [(1,0,0,0),(1,2,3,4),(0,1,1,0),(3,-1,2,5)]:
        R=np.array(rotation(np.array(q,dtype=float)))
        C=np.einsum('aij,jk,blk->abil',A,R,B)
        trace=np.trace(C,axis1=2,axis2=3)
        p=alpha-g*trace*trace/9
        assert np.min(p)>=-1e-14 and np.max(p)<=1+1e-14
        D=p[:,:,None,None]*np.eye(3)+(1-p)[:,:,None,None]*Fz
        output=np.einsum('aji,abjk,bkl->abil',A,D,B)
        M=np.einsum('a,b,abij->ij',w,w,output)
        err=float(np.max(np.abs(M-expected_kappa*R)))
        assert err<3e-14
        residuals.append(err)
        relative_trace=np.einsum('ij,abij->ab',R,output)
        mse=np.einsum('a,b,ab->',w,w,6-2*relative_trace)
        identity_residuals.append(abs(mse-6*(1-expected_kappa)))
    # A finite Monte Carlo matrix is NOT certified depolarizing. A single
    # coherent rotation is a direct counterexample to interpreting MSE/8
    # as its diamond error without the exact twirl theorem.
    theta=.1
    proxy=float(np.sin(theta/2)**2); actual=float(np.sin(theta/2))
    assert actual>10*proxy
    return {'N_record_registers':1,'degree_per_SO3_factor':3,'quadrature_nodes_per_factor':len(w),
            'nontrivial_binary_instrument_kappa':expected_kappa,'unknown_frames_tested':len(residuals),
            'maximum_covariance_residual':max(residuals),'maximum_trace_mse_residual':max(identity_residuals),
            'coherent_counterexample':{'rotation_angle':theta,'mse_over_eight':proxy,'halfdiamond':actual}}


def finite_randomization_check():
    rng=np.random.default_rng(78145); tested=0; worst=0.0
    for b in [2,4,8,16,24]:
        h=2.**(-b)
        for _ in range(1000):
            u=rng.random(3)
            v=(np.floor(u*(2**b))+.5)/(2**b)
            aa,ga=2*pi*u[0],2*pi*u[1];ap,gp=2*pi*v[0],2*pi*v[1]
            z,zp=2*u[2]-1,2*v[2]-1
            beta,bp=np.arccos(z),np.arccos(zp)
            assert abs(beta-bp)<=pi*np.sqrt(h/2)+1e-12
            def one(a,b,g):
                ca,sa,cg,sg,z,t=np.cos(a),np.sin(a),np.cos(g),np.sin(g),np.cos(b),np.sin(b)
                return np.array([[ca*z*cg-sa*sg,-ca*z*sg-sa*cg,ca*t],
                                 [sa*z*cg+ca*sg,-sa*z*sg+ca*cg,sa*t],[-t*cg,t*sg,z]])
            error=np.linalg.norm(one(aa,beta,ga)-one(ap,bp,gp),2)
            assert error<=9*np.sqrt(h)+1e-12
            worst=max(worst,error/(9*np.sqrt(h)));tested+=1
    schedules=[]
    for N,delta in [(45,F(1,100)),(45000,F(1,1000)),(10**9,F(1,10**9))]:
        b=0
        while F(32*(N+1),2**(b//2))>delta:b+=2
        assert F(32*(N+1),2**(b//2))<=delta
        schedules.append({'N':N,'delta_twirl':str(delta),'bits_per_Euler_coordinate':b,'total_fair_bits':6*b})
    return {'seed':78145,'midpoint_coupling_cases':tested,'max_SO3_bound_ratio':worst,
            'integer_chosen_precision_schedules':schedules}


def exact_cap_and_metric_checks():
    rows=[]
    for N in [1,5,45]:
        L=(9*N+1)//2
        for eta in [F(0),F(1,10),F(1,2)]:
            q=(8+eta)/18
            abort=sum((F(comb(L,k))*q**k*(1-q)**(L-k) for k in range(N)),F(0))
            assert F(N)/q<=F(9*N,4)
            assert abort<=F(1,2)
            assert abort**7<=F(1,128)
            rows.append({'N':N,'eta':str(eta),'ordinary_call_cap':L,'readiness':float(1-abort)})
    metric=[]
    for kappa in [F(-1,3),F(0),F(1,2),F(1)]:
        pauli=[(1+3*kappa)/4]+[(1-kappa)/4]*3
        assert min(pauli)>=0 and sum(pauli)==1
        # Maximally-entangled input gives the Bell-diagonal Choi difference.
        # Pauli-mixture triangle inequality gives the identical diamond upper.
        choi_distance=(abs(pauli[0]-1)+sum(pauli[1:]))/2
        triangle_upper=sum(pauli[1:])
        assert choi_distance==triangle_upper==3*(1-kappa)/4
        assert choi_distance==F(6,8)*(1-kappa)
        metric.append({'kappa':str(kappa),'exact_halfdiamond':str(choi_distance)})
    return {'negative_binomial_cap_cases':rows,'exact_qubit_depolarizing_metric_cases':metric}


def main():
    result={'exact_tomography_variance':exact_variance(),'eigenvector_and_projection':perturbation_checks(),
            'quadrature_against_exact_Euler_integrals':exhaustive_quadrature_check(),
            'operational_covariance':operational_covariance_check(),
            'finite_randomization':finite_randomization_check(),
            'exact_caps_and_depolarizing_metric':exact_cap_and_metric_checks(),
            'scope':'Independent exact algebra and finite numerical diagnostics; not a certified finite-Monte-Carlo diamond norm or native execution.'}
    (ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
