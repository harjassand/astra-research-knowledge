"""Write owned phase-2 review. No peer mutation, no scripts imported."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name('CROSS_REVIEW.json')
ids = ['c09_s01', 'c09_s02', 'c09_s03', 'c09_l03', 'c09_l06', 'c09_l09']
snapshots = {}
for name in ids:
    p = ROOT / 'outputs/round6/frozen_initials' / name / 'INITIAL.txt'
    snapshots[name] = {'path': str(p.relative_to(ROOT)),
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                       'current_matches_frozen': p.read_bytes() == (ROOT / 'work/cycle6' / name / 'INITIAL.txt').read_bytes()}

rows = [
 dict(origin='c09_l03', claim_id='joint-density-affine-archive',
      exact_claim='Affine bounded-score experiments f_v=1+sum s_i v_i Z_i, ||s||_2<1, and strictly positive C1 score marginals with coordinate log-density derivatives bounded by dimension-independent L admit a finite-label positive codec and hybrid-memory converse. For s_i=a exp(-bi), both leading archive coefficients are ln^2(a/eps)/(4b ln 2) when dimension reaches the cutoff.',
      proof_status='INTERNALLY_CHECKED_CONDITIONAL_THEOREM',
      checked=['Full INITIAL proof, including conditional marginal derivative under other labels, graded-hat centroids, fixed-reference moment distortion, joint entropy and hybrid Holevo bound, and dimension-truncated arithmetic sums.',
               'No coordinate independence is used in the joint-entropy converse. Conditioning on independent seeds preserves the Hilbert-dimension bound; the average MSE suffices by entropy concavity.',
               'Strict positivity and C1 compact-cube densities justify differentiation under the finite integrals. The log-gradient hypothesis is much stronger than Fisher orthogonality.'],
      baseline_overlap={
        'c09_s01':'No posterior-density upper or lower theorem; its generic scale-information counterexample does not imply this codec.',
        'c09_s02':'Both show Fisher geometry alone fails. Sol curve models use singular lower-dimensional posterior supports and affine dimension; Luna supplies a sufficient full-dimensional density condition, a distinct admitted regime.',
        'c09_s03':'Sol frozen INITIAL is a covariance-channel information bound in log scale dT/T, with a supplied diagonal-table certificate. It does not prove a joint-posterior codec.'},
      repairs=['Write both encoder and decoder independence of unknown v in every interface statement.',
               'Keep decoder mu_j=phi_j mu/E_mu phi_j explicitly supplied. No conditional mass, sampler, model discovery or finite-bit continuous-output compiler is acquired in this INITIAL.',
               'The source card M already contains posterior-volume/entropy and smooth positive-kernel principles. Attribute these rather than presenting the leading log-squared order as a newly discovered general principle.'],
      dependencies=['Supplied affine likelihood model, feature maps Z_i, spectrum s_i and tail certificate.', 'Supplied conditional reference sampler mu_j.', 'Standard maximum-entropy distortion and Holevo inequalities; primary literature context Hayashi--Tan and Nayak, not a direct asymptotic transfer.'],
      cost={'archive':'sum_{i<=m} log2(J_i+1) bits, all labels charged', 'encoder':'m feature evaluations plus exact/approximate hat coins, not costed in INITIAL', 'decoder':'UNKNOWN; may be arbitrarily costly for an abstract reference space', 'model_acquisition':'UNKNOWN', 'finite_precision':'UNKNOWN'},
      contribution_score=2,
      score_reason='Reusable conditional nonproduct lemma and explicit converse. It does not close the supplied conditional-sampling gate, so score 3 is unsupported.',
      priority='UNKNOWN; no comprehensive priority clearance'),
 dict(origin='c09_l03', claim_id='bounded-interaction-example',
      exact_claim='Density proportional to exp(lambda sum cyclic z_i^2 z_{i+1}^2), fixed 0<lambda<1, has dimension-independent marginal coordinate log-gradient bound, centered and pairwise-uncorrelated coordinates with uniformly nonzero variance; its score law is nonproduct and full-dimensional.',
      proof_status='INTERNALLY_CHECKED',
      checked=['Full density coordinate derivative is at most 4lambda (using a simple cycle). Marginal differentiation gives a conditional average of the same derivative.', 'Independent sign flips force all first and off-diagonal second moments to zero. Comparing a conditional density to uniform gives variance at least exp(-2lambda)/3.'],
      baseline_overlap={'c09_s01':'No overlap.', 'c09_s02':'Excludes the singular curve interface, instead admitting genuinely dependent full-dimensional features.', 'c09_s03':'No overlap in INITIAL.'},
      repairs=['For cycles of length 1 or 2 specify edge multiplicities or use d>=3. State lambda and the known interaction graph as supplied.', 'Conditional sampling remains open in the abstract theorem; the owned digital Gibbs repair will acquire it in a narrower weak-interaction regime.'],
      dependencies=['Known finite interaction graph and lambda.', 'Standard density differentiation and sign symmetry.'],
      cost={'density_evaluation':'O(number of edges)', 'normalizer':'not supplied or computed', 'decoder':'UNKNOWN in INITIAL', 'full_output':'d coordinates'},
      contribution_score=2, score_reason='Concrete admitted dependent class attached to the reusable lemma, not an acquired algorithm.', priority='UNKNOWN'),
 dict(origin='c09_l06', claim_id='blind-code-risk-hybrid-audit',
      exact_claim='With both encoder and decoder fixed independently of v, per-seed dimension D including all classical blocks, and input-independent shared seeds, uniform averaged TV implies the coordinate posterior-distortion bound E(U(X)-U(Y))^2<=4c0 eps/s. Product reference coordinates allow summing information bounds against ln D.',
      proof_status='INTERNALLY_CHECKED_INTERFACE_AUDIT',
      checked=['Full clipped proper-loss Bregman derivation; F double derivative 2/(s c0) on the posterior interval and regret s(U(X)-U(Y))^2/(4c0).', 'Risk transfer uses one fixed loss and averaged joint-TV accuracy; no per-seed accuracy is smuggled in.', 'Hybrid direct-sum dimension sum_j d_j includes every input-dependent classical record. Shared seeds carry no input information.', 'Conditional quantum entropy subadditivity yields the independent-coordinate random-access sum bound.'],
      baseline_overlap={'c09_s01':'Different subject.', 'c09_s02':'Same blind archive interface and Fisher insufficiency are already present; Luna gives useful quantified risk/hybrid accounting.', 'c09_s03':'Different frozen covariance-channel information interface. Later Sol digital Gaussian codec already states input/output/randomness costs, but is not part of frozen INITIAL.'},
      repairs=['Formalize decoder blindness in the original baseline wording. This fixes an ambiguity, not the intended theorem.', 'Do not turn prior-average accuracy into all binary-pair accuracy. D=1 average/worst Bernoulli example correctly separates them.'],
      dependencies=['work/cycle1/statistical_memory.txt; original same-Fisher construction and positive-hat channel.', 'Standard proper scoring and Holevo architecture, with primary antecedents listed by the worker.'],
      cost={'archive':'all blocks sum_j d_j; D bounded per seed', 'diagnostic':'exact rational J=4,N=16 fixture; no source-data acquisition', 'model_sampler':'UNKNOWN, not newly acquired'},
      contribution_score=1, score_reason='Useful interface repair and exact diagnostic of prior work, not a new posterior acquisition theorem.', priority='BASELINE_AUDIT'),
 dict(origin='c09_l06', claim_id='hat-normalization',
      exact_claim='Periodic and graded positive-hat channels preserve the reference law with the correct factor 1/2 for Lebesgue density on [-1,1]. No normalization defect was found.',
      proof_status='INTERNALLY_CHECKED', checked=['Kernel stochasticity, symmetry and K1=1 follow directly from normalized hats. Script side effects inspected before any owned replay.'],
      baseline_overlap={'c09_s01':'No overlap.', 'c09_s02':'Positive smooth archives already use this established kernel architecture.', 'c09_s03':'The independent digital compander codec uses normalized hats in a different experiment, after INITIAL.'},
      repairs=[], dependencies=['Existing periodic/graded-hat construction.'], cost={'finite_fixture':'small exact arithmetic only; no general sampler validation'},
      contribution_score=1, score_reason='Useful arithmetic audit; no new normalization theorem.', priority='BASELINE_DUPLICATE'),
 dict(origin='c09_l09', claim_id='covariance-heat-plateau',
      exact_claim='For centered compactly supported log-concave mu, P0<=P(mu_s)<=P0+sigma^2 s/(P0-s), 0<s<P0, where mu_s=mu*N(0,sI) and sigma^2=||Cov mu||op.',
      proof_status='REGULAR_TIME_ALGEBRA_CHECKED_GENERAL_ANALYTIC_GATE_UNKNOWN',
      checked=['Full contact proof E<w,Kw><=lambda|Ew|^2 by Bochner and componentwise PI.', 'Dimension-free conditional-mean estimate Ew=E[phi E(X|Y)]/(P_s-s), Cov E(X|Y)<=Cov X.', 'Independent calculation confirms lambda prime=E||Hess phi||^2-lambda^2=-E<w,Kw> for heat generator (1/2)Delta.', 'Integration and zero-time PI convolution bound are correct.'],
      baseline_overlap={'c09_s01':'The source-specific cap-information counterexample already audits the N75 regime and distinguishes its special eigenfunction field from generic PI fields.', 'c09_s02':'Generic information transfer is already refuted with a smooth actual Gaussian channel, stronger than the Luna abstract substitution warnings.', 'c09_s03':'Own INITIAL information upper has weight dT/T, distinct from this plateau and from actual N75 dT/T^2.'},
      repairs=['Do not present the algebra as a full analytic reconstruction: domains, first-eigenspace perturbation, local Lipschitz regularity and limiting approximation remain UNKNOWN here.', 'Complete N75 packet/source-specific assumptions are absent from the supplied U card; source family093 partial text was separately acquired by Sol c09_s01.', 'The hypothetical sigma^2/P0->0 sequence is not constructed.'],
      dependencies=['Supplied N75 summary.', 'Klartag--Putterman heat spectral monotonicity primary publisher DOI 10.5802/afst.1759.', 'Standard spectral perturbation not fully checked.'],
      cost={'analytic':'no acquired field, eigenfunction or sampler', 'numeric':'closed-form diagnostic only', 'full_general_proof':'UNKNOWN'},
      contribution_score=1, score_reason='Useful transparent reconstruction of a supplied lemma; the unverified analytic gate prevents a new audited theorem score.', priority='UNKNOWN'),
 dict(origin='c09_l09', claim_id='PI-LSI-and-affinity-gap',
      exact_claim='Compact truncated-exponential references have bounded PI/covariance but diverging LSI; a rare binary Gaussian-variance channel has average Hellinger O(p) while MI tends to h2(p).',
      proof_status='INTERNALLY_CHECKED_GENERIC_OBSTRUCTIONS',
      checked=['Full normalized exponential-tilt entropy and energy calculation; Dirichlet energy tends to 1/4, entropy grows linearly in truncation length.', 'Threshold classification of N(0,1) versus N(0,M^2) has error tending to zero; the Hellinger mixture bounds have the stated p scale.'],
      baseline_overlap={'c09_s01':'Sol already supplies the stronger exact-profile, exact-weight rare-field MI lower growing log L under heat smoothing and PI/covariance/energy controls.', 'c09_s02':'Sol already supplies an analytic scalar Gaussian covariance-channel counterexample under a continuous heat-smoothed reference, plus the exponential entropy/affinity witness.', 'c09_s03':'Different log-scale covariance upper; the mismatch does not repair source-weight information.'},
      repairs=['Retain binary-prior versus continuous log-concave reference distinction.', 'Do not call these source-specific N75 counterexamples or a KLS contradiction.'], dependencies=['Standard elementary exponential/Gaussian calculations.'],
      cost={'acquisition':'none; explicitly constructed examples', 'finite_diagnostic':'closed-form floating evaluations'},
      contribution_score=0, score_reason='Valid but covered by stronger frozen cluster Sol obstructions.', priority='DUPLICATE_RELATIVE_TO_FROZEN_CLUSTER'),
 dict(origin='c09_l09', claim_id='new-KLS-primary-reset',
      exact_claim='Bizeul--Klartag--Lehec arXiv:2610.05474v1, submitted 4 October 2026, claims the full KLS theorem. If correct, it excludes the hypothetical plateau sequence by applying KLS after fixed small heat time.',
      proof_status='SOURCE_REPORTED_FULL_KLS_UNVERIFIED',
      checked=['Primary abstract, Theorem 1.1, Proposition 7.1 suspension and disclosure inspected. The conditional contradiction P_s>=1 and P_s<=C(sigma^2+s) is valid.', 'The full 32-page proof, cumulant induction and imported Song--Zhang criterion have not been independently validated by this review.'],
      baseline_overlap={'c09_s01':'No current full KLS primary preprint cited in frozen INITIAL.', 'c09_s02':'No full KLS primary preprint audited in frozen INITIAL.', 'c09_s03':'No full KLS primary preprint audited in frozen INITIAL.'},
      repairs=['Current-source reset is a useful retrieval, not a theorem discovered or proved by this team.', 'Owned suspension audit only checks a sharpening conditional on a universal cumulant premise. Keep full KLS status UNKNOWN.'],
      dependencies=['https://arxiv.org/html/2610.05474v1'], cost={'literature':'primary page read', 'whole_proof_validation':'UNKNOWN'},
      contribution_score=1, score_reason='Consequential current-source correction and valid conditional consequence; imported theorem proof remains unverified.', priority='IMPORTED_PRIMARY_PREPRINT')
]

data = {
 'worker_id':'c09_s03', 'phase':'2', 'utc':datetime.now(timezone.utc).isoformat(),
 'exposure':'Authorized after all three Sol INITIALs frozen. No peer writes or in-place script execution.',
 'snapshots':snapshots,
 'proof_review_scope':'Full assigned Luna INITIAL proofs and all three frozen Sol INITIALs read. Numeric fixtures are diagnostics only.',
 'claims':rows,
 'worker_scores':{'c09_l03':2,'c09_l06':1,'c09_l09':1},
 'causal_model_comparison':'NOT_INFERRED; assignment provenance and unequal scope are retained.',
 'own_initial_correction':{'immutable_initial_preserved':True,'weight_mismatch':'Own INITIAL integrates dT/T; actual N75 source integrates dT/T^2. INITIAL theorem remains valid in its stated regime but does not close N75.', 'repair_path':'revisions/PHASE2_INFORMATION_AND_SUSPENSION.txt'},
 'next_attack':'Costed covariance-whitened suspension audit, correct-weight logarithmic-cap information upper, and acquired finite-digital conditional Gibbs decoder for a specified weak-interaction posterior model.'
}
OUT.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'path':str(OUT),'claim_count':len(rows),'scores':data['worker_scores']}))
