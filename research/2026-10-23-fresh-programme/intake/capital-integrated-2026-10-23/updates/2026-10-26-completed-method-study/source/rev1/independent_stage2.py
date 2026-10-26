"""Fresh reviewer checks of stage2 additions, without importing candidate code."""
from pathlib import Path
import csv
import json
import math
import mpmath as mp
import numpy as np
from scipy.linalg import qr
from scipy.special import gammainc
import independent_checks as first

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(61928027)


def integration_terms(width):
    if np.isinf(width):
        return 1., 1., 2.
    return -np.expm1(-width), gammainc(2, width), 2*gammainc(3, width)


def curve_moments(grid, slopes, star_slopes):
    own_t = star_t = mean = second = cross = 0.
    for j, start in enumerate(grid):
        end = grid[j+1] if j+1 < len(grid) else np.inf
        width = end-start
        i0, i1, i2 = integration_terms(width)
        a, b = slopes[j], star_slopes[j]
        wt = math.exp(-start)
        mean += wt*(own_t*i0+a*i1)
        second += wt*(own_t**2*i0+2*own_t*a*i1+a*a*i2)
        cross += wt*(own_t*star_t*i0+(own_t*b+star_t*a)*i1+a*b*i2)
        if np.isfinite(width):
            own_t += a*width
            star_t += b*width
    return mean, second, cross


def q17():
    mp.mp.dps = 85
    rows = []
    for kval in ['1.05', '2.3', '13', '203', '2000']:
        k = mp.mpf(kval)
        rhs = -mp.log(1-1/k)-1/k
        lo, hi = mp.mpf(0), mp.mpf(1)
        for _ in range(300):
            mid = (lo+hi)/2
            if 2*(mp.atanh(mid)-mid) < rhs:
                lo = mid
            else:
                hi = mid
        v = (lo+hi)/2
        d = 2*v-1/k
        eta = mp.exp(-d)
        # Direct integrals over released energy's Exp(1) coordinate.
        tstar = lambda z: min(z,d)+max(z-d,mp.mpf(0))/k
        mean = mp.quad(lambda z:tstar(z)*mp.exp(-z), [0,d,mp.inf])
        second = mp.quad(lambda z:tstar(z)**2*mp.exp(-z), [0,d,mp.inf])
        measured = second/mean**2-1
        slacks, gaps = [], []
        for _ in range(30):
            grid = np.unique(np.r_[0.,float(d),RNG.uniform(0,6,18)])
            star_slopes = np.where(grid < float(d),1.,1/float(k))
            slopes = RNG.uniform(1/float(k),1,len(grid))
            if RNG.random() < .5:
                slopes = np.where(slopes < (1+1/float(k))/2,1/float(k),1.)
            m, s, cross = curve_moments(grid,slopes,star_slopes)
            slacks.append(cross-(1+float(v))*float(mean)*m)
            gaps.append(s/m**2-1-float(v))
        rows.append(dict(K=kval, CV=mp.nstr(mp.sqrt(v),20), threshold=mp.nstr(eta,20),
                         high_precision_cv2_error=mp.nstr(abs(measured-v),8),
                         conditional_expectation_boundary_error=mp.nstr(abs(d+1/k-(1+v)*mean),8),
                         minimum_functional_certificate_slack=min(slacks),
                         minimum_random_curve_cv2_gap=min(gaps)))
    return dict(cases=rows, random_nonmonotone_curves=150,
                max_high_precision_cv2_error=max(float(r['high_precision_cv2_error']) for r in rows),
                minimum_certificate_slack=min(r['minimum_functional_certificate_slack'] for r in rows),
                minimum_curve_gap=min(r['minimum_random_curve_cv2_gap'] for r in rows))


def mm(a,b):
    return np.einsum('ik,kj->ij',a,b,optimize=False)


def mv(a,v):
    return np.einsum('ij,j->i',a,v,optimize=False)


def free(ch,q,u):
    val = 0.
    for row in ch:
        w = sum(v*a for v,a in zip(row,q))
        vv = sum(v*a for v,a in zip(row,u))
        val += np.vdot(vv,np.linalg.solve(w,vv)).real
    return float(val)


def metric(a,h):
    w,v = np.linalg.eigh(a)
    assert min(w)>0
    hh = mm(mm(v.conj().T,h),v)
    result = 0.
    for i,x in enumerate(w):
        for j,y in enumerate(w):
            coefficient = 1/x if x==y else (math.log(x)-math.log(y))/(x-y)
            result += abs(hh[i,j])**2*coefficient
    return float(result)


def relative(a,b):
    w,v = np.linalg.eigh(a)
    z,u = np.linalg.eigh(b)
    assert min(w)>0 and min(z)>0
    logdiff = mm(v*np.log(w),v.conj().T)-mm(u*np.log(z),u.conj().T)
    return float(np.trace(mm(a,logdiff)).real)


