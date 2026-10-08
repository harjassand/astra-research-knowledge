"""New compact-chart Gram, bounded-rank stability and thermal moment checks."""
import json
import math
from pathlib import Path

import numpy as np


def phase_grid(l, r):
    m = l+1
    return np.array([[r*np.exp(2j*math.pi*a/m),r*np.exp(2j*math.pi*b/m)]
                     for a in range(m) for b in range(m)])


def fourier_grid(l):
    m = l+1
    ix = [(a,b) for a in range(m) for b in range(m)]
    return np.array([[np.exp(2j*math.pi*(a*s+b*t)/m)/m
                      for s,t in ix] for a,b in ix])


def gram_cases():
    rows = []
    for l in (1,2,3,4):
        for r in (.4,.5):
            zz = phase_grid(l,r)
            d, mgrid = len(zz), l+1
            gram = np.exp(-2*r*r+zz.conj()@zz.T)
            pp = [sum(r**(2*n)/math.factorial(n)
                      for n in range(s,81,mgrid))*math.exp(-r*r)*mgrid
                  for s in range(mgrid)]
            spec = np.array([a*b for a in pp for b in pp])
            ff = fourier_grid(l)
            # Either Fourier convention orders conjugate residues; compare spectra.
            actual = np.sort(np.linalg.eigvalsh(gram))
            err = float(np.max(np.abs(actual-np.sort(spec))))
            assert err < 2e-12
            bound = d*math.exp(-2*r*r)*r**(4*l)/math.factorial(l)**2
            assert spec.min() >= bound*(1-1e-12)
            assert np.abs(gram).min() >= math.exp(-4*r*r)-1e-12
            rows.append({'kind':'oscillator','L':l,'r':r,
                         'gram_spectrum_error':err,'gram_min':float(spec.min()),
                         'proved_gram_lower':bound})

            mcarrier = 4*l*l
            gg = ((mcarrier+zz.conj()@zz.T)/(mcarrier+2*r*r))**mcarrier
            residues = np.zeros((mgrid,mgrid))
            for n1 in range(mcarrier+1):
                for n2 in range(mcarrier-n1+1):
                    n3 = mcarrier-n1-n2
                    logp = (math.lgamma(mcarrier+1)-math.lgamma(n1+1)-
                            math.lgamma(n2+1)-math.lgamma(n3+1)+
                            (n1+n2)*math.log(r*r/(mcarrier+2*r*r))+
                            n3*math.log(mcarrier/(mcarrier+2*r*r)))
                    residues[n1 % mgrid,n2 % mgrid] += math.exp(logp)
            expected = d*residues.ravel()
            ferr = float(np.max(np.abs(np.sort(np.linalg.eigvalsh(gg))-
                                       np.sort(expected))))
            assert ferr < 5e-12
            fbound = bound/math.e
            assert expected.min() >= fbound*(1-1e-12)
            assert np.abs(gg).min() >= math.exp(-8*r*r)-1e-12
            rows.append({'kind':'finite_Sym','m':mcarrier,'L':l,'r':r,
                         'gram_spectrum_error':ferr,'gram_min':float(expected.min()),
                         'proved_gram_lower':fbound})
    return rows


