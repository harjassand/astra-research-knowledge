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
gate(5, 'G-THERMAL-SQRT-WINDOW', 'Resolve the stationary sqrt(N) bath window', ['N131','N138'],
    'For nu=c sqrt(N), what is the limiting distance to the full separable set?',
    'Derive a nontrivial limiting distance/constant threshold or an explicit separable approximant under the same stationary sector weights and arbitrary full-SEP adversary. Distance to I/2^N is only an upper bound; retain preparation, normalization and calibration costs.',
    'Current state proves only below/above polynomial exponents and identifies this exact remaining window; no complete phase diagram follows.',
    [evidence('state/2026-10-08-thermal-character-temperature-scaling/RESULT_AND_RESTART.md',68,93)])
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

gate(11, 'G-ORIGINAL-FAMILY197-ENTROPY', 'Decide original family-197 entropy before Bernoulli classification', ['N166','N167','N168','N169','N170'],
    'Can the original family-197 group be proved to have h_sup=0 or >0 under an independently checked witness?',
    'Acquire actual witness/group-word operations and a rank-density-to-zero sequence, or construct an actual arbitrarily-small-entropy generating measurable partition, or a nonsofic-applicable positive entropy lower bound. State the separate measurable conjugacy/invariant gate. Product G times Thompson V does not answer original G.',
    'Branches add concrete support, coding, finite-model and infinite-tail obstructions but do not decide original entropy. Corrected Corollary 7.7 removes the spurious infinite-only loophole; equality of all Bernoulli entropy still does not imply isomorphism.',
    [evidence('state/2026-10-08-bowen-bernoulli-direct-finiteness/CORRECTED_AUDIT.md',39,81),evidence('state/2026-10-08-family197-infinite-tail/RESEARCH.md',84,94)])

write_jsonl('CURRENT_CLAIM_STATUS.jsonl', list(ROWS.values()))
write_jsonl('OPEN_PROOF_GATES.jsonl', GATES)

priority_lines = ['# Current frontier', '',
    'Read this only for coordination. Workers start with `00_START_HERE.txt` and retrieve the relevant topic/card, its current-status row, scoped material updates, blockers and decisive proof ranges. `01_CORE.txt` is optional.', '',
    'This is a curated decision view of existing evidence, not a new research run. Priority means a supported next decision; it predicts neither correctness nor breakthrough value. Archived restart instructions do not authorize continuation.', '',
    'Source card status is immutable. A later claim can refine an older gap while remaining unverified. Proof availability, reported internal checks, external correctness and historical priority are separate. Unlisted relations and incomplete proof coverage remain UNKNOWN.', '',
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
