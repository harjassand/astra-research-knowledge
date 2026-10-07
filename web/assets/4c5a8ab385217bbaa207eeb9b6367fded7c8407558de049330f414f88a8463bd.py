"""Small dense-matrix checks of the written construction, not theorem proof."""
from pathlib import Path
import json
import numpy as np

rng = np.random.default_rng(91217)


def normw(x, omega):
    return np.sqrt(max(0., np.trace(omega @ x.conj().T @ x).real))


def gibbs(h):
    vals, u = np.linalg.eigh((h+h.conj().T)/2)
    vals = np.exp(vals-vals.max())
    return (u * (vals/vals.sum())) @ u.conj().T


def trace_distance(a, b):
    return np.abs(np.linalg.eigvalsh((a-b+(a-b).conj().T)/2)).sum()/2


def phases(vals, width):
    residues = np.unique(np.mod(vals, width))
    points = np.r_[0., residues, width]
    return [float((a+b)/2) for a, b in zip(points[:-1], points[1:]) if b>a]


def reference_pinching(logp, aa, width):
    omega = np.diag(np.exp(logp))
    best = None
    for offset in phases(logp, width):
        labels = np.floor((logp-offset)/width).astype(int)
        mask = labels[:,None] == labels[None,:]
        current = [a*mask for a in aa]
        cost = sum(normw(a-c, omega)**2 for a,c in zip(aa,current))
        if best is None or cost < best[0]:
            kp = offset + width*(labels+.5)
            ref = np.exp(kp-kp.max()); ref /= ref.sum()
            best = (cost, current, np.diag(ref), labels)
    return best


def commuting_grid(aa, omega, labels, width):
    dim, k = len(omega), len(aa)
    current = [a.copy() for a in aa]
    result, total_u, steps = [], np.eye(dim, dtype=complex), []
    for i in range(k):
        u, vals = np.zeros((dim,dim),dtype=complex), np.empty(dim)
        for label in np.unique(labels):
            ix = np.flatnonzero(labels == label)
            vv, uu = np.linalg.eigh(current[i][np.ix_(ix,ix)])
            u[np.ix_(ix,ix)] = uu
            vals[ix] = vv
        current = [u.conj().T@a@u for a in current]
        result = [u.conj().T@a@u for a in result]
        omega = u.conj().T@omega@u
        total_u = total_u@u
        best = None
        for offset in phases(vals, width):
            grid = np.floor((vals-offset)/width).astype(int)
            keys = list(zip(labels.tolist(),grid.tolist()))
            lookup = {key:j for j,key in enumerate(sorted(set(keys)))}
            nested = np.array([lookup[key] for key in keys])
            mask = nested[:,None] == nested[None,:]
            cost = sum(normw(current[j]-current[j]*mask,omega)**2
                       for j in range(i+1,k))
            if best is None or cost < best[0]:
                rounded = np.clip(offset+width*(grid+.5),-1,1)
                best = (cost,nested,mask,rounded)
        _, labels, mask, rounded = best
        bound = sum(normw(current[i]@current[j]-current[j]@current[i],omega)
                    for j in range(i+1,k))/width
        assert best[0] <= bound + 2e-12
        assert np.linalg.norm(current[i]-np.diag(rounded),2) <= width+2e-12
        result.append(np.diag(rounded))
        for j in range(i+1,k):
            current[j] = current[j]*mask
        steps.append(float(best[0]))
    return result, omega, total_u, steps


