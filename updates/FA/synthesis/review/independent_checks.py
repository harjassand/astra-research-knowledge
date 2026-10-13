"""Internal exact rational and independent floating proof diagnostics.

No producer code is imported. Every fixture here is finite and synthetic.
These checks do not formally verify the universal theorems or physical models.
"""
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import itertools


def entropy(rho):
    eig = np.linalg.eigvalsh(rho)
    assert eig.min() > -2e-13
    eig = eig[eig > 1e-14]
    return float(-np.sum(eig*np.log(eig)))


def thermal():
    # In an abstract singlet/triplet basis the channel has no square roots.
    k0 = np.diag([1., .5, .5, .5])
    ps = np.diag([1., 0., 0., 0.])
    def channel(rho):
        return k0@rho@k0+.75*ps*np.trace(rho[1:,1:])
    def gain(rho):
        return entropy(channel(rho))-entropy(rho)
    def polynomial(y):
        return y**3*(4+3*y)-27
    assert polynomial(F(59,40)) > 0
    lo, hi = F(1), F(59,40)
    assert polynomial(lo) < 0
    for _ in range(80):
        mid = (lo+hi)/2
        if polynomial(mid) <= 0: lo = mid
        else: hi = mid
    assert polynomial(lo) <= 0 < polynomial(hi)
    y = float((lo+hi)/2); x = y/(1+y)
    rho = np.diag([1-x]+[x/3]*3)
    s = -math.log(1+.75*y)
    assert abs(gain(rho)-s) < 5e-15
    rng = np.random.default_rng(2026101311)
    gains = []
    convex_gaps = []
    twirl_gaps = []
    for _ in range(160):
        raw = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        a = raw@raw.conj().T; a/=np.trace(a)
        raw = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        b = raw@raw.conj().T; b/=np.trace(b)
        p = rng.random()
        convex_gaps.append(p*gain(a)+(1-p)*gain(b)-gain(p*a+(1-p)*b))
        xa = float(np.trace(a[1:,1:]).real)
        twirled = np.diag([1-xa]+[xa/3]*3)
        twirl_gaps.append(gain(a)-gain(twirled))
        gains.append(gain(a))
        assert convex_gaps[-1] > -2e-13
        assert twirl_gaps[-1] > -2e-13
        assert gains[-1] > s-2e-13
    c = (5-math.sqrt(13))/8
    return {'exact_positive_root_polynomial':'y^3*(4+3*y)-27',
            'exact_root_bracket':[str(lo),str(hi)],
            'conservative_entropy_penalty':'log(337/160)',
            'root_floating':y, 'minimum_entropy_gain_floating':s,
            'previous_kappa_penalty':math.log(13/4),
            'conservative_threshold_tau_floating':c/math.log(337/160),
            'exact_scalar_threshold_tau_floating':c/(-s),
            'random_state_cases':len(gains),
            'minimum_convexity_gap':min(convex_gaps),
            'minimum_twirl_gap':min(twirl_gaps)}


def singular_work():
    # For Gamma>0, G=C*Gamma C has exactly ker(C), so Hc kills
    # every zero-response vector: a quotient is automatically legitimate.
    gamma = np.diag([1.,2.,3.])
    c = np.array([[1,1,0],[0,0,1],[1,1,1]],complex)
    g = np.array([1.,0.,2.]); h = np.array([0.,1.,1.])
    H=(np.outer(g,h)-np.outer(h,g))/(2j)
    G=c.conj().T@gamma@c; Hc=c.conj().T@H@c
    null = np.array([1.,-1.,0.])
    assert np.max(np.abs(G@null)) < 1e-14
    assert np.max(np.abs(Hc@null)) < 1e-14
    return {'positive_damping_zero_response_quotient_safe':True}


