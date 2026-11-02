#!/usr/bin/env python3
"""Exact structural occupancy and phenotype-degeneracy calculations for
10 spatially separated PDI dimers on source-demonstrated 6HB geometry.
Not a measurement of spectra, chemical functionality, or allele-coded expression.
The 2024 source deliberately places ten dimers sufficiently separated to
spectroscopically average; identical, decoupled units imply <=11 distinct
spectra for 2^10 binary arrangements under the stated identical-unit model.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.special import roots_jacobi, comb

def pdi_distribution(p=0.85,kappa=None,n=10):
    if kappa is None:
        # each dimer succeeds only if both modified staple positions are present
        q=p*p
        return np.array([comb(n,k)*q**k*(1-q)**(n-k) for k in range(n+1)])
    a=p*kappa;b=(1-p)*kappa
    x,w=roots_jacobi(16,b-1,a-1) # weighted integral of all polynomials <=31
    u=(x+1)/2
    q=u*u
    distr=np.array([np.sum(w*comb(n,k)*q**k*(1-q)**(n-k))/sum(w) for k in range(n+1)])
    return distr

def report(p=.85,kappa=12):
    d0=pdi_distribution(p,None)
    d1=pdi_distribution(p,kappa)
    E=(lambda d:float(np.dot(np.arange(len(d)),d)))
    V=(lambda d:float(np.dot(np.arange(len(d))**2,d)-E(d)**2))
    return dict(assumed_per_staple_occupancy=p, correlated_beta_concentration=kappa,
      n_PDI_dimers=10, PDI_staple_positions=20,
      all_20_canonical_sites_occupied_independent=p**20,
      expected_completed_dimers_independent=E(d0),
      expected_completed_dimers_beta_correlated=E(d1),
      variance_dimers_independent=V(d0),
      variance_dimers_beta_correlated=V(d1),
      P_at_least_6_complete_dimers_independent=float(sum(d0[6:])),
      P_at_least_6_complete_dimers_correlated=float(sum(d1[6:])),
      P_at_least_8_complete_dimers_independent=float(sum(d0[8:])),
      P_at_least_8_complete_dimers_correlated=float(sum(d1[8:])),
      n_genotypes=2**10,
      n_spectral_classes_upper_bound_given_identical_decoupled_dimer_spectra=11,
      structural_threshold_is_not_optical_function=True,
      status='exact conditional toy structural occupancy, unmeasured p/kappa; spectrum class conditional on decoupling')

if __name__=='__main__':
    r=report()
    out='/mnt/data/pdi_pair_fidelity_and_information_results.json'
    Path(out).write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
