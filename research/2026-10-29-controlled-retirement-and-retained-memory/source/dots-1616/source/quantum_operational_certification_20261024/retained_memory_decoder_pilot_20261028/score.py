"""POST-HOC privileged scoring, never called by learner updates.
Each fixed baseline/oracle is evaluated on the recorded actual prior memory states
of that run. No counterfactual state evolution or future performance is inferred.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from learner import Learner
from ordinary_comparator import OrdinaryComparator
from quantum_math import I,PAULIS,C0,choi,unitary_choi

def risk(c,masses,targets):
    return float(1-sum(p*np.trace(c@t).real for p,t in zip(masses,targets)))

def summarize(directory):
    meta=json.loads((directory/'metadata.json').read_text())
    public=[json.loads(x) for x in (directory/'public_records.jsonl').read_text().splitlines()]
    private=[json.loads(x) for x in (directory/'private_source_audit.jsonl').read_text().splitlines()]
    assert len(public)==len(private)==meta['plant']['source_calls']
    u=np.array(meta['plant']['unitary']['real'])+1j*np.array(meta['plant']['unitary']['imag'])
    targets=[unitary_choi((u@p).conj().T) for p in PAULIS]
    ideal=unitary_choi(u.conj().T);identity=unitary_choi(I)
    bandit=meta['algorithm']=='bandit'
    learner=Learner() if bandit else OrdinaryComparator()
    scored=[]
    for r,audit in zip(public,private):
        masses=audit['branch_masses']
        if bandit:
            center=choi(learner.theta);played,_=learner.act(r['i'],r['z'])
        else:
            center,_=learner.decoder();played=center
        row={'t':r['t'],'played_policy_bell_loss':risk(played,masses,targets),
             'center_policy_bell_loss':risk(center,masses,targets),
             'identity_no_learning_bell_loss':risk(identity,masses,targets),
             'depolarizing_no_learning_bell_loss':risk(C0,masses,targets),
             'known_U_oracle_bell_loss':risk(ideal,masses,targets)}
        row['oracle_formula_error']=abs(row['known_U_oracle_bell_loss']-(1-masses[0]))
        scored.append(row)
        if bandit: learner.observe(r['y'])
        else:learner.observe(r['j'],r['s'],r['m'],r['b'])
    final=choi(learner.theta) if bandit else learner.decoder()[0]
    with (directory/'posthoc_scores.jsonl').open('w') as f:
        for row in scored:f.write(json.dumps(row)+'\n')
    mean=lambda key:float(np.mean([r[key] for r in scored]))
    result={'run':directory.name,'actual_source_calls':len(public),
        'played_policy_mean_bell_loss':mean('played_policy_bell_loss'),
        'center_policy_mean_bell_loss':mean('center_policy_bell_loss'),
        'identity_no_learning_mean_bell_loss':mean('identity_no_learning_bell_loss'),
        'depolarizing_no_learning_mean_bell_loss':mean('depolarizing_no_learning_bell_loss'),
        'known_U_oracle_mean_bell_loss':mean('known_U_oracle_bell_loss'),
        'final_decoder_retrospective_past_occupation_loss':float(np.mean([risk(final,a['branch_masses'],targets) for a in private])),
        'max_oracle_formula_error':max(r['oracle_formula_error'] for r in scored),
        'acquisition_wall_seconds':meta['total_acquisition_wall_seconds'],
        'source_simulation_seconds':sum(r['diagnostics']['source_simulation_seconds'] for r in public),
        'source_probability_X_min':min(a['branch_masses'][1] for a in private),
        'source_probability_X_max':max(a['branch_masses'][1] for a in private),
        'source_probability_Z_min':min(a['branch_masses'][3] for a in private),
        'source_probability_Z_max':max(a['branch_masses'][3] for a in private),
        'max_conditioning_trace_distance':max(a['conditional_vs_unobserved_trace_distance'] for a in private),
        'mean_conditioning_trace_distance':float(np.mean([a['conditional_vs_unobserved_trace_distance'] for a in private])),
        'memory_min_eigen':min(a['memory_post_min_eigen'] for a in private),
        'memory_max_abs_coherence':max(a['memory_post_offdiagonal_abs'] for a in private),
        'failure_count':meta['failure_count']}
    if bandit:
        result.update({'realized_mismatch_count':sum(r['y'] for r in public),
            'realized_mismatch_fraction':float(np.mean([r['y'] for r in public])),
            'whitening_seconds':sum(r['diagnostics']['whitening_seconds'] for r in public),
            'decoder_matrix_compilation_seconds':sum(r['diagnostics']['decoder_matrix_compilation_seconds'] for r in public),
            'prox_seconds':sum(r['update']['prox_seconds'] for r in public),
            'newton_iterations_total':sum(r['update']['newton_iterations'] for r in public),
            'newton_iterations_max':max(r['update']['newton_iterations'] for r in public),
            'newton_backtracks_total':sum(r['update']['newton_backtracks'] for r in public),
            'max_stationarity_residual':max(r['update']['stationarity_residual'] for r in public),
            'stationarity_target':meta['delta'],
            'max_locality_squared':max(r['update']['locality_squared'] for r in public),
            'min_played_eigen':min(r['diagnostics']['played_eigen_min'] for r in public),
            'min_center_eigen':min(r['diagnostics']['center_eigen_min'] for r in public),
            'max_played_tp_residual':max(r['diagnostics']['played_tp_residual'] for r in public),
            'max_unitary_residual':max(r['diagnostics']['unitary_residual'] for r in public),
            'max_kraus_tp_residual':max(r['diagnostics']['kraus_tp_residual'] for r in public),
            'max_dual_variance_bound_ratio':max(r['update']['dual_norm_squared']/r['update']['variance_bound'] for r in public if r['y']),
            'max_hessian_condition':max(r['diagnostics']['center_hessian_condition'] for r in public),
            'final_theta_norm':float(np.linalg.norm(learner.theta)),
            'general_probe_decoder_count':len(public),'matrix_unitary_dimension':8})
    else:
        result.update({'decoder_svd_seconds':sum(r['diagnostics']['decoder_svd_seconds'] for r in public),
            'update_seconds':sum(r['diagnostics']['update_seconds'] for r in public),
            'general_probe_decoder_count':0,'local_pauli_measurement_count':len(public)})
    (directory/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('runs',type=Path);a=p.parse_args()
    summaries=[summarize(d) for d in sorted(a.runs.iterdir()) if d.is_dir()]
    (a.runs/'aggregate_summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
    for s in summaries:
        print(s['run'], 'policy',round(s['played_policy_mean_bell_loss'],6),
              'oracle',round(s['known_U_oracle_mean_bell_loss'],6),
              'identity',round(s['identity_no_learning_mean_bell_loss'],6),
              'final(retrospective)',round(s['final_decoder_retrospective_past_occupation_loss'],6))
