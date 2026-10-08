#!/usr/bin/env python3
"""Bounded diagnostics for PROOF.md; finite SVD is not a proof certificate."""
from itertools import product
from fractions import Fraction
from pathlib import Path
import json
import numpy as np

states=list(product((-1,1), repeat=5))

def channel(eta, mode='full', shared_point=False):
    weights=[eta,eta,1-2*eta]
    rows=[]; alphabet={}
    for x,y,u,v,r in states:
        symbols=[('A',x,u),('B',y,u if shared_point else v)]
        symbols.append(('F',x,y,u,v,r) if mode=='full' else ('F',x*y*u*v*r))
        rows.append(symbols)
        for symbol in symbols:
            if symbol not in alphabet: alphabet[symbol]=len(alphabet)
    matrix=np.zeros((len(states),len(alphabet)))
    for i,symbols in enumerate(rows):
        for weight,symbol in zip(weights,symbols):matrix[i,alphabet[symbol]]=float(weight)
    return matrix,rows,alphabet,weights

def diagnostic(rho,eta,mode='independent',shared_point=False):
    pi=np.array([float((1+rho*x*y)/32) for x,y,u,v,r in states])
    a,rowsa,alpa,weights=channel(eta,shared_point=shared_point)
    b,rowsb,alpb,_=channel(eta,'parity' if mode=='asymmetric' else 'full',shared_point)
    if mode=='correlated_selectors':
        joint=np.zeros((len(alpa),len(alpb)))
        for i in range(len(states)):
            for weight,sa,sb in zip(weights,rowsa[i],rowsb[i]):
                joint[alpa[sa],alpb[sb]]+=pi[i]*float(weight)
    else:
        joint=a.T @ (pi[:,None]*b)
    m0=joint.sum(axis=1);m1=joint.sum(axis=0)
    norm=joint/np.sqrt(m0[:,None]*m1[None,:])
    singular=np.linalg.svd(norm,compute_uv=False)
    rho_out=float(singular[1])
    sigma_out=(1-rho_out)/2
    bound=eta*(1-rho)/2
    return {'rho_input':str(rho),'eta':str(eta),'mode':mode,
            'shared_point_register':shared_point,
            'latent_states':len(states),'joint_shape':list(joint.shape),
            'rho_output_svd':rho_out,'global_sigma_output_svd':sigma_out,
            'claimed_bound_if_hypotheses_hold':str(bound),
            'bound_holds_to_1e_12':sigma_out+1e-12>=float(bound),
            'analytic_sharp_sigma':str(bound) if mode=='independent' and not shared_point else None,
            'exact_input_probabilities':'mu(x,y)=(1+rho*x*y)/4; U,V,R independent uniform signs',
            'evidence_type':'finite floating-point SVD diagnostic'}

rows=[]
for rho in (Fraction(0),Fraction(1,2),Fraction(7,8)):
    for eta in (Fraction(1,9),Fraction(1,3)):
        row=diagnostic(rho,eta)
        assert row['bound_holds_to_1e_12']
        assert abs(row['global_sigma_output_svd']-float(eta*(1-rho)/2))<1e-12
        rows.append(row)
rows.append(diagnostic(Fraction(1,2),Fraction(1,9),'asymmetric'))
assert rows[-1]['bound_holds_to_1e_12']
rows.append(diagnostic(Fraction(1,2),Fraction(1,9),'correlated_selectors'))
assert abs(rows[-1]['global_sigma_output_svd'])<1e-12
rows.append(diagnostic(Fraction(1,2),Fraction(1,9),shared_point=True))
assert abs(rows[-1]['global_sigma_output_svd'])<1e-12
out={'scope':'6 sharp full-seed cases, 1 asymmetric case, 2 deliberate assumption violations',
     'costs':{'max_latent_states':32,'max_joint_entries':1600,'precision':'numpy float64','no_support_enumeration_of_actual_verifier':True},
     'fixtures':rows,'all_expected_checks_pass':True}
Path(__file__).with_name('view_gap_diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_expected_checks_pass':True,'fixtures':len(rows),'sharp_full_seed_cases':6,
                  'deliberate_assumption_violations':2,'output':'view_gap_diagnostics.json'}))
