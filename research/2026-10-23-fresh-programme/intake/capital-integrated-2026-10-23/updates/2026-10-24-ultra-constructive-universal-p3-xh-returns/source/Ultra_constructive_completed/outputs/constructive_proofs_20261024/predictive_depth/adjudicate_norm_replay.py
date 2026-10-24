#!/usr/bin/env python3
"""Source-free verification of the two exact perturbation identities."""
import builtins
import itertools
import json
from pathlib import Path
import numpy as np

original_import = builtins.__import__
def no_plant_import(name,*args,**kwargs):
    if 'quantum_shot_plant' in name:
        raise AssertionError('No private plant in norm adjudication')
    return original_import(name,*args,**kwargs)
builtins.__import__ = no_plant_import
from finite_predictive_learner import CountOracle,learn
from direct_macro_learner import learn_macro

ROOT = Path(__file__).resolve().parent


def main():
    pilot = json.loads((ROOT/'calibration_counts.json').read_text())
    macro_data = json.loads((ROOT/'direct_macro_counts.json').read_text())
    m = learn(pilot)
    mm = learn_macro(macro_data)
    a,ainv = mm['H'],mm['H_inverse']
    cert = mm['certificate']
    dh = cert['H_error_infinity_bound']
    jhat,jbar = cert['inverse_H_infinity_norm'],cert['true_inverse_H_upper_bound']
    r = len(a)
    khat = max(np.linalg.norm(ainv@np.array(s),1) for s in itertools.product([-1,1],repeat=r))
    kbar = khat+r*jbar*dh*jhat
    assert kbar == cert['physical_quotient_kappa_upper_bound']
    cells = {(tuple(s['preparation']),s['future_action']):s for s in macro_data['macro']}
    raw,repairs,independent = {},{},{}
    width = cert['maximum_entry_statistical_width']+cert['cap_systematic_entry_error_upper_bound']
    dz = r*width
    for branch in ['success','abort']:
        f = np.zeros((r,r))
        for j,p in enumerate(macro_data['preparations']):
            for i,test in enumerate(macro_data['tests']):
                action = test[0][0] if test else macro_data['tests'][1][0][0]
                cell = cells[tuple(p),action]
                if test:
                    f[i,j] = cell['counts'][f'{branch},{test[0][1]}']/cell['shots']
                else:
                    f[i,j] = sum(cell['counts'][f'{branch},{o}'] for o in range(2))/cell['shots']
        raw[branch] = f@ainv
        repairs[branch] = float(np.linalg.norm(mm['ops'][branch]-raw[branch],np.inf))
        independent[branch] = float((dz+np.linalg.norm(raw[branch],np.inf)*dh)*jbar+repairs[branch])
        assert abs(independent[branch]-cert['branch_coordinate_error_bounds'][branch]) < 1e-14
    rng = np.random.default_rng(60710024)
    residuals,inverse_residuals,ratios = [],[],[]
    for _ in range(256):
        perturb = rng.normal(size=(r,r))
        perturb *= (dh*rng.uniform(.1,.9))/np.linalg.norm(perturb,np.inf)
        h = a-perturb
        hi = np.linalg.inv(h)
        f = rng.normal(size=(r,r))
        dg = rng.normal(size=(r,r))
        dg *= (.02*rng.uniform(.1,.9))/np.linalg.norm(dg,np.inf)
        g = f-dg
        bhat,b = f@ainv,g@hi
        identity = (bhat-b)@h-(dg-bhat@perturb)
        residuals.append(float(np.max(abs(identity))))
        inverse_residuals.append(float(np.max(abs(hi-ainv-hi@perturb@ainv))))
        bound = (np.linalg.norm(dg,np.inf)+np.linalg.norm(bhat,np.inf)*dh)*jbar
        error = np.linalg.norm(bhat-b,np.inf)
        assert error <= bound+1e-12
        actual_kappa = max(np.linalg.norm(hi@np.array(s),1) for s in itertools.product([-1,1],repeat=r))
        assert actual_kappa <= kbar+1e-12
        ratios.append(float(error/bound))
    result = {'status':'PASS','private_plant_import_forbidden':True,
              'claimed_norm_defect':'REJECTED_EXACT_RESIDUAL_IDENTITY_IS_VALID',
              'saved_primitive_instrument_bound':m['certificate']['primitive_instrument_quotient_error_upper_bound'],
              'raw_macro_infinity_norms':{b:float(np.linalg.norm(x,np.inf)) for b,x in raw.items()},
              'charged_repair_norms':repairs,
              'independently_recomputed_macro_branch_bounds':independent,
              'independently_recomputed_macro_joint_bound':float(kbar*sum(independent.values())),
              'kappa_vertex_norm':float(khat),
              'kappa_inverse_perturbation_margin':float(r*jbar*dh*jhat),
              'kappa_upper_bound':float(kbar),
              'noncommuting_nearby_core_cases':256,
              'max_exact_residual_identity_error':max(residuals),
              'max_exact_inverse_identity_error':max(inverse_residuals),
              'max_actual_to_certified_error_ratio':max(ratios),
              'scope':'Algebra/count-code adjudication; global certificate still vacuous.'}
    (ROOT/'NORM_ADJUDICATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
