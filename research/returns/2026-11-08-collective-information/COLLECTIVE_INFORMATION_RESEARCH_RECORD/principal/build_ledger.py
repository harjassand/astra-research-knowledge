from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[1]
spec=[
('RELATIVE_FORM','PROVED','Nonautonomous common-metric gap-free estimate','principal/RELATIVE_ENERGY_CONSTRUCTION.md'),
('CONDITIONAL_COARSE','PROVED','Conditional relative fluctuations yield retained predictions','principal/RELATIVE_ENERGY_CONSTRUCTION.md'),
('UNIFORM_CC','PROVED','Count-shell constant independent of block count and size','principal/RELATIVE_ENERGY_CONSTRUCTION.md'),
('CALIBRATION','PROVED_WITH_APPARATUS_CONTRACT','Finite-noisy positive mobility acquisition','principal/RELATIVE_ENERGY_CONSTRUCTION.md'),
('MASS_REPAIR','PROVED_FROZEN_CONTROL','Changed equilibrium mass with8d/(1-d) bound','principal/MASS_METRIC_REPAIR.md'),
('THERMAL_ACTION','PROVED_BOUNDED_ACTION','Changing-energy error W exp(K)D(d)','auditor/REVIEW_RELATIVE_ENERGY.md'),
('FINITE_T','PROVED_FINITE_HORIZON','Arbitrary-source Poisson closure and learned-rate KL','auditor/REVIEW_RELATIVE_ENERGY.md'),
('RESIDUAL_W','PROVED_CONDITIONAL_EFFICIENCY','Interacting conditional acquisition requires quantitative gap','machinery/FOLLOWUP.md'),
('LIFETIME','PROVED_SPECIFIED_SOURCE','Gibbs conditioned on entire transient complement; Schur relative mean','auditor/REVIEW_RELATIVE_ENERGY.md'),
('WRITER','PROVED_WITH_APPARATUS_CONTRACT','Bounded-increment finite-temperature pin/throttle preparation','auditor/REVIEW_RELATIVE_ENERGY.md'),
('UNKNOWN_U','PROVED_ONE_BLOCK','Acquire count-energy increments; no automatic size transfer','auditor/REVIEW_RELATIVE_ENERGY.md'),
('NUMERICS','PROVED_FINITE_Q','Positive numerical semigroup polynomial in log horizon; q charged','principal/EVALUATION_AND_PREPARATION.md'),
('LOCAL_CONTRACTION','PROVED_RESTRICTED','Common Dobrushin local-window prediction; full window dimension charged','initial/machinery.md'),
('MEAN_FIELD','PROVED_RESTRICTED','Kac nonlinear field; fixed dimension/horizon and paid pair isolation','initial/constructor.md'),
('PRIMAL_CELL','PROVED','Issued-bond open-current coefficient; fresh ghosts and all marks','constructor/FOLLOWUP.md'),
('DUAL_CELL','PROVED','Closed count-sector correlation; frozen exterior and explicit gap','constructor/DUAL_ADAPTIVE_BRACKET.md'),
('ADAPTIVE_D','PROVED_DECLARED_CLASS','Density-uniform effective coefficient stopping with observed duality gap','constructor/DUAL_ADAPTIVE_BRACKET.md'),
('PDE','PROVED_1D','Nonlinear primitive, Fourier and Euler error; no hidden solver','constructor/FOLLOWUP.md'),
('SUCCINCT_CORRECTOR','PROVED_DECLARED_ORACLE','Fixed-seed finite Poisson program; log input-cardinality rather than enumeration','principal/SUCCINCT_POISSON_CORRECTOR.md'),
('OBSERVED_RESIDUAL','PROVED_DECLARED_CLASS','Admissible density-free corrector with observed all-density constitutive residual','constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md'),
('CANONICAL_VARIANCE','PROVED_1D_FIXED_BARE_RANGE','All-count and all-bare-exterior variance; freeze corrector before replacement growth','constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md'),
('SPECTRAL_REPLACEMENT','PROVED_PRESCRIBED_WEIGHTS','Block-to-ring spectral and signed integrated expectation bound; no state-dependent weights or path supremum','constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md'),
('INVARIANT_WEIGHT','PROVED_FIXED_GENERATOR','Sector-invariant nonlinear test weights and explicit approximate-invariance budget','principal/INVARIANT_WEIGHT_LIFT.md'),
('DISCRETE_PRIMITIVE','PROVED_AUXILIARY','Exact count-window flux primitive and Fourier noise budget; nonlinear closure remains open','principal/NONLINEAR_CLOSURE_ATTACK.md'),
('FINITE_N_SERVICE','OPEN_NOT_ACHIEVED','Effective inhomogeneous nonlinear finite-system prediction and arbitrary-force closure','constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md'),
('FINITE_N_PROTOCOL','CONDITIONAL_EFFECTIVE_CONSTANTS','Finite homogeneous kinetic-protocol hydrodynamics; not arbitrary forcing','constructor/FOLLOWUP.md'),
('KINETIC_CLOCK','DISPROVED_SHORTCUT','Equilibrium does not identify new-drive kinetic prefactors','initial/auditor.md'),
('HIDDEN_HISTORY','DISPROVED_SHORTCUT','Vanishing passive kernel does not imply reusable driven closure','initial/auditor.md'),
('RARE_CLOCK','PROVED_OBSTRUCTION','Unforced kinetic exposure can scale inverse rare rate','initial/auditor.md'),
('PARITY_NOISE','PROVED_OBSTRUCTION','Small collective alphabet does not remove detector conditioning','initial/auditor.md'),
('MASS_RATE_SHORTCUT','DISPROVED_SHORTCUT','Small per-edge error can cause large stationary macro error','auditor/REVIEW_RELATIVE_ENERGY.md'),
('GENERIC_GOAL','OPEN_NOT_ACHIEVED','Generic sufficient fields, constructed kinetics and growing controlled reuse','principal/CONSOLIDATED_DOSSIER.md')]
a=[]
for i,st,claim,f in spec:
 p=r/f;a.append(dict(id=i,status=st,statement=claim,proof=f,complete_assumptions='All hypotheses and quantifiers in the named proof section; none omitted by this summary.',proof_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),historical_novelty='UNKNOWN_OR_ESTABLISHED_MACHINERY'))
o=dict(date_local='2026-11-07',timezone='Australia/Brisbane',research_return='COMPLETE_AT_REPORTED_SCOPES',broad_objective='NOT_ACHIEVED_OPEN',historical_novelty='UNKNOWN',practical_advantage='NOT_ESTABLISHED',physical_experiments=0,record_directory='COLLECTIVE_INFORMATION_RESEARCH_RECORD',proof_paths_relative_to_record=True,claims=a)
(r/'COLLECTIVE_INFORMATION_THEOREM_LEDGER.json').write_text(json.dumps(o,indent=2));print(len(a))
