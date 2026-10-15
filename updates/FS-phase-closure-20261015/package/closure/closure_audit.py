#!/usr/bin/env python3
"""Reproducible synthetic audit of decision-level thermal-emulation certificates.

This is an analytical toy model, NOT experimental validation or a validated
reactor simulator. No input data are downloaded. The heterogeneous counterexample
uses deliberately chosen positive Arrhenius kinetics, not a fit to Rh data.

Run: python closure_audit.py --output-dir results
Dependencies: numpy, scipy. Python >=3.10.
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

RGAS = 8.314462618  # J mol^-1 K^-1

def gain(temperature: np.ndarray | float, barrier: float = 80000.0,
         reference: float = 573.0) -> np.ndarray:
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError('Absolute temperatures must be positive.')
    return np.exp(barrier / RGAS * (1.0 / reference - 1.0 / t))

def lp_distance(library: np.ndarray, fractions: np.ndarray,
                target: np.ndarray) -> tuple[float, np.ndarray]:
    """L-infinity distance to a weighted Minkowski sum of local finite hulls.

    library has dimensions (populations, modes, output_channels). Nonnegative
    lambda weights for each population sum to its fixed catalyst fraction.
    Fractions may equally describe pre-calibrated disjoint reactor modules.
    """
    n, k, d = library.shape
    if fractions.shape != (n,) or target.shape != (d,):
        raise ValueError('Incompatible shapes.')
    if not np.isclose(fractions.sum(), 1.0) or np.any(fractions < 0):
        raise ValueError('Fractions must be nonnegative and sum to one.')
    matrix = library.reshape(n*k, d).T
    objective = np.r_[np.zeros(n*k), 1.0]
    equalities = np.zeros((n, n*k+1))
    for i in range(n):
        equalities[i, i*k:(i+1)*k] = 1.0
    inequalities = np.vstack([np.c_[matrix, -np.ones(d)],
                              np.c_[-matrix, -np.ones(d)]])
    result = linprog(objective, A_ub=inequalities,
                     b_ub=np.r_[target, -target],
                     A_eq=equalities, b_eq=fractions,
                     bounds=[(0, None)]*(n*k+1), method='highs')
    if not result.success:
        raise RuntimeError(f'LP failed: {result.message}')
    return float(result.fun), result.x[:-1].reshape(n, k)

def main(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20261015)
    temperatures = np.linspace(523., 623., 101)
    f = (.60-.02)/(.98-.02)
    fractions = np.array([f, 1-f])
    selectors = np.array([[.98, .02], [.02, .98]])
    library = gain(temperatures)[None, :, None] * selectors[:, None, :]
    uniform = np.einsum('i,ikd->kd', fractions, library)
    s_dark = uniform[:,0]/uniform.sum(axis=1)
    assert np.max(np.abs(s_dark-.60)) < 1e-12

    # The same two populations, but differential (entirely thermal) heating.
    target = fractions[0]*library[0,-1] + fractions[1]*library[1,0]
    s_target = float(target[0]/target.sum())
    naive_q = (s_target-.60)/.40
    naive_distance, _ = lp_distance(uniform[None, :, :], np.ones(1), target)
    repaired_distance, _ = lp_distance(library, fractions, target)
    assert naive_distance > .1 and repaired_distance < 1e-9

    # A common homogeneous calibration is sound for homogeneous mixtures.
    mixtures = rng.dirichlet(np.ones(len(temperatures)), size=10000)
    bulk_mixed = mixtures @ uniform
    bulk_s = bulk_mixed[:,0]/bulk_mixed.sum(axis=1)
    assert np.max(np.abs(bulk_s-.60)) < 1e-12

    # Exercise local-hull feasibility with arbitrary distributions, including sparse ones.
    max_distance = 0.
    for _ in range(100):
        weights = rng.dirichlet(np.full(len(temperatures), .08), size=2)
        sample = np.einsum('i,ik,ikd->d', fractions, weights, library)
        distance, _ = lp_distance(library, fractions, sample)
        max_distance = max(max_distance, distance)
    assert max_distance < 1e-8

    # Check the support-function bound (an exact elementary theorem, numerically exercised).
    support_max_violation = -float('inf')
    for _ in range(1000):
        w = rng.normal(size=2)
        weights = rng.dirichlet(np.ones(len(temperatures)), size=2)
        sample = np.einsum('i,ik,ikd->d', fractions, weights, library)
        support = np.sum(fractions*np.max(library @ w, axis=1))
        support_max_violation = max(support_max_violation, float(w @ sample-support))
    assert support_max_violation < 1e-8

    # A constant linear cross-sensitive detector preserves the forward convex model.
    detector = np.array([[1.0,.12], [.08,.90], [.70,.20]])
    detector_library = library @ detector.T
    detector_target = detector @ target
    detector_distance, _ = lp_distance(detector_library, fractions, detector_target)
    assert detector_distance < 1e-8

    # Artificial signal injection tests discrimination, not a physical light mechanism.
    injected = target + np.array([.5, 0.])
    injection_distance, _ = lp_distance(library, fractions, injected)
    assert injection_distance > .05
    methane_excess = float(injected[0]-np.max(uniform[:,0]))
    assert methane_excess > 0

    # A tiny finite-array resource allocation check. The LP is an OUTER relaxation:
    # its time-sharing solution is not asserted to be physically replayable.
    tsmall = np.linspace(523.,623.,5)
    mode_cost = (tsmall-523.)/100.  # dimensionless synthetic cost, NOT measured watts
    libsmall = gain(tsmall)[None,:,None]*selectors[:,None,:]
    budget = .75
    score = np.array([1., -.2])
    mode_score = libsmall @ score
    objective = -(fractions[:,None]*mode_score).reshape(-1)
    Aeq = np.zeros((2,10)); Aeq[0,:5]=1.; Aeq[1,5:]=1.
    allocation = linprog(objective,
        A_ub=np.tile(mode_cost,2)[None,:], b_ub=[budget],
        A_eq=Aeq,b_eq=np.ones(2), bounds=[(0,None)]*10,method='highs')
    assert allocation.success
    lp_score = -float(allocation.fun)
    deterministic = []
    for i,j in itertools.product(range(5),repeat=2):
        cost = mode_cost[i]+mode_cost[j]
        if cost <= budget+1e-12:
            y = fractions[0]*libsmall[0,i]+fractions[1]*libsmall[1,j]
            deterministic.append(float(score@y))
    best_discrete = max(deterministic)
    assert lp_score+1e-10 >= best_discrete
    beta = -float(allocation.ineqlin.marginals[0])
    alpha = np.max(fractions[:,None]*mode_score-beta*mode_cost[None,:], axis=1)
    dual_value = float(beta*budget+alpha.sum())
    assert abs(dual_value-lp_score) < 1e-9
    nonzero_modes = int(np.count_nonzero(allocation.x > 1e-9))
    assert nonzero_modes <= 3  # 2 normalizations + 1 active resource budget

    # Calculations from two published scalar enhancement numbers. Not raw-data reanalysis.
    # Zhang et al., Nature Communications 8,14542 (2017), doi:10.1038/ncomms14542.
    equivalent_temperatures = []
    for temperature, enhancement in [(623.,7.41),(523.,24.4)]:
        equivalent = 1/(1/temperature-RGAS/78600.*np.log(enhancement))
        equivalent_temperatures.append({
            'reported_temperature_K':temperature,
            'reported_methane_enhancement':enhancement,
            'assumed_fixed_activation_energy_J_mol':78600.,
            'calculated_uniform_thermal_equivalent_K':float(equivalent),
            'calculated_shift_K':float(equivalent-temperature),
            'scope':'Arrhenius extrapolation only; not evidence this temperature occurred.'})

    results = {
        'status':'synthetic audit only; no empirical validation or novelty certification',
        'seed':20261015,
        'counterexample':{
            'activation_energy_J_mol':80000., 'reference_temperature_K':573.,
            'methane_selectivity_A':.98, 'methane_selectivity_B':.02,
            'fraction_A':float(f), 'fraction_B':float(1-f),
            'uniform_dark_methane_selectivity':.6,
            'differential_temperature_A_K':623., 'differential_temperature_B_K':523.,
            'rates_methane_CO_reference_units':target.tolist(),
            'differential_heating_methane_selectivity':s_target,
            'invalid_bulk_outside_fraction_lower_bound':float(naive_q),
            'distance_to_invalid_bulk_hull':naive_distance,
            'distance_to_local_hull':repaired_distance},
        'checks':{
            'homogeneous_mixtures_checked':10000,
            'homogeneous_selectivity_max_absolute_error':float(np.max(np.abs(bulk_s-.60))),
            'local_hull_LPs_checked':100,
            'local_hull_max_Linf_distance':max_distance,
            'support_inequalities_checked':1000,
            'largest_support_bound_violation':support_max_violation,
            'linear_detector_Linf_distance':detector_distance},
        'artificial_positive_control':{
            'injected_methane_reference_units':.5,
            'distance_to_local_hull':injection_distance,
            'methane_excess_above_all_modes':methane_excess,
            'scope':'algebraic sensor-input injection, not an obtainable photocatalytic process'},
        'finite_array_resource_relaxation':{
            'modes_per_population':5, 'budget_arbitrary_units':budget,
            'best_deterministic_score':best_discrete,
            'relaxed_upper_bound':lp_score,
            'nonzero_LP_modes':nonzero_modes,
            'dual_resource_multiplier':beta,
            'dual_value':dual_value,
            'duality_gap':abs(dual_value-lp_score),
            'mode_weights':allocation.x.reshape(2,5).tolist(),
            'scope':'Resource costs are synthetic. Convex mixing not assumed experimentally free.'},
        'published_scalar_calculations':equivalent_temperatures,
        'all_assertions_passed':True}
    (output_dir/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    with (output_dir/'synthetic_dark_library.csv').open('w',newline='') as fh:
        writer=csv.writer(fh)
        writer.writerow(['population','temperature_K','fraction','methane_rate_reference_units','CO_rate_reference_units'])
        for pop in range(2):
            for k,t in enumerate(temperatures):
                writer.writerow([pop,float(t),float(fractions[pop]),*map(float,library[pop,k])])
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path('results'))
    main(parser.parse_args().output_dir)
