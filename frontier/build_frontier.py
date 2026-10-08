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
gate(2, 'G-GROUP-RING-PREMISE-FAILURE', 'Resolve the positive-characteristic source discrepancy and candidate geometry', ['N47','N129','N65','N165'],
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
gate(7, 'G-COMMON-EB-ARBITRARY-RANK', 'Decide the universal constant common-EB gate', ['N93','N143','N144'],
    'Is there one legal arbitrary-rank dimension-free common POVM, or a global legal counterexample?',
    'Prove a common full-domain comparator with a universal constant under the exact self-compatible/unital/HS-self-adjoint contract, or supply an actual channel obstruction. A restricted seed-hull failure or separate measurement for each direction is insufficient; charge broadcaster acquisition and finite-bit implementation.',
    'The logarithmic-dimension comparator is a concrete candidate improvement, while the dimension-free and continuous-support gates remain explicitly open.',
    [evidence('updates/AD/package/checkpoint/evidence/c4_quantum_lift/FINAL_REPORT.md',3,17),evidence('updates/AD/package/checkpoint/ACTIVE_GATES.json',20,40)])
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
gate(16, 'G-FACTORIAL-REGULARIZED-ENTROPY', 'Determine regularized entanglement entropy of engineered probes', ['N197','N198','N199','N224'],
    'Does the ordinary single-copy ln(N)+O(1) law survive regularization across N separated laboratories?',
    'Establish an across-copy lower and upper bound under arbitrary within-laboratory quantum correlations, or identify a valid lower-order comparator. Global Casimir conditioning cannot be assumed to preserve the separable alternative; keep single-copy and regularized quantities distinct.',
    'The sharp global heat effect proves the ordinary single-copy law. Only a separate small local noisy lower bound is regularization-safe; the logarithmic regularized law remains open. N224 now falsifies naive overlap multiplicativity with exact N=4 values 1/8>1/9.',
    [evidence('updates/AJ/package/CASIMIR_EXTREMALITY_AND_ENTROPY.md',56,128),evidence('updates/AJ/package/UNIVERSAL_BOUND_ENTANGLEMENT_PROOF.md',315,376),evidence('updates/AN/package/AUDIT_AND_FAILED_ROUTES.md',49,65)])
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
gate(21,'G-PPT-COMPOSITION-SENSITIVE-WITNESS','Acquire a composition-sensitive physical PPT-channel obstruction',['N213','N215','N220','N225'],
    'Can any admitted physical-channel invariant obstruct PPT squared or cubed after the channels are actually composed?',
    'Construct a physical PPT-channel composition with a globally valid entanglement witness or prove an admitted universal composition theorem. Keep reshuffling HS and operator norms distinct; a large individual decomposition rank is not a composition witness.',
    'Both surviving Gaussian obstruction ensembles can have entanglement-breaking squares, so their linear rank allowance does not settle PPT composition.',
    [evidence('updates/AM/package/PROOF.md',283,343),evidence('updates/AN/package/proofs/ITERATION_AND_LIMIT_BARRIERS.md',5,40)])
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

gate(26,'G-CIRCUIT-LOGARITHMIC-CONTACT','Decide circuit-size-sensitive logarithmic contact',['N246','N247','N248','N249','N250'],
    'Is there a uniform explicit polynomial contact bound B(n,s,D) for every nonzero admitted small commutative circuit, or a small-circuit counterfamily?',
    'Prove the size/degree/field/constant/evaluation contracts and a polynomial contact bound without expanding exponential derivative closure, or construct a uniform polynomial-size circuit family with superpolynomial contact. Four finite fixtures, large linear-state dimension or the prior small-derivative theorem do not settle this. Keep exact rational generator costs separate from black-box evaluation.',
    'The sufficient reduction is supplied, hypothesis unproved; direct nonlinear contact is not blocked by faithful linear-realization lower bounds.',[card_ev('N250'),card_ev('N249')])
gate(27,'G-DEFECT-BERNOULLICITY-OR-COCYCLE','Decide a residual Bernoullicity or cocycle-stabilization bridge',['N251','N252','N253','N254','N255','N256','N257','N258','N165','N166'],
    'Can the explicit finite defect power be proved Bernoulli, or can a stabilized Bernoulli insertion preserve the original twisted extension cocycle?',
    'Validate the actual torsion-free algebraic witness and the coloring/right-inverse proof, then prove the independent generating-Bernoulli property of K-power/X-times-residual, or exhibit exact measurable displacement lift/cocycle identity with a legal residual automorphism. Finite XOR feasibility, almost-cocycle convergence, infinite weak Pinsker entropy, mutual factors and equal ordinary invariants do not imply conjugacy. Earlier two-defect relative-isomorphism application requires separate exact-source review.',
    'A finite-power exact direct-product candidate is preserved, but unequal-entropy Bernoulli conjugacy and original supremal Rokhlin entropy sign both remain unresolved.',[card_ev('N252'),card_ev('N255'),card_ev('N256'),card_ev('N165')])
gate(28,'G-RANK-OR-MANIFOLD-TRANSFER','Acquire a bridge beyond rank and PL thickening obstructions',['N259','N260','N261','N65','N165'],
    'Is there an additional unitary-microstate obstruction or an alternative compact aspherical five-manifold realizing the required group?',
    'For approximation, supply structure beyond rectangular-word separation without an impossible characteristic-zero lift. For Singer, realize G-times-F2 in a compact aspherical five-manifold or supply a different above-middle homology mechanism, validating source geometry and the exact published reflection theorem. Canonical graph-product spines fail classical local link embeddings. Source rank obstructions and conditional hyperbolic five-manifold deduction are not these endpoints.',
    'Both routes need genuinely new mathematical input; do not treat an explicit obstruction, existing theorem application or repository integration as a historic discovery.',[card_ev('N259'),card_ev('N260'),card_ev('N261')])

write_jsonl('CURRENT_CLAIM_STATUS.jsonl', list(ROWS.values()))
write_jsonl('OPEN_PROOF_GATES.jsonl', GATES)

priority_lines = ['# Current frontier', '',
    'Read this only for coordination. Workers start with `00_START_HERE.txt` and retrieve the relevant topic/card, its current-status row, scoped material updates, blockers and decisive proof ranges. `01_CORE.txt` is optional.', '',
    'This is a curated decision view of existing evidence, not a new research run. Priority means a supported next decision; it predicts neither correctness nor breakthrough value. Archived restart instructions do not authorize continuation.', '',
    'Source card status is immutable. A later claim can refine an older gap while remaining unverified. Proof availability, reported internal checks, external correctness and historical priority are separate. Unlisted relations and incomplete proof coverage remain UNKNOWN.', '',
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
