"""Build a compact manifest and report table from completed, saved runs."""
import json,math,shutil
from pathlib import Path
import numpy as np
from control_search import CollisionModel,trace_pair,policy_stats

base=Path(__file__).resolve().parent;results=base/'results'
# Earlier exploratory filenames used decimal angle strings. Preserve their exact
# checkpoints under unambiguous canonical names and reconstruct their metadata.
lines=[json.loads(s) for s in (base/'m2_scaling.log').read_text().splitlines() if s.startswith('{"m"')]
for theta,n,tag in [(.5,37,'05'),(.3,262,'03'),(.2,1283,'02')]:
 old=results/f'm2_t{theta:g}_n{n}_prefix.npz';new=results/f'm2_t{tag}_n{n}_prefix.npz'
 if old.exists():
  if not new.exists():shutil.copyfile(old,new)
  data=np.load(new);model=CollisionModel(2,theta);fe=trace_pair(model.terminal_cost(data['decoder']),data['states'][-1])
  hist=[x for x in lines if x['theta']==theta and x['n']==n]
  meta=dict(m=2,C=1,theta=theta,n=n,init='prefix',fidelity=fe,error=1-fe,history=hist,
            policy_stats=policy_stats(data['policy'],2),metadata_reconstructed_from_saved_checkpoint=True)
  new.with_suffix('.json').write_text(json.dumps(meta,indent=2))

spec=[
 ('m2_t07_n12_prefix','Unrestricted nonselective; capture start'),
 ('m2_t05_n37_prefix','Unrestricted nonselective; capture start'),
 ('m2_t03_n262_prefix','Unrestricted nonselective; capture start'),
 ('m2_t02_n1283_prefix','Unrestricted nonselective; capture start'),
 ('m4_t07_n12_prefix','Unrestricted nonselective; capture start'),
 ('m4_t07_n12_random05_scs','Unrestricted nonselective; random start'),
 ('m4_t07_n12_random15_scs','Unrestricted nonselective; second random start'),
 ('feedback_m2_C2_t07_n12_prefix','Two-state feedback; capture start'),
 ('feedback_m2_C2_t07_n12_random','Two-state feedback; random start'),
 ('feedback_m2_C2_t05_n37','Two-state feedback'),
 ('feedback_m2_C2_t03_n262','Two-state feedback'),
 ('feedback_m2_C4_t05_n37','Four-state feedback'),
 ('feedback_m2_C4_t03_n262','Four-state feedback'),
 ('gauge_j05_t07_n12','Payload × spin-1/2 gauge, tracial'),
 ('gauge_j05_t05_n37','Payload × spin-1/2 gauge, tracial'),
 ('gauge_j1_t05_n37','Payload × spin-1 gauge, tracial'),
 ('gauge_j2_t05_n37','Payload × spin-2 gauge, tracial'),
 ('gauge_j2_north_t05_n37','Payload × spin-2 gauge, pure north'),
 ('gauge_j4_north_t05_n37','Payload × spin-4 gauge, pure north'),
 ('gauge_j4_random_t05_n37','Payload × spin-4 gauge, generic pure'),
 ('gauge_j2_t03_n262','Payload × spin-2 gauge, tracial'),
 ('gauge_j2_north_t03_n262','Payload × spin-2 gauge, pure north'),
 ('rotor_L1_t05_n37_matched','Coherent regular SO(3) frame, j=0,1'),
 ('cascade_k2_t03_n262','Two-qubit pure matched-cascade start'),
 ('cascade_k3_t05_n37','Three-qubit pure matched-cascade start'),
 ('cascade_k3_t03_n262','Three-qubit pure matched-cascade start')]
rows=[]
for stem,label in spec:
 p=results/(stem+'.json')
 if not p.exists():raise RuntimeError('Run not yet completed: '+str(p))
 d=json.loads(p.read_text());m=d['m'];theta=d['theta'];n=d['n'];ps=d.get('policy_stats',{})
 tp=d.get('maximum_tp_residual',ps.get('max_tp_residual'))
 mineig=d.get('minimum_choi_eigenvalue',d.get('minimum_coefficient_eigenvalue',ps.get('min_eigenvalue')))
 if tp is not None and tp>1e-7:raise RuntimeError('Large TP residual '+stem)
 if mineig is not None and mineig < -1e-7:raise RuntimeError('Large CP violation '+stem)
 rows.append(dict(label=label,theta=theta,n=n,m=m,retained_qubits=math.ceil(math.log2(m)),classical_states=d.get('C',1),
                  fidelity=d['fidelity'],halfdiamond_error_after_twirl=1-d['fidelity'],
                  passive_buffer_fidelity=1-.75*(1-np.sin(theta)**4)**n,
                  initial_fidelity=d['history'][0]['fidelity'],sweeps=len(d['history'])-1,
                  maximum_tp_residual=tp,minimum_cp_eigenvalue=mineig,
                  metadata_path=str(p.relative_to(base)),policy_path=str((results/(stem+'.npz')).relative_to(base))))
