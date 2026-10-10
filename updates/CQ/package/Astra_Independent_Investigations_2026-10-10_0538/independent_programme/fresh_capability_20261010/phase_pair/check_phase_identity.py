"""Small synthetic arithmetic check; not physical instrument validation."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np, json
from pathlib import Path

def interval(zp,zm,eta,a,b):
    if min(abs(zp),abs(zm))<=eta: return [0.,None]
    raw=np.angle(zm*np.conj(zp))
    phi=.5*raw
    e=.5*(np.arcsin(eta/abs(zp))+np.arcsin(eta/abs(zm)))
    lo=max(0.,phi-e); hi=min(np.pi/2,phi+e)
    if hi<=0 or lo>=np.pi/2: return None
    return [max(0.,a/b/np.tan(hi)),None if lo<=0 else a/b/np.tan(lo)]

def main():
    M=65536; N=4096; a=1.; b=.4; lam=.5; nu=2e-4
    th=2*np.pi*np.arange(M)/M; k=np.fft.fftfreq(M,1/M)
    H=(1+1j*.7*k)**-2*np.exp(-1j*.37*k)  # positive gamma-kernel + delay
    rows=[]
    rng=np.random.default_rng(20261010)
    for name in ('sigmoid','saturation','threshold'):
        for x in (.2,1.,3.,8.):
            c=lam*x+a
            def h(z):
                if name=='sigmoid': return 1/(1+np.exp(-2*(z-2)))
                if name=='saturation': return np.minimum(np.maximum((z-.3)/3,0),1)
                return (z>c).astype(float)
            z=[]
            for s in (1,-1):
                u=(lam+b*np.cos(th))*x+a*(1+s*np.sin(th))
                assert min(u)>0
                y=np.fft.ifft(np.fft.fft(h(u))*H).real
                ys=y[::M//N]
                noise=rng.uniform(-nu,nu,N)
                zn=np.mean((ys+noise-.5)*np.exp(-1j*th[::M//N]))
                z.append(zn)
            zp,zm=z
            phi=.5*np.angle(zm*np.conj(zp)); xhat=a/b/np.tan(phi)
            # BV<=2 and centered amplitude<=0.5 for a monotone static map into
            # [0,1] followed by positive unit-mass convolution. Fine-grid
            # simulation allowance below is explicit, not a formal FFT bound.
            eta=(2+np.pi)/N+nu+1e-4
            ci=interval(zp,zm,eta,a,b)
            covered=ci is not None and ci[0]<=x and (ci[1] is None or x<=ci[1])
            assert covered,(name,x,ci)
            naivephi=-np.angle(zp)
            rows.append({'response':name,'x':x,'estimate':float(xhat),'relative_error':float(abs(xhat/x-1)),'measured_fundamental_min':float(min(abs(zp),abs(zm))),'certificate_eta':float(eta),'interval':ci,'contains_truth':bool(covered),'uncancelled_single_scan_phase':float(naivephi),'true_encoded_phase':float(np.arctan2(a,b*x))})
    out={'description':'Twelve synthetic paired-wave checks with unknown nonlinear static response, common second-order low-pass lag, and pure delay. Not a hardware test and not a novelty claim. Exact theorem is in THEOREM_AND_PRIOR_BOUNDARY.md.','reference_grid':M,'samples_per_scan':N,'noise_bound':nu,'cases':rows}
    Path(__file__).with_name('phase_identity_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'max_relative_error':max(r['relative_error'] for r in rows),'all_intervals_cover':all(r['contains_truth'] for r in rows),'worst_relative_interval_width':max((r['interval'][1]-r['interval'][0])/r['x'] for r in rows if r['interval'][1] is not None)},indent=2))
if __name__=='__main__': main()