def sparse_channel(m,n):
    while True:
        a = RNG.uniform(.1,1,(m,n))*(RNG.uniform(size=(m,n))<.6)
        if np.all(a.sum(axis=0)>0) and np.all(a.sum(axis=1)>0):
            return a/a.sum(axis=0)


def q28():
    rows, lower = [], []
    for n,mk,ml in [(3,4,3),(5,3,4),(7,5,4)]:
        bound = n-1+mk+ml
        d = bound+6
        for trial in range(4):
            raw = []
            for _ in range(n):
                z = RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d))
                raw.append(mm(z,z.conj().T)/d+.2*np.eye(d))
            root = np.linalg.cholesky(sum(raw))
            inverse = np.linalg.inv(root)
            q = [mm(mm(inverse,a),inverse.conj().T) for a in raw]
            u = [RNG.normal(size=d)+1j*RNG.normal(size=d) for _ in range(n-1)]
            u.append(-sum(u))
            k,l = sparse_channel(mk,n),sparse_channel(ml,n)
            vectors = u[:-1].copy()
            for channel in [k,l]:
                for row in channel:
                    w = sum(v*a for v,a in zip(row,q))
                    vv = sum(v*a for v,a in zip(row,u))
                    vectors.append(np.linalg.solve(w,vv))
            basis,upper,pivot = qr(np.column_stack(vectors),mode='economic',pivoting=True)
            rank = int(np.sum(abs(np.diag(upper))>abs(upper[0,0])*1e-11))
            basis = basis[:,:rank]
            qp = [mm(mm(basis.conj().T,a),basis) for a in q]
            up = [mv(basis.conj().T,a) for a in u]
            errors = [abs(free(ch,q,u)-free(ch,qp,up))/max(1,free(ch,q,u)) for ch in [k,l]]
            rows.append(dict(n=n,trial=trial,dimension_before=d,dimension_after=rank,bound=bound,
                             max_relative_compression_error=max(errors),
                             channel_zero_entries=int(np.sum(k==0)+np.sum(l==0))))
            if trial:
                continue
            prob = np.arange(1,n+1,dtype=float)
            prob /= prob.sum()
            goal = free(k,qp,up)/free(l,qp,up)
            convergence = []
            for eps in [1e-3,1e-7,1e-15]:
                ss,hh = [],[]
                for qi,ui,pi in zip(qp,up,prob):
                    si = np.zeros((rank+1,rank+1),complex)
                    si[:rank,:rank] = (1-eps)*qi/rank
                    si[-1,-1] = eps*pi
                    hi = np.zeros_like(si)
                    hi[:rank,-1],hi[-1,:rank] = ui,ui.conj()
                    ss.append(si)
                    hh.append(hi)
                channel_values,bounds = [],[]
                for ch in [k,l]:
                    value = 0.
                    wspec = []
                    for row in ch:
                        s = sum(v*a for v,a in zip(row,ss))
                        h = sum(v*a for v,a in zip(row,hh))
                        value += metric(s,h)
                        wspec.extend(np.linalg.eigvalsh(sum(v*a for v,a in zip(row,qp))))
                    wmin,wmax = min(wspec),max(wspec)
                    probs = ch@prob
                    delta = max(eps*(1+rank*probs/wmin))
                    bconst = math.log(2)+max(abs(math.log(w/(rank*p))) for w in [wmin,wmax] for p in probs)
                    scaled_error = abs(value/(2*rank*math.log(1/eps))-free(ch,qp,up))/free(ch,qp,up)
                    bound_error = (delta+bconst/math.log(1/eps))/(1-delta)
                    assert scaled_error<=bound_error+1e-8
                    bounds.append(dict(actual_relative_error=scaled_error,proved_bound=bound_error))
                    channel_values.append(value)
                record = dict(epsilon=eps,metric_ratio=channel_values[0]/channel_values[1],
                              free_ratio=goal,relative_error_bounds=bounds)
                if eps==1e-3:
                    schur = [math.sqrt(eps*pi*(1-eps)/(rank*np.vdot(ui,np.linalg.solve(qi,ui)).real))
                             for qi,ui,pi in zip(qp,up,prob)]
                    step = min(schur)/50
                    rho = [s+step*h for s,h in zip(ss,hh)]
                    values = []
                    for ch in [k,l]:
                        values.append(sum(relative(sum(v*a for v,a in zip(row,rho)),
                                                   sum(v*a for v,a in zip(row,ss))) for row in ch))
                    record.update(step=step,finite_entropy_ratio=values[0]/values[1],
                                  minimum_input_eigenvalue=min(np.linalg.eigvalsh(a)[0] for a in rho),
                                  equal_marginal_error=float(np.linalg.norm(sum(rho)-sum(ss))))
                convergence.append(record)
            lower.append(dict(n=n,reference_dimension=rank+1,allowed_dimension=bound+1,
                              nonuniform_input_prior=prob.tolist(),convergence=convergence))
    # Explicit zero-denominator edge case: L merges labels distinguished by K.
    l = np.array([[1.,1.,0.],[0.,0.,1.]])
    k = np.eye(3)
    q = [np.array([[1/3]]) for _ in range(3)]
    u = [np.array([1.]),np.array([-1.]),np.array([0.])]
    zero_case = dict(F_K=free(k,q,u),F_L=free(l,q,u))
    assert zero_case['F_K']>0 and zero_case['F_L']==0
    return dict(compressions=rows,explicit_witnesses=lower,zero_denominator_case=zero_case,
                maximum_compression_error=max(r['max_relative_compression_error'] for r in rows))


