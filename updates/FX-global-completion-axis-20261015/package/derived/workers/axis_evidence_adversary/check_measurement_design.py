#!/usr/bin/env python3
"""Exact countermodels and synthetic design checks. NO physical measurements."""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent

def rat(x): return str(x)

def main():
    # Superlattice weight a_j=f_j*S_j^2; incoherent integrated kinematic regime.
    # Identical poles and phase volume, different desired volume-axis tensors.
    worlds = {
        'A': {'f': [F(1,2),F(1,2)], 's2': [F(9,25),F(9,25)]},
        'B': {'f': [F(3,4),F(1,4)], 's2': [F(6,25),F(18,25)]}}
    for world in worlds.values():
        world['a'] = [f*s for f,s in zip(world['f'],world['s2'])]
    assert worlds['A']['a'] == worlds['B']['a'] == [F(9,50),F(9,50)]
    assert sum(worlds['A']['f']) == sum(worlds['B']['f']) == 1
    assert worlds['A']['f'] != worlds['B']['f']

    # False positive under orthogonal intervention: axes and volumes unchanged.
    fixed_f = [F(1,2),F(1,2)]
    s2_x = [F(16,25),F(4,25)]
    s2_y = list(reversed(s2_x))
    ax = [f*s for f,s in zip(fixed_f,s2_x)]
    ay = [f*s for f,s in zip(fixed_f,s2_y)]
    assert sum(ax) == sum(ay) == F(2,5)
    dx = (ax[0]-ax[1])/sum(ax)
    dy = (ay[0]-ay[1])/sum(ay)
    assert dx-dy == F(6,5)

    # Acquired energy/reciprocal-space nuisance basis would replace these data.
    # Purely synthetic full-rank and failure examples test the algebra only.
    U = np.array([[1.,0.],[1.,1.],[1.,-1.]])
    g = np.array([1.,3.,3.])
    P = np.eye(3)-U@np.linalg.pinv(U)
    w = P@g/(g@P@g)
    assert np.allclose(w@g,1)
    assert np.allclose(w@U,0)
    a_true = 0.18
    nuisance = np.array([2.,0.4])
    y = a_true*g+U@nuisance
    assert abs(float(w@y)-a_true)<1e-12
    g_bad = U@np.array([1.,2.])
    assert np.linalg.norm(P@g_bad)<1e-12

    # Independent audit of the matrix-sandwich lemma supplied by root.
    # Noncommuting positive matrices are intentionally used.
    P_atom = np.array([[.3,.1,0.],[.1,.2,.02],[0.,.02,.1]])
    Q_atom = np.array([[.1,0.,.03],[0.,.15,.01],[.03,.01,.15]])
    s = .4
    M = P_atom+Q_atom
    W = P_atom+s*s*Q_atom
    P_recovered = (W-s*s*M)/(1-s*s)
    Q_recovered = (M-W)/(1-s*s)
    assert min(np.linalg.eigvalsh(P_atom))>0
    assert min(np.linalg.eigvalsh(Q_atom))>0
    assert np.allclose(P_recovered,P_atom)
    assert np.allclose(Q_recovered,Q_atom)
    commutator = float(np.linalg.norm(M@W-W@M))
    assert commutator>1e-5

    # Finite angular cells: exact theorem in report; random checks are diagnostics.
    rng = np.random.default_rng(20261015)
    max_error = 0.
    for _ in range(1000):
        n = rng.normal(size=3); n /= np.linalg.norm(n)
        m = rng.normal(size=3); m /= np.linalg.norm(m)
        theta = math.acos(min(1.,abs(float(n@m))))
        error = np.linalg.norm(np.outer(n,n)-np.outer(m,m),ord=2)
        max_error = max(max_error,abs(error-math.sin(theta)))
    assert max_error<1e-12
    # Source A21: 14.37keV, L=10.3nm, profile around 2theta=28deg.
    # Scherrer K=.9 is an explicit illustrative choice, not a measured width.
    hc_kev_nm = 1.239841984
    wavelength = hc_kev_nm/14.37
    beta_rad = .9*wavelength/(10.3*math.cos(math.radians(14)))
    beta_deg = math.degrees(beta_rad)

    out = {
      'status':'CONDITIONAL_MATHEMATICAL_MEASUREMENT_DESIGN_AND_EXACT_FALSIFIERS',
      'physical_experiment_performed':False,
      'raw_stress_axis_response_acquired':False,
      'identical_superlattice_poles_different_volume_tensor': {
        name:{key:[rat(v) for v in value] for key,value in world.items()}
        for name,world in worlds.items()},
      'fixed_axes_false_positive': {
        'f_x_f_y':[rat(v) for v in fixed_f],
        'S_squared_x_intervention':[rat(v) for v in s2_x],
        'S_squared_y_intervention':[rat(v) for v in s2_y],
        'superlattice_a_x_intervention':[rat(v) for v in ax],
        'superlattice_a_y_intervention':[rat(v) for v in ay],
        'constant_total_superlattice_weight':rat(sum(ax)),
        'D_order_weighted_x':rat(dx),'D_order_weighted_y':rat(dy),
        'apparent_write_contrast':rat(dx-dy),
        'true_volume_write_contrast':'0'},
      'synthetic_nuisance_projection_check':{
        'g':g.tolist(),'U':U.tolist(),'contrast_weights':w.tolist(),
        'a_true':a_true,'a_recovered':float(w@y),
        'bad_design_residual_norm':float(np.linalg.norm(P@g_bad)),
        'warning':'Purely synthetic arrays; no acquired energy response or material background.'},
      'root_matrix_sandwich_independent_audit':{
        's':s,'M':M.tolist(),'W':W.tolist(),
        'P_reconstruction_max_error':float(np.max(np.abs(P_atom-P_recovered))),
        'Q_reconstruction_max_error':float(np.max(np.abs(Q_atom-Q_recovered))),
        'commutator_frobenius_norm':commutator,
        's0_only_closure_example':{'M_diagonal':['1/2','1/2','0'],
          'W_diagonal':['1/10','0','0'],
          'impossible_with_positive_S':'W_yy=0 and M_yy>0 contradict S>0 almost everywhere on ordered volume'},
        'warning':'Algebra check only; theorem requires independently acquired/calibrated f, s, W.'},
      'finite_cell_operator_bound_diagnostic':{
        'trials':1000,'max_identity_residual':max_error,
        'bound_Q_operator_at_2deg':math.sin(math.radians(2)),
        'bound_D_absolute_at_2deg':2*math.sin(math.radians(2)),
        'warning':'Geometric design bounds, not angular coverage or precision achieved.'},
      'A21_peak_width_reference':{
        'photon_energy_keV':14.37,'wavelength_nm':wavelength,
        'source_Scherrer_diameter_nm':10.3,'assumed_K':.9,
        'reference_2theta_deg':28.,'illustrative_Scherrer_fwhm_deg':beta_deg,
        'source_reference_200_002_split_deg':.19,
        'width_over_reference_split':beta_deg/.19,
        'warning':'Illustrative inverse-Scherrer width, not independent measured broadening or proof that full-pattern inference is impossible.'}
    }
    (BASE/'measurement_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__': main()
