"""Small fixed-seed tests, no new large Monte Carlo or external computation."""
import json,time
import numpy as np
from scipy.stats import beta
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import expm
from fragment_inverse import uniformized_forward,invert
from causal_clipped_inverse import clipped_inverse,numerical_defect,recover_with_precision,repair_prefix_mass
from reference_extension_test import density_forward


def true_cell_masses(h,n):
    edges=np.exp(-h*np.arange(n))
    z=.5*(edges[:-1]**2-edges[1:]**2)
    z+=.5*(beta.cdf(edges[:-1],4,3)-beta.cdf(edges[1:],4,3))
    return np.r_[0,z]


def main():
    rng=np.random.default_rng(105219)
    out={'seed':105219,'binning_convention':'positive ceiling bins; intact atom separate',
         'density_cap':2.,'precision_cases':[],'noisy_continuous_bins':[],'constant_check':[]}
    # Verify the displayed summed path-series constant numerically.
    from math import factorial
    for a in [.2,1.,2.]:
        gamma=1.3;V=5.
        direct=sum(a**r/factorial(r)*(gamma*(2*r-1)*(r+a)+(r-1)*V) for r in range(1,80))
        closed=gamma*(4*a*a*np.exp(a)+a)+V*((a-1)*np.exp(a)+1)
        out['constant_check'].append({'a':a,'difference':float(abs(direct-closed))})
    h=.04;n=101;t=2.;cap=2*h;k=true_cell_masses(h,n)
    for gamma in [1.3,.1,.02]:
        q=np.exp(-gamma*h);f=uniformized_forward(k,q,t)
        y=rng.poisson(f*100000)/100000;y[0]=f[0]
        kd,p,w=clipped_inverse(y,q,t,cap)
        dd,_,_=numerical_defect(kd,y,q,t,cap)
        st=time.perf_counter();kh,attempts,ok=recover_with_precision(y,q,t,cap);elapsed=time.perf_counter()-st
        out['precision_cases'].append({'gamma':gamma,'double_l1_error':float(sum(abs(kd-k))),
             'double_defect':dd,'success':ok,'seconds':elapsed,'attempts':attempts,
             'recovered_l1_error':float(sum(abs(kh-k))),
             'repaired_l1_error':float(sum(abs(repair_prefix_mass(kh)-k))),
             'prefix_mass_before_repair':float(sum(kh))})
    # Independent continuous-density forward quadrature, then exact edge bins.
    # The input law has positive density at zero and fails SC.
    gamma=1.3;hfine=.002;s=np.arange(2001)*hfine
    density=np.exp(-2*s)+30*np.exp(-4*s)*(1-np.exp(-s))**2
    f=density_forward(density,s,t,gamma)
    cdf=np.r_[0.,cumulative_trapezoid(f,s)]
    for h in [.08,.04,.02]:
        step=round(h/hfine);n=round(4/h)+1;q=np.exp(-gamma*h);cap=2*h
        truek=true_cell_masses(h,n)
        observed=np.r_[np.exp(-t),np.diff(cdf[::step])]
        flattice=uniformized_forward(truek,q,t)
        model_bias=float(sum(abs(observed-flattice)))
        probs=np.r_[observed,max(0,1-sum(observed))];probs/=sum(probs)
        for samples in [10000,100000]:
            vals=[]
            for rep in range(12):
                y=rng.multinomial(samples,probs)[:-1]/samples
                y[0]=np.exp(-t) # alpha is known; intact count not used to refit it.
                kh,p,w=clipped_inverse(y,q,t,cap)
                defect,_,_=numerical_defect(kh,y,q,t,cap)
                repaired=repair_prefix_mass(kh)
                vals.append([sum(abs(repaired-truek)),defect,sum(kh)])
            vals=np.asarray(vals)
            out['noisy_continuous_bins'].append({'h':h,'samples':samples,'replicates':12,
                'continuous_lattice_bin_bias':model_bias,'mean_l1':float(vals[:,0].mean()),
                'sd_l1':float(vals[:,0].std()),'max_numerical_defect':float(vals[:,1].max()),
                'mass_repair_count':int(sum(vals[:,2]>1))})
    print(json.dumps(out,indent=2))
    json.dump(out,open('no_sc_noise_results.json','w'),indent=2)


if __name__=='__main__':main()