def stability_cases():
    rows = []
    for l,r in ((1,.1),(1,.25),(2,.1),(2,.2)):
        zz = phase_grid(l,r)
        gg = np.exp(-2*r*r+zz.conj()@zz.T)
        ev,uu = np.linalg.eigh(gg)
        assert ev.min() > 0
        # Columns x_s form exactly the declared Gram, in their D-dimensional span.
        xx = (np.sqrt(ev)[:,None]*uu.conj().T)
        d = len(zz)
        b, g = float(np.abs(gg).min()), float(ev.min())
        # Highest frame eigenmodes first: states share the large scalar mode.
        xx = xx[::-1,:]
        for rank in (1,2):
            if rank > d/2:
                continue
            aa = []
            for start in range(0,d,rank):
                diag = np.zeros(d)
                diag[start:min(d,start+rank)] = 1
                aa.append(np.diag(diag))
            errors = []
            infid = []
            for s in range(d):
                rho = np.outer(xx[:,s],xx[:,s].conj())
                out = sum((a@rho@a for a in aa),np.zeros_like(rho))
                errors.append(.5*np.abs(np.linalg.eigvalsh(rho-out)).sum())
                infid.append(1-float(np.vdot(xx[:,s],out@xx[:,s]).real))
            eps = float(max(errors))
            assert max(infid) <= eps+1e-11
            if eps <= .5:
                assert eps >= (b*g/56)**2-1e-12
            lam = np.array([[np.vdot(xx[:,s],a@xx[:,s])
                             for s in range(d)] for a in aa])
            cap = 0.
            for a,v in zip(aa,lam[:,0]):
                cap += np.linalg.norm(a-v*np.eye(d),'fro')**2
            lower = (d-rank)*float(np.sum(np.abs(lam[:,0])**2))
            assert cap >= lower-1e-11
            assert cap <= 14*d*math.sqrt(eps)/(b*g)+1e-11
            rows.append({'L':l,'r':r,'Q':rank,'dimension':d,
                         'whole_trace_error':eps,'rank_stability_floor':(b*g/56)**2,
                         'scalar_distance':float(cap),'kernel_lower':lower})
    return rows


def cutoff_cases():
    rows = []
    for mu in (.25,1.,3.):
        for k in (2,6,12):
            p = [math.exp(-mu)*mu**n/math.factorial(n) for n in range(k+1)]
            delta = max(0.,1-sum(p))
            # Radial number vectors plus one aggregate tail give exact pure error.
            psi = np.sqrt(np.array(p+[delta]))
            rho = np.outer(psi,psi)
            out = rho.copy()
            out[-1,:] = 0
            out[:,-1] = 0
            out[0,0] += delta
            err = float(.5*np.abs(np.linalg.eigvalsh(rho-out)).sum())
            assert err <= 2*math.sqrt(delta)+1e-12
            if k+1 >= mu:
                chernoff = math.exp(-(k+1)*math.log((k+1)/mu)+(k+1)-mu)
                assert delta <= chernoff+1e-12
            rows.append({'mean':mu,'K':k,'missing_mass':delta,'whole_trace_error':err})
    return rows


def thermal_cases():
    dim = 120
    a = np.diag(np.sqrt(np.arange(1,dim)),1)
    rows = []
    for q,z,gamma in ((0.,.5,.2),(.25,.7,.1),(.6,1.,.1),(.6,.3,.2)):
        hh = 1j*(z*a.conj().T-z*a)
        ee,uu = np.linalg.eigh(hh)
        disp = (uu*np.exp(-1j*ee))@uu.conj().T
        probs = (1-q)*q**np.arange(dim)
        rho = (disp*probs)@disp.conj().T
        actual = float(np.exp(gamma*np.arange(dim))@np.diag(rho).real)
        predicted = ((1-q)/(1-q*math.exp(gamma))*
                     math.exp((math.exp(gamma)-1)*(1-q)*z*z/(1-q*math.exp(gamma))))
        error = abs(actual-predicted)
        assert error < 2e-9
        rows.append({'q':q,'z':z,'gamma':gamma,'finite_fock_moment':actual,
                     'exact_gaussian_formula':predicted,'moment_error':error})
    return rows


def main():
    result = {'status':'FINITE-EVIDENCE',
              'scope':'Sixteen new coherent/multinomial Gram cases, eight bounded-rank stability fixtures, nine coherent cutoff errors and four displaced thermal number moments only',
              'gram_cases':gram_cases(),'stability_cases':stability_cases(),
              'cutoff_cases':cutoff_cases(),'thermal_cases':thermal_cases(),
              'old_suites_rerun':False,'uniform_external_iid_or_novelty_validation':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v if not k.endswith('_cases') else len(v)
                      for k,v in result.items()},indent=2))


if __name__ == '__main__':
    main()
