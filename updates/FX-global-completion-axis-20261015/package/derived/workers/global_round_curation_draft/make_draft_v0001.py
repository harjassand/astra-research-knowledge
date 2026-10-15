#!/usr/bin/env python3
"""Create a reviewable FX draft and verify exact reference integrity only.

Writes are confined to this worker directory. This is not a root freeze,
scientific adjudicator, live integration generator, or checkpoint publisher.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

R = Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-global-completion-axis-v1')
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015')
D = R / 'workers/global_round_curation_draft'
BASE = 'ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25'
FX = 'updates/FX-global-completion-axis-20261015/'
BOUNDARY = ('DRAFT ONLY, pending root adjudication and exact selected-byte freeze. '
            'Source claims, internal derivations and same-team checks are separately attributed. '
            'External mathematical correctness, historical originality, formal verification '
            'and physical capability are UNKNOWN. Hash and line checks establish integrity only.')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def head() -> str:
    return subprocess.check_output(['git', '-C', str(W), 'rev-parse', 'HEAD'], text=True).strip()


def exclusive(name: str, raw: bytes):
    path = D / name
    assert path.parent == D and not path.exists(), path
    with path.open('xb') as stream:
        stream.write(raw)


inputs = {}
sources = {}
evidence = {}
head_before = head()
assert head_before == BASE, head_before


def source(path: str, label: str, role='worker_derivation', kind='proof', *, origin='R', sid=None):
    key = (origin, path)
    if key in sources:
        return sources[key]
    root = R if origin == 'R' else W
    raw = (root / path).read_bytes()
    raw.decode('utf-8')
    record = {'origin': origin, 'local_relative_path': path, 'sha256': digest(raw),
              'bytes': len(raw), 'line_count': len(raw.decode('utf-8').splitlines())}
    inputs[key] = record
    if origin == 'W':
        target = path
        assert sid is not None
    else:
        target = FX + 'package/' + ('originals/' if path.startswith('sources/') else 'derived/') + path
        sid = sid or 'src-FX-GCA-' + digest(path.encode())[:16]
    obj = {'path': target, 'sha256': record['sha256'], 'source_id': sid, 'title': label,
           'read_depth': 'Decisive cited statement and proof or documentary ranges read for this draft; curation reading is not a fresh independent scientific audit.',
           'provenance_role': 'supplied_original_file' if path.startswith('sources/') else role,
           'scope': BOUNDARY, 'local_origin': origin, 'research_relative_path': path if origin == 'R' else None,
           'local_relative_path': path, 'payload_kind': kind}
    sources[key] = obj
    return obj


def ev(key: str, path: str, lines, scope: str, *, label=None, role='worker_derivation', kind='proof', origin='R', sid=None):
    src = source(path, label or path.split('/')[-1], role, kind, origin=origin, sid=sid)
    count = inputs[(origin, path)]['line_count']
    end = count if lines[1] is None else lines[1]
    assert 1 <= lines[0] <= end <= count, (path, lines, count)
    evidence[key] = {'path': src['path'], 'sha256': src['sha256'], 'source_id': src['source_id'],
                     'lines': [lines[0], end], 'range_scope': scope, 'status': BOUNDARY,
                     'hash_kind': 'original_utf8_bytes', 'source_revision': BASE if origin == 'W' else None,
                     'local_origin': origin, 'local_relative_path': path,
                     'research_relative_path': path if origin == 'R' else None,
                     'package_path_status': 'existing_pinned_evidence' if origin == 'W' else 'PROPOSED_ROOT_FREEZE_MAPPING_NOT_YET_PRESERVED_BY_THIS_WORKER'}


ev('shear_source_statements', 'sources/global_compatible_positivity/RESEARCH_REPORT.md', [10, 120],
   'Definitions; universal isotropic H-subtracted completion; exact finite-alpha projection; fixed-input-heat determinant-square obstruction.', label='Supplied universal shear-completion report')
ev('shear_schur_proof', 'workers/global_completion_reconstruction/AUDIT.md', [51, 146],
   'Independent internal reconstruction of universal identities, quotient positivity, both Schur estimates and sufficient completion margin.', label='Independent global-completion reconstruction', role='same_team_review')
ev('shear_heat_analytic', 'workers/global_completion_reconstruction/AUDIT.md', [148, 198],
   'All-background relative heat energy, exact-form Stokes, density/periodic extension and classical sqrt(24) Beurling constant.', role='same_team_review')
ev('shear_projection', 'workers/global_completion_reconstruction/AUDIT.md', [200, 246],
   'Exact acoustic necessities and decomposition F=lambda P_(alpha/lambda,rho)+(gamma-lambda)det^2; equality only after deleting alpha.', role='same_team_review')
ev('shear_prior_and_positive_export', 'workers/global_completion_reconstruction/AUDIT.md', [248, 313],
   'Existing negative sharp theorem dominates the nonsharp completion there; positive high-alpha scope and explicit 62385H+j^2+uj export; positive sharp QC remains unknown.', role='same_team_review')
ev('ordinary_pc_all_alpha', 'workers/global_completion_reconstruction/EXACT_NONPOLYCONVEX_COMPLETION.md', [29, 104],
   'Ordinary finite convex lift has local support; forced determinant slope; alpha-independent null Hessian direction and nonzero cubic; C3-flat corrections cannot repair.', label='Ordinary polyconvexity obstruction at every finite H coefficient')
ev('ordinary_pc_curved_boundary', 'workers/global_completion_reconstruction/EXACT_NONPOLYCONVEX_COMPLETION.md', [106, 135],
   'Entire nonzero curved projected boundary has no finite ordinary-PC completion; strict interior and positive sharp-QC thresholds remain undecided.')
ev('source_input_heat_obstruction', 'workers/global_completion_reconstruction/AUDIT.md', [315, 353],
   'Actual compatible determinant-square energy rise under each SPD input heat; no universal zero-integral repair for that same dissipation.', role='same_team_review')
ev('prior_negative_face', 'updates/FW-moving-heat-observable-20261015/package/derived/workers/moving_kernel_genesis/REPORT.v0002.txt', [16, 95],
   'Pinned N867 sharp complete negative-delta QC iff ROC iff two LMIs and exact nonnegative sharp-generator/minor/H decomposition.', origin='W', sid='src-FW-MHO-negative-face-v2')
ev('prior_universal_negative', 'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_REPORT.txt', [109, 201],
   'Inherited universal rational corrected-heat identity, all twelve strictly positive pivot functions for r<-2, and all-affine analytic QC implication.', origin='W', sid='src-FW-MHO-sharp-universal')
ev('prior_negative_analytic_audit', 'updates/FW-moving-heat-observable-20261015/package/derived/workers/nonlinear_flow_audit/UNIVERSAL_QC_ANALYTIC_AUDIT.md', [22, 96],
   'Fixed-r heat quantifier, density and periodic passage; negative-delta decomposition; no branch-uniform estimate asserted.', origin='W', sid='src-FW-MHO-universal-analytic-final', role='same_team_review')
ev('prior_same_G_coercivity_scope', 'updates/FW-moving-heat-observable-20261015/package/derived/root/COERCIVITY_AND_STORAGE_COROLLARY.md', [7, 80],
   'Existing margin 4nu/1875, no boundary constant from H subtraction, same-G 3/1250 and unchanged N866 fixed-integrand contract.', origin='W', sid='src-FW-MHO-storage-root', role='root_synthesis')
ev('prior_storage_uniform_input', 'updates/FW-storage-computability-20261015/package/storage_horizon/FINITE_HORIZON_STORAGE.md', [9, 63],
   'N866 needs a positive numerical uniform gradient-energy constant and a certified endpoint extension budget; strictness alone is insufficient.', origin='W', sid='src-FW-storage-horizon')
ev('nonshear_statement', 'workers/full_invariant_genesis/REPORT.md', [20, 102],
   'Exact existential completion equivalence on alpha H+k w^2+ell vj+m v^2; strict k,L,D cone plus convex exception; sufficient alpha and reserve margin.', label='Independent nonshear contact-stratum construction')
ev('nonshear_contact_distinction', 'workers/full_invariant_genesis/REPORT.md', [104, 170],
   'Trace invariant distinguishes (I,e11) from (I,e12); ROC plus contact stationarity forces the four-dimensional span.')
ev('nonshear_necessity_boundaries', 'workers/full_invariant_genesis/REPORT.md', [172, 256],
   'Weak conformal necessity and actual alpha-independent leading-sign acoustic obstructions at L=0 and D=0.')
ev('nonshear_quadratic_and_flatness', 'workers/full_invariant_genesis/REPORT.md', [258, 336],
   'Supplied lambda=3ell gives PSD quadratic support with kernel span e11, explicit transverse kappa, tensor bound and cubic flatness.')
ev('nonshear_completion_proof', 'workers/full_invariant_genesis/REPORT.md', [338, 456],
   'Complete Taylor/Young absorption at every affine background, classical elliptic estimates, zero-boundary/periodic extension and 4nu/1875 margin.')
ev('nonshear_contacts_and_nonpc_example', 'workers/full_invariant_genesis/REPORT.md', [458, 532],
   'Global nonzero acoustic contact set at sufficient alpha; no single invertible two-sided transport from a shear-contact quartic; explicit completed non-PC example.')
ev('nonshear_independent_audit', 'workers/nonshear_face_independent_audit/REPORT.md', [7, 127],
   'Independent statement and necessity/boundary reconstruction; contact equality alone is insufficient and has an explicit non-ROC counterexample.', label='Independent nonshear-face audit', role='same_team_review')
ev('nonshear_independent_analytic', 'workers/nonshear_face_independent_audit/REPORT.md', [129, 265],
   'Independent complete analytic sufficiency proof using a finite standard L4 elliptic bound, with no strict-LH theorem at the degenerate contact.', role='same_team_review')
ev('general_flat_statement', 'workers/full_invariant_genesis/GENERAL_FLAT_COMPLETION.md', [1, 52],
   'Joint root/worker full-space sufficient theorem with supplied lambda, PSD Q, kernel cubic-flatness, explicit alpha and exact reserve margin.', label='Joint full-space degenerate-flat completion compiler')
ev('general_flat_proof', 'workers/full_invariant_genesis/GENERAL_FLAT_COMPLETION.md', [54, 123],
   'Complete degenerate Taylor/Young proof and zero-rank case G=cH; no ellipticity assumed on the kernel.')
ev('general_flat_compiler_scope', 'workers/full_invariant_genesis/GENERAL_FLAT_COMPLETION.md', [125, 203],
   'Fixed-dimensional rational principal-minor/kernel/flatness compiler with supplied lambda; eigenvalue-free kappa; failure means unresolved; inherited QC sharp J fails the sufficient predicate.')
ev('general_flat_independent_proof_audit', 'workers/general_flat_completion_independent_audit/REPORT.md', [7, 101],
   'Independent generalized theorem, Frobenius normalization, complete Taylor absorption, reserve identity, zero-rank proof and rational supplied-certificate bit-cost audit; initial implementation-pending sentence is superseded by final addendum.', label='Independent general flat-completion mathematical audit', role='same_team_review')
ev('general_flat_corrected_implementation_audit', 'workers/general_flat_completion_independent_audit/ADDENDUM_IMPLEMENTATION.md', [3, 51],
   'Final corrected exact-input implementation passes76 independent assertions; supplied rational lambda and reserve bit lengths charged; pre-correction decimal-rounding defect retained as history.', label='Final independent corrected-compiler audit', role='same_team_review')
ev('general_flat_parser_correction', 'workers/full_invariant_genesis/PARSER_CORRECTION.v0002.md', [3, 56],
   'Author preserved initial code/receipts and corrected JSON decimal/scientific parsing; accepts exact rationals, rejects floats/nonfinite/booleans/invalid reserves; theorem and protected stratum artifacts unchanged.', label='Exact rational parser correction v2', role='worker_derivation', kind='review')
ev('output_heat_common_datum', 'workers/output_heat_rank_preservation/ANALYTIC_PROOF.md', [7, 130],
   'Exact ordered spatial-sum convention, coercive real symbol, common compact rank-one-gradient datum and velocity 4 C11_22; energy rises at positive time, not first derivative at zero.', label='Output-matrix determinant-square analytic obstruction')
ev('output_heat_no_null_repair', 'workers/output_heat_rank_preservation/ANALYTIC_PROOF.md', [132, 169],
   'Exact compact perturbation v_s=u0+sLu0 has negative integrated dissipation; every universally integral-null pointwise repair of the same operation is impossible.')
ev('output_heat_tangency_classification', 'workers/output_heat_rank_preservation/ANALYTIC_PROOF.md', [171, 218],
   'The zero effective homogeneous constant second-order planar operator is the only universal rank-one-gradient tangent; every nonzero such operator has negative integrated determinant-square dissipation without a parabolic premise.')
ev('output_heat_adaptive_dimension_scope', 'workers/output_heat_rank_preservation/ANALYTIC_PROOF.md', [220, 301],
   'C1 autonomous C(u,Du) near-zero obstruction conditional on classical evolution; fixed constant strongly parabolic extension to all square n>=2; determinant square remains PC and QC.')
ev('scalar_projection_J_counterexample', 'workers/positive_branch_new_operation/REPORT.md', [92, 276],
   'Actual compatible periodic scalar-potential projection raises sharp J_r energy for every r>0; explicit r=1 positive-radius disk gap; both energies positive.', label='Positive-branch nonlocal operation audit')
ev('burkholder_contact_obstruction', 'workers/positive_branch_new_operation/REPORT.md', [278, 397],
   'Strict relative-shear symmetric second difference of quartic Burkholder terms excludes well-defined positive invertible superpositions plus a ROC remainder; no Burkholder-QC premise is used.')
ev('positive_QC_moment_gate', 'workers/positive_branch_new_operation/REPORT.md', [399, 461],
   'Exact all-background QC reformulation for every compatible periodic gradient using A,c,K and a PSD block/Schur inequality; equivalence is not a proof of the inequality.')
ev('positive_branch_failed_search_scope', 'workers/positive_branch_new_operation/REPORT.md', [463, 542],
   'Exact three-wave phase formulas, finite failed numerical searches, non-gradient clipping falsifier and precise remaining coupled operation; numerical outputs do not upgrade UNKNOWN.')
ev('classical_completion_priority_scope', 'workers/compatible_positivity_priority/PRIORITY_AND_APPLICABILITY.md', [3, 47],
   'Acquired primary strict-LH completion and projection-closure results are classical; persistent degenerate contact invalidates direct applicability; bounded search does not clear priority.', label='Primary-literature applicability audit', role='same_team_review')
ev('closed_isotropic_orbit_noninheritance', 'workers/compatible_positivity_priority/ORBIT_COMPLETION_NONINHERITANCE.md', [10, 77],
   'Common shear contact forces the stated closed positive isotropic-orbit-plus-convex source cone to be PC there; all-alpha cubic excludes every q>0 curved completion from that exact route.', label='Finite-completion closed-orbit exclusion', role='same_team_review')
ev('axis_original_hypothesis', 'sources/axis_writing/README.md', [5, 41],
   'Supplied FeNiN directional retained-axis hypothesis, no raw experiment, same immobilized material and cyclic rewrite requirement.', label='Supplied chemical-axis hypothesis dossier')
ev('axis_root_v4', 'root/ORDER_VOLUME_IDENTIFICATION.v0004.md', [5, 49],
   'Corrected root exact false-positive, unrestricted positive-floor identified set, restricted-axis LP, sharp intervals and fixed-W versus joint zero-floor closure.', label='Root order-volume identification v4', role='root_synthesis')
ev('axis_final_independent_review', 'independent_audits/axis_evidence_adversary_final/ROOT_LEMMA_FINAL_AUDIT_ADDENDUM.v0002.md', [3, 30],
   'Current independent sign-off verifies root v4 hash and20 corrected checks; earlier scope/notation/checker findings are closed; sharp intervals and physical boundary retained.', label='Independent corrected root-v4 order-volume audit v2', role='same_team_review')
ev('axis_independent_vertex_proof_history', 'independent_audits/axis_evidence_adversary_final/ROOT_LEMMA_FINAL_AUDIT_ADDENDUM.md', [19, 48],
   'Retained initial-audit proof of unrestricted/support qualification and independent sharp vertex endpoints; fixed-fiber correction has now been incorporated and verified in v2, so this is not an unresolved current finding.', label='Retained initial independent order-volume proof history', role='same_team_review')
ev('axis_control_limits', 'workers/axis_control_genesis/PROOFS.md', [5, 57],
   'Conditional label-preserving invariance/site-count, common-channel information contraction, restricted cubic-variant alignment bound, planar countermodel and explicitly modeled nucleation benchmark.', label='Conditional chemical-axis control limits')
ev('axis_measured_literature_scope', 'workers/axis_evidence_adversary/EVIDENCE_REPORT.md', [9, 40],
   'Source-attributed primary evidence and access limits; strong orientation/stress comparators, absent same-domain response, measurement gates and complete costs.', label='Adversarial chemical-axis evidence review', role='same_team_review')
ev('axis_measurement_countermodels', 'workers/axis_evidence_adversary/MEASUREMENT_DESIGN.md', [5, 22],
   'Identical superlattice moments with different volume moments and 6/5 apparent write contrast at unchanged fixed-axis volume tensor.', label='Chemical-axis measurement interface and exact falsifiers')
ev('axis_measurement_acquisition_gates', 'workers/axis_evidence_adversary/MEASUREMENT_DESIGN.md', [32, 76],
   'Nuisance response rank and conditioning, angular integrated-mass error, missing mass, order-floor upgrade and same-domain causal controls; actual response arrays missing.')
ev('axis_competent_comparators', 'workers/axis_control_genesis/README.md', [9, 50],
   'Applicant-reported precursor milling texture versus epitaxial/stress comparators; broad mechanism already disclosed; narrow fixed-material rewrite remains unacquired; full preparation/reset costs.')
ev('sharp_rank_one_bound', 'workers/sharp_boundary_coercivity/PROOFS.md', [68, 112],
   'Rank-one quartic Bregman bound at every B and alpha(r)/3 fourth-power margin for rank-one-valued gradients.', label='Sharp negative-boundary strictness and angular construction')
ev('sharp_individual_strictness', 'workers/sharp_boundary_coercivity/PROOFS.md', [114, 213],
   'Exact necessary kernel rows plus analytic rigidity and inherited heat identity give strict Jensen positivity for each individual nonzero perturbation; no uniform constant.')
ev('sharp_angular_margin', 'workers/sharp_boundary_coercivity/PROOFS.md', [215, 372],
   'Degree-half homogeneous heat renormalization, rough-data one-sided Fatou, one-dimensional compactness and rank-one bound prove a nonconstructive positive angular margin at each fixed r; fixed B annuli only.')
ev('sharp_uniform_gate_and_storage_boundary', 'workers/sharp_boundary_coercivity/PROOFS.md', [374, 490],
   'Exact affine-minimized residual, numerical outputs as upper candidates only, missing all-affine uniform fourth-power margin and no sharp-J N866 transfer.')
ev('sharp_clarification', 'workers/sharp_boundary_coercivity/CLARIFICATION_20261015_V1.md', [12, 121],
   'Additive clarification gives all eight outer-product equations, full affine gradient in strictness, and normalized/angular amplitude condition at fixed B; small amplitudes create growing effective backgrounds.', label='Frozen sharp-boundary additive clarification v1')
ev('sharp_independent_analytic_audit', 'workers/global_completion_reconstruction/sharp_strict_audit/AUDIT.md', [23, 320],
   'Independent analytic reconstruction validates strictness, truncated critical heat renormalization, rough-data Fatou and angular compactness with accepted outer-product/full-affine/normalized-amplitude clarifications; uniform all-affine margin remains unproved.', label='Final independent sharp strictness and angular analytic audit', role='same_team_review')
ev('sharp_supporting_exact_audit', 'workers/global_completion_reconstruction/sharp_strict_audit/EXACT_AUDIT_RECEIPT.json', [1, None],
   'Independent exact kernel/scaling/polarization supporting checks only; does not adjudicate analytic strictness or angular compactness.', label='Independent sharp-strictness exact reduction receipt', role='same_team_review', kind='receipt')
ev('pulse_identity_and_data_roles', 'workers/new_source_identity_luna/REPORT.md', [6, 33],
   '55 sources in 7 groups; all25 pulse files byte-identical to prior FW; embedded archive identity; pasted archival prompts are DATA and cannot certify exact role boundaries.', label='Exact new-source identity audit', role='same_team_review', kind='review')
ev('external_paper_not_admitted', 'workers/projection_claim_audit/REPORT.md', [1, 29],
   'External preliminary projection/Burkholder/Beurling paper internally reconstructed only, AUDIT_RECONSTRUCTED_NOT_ADMITTED; no sharp constant admission or causal-AI identity inference.', label='External preliminary projection-paper admission boundary', role='same_team_review', kind='review')


def card(cid, title, scope, statement, assumptions, proof_spine, refs, *, costs, acquisition,
         obstruction, comparator, missing, next_step, review, internal='complete_internal_proof',
         inventory=(), paragraphs=(), failed=(), relations=None):
    obj = {'id': cid, 'title': title, 'scientific_scope': scope, 'statement': statement,
           'costs': costs, 'information_acquisition': acquisition, 'obstruction': obstruction,
           'comparator': comparator, 'missing_lemma': missing, 'next_decisive_step': next_step,
           'read_review_depth': review, 'reported_status': BOUNDARY,
           'proof_availability_scope': 'Readable internal proofs are available for precisely the mathematical subclaims in the cited spans. No physics, priority or unproved extension is included.',
           'topics': [], 'assumptions': assumptions, 'proof_spine': proof_spine,
           'proof_availability': 'provisional_manuscript_available', 'proof_refs': refs,
           'inventory_refs': list(inventory), 'paragraphs': list(paragraphs),
           'reported_failed_attempts': list(failed), 'missing_artifacts': [],
           'internal_proof_status': internal, 'route_assignment': 'TENTATIVE_UNRESERVED_ROOT_ONLY'}
    if relations:
        obj.update(relations)
    return obj


N867 = 'N867-sharp-contact-face-and-quasiconvex-boundary'
N863 = 'N863-compatible-null-heat-roc-ray'
N868 = 'N868-smooth-quasilinear-tangent-obstruction'
N869 = 'N869-pulse-hard-pair-and-finite-ramp-acquisition'
N866 = 'N866-effective-storage-value-computability'
N872 = 'N872-universal-shear-completion-and-ordinary-polyconvexity-obstruction'
N873 = 'N873-nonshear-projection-and-degenerate-flat-completion'
N874 = 'N874-determinant-energy-and-positive-branch-operation-limits'
N875 = 'N875-chemical-axis-order-volume-identification-and-physical-gate'
N876 = 'N876-sharp-negative-strict-jensen-and-angular-margin'

cards = [
    card(N872, 'Universal finite H completion on the shear projection and no finite ordinary-PC repair',
         'Real homogeneous quartics F=alpha H+beta u^2+gamma j^2+delta uj on 2x2 matrices, H=((a-d)^2+(b+c)^2)^2, u=a^2+c^2, j=det A; existence of finite alpha after deleting that coordinate.',
         'Some finite alpha makes F ROC iff some finite alpha makes it all-background QC iff either delta=0 with beta,gamma>=0, or delta!=0, gamma>0, 6beta gamma-delta^2+delta gamma>=0 and 2beta+delta>0. For q=r(r+2)>0, the exact universal isotropic construction supplies a finite c(r) with P_(c(r),r) QC and, for alpha>=c(r), Jensen gap >=4(alpha-c(r))/1875 times integral|Dphi|^4. Every finite P_(alpha,r) with r(r+2)!=0 is ordinarily non-polyconvex, even allowing arbitrary nonsmooth nonpolynomial convex lifts. The same local obstruction survives every everywhere-finite C3 correction flat through degree three at I. On the nonzero curved projected boundary, finite QC completion exists while finite ordinary-PC completion does not. QC at the positive sharp floor remains UNKNOWN.',
         ['Every bounded planar Lipschitz domain, every affine background B and every W0^(1,4) perturbation; periodic analogue.',
          'Projection quantifies existence of one finite real alpha independent of B and the perturbation; it is not equality of individual alpha fibres.',
          'Ordinary-PC theorem uses an everywhere-finite integrand smooth near I; cubic-flat extension uses the stated local C3 jet.'],
         ['Direct acoustic tests force the projection inequalities and rule out r=-2 for every finite alpha.',
          'Universal rational identity and 6+4+8 quotient/Schur construction are positive on both unbounded q>0 branches.',
          'Exact-form Stokes, relative heat decay and density imply all-background QC; a separate nonnegative det^2 Jensen term completes the general projected triple.',
          'Ordinary lifted support forces slope r+2; the support gap along diag(1,-r-1) is -r(r+2)t^3/3+O(t^4), independent of finite alpha at cubic order.'],
         ['shear_source_statements', 'shear_schur_proof', 'shear_heat_analytic', 'shear_projection', 'ordinary_pc_all_alpha', 'ordinary_pc_curved_boundary', 'shear_prior_and_positive_export'],
         costs='At rational r the sufficient compiler uses finite exact rational matrices of order at most18, with no optimization oracle. Coefficients and conditioning can grow near r=-2; no optimal alpha or general bit/runtime/energy bound is claimed. All arithmetic, input reading and exact certificate checks are charged.',
         acquisition='Quartic coefficients, source JSON and parameter are supplied mathematical data. The positive r=1 export is 62385H+j^2+uj with at least4/1875 reserve margin, not acquired material response or a useful numerical solver.',
         obstruction='The nonclosed projection limit r=-2 has a genuine acoustic obstruction and unavoidable necessary alpha divergence. The compiler is nonsharp. Non-PC is not non-QC; no strict-interior PC classification follows.',
         comparator='Pinned N867 already proves the optimal negative sharp floor and all delta<=0 fibres. Its sharper result is retained; classical strict-LH completion is inherited and misses persistent contacts.',
         missing='Positive sharp-fibre QC, exact full nine-dimensional QC classification, strict-interior ordinary-PC classification, external review and historical priority remain open.',
         next_step='Prove the compatible moment/Schur inequality for every positive sharp J_r or construct a certified compatible negative Jensen perturbation; compare boundary applicability to primary literature.',
         review='Supplied theorem statements and independent reconstruction proofs read, including both Schur bounds, analytic QC passage and all-alpha ordinary-PC support proof. Prior negative sharp proofs and current notices read; this curation does not add another independent audit.',
         inventory=['classical_completion_priority_scope', 'closed_isotropic_orbit_noninheritance'],
         paragraphs=['The new completion adds positive-branch finite-alpha and full projected scope. It does not improve the inherited negative sharp threshold, the original G certificate, or any storage result.', 'The stated closed positive isotropic-orbit-plus-convex inheritance route is also excluded for every q>0 finite completion by the same contact and ordinary-PC cubic; signed or more general routes remain outside that argument.'],
         relations={'material_updates': [{'target': N867, 'scope': 'Adds the full finite-alpha completion projection, positive high-alpha QC completion and all-finite-alpha ordinary-PC obstruction; preserves the stronger inherited negative sharp theorem and the unresolved positive sharp fibre.', 'relation_status': 'scoped internal mathematical addition; external review UNKNOWN', 'ref_ids': ['shear_projection', 'ordinary_pc_all_alpha', 'shear_prior_and_positive_export']}]}),
    card(N873, 'A nonshear completion projection and a supplied-certificate degenerate-flat compiler',
         'Left-SO(2)-invariant real homogeneous quartics on 2x2 matrices; the exposed ROC contact face at (I,e11), plus a separate sufficient compiler in the full nine-dimensional invariant space.',
         'For every real k,ell,m, some finite alpha makes alpha H+k w^2+ell vj+m v^2 ROC iff some finite alpha makes it all-background QC iff (k=ell=0,m>=0) or (k>0,L=ell+2m>0,D=2km-k ell-ell^2>0). ROC plus the contact equality gives the four-dimensional span; contact alone does not. Separately, any invariant quartic G=T(A,A,A,A) admits the sufficient completion if a supplied lambda makes Q(X)=D2G(I)[X,X]/2-lambda det X PSD and T(I,Z1,Z2,E)=0 for every Z1,Z2 in kerQ and every E. With Q nonzero, supplied positive kappa on kerQ-perp and tensor bound M, alpha_*=401296M^2/kappa+(9391/4)M suffices; extra nu H gives4nu/1875 margin. If Q=0, flatness forces G=cH and convex completion is explicit. Failed admission means UNRESOLVED_BY_THIS_COMPILER.',
         ['All-background bounded-Lipschitz W0^(1,4) and periodic gradient contract.',
          'The contact-stratum description assumes rank-one convexity or quasiconvexity as well as D2F(I)[e11,e11]=0.',
          'Full-space theorem assumes exact supplied lambda, PSD quadratic support and the quantified two-kernel-vector cubic flatness; it is sufficient only.'],
         ['Acoustic stationarity yields codimension-five contact span; direct conformal tests give k>=0,L>=0,D>=0.',
          'Actual rank-one acoustic curves exclude nontrivial L=0 and D=0 equality boundaries for every finite alpha.',
          'Transverse PSD support and cubic flatness control the full Taylor remainder; classical CR L2/L4 estimates let H absorb it at every B.',
          'The joint generalization handles arbitrary kernel rank, the Q=0 case and a fixed-dimensional rational admission compiler with eigenvalue-free kappa.'],
         ['nonshear_statement', 'nonshear_contact_distinction', 'nonshear_necessity_boundaries', 'nonshear_quadratic_and_flatness', 'nonshear_completion_proof', 'nonshear_contacts_and_nonpc_example', 'nonshear_independent_audit', 'nonshear_independent_analytic', 'general_flat_statement', 'general_flat_proof', 'general_flat_compiler_scope', 'general_flat_independent_proof_audit', 'general_flat_corrected_implementation_audit', 'general_flat_parser_correction'],
         costs='Rational lambda, coefficients and reserve are supplied and their numerator/denominator bit lengths are charged. Principal-minor, kernel and flatness checks use matrices of order at most4 and at most35 monomials; fixed rational expressions have O(n) bit size and polynomial total bit work for n-bit rational inputs. Finding lambda is separate. Corrected exact JSON parsing preserves decimal/scientific rationals and rejects pre-parsed floats/nonfinite/boolean inputs; initial rounded-input failure and code are preserved. Large sufficient alpha is a conservative proof cost, not an optimum or practical algorithm claim.',
         acquisition='The independent stratum construction and independent stratum audit are distinct. GENERAL_FLAT_COMPLETION is a subsequent root/worker joint extension and must not be counted as independent corroboration. No physical inputs or devices are acquired.',
         obstruction='The trace of A^-1R distinguishes the nonshear contact from the old shear contact under invertible two-sided transforms. At sufficient alpha the entire nonzero-background contact set is sQtheta,rQtheta e11, excluding equality to a single shear-contact transport; positive sums and limits are not excluded. Known QC sharp J_r fails the compiler cubic-flatness predicate, proving the predicate is not necessary.',
         comparator='The classical Iwaniec-Kristensen strict-LH completion framework is credited; persistent rank-one contacts violate its strict premise. The independent audit reconstructs degenerate sufficiency directly.',
         missing='Least alpha, full eight-dimensional projected boundary membership, necessity of the general admission predicate, other nonzero-trace contact-angle strata and an efficient lambda-finding procedure remain open.',
         next_step='Classify an additional contact-angle stratum or enlarge the supplied-certificate admission region with a proved lemma; a failed compiler check must stay unresolved.',
         review='Independent stratum construction/audit and subsequent independent general mathematical audit read. Final implementation addendum and parser v2 correction read; corrected compiler SHA bb0cea71e048eccac401a91288b17d7ed1ce7d705250d52dfc29addc71d21433 has76 independent passing assertions. Contact-only and supplied-lambda qualifications retained.',
         inventory=['classical_completion_priority_scope'],
         paragraphs=['An explicit admitted quartic is113325063H+w^2-vj+(3/4)v^2. It has all-background Jensen margin at least1/1125 times integral|Dphi|^4 and F(I)=-1/4, so it is non-PC. The large coefficient is sufficient only.']),
    card(N874, 'Determinant energy defeats constant second-order operations; sharp positive QC remains open',
         'Exact limitations of specified smoothing, scalar-potential projection and positive Burkholder-superposition operations; they do not classify QC.',
         'For planar vector maps, L u=sum C^{ij}u_ij with real constant output matrices and C^{ij}=C^{ji}: L=0 is the only homogeneous second-order operator universally tangent to all rank-one gradients. Every nonzero such L has a smooth compact compatible map with negative integrated determinant-square dissipation, excluding every correction that has universally zero integral and makes that same density pointwise nonnegative. For the coercive real strongly-parabolic subclass, one common compact datum u0=(f,f^2), f=x1+x1x2 near0, satisfies detDu0=0 and determinant velocity4 C11_22>0; E(0)=Eprime(0)=0 and E grows at positive times. C1 autonomous C(u,Du) has the corresponding near-zero obstruction conditional on classical evolution. Separately, scalar-component constrained-potential projection can increase sharp J_r energy for every r>0, and well-defined positive invertible Burkholder superpositions plus a ROC remainder cannot represent J_r. Sharp positive QC is UNKNOWN.',
         ['Ordered spatial sum includes2C12 partial12; no output symmetry is required.',
          'Strong parabolicity means the real symmetric-symbol coercivity a_alpha Cij_alpha,beta a_beta xi_i xi_j>=lambda|a|^2|xi|^2, lambda>0, rather than an eigenvalue-real-part substitution.',
          'Compact smooth planar maps or smooth periodic maps; state-adaptive corollary assumes classical solution, initial differentiation and finite energy.',
          'Burkholder exclusion assumes positive measure and absolute integrability near I,I+-t e12, with a ROC remainder; no external Burkholder-QC theorem is assumed.'],
         ['Exact compact curve-image jets give nonzero determinant velocity; differentiating v_s=u0+sLu0 gives strictly negative integrated same-operation dissipation.',
          'Three local scalar jets force all12 effective constant operator coefficients to vanish under universal rank-one tangency.',
          'A compatible periodic first-variation construction makes scalar-row projection raise positive J_r energy; at r=1 a positive-radius disk has an exact gap.',
          'Every invertible Burkholder term has strict relative-shear quadratic variation while J_r has only fourth-order shear variation; positivity and Fatou rule out the stated representation.'],
         ['source_input_heat_obstruction', 'output_heat_common_datum', 'output_heat_no_null_repair', 'output_heat_tangency_classification', 'output_heat_adaptive_dimension_scope', 'scalar_projection_J_counterexample', 'burkholder_contact_obstruction', 'positive_QC_moment_gate'],
         costs='Finite symbolic differentiation and coefficient/rank checks establish the stated algebra; semigroup/compactness/Fatou arguments are written analytic proofs. No faster PDE solver, finite-dimensional QC test, convergence rate, physical implementation or cost advantage is supplied. Nonzero nonparabolic L has an algebraic dissipation witness without an evolution-existence claim.',
         acquisition='Operator coefficients, compatible test maps and quartic coefficients are supplied. No experimental operation is acquired. The preliminary external sharp Beurling paper is AUDIT_RECONSTRUCTED_NOT_ADMITTED; all completion margins retain the established nonsharp sqrt(24) bound.',
         obstruction='Determinant square remains PC and QC. No-null-repair excludes only corrections with both universal zero integral and pointwise positivity for the same dissipation. State adaptation does not cover explicit x dependence, divergence-form substitution, lower-order compensation, singular/degenerate coefficients, nonlocal rules or auxiliary states. Projection counterexamples do not refute the actual scalar lemma.',
         comparator='Separate determinant-Jensen addition already succeeds in the completion proof and is outside universal monotonicity of one flow. Classical scalar projection contracts matching convex radial scalar energies; determinant-coupled vector energies require a different argument.',
         missing='For every compatible periodic V, with A=<J_r(V)>,c=<DJ_r(V)>,K=<D2J_r(V)>/2, positive sharp QC is equivalent to PSD [[A,cT/2],[c/2,K]], or c in rangeK and cT Kdagger c<=4A. No proof for all V or compatible negative witness exists.',
         next_step='Prove the nonlocal moment/Schur inequality for every compatible V, or provide an exact compatible negative Jensen map; a new operation must state which ruled-out hypothesis changes and prove its full integral guarantee.',
         review='Output-matrix proof read through common-datum, algebraic no-null-repair, universal tangency, adaptive and dimension scopes. Projection/Burkholder written proofs and all-background moment reduction read; finite searches classified separately.',
         inventory=['positive_branch_failed_search_scope', 'external_paper_not_admitted'],
         failed=[{'attempt': 'Fixed and variable-covector three-wave searches for positive sharp J_r', 'failure_scope': 'Finite floating-point local searches found no negative candidate; precision loss and unbalanced limiting scales prevent a universal or global inference.', 'evidence_ref_ids': ['positive_branch_failed_search_scope']}],
         relations={'material_updates': [{'target': N867, 'scope': 'Adds operation-specific nonlocal projection and positive Burkholder representation obstructions, with the positive sharp QC question still UNKNOWN.', 'relation_status': 'scoped internally proved operation boundary, no QC-status promotion', 'ref_ids': ['scalar_projection_J_counterexample', 'burkholder_contact_obstruction', 'positive_QC_moment_gate']}], 'contrasting_blockers': [{'target': N868, 'scope': 'The new determinant-square argument uses actual negative integrated dissipation; the existing local Peano tangent theorem has its separate density/hypothesis contract. Neither proves non-QC.', 'relation_status': 'distinct scoped operation obstructions', 'ref_ids': ['output_heat_no_null_repair', 'output_heat_adaptive_dimension_scope']}]}),
    card(N875, 'Order-weighted scattering does not identify volume-axis writing; conditional sharp bounds',
         'Conditional moment identification for Fe/Ni chemical-axis proposals, with physical stress writing and same-domain rewrite unacquired.',
         'Under the additive corrected scattering model, M=integral nnT dV, f=traceM and W=integral S^2 nnT dV are distinct targets. Fixed x/y populations of volume1/2 with S=(4/5,2/5), then swapped, have unchanged M and total intensity while normalized intensity contrast changes by6/5. For unrestricted unit axes and supplied0<s<1 with s<=S<=1 plus acquired W and f, the exact identified set is s^2M<=W<=M, traceM=f; spectral atoms of P=(W-s^2M)/(1-s^2),R=(M-W)/(1-s^2) attain every feasible pair. Known finite axis support instead requires the exact m_i,w_i mixture LP. At s=2/5,f=1 the two-arm volume contrasts are[0,21/25] and[-21/25,0], so their difference can be0 despite intensity difference6/5. Without a uniform floor but0<S<=1, fixed-W feasibility additionally requires equal supports; dropping that condition gives joint-pair closure when W varies, not closure of a fixed-W fiber. No retained physical axis write or same-specimen rewrite is acquired.',
         ['Scattering-to-W must be independently validated: additive intensity, absolute scale, angular/satellite integration, structure factors, absorption and contamination controls.',
          'The same included ordered material supplies f, W and a valid local common lower order floor; aggregate published S values do not supply that floor.',
          'Unrestricted support is required for spectral sufficiency; known allowed axes, per-parent masses, indivisible variants and shared-domain coupling require their own constraints.',
          'f>0 is required for Q=M/f; with f=0 normalized texture is undefined.'],
         ['Exact unchanged-domain counterexample separates order intensity from volume orientation even at fixed phase volume and total intensity.',
          'Two PSD matrices P,R prove sharp positive-floor attainability without requiring commutation; diagonal pinching and rational water filling give exact endpoints.',
          'Independent final audit reconstructs the theorem and fixes joint-closure versus fixed-fiber scope; root v4 incorporates the correction.',
          'Nuisance rank/conditioning and angular missing-mass bounds specify which measured channels could supply W; conditional site-label and extraction contraction arguments identify missing physical control.'],
         ['axis_original_hypothesis', 'axis_root_v4', 'axis_final_independent_review', 'axis_independent_vertex_proof_history', 'axis_control_limits', 'axis_measurement_countermodels', 'axis_measurement_acquisition_gates', 'axis_measured_literature_scope', 'axis_competent_comparators'],
         costs='Charge precursor synthesis, gas throughflow versus net inventory, loading at reaction temperature, repeated nitrogen insertion/removal, furnace time, milling/classification/coating if used, rejected fractions, load transfer, beamtime over energies/angles, references/calibration, local-order bounds, registration, damage/mass balance, retention and reset. No acquired full energy, throughput, price, cycle life, yield, spectral condition number or matched advantage is available. The3x3 SDP is post-supplied-information computation.',
         acquisition='Root v4 is a conditional information operation, not an acquired tensor. No raw stress-to-retained-axis response, validated W interface, same-domain rewrite or useful magnet benchmark was acquired. Primary plots and applicant patent reports remain source-attributed evidence; inaccessible fulltext and raw-data limits remain explicit.',
         obstruction='A volume-tensor change can also arise through selective ordering, phase growth/destruction, replacement, grain/particle motion or loss. Label-preserving nitrogen-only cycles cannot change fixed metal-order labels, but reconstructive nitrogen-assisted mobility is outside that no-go. Planar texture does not imply a specified in-plane axis.',
         comparator='Applicant-reported mechanical treatment of N-rich precursor before denitriding, epitaxial oriented NITE islands and direct stress/field-assisted ordering are close established/source-reported comparators. Broad nitrogen-assisted retained texture is not a new capability claim. Film texture, theoretical-density powder magnetic figures and a hypothetical bulk rewrite are not one demonstrated regime.',
         missing='Acquire and validate same-specimen f,W,local order or a common floor, supported-axis model, nuisance conditioning and missing angular mass; then separate same-domain reorientation from population replacement and demonstrate repeated orthogonal retained writes with complete costs.',
         next_step='On the same marked immobilized material, acquire calibrated order/volume-resolved chemical-axis data through x-write, nitrogen removal and y-rewrite, with unloaded chemistry, final-metal load and comparable direct stress/field controls; reject a write explained by order variation, loss/replacement, rigid rotation or contamination.',
         review='Root v4, current20-check receipt, independent final addendum and actual false-positive/identified-set proofs read. Source-attributed evidence and acquisition contracts read; no new experimental validation was performed.',
         paragraphs=['These are complete internal proofs of their conditional information claims. Physical acquisition is a separate open obligation. No technology record or gate is promoted.']),
    card(N876, 'Sharp negative generators: strict individual Jensen gaps and a positive angular subroute',
         'Partial-result route for each fixed sharp negative generator J_r, r<-2, using the pinned universal heat certificate and the internally accepted independent analytic audit with additive clarifications.',
         'The clarified construction and independent analytic audit prove strict positive Jensen gap for every individual nonzero compatible compact/W0^(1,4)/periodic perturbation and every fixed affine B. It proves a pointwise rank-one Bregman bound and a quantitative alpha(r)/3 margin for rank-one-valued gradients. They also prove a positive nonexplicit delta_r for all degree-half homogeneous angular profiles h in W1,4(S1;R2), ruling out the specified logarithmic annular zero-margin construction at B=0; at fixed nonzero B the extension requires normalized profiles or the stated amplitude condition. These do not prove a constant gamma_r>0 uniform over all affine backgrounds and all compatible gradients. No general zero-margin sequence is constructed and no storage transfer is established. Root has accepted these partial analytic results in coordination; final curation and evidence freeze remain root-owned.',
         ['Fixed real r<-2 and exact inherited positive reduced Gram/exact-form certificate.',
          'Strictness concerns each individual perturbation; no quantitative uniformity over a normalized sequence follows.',
          'Angular theorem concerns rho^(1/2)h(theta) and a fixed r; the fixed-B annular extension requires N(h_T)=1, amplitudes bounded away from zero, or the explicit cross-term condition. Arbitrary shrinking amplitudes and growing effective backgrounds are outside the closed subroute.'],
         ['Convex scalar quartic on a rank-one line gives Bregman gap>=J(R)/3>=alpha(r)|R|^4/3.',
          'Eight necessary kernel rows imply analytic zero-density rigidity in the affine-plus-Schwartz and sublinear-growth classes; heat injectivity gives strict individual gaps.',
          'Renormalized degree-half heat identity, rough-data one-sided Fatou and one-dimensional compactness upgrade angular strictness to a nonconstructive angular margin.',
          'Exact affine minimization leaves K(q)-L(q)T M(q)dagger L(q)/4 as the unresolved uniform residual.'],
         ['prior_universal_negative', 'prior_negative_analytic_audit', 'sharp_rank_one_bound', 'sharp_individual_strictness', 'sharp_angular_margin', 'sharp_clarification', 'sharp_independent_analytic_audit', 'sharp_uniform_gate_and_storage_boundary'],
         costs='The angular delta_r is nonexplicit and not shown computable or uniform in r. Exact supporting algebra is checked separately; finite floating-point searches produce only candidate upper ratios, not lower bounds. No numerical storage value, practical solver or runtime/energy advantage follows.',
         acquisition='The inherited universal certificate is supplied, with SHA f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7. The independent analytic audit and root coordination accept strictness/angular compactness with the preserved additive clarification; final scientific curation remains root-owned. No physical information is acquired.',
         obstruction='The main all-affine fourth-order coercivity target remains unresolved. Strict positivity, reduced-Gram definiteness, rank-one exclusion and angular positivity are not substitutes for a global uniform margin; genuinely two-dimensional concentration/oscillation and growing backgrounds remain possible escape mechanisms.',
         comparator='Pinned N867 supplies QC at the sharp negative floor. Its interior H-reserve gives an explicit margin, but H subtraction fails ROC at the sharp floor. N866 requires an actual uniform gradient-energy constant for arbitrary zero-end strip loops; this route does not supply it.',
         missing='The independent analytic audit validates strictness/rough-angular/compactness with the explicit clarification. A uniform lower bound on the affine-minimized residual for every compatible gradient, or an explicit zero-margin rank-two sequence, remains missing.',
         next_step='Prove a quantitative stability estimate for the residual over all B and compatible q, or construct an exact rank-two sequence whose normalized residual tends to zero.',
         review='Construction proof, full additive clarification and completed independent analytic audit read through rank-one, full-affine outer-product rigidity, strictness, angular renormalization/Fatou/compactness and normalized-amplitude scope. Exact reductions support the analytic proof; root has accepted the partial results.',
         internal='partial_internal_proof', inventory=['sharp_supporting_exact_audit', 'prior_same_G_coercivity_scope', 'prior_storage_uniform_input'],
         paragraphs=['The clarified partial results have a completed independent internal analytic audit and root acceptance. Supporting exact checks alone would not prove them. The uniform all-affine target remains open.', 'No bridge from this route to N866 is proposed. The existing same-G improvement and effective endpoint restrictions of N866 remain unchanged.'])
]
cards[0]['topics'] = ['quasiconvexity', 'polyconvexity', 'finite distortion completion', 'compatible heat', 'shear contact']
cards[1]['topics'] = ['quasiconvexity', 'acoustic contact', 'degenerate cubic flatness', 'exact compiler']
cards[2]['topics'] = ['determinant energy', 'output matrix heat', 'compatible gradients', 'scalar projection', 'Burkholder operations']
cards[3]['topics'] = ['FeNi chemical order', 'axis identification', 'moment bounds', 'physical acquisition']
cards[4]['topics'] = ['sharp quasiconvex boundary', 'strict Jensen positivity', 'angular concentration', 'coercivity gate']
cards[4]['conditional_inclusion'] = 'Completed independent analytic audit and additive clarification have been read; root accepted the partial results in coordination. Root still owns final curation and selected-byte freeze. Uniform all-affine coercivity remains unproved.'
cards[4]['missing_artifacts'] = []


def notice(nid, ids, issue, clarification, refs):
    return {'notice_id': 'SN-FX-GCA-' + nid, 'card_ids': ids, 'issue': issue,
            'clarification': clarification, 'ref_ids': refs}


notices = [
    notice('shear-projection-positive-fibre', [N872, N867], 'Projection versus fixed fibre and prior stronger negative theorem',
           'New finite-H completion covers the whole admissible projection, including every r>0 at a sufficient high coefficient. It does not equate individual alpha fibres. The pinned negative-delta sharp theorem already dominates the new nonsharp construction there; QC at sharp r>0 remains UNKNOWN.', ['shear_projection', 'shear_prior_and_positive_export', 'prior_negative_face']),
    notice('ordinary-PC-all-finite-alpha', [N872, N867], 'Ordinary PC obstruction extends past the sharp floor',
           'For r(r+2)!=0 every finite P_(alpha,r) fails ordinary polyconvexity, including arbitrary nonsmooth nonpolynomial convex lifts; C3-flat-through-order3 corrections cannot repair the local support cubic. On q>0 this excludes finite PC completion on the nonzero curved projected boundary while finite QC completion exists. Strict-interior PC and positive sharp QC are not decided.', ['ordinary_pc_all_alpha', 'ordinary_pc_curved_boundary']),
    notice('nonshear-joint-compiler-scope', [N873], 'Contact hypothesis and provenance of generalization',
           'The contact span requires ROC/QC plus the contact equality; equality alone has a counterexample. The nonshear stratum has independent construction and independent audit. The full-space degenerate-flat compiler is a later root/worker joint extension, sufficient only, with supplied lambda and explicit kernel-flatness; it is not independent corroboration or a full projection equivalence.', ['nonshear_independent_audit', 'general_flat_statement', 'general_flat_compiler_scope']),
    notice('operation-boundaries-not-nonQC', [N874, N863, N867, N868], 'Operation obstruction is not a QC counterexample',
           'Actual determinant-square negative integrated dissipation excludes universal integral-null pointwise repair of each nonzero constant homogeneous second-order planar operation. Coercive strong parabolicity adds a common datum and evolution result; C1 autonomous state adaptation has the stated conditional scope. Scalar projection/Burkholder shortcuts have their separate compatible or contact witnesses. Determinant square remains PC/QC, and QC of positive sharp J_r and unrestricted QC/PC of the older exposed FV quartic remain UNKNOWN.', ['output_heat_no_null_repair', 'output_heat_tangency_classification', 'output_heat_adaptive_dimension_scope', 'scalar_projection_J_counterexample', 'burkholder_contact_obstruction']),
    notice('axis-order-volume-interface', [N875], 'Readout does not acquire a physical write',
           'Normalized superlattice intensity generally measures order-squared weighting, not volume-axis Q. The exact unchanged-axis counterexample gives apparent contrast6/5. Root v4 sharp bounds require validated absolute W,f and a common local order floor; spectral attainability assumes unrestricted axes. Fixed-W zero-floor fibers retain equal support and are closed, while dropping support equality describes joint-pair closure with W varying. No stress write, same-domain rewrite or device capability is acquired.', ['axis_root_v4', 'axis_final_independent_review', 'axis_measurement_acquisition_gates']),
    notice('sharp-strictness-not-uniform-coercivity', [N876, N867], 'Pending partial sharp-boundary progress is weaker than the required uniform bound',
           'Strict Jensen and angular-margin claims have a completed independent internal analytic audit with accepted additive clarifications. They prove neither a positive all-affine pure-fourth-order constant nor a zero-margin sequence. Fixed-B angular closure additionally requires normalized profiles or the stated amplitude condition; shrinking amplitudes, growing effective backgrounds and general rank-two multiscale gradients remain open. No sharp-J storage transfer is established; the existing same-G N866 scope is unchanged.', ['sharp_individual_strictness', 'sharp_angular_margin', 'sharp_clarification', 'sharp_independent_analytic_audit', 'sharp_uniform_gate_and_storage_boundary', 'prior_same_G_coercivity_scope']),
    notice('repeated-pulse-identity', [N869], 'Repeated source bytes are not new scientific evidence',
           'All25 current pulse-observable files are byte-identical to prior FW inputs, and all19 embedded old moving-kernel archive members have prior FW identity. The55-file7-group intake is preserved as supplied DATA, including archival prompts. These repeated inputs do not receive a new scientific card and do not independently confirm earlier claims.', ['pulse_identity_and_data_roles']),
    notice('external-paper-not-admitted', [N872, N873, N874], 'No sharp Beurling premise admission',
           'The preliminary external projection/Burkholder/Beurling paper is AUDIT_RECONSTRUCTED_NOT_ADMITTED with premise_admission=false. Its internal reconstruction does not establish community acceptance or causal identity with this workspace. Completion/coercivity constants in this intake use the established nonsharp complex bound sqrt(24); no sharp constant or source attribution is promoted.', ['external_paper_not_admitted', 'shear_heat_analytic', 'nonshear_completion_proof'])
]
notices.append(notice('exact-compiler-parser-v2', [N873], 'Corrected exact-input boundary with retained failure history',
                     'The initial compiler rounded a long JSON decimal before rational conversion. Version2 preserves decimal/scientific tokens exactly and rejects pre-parsed floats, nonfinite values, booleans and invalid reserves. Initial code/receipts and the executed defect remain history. The theorem and stratum artifacts are unchanged. Corrected compiler SHA bb0cea71e048eccac401a91288b17d7ed1ce7d705250d52dfc29addc71d21433 passed76 independent implementation assertions; supplied lambda and reserve precision remain charged.',
                     ['general_flat_parser_correction', 'general_flat_corrected_implementation_audit', 'general_flat_independent_proof_audit']))


def interface(objects, quantifiers, supplied, acquired, access, guarantee, units, costs):
    return dict(zip(['objects', 'regime_and_quantifiers', 'supplied_information', 'acquired_information',
                     'legal_access', 'guarantee', 'units_norm_and_precision', 'costs'],
                    [objects, quantifiers, supplied, acquired, access, guarantee, units, costs]))


def bridge(bid, state, ids, subclaim, destination, src, dst, alignment, missing, falsifier,
           sr, dr, transfer=(), counter=(), forward='', reverse='No converse or broader regime is established.'):
    refs = list(dict.fromkeys([*sr, *dr, *transfer, *counter]))
    return {'id': 'FX_GCA_' + bid, 'state': state, 'cards': ids, 'source_subclaim': subclaim,
            'destination_obligation': destination, 'source_interface': src, 'destination_interface': dst,
            'alignment': alignment, 'missing_lemma': missing, 'falsifier': falsifier,
            'source_ref_ids': sr, 'destination_ref_ids': dr, 'transfer_proof_ref_ids': list(transfer),
            'counterexample_ref_ids': list(counter), 'ref_ids': refs,
            'reciprocity': {'forward': forward or alignment, 'reverse': reverse}}


bridges = [
    bridge('shear_core_plus_minor_jensen', 'PROVEN LOGICAL DEPENDENCY', [N872],
           'For each rho(rho+2)>0 the exact finite core P_(c(rho),rho) is all-background QC; extra H supplies an explicit fourth-power gradient reserve.',
           'A general projected shear triple satisfying delta!=0,gamma>0,6beta gamma-delta^2+delta gamma>=0,2beta+delta>0 needs one finite QC alpha independent of B and phi.',
           interface('P_(alpha,rho) and compatible planar gradients.', 'Each fixed real rho with rho(rho+2)>0; every B, bounded Lipschitz domain and W0^(1,4) test.', 'Exact quartic and universal rational coefficient/form data; sufficient c(rho).', 'No empirical data acquired.', 'Read exact polynomial/certificate and use classical analytic estimates; no optimizer oracle.', 'QC core; margin4(alpha-c(rho))/1875 for alpha>=c(rho).', 'Frobenius |Dphi| and Lebesgue integrals; exact constants, no numerical error promise.', 'Finite rational matrices order<=18 at rational rho; conditioning and coefficient growth paid; no optimality/runtime guarantee.'),
           interface('F=alpha H+beta u^2+gamma j^2+delta uj.', 'Every supplied admissible projected triple; exists a single finite alpha; same all-B/domain/test quantifiers.', 'beta,gamma,delta exactly supplied; p=6beta+delta>0.', 'No added acquired information.', 'Set lambda=delta^2/p,rho=p/delta and check gamma-lambda>=0.', 'F=lambda P_(alpha/lambda,rho)+(gamma-lambda)j^2 is QC; reserve margin4[alpha-lambda c(rho)]/1875.', 'Same matrix, gradient norm, domain and exact arithmetic; no hidden redefinition of alpha.', 'Coefficient reading and exact algebra paid; separate minor Jensen uses no physical service.'),
           'Exact decomposition supplies the destination using a nonnegative determinant-square Jensen channel; it does not require monotonicity of det^2 under the core heat.',
           'None for the stated sufficient projection implication. Least-alpha positive fibres and single-flow inclusion remain unproved.',
           'Any coefficient mismatch, rho outside q>0, negative remainder or failure of the exact core identity invalidates this transfer; the explicit source det^2 heat witness falsifies replacing separate Jensen by universal same-flow monotonicity.',
           ['shear_schur_proof', 'shear_heat_analytic'], ['shear_source_statements', 'shear_projection'], transfer=['shear_projection']),
    bridge('nonshear_to_flat_compiler', 'ESTABLISHED COMPATIBLE INTERFACE', [N873],
           'Strict nonshear parameters give quadratic support lambda=3ell, kerQ=span e11 and cubic flatness; the report supplies a positive transverse kappa and tensor bound.',
           'General degenerate-flat completion requires an exact scalar lambda, PSD Q, T(I,K,K,E)=0, positive kappa off a nonzero kernel and a tensor norm bound.',
           interface('G=k w^2+ell vj+m v^2.', 'k>0,L=ell+2m>0,D=2km-kell-ell^2>0; each fixed triple.', 'Exact coefficients; lambda=3ell, kappa=3LD/[D+3L(2k+L)] and M=4(|k|+|ell|+|m|).', 'No physical data.', 'Differentiate and read the supplied PSD support and cubic identities.', 'Q=(k+L)b^2+2(k+ell)bc+kc^2+3Ld^2; Q>=kappa|(b,c,d)|^2; kernel span e11; T(I,e11,e11,E)=0.', 'Euclidean matrix norm and exact rational/real coefficients; no spectral approximation.', 'Fixed-dimensional derivative and minor checks; rational expressions and input precision charged.'),
           interface('General left-SO(2)-invariant quartic G plus alpha H.', 'Every admitted supplied certificate; every B, bounded planar Lipschitz domain and W0^(1,4) test, plus periodic gradients.', 'Same G, supplied lambda and exact M,kappa fulfilling the general predicate.', 'No additional acquired information.', 'Use the written general Taylor/Young proof and exact compiler admission checks.', 'alpha>=401296M^2/kappa+(9391/4)M suffices; additional nuH gives4nu/1875 gradient margin.', 'Same Frobenius norm, H convention and exact quantitative coefficients.', 'PSD/kernel/flatness arithmetic order<=4; lambda finding is not included; large sufficient alpha is paid.'),
           'The nonshear theorem supplies every hypothesis of the later general compiler exactly. This is a compatible interface and alternative proof route, not independent confirmation or a historical dependence of the original stratum construction.',
           'None for this strict stratum. Necessity of the general predicate and full projected classification remain unproved.',
           'A missed kernel direction or nonzero T(I,Z1,Z2,E) falsifies admission; known QC sharp J_r fails this predicate and falsifies treating it as necessary.',
           ['nonshear_quadratic_and_flatness'], ['general_flat_statement', 'general_flat_compiler_scope'], transfer=['general_flat_proof', 'general_flat_compiler_scope']),
    bridge('order_intensity_to_volume_axis', 'REFUTED TRANSFER', [N875],
           'A validated additive superlattice measurement supplies W=integral S^2nnT dV and normalized order-weighted poles.',
           'The proposal would identify Q=M/f or an x-versus-y volume-axis change from normalized W alone, even at fixed f and total intensity.',
           interface('Order-squared weighted axis moment W.', 'Fixed region, unit axes,0<S<=1; additive corrected integrated scattering model.', 'A hypothetical perfectly calibrated W, same total f and intensity in both arms.', 'No such W was actually acquired in this round.', 'Registered chemical scattering after nuisance/geometry calibration; absent raw response remains a gate.', 'Only the order-weighted moment, not orientation-specific volume and order separately.', 'Tensor normalized by traceW; contrast is D_int, distinct from volume Q.', 'All calibration, angular mass, local-order heterogeneity and instrument costs required; values unknown.'),
           interface('Volume-axis moment M and Q=M/f.', 'Same included material and f>0; desired orientation change rather than only order variation.', 'No independent per-orientation S or common floor assumed by the refuted shortcut.', 'Missing orientation-resolved volume/order, or valid floor plus absolute W,f.', 'Would require an additional measured/justified order/support model and same-domain tracking.', 'A unique or nonzero-separated volume-axis contrast.', 'Volume weighting, not order-squared weighting; undefined when f=0.', 'Acquire extra order/phase data and track same domains; a small SDP after supply does not acquire them.'),
           'Two fixed populations with volumes1/2 and unchanged x/y axes change S from(4/5,2/5) to(2/5,4/5); W contrast changes6/5, M is identical, f and total intensity are unchanged.',
           'Repair needs measured common nonzero order, per-orientation order/volume, or the valid-floor identified-set assumptions with correct support; these are missing acquisition services.',
           'The exact fixed-axis order-swap construction is the executed mathematical falsifier. A genuine rewrite claim additionally fails if its tensor change is explained by ordering, replacement, loss or rigid motion.',
           ['axis_measurement_countermodels'], ['axis_original_hypothesis', 'axis_measurement_acquisition_gates'], counter=['axis_root_v4', 'axis_measurement_countermodels'],
           reverse='Conditional positive-floor bounds are valid after their additional inputs are supplied; they neither acquire W nor certify same-domain reorientation.'),
    bridge('scalar_projection_to_sharp_J_monotonicity', 'REFUTED TRANSFER', [N874, N867],
           'Scalar-potential L2 projection onto a compact convex gradient constraint has the stated integrated gradient pairing and can contract matching convex radial scalar energies.',
           'Apply an independent scalar-component projection to a compatible vector map and assume every sharp J_r,r>0 energy decreases.',
           interface('Scalar periodic potentials and their actual nonlinear constrained L2 projection.', 'Nonempty compact convex K, slope p in K, periodic Lipschitz potential; source paper wider conclusions are not admitted premises.', 'Definition of projection and classical scalar variational inequality; only the locally reconstructed scalar facts are used.', 'No empirical information.', 'Projection in potentials, preserving gradient compatibility; pointwise clipping is not a legal substitute.', 'Integrated scalar pairing and matching radial-convex comparison only.', 'L2 metric on potentials; normalized torus gradient integrals.', 'Infinite-dimensional projection existence is analytic; no efficient finite-bit implementation or convergence rate supplied.'),
           interface('Compatible vector map v=(epsilon phi,psi) and sharp J_r.', 'Every r>0; proposed universal energy monotonicity over smooth periodic vector maps.', 'Same scalar projection applied only to first component, second component fixed.', 'No additional data.', 'Actual K={0} projection to constants; r=1 also has a strictly positive-radius disk witness.', 'Claimed J_r-energy nonincrease, which fails.', 'Same normalized torus energy; both witness energies are positive, not negative Jensen energy.', 'Exact rational/trigonometric witness checks; no solver complexity, hardware or acquisition consequence.'),
           'For every r>0 the exact compatible construction has Eprime_r(0)<0, so projection to constants raises energy; at r=1 every feasible positive-cap output exceeds input by at least52159/16384000.',
           'A coupled vector projection or a different supporting inequality controlling determinant terms is needed; the actual scalar lemma is not refuted.',
           'The saved compatible positive-energy witness already falsifies universal independent-row J_r monotonicity. It does not falsify QC of J_r.',
           ['scalar_projection_J_counterexample', 'external_paper_not_admitted'], ['positive_QC_moment_gate'], counter=['scalar_projection_J_counterexample'])
]


gates = [
    {'gate_id': 'G-FX-GCA-POSITIVE-SHARP-QC', 'card_ids': [N872, N874], 'title': 'Positive sharp all-compatible moment inequality',
     'question': 'Does every positive sharp J_r satisfy the exact moment/Schur PSD condition for every compatible periodic gradient?',
     'pass_condition': 'A readable all-gradient proof with exact r/background/domain quantifiers, or a certified actual compatible negative Jensen perturbation. Finite searches, local heat separation and unconstrained matrix laws do not pass.',
     'ref_ids': ['positive_QC_moment_gate', 'shear_prior_and_positive_export'], 'priority_order': 872},
    {'gate_id': 'G-FX-GCA-FULL-PROJECTED-BOUNDARY', 'card_ids': [N873], 'title': 'Exact full projected boundary beyond the sufficient compiler',
     'question': 'Which full eight-dimensional H-projected invariant quartics have a finite QC completion beyond the supplied-lambda cubic-flat predicate?',
     'pass_condition': 'A proved new boundary theorem or exact compatible obstruction, with supplied lambda/finding cost and kernel-flatness scope. Failure of the present compiler remains unresolved.',
     'ref_ids': ['general_flat_compiler_scope', 'nonshear_necessity_boundaries'], 'priority_order': 873},
    {'gate_id': 'G-FX-GCA-CHANGED-OPERATION', 'card_ids': [N874], 'title': 'A distinct operation with a proved integral guarantee',
     'question': 'Can a changed flow, energy, coupled projection or auxiliary-state operation establish the needed QC inequality outside the proved operation obstructions?',
     'pass_condition': 'State every changed hypothesis, legal compatibility map, analytic existence/differentiation requirement and full integral guarantee. A failed same-operation null/SOS search does not establish this.',
     'ref_ids': ['output_heat_no_null_repair', 'output_heat_adaptive_dimension_scope', 'scalar_projection_J_counterexample', 'burkholder_contact_obstruction'], 'priority_order': 874},
    {'gate_id': 'G-FX-GCA-AXIS-ACQUISITION', 'card_ids': [N875], 'title': 'Acquire calibrated same-domain chemical-axis writing evidence',
     'question': 'Can the same immobilized material undergo controlled retained x-write then y-rewrite, with a volume-axis observation that excludes order weighting and replacement?',
     'pass_condition': 'Acquire validated additive absolute W, f, orientation-resolved order or a common local floor, nuisance conditioning and angular missing-mass bounds; retain raw registered chemical maps, phase/mass balance, load transfer and repeated matched controls. Demonstrate a change beyond uncertainty unexplained by order variation, new/lost domains, rigid rotation or contamination; charge full preparation/reset costs.',
     'ref_ids': ['axis_root_v4', 'axis_measurement_acquisition_gates', 'axis_competent_comparators', 'axis_measured_literature_scope'], 'priority_order': 875},
    {'gate_id': 'G-FX-GCA-SHARP-ANALYTIC-AUDIT', 'card_ids': [N876], 'title': 'Root adjudication of strictness and angular proof',
     'question': 'Does the independent analytic audit validate the exact strictness, rough-data heat/Fatou and compactness arguments in the selected construction bytes?',
     'pass_condition': 'Read and hash the completed independent analytic report, reconcile every correction with retained prior versions, and have root explicitly adjudicate the selected proof scope. Supporting exact reductions alone do not pass.',
     'ref_ids': ['sharp_individual_strictness', 'sharp_angular_margin', 'sharp_supporting_exact_audit'], 'priority_order': 876},
    {'gate_id': 'G-FX-GCA-SHARP-UNIFORM-MARGIN', 'card_ids': [N876], 'title': 'Uniform all-affine pure fourth-order coercivity',
     'question': 'For each fixed r<-2 is the affine-minimized residual bounded below by gamma_r integral|q|^4 with one gamma_r>0 for every compatible q?',
     'pass_condition': 'A quantitative proof controlling all compatible rank-two oscillation/concentration and growing affine backgrounds, or an explicit exact zero-margin sequence. Strictness, angular positivity and finite numerical candidate ratios do not discharge this. No N866 transfer until its full uniform input is actually supplied.',
     'ref_ids': ['sharp_uniform_gate_and_storage_boundary', 'prior_storage_uniform_input'], 'priority_order': 877}
]
# The root-confirmed completed internal audit is evidence, not an open
# internal-completion gate. External review is still generated per card.
gates = [g for g in gates if g['gate_id'] != 'G-FX-GCA-SHARP-ANALYTIC-AUDIT']

curation = {
    'schema': 'astra.fx-curation-input.v1', 'intake_id': 'FX-global-completion-axis-20261015',
    'curation_status': 'DRAFT_PENDING_ROOT_ADJUDICATION', 'curated_by': 'global_round_curation_draft_worker',
    'base_revision': BASE, 'date_version': '2026-10-15', 'reserved_routes': [],
    'tentative_routes': ['N872', 'N873', 'N874', 'N875', 'N876'],
    'route_status': 'UNRESERVED; root must recheck current main and choose final IDs',
    'checkpoint_path': None, 'checkpoint_draft_path': FX + 'CHECKPOINT_RECORD.preservation.v0001.json',
    'selected_freeze': None,
    'draft_dependencies': ['Root final scientific curation; N876 partial analytic results already accepted in root coordination under the final audit and clarification.',
                           'Root selected-byte freeze and preservation of proposed derived mappings.',
                           'Root final route reservation and live-generator validation.'],
    'sources': [{k: v for k, v in src.items() if k != 'payload_kind'} for src in sources.values() if src['local_origin'] == 'R'],
    'evidence': evidence, 'cards': cards, 'notices': notices, 'bridges': bridges, 'gates': gates,
    'boundary': BOUNDARY,
    'non_actions': ['No live W writes.', 'No scientific source edits.', 'No root freeze or scientific adjudication.',
                    'No checkpoint publication.', 'No technology status or gate promotion.', 'No Git/GitHub mutation.',
                    'No external communication.', 'No subagent delegation.']
}

# A selection recommendation is not a selection freeze. Original supplied
# sources remain covered by the separate mandatory all-byte preservation.
candidate_files = []
for (origin, path), src in sources.items():
    if origin != 'R' or path.startswith('sources/'):
        continue
    rec = inputs[(origin, path)]
    candidate_files.append({'research_relative_path': path, 'path': src['path'],
                            'sha256': rec['sha256'], 'bytes': rec['bytes'],
                            'provenance_role': src['provenance_role'], 'payload_kind': src['payload_kind'],
                            'contains_external_fulltext': False, 'contains_external_dataset_or_clone': False,
                            'selection_reason': 'Exact cited proof, counterexample, internal review or scoped receipt in the reviewable scientific draft; root must select/freeze final bytes.'})

# Include replayable authored checks and their completed receipts as optional
# exact audit capital. They are not substituted for the written proofs.
support_files = [
    ('workers/global_completion_reconstruction/reconstruct_global_completion.py', 'root_or_worker_executable_check', 'code'),
    ('workers/global_completion_reconstruction/RECONSTRUCTION_RECEIPT.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/global_completion_reconstruction/verify_no_polyconvex_completion.py', 'root_or_worker_executable_check', 'code'),
    ('workers/global_completion_reconstruction/NONPOLYCONVEX_COMPLETION_RECEIPT.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/global_completion_reconstruction/POSITIVE_R1_COMPLETION.json', 'worker_derivation', 'counterexample'),
    ('workers/global_completion_reconstruction/POSITIVE_R1_EXPORT_RECEIPT.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/full_invariant_genesis/flat_completion_compiler.v0002.py', 'root_or_worker_executable_check', 'code'),
    ('workers/full_invariant_genesis/GENERAL_COMPILER_RECEIPT.v0002.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/full_invariant_genesis/flat_completion_compiler.v0001.py', 'root_or_worker_executable_check', 'code'),
    ('workers/full_invariant_genesis/GENERAL_COMPILER_RECEIPT.v0001.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/full_invariant_genesis/PARSER_CORRECTION_BASELINE.v0001.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/full_invariant_genesis/PARSER_CLI_RECEIPT.v0002.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/general_flat_completion_independent_audit/FINAL_AUDIT_RECEIPT.json', 'same_team_review', 'receipt'),
    ('workers/general_flat_completion_independent_audit/verify.py', 'root_or_worker_executable_check', 'code'),
    ('workers/general_flat_completion_independent_audit/verify_implementation.py', 'root_or_worker_executable_check', 'code'),
    ('workers/general_flat_completion_independent_audit/implementation_verification.json', 'same_team_review', 'receipt'),
    ('workers/general_flat_completion_independent_audit/PRE_CORRECTION_INPUT_FINDING.json', 'same_team_review', 'receipt'),
    ('workers/full_invariant_genesis/verify_theorem.py', 'root_or_worker_executable_check', 'code'),
    ('workers/full_invariant_genesis/EXACT_RECEIPT.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/nonshear_face_independent_audit/verify.py', 'root_or_worker_executable_check', 'code'),
    ('workers/nonshear_face_independent_audit/receipt.json', 'same_team_review', 'receipt'),
    ('workers/output_heat_rank_preservation/verify_output_heat.py', 'root_or_worker_executable_check', 'code'),
    ('workers/output_heat_rank_preservation/RECEIPT.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/positive_branch_new_operation/verify_new_operation.py', 'root_or_worker_executable_check', 'code'),
    ('workers/positive_branch_new_operation/EXACT_VERIFICATION.json', 'root_or_worker_executable_check', 'receipt'),
    ('root/check_order_volume_identification.py', 'root_or_worker_executable_check', 'code'),
    ('root/ORDER_VOLUME_CHECK.json', 'root_or_worker_executable_check', 'receipt'),
    ('root/ORDER_VOLUME_FINAL_SCOPE_CORRECTION.json', 'root_synthesis', 'receipt'),
    ('independent_audits/axis_evidence_adversary_final/check_independent.py', 'root_or_worker_executable_check', 'code'),
    ('independent_audits/axis_evidence_adversary_final/INDEPENDENT_CHECK.json', 'same_team_review', 'receipt'),
    ('independent_audits/axis_evidence_adversary_final/AUDIT_RECEIPT.v0002.json', 'same_team_review', 'receipt'),
    ('workers/axis_evidence_adversary/acquisition_receipts.jsonl', 'acquired_primary_literature_receipt', 'acquisition_pointer'),
    ('workers/axis_evidence_adversary/reading_receipts.json', 'acquired_primary_literature_receipt', 'receipt'),
    ('workers/axis_control_genesis/source_ledger.json', 'acquired_primary_literature_receipt', 'acquisition_pointer'),
    ('workers/sharp_boundary_coercivity/EXACT_REDUCTIONS.py', 'root_or_worker_executable_check', 'code'),
    ('workers/sharp_boundary_coercivity/EXACT_REDUCTIONS.json', 'root_or_worker_executable_check', 'receipt'),
    ('workers/sharp_boundary_coercivity/CLARIFICATION_SHA256_RECEIPT.json', 'worker_derivation', 'receipt'),
    ('workers/global_completion_reconstruction/sharp_strict_audit/check_kernel_and_scaling.py', 'root_or_worker_executable_check', 'code'),
    ('workers/new_source_identity_luna/run_receipt.json', 'same_team_review', 'receipt'),
    ('workers/new_source_identity_luna/file_hash_ledger.tsv', 'same_team_review', 'receipt'),
    ('workers/new_source_identity_luna/prior_identity_ledger.tsv', 'same_team_review', 'receipt'),
    ('workers/projection_claim_audit/CLAIMS.json', 'same_team_review', 'review'),
    ('workers/projection_claim_audit/acquisition_receipts.json', 'acquired_primary_literature_receipt', 'receipt')
]
for path, role, kind in support_files:
    raw = (R / path).read_bytes()
    raw.decode('utf-8')
    rec = {'origin': 'R', 'local_relative_path': path, 'sha256': digest(raw), 'bytes': len(raw),
           'line_count': len(raw.decode('utf-8').splitlines())}
    inputs[('R', path)] = rec
    assert not any(x['research_relative_path'] == path for x in candidate_files)
    candidate_files.append({'research_relative_path': path, 'path': FX + 'package/derived/' + path,
                            'sha256': rec['sha256'], 'bytes': rec['bytes'], 'provenance_role': role,
                            'payload_kind': kind, 'contains_external_fulltext': False,
                            'contains_external_dataset_or_clone': False,
                            'selection_reason': 'Optional authored replay/check or acquisition/provenance receipt associated with cited claims. Integrity only; root must select final evidence.'})

selection = {'schema': 'astra.fx-selected-candidates.v1', 'status': 'DRAFT_RECOMMENDATION_NOT_ROOT_FROZEN',
             'base_revision': BASE, 'research_root': str(R), 'files': candidate_files,
             'total_files': len(candidate_files), 'total_bytes': sum(x['bytes'] for x in candidate_files),
             'excluded': ['Newly acquired third-party PDFs, TeX archives, fulltexts, page images, complete datasets and clones remain in R; preserve authored receipts/pointers only.',
                          'The repeated pulse group receives no new scientific card.',
                          'N876 analytic audit and additive clarification are selected as reviewed candidate bytes; uniform all-affine coercivity and storage transfer remain unproved.'],
             'scope': 'A root selection recommendation, not a root freeze. All55 supplied original files in7 groups have mandatory separate byte preservation.'}

pending = R / 'workers/global_completion_reconstruction/sharp_strict_audit/AUDIT.md'
assert pending.exists()
pending_state = 'FINAL_ANALYTIC_AUDIT_AND_CLARIFICATION_READ_ROOT_ACCEPTED_PARTIAL_RESULTS_UNIFORM_MARGIN_UNPROVED'
review = f'''# Reviewable scientific curation draft v0001

This is a worker draft against `{BASE}`. Root owns scientific adjudication, route reservation, selected-byte freeze and any live application. No checkpoint, technology status, GitHub record or live W scientific artifact was changed. Proposed package paths are mappings for root to preserve; derived bytes are not copied by this worker.

| Tentative route | Exact retained scope | Open boundary |
|---|---|---|
| N872 | Whole finite-H shear projection; universal isotropic sufficient completion; every finite curved completion is ordinary non-PC | Positive sharp QC and full cone unresolved; prior negative sharp theorem remains stronger |
| N873 | Exact nonshear existential projection; independently audited degenerate proof; later joint full-space sufficient flat compiler | Contact alone insufficient; least alpha, general necessity, lambda finding and other angles unresolved |
| N874 | Every nonzero constant homogeneous planar second-order operation has det-squared negative integrated dissipation; scoped adaptive and nonlocal-operation limits | Determinant square stays PC/QC; positive sharp QC remains UNKNOWN |
| N875 | Exact order/volume false-positive and sharp conditional moment bounds, with corrected support/closure scope | No calibrated same-specimen W,f,local order or retained write/rewrite acquired |
| N876 | Rank-one bound, strict individual gaps and nonconstructive fixed-r angular margin, independently internally audited with clarifications | Uniform all-affine margin UNPROVED; fixed-B annuli require normalized/amplitude scope; no storage transfer |

The N872 proof uses a separate nonnegative minor-Jensen channel after the exact core decomposition. It never assumes determinant-square energy is monotone under the same heat flow. The N873 report supplies every hypothesis of the later general compiler, but the compiler construction is a joint extension. A separate general mathematical/implementation audit now passes; it is distinguished from the independent original stratum audit. The exact-input parser defect was corrected in version2, while initial code, receipts and failure remain history. Corrected compiler SHA is `bb0cea71e048eccac401a91288b17d7ed1ce7d705250d52dfc29addc71d21433`, with76 independent assertions passing. Its failure on known QC sharp generators explicitly disproves necessity of its admission predicate.

Four paired contracts are drafted: the exact shear-core/minor-Jensen dependency; the nonshear-to-flat-compiler compatible interface; the refuted order-intensity-to-volume-axis shortcut; and the refuted scalar-projection-to-sharp-J monotonicity shortcut. Each states both input/output domains, quantifiers, supplied/acquired information, norms, costs, losses or missing hypotheses and its exact proof/counterexample spans. There is no N876-to-N866 bridge and no analogy-based external-capital bridge.

The axis theorem uses root v4. Its intervals are `[0,21/25]`, `[-21/25,0]`, difference `[0,42/25]`. Unrestricted spectral atoms establish sufficiency only over unrestricted axes. Fixed supported axes require the stated mixture LP and any per-parent/indivisibility/coupling constraints. At zero lower floor, dropping equal support gives closure of joint `(M,W)` pairs when W varies; fixed-W fibers retain support equality and are already closed. Root's correction receipt and older reviewed bytes are retained as history. The current independent v2 addendum verifies root v4 and all20 corrected checks; no old snapshot defect is presented as unresolved current state.

All25 pulse files are byte-identical to prior FW sources. The55-file7-group intake and archival prompt texts remain DATA; repeated bytes do not get a new scientific card. The external preliminary Burkholder/Beurling paper remains `AUDIT_RECONSTRUCTED_NOT_ADMITTED`, with no premise or sharp-constant promotion. The established complex nonsharp `sqrt(24)` estimate suffices for all constants used here. Newly acquired fulltexts are excluded from the proposed selected authored payload; acquisition and reading receipts retain their access scope.

N876 audit state at build: `{pending_state}`. Its completed independent analytic report and additive clarification have been read, and root has accepted the partial results. The clarification states all eight outer-product equations, uses the full affine gradient, and restricts fixed-B annuli to normalized profiles or the stated amplitude condition. Arbitrarily shrinking amplitudes create a growing effective background and remain outside this subroute. The supporting exact receipt alone proves only algebra. The general all-affine pure-fourth-order coercivity gate remains open. Numerical searches are saved failed construction attempts and candidate upper ratios, not certified lower bounds.

The machine draft contains {len(cards)} tentative cards, {len(notices)} scoped notices, {len(bridges)} paired bridges, {len(gates)} explicit proof/acquisition gates and {len(evidence)} inclusive evidence spans. Every span has a full current SHA256 and actual research-relative or pinned-repository path. `SELECTED_FILES.candidates.v0001.json` recommends exact authored files and receipts; it is not a freeze. `reserved_routes=[]` and `selected_freeze=null` intentionally prevent treating this as root-final input. Generator validation is deferred until root preserves the selected bytes and reserves final routes.

`INTEGRITY_RECEIPT.v0001.json` reports current reference existence, inclusive line validity, hashes and any concurrent change observed during build. It verifies neither mathematical truth nor physical feasibility. External review, historical originality and physical capability remain UNKNOWN.
'''

for obj, keys in [(c, ['proof_refs', 'inventory_refs']) for c in cards]:
    for key in keys:
        assert all(x in evidence for x in obj[key]), (obj['id'], key)
for obj in [*notices, *gates]:
    assert all(x in evidence for x in obj['ref_ids'])
for obj in bridges:
    for key in ['source_ref_ids', 'destination_ref_ids', 'transfer_proof_ref_ids', 'counterexample_ref_ids', 'ref_ids']:
        assert all(x in evidence for x in obj[key]), (obj['id'], key)
    if obj['state'] in {'PROVEN LOGICAL DEPENDENCY', 'ESTABLISHED COMPATIBLE INTERFACE'}:
        assert obj['transfer_proof_ref_ids']
    if obj['state'] == 'REFUTED TRANSFER':
        assert obj['counterexample_ref_ids']
assert not any(N866 in x['cards'] for x in bridges)
assert not any('pulse' in c['id'] for c in cards)

snapshot = {'schema': 'astra.curation-draft-input-snapshot.v1', 'base_revision': BASE,
            'captured_at_utc': datetime.now(timezone.utc).isoformat(), 'inputs': list(inputs.values()),
            'root_analytic_audit_state': pending_state, 'scope': 'Exact draft references; selected files remain under root control.'}
outputs = {
    'INPUT_SNAPSHOT.v0001.json': encode(snapshot),
    'CURATION_INPUT.draft.v0001.json': encode(curation),
    'SELECTED_FILES.candidates.v0001.json': encode(selection),
    'REVIEW.draft.v0001.md': review.encode()
}
for name, raw in outputs.items():
    exclusive(name, raw)

changed = []
for (origin, path), rec in inputs.items():
    raw = ((R if origin == 'R' else W) / path).read_bytes()
    if digest(raw) != rec['sha256'] or len(raw) != rec['bytes']:
        changed.append({'origin': origin, 'path': path, 'before_sha256': rec['sha256'],
                        'after_sha256': digest(raw), 'after_bytes': len(raw)})
for key, ref in evidence.items():
    rec = inputs[(ref['local_origin'], ref['local_relative_path'])]
    assert ref['sha256'] == rec['sha256']
    assert 1 <= ref['lines'][0] <= ref['lines'][1] <= rec['line_count']
head_after = head()
receipt = {'schema': 'astra.curation-draft-integrity-receipt.v1',
           'status': 'PASS_SCOPED_REFERENCE_INTEGRITY' if not changed and head_after == head_before else 'INPUT_CHANGED_REQUIRES_NEW_VERSION',
           'generated_at_utc': datetime.now(timezone.utc).isoformat(),
           'worktree_head_before': head_before, 'worktree_head_after': head_after,
           'input_file_count': len(inputs), 'evidence_reference_count': len(evidence),
           'every_reference_exists': True, 'every_inclusive_span_valid': True,
           'reference_hashes_match_snapshot': True, 'inputs_changed_during_build': changed,
           'outputs': [{'path': 'workers/global_round_curation_draft/' + name, 'sha256': digest(raw), 'bytes': len(raw)} for name, raw in outputs.items()],
           'builder_script': {'path': 'workers/global_round_curation_draft/make_draft_v0001.py', 'sha256': digest(Path(__file__).read_bytes())},
           'tentative_route_count': len(cards), 'scoped_notice_count': len(notices),
           'paired_bridge_count': len(bridges), 'explicit_gate_count': len(gates),
           'selection_candidate_count': len(candidate_files), 'N876_analytic_audit_state': pending_state,
           'generator_validation': 'NOT_RUN: root-selected derived preservation and route reservations pending.',
           'scientific_scripts_executed_by_curation_worker': [],
           'write_scope': str(D), 'other_worker_or_source_edits_performed': False,
           'live_W_or_Git_or_GitHub_mutations_performed': False,
           'scientific_adjudication': 'NOT_PERFORMED; root only',
           'checkpoint_publication': 'NOT_PERFORMED', 'technology_gate_promotion': 'NOT_PERFORMED',
           'boundary': BOUNDARY}
exclusive('INTEGRITY_RECEIPT.v0001.json', encode(receipt))
print(json.dumps({'status': receipt['status'], 'files': list(outputs) + ['INTEGRITY_RECEIPT.v0001.json'],
                  'cards': len(cards), 'evidence': len(evidence), 'selected_candidates': len(candidate_files),
                  'pending': pending_state}, indent=2))
