#!/usr/bin/env python3
"""Build the curated decision view without changing cards, sources or their status.

The explicit relations and gates below are curation, not inferred theorem edges.
SQL is read-only. This file is confined to the frontier layer.
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'frontier'
DB = sqlite3.connect(f'file:{ROOT / "indexes/knowledge.sqlite3"}?mode=ro', uri=True)
DB.row_factory = sqlite3.Row
CLAIMS = [json.loads(x) for x in (ROOT / 'indexes/claims.jsonl').read_text().splitlines()]
FILES = {x['path']: x for x in map(json.loads, (ROOT / 'indexes/files.jsonl').read_text().splitlines())}
BY_ID = {x['id']: x for x in CLAIMS}
ALIASES = {x['id'].split('-')[0]: x['id'] for x in CLAIMS if x['id'].startswith('N')}
CACHE = {}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def cid(short):
    return ALIASES.get(short, short)

def evidence(path, start=1, end=None, scope='curated cited passage'):
    """Line numbers refer to the immutable indexed text, or the direct state file."""
    if path not in CACHE:
        row = DB.execute('SELECT id,path,sha256,text,extraction FROM docs WHERE path=?', (path,)).fetchone()
        if row:
            value = dict(row)
            value['lines_count'] = max(1, len(value['text'].splitlines()))
            # Indexed sha is text identity; original byte identity may differ for extraction.
            value['text_hash_verified'] = hashlib.sha256(value['text'].encode()).hexdigest() == value['sha256']
        else:
            p = ROOT / path
            if not p.is_file():
                raise ValueError(f'Missing evidence: {path}')
            text = p.read_text()
            value = {'path': path, 'sha256': digest(p), 'text': text,
                     'lines_count': max(1, len(text.splitlines())), 'text_hash_verified': True}
        CACHE[path] = value
    d = CACHE[path]
    end = d['lines_count'] if end is None else end
    if not 1 <= start <= end <= d['lines_count']:
        raise ValueError(f'Invalid evidence range: {path}:{start}-{end}')
    out = {'path': path, 'sha256': d['sha256'], 'lines': [start, end], 'range_scope': scope}
    if 'id' in d:
        out['source_id'] = d['id']
        out['read_path'] = f'web/pages/{d["id"]}.html'
        out['hash_kind'] = 'indexed_utf8_text'
        f = FILES.get(path)
        if f:
            out['original_sha256'] = f['sha256']
            out['original_object_path'] = f'evidence/objects/{f["sha256"][:2]}/{f["sha256"][2:]}'
    else:
        out['read_path'] = path
        out['hash_kind'] = 'direct_utf8_file'
    return out

def card_ev(short, start=1, end=None):
    return evidence(BY_ID[cid(short)]['path'], start, end)

def write_jsonl(name, rows):
    (OUT / name).write_text(''.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '\n' for x in rows))

# These are identified proof-bearing documents. Presence does not assert full coverage,
# validity, independent reconstruction, or that every cited external premise is available.
PROOF_TEXT = {
    'N342': [('updates/AZ/package/research/outputs/universal-entropy-pi/general-origin/INDEPENDENT_MODULAR_GRAM_PROOF.txt', 1, None), ('updates/AZ/package/research/outputs/universal-entropy-pi/general-physical-audit/EXPOSED_AUDIT.txt', 1, None), ('updates/AZ/package/research/outputs/universal-entropy-pi/general-representation/REPRESENTATION_AUDIT_FROZEN_v1.txt', 1, None)],
    'N343': [('updates/AZ/package/research/outputs/universal-entropy-pi/general-independent-variance/EXPOSED_COMPARISON_AND_NONLINEAR_SHARPNESS.txt', 1, None)],
    'N344': [('updates/AZ/package/research/outputs/universal-entropy-pi/general-canonical-consequences/ALL_DIMENSION_FIXED_COMPARATOR_THEOREM.txt', 1, None)],
    'N345': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/kms-origin/INDEPENDENT_ALL_P_PROFILE_PROOF.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/kms-independent/EXPOSED_ROOT_DILATION_AUDIT.txt', 1, None)],
    'N346': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-lower/EXPOSED_FINITE_P_IMPROVED_PROFILE_PROOF.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-lower/FORWARD_PI_OVER_TWO_HARDY_PROOF.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-upper-review/PHASE_UPPER_AUDIT_FROZEN_v1.txt', 1, None)],
    'N347': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-upper/ERRATUM_PHYSICAL_HAMILTONIAN.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/kms-origin/CONCRETE_QUTRIT_STRONG_P3_COUNTERFAMILY.txt', 1, None)],
    'N348': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/raw-origin/RAW_FIXED_MARGIN_CANONICAL_POWER_PROOF.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/raw-review/EXPOSED_AUDIT.txt', 1, None)],
    'N349': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/stationarity-origin/INDEPENDENT_BASELINE.txt', 1, None), ('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/petz-review/EXPOSED_BINARY_ENDPOINT_AUDIT.txt', 1, None)],
    'N350': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/root/ROOT_POLAR_KATO_AND_SINE_HYPERCONTRACTIVITY.txt', 1, None)],
    'N351': [('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/raw-origin/RAW_COPY_DEFICIT_AND_CLASSICAL_MEDIATOR.txt', 1, None)],

    'N330': [('updates/AY/package/BROADCAST_TREE_COMPARISON.txt', 22, 391)],
    'N331': [('updates/AY/package/BROADCAST_TREE_COMPARISON.txt', 445, 539)],
    'N332': [('updates/AY/package/BROADCAST_TREE_COMPARISON.txt', 392, 444)],
    'N333': [('updates/AY/package/COARSE_KERNEL_AND_STATIONARY_SMOOTHING.tex', 47, 445)],
    'N334': [('updates/AY/package/COARSE_KERNEL_AND_STATIONARY_SMOOTHING.tex', 453, 626)],
    'N335': [('updates/AY/package/CUBIC_ETALE_RATIONAL_DETECTOR.txt', 7, 171)],
    'N336': [('updates/AY/package/CUBIC_ETALE_RATIONAL_DETECTOR.txt', 172, 251)],
    'N337': [('updates/AY/package/EUCLIDEAN_REAL_LOCUS_S3_COVER.txt', 7, 113)],
    'N338': [('updates/AY/package/EUCLIDEAN_REAL_LOCUS_S3_COVER.txt', 114, 167)],
    'N339': [('updates/AY/package/FIXED_FLOW_STOCHASTIC_LIFETIMES.txt', 36, 144)],
    'N340': [('updates/AY/package/FIXED_FLOW_STOCHASTIC_LIFETIMES.txt', 9, 35), ('updates/AY/package/FIXED_FLOW_STOCHASTIC_LIFETIMES.txt', 145, 329)],

    'N322': [('updates/AX/package/novelty_and_consequences/ASM_COUNTING_SPACE_BRIDGE.md', 22, 104)],
    'N323': [('updates/AX/package/novelty_and_consequences/ASM_COUNTING_SPACE_BRIDGE.md', 105, 127), ('updates/AX/package/novelty_and_consequences/NOVELTY_AND_FOUNDATIONAL_CONSEQUENCES.md', 21, 104)],
    'N324': [('updates/AX/package/number_theory_bridges/ALGEBRAIC_LOGARITHM_CANDIDATE.md', 53, 222)],
    'N325': [('updates/AX/package/number_theory_bridges/ALGEBRAIC_LOGARITHM_CANDIDATE.md', 27, 52), ('updates/AX/package/algebraic_log_audit/BLIND_RECONSTRUCTION.md', 1, 86)],
    'N326': [('updates/AX/package/number_theory_bridges/EMBEDDING_GATE_AND_NOGO.md', 1, 89)],
    'N328': [('updates/AX/package/SYMPLECTIC_USER_REPORT.txt', 30, 229)],
    'N329': [('updates/AX/package/SYMPLECTIC_USER_REPORT.txt', 230, 313)],

    'N308': [('updates/AW/package/research/outputs/broadcasting-theorems/orthogonal/PROOF.txt', 5, 174)],
    'N309': [('updates/AW/package/research/outputs/broadcasting-theorems/tensor/NONSELFADJOINT_MIXED_SPAN_THEOREM.txt', 9, 248)],
    'N310': [('updates/AW/package/research/work/agents/spin1_anisotropic_sol/SPIN1_ALL_WEIGHTS_THEOREM.txt', 5, 236)],
    'N311': [('updates/AW/package/research/outputs/broadcasting-theorems/tensor/FULL_QUTRIT_TENSOR_THEOREM.txt', 7, 273)],
    'N312': [('updates/AW/package/research/work/agents/tensor_frame_sol/PROOF.txt', 6, 446)],
    'N313': [('updates/AW/package/research/work/agents/covariant_obstruction_sol/PROOF_REPORT.txt', 88, 150)],
    'N314': [('updates/AW/package/research/work/agents/covariant_obstruction_sol/PROOF_REPORT.txt', 199, 318)],
    'N315': [('updates/AW/package/research/work/agents/covariant_obstruction_sol/PROOF_REPORT.txt', 151, 198)],
    'N316': [('updates/AW/package/research/work/agents/quadratic_dilation_sol/PARAMETRIC_MOMENT_OBSTRUCTION.txt', 1, 117)],
    'N317': [('updates/AW/package/research/work/agents/variance_monogamy_sol/TRIPARTITE_SCOPE_OBSTRUCTION.txt', 1, 97)],
    'N318': [('updates/AW/package/research/work/agents/variance_monogamy_sol/general_escalation/C5_OBSTRUCTION_AND_GLUING.txt', 1, 152)],
    'N319': [('updates/AW/package/research/work/agents/covariant_obstruction_sol/all_spin_escalation/REPORT.txt', 1, 306)],
    'N321': [('updates/AW/package/research/work/agents/variance_monogamy_sol/general_escalation/DUAL_INTERFACE.txt', 1, 78), ('updates/AW/package/research/work/agents/broadcasting_proof_sol/GENERAL_GATE_AND_FAILED_ROUTES.txt', 1, 148)],

    'N304': [('updates/AV/package/INVESTIGATION.md', 17, 79)],
    'N305': [('updates/AV/package/INVESTIGATION.md', 81, 153)],
    'N306': [('updates/AV/package/INVESTIGATION.md', 155, 212)],

    'N298': [('updates/AU/package/space_simulation/HISTORY_INDEPENDENT_HF_SPACE_SIMULATION.md', 5, 182), ('updates/AU/package/space_simulation/DIMENSION_AND_BINARY_COMPILER_AUDIT.md', 13, 300)],
    'N299': [('updates/AU/package/space_simulation/HISTORY_INDEPENDENT_HF_SPACE_SIMULATION.md', 35, 170)],
    'N300': [('updates/AU/package/space_simulation/HISTORY_INDEPENDENT_HF_SPACE_SIMULATION.md', 59, 110)],
    'N301': [('updates/AU/package/space_simulation/DIMENSION_AND_BINARY_COMPILER_AUDIT.md', 13, 242)],
    'N302': [('updates/AU/package/space_simulation/HISTORY_INDEPENDENT_HF_SPACE_SIMULATION.md', 171, 182), ('updates/AU/package/space_simulation/DIMENSION_AND_BINARY_COMPILER_AUDIT.md', 277, 300)],

    'N292': [('updates/AT/package/reports/FOUNDATIONAL_GAUSSIAN_CHECKPOINT.txt', 45, 83)],
    'N293': [('updates/AT/package/reports/FOUNDATIONAL_GAUSSIAN_CHECKPOINT.txt', 84, 146)],
    'N294': [('updates/AT/package/reports/FOUNDATIONAL_GAUSSIAN_CHECKPOINT.txt', 147, 174)],
    'N295': [('updates/AT/package/reports/FOUNDATIONAL_GAUSSIAN_CHECKPOINT.txt', 175, 210)],
    'N296': [('updates/AT/package/reports/FOUNDATIONAL_GAUSSIAN_CHECKPOINT.txt', 211, 264)],

    'N276': [('updates/AS/package/ultra/work/agents/ppt_cube_chain_sol/PROOF.txt', 1, None)],
    'N277': [('updates/AS/package/ultra/work/agents/broadcasting_proof_sol/CLIFFORD_FACTOR_TWO.txt', 1, None)],
    'N278': [('updates/AS/package/ultra/work/agents/broadcasting_proof_sol/GENERAL_GATE_AND_FAILED_ROUTES.txt', 1, None)],
    'N279': [('updates/AS/package/ultra/work/agents/algebra_proof_recon/PROOF.txt', 1, None)],
    'N280': [('updates/AS/package/ultra/work/agents/complexity_proof_recon.txt', 1, None)],
    'N281': [('updates/AS/package/ultra/work/agents/foundational_transfer_sol/proofs.txt', 1, None)],
    'N282': [('updates/AS/package/ultra/work/agents/ppt_index_tangent_sol/PROOFS.txt', 1, None)],
    'N283': [('updates/AS/package/ultra/work/agents/ppt_cube_chain_sol/PHASE_D_ALIGNMENT.txt', 1, None)],
    'N284': [('updates/AS/package/ultra/work/agents/ppt_index_tangent_sol/PHASE_D_ROTATIONS.txt', 1, None)],
    'N285': [('updates/AS/package/first/proof_mining/EXPONENTIAL_INTERPRETATION_SPACE_CANDIDATE.md', 1, None)],
    'N286': [('updates/AS/package/first/vector_cofilling/uniform_vector_cofilling_audit.md', 1, None)],
    'N287': [('updates/AS/package/first/support_audit/characteristic_two_automorphism_boundary.md', 1, None)],
    'N288': [('updates/AS/package/first/entropy_audit/GENERAL_CENTRAL_ENTROPY_THEOREM.md', 1, None)],
    'N289': [('updates/AS/package/first/contact/CONTACT_REPORT.md', 1, None)],
    'N290': [('updates/AS/package/first/frontier/GAUSSIAN_PAIR_COMPOSITION_LEMMA.md', 1, None)],

    'N272': [('updates/AR/package/reports/SOL_B_COCYCLE_ABSORPTION.txt', 1, None)],
    'N273': [('updates/AR/package/reports/SOL_B_COCYCLE_ABSORPTION.txt', 1, None)],
    'N274': [('updates/AR/package/reports/SOL_B_COCYCLE_ABSORPTION.txt', 1, None)],
    'N275': [('updates/AR/package/reports/SOL_B_COCYCLE_ABSORPTION.txt', 1, None)],

    'N265': [('updates/AQ/package/reports/01_AFFINE_RATIONAL_SMOOTHING.md', 1, None)],
    'N266': [('updates/AQ/package/reports/01_AFFINE_RATIONAL_SMOOTHING.md', 1, None)],
    'N267': [('updates/AQ/package/reports/01_AFFINE_RATIONAL_SMOOTHING.md', 1, None)],
    'N268': [('updates/AQ/package/reports/02_FREE_SUBGROUP_RANDOM_BASIS.txt', 1, None)],
    'N269': [('updates/AQ/package/reports/02_FREE_SUBGROUP_RANDOM_BASIS.txt', 1, None)],
    'N270': [('updates/AQ/package/reports/02_FREE_SUBGROUP_RANDOM_BASIS.txt', 1, None)],

    'N246': [('updates/AP/package/pit/RESEARCH_STATE.md', 1, None)],
    'N247': [('updates/AP/package/pit/RESEARCH_STATE.md', 1, None)],
    'N248': [('updates/AP/package/pit/RESEARCH_STATE.md', 1, None)],
    'N249': [('updates/AP/package/pit/RESEARCH_STATE.md', 1, None)],
    'N250': [('updates/AP/package/pit/RESEARCH_STATE.md', 1, None)],
    'N251': [('updates/AP/package/reports/02_RELATIVE_BERNOULLI_SPLITTING.txt', 1, None)],
    'N252': [('updates/AP/package/reports/06_FINITE_POWER_EXTRACTION.txt', 1, None)],
    'N253': [('updates/AP/package/reports/06_FINITE_POWER_EXTRACTION.txt', 1, None)],
    'N254': [('updates/AP/package/reports/03_TRACK_A_COCYCLE.txt', 1, None)],
    'N255': [('updates/AP/package/reports/03_TRACK_A_COCYCLE.txt', 1, None)],
    'N256': [('updates/AP/package/reports/03_TRACK_A_COCYCLE.txt', 1, None)],
    'N257': [('updates/AP/package/reports/04_TRACK_B_NONCOLLAPSE.txt', 1, None)],
    'N258': [('updates/AP/package/reports/04_TRACK_B_NONCOLLAPSE.txt', 1, None)],
    'N259': [('updates/AP/package/reports/05_RANK_TOPOLOGY_BARRIERS.txt', 1, None)],
    'N260': [('updates/AP/package/reports/05_RANK_TOPOLOGY_BARRIERS.txt', 1, None)],
    'N261': [('updates/AP/package/reports/05_RANK_TOPOLOGY_BARRIERS.txt', 1, None)],
    'N262': [('updates/AP/package/branches/research/2026-10-08-independent-geometry-audit/RESEARCH_REPORT.md', 1, None)],
    'N263': [('updates/AP/package/branches/state/2026-10-08-steklov-kyfan-growth-budget.md', 1, None)],

    'N227': [('updates/AO/package/proofs/chemistry/ORDER5_FROZEN.md', 1, None), ('updates/AO/package/proofs/chemistry/ORDER5_EXACT_RATE_CLASSIFICATION.md', 1, None), ('updates/AO/package/proofs/rate_phase_blind/report.md', 1, None)],
    'N228': [('updates/AO/package/proofs/chem_explosion_blind/phase2/no_pure_cubic_nonexplosion.md', 1, None), ('updates/AO/package/proofs/chem_explosion_blind/phase2/both_pure_cubic_nonexplosion.md', 1, None), ('updates/AO/package/proofs/cubic_one_pure_blind/proof_v1.md', 1, None), ('updates/AO/package/proofs/integration/two_species_cubic_composition_scope_v1.md', 1, None)],
    'N229': [('updates/AO/package/proofs/chemistry/ORDER4_NONEXPLOSIVE_NEARMISS.md', 1, None)],
    'N230': [('updates/AO/package/proofs/concentration_blind/CONCENTRATION_FROZEN_REPORT.txt', 15, 302)],
    'N231': [('updates/AO/package/proofs/qudit_blind/proof.md', 5, 239)],
    'N232': [('updates/AO/package/proofs/thermal/centered_relative_entropy_FROZEN.md', 5, 107)],
    'N233': [('updates/AO/package/proofs/sharp_centered/SHARP_CENTERED_FROZEN_REPORT.txt', 15, 317)],
    'N234': [('updates/AO/package/proofs/thermal/centered_relative_entropy_FROZEN.md', 108, 130)],
    'N235': [('updates/AO/package/proofs/heat_upper_blind/upper_FROZEN.md', 5, 304)],
    'N236': [('updates/AO/package/proofs/heat_upper_blind/calibration_addendum_FROZEN.md', 5, 190)],
    'N237': [('updates/AO/package/proofs/thermal/original_derivation.md', 5, 76), ('updates/AO/package/proofs/integration/mean_casimir_centered_counterexample_v1.md', 1, 35)],
    'N238': [('updates/AO/package/proofs/curie_weiss/CRITICAL_PROOF_FROZEN.md', 5, 280), ('updates/AO/package/proofs/critical_quantitative_audit/INDEPENDENT_PROOF.md', 1, 316)],
    'N239': [('updates/AO/package/proofs/critical_quantitative_audit/INDEPENDENT_PROOF.md', 1, 316)],
    'N240': [('updates/AO/package/proofs/geometry_blind/li_wang_derivation.md', 5, 130), ('updates/AO/package/proofs/geometry_lower_audit/report.md', 1, None)],
    'N241': [('updates/AO/package/proofs/integration/minasyan_application_independent_v1.md', 1, 31), ('updates/AO/package/proofs/algebra/report.md', 1, None)],
    'N242': [('updates/AO/package/proofs/tcs/PROOF_v2.md', 1, None), ('updates/AO/package/proofs/tcs/SOURCE_INTERFACE_FAILURE.md', 1, None)],
    'N243': [('updates/AO/package/proofs/statistics/proof.md', 1, None)],
    'N244': [('updates/AO/package/proofs/independent/phase2/DERIVATION.md', 1, None)],

    'N213': [('updates/AM/package/PROOF.md', 7, 282)],
    'N214': [('updates/AM/package/PROOF.md', 64, 193)],
    'N215': [('updates/AM/package/PROOF.md', 283, 343)],
    'N216': [('updates/AM/package/PROOF.md', 344, 375)],
    'N217': [('updates/AM/package/verify_obstruction.py', 59, 89)],
    'N219': [('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md', 9, 48), ('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md', 226, 386)],
    'N220': [('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md', 49, 291)],
    'N221': [('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md', 292, 368)],
    'N222': [('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md', 146, 225)],
    'N223': [('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md', 19, 42)],
    'N224': [('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md', 43, 65)],
    'N225': [('updates/AN/package/proofs/ITERATION_AND_LIMIT_BARRIERS.md', 5, None)],

    'N210': [('updates/AL/package/state/2026-10-08-steklov-capacity/RESEARCH.md',8,122)],
    'N211': [('updates/AL/package/state/2026-10-08-steklov-capacity/RESEARCH.md',33,122)],
    'N212': [('updates/AL/package/state/2026-10-08-critical-lamperti-explosion/RESEARCH_STATE.md',95,178),('updates/AL/package/state/2026-10-08-stochastic-universality/RESULT_AND_RESTART.md',72,108)],
    'N195': [('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 54, 72), ('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 229, 314)],
    'N196': [('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 131, 228)],
    'N197': [('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 73, 118), ('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 315, 376)],
    'N198': [('updates/AJ/package/CASIMIR_EXTREMALITY_AND_ENTROPY.md', 5, 55)],
    'N199': [('updates/AJ/package/CASIMIR_EXTREMALITY_AND_ENTROPY.md', 56, 128)],
    'N200': [('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 377, 427)],
    'N201': [('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md', 428, 451)],
    'N203': [('updates/AK/package/state/2026-10-08-sud-singlet-separability/RESEARCH_STATE.md', 1, None)],
    'N204': [('updates/AK/package/state/2026-10-08-sud-singlet-separability/EXACT_GLOBAL_SINGLET_ENTANGLEMENT.md', 5, 108)],
    'N205': [('updates/AK/package/state/2026-10-08-sud-singlet-separability/FINITE_N_AUDIT.md', 5, 120)],
    'N206': [('updates/AK/package/state/2026-10-08-convex-gradient-diophantine/RESEARCH_STATE.md', 14, 89)],
    'N207': [('updates/AK/package/state/2026-10-08-convex-gradient-diophantine/DETAILED_BALANCE_OBSTRUCTION.md', 5, 46), ('updates/AK/package/state/2026-10-08-convex-gradient-diophantine/KINETIC_REALIZATION_GATE.md', 5, 43)],
    'N208': [('updates/AK/package/state/2026-10-08-family197-maximizing-tail/FAMILY197_RESEARCH.md', 31, 216)],
    'N209': [('updates/AK/package/state/2026-10-08-critical-lamperti-explosion/RESEARCH_STATE.md', 20, 150)],

    'N175': [('updates/AI/package/work/agents/common_metric_attack/PROOF_v3.txt', 1, None), ('updates/AI/package/work/agents/common_metric_attack/POST_SOURCE_STATUS.txt', 1, None)],
    'N176': [('updates/AI/package/work/agents/common_metric_attack/PROOF_v3.txt', 114, None), ('updates/AI/package/work/agents/geometry_transfer_audit/POSTFREEZE_AUDIT.txt', 1, None)],
    'N177': [('updates/AI/package/work/agents/spectral_transversality_audit/REPORT.txt', 1, None), ('updates/AI/package/work/agents/spectral_exact_double_audit/REPORT.txt', 1, None), ('updates/AI/package/work/agents/spectral_crossblock_audit/REPORT.txt', 1, None)],
    'N178': [('updates/AI/package/work/agents/common_metric_attack/PROOF_v3.txt', 213, 258), ('updates/AI/package/work/agents/geometry_uniformity_redteam/REPORT.txt', 1, None)],
    'N179': [('updates/AI/package/work/agents/thermal_window/REPORT.txt', 27, 222), ('updates/AI/package/work/agents/thermal_window/COST_ADDENDUM.txt', 1, None)],
    'N180': [('updates/AI/package/work/agents/thermal_blind/REPORT.txt', 1, None)],
    'N181': [('updates/AI/package/work/agents/chemical_recurrence/REPORT.txt', 1, None), ('updates/AI/package/work/agents/critical_crn_blind/REPORT.txt', 1, None)],
    'N182': [('updates/AI/package/work/agents/chemical_recurrence/RETURN_TIME_ADDENDUM.txt', 1, None)],
    'N183': [('updates/AI/package/work/agents/repetition_application/COUNTEREXAMPLE.txt', 1, 47)],
    'N184': [('updates/AI/package/work/agents/repetition_application/REPAIRED_DETYPING_GAP.txt', 1, 71)],
    'N185': [('updates/AI/package/work/agents/thermodynamic_inference/REPORT.txt', 35, 158), ('updates/AI/package/work/agents/entropy_blind_audit/REPORT.txt', 1, None)],
    'N186': [('updates/AI/package/work/agents/thermodynamic_inference/REPORT.txt', 159, 239)],
    'N187': [('updates/AI/package/work/agents/kls_mechanism/REPORT.txt', 28, 257)],
    'N188': [('updates/AI/package/work/agents/learning_acquisition/REPORT.txt', 62, 186), ('updates/AI/package/work/agents/learning_acquisition/REPORT.txt', 246, 268)],
    'N189': [('updates/AI/package/work/agents/learning_acquisition/REPORT.txt', 186, 245)],
    'N190': [('updates/AI/package/work/agents/epr_parity/DETERMINANT_LIFT_FINAL.txt', 1, None)],
    'N191': [('updates/AI/package/work/agents/epr_parity/DETERMINANT_LIFT_FINAL.txt', 1, None)],
    'N192': [('updates/AI/package/work/agents/epr_matroid_gluing/REPORT.txt', 28, 75), ('updates/AI/package/work/agents/epr_matroid_gluing/REPORT.txt', 136, 151)],
    'N193': [('updates/AI/package/work/agents/epr_matroid_gluing/REPORT.txt', 76, 118), ('updates/AI/package/work/agents/epr_parity/DETERMINANT_LIFT_FINAL.txt', 1, None)],
    'N174': [('updates/AH/package/state/2026-10-08-family197-infinite-tail/RESEARCH.md', 97, 114)],
    'N165': [('updates/AG/package/state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md', 94, 110)],
    'N166': [('updates/AG/package/state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md', 11, 81)],
    'N167': [('updates/AG/package/state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md', 83, 93)],
    'N168': [('updates/AG/package/state/2026-10-08-family197-support-expansion-entropy.md', 13, 52)],
    'N169': [('updates/AG/package/state/2026-10-08-family197-coding-and-model-audits/RESEARCH.md', 11, 83)],
    'N170': [('updates/AG/package/state/2026-10-08-family197-infinite-tail/RESEARCH.md', 16, 73)],
    'N171': [('updates/AG/package/state/2026-10-08-reversible-singular-explosion/RESEARCH_STATE.md', 11, 25)],
    'N172': [('updates/AG/package/state/2026-10-08-reversible-singular-explosion/RESEARCH_STATE.md', 27, 90)],
    'N173': [('updates/AG/package/state/2026-10-08-log-valuation-permanence/PROOF_AND_AUDIT.md', 22, 165)],
    'N160': [('updates/AF/package/THEOREM_AND_PROOF.md', 9, 79), ('updates/AF/package/THEOREM_AND_PROOF.md', 121, 324)],
    'N161': [('updates/AF/package/THEOREM_AND_PROOF.md', 79, 324)],
    'N162': [('updates/AF/package/THEOREM_AND_PROOF.md', 325, 363)],
    'N163': [('updates/AF/package/THEOREM_AND_PROOF.md', 364, 472)],
    'N06': [('updates/L/package/work/nonsofic_adversary.md', 31, 148)],
    'N07': [('updates/L/package/work/critical_gaussian_audit.md', 11, 231)],
    'N09': [('updates/L/package/work/unknown_field.md', 84, 490)],
    'N18': [('updates/M/package/work/deep/energy_exponent_audit.md', 18, 120)],
    'N20': [('updates/M/package/work/deep/critical_gibbs_audit.md', 35, 345)],
    'N21': [('updates/M/package/work/deep/memory_endpoint_audit.md', 31, 245)],
    'N62': [('updates/S/package/hard_energy_detection.tex', 1, None)],
    'N143': [('updates/AD/package/checkpoint/evidence/c4_quantum_lift/FINAL_REPORT.md', 13, 78)],
    'N145': [('updates/AD/package/checkpoint/evidence/c12_effective_permanence/EFFECTIVE_FIXED_FAMILY.md', 3, 104)],
    'N148': [('updates/AE/package/research/sol_collision_precision/IID_PINCHED_JOINT.txt', 1, 436)],
    'N150': [('updates/AE/package/research/sol_xxz_coexistence/proof.txt', 11, 386)],
    'N153': [('updates/AE/package/research/sol_semiclassical_memory/wall_su3/analytic_spectral_gate/LOW_WINDOW_JACOBI_PROOF.txt', 1, 250)],
    'N154': [('updates/AE/package/research/sol_classicality/COLLECTIVE_LIE_GIBBS_SCHUR_ARCHIVE_PROOF.txt', 1, 421)],
    'N155': [('updates/AE/package/research/sol_classicality/COLLECTIVE_NATURAL_GIBBS_ARCHIVE_PROOF.txt', 1, 368)],
    'N156': [('updates/AE/package/research/sol_boson_4d_audit/RESULT.txt', 1, 394)],
    'N157': [('updates/AE/package/research/sol_boson_2d/QUARTIC_EB_OBSTRUCTION.txt', 34, 198)],
    'N158': [('updates/AE/package/research/sol_collective_critical/proof.txt', 1, 408)],
}

ROWS = {}
for claim in CLAIMS:
    path = ROOT / claim['path']
    lines = path.read_text().splitlines()
    short = claim['id'].split('-')[0]
    status = lines[1] if len(lines) > 1 else ''
    source_pointers = [evidence(p, scope='whole indexed cited source; finer claim-to-proof mapping unclassified')
                       for p in claim.get('source_paths', [])]
    located = [evidence(p, a, b, 'identified technical proof text; completeness and correctness not audited here')
               for p, a, b in PROOF_TEXT.get(short, [])]
    summary_only = any(s in status.lower() for s in (
        'result-summary only', 'summary retained;linked full proof/package absent',
        'summary preserved; linked sandbox proof/checkpoint not supplied',
        'full linked proof/code/results absent', 'linked sandbox full proof/packet unavailable'))
    if located:
        availability = 'proof_text_located_not_completeness_audited'
    elif summary_only:
        availability = 'summary_only_at_original_cited_version'
    elif 'pdf' in status.lower() and short == 'N129':
        availability = 'provisional_manuscript_available'
    else:
        availability = 'cited_source_inventory_available_proof_scope_unclassified'
    deps = []
    for target in claim.get('depends_on', []):
        deps.append({'target': cid(target), 'scope': 'Dependency explicitly recorded in original claim ledger; exact use must be reopened.',
                     'relation_status': 'declared_not_independently_validated', 'evidence': [card_ev(claim['id'])]})
    for dep in claim.get('scoped_dependencies', []):
        if dep['relation'].startswith('requires'):
            deps.append({'target': cid(dep['id']), 'scope': dep['relation'],
                         'relation_status': 'declared_not_independently_validated', 'evidence': [card_ev(claim['id'])]})
    ROWS[claim['id']] = {
        'schema_version': 1, 'card_id': claim['id'], 'card_path': claim['path'],
        'card_sha256': digest(path), 'title': claim['title'], 'topics': claim['topics'],
        'claim_status': claim['status'], 'reported_status': status,
        'status_authority': 'original claim ledger and immutable card; later notices remain separately scoped',
        'proof_availability': {
            'classification': availability, 'classification_scope': 'cited version only; no exhaustive scientific proof audit',
            'located_proof_sources': located, 'available_evidence_sources': source_pointers,
            'unavailable_or_unclassified': 'Linked full packet absent at cited version' if summary_only else 'Completeness of all subclaims and imported premises unclassified',
        },
        'validation': {'internal': 'as reported in immutable card; no new scientific replay or proof reconstruction in this restructure',
                       'external_correctness': 'not established by this layer', 'historical_priority': 'not established by this layer',
                       'reported_status_evidence': [card_ev(claim['id'], 2, 2)]},
        'supersedes': [], 'invalidates': [], 'depends_on': deps,
        'requires_external_validation': [{'target': 'external:correctness_and_scope_review',
            'scope': 'Consequential scientific use requires source/interface review; this status view does not establish external correctness or priority.',
            'evidence': [card_ev(claim['id'], 2, 2)]}],
        'material_updates': [], 'contrasting_blockers': [],
        'relation_coverage': 'explicit curated subset plus existing declared dependencies; unlisted relations UNKNOWN',
    }

def relation(owner, kind, target, scope, ev, component=None):
    owner, target = cid(owner), cid(target)
    rel = {'target': target, 'scope': scope, 'relation_status': 'source_supported_scoped_notice_not_correctness_promotion', 'evidence': ev}
    if component:
        rel.update(target_component=component, whole_claim_invalidated=False)
    ROWS[owner][kind].append(rel)
    if target in ROWS:
        notice = dict(rel, target=owner, relation=kind, source_card=owner)
        ROWS[target]['material_updates'].append(notice)

relation('N160', 'supersedes', 'N135',
    'Candidate sharp identical-unital boundary tr(TT^T)=1 and three-axis/halftrace separation for fixed T and nu_N=o(sqrtN) strengthen the historical sufficient depolarizing lambda>sqrt(pi/8) to lambda>1/sqrt3. The old sufficient bound remains valid; only its exact-threshold open gate is addressed. Full new proof/code available, no independent intake reconstruction or external correctness/priority verification. No uniform shrinking channel-gap or critical-bath transfer.',
    [evidence('updates/AF/package/THEOREM_AND_PROOF.md', 41, 77), evidence('updates/AF/package/THEOREM_AND_PROOF.md', 276, 324)],
    component='exact post-preparation identical-unital threshold; historical sufficient bound retained')
relation('N136', 'supersedes', 'N132',
    'Newer candidate one-quarter upper closes the historical one-quarter versus one-half coefficient gap ONLY for the specified family, fixed admissible bath and t>=T_sep. The lower argument and historical proof remain available. Full newer packet is absent; newer is not externally verified.',
    [card_ev('N136', 5, 7), card_ev('N132', 5, 8)])
relation('N137', 'supersedes', 'N133',
    'Newer candidate sufficient time gives actual singleton separability for all N>=2 under the stated ideal unnormalized bath and strict interior occupation. It improves a sufficient preparation claim; it does not invalidate the old PPT theorem or enlarge the N4 fixture scope.',
    [card_ev('N137', 5, 8), card_ev('N133', 5, 10)])
relation('N62', 'supersedes', 'N32',
    'Exact hard-support asymptotic reliability formula extends the earlier summary/two-use witness under its hard energy ceiling. It does not replace N18 expected-cost law.',
    [card_ev('N62', 5, 10)])
relation('N159', 'invalidates', 'N65',
    'AE cycle7 actual-origin instantiation used LABEL coordinates instead of retained MARK POINT coordinates. d_O=s and dependent block moduli/audits do not instantiate the true origin. Abstract stipulated-size block models remain valid; no N65 theorem refutation follows.',
    [evidence('updates/AE/package/research/root_checks/N65_POINT_LABEL_CORRECTION.txt', 4, 33), card_ev('N159', 7, 7)],
    component='AE/groups_operator/cycle7 actual-origin blocks and audits')
relation('N154', 'depends_on', 'N01',
    'Order/Jensen/Schur mechanism is existing N01 capital, not a new classicality principle. The new all-copy/general-carrier quantitative contracts and supplied H0 conditions must be checked separately.',
    [evidence('updates/AE/package/research/RESTART.txt', 44, 53), card_ev('N154', 5, 7)])
relation('N136', 'depends_on', 'N131',
    'Angular-test and conditional-laboratory KL lower used for the regularized lower bound; preserve arbitrary cross-copy correlation within each laboratory.',
    [card_ev('N136', 5, 6)])
relation('N136', 'depends_on', 'N137',
    'The candidate finite-time sharp law is asserted for t>=the N137 sufficient T_sep in the same ideal bath model.',
    [card_ev('N136', 5, 5)])

relation('N174', 'supersedes', 'N170',
    'Pinned branch followup adds the finite-stage full-shift-conjugate linear SFT tower and inclusion of the full shift inflated from the maximal residually finite quotient in the non-SFT tail. Original tail deduction remains valid; no entropy or measurable-conjugacy resolution, no claim that the quotient subsystem exhausts the tail.',
    [evidence('updates/AH/package/state/2026-10-08-family197-infinite-tail/RESEARCH.md',97,114)],
    component='additional finite-stage and finite-quotient tail structure; original theorem retained')

# AI source modules advance scoped contracts while keeping historical raw cards.
relation('N179', 'supersedes', 'N138',
    'At the stationary nu_N/sqrt(N)->fixed c>0 window, the new authored proof constructs a FULLSEP approximant with explicit asymptotic upper integral (about5.82e-5 atc1) and charged sampler/precision costs. N180 supplies an independent bounded-effect lower bound for c<c_w. This partially advances the historical window gap; exact distance, intrinsic phase boundary and useful finite-N convergence rates remain open. It does not supply the absent AC sharp entropy proof or transfer to post-preparation noise.',
    [evidence('updates/AI/package/work/agents/thermal_window/REPORT.txt',84,222),evidence('updates/AI/package/work/agents/thermal_blind/REPORT.txt',1,145)],
    component='critical sqrt(N) stationary-bath window: partial bounds, not full phase diagram')
relation('N187', 'supersedes', 'N75',
    'New candidate sharp actual-KL cap functional and exact first-Neumann-gradient diffuse product witness strengthen the earlier mean/covariance plateau obstruction under the stated weaker contract. Cov/P tends1/4, not0; no KLS proof/refutation or imported high-order/posterior hierarchy certification. Historical N75 retained.',
    [evidence('updates/AI/package/work/agents/kls_mechanism/REPORT.txt',28,257)],
    component='mean-only actual-information replacement obstruction; anomalous KLS gate remains open')
for short in [f'N{n}' for n in range(175,195)]:
    key=cid(short)
    ROWS[key]['status_authority']='Immutable AI curated card; packet CLAIM_LEDGER current status, geometry POST_SOURCE_STATUS and EPR DETERMINANT_LIFT_FINAL/cactus REPORT Section9 take precedence over explicitly retained historical source freezes; chronology alone does not certify correctness.'
    ROWS[key]['proof_availability']['unavailable_or_unclassified']='Authored proof/audit/script modules retained; third-party originals listed in AI SOURCE_OMISSIONS are absent from this packet; full subclaim/import completeness unclassified.'

# AJ/AK additions remain scoped candidates, with distinct engineered/thermal inputs.
relation('N208', 'supersedes', 'N170',
    'Under the original torsion-free one-sided-inverse premise, the newly captured branch adds relative entropy h(X|Theta)=h(X) and a free mixing residual Haar action attaining the finite-entropy supremum. Original entropy sign and measurable conjugacy remain open; no branch timestamp is proof validation. Its additional Baumslag-Solitar route still depends on the disputed printed positive-characteristic attribution N165.',
    [evidence('updates/AK/package/state/2026-10-08-family197-maximizing-tail/FAMILY197_RESEARCH.md',31,216)], component='conditional relative entropy and supremal tail; original algebraic structure retained')
relation('N208', 'supersedes', 'N174',
    'Adds a conditional maximizing-tail entropy identity to the earlier finite-stage and finite-quotient structural refinement; neither determines the original group entropy sign or Bernoulli isomorphism.',
    [evidence('updates/AK/package/state/2026-10-08-family197-maximizing-tail/FAMILY197_RESEARCH.md',179,216)], component='conditional tail entropy only')
relation('N209', 'supersedes', 'N181',
    'The catalytic polynomial factor (A)_p preserves the named base jump chain but changes its physical clock. The branch candidate classifies explosion iff kappa<2lambda and p>=3, including nonexplosive critical equality. The original p=0 recurrence classification is retained, not contradicted; inherited deterministic geometry is not reconstructed here.',
    [evidence('updates/AK/package/state/2026-10-08-critical-lamperti-explosion/RESEARCH_STATE.md',20,150)], component='new polynomial catalytic clock and critical explosion boundary')
relation('N197', 'depends_on', 'N195',
    'The finite local bounded-score theorem requires the engineered factorial input with tight j=O(1). It does not address G-UNITAL-NOISE-BOUNDED-SCORES for the older thermal input with j~sqrt(N).',
    [evidence('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md',73,118),evidence('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md',483,492)])
for n in range(195,210):
    key=cid('N'+str(n))
    ROWS[key]['status_authority']='Immutable AJ supplied-folder or AK pinned-branch source and scoped curated card; source-reported analytic/finite checks, no intake scientific replay or independent proof reconstruction. Newer does not imply correctness.'
    ROWS[key]['proof_availability']['unavailable_or_unclassified']='Full identified authored proof/code text available for technical cards; completeness of imported published premises and all subclaims unclassified. N202 is an evidence-scope record, not a separate general proof.'
ROWS[cid('N208')]['requires_external_validation'].append({'target':'external:positive_characteristic_BLR_scope', 'scope':'The ADDITIONAL Baumslag-Solitar application uses a disputed printed positive-characteristic theorem. Do not reuse it unconditionally; N165 discrepancy remains open. The relative/tail entropy argument has a separately stated torsion-free premise.', 'evidence':[evidence('updates/AK/package/state/2026-10-08-family197-maximizing-tail/FAMILY197_RESEARCH.md',236,248),card_ev('N165')]})

relation('N212', 'supersedes', 'N209',
    'The late pinned source retains the balanced theorem and adds a second leading-drift representation plus a direct deterministic/endotactic reconstruction. Its complete all-positive-rate phase diagram is CONDITIONAL on separately inherited unequal-rate source arguments, not newly reverified here. The AK source/card remain immutable at their earlier version.',
    [evidence('updates/AL/package/state/2026-10-08-critical-lamperti-explosion/RESEARCH_STATE.md',95,178),evidence('updates/AL/package/state/2026-10-08-stochastic-universality/RESULT_AND_RESTART.md',72,108)],component='late drift/structural proof and inherited unequal-rate combination')
relation('N210', 'depends_on', 'N175',
    'ONLY the matching geometric lower-coefficient corollary requires independently validating N175 and all the additional slow-polar-end regularities. The upper bound itself does not use N175; no unconditional geometric optimality or Ricci-only theorem follows.',
    [evidence('updates/AL/package/state/2026-10-08-steklov-capacity/RESEARCH.md',111,122)])
for n in range(210,213):
    ROWS[cid('N'+str(n))]['status_authority']='Immutable AL pinned late-branch source and scoped card. All10 frozen tips in main ancestry; branch merge and finite diagnostics do not validate general proofs or priority.'

# AM/AN source packages: scoped mathematical advances, no correctness promotion.
relation('N220','supersedes','N213',
    'The separate partial-transpose-invariant ensemble improves the sufficient dimension/rank constant from 2^24 to 2^23 and supplies both transpose symmetries. Quantitative halftrace margins differ (7/3200 versus 1/576); do not combine constants across ensembles. Both linear-order arguments and the unresolved d=4,k=2 gate remain. Established Gaussian antecedents credited; neither proof externally verified.',
    [evidence('updates/AM/package/PROOF.md',7,63),evidence('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md',49,79)],component='stronger sufficient dimension constant and PT-invariant construction; prior ensemble retained')
relation('N223','supersedes','N195',
    'Adds an explicit one-copy Schmidt-rank-two negative partial-transpose vector on the engineered factorial family after grouping two qubits against the rest, for even N>=4. Does not contradict singleton separability, depth two, universal survival, or claim all grouped cuts/distillability rates. A successful local filter yields an entangled two-qubit pair; no pure Bell pair from one copy or efficient success-rate guarantee.',
    [evidence('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md',19,42)],component='explicit grouped 2:rest one-copy distillability; original engineered-family theorem retained')
for target in ['N198','N199']:
    relation('N224','invalidates',target,
        'The laboratory-separable cross-copy Bell comparator gives singlet-overlap 1/8 at N=4, exceeding the naive single-copy squared bound 1/9. This refutes the overlap-multiplicativity shortcut only. The exact single-copy optimizer and ln(N)+O(1) entropy remain; regularized logarithmic law is unresolved and local noisy N197 is separate.',
        [evidence('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md',49,65)],component='proposed cross-copy overlap multiplicativity transfer, not single-copy theorem')
for owner,target in [('N215','N225'),('N225','N215')]:
    ROWS[cid(owner)]['material_updates'].append({'target':cid(target),'source_card':cid(target),'relation':'parallel_construction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Both physical Gaussian PPT-channel ensembles have entanglement-breaking squares. AM uses a general complex projected Gaussian and AN a real separately PT-invariant ensemble with exact index two. Distinct normalizations/constants; no logical dependence or composition-conjecture resolution. Gurvits-Barnum ball is imported only for these square corollaries.','evidence':[card_ev(target)]})
for n in range(213,227):
    ROWS[cid('N'+str(n))]['status_authority']='Immutable AM/AN authored proofs and scoped cards; exact original archives retained. AM selected17 repository blobs verified at d20c4b0; AN earlier pinned repository is orientation only. Main positive-map arguments do not import unverified Astra/release candidates. Source-reported internal checks, no intake scientific replay or external correctness/priority clearance.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full authored proof/audit/script/result modules retained; bibliography read scopes retained, external primary-paper byte captures absent. N218/N226 are evidence-scope records. Full subclaim/import completeness unclassified.'

# AO paused checkpoint: exact ledger current, source-reported reviews only.
relation('N233','supersedes','N232',
    'Adds the sharp centered Petz supremum coefficient3 and explicit finite remainder to the earlier white-Schur big-O theorem. Actual product marginal, arbitrary within-sector states and both parities retained. Asymptotic extremizers are not exact finite optimizers; no sharp KL/testing constant.',
    [evidence('updates/AO/package/proofs/sharp_centered/SHARP_CENTERED_FROZEN_REPORT.txt',15,64)],component='sharp Petz coefficient only, earlier quadratic theorem retained')
relation('N235','supersedes','N232',
    'The later finite three-axis upper closes only the source-file historical growing-r ALLSEP upper question in centered_relative_entropy Section7. Requires a positive polarization-gap floor and all readout outcomes, with charged preparations/calibration. The earlier centered lower remains and the broad concentration theorem has no generic matched certification upper.',
    [evidence('updates/AO/package/proofs/thermal/centered_relative_entropy_FROZEN.md',128,130),evidence('updates/AO/package/proofs/heat_upper_blind/upper_FROZEN.md',5,52)],component='historical narrower-class growing-r certification upper availability')
relation('N237','invalidates','N232',
    'Refutes only the proposed extension from exact white sector weights to a mean-Casimir-only promise: a rare polarized sector yields centered entropy Omega(r/N). The exact-white theorem and weaker mean-only trace corollary remain valid candidates.',
    [evidence('updates/AO/package/proofs/integration/mean_casimir_centered_counterexample_v1.md',1,35)],component='mean-only extension, not exact-white theorem')
relation('N239','invalidates','N238',
    'A separately constructed fully separable rare-symmetric-sector mixture has the same limiting critical mean/pair scale but vanishing trace/KL at every subsystem size; chi-square can diverge. This refutes mean/pair/chi-only extrapolation, not the exact critical Gibbs theorem or its bounded witnesses.',
    [evidence('updates/AO/package/proofs/critical_quantitative_audit/INDEPENDENT_PROOF.md',1,316)],component='extension replacing exact Gibbs law with mean/pair or chi-only data')
relation('N240','supersedes','N210',
    'A directly attributed Li-Wang energy-Gram corollary gives the same3D upper coefficient for compact positive total-area4pi polar links without slow variation, pointwise-common area form or radial-derivative assumptions. N210/N211 sufficient slow-class method retained; the broader upper is a routine published-method application, not a new headline discovery. Matching lower still depends on independently validating inherited N175 and class membership; no endpoint attainment or Ricci-only theorem.',
    [evidence('updates/AO/package/proofs/geometry_blind/li_wang_derivation.md',5,130)],component='3D sufficient polar hypotheses and prior-art ranking, older higher-d formula not replaced')
relation('N242','supersedes','N184',
    'Refines the still-open downstream final-answer-reduction wire gate: protected independent branches support an ideal-law gap, but recognizable probability1/3 cannot be exactly generated by a finite uniform binary-field seed. Actual adjusted four-role and detyped-prefix implementation remains conditional. Does not invalidate the repaired predicate or prove a compression refutation.',
    [evidence('updates/AO/package/proofs/tcs/report.md',5,15),evidence('updates/AO/package/proofs/tcs/SOURCE_INTERFACE_FAILURE.md',1,None)],component='actual downstream sampler/gap gate, repaired predicate retained')
for n in range(227,246):
    ROWS[cid('N'+str(n))]['status_authority']='Immutable AO original checkpoint and source CLAIM_LEDGER26 exact contracts; later ledger/final reports take precedence over preserved preliminary pending-audit notes. Source-reported fresh target-only derivations, argument-exposed reconstructions and finite diagnostics are separate scopes, no intake independent proof reconstruction/replay or external/formal correctness/priority clearance. Programme user-reported paused; archived continuation text is data.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Authored technical proofs/audits/code/results available; primary full-paper bytes excluded from distributable ZIP, versions/hashes/read scopes retained. Completeness of all imported proofs and subclaims unclassified.'
ROWS[cid('N245')]['proof_availability']['available_evidence_sources'] += [evidence('updates/AO/package/'+p,scope='authoritative checkpoint metadata and reported review/replay scope, not proof certification') for p in ['REPORT.md','CLAIM_LEDGER.json','PROVENANCE_AND_REPRODUCTION.md','PACKAGE_MANIFEST.json','verification/REPLAY_SUMMARY.json','process/resource_usage.json']]

# AP six foundational reports, independently pinned missing branch capture.
relation('N253','supersedes','N251',
    'The later finite-power coloring/right-inverse argument obtains arbitrary finite-entropy Bernoulli direct factors of X and infinite weak Pinsker entropy without the earlier inhomogeneous-extension relative-isomorphism application. It neither validates nor refutes the earlier K-squared extraction claim. Residual cancellation and Bernoulli conjugacy remain unproved; group-ring torsion-free premises conditional.',
    [evidence('updates/AP/package/reports/06_FINITE_POWER_EXTRACTION.txt')],component='alternative proof route for X splitting and weak Pinsker conclusion only')
relation('N263','supersedes','N210',
    'The variable-angular-measure birth-degree proof permits bounded time variation of smoothly precompact polar angular metrics with convergent area, retaining an O(p) measure-derivative correction. Same limsup coefficient and new liminf/birth-degree organization in every stated dimension; no general Ricci-only result. A convergent scalar f/r does not alone bound the derivative of its rescaled angular metric, so the fixed-area proof and general Theorem B require separate interface checks.',
    [evidence('updates/AP/package/branches/state/2026-10-08-steklov-kyfan-growth-budget.md')],component='polar sufficient assumptions and additional birth-degree/liminf bound, existence unverified')
for owner,target,scope in [
 ('N253','N166','Adds conditional infinite weak Pinsker direct-product extraction, not a change to the strict finite supremal Rokhlin upper or a proof of the original entropy sign. Weak Pinsker and Rokhlin entropy are distinct invariants.'),
 ('N254','N174','Adds infinite mixing residual tail and cyclic Bernoulli restrictions, not a G-Bernoulli tail or an entropy separator.'),
 ('N256','N170','Canonical tail projections are iid at a coordinate and linear shears stay one-half apart in measure; no naive convergent linear Hilbert-hotel limit. A different nonlinear measurable conjugacy is not excluded.'),
 ('N262','N210','Time-averaged variable-area capacity removes the scalar rf-prime/f limit by exact integrated endpoint cancellation, under slowly varying smoothly precompact angular geometry. Historically novel status unverified.'),
 ('N263','N240','Parallel all-dimensional Steklov/birth-degree organization; N240 broader attributed published three-dimensional energy-Gram corollary and priority downgrade remain current. No chronological novelty promotion.'),
 ('N259','N65','Rank-two faithful linear models block rectangular-separation-only transfers; the original finite-field permutation construction is retained.'),
 ('N260','N65','Characteristic-zero inner rank blocks the naive low-rank lift, without establishing a unitary-microstate obstruction.'),
 ('N261','N65','Conditional L2 homology and classical embedding barriers narrow the Singer route; no counterexample or source-geometry certification.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_scoped_extension_or_transfer_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(246,265):
    ROWS[cid('N'+str(n))]['status_authority']='AP immutable six pasted reports, original PIT authored archive and captured Git blobs; explicit source-ledger mapping. Complete arguments are source-reported and premises remain conditional. No intake scientific replay, independent proof reconstruction, formal/external correctness or priority certification; merge is preservation only.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Identified written proofs in reports available, plus full PIT verifier/fixtures/archive and geometry proof/code. Other linked sandbox checkpoints and primary-paper copies absent. All imported premise completeness and relative-isomorphism application unclassified.'
ROWS[cid('N251')]['requires_external_validation'].append({'target':'external:relative_isomorphism_to_G_conjugacy','scope':'Independently check the precise Hoff Lemma3.3.7/Thouvenot orbit-equivalence-relation to G-equivariant homogeneous Bernoulli extension interface. Later finite-power proof avoids this interface; not a validation of K-squared extraction.','evidence':[card_ev('N251'),card_ev('N252')]})
for n in [251,252,253,254,255,256]:
    ROWS[cid('N'+str(n))]['requires_external_validation'].append({'target':cid('N165'),'scope':'Conditional on an actual torsion-free F2 group-ring one-sided inverse/witness; published Lean torsion-bearing scope does not prove the companion torsion-free claim. Do not import disputed positive-characteristic citation unconditionally.','evidence':[card_ev('N165'),card_ev('N252')]})

# AQ rational smoothing and free-subgroup/random-basis reports; no status promotion.
for owner,target,scope in [
 ('N268','N254','The source claims a full continuous nonatomic Bernoulli restriction for the defect K on infinite-index free subgroups, whereas N254 concerns a distinct residual tail and cyclic factors. No global G conjugacy follows; exact FIR/duality premises need review.'),
 ('N269','N256','Adds a distinct iid-pivot-thinning finite-relation obstruction and no global equivariant random well-order. Correlated local-priority bases and nonlinear measurable conjugacy are not excluded.'),
 ('N270','N255','A measurable equivariant F2-vector-space basis of Rp would give a separate conditionally linear sufficient conjugacy route, avoiding residual cancellation/cocycle stabilization. No such basis is constructed; both spanning and independence are required.'),
 ('N270','N252','The new source explicitly inherits finite-defect extraction as a working lemma with audit deferred. Its basis route bypasses that lemma; this does not independently validate or refute N252, nor establish finite-power Bernoullicity.'),
 ('N270','N253','The unconstructed equivariant basis route would yield two-versus-four Bernoulli conjugacy directly from Haar splitting without cancelling the finite residual. It does not close N253 residual Bernoullicity or original Rokhlin-entropy gates.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_parallel_route_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(265,272):
    ROWS[cid('N'+str(n))]['status_authority']='AQ exact separately authored reports and clearly separated intake clarification; source analytic reconstructions/conditional statements preserved, no independent intake proof reconstruction, scientific replay or external correctness/priority certification.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full report text available; no scientific script/output or external primary-paper fulltext supplied. Imported H10(Q), FIR and actual group-ring witness not independently validated; theorem completeness unclassified.'
ROWS[cid('N266')]['requires_external_validation'].append({'target':'external:OpenAI-family004-H10Q-pinned-fd4aeeb2','scope':'Only degree-eight undecidability/Turing-degree corollary imports the unverified H10(Q) theorem. The unconditional source smoothing reduction remains logically separate. Independently reconstruct upstream theorem before asserting undecidability.','evidence':[card_ev('N266')]})
ROWS[cid('N268')]['requires_external_validation'].append({'target':'external:Cohn-free-group-algebra-FIR-exact-scope','scope':'Locate and check exact submodule-freeness theorem, countability, left-coset choice and convolution/duality conventions. Infinite free rank needs finite-generation support argument; separate intake note supplies a clarification, not a whole-proof review receipt. Retain infinite-index assumption.','evidence':[evidence('updates/AQ/package/CURATION_NOTES.md'),card_ev('N268')]})
for n in [268,269,270]:
    ROWS[cid('N'+str(n))]['requires_external_validation'].append({'target':cid('N165'),'scope':'Supply/validate the actual F2[G] one-sided inverse with p nonzero; torsion-free companion construction and positive-characteristic citation discrepancy remain unverified. Source theorem is conditional on the witness, not evidence the witness was acquired.','evidence':[card_ev('N165'),card_ev('N268')]})

# AR residual homology, character coherence, relative spectral and integer-power lifts.
for owner,target,scope in [
 ('N272','N254','The same inherited residual D has source-claimed flat nonprojective dual R/M of projective dimension1, continuum Ext and a pure nonsplit limit. Finite algebraic truncations split. This strengthens an algebraic obstruction, not a nonlinear measurable nonisomorphism.'),
 ('N272','N256','Global algebraic nonprojectivity explains a limit obstruction beyond finite-stage compatibility. It does not exclude all measurable cocycle solutions or contradict conditional finite-power iid extraction.'),
 ('N273','N255','Every nonzero dual-character orbit admits exact scalar cocycle transfers under mixing/torsion-free assumptions; a D-valued transfer additionally requires multiplicative coherence across all characters. No coherent family/witness constructed.'),
 ('N274','N257','The source extends ordinary spectral agreement to full fibre-enriched D-semidir-G Koopman representations for every continuous equivariant fibre automorphism. The Walsh unitary is nonmultiplicative, hence not a spatial Bernoulli conjugacy.'),
 ('N275','N255','Identity-sigma displacement lifting extends to all integer powers sigma_k=(A|D)^k: a supplied insertion Q with X output must admit ThetaLambda=j−tau_k. Explicit forward/inverse formulas remain conditional; the known k1 shift extracts K, not X.'),
 ('N273','N270','The fixed G-permuted-basis obstruction concerns nonprojective Dhat=R/M. N270 seeks an environment-dependent random F2 basis of the distinct projective Rp. This new obstruction does not refute that route or every nonlinear measurable absorption.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_residual_mechanism_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(272,276):
    ROWS[cid('N'+str(n))]['status_authority']='AR exact authored SOL/B report, detailed source curation only. Conditional inherited algebraic witness, residual setup and mixing; no independent intake proof reconstruction, scientific replay, external correctness or historical priority certification. No conjugacy or all-measurable obstruction established.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full written report available; scientific diagnostics/outputs and primary-paper fulltexts not supplied. Actual witness and completeness of imported residual/mixing hypotheses not independently audited.'
    ROWS[cid('N'+str(n))]['requires_external_validation'].append({'target':cid('N165'),'scope':'The report refers to algebraic input in an earlier prompt. Validate an actual countable torsion-free F2[G] one-sided inverse and inherited Haar/residual contracts; do not promote the disputed positive-characteristic citation or any source reconstruction to a supplied verified witness.','evidence':[card_ev('N165'),card_ev('N272')]})

# AS two-record source curation; newer notices do not certify mathematical correctness.
ROWS[cid('N93')]['material_updates'].append({'target':cid('N277'),'source_card':cid('N277'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Clifford-span factor2 and its trace-family corollary are restricted matched-register results; they neither replace the unrestricted output-star control nor establish the general comparator.','evidence':[card_ev('N277')],'whole_claim_invalidated':False})
ROWS[cid('N93')]['material_updates'].append({'target':cid('N278'),'source_card':cid('N278'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Arbitrary-frame one-common-measurement gate is open; canonical support function and legal Choi constraints are explicit. The seven-cycle positive-part rounding failure is not a classicality counterexample.','evidence':[card_ev('N278')],'whole_claim_invalidated':False})
ROWS[cid('N143')]['material_updates'].append({'target':cid('N277'),'source_card':cid('N277'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'One canonical full-domain EB measurement attains factor2 on the specified Clifford span; arbitrary observables remain open.','evidence':[card_ev('N277')],'whole_claim_invalidated':False})
ROWS[cid('N143')]['material_updates'].append({'target':cid('N278'),'source_card':cid('N278'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'General frame bound 2s<=V+k remains unproved; all-direction common POVM is required. Clifford-only proof cannot close it.','evidence':[card_ev('N278')],'whole_claim_invalidated':False})
ROWS[cid('N252')]['material_updates'].append({'target':cid('N279'),'source_card':cid('N279'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Conditional finite-field witness transfers through a cyclic corner and free product to a different essentially-free torsion group; finite coloring/right-inverse extraction applies there.','evidence':[card_ev('N279')],'whole_claim_invalidated':False})
ROWS[cid('N253')]['material_updates'].append({'target':cid('N279'),'source_card':cid('N279'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Conditional binary weak-Pinsker infinity now fits the enlarged group. It does not decide original-group entropy, residual Bernoullicity or two-versus-four conjugacy.','evidence':[card_ev('N279')],'whole_claim_invalidated':False})
ROWS[cid('N165')]['material_updates'].append({'target':cid('N279'),'source_card':cid('N279'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'New-group CRT/free-product implication still requires an actual finite-field one-sided inverse. It does not validate the disputed torsion-free characteristic-p source citation.','evidence':[card_ev('N279')],'whole_claim_invalidated':False})
ROWS[cid('N166')]['material_updates'].append({'target':cid('N279'),'source_card':cid('N279'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Ordinary Rokhlin upper ln2 and enlarged-group weak-Pinsker infinity are distinct from the unresolved original-group strict supremal entropy claim.','evidence':[card_ev('N279')],'whole_claim_invalidated':False})
ROWS[cid('N250')]['material_updates'].append({'target':cid('N280'),'source_card':cid('N280'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Sharp contact on binomial/product classes and rational pullback alphabet costs are scoped advances; general small-circuit contact remains open.','evidence':[card_ev('N280')],'whole_claim_invalidated':False})
ROWS[cid('N250')]['material_updates'].append({'target':cid('N289'),'source_card':cid('N289'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Exact P4 no rank-one-variable determinant at any matrix size excludes one finite compression route; it is not a uniform small-circuit counterfamily.','evidence':[card_ev('N289')],'whole_claim_invalidated':False})
ROWS[cid('N199')]['material_updates'].append({'target':cid('N288'),'source_card':cid('N288'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'All-copy original-laboratory central entropy is now source-claimed Theta(logN) under a bounded log-spin moment. Exact leading coefficient remains in[1/2,1], externally unverified.','evidence':[card_ev('N288')],'whole_claim_invalidated':False})
ROWS[cid('N224')]['material_updates'].append({'target':cid('N288'),'source_card':cid('N288'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Grouped-cut coherent information avoids the refuted cross-copy overlap shortcut; logarithmic regularized order is internally claimed, not exact coefficient or external proof certification.','evidence':[card_ev('N288')],'whole_claim_invalidated':False})
ROWS[cid('N197')]['material_updates'].append({'target':cid('N288'),'source_card':cid('N288'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Same factorial input is covered by a broader central log-spin moment all-copy order candidate; no thermal-family or sharp-coefficient extension follows.','evidence':[card_ev('N288')],'whole_claim_invalidated':False})
ROWS[cid('N225')]['material_updates'].append({'target':cid('N290'),'source_card':cid('N290'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Any pair of admitted Gaussian norm events yields EB composition even with adversarial alignment; distinct draws do not escape the ball argument.','evidence':[card_ev('N290')],'whole_claim_invalidated':False})
ROWS[cid('N215')]['material_updates'].append({'target':cid('N290'),'source_card':cid('N290'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'The broader norm-controlled pair composition strengthens this transfer obstruction; arbitrary PPT composition outside the norm ball remains open.','evidence':[card_ev('N290')],'whole_claim_invalidated':False})
ROWS[cid('N276')]['material_updates'].append({'target':cid('N283'),'source_card':cid('N283'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Separate Hodge-cancelled channel has another exact EB cube certificate; its square/exact index remain unknown. Original-channel square theorem cannot transfer.','evidence':[card_ev('N283')],'whole_claim_invalidated':False})
ROWS[cid('N276')]['material_updates'].append({'target':cid('N284'),'source_card':cid('N284'),'relation':'refines_with_scoped_AS_result_or_obstruction','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':'Specific rotation family has all-real-parameter full Choi rank; six nonzero frozen samples remain UNKNOWN, not proved entangled or separable.','evidence':[card_ev('N284')],'whole_claim_invalidated':False})
for n in range(276,292):
    ROWS[cid('N'+str(n))]['status_authority']='AS immutable two-record capture: first final README/vector/HF audits; Ultra final CLAIM_LEDGER/STATUS. Source-reported mathematical checks/audits, no intake scientific replay, independent proof reconstruction, formal/external correctness or historical novelty clearance. Earlier drafts remain historical.'
    if n<291:
        ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Identified full written modules archived; completeness and imported premises not independently audited. Exact original certificates/checkers available separately. Available proof text is not proof certification.'
ROWS[cid('N276')]['requires_external_validation'].append({'target':'external:AS_square_nonEB','scope':'Exact index3 alone imports the separate source BS square non-EB theorem; the original cube certificate itself does not require it. Finite modular checks do not certify the whole algebraic/formal chain.','evidence':[card_ev('N276')]})
ROWS[cid('N279')]['requires_external_validation'].append({'target':cid('N165'),'scope':'Acquire an actual countable finite-field group-ring one-sided inverse and check the new-group CRT/freeness/coloring contracts; do not certify the disputed original torsion-free source theorem.','evidence':[card_ev('N279'),card_ev('N165')]})

# AT Gaussian checkpoint: restrictions and failed transfers remain explicit.
for owner,target,scope in [
 ('N297','N187','The new checkpoint repeats that mean-only actual-KL cap laws do not meet the full KLS hypotheses. Reported October priority claims lack primary locators; they are not verified solutions or refutations.'),
 ('N297','N75','Claimed October KLS preprints make novelty screening source-dependent; acquire exact primary versions before using priority status. Historical covariance-only obstruction remains scoped, not a KLS resolution.'),
 ('N296','N292','Sector optimality requires balance on every radius. The globally balanced coupled radial comparison is unproved and stronger than the original conjecture; it could fail while the conjecture is true.'),
 ('N294','N293','Slabs can beat the propeller at Hermite level2 while being strictly unstable for total noise stability. A per-level gain does not imply an optimizing partition or a counterexample.'),
 ('N296','N295','Single-profile near-rho1 concavity is false; this does not refute a coupled3-profile inequality with sum profiles1 at every radius. Exact intermediate-correlation comparison remains open.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AT_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(292,298):
    ROWS[cid('N'+str(n))]['status_authority']='AT exact pasted9Oct2026 checkpoint, source internal reconstructions only. Full written arguments retained; no independent intake proof reconstruction, scientific replay, external correctness, formal verification or historical priority clearance. Rendered citation labels are not immutable source locators.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='No separately supplied scientific code/results, audit receipts or external primary fulltexts. Exact circular rearrangement, optimizer dimension-reduction, perimeter asymptotic and KLS-claim theorem/version locators remain UNKNOWN; checkpoint argument presence does not certify imported assumptions.'
ROWS[cid('N296')]['requires_external_validation'].append({'target':'external:AT_dimension_reduction','scope':'Verify the precise optimizer dimension-reduction theorem, dimension/balance/attainment contracts before converting a planar result into a full ambient-dimensional simplex consequence.','evidence':[card_ev('N296')]})
ROWS[cid('N297')]['requires_external_validation'].append({'target':'external:AT_KLS_priority_claims','scope':'Acquire actual primary titles/URLs/immutable versions and exact theorem scopes for source-reported4/6Oct2026 Poincare claims. No historical priority or correctness established by rendered domain labels.','evidence':[card_ev('N297')]})

# AU quantitative HF simulation: current addendum, exact model boundaries.
for owner,target,scope in [
 ('N298','N285','The separate main addendum now internally claims a runtime-independent polynomial peak-state simulation for fixed BGS/Rossman term syntax with ordinary Card and binary/unary input n>=2. This advances the earlier simulation interface, but does not validate the exponential lower-bound inputs or unrestricted bit-space/CPT claims.'),
 ('N301','N285','A resettable fixed-program binary2D compiler is separately supplied with max target universe C(1+S)^(K*r), logical-sort Hartig and duplicate-incidence cleanup. Input remains binary; constants depend on fixed dimensions, arities and width. Strict congruence adds a finite loop, not the automatic-quotient bounded-time guarantee.'),
 ('N302','N285','Conditional transfer now has both quantitative simulation modules available in the specified model. It still requires the separately audited binary hard-pair lower bound and all N286/N287 imported premises. Internal simulation closure is not external proof certification.'),
 ('N302','N286','The transfer retains collective-cochain support, KOW coefficient-uniformity and family243 base homogeneity/equivalence as separate unvalidated imported obligations. The simulation addendum alone cannot certify them.'),
 ('N300','N287','The supplied concrete fresh-set constructor separates atoms from empty sets, saturates all relation coordinates before quotient and stores exact hereditary closure on a transitive domain. This scoped construction does not validate every prior arbitrary-rank quotient-counting input; characteristic2 warnings remain.'),
 ('N303','N287','Negative controls preserve failure of history retention, atom-empty row identification, nontransitive closure restriction and descriptor counting. High-arity faithful startup and tiny-input exceptions are explicit; no scientific scripts were replayed during ingestion.'),
 ('N303','N298','Use peak-over-run hereditary cardinality, fixed term syntax and unary/binary input n>=2. Reserve may exceed current native closure; result is not instantaneous or general bit/Turing-space simulation. Full FO generator/execution and external correctness/novelty remain unestablished.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AU_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(298,304):
    ROWS[cid('N'+str(n))]['status_authority']='AU immutable14-file addendum: root README, main HF simulation proof and final independent audit give current scope. Blind reconstruction is provisional; companion-module HF prerequisites are local historical boundaries superseded by the separate main construction. Scientific proofs/audits/finite checks source-reported; no intake scientific replay, independent proof reconstruction, formal/external correctness or priority clearance.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full authored proof modules, separate audits and3 diagnostic scripts/result JSONs available. Full generated FO compiler was not supplied or executed. GKPS15 URL/DOI/section locators supplied, primary PDF bytes absent; imported lower-bound premises and proof completeness unclassified. N303 is an evidence/limitations record.'
ROWS[cid('N302')]['requires_external_validation'].append({'target':cid('N285'),'scope':'Validate the separate binary2D exponential max-universe hard-pair lower bound and N286/N287 source premises before the HF corollary. Both new simulation stages require fixed program parameters, unchanged binary input size and peak-over-run cardinality; not unrestricted Turing bit space.','evidence':[card_ev('N302'),card_ev('N285'),card_ev('N286'),card_ev('N287')]})

# AV NPT packet: preserve the existential target and exact failure scope.
for owner,target,scope in [
 ('N305','N304','The arbitrary-site product-ray argument applies only when ran(C) or ran(C*) contains a fully product vector. General complex rank-two support planes need not do so; no all-copy NPT theorem follows.'),
 ('N306','N305','Exact entangled-reference co-Choi domination fails: two-site v*(R+S)v=-2, four-site v*(R tensor R-S tensor S)v=-40. This blocks the arbitrary-reference sufficient-certificate promotion only; the valid product-reference proof remains.'),
 ('N306','N304','The negative exact certificate occurs for CP qubit reduction tensor powers, whose actual rank-two positivity holds. It is not a Werner distillability witness or NPT bound-entangled state.'),
 ('N306','N224','A separate exact arbitrary-reference co-Choi tensor certificate fails in a CP qubit model. This is a contextual tensor-transfer obstruction, not a proof dependency or correction to the distinct factorial-spin/cross-copy statement in N224.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AV_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(304,308):
    ROWS[cid('N'+str(n))]['status_authority']='AV exact9Oct2026 investigation, source manifest and rational audit receipt. Target explicitly unresolved; restricted proof and exact method-counterexample source-reported. No independent intake proof reconstruction, scientific replay, formal or external correctness/priority certification.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full authored investigation, exact Fraction verifier/receipt, separate SymPy derivation and exploratory NumPy scripts/arrays supplied. Third-party primary papers/repository checkouts and the October716-term rational certificate absent. N304 locates reduction/elementary arguments, not a proof of its all-copy open obligation; N307 is a provenance/limitations record.'
ROWS[cid('N304')]['requires_external_validation'].append({'target':'external:AV_Werner_finite_copy_sources','scope':'Verify the inherited rank-two criterion and precise July2-copy hypotheses. October pinned anonymous written3-copy candidate was read by the source but its full rational matrices and716 positive multipliers were not replayed or supplied. Neither finite-copy assertion yields all-copy undistillability.','evidence':[card_ev('N304'),card_ev('N307')]})

# AW checkpoint02: scoped structured theorems and proof-route obstructions.
for owner,target,scope in [
 ('N308','N93','One common sharpC2 comparator is internally proved on full defining-O(d)-covariant channel algebras and their finite products/closures. This structured class does not settle arbitrary channels or acquire their factorization.'),
 ('N309','N93','Products of arbitrary unital self-compatible qubit channels now admit sharpC2 even without local HS symmetry or normality; full global Hermitian domain. Arbitrary global nonfactorable channels remain outside the theorem.'),
 ('N308','N143','Full orthogonal-covariant and tensor families supply structured constant2 positive results; the dimension-independent arbitrary-channel/frame gate remains unresolved.'),
 ('N309','N143','Nonselfadjoint unital qubit products supply full-domain constant2. Local Clifford/vector-spin1 products cover only their stated tensor spans, and representations/broadcasters remain supplied.'),
 ('N309','N277','The later signed-star/SVD/two-GLOBAL-ensemble construction removes local self-adjointness for supplied Clifford and spin1 spans, including arbitrary full qubit products. Exact naive local-mixture tensoring fails by1/40; the new polar repair is essential.'),
 ('N308','N278','Actual real/circular O(d) pure ensembles give full-domain absolute-spectrum majorants on this class. They do not make general spectral positive-part rounding a physical channel.'),
 ('N318','N278','An exact C5 frame defeats every scalar allocation of an optimal L+G envelope, but a more flexible local-dual gluing certificate provesC2 for the same frame. This is a failed proof ansatz, not a legal C2 counterexample.'),
 ('N318','N93','General scalar-envelope allocation fails exactly while the same frame has a valid local-dual repair. No universal finiteC or divergent legal target ratio was established.'),
 ('N309','N312','The newer theorem removes the earlier local HS-selfadjointness restriction using left/right singular proxies and a half-mixture of two entire product ensembles. The earlier positive-contraction tensor/sandwich lemma remains valid.'),
 ('N311','N310','The five quadrupole directions are covered for the defining-SO3-covariant qutrit family with explicit18/21-atom designs; arbitrary qutrit channels still have only the vector-spin span guarantee.'),
 ('N319','N310','The spin1 fraction3/5 cannot be transferred to all spins; alpha_j=(2j+1)/(4j+1) is necessary near isotropy. This does not invalidate spin1 or prove global all-weight positivity at the revised fraction.'),
 ('N320','N291','Checkpoint02 current STATUS/native21-claim ledger and scoped final audits add structured broadcasting advances while preserving all checkpoint01 claims and frozen proofs. Some earlier pending-review prefaces are historical; later PASS does not establish external correctness or novelty.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AW_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(308,322):
    ROWS[cid('N'+str(n))]['status_authority']='AW checkpoint02 current STATUS and native21-claim ledger, with the identified scoped final blind/exposed or root reviews. Full authored frozen proofs and historicalcheckpoint01 preserved. Some proof prefaces awaiting review are earlier versions. Internal mathematical/arithmetic checks SOURCE-REPORTED; no intake scientific replay, independent proof reconstruction, formal or external correctness/priority certification.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full authored proofs, scoped audits, scripts and selected primary PDF/HTML/Lean captures supplied; full repositories/caches/session transcripts excluded. Supporting premise reconstruction, efficient acquisition and finite-bit implementations are not supplied by a source locator. N319 has root scope review but no separate full blind all-j reconstruction; N320 is provenance, and N321 includes an explicitly open universal obligation.'
for owner,target,scope in [('N309','N310','requires signed all-weight spin1 star certificate when a spin1 local factor is used'),('N309','N312','requires positive-contraction tensor Bernoulli lemma'),('N311','N310','originator uses spin1 cap and sharpness; independent18-atom proof retained separately'),('N318','N310','requires explicit spin1 positive block certificate for the corrected C5 gluing example')]:
    ROWS[cid(owner)]['depends_on'].append({'target':cid(target),'scope':scope,'relation_status':'declared_source_dependency_not_independently_reconstructed_at_intake','evidence':[card_ev(owner)]})

# AX second record and independent Hamiltonian fixed-locus proof.
for owner,target,scope in [
 ('N322','N298','The later local bridge encodes fixed finite-support FS24 dynamic-function ASMs plus standard BGS Card by sparse current graphs and full eager-step footprints. It extends the fixed-HF-term interface to this precise model, with no elapsed-runtime factor; no full target-syntax generator was executed.'),
 ('N323','N302','The new model-relative conditional transfer covers the exact Card-ASM peak-space contract. Original grids already supply qualitative noncapture under the earlier base/HF imports; the exponential scale additionally needs the coefficient-uniform expander premise. It is not P versus PSPACE or every logical enrichment.'),
 ('N323','N285','Qualitative conditional Card-ASM noncapture uses original grids and does not need the expander/KOW premise; the stronger exponential peak lower bound does. Neither scale newly verifies family243 or every source dependency.'),
 ('N323','N287','The lower bound is for the precise Card-only model; one prescribed F3-solvability primitive can decide the hard query after the stated logical preprocessing. A complete machine-level syntactic compiler of that preprocessing is not supplied.'),
 ('N326','N324','The candidate degree-only 2d exponent does not establish general exponent2. Matched-embedding 2d/r is a proposed supplementary extension, not a fully reconstructed theorem; r<=2 and the explicit Pell counterexample limit the norm shortcut.'),
 ('N328','N206','Fixed-dimensional quadratic symplectic integer-fixed-point hardness follows a classical universal-Diophantine gate/multiplier construction. This distinct Hamiltonian representation does not implement the earlier chemical kinetic compiler or close its energy/sampling obligations.'),
 ('N329','N265','The all-ring Hamiltonian fixed-locus retract and rational-point equivalence are unconditional representations; rational undecidability still depends on the separate unverified H10(Q) claim. The special universal family N328 always has a supplied rational point and cannot serve as that rational-hard family.'),
 ('N327','N291','The second record supplies later counting/logarithm outcomes and final audit authority while retaining the first record unchanged. Original blind-draft hashes differ from edited release hashes; source report of unchanged older repositories/ZIPs is not a new intake verification of those originals.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AX_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(322,330):
    ROWS[cid('N'+str(n))]['status_authority']='AX supplied second-record README and final blind-reconstruction/comparison verdicts, with original versus released proof hashes distinguished; independent pasted Hamiltonian proof has source-reported status only. Moving-center interpolation is reported internally reconstructed with no identified gap, not an unproved imported input. No new intake scientific execution or proof reconstruction, formal or external correctness/priority certification.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full authored counting/logarithm proofs, two independent reconstructions, final verdicts, three diagnostic scripts and prior results supplied. Full external primary-paper bytes, a generated full ASM/solvability-preprocessing compiler and executed general interpolation generator absent. The separate Hamiltonian proof is complete as text but has no packaged executable checker or instantiated universal polynomial/circuit. N327 is provenance; source reported finite checks are not general proof certification.'

# AY five independent full-text attachments: stated arguments, not new certification.
for owner,target,scope in [
 ('N330','N93','A supplied complete tree/covariance/regression proof claims C4 on arbitrary observables for finite-d unital CPTP HS-selfadjoint self-compatible channels. This does not validate the broader bounded-Holevo/nontracial reductions or acquire a channel/broadcaster/efficient measurement.'),
 ('N330','N143','The finite-universal-constant reversible gate has a supplied complete C4 argument using one physical full-space comparator. Sharp C2 remains unresolved; no external correctness, formal certification or priority clearance occurred.'),
 ('N330','N278','A separately constructed canonical EB comparator dominates the HS spectral positive part using broadcast trees and full-space regression. This bypasses, and does not invalidate, the earlier failed direct spectral-positive-part channel lift or scalar-dual ansatz.'),
 ('N330','N321','The later source claims a complete finite C4 construction for the exact HS-selfadjoint general contract. Do not keep that internal target labelled as having no argument. Sharp C2 and general nonselfadjoint extension remain open, with the supplied proof externally unverified.'),
 ('N331','N308','General reversible C4 and the universal lower bound C>=2 leave a sharpness interval; earlier structured full O(d) C2 remains stronger on its own class.'),
 ('N331','N309','The new C4 theorem requires global HS-selfadjointness and does not subsume the earlier nonnormal qubit-product C2 result or settle arbitrary nonnormal channels.'),
 ('N335','N265','The parameter-free U^3(1+f^2)=1 detector has exactly one rational lift and polynomial-time explicit construction at degree2d+3. The older three-lift degree max(3,2d) result remains valid; this is a different tradeoff.'),
 ('N335','N266','Fixed cubic cover removes smoothing-parameter search at higher degree, while retaining exact rational-point bijection. No bounded-degree projective hypersurface reduction follows.'),
 ('N338','N265','The z^3+z detector and its discriminant-localized S3 cover give one rational lift, a Euclidean real locus and a quadratic-CI compiler; the older detector is not invalidated.'),
 ('N338','N266','Acquired positive m in z^3+z=m^2 f^2 preserves the earlier single-hypersurface degree and terminates by critical-value avoidance, now with one rational lift. Its Groebner runtime and bit bounds remain unbounded by the supplied proof.'),
 ('N336','N267','Conditional H10(Q) transfers to degree11 affine hypersurfaces and, by existing Poonen machinery, smooth projective varieties. Neither establishes a bounded-degree smooth projective hypersurface reduction or fixes naive infinity points.'),
 ('N340','N206','The new legal fixed mass-action family encodes stochastic lifetime decisions despite one unchanged stable ODE and supplied Lyapunov certificate. This does not realize the older integer/rational equilibrium-preserving SOS kinetic compiler.'),
 ('N341','N227','The summarized two-species seven-reaction order4 lifetime example is not supplied as a full listing/proof and has no endotactic promise. It does not close the two-species strongly-endotactic order4 gate.'),
 ('N339','N209','The new harmonic-observable threshold includes critical equality and physical lifetime in an autonomous recurrent environment. The older catalytic-clock theorem retains its separate network/rate contract.'),
 ('N338','N335','Both give exact one-lift rational detectors with different elliptic curves: fixed mu3 cover at higher hypersurface degree versus S3 monotone cover plus localized quadratic CI or acquired lower-degree hypersurface. Neither construction uniformly supersedes all interfaces.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AY_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(330,342):
    ROWS[cid('N'+str(n))]['status_authority']='AY exact five supplied text reports/manuscript state complete arguments with source-reported finite checks. No independent audit receipts or executable/check-output packages supplied. New record is source-derived unreviewed; intake reads/curates arguments without scientific replay, independent proof reconstruction, compilation, formal/external correctness or priority certification.'
    ROWS[cid('N'+str(n))]['proof_availability']['unavailable_or_unclassified']='Full displayed proofs/derivations are present; completeness not audited. Sandbox-linked archives, scientific scripts/exact receipts, primary fulltexts, full r-output/covariance/trace-reconstruction supplements and the seven-reaction listing are absent. Universal DPRM reaction instance is not expanded. N331 has full two-output trace/cloner arguments but only displayed multioutput recursion/conclusion; N341 is provenance and explicitly summary-only small-example evidence.'
ROWS[cid('N330')]['requires_external_validation'].append({'target':'external:AY-broadcast-tree-full-space-argument','scope':'Independently reconstruct the full covariance recursion, negative-eigenvalue congruence, full-space regression and one physical finite compact-limit comparator under exact global HS-selfadjointness. Do not treat the source finite tests or new locator as certification.','evidence':[card_ev('N330')]})
ROWS[cid('N336')]['requires_external_validation'].append({'target':'external:OpenAI-family004-H10Q-pinned-fd4aeeb2','scope':'Only rational undecidability/Turing-degree corollaries import the unverified family004 proof. Integer quintic DPRM reduction and rational smoothing compilers are logically separate. Turing-hardness is not a many-one halting reduction.','evidence':[card_ev('N336')]})
ROWS[cid('N338')]['requires_external_validation'].append({'target':'external:OpenAI-family004-H10Q-pinned-fd4aeeb2','scope':'Only a claim of rational undecidability imports family004; unconditional decision/topological compilers do not resolve H10(Q) or Mazur.','evidence':[card_ev('N338')]})

# AZ preserves original08 endpoint and linked09 later closure as separate scopes.
for owner,target,scope in [
 ('N342','N93','Complete finite KMS physical entropy/root-energy endpoint is now source-reported internally proved at pi, including arbitrary finite references. This removes that specified nonlinear prerequisite, not broader bounded-Holevo or varying-margin radius interfaces.'),
 ('N348','N93','Later09 supplies one raw-broadcaster/sigma-selected canonical channel with e^3<=240(2+sqrt2)I sqrt(b)/pi for ALL finite-reference common-margin states, optimized squared exponent1/3. Varying-margin/observational-radius conversion, common orthogonal basis and original-output agreement remain open; no whole historical claim invalidation.'),
 ('N344','N143','Sharp pi complete entropy plus weighted canonical C4/trace bounds give the same physical comparator a genuine-D cubic disturbance theorem on the exact KMS stationary compatible contract.'),
 ('N348','N143','Non-KMS forward pi/2 plus a legal Petz ENERGY bypass extends genuine-D cubic disturbance to stationary compatible channels and raw common-margin MI families. It does not establish sharp C2 or arbitrary observable-frame factor-two.'),
 ('N345','N342','At08 fullLp remained open; linked09 internally closes all finite positive KMS p>1 with sharp sine profile plus explicitly defined signed/polar extensions. Endpoint and universal pi sharpness remain valid. Non-KMS signed/polar/infinite extensions are not included.'),
 ('N348','N344','Later09 raw common-margin result removes stationarity/KMS hypotheses on the ORIGINAL broadcaster using repair/energy comparison. The stronger KMS cubic b coefficient and smaller constant on its exact class remain retained; no uniform supersession across interfaces.'),
 ('N348','N349','Petz TRACE-residual transfer on arbitrary bounded-I mixed references remains unresolved with sharp >1/2 obstruction. The new raw proof uses Petz ENERGY only, so this gate no longer blocks the common-margin theorem.'),
 ('N348','N61','Bounded-I exact common-margin raw preservation now has one simultaneous canonical reconstruction bound. The earlier complexity/unbounded-information copy ladder is not invalidated or an automatic counterexample to the new restricted theorem.'),
 ('N344','N330','New packet supplies weighted nontracial complete trace/entropy composition and internal audit authority; the historical AY tracial C4 source remains unchanged. Sharp C2/arbitrary-frame nonnormal extension is still separate.'),
 ('N348','N321','The raw common-margin state/reference theorem now has a supplied internally closed ENERGY-based argument. Historical general observable-frame C2 and varying-margin budget gates are not thereby closed.')]:
    ROWS[cid(target)]['material_updates'].append({'target':cid(owner),'source_card':cid(owner),'relation':'refines_with_scoped_AZ_result_or_limit','relation_status':'source_supported_scoped_notice_not_correctness_promotion','scope':scope,'evidence':[card_ev(owner)],'whole_claim_invalidated':False})
for n in range(342,353):
    r=ROWS[cid('N'+str(n))]
    r['status_authority']='AZ exact authored checkpoint09 STATUS and final cycle08/09 dependency closures, with named blind/exposed audit receipts, govern only their stated claims. User summary describes earlier08 endpoint; later09 closure is separate. Internal analytic proof/audit is source-reported; no intake scientific replay, independent proof reconstruction, formal/external correctness, priority or research-capability promotion.'
    r['proof_availability']['unavailable_or_unclassified']='Full authored proofs, scoped audits, code, finite receipts and selected primary captures supplied. Complete research repositories, environments/caches and session transcripts excluded by archive. Efficient acquisition, bounded conditioning/finite-bit implementation, infinite-dimensional dynamics, varying-margin observational-radius transfer and external/formal validation absent. N352 is provenance, not an additional theorem proof.'
ROWS[cid('N347')]['scoped_source_errata']=[{'target_path':'updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-upper/INDEPENDENT_OBSTRUCTION.txt','target_sha256':'afb137e346367d02c4e5d65d353d8c081ec8f4f60f9586dd6406aa936776232e','scope':'Section1 physical Hamiltonian prose requires (C-C*)/(4i), not /(2i). Exact positive C generator formula and executable evidence used correct normalization. Only prose factor is corrected; do not invalidate the physical theorem wholesale.','evidence':[evidence('updates/AZ/package/research/outputs/stationary-regularity-and-raw-classicality/nonkms-upper/ERRATUM_PHYSICAL_HAMILTONIAN.txt')]}]

# The focused branch correction supersedes the earlier unsupported impossibility gloss.
# It neither refutes BLR's printed claim nor certifies the original hyperbolic candidate.
state_ev = [evidence('state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md', 94, 110),
            evidence('state/2026-10-08-formanek-frontier/RESEARCH_STATE.md', 1, 2)]
for short in ('N47', 'N129'):
    relation('N165', 'supersedes', short,
        'Focused source-reported audit withdraws the earlier all-characteristics Formanek/Burger-Valette impossibility gloss as unsupported by cited originals. Formanek uses characteristic zero; Burger-Valette characteristic-p lemma constrains trace only; BLR prints a stronger claim whose proof scope needs specialist resolution. The original hyperbolic group-ring route remains conditional and unreviewed; neither candidate validity nor impossibility is established, and separate nonsofic constructions are not adjudicated.',
        state_ev, component='earlier frontier/state all-characteristics impossibility gloss; original candidate not refuted')
for short in ('N169','N170'):
    relation('N166', 'supersedes', short,
        'Corrected Seward Corollary 7.7 removes the historical source-branch infinite-only-positive-entropy caveat: h_sup=0 excludes every positive free ergodic Rokhlin entropy including infinite. Core algebraic/coding/tail deductions are retained; original G entropy and measurable conjugacy remain unresolved.',
        [evidence('state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md',65,81)],
        component='historical infinite-only entropy caveat; core deduction retained')

# Automatic proof-dependency propagation is deliberately absent. Every existing
# blocker is only a contrasting retrieval route; outdated clauses can coexist with
# higher-precedence scoped notices above and must not override them.
BLOCKERS = json.loads((ROOT / 'indexes/blockers.json').read_text())['blockers']
for blocker in BLOCKERS:
    ev = []
    for pointer in blocker.get('source_pointers', []):
        ev.append(evidence(pointer['evidence_path'], scope='whole blocker-cited source; blocker interpretation is metadata'))
    for affected in blocker.get('affected_cards', []):
        key = cid(affected)
        if key in ROWS:
            ROWS[key]['contrasting_blockers'].append({'blocker_id': blocker['id'],
                'scope': blocker['limitation'], 'required_cards': [cid(x) for x in blocker.get('required_cards', [])],
                'status': blocker['status'], 'evidence': ev,
                'precedence': 'Read material_updates first; historical blocker clauses are not automatically current.'})

GATES = []
def gate(number, code, title, cards, question, pass_condition, rationale, ev):
    GATES.append({'schema_version': 1, 'gate_id': code, 'priority_order': number,
        'title': title, 'status': 'open', 'gate_kind': 'finite_decision_or_explicit_proof_obligation',
        'card_ids': [cid(x) for x in cards], 'question': question,
        'pass_condition': pass_condition, 'priority_rationale': rationale,
        'evidence': ev, 'completion_evidence': [],
        'validation_boundary': 'No gate is closed by indexing, agreement, finite diagnostics, or a newer timestamp; this is a routing decision, not predicted breakthrough value.'})

gate(1, 'G-THERMAL-PROOF-AVAILABILITY', 'Acquire and audit the newer sharp thermal proof', ['N132','N136','N137','N141'],
    'Can the sharp coefficient and actual singleton-separability sufficient time be checked from full theorem/proof artifacts?',
    'Obtain immutable full proof/certificates; map the stated model, regularization and time normalization to each claimed step; independently reconstruct the load-bearing bound or record a specific failure. Acquisition alone closes only availability, not correctness.',
    'The newer summary materially changes two old frontier gaps, but its linked full packet is unavailable. Resolve the evidence boundary before using it as a premise.',
    [evidence('updates/AC/package/SOURCE_AVAILABILITY.json',1,5),card_ev('N136',5,7),card_ev('N137',5,8)])
gate(2, 'G-GROUP-RING-PREMISE-FAILURE', 'Resolve the positive-characteristic source discrepancy and candidate geometry', ['N47','N129','N65','N165','N279'],
    'Is there a valid positive-characteristic torsion-free hyperbolic idempotent theorem, or an identified candidate geometric/witness failure independent of the disputed attribution?',
    'Obtain a primary statement and proof with exact characteristic and group hypotheses, specialist review or erratum; separately attack the uniform graph, disk/Dehn, torsion-free and witness preservation interfaces. Neither the printed-citation mismatch nor characteristic-zero/trace-only results imply a positive-characteristic impossibility.',
    'The corrected branch audit withdraws the earlier unsupported no-go gloss. Preserve conditional candidates and concrete proof obligations without certifying either side.',state_ev)
gate(3, 'G-PERMANENCE-GLOBAL-COMPOSITION', 'Close global permanence geometry and viability', ['N33','N142','N145','N173'],
    'Can conditional one-scale entry be composed into the original measurable-rate class-common absorber theorem?',
    'Construct the usable scale/class representative; prove positive-box or plateau viability from the vector field rather than assume it; establish measurable-rate existence/continuation; compose global class-common absorption with all source interfaces and costs explicit.',
    'The older conditional composition gate persists. N173 supplies a full source-conditioned global proof for its strict uniform log-order/inwardness contract; it is not an unconditional solution for every older kinetic class. Audit its inherited affine lemma and exact regularity/viability steps separately.',
    [evidence('updates/AD/package/checkpoint/evidence/c12_permanence_compose/REPORT.md',26,45),evidence('updates/AD/package/checkpoint/ACTIVE_GATES.json',7,17)])
gate(4, 'G-QUTRIT-ULTRAFINE-AND-COST', 'Resolve an admitted qutrit extension or total-cost bound', ['N148','N149'],
    'What changes at zeta=1/ultrafine precision, vanishing splitting, general collisions, or charged total/classical memory?',
    'Freeze one extension and exact information contract; establish matching lower/upper bounds or a legal counterexample without deleting input tails. For a cost claim, charge classical labels, acquisition, output and implementation and compare an equally informed baseline.',
    'The fixed positive splitting/fixed zeta<1 branch law is source-internally closed; these are the explicitly named uncovered interfaces, not a repeat of the old proof.',
    [evidence('updates/AE/package/research/RESTART.txt',11,21),card_ev('N148',5,7)])
gate(5, 'G-THERMAL-SQRT-WINDOW', 'Close the critical-bath distance and finite-N error gates', ['N131','N138','N179','N180'],
    'For nu_N/sqrt(N)->fixed c>0, can the explicit upper/lower bounds become an exact full-SEP law or certified finite-N guarantee?',
    'Independently validate the whole-state tracial-L2 lift and uniform heterogeneous-product heat supremum; derive useful finite-N stationary trace-distance rates/onset, or matching limiting distance/phase-boundary bounds. Charge endpoint truncation, random proposals, precision, calibration and physical measurement. The witness rootc_w is not a separability threshold.',
    'AI supplies full authored critical-window upper and lower proofs, including about5.82e-5 asymptotic upper integral atc1; exact d(c), intrinsic boundary and finite-N convergence rates remain open. This does not acquire the absent AC entropy-coefficient proof.',
    [evidence('updates/AI/package/work/agents/thermal_window/REPORT.txt',84,222),evidence('updates/AI/package/work/agents/thermal_window/COST_ADDENDUM.txt',1,None),evidence('updates/AI/package/work/agents/thermal_blind/REPORT.txt',1,145)])
gate(6, 'G-XXZ-TRICRITICAL-NUMBER', 'Prove a tricritical Gibbs number law', ['N150','N151','N159'],
    'Can partition lower bounds become uniform number-distribution statements at the tricritical scale?',
    'Control growing-sector canonical heat traces, excited multiplicities and all-sector tails; then derive the proposed sqrt(L)/L^(2/3) number laws or cubic density, or give a source-legal counterexample. Keep both endpoint fields and exact moving-threshold contracts.',
    'The restart explicitly distinguishes partition witnesses from unknown number laws and records the moving-below-threshold failure of uniform extension.',
    [evidence('updates/AE/package/research/RESTART.txt',22,36),card_ev('N159',5,5)])
gate(7,'G-COMMON-EB-ARBITRARY-RANK','Validate the general reversible C4 argument and decide sharp C2',['N93','N143','N144','N277','N278','N308','N309','N310','N318','N319','N321','N330','N331','N332','N342','N344','N348'],
    'Does the supplied broadcast-tree argument establish full-space C4 on the exact reversible contract, and can sharp C2 or an arbitrary nonselfadjoint extension be established?',
    'First independently reconstruct one finite canonical physical POVM/EB comparator dominating (2Phi^2-I)_+ for every finite-d unital CPTP HS-selfadjoint self-compatible Phi: full covariance identity, congruence with mixed-sign eigenvalues, original-space compactness and regression for arbitrary slow/fast mixtures. Then prove C2 or give a legal broadcaster/channel plus unrestricted ensemble-support counterexample; a failed scalar allocation or nontracial witness is insufficient. Treat arbitrary nonselfadjoint channels as a separate extension, and acquire any claimed measurement/precision/dense-output algorithm. AZ now supplies complete weighted genuine-D cubic comparison and raw common-margin MI reconstruction via Petz energy; validate those exact state interfaces separately from arbitrary-frame C2. Varying-margin observational-radius/bounded-Holevo conversion, revised all-spin/all-weight inequalities and external priority still require separate proofs.',
    'AY supplies a complete C4 argument and a cloner lower bound C>=2, so finite universal C on the reversible contract is no longer an identified no-argument internal gate. AZ internally closes specific nontracial entropy and raw common-margin STATE reconstruction interfaces; it does not close arbitrary nonselfadjoint observable-FRAME C2 or optimized varying-margin radius. External correctness remains unverified; sharp C2 and these broader interfaces remain open. Earlier structured C2 theorems and exact failed spectral/scalar ansatz counterexamples remain valid.',[card_ev('N330'),card_ev('N331'),card_ev('N332'),card_ev('N308'),card_ev('N309'),card_ev('N318')])

gate(8, 'G-CONDITIONAL-SAMPLER-COMPILER', 'Implement and audit the admitted conditional sampler interface', ['N95','N109','N110','N111','N113'],
    'Can all counting, support/range and bit-operation oracles be acquired for the exact admitted spin/fermion class?',
    'Independently check the site-dependent gap and local cone premises; implement an end-to-end acquired oracle/counting/compiler pipeline; account for tensor-incidence variable count, precision, initialization, herald and preparation costs; compare equally informed existing samplers.',
    'The current source review reports no end-to-end FPRAS/compiler execution and exposes astronomical sufficient schedules; finite Hamiltonian checks do not settle this operational gate.',
    [evidence('state/2026-10-08-formanek-frontier/RESEARCH_STATE.md',24,34),card_ev('N109',5,7)])
gate(9, 'G-EXTERNAL-PRIORITY-REVIEW', 'Obtain independent exact-contract correctness and priority review', ['N62','N117','N136','N148','N150'],
    'Which surviving candidates withstand independent source-level criticism and precise prior-art comparison?',
    'Record reviewer/checker identity, immutable claim/proof version, exact scope, concrete findings and unresolved premises. A novelty claim also needs a specific primary-source comparison; no aggregate internal-agent count or integrity receipt substitutes for it.',
    'All current scientific leads retain unverified external correctness/priority; this gate is universal and does not rank fields by expected breakthrough.',
    [evidence('updates/AE/package/research/RESTART.txt',65,67),card_ev('N141',5,7)])

gate(10, 'G-UNITAL-NOISE-BOUNDED-SCORES', 'Make the three-axis unital-noise separation quantitatively executable', ['N160','N161','N163','N164'],
    'Can the existence proof produce certified bounded three-axis scores, useful finite-N error/onset and channel-gap-dependent sample costs without postselection?',
    'Emit an immutable bounded-score table/construction, certified separable bound and target finite-N margin in the admitted fixed-channel/bath model; charge precision, calibration, samples and preparation. Track dependence on tr(TT^T)-1 and distinguish fixed channels from boundary-approaching sequences.',
    'Full AF proof/code available; source-reported diagnostics do not emit bounded scores or a useful finite-N threshold. The independent filter has exp[-t sqrt(N)/2+O(1)] herald cost and does not give unfiltered distance by itself.',
    [evidence('updates/AF/package/THEOREM_AND_PROOF.md',317,324),evidence('updates/AF/package/THEOREM_AND_PROOF.md',405,423),evidence('updates/AF/package/RESEARCH_STATE.md',73,81)])

gate(11, 'G-ORIGINAL-FAMILY197-ENTROPY', 'Decide original family-197 entropy before Bernoulli classification', ['N166','N167','N168','N169','N170','N253','N254','N257'],
    'Can the original family-197 group be proved to have h_sup=0 or >0 under an independently checked witness?',
    'Acquire actual witness/group-word operations and a rank-density-to-zero sequence, or construct an actual arbitrarily-small-entropy generating measurable partition, or a nonsofic-applicable positive entropy lower bound. State the separate measurable conjugacy/invariant gate. Product G times Thompson V does not answer original G.',
    'Branches add concrete support, coding, finite-model and infinite-tail obstructions but do not decide original entropy. Corrected Corollary 7.7 removes the spurious infinite-only loophole; equality of all Bernoulli entropy still does not imply isomorphism.',
    [evidence('state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md',39,81),evidence('state/2026-10-08-family197-infinite-tail/RESEARCH.md',84,94)])

gate(12, 'G-SINGLE-METRIC-GEOMETRY-REVIEW', 'Specialist review of the one-manifold harmonic limsup candidate', ['N175','N176','N177','N178'],
    'Does the complete spectral/PDE/countable-transfer proof survive external exact-contract reconstruction?',
    'Record a specialist or formal reconstruction at immutable PROOF_v3+POST_SOURCE_STATUS versions: all adjacent spectral inputs, pre-gauge controls, compact-family freezing, whole-local-matrix repair, stage-order quantifiers, birth-only fixed point, all-radius growth and independence. Perform focused primary-source priority comparison; any found gap gets a scoped dependency notice.',
    'This is the AI packet lead after separate internal source/transfer/uniformity/integration audits. No remaining internal obstruction was reported, but existence is nonquantitative and no external proof/priority clearance or metric materialization exists. This slot does not establish a cross-field value ranking.',
    [evidence('updates/AI/package/work/agents/common_metric_attack/POST_SOURCE_STATUS.txt',1,None),evidence('updates/AI/package/work/agents/common_metric_attack/PROOF_v3.txt',213,258)])
gate(13, 'G-EPR-GLOBAL-VARIANCE-ORACLE', 'Acquire a general EPR counting interface beyond positive per-draw determinants', ['N190','N191','N192','N193'],
    'Can an admitted general physical EPR circuit acquire polynomial relative variance or a valid global counting representation?',
    'Prove a scalable phase/decomposition/conditional estimator or two-measure selector lift with all support, positivity, equality-sewing, loop-parity and bit costs explicit. Implement acquired oracles and compare exact tractable families. Neither positive determinant expectation nor block-ordered cactus common bases yields a general FPRAS.',
    'The physical equality-sewing lift is explicit; specified raw/tuned gauges can have exponential relative second moments, identity gauges can have zero variance, and the cactus family is already exactly solvable. General sampling complexity remains open.',
    [evidence('updates/AI/package/work/agents/epr_parity/DETERMINANT_LIFT_FINAL.txt',1,None),evidence('updates/AI/package/work/agents/epr_matroid_gluing/REPORT.txt',136,151)])
gate(14, 'G-DETYPING-DOWNSTREAM-REPAIR', 'Audit repaired symmetric detyping through later compression stages', ['N183','N184','N242','L02'],
    'Does the precisely repaired predicate/parser and acquired wire gap compose with every later named use?',
    'Pin intended symmetric sampler and valid padded serialization, reproduce the exact counterexample and affine value identity, verify imported L02 and every subsequent soundness/sampler register. Charge t, seed, answer, repetition and evaluation costs. Obtain source-author/specialist review before broader conclusions.',
    'The scalar CHSH fixture contradicts scoped completeness; the repair and sigma>=1/4 are internally derived at the named stage. Final answer reduction and full167-page compression interfaces remain unreviewed; no MIPco=coRE refutation or global repair claimed.',
    [evidence('updates/AI/package/work/agents/repetition_application/COUNTEREXAMPLE.txt',1,47),evidence('updates/AI/package/work/agents/repetition_application/REPAIRED_DETYPING_GAP.txt',1,71)])

gate(15, 'G-FACTORIAL-NONUNITAL-RAW-GAP', 'Decide unfiltered nonunital distinguishability and cost', ['N195','N200','N201'],
    'For a fixed nonunital non-EA channel, does the engineered input retain a nonvanishing raw full-separability distance or a practical local test?',
    'Prove an admitted unfiltered distance/sample lower bound with useful finite-N onset and calibration costs, or a legal trace-distance counterexample. Charge state preparation/routing and filter success; Gaussian covariance matching alone is insufficient.',
    'Universal binary survival can rely on exp(-cN) output filtering; the exact GAD fixture defeats the simple covariance condition. It gives neither a nonvanishing unfiltered margin nor an efficient general experiment.',
    [evidence('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md',377,427)])
gate(16,'G-FACTORIAL-REGULARIZED-ENTROPY','Review the all-copy log order and decide its leading coefficient',['N197', 'N198', 'N199', 'N224', 'N288'],
    'Does the all-copy central log-spin-moment argument withstand reconstruction, and is the leading regularized coefficient 1/2,1 or another value?',
    'Independently reconstruct grouped-half Schur/coherent-information bounds allowing arbitrary within-original-laboratory copy correlations and the central separable domination upper. Close the[1/2,1] coefficient gap or identify a valid obstruction under the exact model; retain centrality and moment assumptions. External correctness/priority review is separate.',
    'N288 now internally claims Theta(logN) for every copy count under bounded log-spin moment, including factorial probes. This refines the old order question but does not establish exact coefficient or restore naive Casimir overlap multiplicativity refuted by N224.',[card_ev('N288'),card_ev('N224'),card_ev('N199')])

gate(17, 'G-DIOPHANTINE-KINETIC-COMPILER', 'Acquire an arithmetic-preserving positive mass-action realization', ['N206','N207'],
    'Can the SOS clock reduction be realized by an admitted reaction network while preserving the integer/rational equilibrium decision problem?',
    'Give an exact finite compiler with positivity, auxiliary-species, rational/integer projection and converse-lifting contracts, or prove a precise obstruction. The same-species kinetic example excludes weak reversibility; detailed-balanced global rational equilibria are decidable. Conditional H10(Q) is not a verified imported theorem here.',
    'The abstract convex-flow reduction does not implement chemistry or robust physical computation; adding a positive clock floor destroys the arithmetic stationary interface.',
    [evidence('updates/AK/package/state/2026-10-08-convex-gradient-diophantine/RESEARCH_STATE.md',105,None),evidence('updates/AK/package/state/2026-10-08-convex-gradient-diophantine/KINETIC_REALIZATION_GATE.md',22,43)])

gate(18, 'G-STEKLOV-UNIFORM-COLLAR-REVIEW', 'Review polar capacity, published-method attribution and matching geometry', ['N210','N211','N240','N262','N263','N175'],
    'Does the broader published energy-Gram route give the stated3D upper, and do inherited matching metrics meet the compact positive polar-link class?',
    'Independently reconstruct uniform quadratic-form and outer-norm comparison, precompact-family Weyl control, boundary measure evolution, trace independence and determinant integration at fixed immutable versions. Verify N175 separately before matching sharpness; compare precise earlier dimension bounds. No no-foliation extension is implied.',
    'N240 attributes a broader3D energy-Gram upper to Li-Wang machinery and removes slow variation. Old higher-dimensional/collar statements retained; exact primary source and countable matching still require independent specialist review, not finite capacity algebra.',
    [evidence('updates/AL/package/state/2026-10-08-steklov-capacity/RESEARCH.md',33,110),evidence('updates/AL/package/state/2026-10-08-steklov-capacity/RESEARCH.md',127,137)])

gate(19,'G-PPT-SMALL-DIMENSION-DSP','Obtain a globally certified small-dimensional PPT rank obstruction',['N213','N214','N217','N220'],
    'Does an explicit d=4 PPT state lie outside DSP_2 with a proof valid for every complex Schmidt-rank-two vector?',
    'Provide an exact state and valid two-sided witness with universal complex rank-two block positivity, or a complete contrary certificate. Random vector sampling, real-only fixtures and the failed Breuer-Hall copositivity ansatz are insufficient.',
    'Linear-order asymptotics begin at astronomical dimensions; the useful small-dimensional case is not settled by either ensemble.',
    [evidence('updates/AM/package/PROOF.md',7,63),card_ev('N217'),card_ev('N220')])
gate(20,'G-POSITIVE-MAP-FINITE-REFERENCE-REVIEW','Review the finite-reference EB definition and separable compression proof',['N219','N221','N222','N226'],
    'Does the precise non-CP finite-reference theorem answer the cited published problem under its original complex definition?',
    'Independently reconstruct the complex bilinear net, noncommuting-block separable ball, conjugated-isometry Choi compression, all-positive-input extension, adjoint symmetry and robust diamond witness. Check the immutable original problem and priority; charge dimension/rational bit construction. Specialist validation is separate from internal diagnostics.',
    'For every finite r there is a map, not one fixed all-reference map. Positive non-CP maps are not physical channels; the dimension threshold is d>=2^23 r^3.',
    [evidence('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md',9,48),evidence('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md',146,202),evidence('updates/AN/package/proofs/GAUSSIAN_CONE_SEPARATION.md',292,394)])
gate(21,'G-PPT-COMPOSITION-SENSITIVE-WITNESS','Find a physical PPT composition witness beyond ruled-out candidates',['N213', 'N215', 'N220', 'N225', 'N276', 'N282', 'N283', 'N284', 'N290'],
    'Can an admitted physical PPT composition have a globally valid entanglement witness, or can a universal composition bound be proved?',
    'Construct a legal composed channel and a universal complex entanglement certificate or an exact-contract universal theorem. Original family272 cube and its specified Hodge-cancelled cube have rational EB certificates; source-dependent original index3 is distinct. Rotation-family rank/witness nulls and failed frozen decomposition do not classify six UNKNOWN samples. Keep Choi reshuffling norms and charged cost interfaces.',
    'Individual linear rank obstructions do not settle composition. N290 extends the Gaussian EB-square control to any two admitted norm events; EB admixture cannot prolong index. New exact cubes rule out specified counterexamples, not universal PPT cubed.',[card_ev('N276'),card_ev('N282'),card_ev('N283'),card_ev('N284'),card_ev('N290')])

gate(22,'G-FIXED-MAP-ALL-TENSOR-POWERS','Preserve a nontrivial fixed-map interface across every tensor power',['N219','N224','N225'],
    'Can a fixed non-CP/non-copositive map remain positive at all tensor powers in one fixed algebra?',
    'Supply a nontrivial fixed-dimensional map and all-power positivity proof, or a theorem obstructing the exact interface. Establish stabilized-norm compactness and uniform estimates before a limiting argument; for all finite r exists P_r is not exists P for all powers.',
    'The finite-reference maps change algebra with r, approach the depolarizer in a nonstabilized HS norm, and have a stabilized diamond obstruction. Two-producible inputs cannot witness beyond pair positivity.',
    [evidence('updates/AN/package/proofs/ITERATION_AND_LIMIT_BARRIERS.md',41,None),evidence('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md',43,48)])

gate(23,'G-ENDOTACTIC-TWO-SPECIES-ORDER-FOUR','Decide the two-species order-four explosion boundary',['N227','N228','N229'],
    'Is the minimum explosive source order4 or5 for fully endotactic stochastic mass action on two species?',
    'Give a legal all-direction endotactic order-four diagram and an all-state physical-clock explosion proof, or a universal two-species order-four nonexplosion theorem covering arbitrary finite products, positive rates, tangent faces and disabled factorial terms. Independently review the cubic exclusion and exact order-five equality. An order-four near-miss or total-direction-only cubic witness does not decide the question.',
    'The paused checkpoint narrows the exact named minimum to{4,5}; arbitrary species remains{3,4,5}. This is the source-recommended next mathematical decision, not authorization to resume.',
    [evidence('updates/AO/package/proofs/integration/two_species_cubic_composition_scope_v1.md',1,19),card_ev('N227'),card_ev('N229')])
gate(24,'G-COLLECTIVE-CONCENTRATION-INTERFACE','Validate or acquire the full concentration-to-local-information interface',['N230','N231','N232','N233','N234','N235','N236','N237'],
    'Can an admitted model acquire the all-direction uniform MGF and faithful-marginal promises, or rigorously extend the fixed-d theorem?',
    'Reconstruct complex Gram/support Parseval, Cauchy sphere contraction and exact centering; retain dimension/marginal floors and baselineN when variance grows. For an acquisition result charge measurements, error, computation and equally informed controls. For certification retain unrestricted ALLSEP null, independent preparations, gap floor and clipped calibration; finite variances or mean Casimir alone fail. External priority/correctness review remains separate.',
    'Quadratic Petz order is sharp even on separable mixtures. Only exact white-Schur polarized targets have the matched charged upper/lower; the general structural theorem is not a universal entanglement test.',
    [evidence('updates/AO/package/proofs/concentration_blind/CONCENTRATION_FROZEN_REPORT.txt',15,302),card_ev('N235'),card_ev('N236'),card_ev('N237')])
gate(25,'G-CRITICAL-GIBBS-LOCAL-REVIEW','Review the exact critical Gibbs local window and quantitative regimes',['N238','N239'],
    'Do the exact critical Gibbs tail and bounded measurement arguments establish every claimed local trace/KL regime, including r comparable toN?',
    'Independently reconstruct parity-aware finite Stirling/quartic envelopes, normalized radial moments, complex support expansion, bounded heat/cosine witnesses, exact hypergeometric large-window law and PI/SSA global-to-local entropy upper. Distinguish fresh window proof from separate stronger linear-KL audit; perform precise primary-source priority review. Gibbs preparation and model/temperature acquisition stay charged.',
    'The sharp r~sqrtN window is an exact-model candidate; a separable rare-sector mixture defeats replacing it with matching means/pairs or a chi-square lower. No ALLSEP entanglement conclusion.',
    [evidence('updates/AO/package/proofs/curie_weiss/CRITICAL_PROOF_FROZEN.md',5,280),evidence('updates/AO/package/proofs/critical_quantitative_audit/INDEPENDENT_PROOF.md',1,316)])

gate(26,'G-CIRCUIT-LOGARITHMIC-CONTACT','Decide circuit-size-sensitive logarithmic contact',['N246','N247','N248','N249','N250','N280','N289'],
    'Is there a uniform explicit polynomial contact bound B(n,s,D) for every nonzero admitted small commutative circuit, or a small-circuit counterfamily?',
    'Prove the size/degree/field/constant/evaluation contracts and a polynomial contact bound without expanding exponential derivative closure, or construct a uniform polynomial-size circuit family with superpolynomial contact. Four finite fixtures, large linear-state dimension or the prior small-derivative theorem do not settle this. Keep exact rational generator costs separate from black-box evaluation.',
    'The sufficient reduction is supplied, hypothesis unproved; direct nonlinear contact is not blocked by faithful linear-realization lower bounds. N280 supplies sharp binomial/product contact and exact rational pullback alphabet costs; N289 rules out rank-one-variable determinants for a finite maximal fixture. Neither closes the general circuit gate.',[card_ev('N250'),card_ev('N249')])
gate(27,'G-DEFECT-BERNOULLICITY-OR-COCYCLE','Decide a residual Bernoullicity or cocycle-stabilization bridge',['N251','N252','N253','N254','N255','N256','N257','N258','N268','N269','N270','N272','N273','N274','N275','N279','N165','N166'],
    'Can the explicit finite defect power be proved Bernoulli, or can a stabilized Bernoulli insertion preserve the original twisted extension cocycle?',
    'Validate the actual torsion-free algebraic witness and the coloring/right-inverse proof, then prove the independent generating-Bernoulli property of K-power/X-times-residual, or exhibit exact measurable displacement lift/cocycle identity with a legal residual automorphism. Finite XOR feasibility, almost-cocycle convergence, infinite weak Pinsker entropy, mutual factors and equal ordinary invariants do not imply conjugacy. Earlier two-defect relative-isomorphism application requires separate exact-source review. AR adds per-orbit scalar solutions, but an exact D-valued transfer needs all-character multiplicative coherence; integer-power sigma_k permits ThetaLambda=j−tau_k for a supplied X-output insertion. Pure nonsplitting and enriched Koopman equivalence are algebraic/spectral limits, not general measurable nonexistence.',
    'A finite-power exact direct-product candidate is preserved, but unequal-entropy Bernoulli conjugacy and original supremal Rokhlin entropy sign both remain unresolved. N279 repairs finite-field/torsion premises conditionally on a different enlarged group, not the original witness or residual Bernoullicity.',[card_ev('N252'),card_ev('N255'),card_ev('N256'),card_ev('N165')])
gate(28,'G-RANK-OR-MANIFOLD-TRANSFER','Acquire a bridge beyond rank and PL thickening obstructions',['N259','N260','N261','N65','N165'],
    'Is there an additional unitary-microstate obstruction or an alternative compact aspherical five-manifold realizing the required group?',
    'For approximation, supply structure beyond rectangular-word separation without an impossible characteristic-zero lift. For Singer, realize G-times-F2 in a compact aspherical five-manifold or supply a different above-middle homology mechanism, validating source geometry and the exact published reflection theorem. Canonical graph-product spines fail classical local link embeddings. Source rank obstructions and conditional hyperbolic five-manifold deduction are not these endpoints.',
    'Both routes need genuinely new mathematical input; do not treat an explicit obstruction, existing theorem application or repository integration as a historic discovery.',[card_ev('N259'),card_ev('N260'),card_ev('N261')])

gate(29,'G-PROJECTIVE-RATIONAL-POINT-PRESERVATION','Acquire a smooth projective hypersurface rational-point reduction',['N265','N266','N267','N335','N336','N337','N338'],
    'Can the effective affine one-lift smoothing/cover compilers be upgraded to smooth geometrically integral projective hypersurfaces while preserving rational solvability?',
    'Give an effective iff rational-existence construction controlling every infinity point and exceptional divisor with smoothness/integrality and charged arithmetic costs. Ordinary homogenization already fails; an affine finite etale cover or Euclidean real locus is not projective control. Existing Poonen reduction to arbitrary smooth projective varieties is prior art, not a new bounded-degree hypersurface theorem. Validate upstream family004 separately before any rational undecidability assertion.',
    'AY supplies two different exact one-lift affine compilers: parameter-free higher-degree mu3 cover and S3 monotone localized cover/quadratic CI or acquired lower-degree hypersurface. Integer quintic hardness is unconditional; rational undecidability remains upstream-conditional. No supplied construction resolves the bounded-degree projective hypersurface gate.',[card_ev('N265'),card_ev('N266'),card_ev('N267'),card_ev('N335'),card_ev('N336'),card_ev('N338')])

gate(30,'G-RANDOM-EQUIVARIANT-MODULE-BASIS','Construct or obstruct a globally equivariant random defect-module basis',['N268','N269','N270','N165','N166'],
    'Does Rp admit an iid-environment-measurable finite-support F2-vector-space basis indexed covariantly by G?',
    'Validate the supplied actual group-ring witness/Haar splitting, then construct measurable v_g with both finite-relation independence and full spanning a.s., and covariance v_hg(h omega)=h v_g(omega) on a common conull set; prove a measurable inverse. Alternatively give an obstruction to this precise conditionally linear class, without extrapolating to every nonlinear measurable conjugacy. Charge support tails, finite bits and computation if an effective algorithm is claimed. Iid thinning/global well-order and subgroup bases alone fail to supply the target.',
    'A new sufficient conditional mechanism bypasses finite-power residual cancellation, but no random basis, finite-power Bernoullicity or two-versus-four conjugacy is established.',[card_ev('N268'),card_ev('N269'),card_ev('N270'),card_ev('N165')])

gate(31,'G-INVARIANT-INTERPRETATION-RESOURCE-REVIEW','Review precise HF/Card-ASM transfers and imported lower-bound inputs',['N285','N286','N287','N298','N299','N300','N301','N302','N303','N322','N323'],
    'Do the precise fixed-term HF and finite-support Card-ASM peak-space bridges support their conditional qualitative and exponential native lower-bound transfers under independently valid imports?',
    'Independently validate the full eager-term footprint, sparse nonzero function graphs, frozen-state parallel updates including zero deletion and clash semantics, and ordinal cardinality guards. Reconstruct the resettable binary2D compiler, native saturation/GC and ordinary unary Hartig logical-sort contracts. Separately validate family243 group/base/HF homogeneity: qualitative original-grid noncapture needs no KOW; the exponential scale additionally needs collective cofilling coefficient-uniformity and expander/link premises. Verify all-input query semantics and any claimed machine-level F3-solvability preprocessing compiler. Charge fixed-program dimensions/arity/width, peak-over-run resources and acquisition; compare exact primary priority and seek external review.',
    'AU fixed-HF-term and AX exact finite-support Card-ASM simulation bridges are independently reconstructed internally in their sources. AX claims original-grid qualitative and additionally imported exponential Card-only noncapture; its local bridge is no longer an identified internal proof gap. Neither full syntax compiler nor imported general lower bounds receive intake scientific replay/certification. No PvsPSPACE, all logical enrichments or rank/solvability-augmented noncapture follows.',[card_ev('N285'),card_ev('N286'),card_ev('N298'),card_ev('N302'),card_ev('N322'),card_ev('N323')])

gate(32,'G-COUPLED-RADIAL-GAUSSIAN-SIMPLEX','Prove or falsify the stronger coupled radial comparison',['N292','N293','N294','N295','N296','N297'],
    'Does(L) hold for all measurable coupled radial profiles, including0/1 boundary profiles, and every0<rho<1?',
    'Give a uniform analytic comparison with exact pointwise sum1 and each Gaussian mass1/3, or a rigorously certified legal profile counterexample. A profile counterexample refutes the stronger relaxation, not automatically the real-partition conjecture. Independently acquire exact circular-Riesz and optimizer dimension-reduction theorem versions/interfaces before any full-conjecture implication. Near0/1 leading terms and finite3-shell numerics are insufficient; coefficientwise Hermite dominance and single-profile Jensen are false.',
    'The checkpoint supplies two restricted arguments and two failed-promotion counterexamples. The surviving radial inequality is unproved and could be false even if the original conjecture holds. No10/10 objective, external correctness or novelty clearance is established.',[card_ev('N292'),card_ev('N293'),card_ev('N294'),card_ev('N295'),card_ev('N296'),card_ev('N297')])

gate(33,'G-ALL-COPY-NPT-UNDISTILLABILITY','Resolve the all-copy NPT target beyond product-ray supports',['N304','N305','N306','N307'],
    'Does any finite-dimensional NPT state remain undistillable for every copy number; can the boundary qutrit candidate satisfy q_n(C)>=0 for all n and complex rank(C)<=2?',
    'For a positive answer give one positive trace-one genuinely NPT state and a rigorous universal all-copy rank-two positivity proof with exact bipartition, complex supports and all imported assumptions checked. For the boundary qutrit candidate prove the displayed q_n inequality without rank-preserving partial-trace or arbitrary-reference co-Choi shortcuts. A valid distillation witness rejects that candidate only; negating the existential target requires a theorem covering every finite-dimensional NPT state. Audit any finite3-copy716-term source certificate separately without promoting it to all n; obtain external correctness and focused priority review.',
    'Source reconstructs an arbitrary-site product-ray subclass and gives an exact sufficient-certificate counterexample in a CP qubit model. Neither resolves NPT bound entanglement; finite numerical minima, a three-copy source claim and tensor-closed PPT zero-key coherence do not supply the missing universal mechanism.',[card_ev('N304'),card_ev('N305'),card_ev('N306'),card_ev('N307')])

gate(34,'G-ALGEBRAIC-LOGARITHM-REVIEW','Externally review the internally reconstructed degree-only logarithm bound',['N324','N325','N326','N327'],
    'Does the complete moving-center interpolation plus entrywise norm/determinant argument establish the stated degree-only 2d irrationality exponent?',
    'Specialist reconstruction of center-independent separation versus center-dependent onset, weighted Bezout/logarithmic multiplicity, explicit nef-plus-ample blowup polarization, ordinary Rees/Serre pushdown, and the one-sided weighted-ideal containment. Verify exact algebraic-integral entries after row/column clearing, every conjugate norm factor d, determinant analytic collision bound and the ordered fixed-parameter then H limit. Distinguish rational approximants from number-field approximants, fixed alpha from effective uniform onset, and the already source-published rational case/interpolation theorem. Report any actual gap with immutable locator; no finite matrix rank or scalar schedule check certifies the theorem.',
    'Final independent source reconstruction reports no remaining substantive gap, including the moving-center interpolation step. This gate is external correctness and precise priority review, not a declaration that MI is still unproved internally. The impractical scalar stress schedule is not an executed full general generator; external/formal certification and novelty remain unestablished.',[card_ev('N324'),card_ev('N325'),card_ev('N327')])

gate(35,'G-LOGARITHM-GENERAL-EXPONENT-TWO','Find a valid route beyond the leading algebraic norm degree cost',['N324','N325','N326'],
    'Can the degree-only 2d bound be replaced by exponent2 for general nontrivial positive algebraic alpha without hiding conjugate, torsion or denominator costs?',
    'Prove the source determinant-specific suppression sum_other log|sigma Delta|<=-(d-1)(1-bbar)MH+o(MH) at unchanged clearing, geometric-volume and analytic cost, or a genuinely different valid construction. The Pell fixture refutes generic degree-free norm improvements. Matched-embedding supplementary2d/r requires its own complete proof; non-torsion ratios permit at most r=2 and distinct center fibres, while repeated torsion centres require new interpolation volume/separation. Preserve all branch, field, approximation and parameter-order quantifiers; validate the underlying 2d candidate separately.',
    'General exponent2 is open. Exact matched-embedding and Pell limits are internally derived in source, but supplementary2d/r is not a completed theorem. Constant tuning within the current architecture retains nu>2d; no claimed matched-embedding example resolves the unrestricted target.',[card_ev('N324'),card_ev('N325'),card_ev('N326')])

gate(36,'G-COARSE-CANONICAL-KERNEL-REVIEW','Review the canonical maximal coarse kernel and delimit group transfer',['N333'],
    'Does the supplied growing-divisibility plus maximal transfer/sliding argument inject bounded integer sequences into the stated canonical Rips-colimit assembly kernel?',
    'Specialist reconstruction of congruence lifts/cup-product divisibility, line-bundle binomial K-divisibility, coefficient-independent thresholds and Mayer-Vietoris endpoint pairing. Audit maximal multipliers, fixed-propagation norm control, constant-fibre lift multiplicative defects, unbounded orthogonal height stacks, compact quotient injection and canonical Paschke/index naturality on all product classes. Verify continuum lower/upper cardinality and reduced quotient transfer. A coefficient-free group consequence additionally needs an actual KX-injective index-natural map; Cayley graph containment is insufficient and low-H1/H2 nonzero pairing conflicts with zero group index. Compare exact prior art and get external validation; no borrowed family307 Lean certificate.',
    'Full supplied manuscript reconstructs the source graph and analytic/topological ingredients and adds bounded-sequence amplification/exact continuum rank. This remains internally source-reported, not a certified new coarse or group Novikov counterexample; no group transfer or formal dependency closure is supplied.',[card_ev('N333')])

gate(37,'G-FIXED-FLOW-STOCHASTIC-LIFETIME-REVIEW','Review lifetime undecidability under one fixed stable reaction flow',['N339','N340','N341','N206','N227'],
    'Does the exact positive-rate mass-action compiler preserve the harmonic explosion/recurrence threshold while every parameter has the same globally stable flow and stochastic drift?',
    'Independently prove stopped-Dynkin/Foster nonexplosion and positive recurrence including equality, frozen cubic birth-death uniform mean bounds and recurrent-exposure finite mean lifetime. Check nonnegative quadratic DPRM encoding, factorial expansion, bounded coefficient-rate positivity on the closed parameter interval, source/product order<=8, unchanged full drift and polynomial Lyapunov identity/degree<=12. Materialize any claimed runnable universal instance and obtain missing exact receipts/seven-reaction listing before operational assertions. Preserve exact arithmetic membership and charged witness/time costs; no endotactic promise or equilibrium-compiler closure follows. Get external correctness and focused priority review.',
    'Full pasted construction is available and reports exact diagnostics, but executable packages/receipts and the small-example listing are absent. Integer lifetime hardness imports classical DPRM, not unverified H10(Q); all new scientific correctness/priority remains unverified.',[card_ev('N339'),card_ev('N340'),card_ev('N341')])

gate(38,'G-ARITHMETIC-SELECTIVE-COVER-REVIEW','Review exact rational lifts, monodromy and representation costs',['N335','N336','N337','N338'],
    'Do the two explicit cubic detectors preserve the stated rational-point bijections and geometric/topological interfaces under their different degree/cost contracts?',
    'Verify the two classical elliptic rational-point classifications, genus-one rational-map irreducibility, localized etaleness and S3 discriminant monodromy. Check the positive-genus intermediate-cover principle without assuming base-field regularity; real analytic/Nash diffeomorphism and rational-closure topology. Validate one-lift lower-degree acquired-m smoothness/termination separately from parameter-free polytime higher-degree and quadratic-circuit normal forms. Scope degree3 optimality to proper rational-point selective etale covers. Integer quintic many-one hardness is independent of rational family004 Turing-hardness; inspect exact primary priority before novelty claims. No bounded-degree projective hypersurface or Mazur counterexample is supplied.',
    'Full text proofs supplied; no independent audits, scripts, primary paper bytes or external/formal correctness/priority clearance. Existing Poonen/elliptic precursors and earlier lower-degree Astra formulas remain credited and accessible.',[card_ev('N335'),card_ev('N336'),card_ev('N337'),card_ev('N338')])

gate(39,'G-SHARP-QMS-REGULARITY-EXTERNAL-REVIEW','Externally review internally closed sharp finite QMS regularity',['N342','N343','N345','N346','N347','N350'],
    'Do the exact physical Gram, finite legal sharpness and signed/polar conventions survive specialist or formal reconstruction?',
    'Reconstruct conditional-Choi/full generator representation, complete physical modular Gram with Hamiltonian and stationary potential, Hardy multiplier/reflection lower signs and normalization. Validate legal finite primitive upper families with faithful perturbations in the stated limit order, mandatory factor-four Hamiltonian correction, source weak/strong conventions, singular08 endpoint versus faithful non-KMS endpoint, and complete references. Audit signed/polar KMS only and ordinary positive-LSI hypercontractivity. Check exact primary priority separately; a replay or same-model agreement is insufficient.',
    'The p1 KMS endpoint is internally closed at08, all finite positive p>1 KMS/non-KMS sharp profiles at09. They are not still no-argument proof gates; remaining external/formal correctness, priority and infinite/non-KMS signed/polar extensions are distinct.',[card_ev('N342'),card_ev('N343'),card_ev('N345'),card_ev('N346'),card_ev('N347')])

gate(40,'G-VARYING-MARGIN-OBSERVATIONAL-RADIUS','Transfer the common-margin raw theorem to varying margins or obstruct it',['N93','N61','N344','N348','N349','N351'],
    'Can a legal quantitative varying-margin/optimized observational-radius reduction preserve the genuine entropy budget needed by one common reconstruction channel?',
    'Given ONE raw full-domain broadcaster and a varying-margin family, construct ONE acquired legal fixed channel/faithful weight with quantified simultaneous finite-reference error and genuine relative-entropy control, or give an exact legal counterexample to the claimed interface. Do not replace mutual information plus local D by optimized observational radius, choose one comparator per state, or reverse raw/restricted error inclusions. Preserve half-trace constants, all-reference/family quantifiers, conditioning, atom/precision/copy costs and scoped counterexamples. Validate09 common-margin theorem externally before promotion.',
    'Checkpoint09 raw fixed-margin theorem has internally closed squared exponent1/3 and exact one-map quantifier. Varying margins and optimized observational information are not covered. The old general mixed-reference Petz trace gate remains unresolved but is bypassed, so repeating it is not necessary for the admitted raw theorem.',[card_ev('N348'),card_ev('N349'),card_ev('N351'),card_ev('N93')])

gate(41,'G-PETZ-MIXED-REFERENCE-TRACE','Decide the remaining mixed-reference Petz trace transfer beyond its sharp binary controls',['N348','N349'],
    'Does a positive-power Petz TRACE residual bound exist on arbitrary finite mixed references at a genuine information budget?',
    'Prove one dimension-independent simultaneous bound with exact stationary-channel/sigma/family and reference contracts or give a legal counterexample. Binary CQ has sharp square-root exponent and fixed faithful qubit examples exclude exponents above1/2 even at fixed margin; preserve these scopes. The Petz square is legal, but legality, recovery for pure states, fixed-reference controls and relative-density metrics do not prove this mixed-reference bound. Do not treat a failure of Petz trace transfer as a refutation of the new energy-bypass raw classicality theorem.',
    'The broader Petz trace problem remains UNKNOWN. It no longer blocks raw common-margin reconstruction, and is an auxiliary mechanism decision rather than the current programme endpoint.',[card_ev('N349'),card_ev('N348')])

write_jsonl('CURRENT_CLAIM_STATUS.jsonl', list(ROWS.values()))
write_jsonl('OPEN_PROOF_GATES.jsonl', GATES)

priority_lines = ['# Current frontier', '',
    'Read this only for coordination. Workers start with `00_START_HERE.txt` and retrieve the relevant topic/card, its current-status row, scoped material updates, blockers and decisive proof ranges. `01_CORE.txt` is optional.', '',
    'This is a curated decision view of existing evidence, not a new research run. Priority means a supported next decision; it predicts neither correctness nor breakthrough value. Archived restart instructions do not authorize continuation.', '',
    'Source card status is immutable. A later claim can refine an older gap while remaining unverified. Proof availability, reported internal checks, external correctness and historical priority are separate. Unlisted relations and incomplete proof coverage remain UNKNOWN.', '',
    'AZ N342–352: exact linked archive is09, while user pi update describes08. Sharp complete physical KMS J>=piE and primitive faithful upper witnesses are internally closed;09 adds sharp finite positive KMS sine/non-KMS tangent Lp profiles, forwardpi/2, explicit KMS signed/polar and ordinary positive-LSI hypercontractivity. ONE raw-broadcaster/sigma-selected classical channel has common-margin MI squared exponent1/3 via full-domain repair and Petz ENERGY bypass. Remaining varying-margin/radius, mixed-reference Petz TRACE, orthogonal-basis, original-output and infinite-dynamics gates stay scoped. Mandatory Hamiltonian factor-four correction and old failed freezes retained; all3101 authored members/3098 payloads preserved. No intake scientific replay or external/formal/priority/capability promotion.', '',
    'AY N330–341: supplied complete C4 full-space common EB comparison on reversible bistochastic self-compatible channels, dimension-free power approximation and2<=C*<=4; sharpC2/nonnormal/broader-Holevo gates separate. Specific canonical coarse assembly candidate has continuum-dimensional kernel; stationarity-only L1 smoothing has sharp local8/global224. Exact one-lift cubic detectors have distinct degree/cost/real-topology interfaces, unconditional integer quintic versus conditional rational undecidability. Symmetric noise encodes lifetime undecidability under one unchanged stable flow with bounded rates. All5 original texts preserved; linked sandbox proofs/diagnostic packages and seven-reaction listing absent. No intake scientific replay or correctness/priority/capability promotion.', '',
    'AX N322–329: exact finite-support Card-ASM peak-HF bridge and conditional Card-only noncapture; original-grid qualitative lower bound does not need KOW, exponential scale does. Source-internal degree-only logarithm 2d bound includes reconstructed moving-center interpolation; general exponent2 and supplementary2d/r remain open, Pell refutes norm shortcut. Complete fixed-dimensional Hamiltonian shear encodes integer-fixed-point undecidability while always supplying a rational point, plus all-ring affine-scheme retract. Exact26-file second record and separate full proof preserved; no intake scientific replay/external/formal/priority/capability promotion.', '',
    'AW N308–321: source-internal sharp commonC2 for all defining-O(d) channel algebras and arbitrary unital qubit products including nonnormal channels; all-weight spin1 certificate, explicit full-covariant qutrit designs and other covariant classes. Exact C5 scalar-allocation no-go has a local-dual repair; tensor/moment/nontracial shortcuts have scoped counterexamples. UniversalfiniteC and revised all-spin/all-weight gates remain UNKNOWN. All21 native claims/current audit authority mapped, original603-member checkpoint02 retained; no intake scientific replay/external/formal/novelty/capability promotion.', '',
    'AV N304–307: NPT all-copy existential target remains unresolved; boundary-qutrit rank-two partial-trace obligation exact. Product-ray support subclass works for any finite sites, while an exact qubit co-Choi certificate fails at four sites with−40. Full proof/verifier/receipt/source scopes/probes/arrays preserved; no Werner distillability counterexample, all-copy theorem, primary3-copy certificate replay or external correctness/novelty certification.', '',
    'AU N298–303: fixed-BGS-term HF peak-state simulation independent of elapsed runtime, atom-safe quotient/GC/Card mechanisms and resettable binary2D compiler internally claimed. Conditional exponential transfer retains N285–287 lower-bound premises, binary n>=2 input and fixed-program costs. Full addendum/audits/negative controls/3 semantic suites preserved; no full FO generator execution or external/formal/novelty certification.', '',
    'AT N292–297: source-reconstructed shellwise-balanced all-correlation sector optimality and three-slab instability; Hermite-level dominance and single-profile radial concavity fail. Coupled radial(L) remains a stronger unproved sufficient simplex gate; imported dimension reduction and unlocated KLS priority claims require primary-source review. Exact checkpoint preserved; no foundational breakthrough/external correctness/novelty established.', '',
    'AS N276–291: exact specified PPT cubes plus filtered neighborhoods and scoped no-go/UNKNOWN rotations; Clifford common factor2, general common-frame gate open; conditional enlarged-group Bernoulli repair; restricted log-contact/winding/K1 costs. First record supplies fixed-model interpretation state-size/support/HF candidate, all-copy central log-entropy order with coefficient gap, exact finite determinant obstruction and any-pair Gaussian EB control. Two full captures and original Ultra ZIP preserved; 10/10 objective, external correctness/formal certification/novelty remain unestablished.', '',
    'AR N272–275: source claims flat/nonprojective residual dual with pd1/continuum Ext, exact scalar orbit transfers versus unresolved multiplicative coherence, enriched Koopman equivalence without multiplicativity, and conditional all-integer-power lifting/inverse formulas. No acquired compatible insertion/transfer or unequal-entropy conjugacy; residual R/M is distinct from the random-basis target Rp. Exact report preserved; inherited premises, external correctness and priority remain unverified.', '',
    'AQ N265–271: genus-one rational detector and effective affine smoothing; degree-eight undecidability remains upstream-conditional, projective boundary upgrade open. Infinite-index free-subgroup Bernoulli restriction and iid/global-well-order obstructions lead to an unconstructed random equivariant basis criterion. Full two reports retained, rank inference clarification separately labeled; no scientific replay, full conjugacy or external correctness/priority upgrade.', '',
    'AP six foundational reports plus two formerly missing branches: N246–264 preserve exact PIT representation/lift barriers and prior-art downgrade, conditional finite-power Bernoulli extraction with residual/cocycle and invariant gates, rank/topology transfer obstructions, averaged polar capacity and variable-area birth-degree budgets. Original PIT packet/code retained; other sandbox links unavailable. No foundational endpoint, scientific replay or external correctness/priority upgrade. Old AO programme remains paused.', '',
    'AO checkpoint is user-reported PAUSED: N227–245 preserve26 exact ledger claims, strongest chemical order-five equality/cubic exclusion, collective concentration and narrower charged certification, critical square-root Gibbs marginals. Next source-recommended mathematical gate is two-species order4; no research was resumed. N240 broadens the3D polar upper by attributed published energy-Gram machinery, and N242 makes the actual sampler-law obstacle concrete. Original proofs/audits and negative routes retained; all remain externally unverified.', '',
    'AM/AN: N213–226 include linear PPT decomposition-rank obstructions and a finite-reference non-CP positive-map candidate; N220 refines N213 only within its own ensemble. N223 adds grouped-cut distillability; N224 refutes naive cross-copy overlap multiplicativity without changing the single-copy law. Physical Gaussian channels can have EB squares; no composition or fixed-all-power breakthrough follows. Full authored proofs and original ZIPs retained; external correctness and priority unresolved.', '',
    'Late branch additions AL: N210/N211 uniform Steklov capacity for slow polar ends, independently of N175 existence; geometric matching conditional. N212 retains the balanced Lamperti proof and adds explicitly inherited unequal-rate phases and direct structural reconstruction. All10 frozen tips incorporated; prior source versions retained.', '',
    'Material additions AJ/AK: N195–202 engineered factorial probes and finite local scores; this does not close the original thermal-family score gate. N203–209 include SU(d) singlet theorems/counterexamples, Diophantine kinetic boundaries, conditional maximizing tail and catalytic critical explosion. N208 extends N170/N174 without deciding original entropy; N209 extends the N181 physical clock. All remain externally unverified.', '',
    'Material advances AI: N138 → N179/N180 critical-window bounds; exact full-SEP law and finite-N rates open. N75 → N187 actual-KL cap obstruction; anomalous KLS gate retained. N175–178 geometry source closure/whole-matrix repair uses current POST_SOURCE_STATUS while retaining earlier freeze versions. No internal audit becomes external validation.', '',
    'Material corrections: N135 → N160 is a full-proof candidate sharp identical-unital noise threshold; the old sufficient theorem remains valid. N132 → N136 is a candidate coefficient refinement with the full newer packet absent; N133 → N137 is a candidate stronger sufficient preparation bound. N159 invalidates the AE cycle7 N65 actual-origin blocks/audits, not the N65 theorem. N165 corrects the unsupported all-characteristics Formanek impossibility gloss; N47/N129 remain conditional unreviewed candidates and the primary-source discrepancy remains open. N166 corrects the infinite-only entropy caveat by Seward Corollary 7.7; original family197 entropy and Bernoulli isomorphism remain unresolved.', '',
    '| Order | Decision gate | Reason to decide next |', '|---|---|---|']
for g in GATES:
    priority_lines.append(f'| {g["priority_order"]} | `{g["gate_id"]}` — {g["title"]} | {g["priority_rationale"]} |')
priority_lines += ['', 'Exact pass conditions and immutable source hashes/line ranges are in `OPEN_PROOF_GATES.jsonl`. One row per card is in `CURRENT_CLAIM_STATUS.jsonl`; never preload the whole status file. Retrieve the relevant card row or sidecar through the repository retrieval interface.', '',
    f'Other historical restarts remain in `state/` and source archives. This dashboard selects {len(GATES)} concrete gates; it does not exhaustively rank every field or independently reconstruct all {len(ROWS)} cards. Candidate supersession does not externally validate a gate.', '']
(OUT / 'PRIORITIES.md').write_text('\n'.join(priority_lines))

counts = collections.Counter(x['proof_availability']['classification'] for x in ROWS.values())
receipt = {'schema_version': 1, 'cards': len(ROWS), 'gates': len(GATES),
    'availability_counts': dict(counts),
    'source_inputs': {p: digest(ROOT / p) for p in ('indexes/claims.jsonl','indexes/blockers.json')},
    'card_snapshot_sha256': hashlib.sha256(json.dumps({k:v['card_sha256'] for k,v in ROWS.items()},sort_keys=True).encode()).hexdigest(),
    'located_proof_document_count': sum(len(x['proof_availability']['located_proof_sources']) for x in ROWS.values()),
    'preserved_original_claim_status': True, 'scientific_proofs_replayed_or_validated': False,
    'exhaustive_relation_or_proof_audit': False,
    'files': {n: digest(OUT/n) for n in ('CURRENT_CLAIM_STATUS.jsonl','OPEN_PROOF_GATES.jsonl','PRIORITIES.md')},
    'validation': {'unique_card_ids': len(ROWS)==len(CLAIMS), 'source_text_hashes': all(x['text_hash_verified'] for x in CACHE.values()),
        'evidence_line_ranges': 'checked during generation', 'input_read_only': True}}
(OUT / 'BUILD_VALIDATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({'cards':len(ROWS),'gates':len(GATES),'availability':dict(counts)}))
