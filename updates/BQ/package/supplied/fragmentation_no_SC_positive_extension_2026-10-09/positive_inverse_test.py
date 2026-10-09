"""Targeted comparisons of the cancellation-free redesign, fixed seeds."""
import json,time
import numpy as np
from scipy.linalg import expm
from scipy.stats import beta
from positive_causal_inverse import positive_inverse
from causal_clipped_inverse import clipped_inverse,numerical_defect,repair_prefix_mass
from fragment_inverse import uniformized_forward
from no_sc_noise_test import true_cell_masses


def independent_profile_endpoint(k,rates,a):
    n=len(k);A=-np.diag(rates)
    for j in range(1,n):A[np.arange(j,n),np.arange(n-j)]=k[j]*rates[:n-j]
    return expm(a*A)[:,0]


def main():
    rng=np.random.default_rng(708442)
    out={'seed':708442,'matched_precision':[],'constant_rate':[],
         'arbitrary_rate_profile':[],'scaling':[]}
    h=.04;n=101;a=2.;cap=2*h;k=true_cell_masses(h,n)
    for gamma in [1.3,.1,.02,.001]:
        logq=-gamma*h;q=np.exp(logq)
        f=uniformized_forward(k,q,a)
        y=rng.poisson(f*100000)/100000;y[0]=f[0]
        st=time.perf_counter();kh,diag=positive_inverse(y,a,cap,logq=logq);elapsed=time.perf_counter()-st
        defect,_,_=numerical_defect(kh,y,q,a,cap)
        record={'gamma':gamma,'seconds':elapsed,'order':diag['order'],
            'tail_bound':diag['tail_l1_bound'],'defect':defect,
            'kernel_l1':float(sum(abs(repair_prefix_mass(kh)-k))),
            'table_max':diag['table_max'],'minimum_table':diag['minimum_table_entry']}
        # Independent renewal computation at sufficient precision, on modest
        # cases only; the very small-gamma case is checked by forward defect.
        if gamma>=.02:
            st=time.perf_counter();km,_,wmax=clipped_inverse(y,q,a,cap,dps=100);mt=time.perf_counter()-st
            record.update({'mp_seconds':mt,'mp_difference':float(sum(abs(kh-km))),'renewal_Wmax':wmax})
        out['matched_precision'].append(record)
    # gamma=0 is a regular case for this representation.
    for n in [12,45]:
        k=np.r_[0.,rng.dirichlet(np.ones(n-1)*2)];a=1.7;cap=max(k)*1.1
        rates=np.ones(n);f=independent_profile_endpoint(k,rates,a)
        kh,d=positive_inverse(f,a,cap,logq=0,tolerance=1e-13)
        out['constant_rate'].append({'n':n,'maxerr':float(max(abs(kh-k))),
            'tail_bound':d['tail_l1_bound'],'order':d['order']})
    # The positive algorithm only needs a known rate at every state, bounded
    # above by its initial rate. No exponential profile is used here.
    for n in [16,35]:
        k=np.r_[0.,rng.dirichlet(np.ones(n-1)*2)];a=2.1;cap=max(k)*1.1
        rates=np.r_[1.,rng.uniform(.15,.95,n-1)]
        f=independent_profile_endpoint(k,rates,a)
        kh,d=positive_inverse(f,a,cap,rates=rates,tolerance=1e-13)
        out['arbitrary_rate_profile'].append({'n':n,'maxerr':float(max(abs(kh-k))),
            'tail_bound':d['tail_l1_bound'],'order':d['order']})
    for n in [101,501,1001]:
        h=4/(n-1);gamma=.02;q=np.exp(-gamma*h);a=2.;cap=2*h;k=true_cell_masses(h,n)
        f=uniformized_forward(k,q,a);y=rng.poisson(f*100000)/100000;y[0]=f[0]
        st=time.perf_counter();kh,d=positive_inverse(y,a,cap,logq=-gamma*h);elapsed=time.perf_counter()-st
        defect,_,_=numerical_defect(kh,y,q,a,cap)
        out['scaling'].append({'n':n,'seconds':elapsed,'order':d['order'],'defect':defect,
            'table_max':d['table_max'],'tail_bound':d['tail_l1_bound'],
            'kernel_l1':float(sum(abs(repair_prefix_mass(kh)-k)))})
    print(json.dumps(out,indent=2))
    json.dump(out,open('positive_inverse_results.json','w'),indent=2)


if __name__=='__main__':main()