manifest=dict(status='all_selected_runs_completed',notes=['Coordinate-ascent feasible policies, not certified global optima.','Classical labels are not coherent memory. Generic physical workspace and service queues are accounted separately in the report.','Reported half-diamond error is attained after the explicit global Clifford twirl.','Decimal values are numerical diagnostics, not interval-certified sharp thresholds.'],runs=rows)
(base/'numerical_summary.json').write_text(json.dumps(manifest,indent=2))
text=['## Completed numerical results','', '| Receiver | θ | N | m (qubits) | C | F_e | Twirled error | Passive-buffer F_e |','|---|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:
 text.append(f"| {r['label']} | {r['theta']:.2g} | {r['n']} | {r['m']} ({r['retained_qubits']}) | {r['classical_states']} | {r['fidelity']:.8f} | {r['halfdiamond_error_after_twirl']:.8f} | {r['passive_buffer_fidelity']:.8f} |")
text += ['', 'Here m counts the retained coded quantum space. The generic serial physical realization additionally counts the current carrier and a measured ancillary qubit; arithmetic, routing and queues can add more. C is the number of retained classical controller labels. Frame and cascade searches have C=1 and are restricted covariant-control searches with the stated initial states.', '',
         'All selected runs completed. The largest selected trace-preservation residual is '+f"{max(r['maximum_tp_residual'] or 0 for r in rows):.3g}"+'; the smallest selected repaired CP eigenvalue is '+f"{min(r['minimum_cp_eigenvalue'] or 0 for r in rows):.3g}"+'.', '',
         '## Reproducibility and file map', '',
         '- `numerical_summary.json`: complete selected-run parameters, fidelities, physicality residuals, and exact paths to replayable NPZ policies and JSON histories.',
         '- `control_search.py`, `control_selftest.json`: unrestricted nonselective coordinate SDPs and short-horizon validation.',
         '- `feedback_control.py`, `feedback_selftest.json`: finite classical-state instrument optimization and validation.',
         '- `rep_control.py`: arbitrary physical SU(2) representation blocks, CPTP constraints, Kraus propagation, and scalar/multiplicity optimization.',
         '- `spin_gauge_control.py`, `spin_gauge_selftest.json`: fixed-J tracial and asymmetric initialized gauges.',
         '- `rotor_control.py`: coherent regular-frame control, including right multiplicities.',
         '- `cascade_control.py`: independently pure matched-cascade starts with all stages optimized; propagation cross-checked against the independent channel constructor.',
         '- `policy_ledger.py` and the `*_ledger.json` result files: balanced-Petz acquisition and irreversible-loss diagnostics.',
         '- `covariant_control.py`, `covariant_selftest.json`: the first tensor-qubit Schur-block implementation. Its early exploratory searches are not used as the primary performance benchmarks when the later representation implementation supplies a stronger run.',
         '- `build_numerical_summary.py`: regenerates this selected-run table from saved results.', '',
         'Examples from the present directory:', '', '```bash',
         'python control_search.py --self-test',
         "python control_search.py --m 4 --theta .7 --n 12 --sweeps 12 --init 'random:0.5' --solver SCS --tol .000001 --out results/replay_nonselective",
         "python feedback_control.py --m 2 --C 2 --theta .3 --n 262 --sweeps 12 --init 'random:0.1' --out results/replay_feedback",
         "python spin_gauge_control.py --j 2 --gauge-state north --theta .3 --n 262 --sweeps 12 --init 'random:0.1' --out results/replay_gauge",
         'python rotor_control.py --cutoff 1 --theta .5 --n 37 --sweeps 6 --initial identity --seed-policy matched --solver SCS --tol .0000001 --out results/replay_rotor',
         'python cascade_control.py --k 3 --theta .3 --n 262 --frame triad --sweeps 10 --out results/replay_cascade',
         '```', '', 'The scripts use NumPy, SciPy and CVXPY with CLARABEL/SCS. They cap numerical-library threads at one so concurrent cases do not silently oversubscribe the host. Exact solver versions and hardware can change runtime and the local basin reached. The saved policies, rather than a claim of unique optimizer output, are the reproducible operation.']
report=base/'continuation_mechanism_report.md';content=report.read_text().split('<!-- COMPLETED_RESULTS -->')[0]
report.write_text(content+'<!-- COMPLETED_RESULTS -->\n\n'+'\n'.join(text)+'\n')
print(json.dumps(dict(runs=len(rows),max_tp=max(r['maximum_tp_residual'] or 0 for r in rows),min_cp=min(r['minimum_cp_eigenvalue'] or 0 for r in rows),report=str(report)),indent=2))