def solve_exact(a, b):
    rows=[[F(v) for v in row]+[F(w)] for row,w in zip(a,b)]
    n=len(rows)
    for i in range(n):
        j=next(j for j in range(i,n) if rows[j][i])
        rows[i],rows[j]=rows[j],rows[i]
        pivot=rows[i][i]; rows[i]=[v/pivot for v in rows[i]]
        for j in range(n):
            if j!=i:
                scale=rows[j][i]
                rows[j]=[v-scale*w for v,w in zip(rows[j],rows[i])]
    return [row[-1] for row in rows]


def relative_endpoint():
    def killed(n,c):
        a=[[F(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i]=c+1+(i>0)
            if i>0: a[i][i-1]=-1
            if i+1<n: a[i][i+1]=-1
        b=[F(0)]*n; b[-1]=1
        return a,b
    records=[]
    for n in range(1,9):
        qmat,b=killed(n,F(1)); q=solve_exact(qmat,b)
        for c in [F(97,100),F(4100,4181),F(1,2)]:
            amat,b=killed(n,c); h=solve_exact(amat,b)
            # -G_E = Dq^-1 Q_c Dq + diag(1-c).
            minus_g=[[amat[i][j]*q[j]/q[i] for j in range(n)] for i in range(n)]
            for i in range(n): minus_g[i][i]+=1-c
            b_g=[F(v)/qi for v,qi in zip(b,q)]
            weighted=[[v-(1-c if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(minus_g)]
            mgf=solve_exact(weighted,b_g)
            assert mgf == [hi/qi for hi,qi in zip(h,q)]
            # The transformed process is independent of c.
            baseline_g=[[qmat[i][j]*q[j]/q[i] for j in range(n)] for i in range(n)]
            assert minus_g==baseline_g
            duration=solve_exact(minus_g,[1]*n)
            physical_duration=solve_exact(amat,[1]*n)
            assert all(v<=1/c for v in physical_duration)
            records.append({'n':n,'c':str(c),'relative_yield_exact':str(mgf[0]),
                            'tilted_mean_duration_exact':str(duration[0]),
                            'physical_mean_duration_exact':str(physical_duration[0])})
    durations=[]
    for n in [1,10,100,1000]:
        # Differentiate the exact recurrence at c=1.
        u0,u1=F(1),F(2); d0,d1=F(0),F(1)
        for _ in range(1,n):
            u0,u1,d0,d1=u1,3*u1-u0,d1,u1+3*d1-d0
        durations.append({'n':n,'tilted_mean_duration_floating':float(d1/u1),
                          'mean_duration_divided_by_n':float(d1/u1/n)})
    return {'exact_feynman_kac_cases':len(records),'cases':records,
            'conditioned_duration_growth':durations,
            'asymptotic_mean_duration_per_site':1/math.sqrt(5)}


def flux_current():
    records=[]
    for n,k in [(4,2),(5,2),(6,3)]:
        states=[sum(1<<i for i in c) for c in itertools.combinations(range(n),k)]
        index={x:i for i,x in enumerate(states)}; m=len(states)
        occ=np.array([[(x>>i)&1 for i in range(n)] for x in states])
        theta=.37; z=np.exp(1j*theta)
        T=np.zeros((m,m),complex); J0=np.zeros_like(T)
        for x,bits in enumerate(states):
            for i in range(n):
                j=(i+1)%n
                if (bits>>i)&1 and not (bits>>j)&1:
                    y=index[bits^(1<<i)^(1<<j)]
                    T[y,x]-=z; T[x,y]-=z.conjugate()
                    J0[y,x]+=1j*z; J0[x,y]-=1j*z.conjugate()
        assert np.max(np.abs(T@J0-J0@T)) < 2e-14
        alpha=k*(n-k)/(n*(n-1)); m0=np.vdot(J0,J0).real/(n*m)
        assert abs(m0-2*alpha) < 2e-14
        field=np.array([((7*i+3)%11)-5 for i in range(n)])
        E=occ@field+3*np.sum(occ*np.roll(occ,-1,axis=1),axis=1)
        de=E[:,None]-E[None,:]
        ham=np.sum(np.abs(occ[:,None,:]-occ[None,:,:]),axis=2)
        gamma=ham/2+(32/25)*de**2/(np.hypot(15/4,de)+15/4)
        mask=np.abs(J0)>1e-12
        resistance=np.sum(np.abs(J0[mask])**2*(gamma[mask]+de[mask]**2/gamma[mask]))/(n*m)
        W=max(1.,float(np.max(np.abs(de[mask]))))
        eye=np.eye(m); trace=eye.flatten(order='F')/math.sqrt(m)
        for eps in [.2,1.3]:
            H=np.diag(E)+eps*T
            B=np.diag(gamma.flatten(order='F'))-1j*(np.kron(eye,H)-np.kron(H.T,eye))
            aug=np.zeros((m*m+1,m*m+1),complex)
            aug[:-1,:-1]=B; aug[:-1,-1]=trace; aug[-1,:-1]=trace
            current=(eps*J0).flatten(order='F')
            response=np.linalg.solve(aug,np.r_[current,0j])[:-1]
            residual=np.linalg.norm(B@response-current)/np.linalg.norm(current)
            actual=float(np.vdot(current,response).real/(n*m))
            bare=eps**2*m0*m0/resistance; floor=.97*eps**2*alpha/W
            assert actual>=bare-1e-11 and bare>=floor-1e-11
            records.append({'n':n,'K':k,'bond_phase':theta,'epsilon':eps,
                            'actual_current':actual,'bare_bound':bare,
                            'source_matched_absolute_floor':floor,
                            'relative_solve_residual':float(residual)})
    return {'complex_flux_finite_cases':len(records),'cases':records}


def staggered_current():
    """Alternative quadratic-operator solve, not the worker's many-body builder."""
    records=[]
    for n,k in [(6,1),(6,2),(6,3),(8,3),(8,4),(10,5)]:
        eta=1.; t=1.; delta=6.; gamma=4.7
        twist=1 if k%2 else -1
        U=np.zeros((n,n),complex)
        for i in range(n): U[(i+1)%n,i]=twist if i==n-1 else 1
        T=-t*(U+U.conj().T); J0=1j*t*(U-U.conj().T)
        E=np.array([delta/2*(-1)**i for i in range(n)])
        D=np.diag(E); gaps=E[:,None]-E[None,:]
        widths=eta*(1-np.eye(n))+(gamma-eta)*(gaps/delta)**2
        alpha=k*(n-k)/(n*(n-1)); weight=alpha/n
        AD=lambda x:-1j*(D@x-x@D)
        AT=lambda x:-1j*(T@x-x@T)
        v=AT(AD(J0))
        assert np.max(np.abs(D@v-v@D))<2e-13
        assert abs(weight*np.vdot(v,v).real-8*delta**2*t**4*alpha)<2e-12
        assert np.max(np.abs(np.diag(v)))<2e-13
        f0=gamma*J0/(gamma**2+delta**2)
        g0=-AD(J0)/(gamma**2+delta**2)
        assert np.max(np.abs(widths*f0+AD(g0)-J0))<2e-14
        assert np.max(np.abs(widths*g0+AD(f0)))<2e-14
        for eps in [.01,.1,1.7]:
            H=D+eps*T; eye=np.eye(n)
            B=np.diag(widths.flatten(order='F'))-1j*(np.kron(eye,H)-np.kron(H.T,eye))
            trace=eye.flatten(order='F')/math.sqrt(n)
            aug=np.zeros((n*n+1,n*n+1),complex)
            aug[:-1,:-1]=B; aug[:-1,-1]=trace; aug[-1,:-1]=trace
            j=(eps*J0).flatten(order='F')
            x=np.linalg.solve(aug,np.r_[j,0j])[:-1]
            actual=float(weight*np.vdot(j,x).real)
            f=eps*f0; g=eps*g0
            A=lambda z:-1j*(H@z-z@H)
            functional=weight*(2*np.vdot(eps*J0,f)-np.vdot(f,widths*f)
                               +np.vdot(g,widths*g)+2*np.vdot(A(f),g)).real
            kinetic=2*eps**2*t*t*alpha*gamma/(gamma**2+delta**2)
            residual=B@((f+g).flatten(order='F'))-j
            assert np.max(np.abs(residual-eps**2*AT(g0).flatten(order='F')))<3e-14
            penalty=eps**4*8*delta**2*t**4*alpha/(eta*(gamma**2+delta**2)**2)
            ks=2*np.pi*(np.arange(n)+(0 if k%2 else .5))/n
            denominator=gamma+delta**2/(gamma+16*eps**2*t*t*np.cos(ks)**2/eta)
            fourier=alpha*np.mean(4*eps**2*t*t*np.sin(ks)**2/denominator)
            assert abs(actual-fourier)<2e-12
            assert abs(functional-kinetic)<2e-12
            assert -2e-12<=actual-kinetic<=penalty+2e-12
            records.append({'n':n,'K':k,'epsilon':eps,'actual':actual,
                            'kinetic':kinetic,'corrected_functional':float(functional),
                            'Fourier_response':float(fourier),
                            'residual_penalty':penalty,
                            'actual_error_over_residual_penalty':float((actual-kinetic)/penalty)})
    return {'alternative_one_particle_operator_solve_cases':len(records),'cases':records}


def sector_counterexample():
    states=[sum(1<<i for i in c) for c in itertools.combinations(range(4),2)]
    index={b:i for i,b in enumerate(states)}; n=len(states)
    def bond(i,j):
        a=[[F(0) for _ in range(n)] for _ in range(n)]
        for x,bits in enumerate(states):
            ni=(bits>>i)&1; nj=(bits>>j)&1
            a[x][x]+=F((1-2*ni)*(1-2*nj),4)
            if ni!=nj: a[index[bits^(1<<i)^(1<<j)]][x]+=F(1,2)
        return a
    h0=[[F(0) for _ in range(n)] for _ in range(n)]
    for b in [bond(0,1),bond(0,2),bond(1,3)]:
        h0=[[x+y for x,y in zip(rx,ry)] for rx,ry in zip(h0,b)]
    active=bond(0,1); h1=[[x+y for x,y in zip(rx,ry)] for rx,ry in zip(h0,active)]
    trial=index[12]  # bit positions0,1 active;2,3 collar.
    assert h0[trial][trial]==-F(1,4) and h1[trial][trial]==0
    shifted=[row[:] for row in h1]
    for x,bits in enumerate(states):
        shifted[x][x]+=100*(2-((bits>>2)&1)-((bits>>3)&1))+F(9,97)
    pivots=[]
    for i in range(n):
        p=shifted[i][i]; assert p>0; pivots.append(p)
        for j in range(i+1,n):
            for k in range(i+1,n):
                shifted[j][k]-=shifted[j][i]*shifted[i][k]/p
    assert F(1,4)-F(9,97)==F(61,388)
    return {'exact_sector_dimension':n,'positive_shift_pivots':[str(p) for p in pivots],
            'strong_energy_lower':'-9/97','weak_energy_upper':'-1/4',
            'difference_lower':'61/388'}


def rank_deficient_reachability():
    # Unequal A/B charge multiplicities, rank-deficient sigma and nontrivial
    # isometry completion: these are not the worker's equal-block full-rank tests.
    qa=np.array([0,0,1,2,2]); qb=np.array([2,1,1,1,0,0]); e=4
    rng=np.random.default_rng(2447603); rows=[]
    for _ in range(12):
        p=rng.random(3)+.1; p/=p.sum()
        psi=np.zeros((len(qa),len(qb)),complex)
        phi=np.zeros((len(qa),len(qb),e),complex)
        W=np.zeros((len(qa),e,len(qa)),complex)
        for q in range(3):
            ai=np.flatnonzero(qa==q); bi=np.flatnonzero(qb==2-q)
            bvec=rng.normal(size=len(bi))+1j*rng.normal(size=len(bi)); bvec/=np.linalg.norm(bvec)
            u=rng.normal(size=len(ai)*e)+1j*rng.normal(size=len(ai)*e); u/=np.linalg.norm(u)
            vectors=[u]
            # Complete within each charge block without altering its prescribed
            # Schmidt-support column.
            for basis in np.eye(len(ai)*e):
                if len(vectors)==len(ai): break
                v=basis.astype(complex)
                for z in vectors: v-=z*np.vdot(z,v)
                norm=np.linalg.norm(v)
                if norm>1e-12: vectors.append(v/norm)
                if len(vectors)==len(ai): break
            assert len(vectors)==len(ai)
            for col,a in enumerate(ai): W[ai,:,a]=vectors[col].reshape(len(ai),e)
            psi[ai[0],bi]=np.sqrt(p[q])*bvec
            phi[np.ix_(ai,bi,np.arange(e))]=np.sqrt(p[q])*u.reshape(len(ai),1,e)*bvec[None,:,None]
        ks=[W[:,r,:] for r in range(e)]
        omega=np.einsum('abe,cde->abcd',phi,phi.conj()).reshape(len(qa)*len(qb),-1)
        recovered=sum(np.outer((k@psi).ravel(),(k@psi).ravel().conj()) for k in ks)
        tp=sum(k.conj().T@k for k in ks)
        err=max(np.max(np.abs(recovered-omega)),np.max(np.abs(tp-np.eye(len(qa)))))
        charge=max(np.max(np.abs(k*qa[None,:]-qa[:,None]*k)) for k in ks)
        leak=np.linalg.norm(psi[(qa[:,None]+qb[None,:])!=2])
        assert err<2e-12 and charge==0 and leak==0
        rows.append({'recovery_normalization_error':float(err),'charge_commutator':float(charge)})
    return {'rank_deficient_unequal_block_cases':len(rows),'cases':rows}


def phase_flip_endpoint():
    records=[]
    for n in [1,2,5,10,20]:
        mu=F(n*(n+1),2)
        for zeta in [F(1,10),F(1,100)]:
            gamma=4*mu/zeta; rate=(gamma-1)/2
            c=4*gamma/(gamma*gamma+4)
            u0,u1=F(1),1+c
            for _ in range(1,n): u0,u1=u1,(2+c)*u1-u0
            target=1/u1
            assert c*mu<=zeta and target>=1-zeta
            # Static-rescaling comparator at rational squared amplitude.
            a_squared=mu/zeta-F(1,4)
            c_static=4/(1+4*a_squared)
            assert c_static*mu==zeta
            records.append({'n':n,'target_error':str(zeta),'gamma_exact':str(gamma),
                            'native_pulse_rate_exact':str(rate),
                            'failure_rate_slow_exact':str(c),
                            'actual_target_probability_exact':str(target),
                            'slow_mean_duration_upper_exact':str(mu),
                            'expected_native_pulses_times_epsilon_hop_squared_upper':str(rate*mu),
                            'static_comparator_amplitude_squared':str(a_squared)})
    return {'exact_phase_flip_endpoint_cases':len(records),'cases':records,
            'scope':'finite kinetic first-hit functional; no physical sink or finite-duration pulse proof'}


if __name__ == '__main__':
    out={'status':'PASS; internal finite diagnostics, not formal or external validation',
         'thermal_entropy_refinement':thermal(), 'singular_work':singular_work(),
         'relative_endpoint':relative_endpoint(),'parity_free_flux_current':flux_current(),
         'staggered_current_review':staggered_current(),
         'exact_fixed_sector_counterexample_review':sector_counterexample(),
         'rank_deficient_grouped_reachability':rank_deficient_reachability(),
         'finite_phase_flip_endpoint':phase_flip_endpoint()}
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