fixtures = []
for dim,k,span,perturb in [(4,1,1.,.01),(4,2,10.,.03),(8,3,100.,.03),
                           (8,3,1.,.01),(12,4,30.,.001),(8,2,100.,.2)]:
    pp = np.exp(np.linspace(0.,-span,dim)); pp /= pp.sum()
    omega, logp = np.diag(pp), np.log(pp)
    aa = []
    for _ in range(k):
        x = rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
        x = (x+x.conj().T)/2
        a = np.diag(rng.uniform(-.5,.5,dim)) + perturb*x
        a /= max(1.,np.linalg.norm(a,2))
        aa.append(a)
    sqrtw = np.diag(np.sqrt(pp))
    nu = max(np.linalg.norm(sqrtw@a-a@sqrtw,'fro') for a in aa)
    eta = max(normw(a@b-b@a,omega) for a in aa for b in aa)
    href = min(1.,nu**(1/3))
    cost, cc, omegap, labels = reference_pinching(logp,aa,href)
    assert cost <= 4*k*nu/href + 1e-12
    assert np.max(np.abs(np.log(np.diag(omegap))-logp)) <= href+1e-12
    d0 = max(normw(a-c,omegap) for a,c in zip(aa,cc))
    eta0 = max(normw(a@b-b@a,omegap) for a in cc for b in cc)
    assert eta0 <= np.exp(href/2)*eta+8*d0+1e-12
    hscore = min(1.,max(1e-10,eta+nu**(1/3))**(1/(2**k-1)))
    bb, opfinal, total_u, steps = commuting_grid(cc,omegap,labels,hscore)
    out_original = [total_u@b@total_u.conj().T for b in bb]
    score_error = max(normw(a-b,omegap) for a,b in zip(aa,out_original))
    comm = max(np.linalg.norm(a@b-b@a,'fro') for a in bb for b in bb)
    assert comm < 1e-12
    assert max(np.linalg.norm(opfinal@b-b@opfinal,'fro') for b in bb) < 1e-12
    bpar = rng.normal(size=k); bpar /= np.abs(bpar).sum()
    rho = gibbs(np.diag(logp)+sum(t*a for t,a in zip(bpar,aa)))
    sigma = gibbs(np.diag(np.log(np.diag(omegap)))+
                  sum(t*a for t,a in zip(bpar,out_original)))
    alpha = .5*np.exp(href+3)*(href+score_error)
    discrepancy = trace_distance(rho,sigma)
    assert discrepancy <= alpha+1e-12
    keys = list(zip(*[np.diag(b).real.round(12).tolist() for b in bb]))
    groups = {key:np.array([j for j,keyj in enumerate(keys) if keyj==key])
              for key in set(keys)}
    rho_f = total_u.conj().T@rho@total_u
    sigma_f = total_u.conj().T@sigma@total_u
    refdiag = np.diag(opfinal).real
    def decode(x):
        yy = np.zeros(dim)
        for ix in groups.values():
            prob = np.trace(x[np.ix_(ix,ix)]).real
            yy[ix] = prob*refdiag[ix]/refdiag[ix].sum()
        return np.diag(yy)
    fixed_error = trace_distance(decode(sigma_f),sigma_f)
    actual_error = trace_distance(decode(rho_f),rho_f)
    assert fixed_error < 2e-12
    assert actual_error <= 2*discrepancy+2e-12
    fixtures.append(dict(dim=dim,k=k,log_span=span,perturbation=perturb,
                         nu=nu,eta=eta,href=href,hscore=hscore,
                         reference_pinching_cost=cost,eta0=eta0,
                         score_weighted_error=score_error,commutator=comm,
                         comparison_error=discrepancy,comparison_bound=alpha,
                         sigma_fixed_error=fixed_error,archive_error=actual_error,
                         labels=len(groups),pinching_costs=steps))
tracial = []
for dim,k,perturb in [(12,3,.01),(24,3,.03),(24,4,.02)]:
    oo = np.eye(dim)/dim
    aa = []
    for _ in range(k):
        x = rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
        x = (x+x.conj().T)/(2*np.sqrt(dim))
        a = np.diag(rng.uniform(-.95,.95,dim)) + perturb*x
        a /= max(1.,np.linalg.norm(a,2))
        aa.append(a)
    eta = max(normw(a@b-b@a,oo) for a in aa for b in aa)
    hh = eta**(1/(2**k-1))
    bb, _, uu, steps = commuting_grid(aa,oo,np.zeros(dim,dtype=int),hh)
    error = max(normw(a-uu@b@uu.conj().T,oo) for a,b in zip(aa,bb))
    comm = max(np.linalg.norm(a@b-b@a,'fro') for a in bb for b in bb)
    assert comm < 2e-12
    tracial.append(dict(dim=dim,k=k,eta=eta,width=hh,
                        weighted_error=error,error_over_width=error/hh,
                        commutator=comm,pinching_costs=steps))
out = dict(status='finite dense-matrix diagnostics only',fixtures=fixtures,
           nonzero_pinching_tracial_fixtures=tracial)
Path(__file__).with_name('matrix_diagnostics.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
