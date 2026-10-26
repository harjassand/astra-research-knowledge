#!/usr/local/bin/python3
"""Frequency-dependent noise diagnostic and independent numerical audit.

This is a supplementary diagnostic on the original withheld fixtures, not a
new withheld cohort or a general theorem about thermal-noise spectroscopy.
"""
import sys
sys.dont_write_bytecode=True
import csv,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent


def uniformization(m,dt):
    # A nonnegative series for a Metzler exponential; einsum avoids the BLAS
    # matmul path that emitted warnings in the first run.
    rate=max(1.,float(np.max(-np.diag(m))))
    p=np.eye(len(m))+m/rate
    assert np.min(p)>=-1e-14
    term=np.eye(len(m)); acc=term.copy(); scale=math.exp(-rate*dt)
    normp=np.max(np.sum(np.abs(p),axis=1))
    for j in range(1,1000):
        term=np.einsum('ik,kj->ij',term,p,optimize=False)*(rate*dt/j)
        acc+=term
        ratio=rate*dt*normp/(j+1)
        tail=(scale*np.max(np.sum(np.abs(term),axis=1))*ratio/(1-ratio)
              if ratio<1 else np.inf)
        if tail<1e-15:return scale*acc,j,float(tail)
    raise RuntimeError("uniformization did not converge")


def main():
    fixtures=json.loads((HERE/'withheld_networks.json').read_text())
    rows=[]
    for f in fixtures:
        k=np.array(f['K']); c=np.array(f['C_diagonal']); n=len(k); v=n-1
        maxima=[]
        for floor in (0.,.01):
            r=np.linalg.inv(k); delta0=r[0,v]**2/(1+r[v,v])
            f1=r[0,0]-delta0
            q=delta0/(floor+f1)
            cov=q-math.log1p(q) if q>1e-4 else q*q/2-q**3/3+q**4/4
            baseline=cov+delta0*delta0/(floor+f1)
            best=(0.,None,None)
            for di,d in enumerate(f['loads']):
                for omega in f['omega']:
                    r=np.linalg.inv(k+np.diag(d)+1j*omega*np.diag(c))
                    delta=r[0,v]*r[v,0]/(1+r[v,v])
                    z0=r[0,0]; z1=z0-delta
                    var1=floor+z1.real
                    ratio_minus_one=delta.real/var1
                    assert var1>0 and ratio_minus_one>-1
                    q=ratio_minus_one
                    cov=q-math.log1p(q) if abs(q)>1e-4 else q*q/2-q**3/3+q**4/4
                    # Complex Gaussian Fourier-bin surrogate, with unit mean
                    # current amplitude and S_h=floor+Re Z_h. Units are scaled.
                    kl=cov+abs(delta)**2/var1
                    value=float(kl/baseline)
                    if value>best[0]:best=(value,di,omega)
            maxima.append(best)
        rows.append({'n':n,'kind':f['kind'],
                     'pure_FDT_surrogate_max_KL_divided_by_unloaded_DC':maxima[0][0],
                     'pure_FDT_best_load_index':maxima[0][1],'pure_FDT_best_omega':maxima[0][2],
                     'mixed_FDT_surrogate_max_KL_divided_by_unloaded_DC':maxima[1][0],
                     'mixed_FDT_best_load_index':maxima[1][1],'mixed_FDT_best_omega':maxima[1][2]})
    with (HERE/'spectral_noise_diagnostic.csv').open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

    transient=json.loads((HERE/'transient_data.json').read_text())
    audits=[]
    rng=np.random.default_rng(2026102606)
    for f in transient:
        k=np.array(f['K']);c=np.array(f['C_diagonal']);n=len(k);v=n-1
        for scenario in ('unloaded','loaded'):
            d=np.zeros(n) if scenario=='unloaded' else rng.exponential(1.,n)
            kp=k.copy();kp[v,v]+=1
            m=np.zeros((2*n+1,2*n+1))
            m[:n,:n]=-(k+np.diag(d))/c[:,None]
            m[n:2*n,n:2*n]=-(kp+np.diag(d))/c[:,None]
            m[v,n+v]=1/c[v];m[n,-1]=1/c[0]
            reference,terms,tail=uniformization(m,.5)
            standard=expm(m*.5)
            error=float(np.max(np.abs(reference-standard)))
            assert error<5e-13 and np.all(np.isfinite(standard))
            h=np.array(f['unloaded_operator'])
            assert np.all(np.isfinite(h))
            audits.append({'n':n,'scenario':scenario,'series_terms':terms,
                           'series_tail_bound_inf_norm':tail,
                           'max_entry_difference_expm_vs_nonnegative_series':error,
                           'all_saved_transient_entries_finite':True})
    with (HERE/'numerical_audit.csv').open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(audits[0]));w.writeheader();w.writerows(audits)
    print(json.dumps({'spectral_cases':len(rows),
                      'largest_pure_spectral_ratio':max(r['pure_FDT_surrogate_max_KL_divided_by_unloaded_DC'] for r in rows),
                      'largest_mixed_spectral_ratio':max(r['mixed_FDT_surrogate_max_KL_divided_by_unloaded_DC'] for r in rows),
                      'numerical_audit_cases':len(audits),
                      'worst_exponential_crosscheck_error':max(r['max_entry_difference_expm_vs_nonnegative_series'] for r in audits)},indent=2))


if __name__=='__main__':main()