def q42():
    rows = []
    for cut in [True,False]:
        for trial in range(6):
            # The sole connection between stores in the cut case passes through terminal 2.
            edges = [(0,3,.7),(3,2,.6),(2,4,.5),(4,1,.9)]
            if not cut:
                edges.append((3,4,.8))
            order = RNG.permutation(len(edges))
            phases = [(float(RNG.uniform(.2,.7)),first.laplacian(5,[edges[j]])) for j in order]
            capacities = np.array([.7,1.3])
            y,ys,gap,residual = first.ode_response(phases,np.diag(capacities),3)
            forward,reverse = -y[1,0],-y[0,1]
            record = dict(terminal_cut=cut,trial=trial,forward=forward,reverse=reverse)
            if cut:
                assert abs(forward)<1e-11 and abs(reverse)<1e-11
            else:
                period = sum(dt for dt,ll in phases)
                integrated = sum(dt*ll for dt,ll in phases)
                delta = max(max(np.diag(ll)[3:]/capacities) for dt,ll in phases)
                floor = math.exp(-2*delta*period)*np.prod([-integrated[a,b] for a,b in [(0,3),(3,4),(4,1)]])/(period*np.prod(capacities))
                assert min(forward,reverse)>=floor
                record['reverse_floor'] = floor
            rows.append(record)
    # Reconstruct optimized ring circuits with the independent adaptive ODE solver.
    comparisons = []
    path = OUT/'replay_stage2/Q42/stage2/architecture_comparison.csv'
    for row in csv.DictReader(path.open()):
        if row['architecture']=='ordinary_one_body_control':
            continue
        share,period = float(row['fixed_conductance_share']),float(row['period'])
        fixed = share/3
        active = (1-share)/1.002
        ring = [(3,4),(4,5),(5,3)]
        phases = []
        for j in range(3):
            if row['architecture']=='gated_internal_ring':
                edges = [(v,v+3,fixed) for v in range(3)]
                edges += [(a,b,active if k==j else active*.001) for k,(a,b) in enumerate(ring)]
            else:
                edges = [(a,b,fixed) for a,b in ring]
                edges += [(v,v+3,active if v==j else active*.001) for v in range(3)]
            phases.append((period/3,first.laplacian(6,edges)))
        y,ys,gap,residual = first.ode_response(phases,np.eye(3)/3,3)
        directed = abs(-y[1,0]+y[2,0])
        comparisons.append(dict(architecture=row['architecture'],objective=row['objective'],
                                directional_excess_ode=directed,
                                discrepancy_from_record=abs(directed-float(row['directional_excess'])),
                                mean_conductance=sum(dt*np.trace(ll)/2 for dt,ll in phases)/period))
    mp.mp.dps = 100
    z = mp.mpf(800)
    r = mp.exp(-z)
    a = (1-r)/(3*z*(1+r+r*r))
    underflow = dict(float_reverse=math.exp(-800)/2400,
                     high_precision_reverse=mp.nstr(a*r,40),isolation=mp.nstr(1/r,40),
                     cooling_over_static=mp.nstr(a*(1+r)/(mp.mpf(2)/9),25))
    return dict(support_checks=rows,independent_architecture_integrations=comparisons,underflow=underflow,
                max_architecture_discrepancy=max(r['discrepancy_from_record'] for r in comparisons))


if __name__=='__main__':
    result = dict(seed=61928027,Q17=q17(),Q28=q28(),Q42=q42())
    assert result['Q17']['max_high_precision_cv2_error']<1e-65
    assert result['Q17']['minimum_certificate_slack']>=-1e-10
    assert result['Q17']['minimum_curve_gap']>=-1e-10
    assert result['Q28']['maximum_compression_error']<1e-9
    assert result['Q42']['max_architecture_discrepancy']<1e-9
    (OUT/'independent_stage2.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({
        'Q17':{k:v for k,v in result['Q17'].items() if k!='cases'},
        'Q28':{'maximum_compression_error':result['Q28']['maximum_compression_error'],
               'zero_denominator_case':result['Q28']['zero_denominator_case']},
        'Q42':{'max_architecture_discrepancy':result['Q42']['max_architecture_discrepancy'],
               'underflow':result['Q42']['underflow']}},indent=2))
