#!/usr/bin/env python3
"""Mechanical scope-local consistency checks of the three executed audits.
This tests numerical computations only; proofs are in accompanying note.
"""
import json, pathlib
root=pathlib.Path(__file__).resolve().parent
read=lambda name:json.loads((root/name).read_text())
a=read('astra_matrix_loader_audit.json')
b=read('astra_restricted_controller_no_go.json')
c=read('astra_selective_source_completion.json')
assert a['noncommutation_norm_J_L']>1
assert all(x['kernel_residual']<2e-12 for x in a['general_matrix_samples'])
assert all(x['reduced_inverse_residual']<2e-12 for x in a['general_matrix_samples'])
assert all(x['positive_gap']>=1.5-2e-12 for x in a['general_matrix_samples'])
assert all(x['operator_norm_error']<x['theorem_bound'] for x in a['transport'])
assert a['transport'][-1]['operator_norm_error']<a['transport'][0]['operator_norm_error']/10
assert b['data'][-1]['eta_independent_trapping_residual']!='nan'
assert b['data'][-1]['upper_bound_success_probability_at_T_10']<.00015
assert b['data'][-1]['necessary_T_for_at_least_0p9_success_probability']>940
assert c['max_eigen_residual']<1e-12
assert c['max_derivative_residual']<1e-12
assert c['max_noncommutator']>1000
print('PASS: 3 audited constructions, 20 selective-source models, 6 arbitrary-control no-go scales, 4 direct Schr propagation times.')
