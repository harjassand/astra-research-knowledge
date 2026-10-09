"""Build the local append-only research handoff. Does not access or modify GitHub."""
from pathlib import Path
import json, hashlib, shutil

P = Path(__file__).resolve().parent
ASTRA = '8aed7fd74eb14622ed5a0a3635a799374296e32a'
MATH = 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb'
SID = '2026-10-10-mixed-broadcasting-scale-reservoir-8aed7fd'

def put(name, content):
    (P/name).write_text(content, encoding='utf-8')

def jput(name, content):
    put(name, json.dumps(content, indent=2, ensure_ascii=False)+'\n')

entries = [
('00_START_HERE.txt','complete entry-point text','navigation, no mathematical premise'),
('frontier/PRIORITIES.md','substantial returned coordination text; not a full source-proof audit','selection of competing proof gates'),
('web/BQ-reports.txt','complete returned text','new source intake routing'),
('agent/topics/quantum.tsv','topic-route response searched selectively','quantum wrapper discovery'),
('agent/RESEARCH_WORKFLOW.txt','complete returned text','append-only local session/bridge convention'),
('agent/UPSTREAM_ENTRY.txt','complete returned text','upstream-state routes; no external write endpoint identified'),
('agent/templates/SESSION_TEMPLATE.json','complete returned JSON template','local SESSION.json schema'),
('agent/templates/BRIDGE_TEMPLATE.json','complete returned JSON template','local bridge schemas'),
('frontier/review_cards/N525-werner-rank-two-flat-projection-lifting.txt','complete wrapper and card text','all-copy endpoint remains unproved in source'),
('updates/BQ/package/supplied/werner_projection_research/RESEARCH_PROOF.md','decisive Sections 1–5 and substantial diagnostic text read; response tail truncated','rank-two projection reduction; not an imported premise'),
('frontier/review_cards/N529-monotone-boolean-coordinate-selection-counterexample.txt','complete wrapper and card text','auxiliary Boolean selection obstruction, not FEI'),
('frontier/review_cards/N534-pure-family-broadcasting-linear-eb-reconstruction.txt','complete wrapper and card text','pure-family scope contrast only'),
('frontier/review_cards/N368-linear-log-capacity-classicality.txt','wrapper dependency notices and full original card body read; duplicate response tail truncated','bounded-capacity scope contrast only'),
('frontier/review_cards/N371-entropy-comparator-obstructions.txt','complete wrapper and card text','precise surviving entropy-loss gate'),
]
sources=[]
for path,depth,use in entries:
    sources.append({'repository':'harjassand/astra-research-knowledge','commit':ASTRA,
                    'path':path,'url':f'https://github.com/harjassand/astra-research-knowledge/blob/{ASTRA}/{path}',
                    'raw_sha256':None,'read_depth':depth,'role':use,
                    'proof_imported':False})
for path,depth,use in [
('README.md','complete returned text','collection navigation and verification-status caveat'),
('CONTENTS.md','selected text and keyword searches; not the full collection','searched broadcast and entanglement-breaking; no mathematical premise imported')]:
    sources.append({'repository':'openai/math','commit':MATH,'path':path,
                    'url':f'https://github.com/openai/math/blob/{MATH}/{path}',
                    'raw_sha256':None,'read_depth':depth,'role':use,'proof_imported':False})
identified=[
'updates/BQ/package/derived/Research_Report.extracted.txt',
'updates/BC/package/continuation/linear_capacity_probe/LINEAR_LOGARITHMIC_TRADEOFF.md',
'updates/BC/package/continuation/linear_capacity_probe/INDEPENDENT_ADVERSARIAL_AUDIT.md',
'updates/BC/package/continuation/linear_capacity_probe/WEIGHTED_POLAR_AND_SMOOTHING_INDEPENDENT_AUDIT.md',
'updates/BC/package/continuation/linear_capacity_probe/ENTROPY_TREE_OBSTRUCTION.md',
'updates/BC/package/continuation/linear_capacity_probe/ENTROPY_COMPARATOR_LOCAL_TESTS.md',
'updates/BC/package/continuation/entropy_loss_classicalization/POWER_EXPONENT_OBSTRUCTION.md',
'updates/BQ/package/supplied/Independent_Theory_Results_2026-10-09/boolean_split/PROOF.md']
primary=[
('R1','quant-ph/9511010v1','Noncommuting mixed states cannot be broadcast','Primary abstract; exact theorem statement also inspected through R5.'),
('R2','0707.0848v2','No-local-broadcasting theorem for quantum correlations','Primary abstract.'),
('R3','quant-ph/9812016v1','Optimal state estimation for d-dimensional quantum systems','Primary abstract and bibliographic record; the used inequality is reproved locally.'),
('R4','quant-ph/0410207v3','Reexamination of optimal quantum state estimation of pure states','Primary search abstract and metadata only; attempted HTML retrieval failed.'),
('R5','1608.07569v2','Information-theoretic limitations on approximate quantum cloning and broadcasting','Earlier HTML theorem statements and selected passages inspected; final reopen returned cache miss. Not a full proof audit.'),
('R6','1705.06071v2','Approximate broadcasting of quantum correlations','Earlier HTML definitions/asymptotic framework/dimension-dependent approximation inspected; final reopen returned cache miss. Not a full proof audit.'),
('R7','quant-ph/0201041v1','Embezzling Entangled Quantum States','Primary abstract; analogy only, not an imported theorem.')]
jput('SOURCE_REVISIONS.json',{
 'schema':'astra-local-source-ledger/1','session_id':SID,'session_date_local':'2026-10-10',
 'timezone':'Australia/Brisbane','pinned_repositories':[
 {'repository':'harjassand/astra-research-knowledge','commit':ASTRA,'observed_commit_date_utc':'2026-10-09T14:39:01Z'},
 {'repository':'openai/math','commit':MATH,'observed_commit_date_utc':'2026-10-08T05:20:00Z'}],
 'sources_accessed':sources,
 'paths_identified_but_original_proofs_not_read':[{'repository':'harjassand/astra-research-knowledge','commit':ASTRA,'path':p,'raw_sha256':None} for p in identified],
 'primary_literature':[{'id':i,'arxiv_version':v,'title':t,'url':'https://arxiv.org/abs/'+v,'read_depth':r,'raw_sha256':None} for i,v,t,r in primary]+[
 {'id':'R8','title':'Dispensing of quantum information beyond no-broadcasting theorem—is it possible to broadcast anything genuinely quantum?',
 'doi':'10.1088/1751-8121/acbc5b','read_depth':'Publisher HTML introduction, restricted-measurement setting, and conclusions; not a complete proof audit.','raw_sha256':None}],
 'source_bytes_note':'Repository texts were accessed through GitHub connector responses, not downloaded as original byte snapshots. Null raw SHA-256 values are intentional; Git commit pins do not claim independent proof validation.',
 'priority_status':'unknown; targeted primary-literature search is not an exhaustive priority audit',
 'repository_modifications':[]})

put('HANDOFF.md',r'''# Research handoff: maximal instability of approximate no-broadcasting

## Result to preserve

A finite-dimensional mixed-state family can be broadcast to any prescribed finite number of recipients with arbitrarily small uniform marginal half-trace error, while its distance from every common entanglement-breaking reconstruction and every commuting replacement family is arbitrarily close to one. The lower bounds already hold for one fixed finite prior. A corresponding single classical–quantum state is nearly maximally far from every state classical on the broadcast subsystem, while allowing arbitrarily accurate local and bilocal broadcasting.

This is a complete negative answer to a specified dimension-independent trace-distance stability question. **Historical priority, external correctness, formal certification, and a 9–10/10 significance assessment remain unestablished.** It is not an NPT-bound-entanglement or FEI solution. No unverified Astra theorem is used as a proof premise.

Read `RESEARCH_PROOF.md` for the complete theorem, constructive channel, every estimate, finite-prior construction, resource accounting, and precise remaining question.

## Exact mechanism and interfaces

Use a direct sum of symmetric copy spaces, with copy counts m, m², …, m^L and a uniform classical mixture over these levels. A physical channel divides the copies into m equal groups. Each marginal shifts the level distribution down by one, so its half-trace error is exactly 1/L. The optimized broadcasting error is only bounded above by 1/L.

A fixed decoder retains one elementary qudit. Any common measure-and-prepare reconstruction would then estimate an arbitrary d-dimensional pure state from at most m^L copies. The standard bound (k+1)/(k+d), reproved in the manuscript, gives the EB obstruction. A separate all-basis support-projection second-moment argument gives the commuting-family obstruction; EB outputs are not assumed to commute.

Only pure-state moments through degree 2m^L are needed. One finite weighted projective design suffices simultaneously for every comparator channel and every orthonormal basis. The proof gives both a finite convex-hull bound and an explicit algebraic stick-breaking/Gauss–Jacobi/phase cubature.

For binary broadcasting, L ≥ 1, K=2^L, d=4K²:

- constructed broadcasting error = 1/L;
- common EB reconstruction error ≥ 1 − (2K−2+L)/(4LK²);
- commuting-family distance ≥ 1 − 1/K;
- distance of the cq state from all states classical on H ≥ 1 − 1/√K.

These are analytic parameter bounds. The enormous matrices for large L were not instantiated.

## Scope controls that must accompany reuse

The input already contains genuine copies of an unknown elementary pure state, in a classically uncertain copy-number sector. It is not supplied for free from one unknown qudit. The direct-sum dimension, finite alphabet, and preparation costs are large. The output copies are correlated: the global cloning half-trace error is exactly 1−(L−1)/L^m. For L≥2, the marginal is maximally far from being globally idempotent in diamond norm: ||Φ−Φ²||diamond=2.

Both Holevo capacity and actual-prior Holevo loss are computed exactly in the proof and are large. **Do not mark N371 closed. Do not invalidate N368 or N534.** N368 has a bounded-capacity premise; N534 has a pure-family premise. This example violates both relevant restrictions.

## Single remaining question

For a self-compatible channel Φ and an arbitrary finite ensemble E, does δ=χ(E)−χ(ΦE)→0 force one common EB channel with prior-average trace error at most a dimension-independent g(δ)→0? The construction here has δ=[log D_K−log d]/L, which is large. The reservoir construction therefore cannot simply be relabelled as a counterexample to this information-loss version.

## Reproduce the checks

Use the versions in `requirements.txt` or compatible versions. The recorded environment was Python 3.13.5 on Linux. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 python -O verify_construction.py
OPENBLAS_NUM_THREADS=1 python -O verify_finite_design.py
```

Both scripts write their receipts next to themselves. To retain the distributed receipts unchanged, run a copy of the package. Checks use explicit exceptions, not `assert` statements.

`verify_construction.py` completed 112 checks: exact combinatorial identities, exact low-order moments, full-domain channel fixtures, complex family identities, decoder, global-cloning and idempotence negative controls, and rational parameter bounds. `verify_finite_design.py` completed 44 checks: complete finite ensembles, moment matrices, attainable decoded state-estimation fidelity, and finitely many basis fixtures. Maximum floating residuals were below 4.45e−15 and 1.45e−15. The universal quantifiers are proved analytically, not certified by the finite checks. No proof assistant or external referee was used.

## Source revisions and ingestion

Astra was read at `8aed7fd74eb14622ed5a0a3635a799374296e32a`; openai/math at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. `SOURCE_REVISIONS.json` distinguishes complete wrapper reads, selected original-proof reads, and merely identified source paths. No raw-byte source hashes are invented.

At the pinned Astra revision, `00_START_HERE.txt` still routes through topic TSVs and current review wrappers. Its retrieved ingestion aids are static session and bridge templates. `SESSION.json` and the files under `bridges/` use those schemas as a local append-only handoff. **Nothing was written to either repository, no card status was changed, and no historical evidence was overwritten.** A future ingestion should create a new uniquely named record and preserve all earlier sources; it should not silently revise an existing claim.

`AUDIT_LOG.md` records implementation failures and discarded approaches. `history/` preserves earlier diagnostic scripts and receipts, not additional independent validation. `CLAIMS.json` records the logical dependencies and non-implications. `MANIFEST.sha256` hashes this local package, not the external source repositories.
''')

put('AUDIT_LOG.md',r'''# Internal audit and failure log

**Date:** 10 October 2026, Australia/Brisbane. Author-internal work only.

## Mathematical derivation checks

The construction was checked in two representations: regrouping actual tensor powers, and explicit normalized occupation-number isometries. Kraus completeness is verified on the full direct sum; the analysis does not define a nonlinear map only on the promised family. Off-diagonal input blocks are physically dephased.

The EB lower bound is derived by composing an arbitrary EB channel with a fixed physical decoder. It does not restrict the EB channel's measurement, outcome count, prepared states, runtime, or knowledge of the finite family. The prior is fixed before the comparator is selected.

Commuting replacement is treated separately, since measure-and-prepare channels may output noncommuting states. The final support-moment bound sums projection masses over an arbitrary orthonormal basis. The finite prior exactly reproduces the required moment operators, so one ensemble handles all comparators simultaneously.

For the cq consequence, the competing classical state's X marginal is not fixed. The proof explicitly allows arbitrary q_x and controls the changed weights by a classical overlap/Cauchy–Schwarz estimate. This prevents a hidden fixed-prior restriction in the distance-to-classical-state theorem.

## Consequential negative controls

1. The construction is not global cloning. Exact product-target distance is 1−(L−1)/L^m.
2. It is not globally nearly idempotent: a state in sector H_2 gives orthogonal Φ and Φ² outputs, hence diamond defect 2.
3. It has unbounded Holevo capacity and large actual-prior information loss. It cannot be used to close the entropy-loss gate or refute the bounded-capacity theorem.
4. Six Pauli eigenstates reproduce the required low moments in an exact fixture but do not form a fourth-order design. The script includes this failed higher-moment claim as a negative control.
5. At d=2,L=2 the final second-moment commuting upper bound is capped at one and is trivial. Its numerical basis fixtures are checks of an identity/inequality, not evidence of a nontrivial asymptotic separation at those small parameters.

## Implementation failure history

- An early parameter check attempted to construct the integer 2**K at L=100, K=2**100. That process hit a 200-second timeout. It was replaced by an equivalent bit-length comparison. The final second-moment proof eliminates that older high-moment condition altogether.
- A subsequent run completed the numerical work but failed to serialize a NumPy int64 offset to JSON. The offsets were explicitly converted to Python integers.
- The corrected first script passed 96 checks. That version and its receipt are retained under `history/`.
- Explicit global-cloning-distance fixtures were added, producing the final 112-check script.
- The first commuting-family derivation used a higher moment and an ambient-dimension estimate. A later exact block-mass summation improved the bound to a second moment and reduced the required design order from K² to 2K. The earlier 52-check finite-design script and receipt remain under `history/`. The final finite-design script has 44 checks; it tests smaller complete designs appropriate to the stronger proof.
- The final two scripts were executed under `python -O`, with 112 and 44 checks passing. A check count is not a count of independent mathematical validations.

The failed pre-correction draft bytes were not retained; this log records the observed failures without claiming byte-level preservation of those drafts.

## Competing opportunities and discarded computational route

NPT Werner all-copy positivity was examined before concentration on broadcasting. Astra N525 supplies a rank-two witness-to-flat-projection reduction but no universal lower bound. A weight-enumerator linear-programming relaxation was explored in `exploration/werner_enumerator_lp.py`. Its relaxed negativity does not supply a realizable rank-two projector: nonlinear compatibility/decomposability constraints are absent. Large-copy floating runs also exhibited constraint-residual problems. No LP minimum from this exploration is presented as a proof or a physical counterexample, and no raw LP output receipt was preserved.

Astra N529's Boolean coordinate-selection counterexample was inspected as another direction. It refutes the stated auxiliary selection criterion, not FEI. No new Boolean theorem is claimed and the full referenced Boolean proof was not reconstructed in this session.

## Literature and provenance limitations

The standard pure-state estimation inequality is credited and reproved rather than imported from an unread full proof. Exact no-broadcasting, local no-broadcasting, quantitative entropic broadcasting, finite/asymptotic broadcasting, and embezzlement were considered as predecessors. Historical novelty remains unknown; the literature search was targeted, not exhaustive.

Some primary HTML pages were readable earlier in the session but returned cache misses when reopened near completion. Bibliographic and read-depth metadata preserve that distinction. Direct runtime downloading of repository source bytes was unavailable during this session; source Git revisions and connector-read paths are pinned, but raw source SHA-256 fields remain null.

No external peer review, independently authored audit, proof-assistant kernel run, experimental realization, or demonstrated discovery-capability gain occurred.
''')

jput('SESSION.json',{
 '_template':'astra-session/1','session_id':SID,
 'task':{'goal':'Pursue foundational theoretical discovery and deliver the strongest complete result actually achieved.',
         'question':'Can arbitrarily accurate finite-recipient broadcasting imply dimension-independent classical reconstruction for arbitrary mixed families?',
         'scope':'Finite-dimensional full-domain CPTP channels; finite families and fixed finite priors; half-trace distance; no resource or dimension bound.'},
 'source_revision_hashes':[{'repository':'harjassand/astra-research-knowledge','git_commit':ASTRA},{'repository':'openai/math','git_commit':MATH}],
 'sources':[{'id':f'S{i+1:02d}','path':s['path'],'sha256':None,'cards_or_spans':[s['role']],'read_depth':s['read_depth']} for i,s in enumerate(sources)],
 'contract':{'assumptions':['m>=2 finite','L>=1 finite','d>=2 finite','input state supplied on a direct sum of genuine symmetric copy spaces','comparators unrestricted within physical EB or commuting classes'],
             'interface':'Construct H, a finite family/prior, and one full-domain m-output broadcaster; prove uniform and prior-average separation bounds.',
             'costs':{'largest_input_copy_count':'K=m^L','dimension_H':'sum_{r=0}^L binom(d+m^r-1,m^r)',
                      'finite_prior_support_existential_bound':'D_{2K}^2','explicit_cubature_points':'(ceil((2K+1)/2)*(2K+1))^(d-1)',
                      'efficient_preparation_or_comparator_algorithm_claimed':False}},
 'inputs':{'inherited_or_supplied':['Astra current-status wrappers and scoped open gates','classical no-broadcasting/state-estimation predecessors'],
           'acquired':['new explicit scale-reservoir construction','full all-EB and all-basis proofs','finite prior and cq strengthening','112+44 internal checks']},
 'candidate':{'representation':'Uniform classical mixture over logarithmic copy-number sectors; division translates the level distribution.',
              'hypothesis':'Resolved negatively: b_m can tend to zero while common EB and commuting distances tend to their maximal value one.'},
 'missing_lemma':None,
 'comparator':'Every full-domain EB reconstruction; every common commuting replacement family; every cq comparator classical on H, allowing a changed X marginal.',
 'falsifier_or_next_experiment':'External line-by-line review of the block isometry, moment inequality, finite-prior universality, and changed-prior cq estimate; separately investigate the small-Holevo-loss gate.',
 'unresolved_or_UNKNOWN':['independent correctness review','formal certification','historical priority','historic 9–10/10 significance','dimension-independent small-Holevo-loss stability','efficient physical implementation'],
 'status':'reconstructed','allowed_status':['read','reconstructed','reviewed'],
 'status_note':'Complete self-contained argument and author-internal finite checks. This is a progress label, not independent scientific validation.',
 'source_handling':'source=DATA','evidence_refs':['RESEARCH_PROOF.md','verification_receipt.json','finite_design_receipt.json','AUDIT_LOG.md','SOURCE_REVISIONS.json'],
 'append_only':True})

(P/'bridges').mkdir(exist_ok=True)
bridge_data=[
('mixed_family_scope','Theoretical / N534 mixed-family extension',
 'Unrestricted statewise half-trace mixed-family extension is false. This does not refute the source pure-family result.',
 'rank-L flat mixed states; dimension and resource diverge; no unverified positive theorem imported',
 None,
 ['RESEARCH_PROOF.md sections 2–7','verification_receipt.json','finite_design_receipt.json'],
 ['pure-state premise is absent here','historical priority and external verification unknown']),
('entropy_loss_gate','Theoretical / N371 entropy-loss classicalization',
 'Preserve the distinction between trace disturbance and Holevo information loss.',
 'Same finite design prior; exact capacity and loss; delta=(log D_K-log d)/L is large',
 'Prove a dimension-independent prior-average EB modulus from small actual-prior Holevo loss for every self-compatible channel, or construct a counterexample with delta tending to zero.',
 ['RESEARCH_PROOF.md section 9.4'],
 ['N371 is not closed by this counterexample','N368 bounded-capacity premise is not met']),
('physical_resource','Applied / natural-science quantum broadcasting',
 'Test robustness claims against a resource-bounded interface before treating near-redundancy as approximate classicality.',
 'Copies are supplied, not cloned; large Hilbert space; globally correlated outputs; no small global idempotence defect',
 'A resource-bounded, experimentally accessible version would require a new theorem or construction; none is supplied.',
 ['RESEARCH_PROOF.md sections 3, 6, 9'],
 ['no efficient algorithm or practical experiment','no new physical law','no global cloning'])]
for slug,target,goal,assumptions,gate,evidence,unknown in bridge_data:
 jput(f'bridges/{slug}.json',{
  '_template':'astra-bridge/1','from_session':SID,'to_task':target,'goal_and_scope':goal,
  'source_revision_hashes':[{'repository':'harjassand/astra-research-knowledge','git_commit':ASTRA}],
  'evidence_refs':evidence,'inherited_inputs':['source-status distinctions in current Astra wrappers'],
  'acquired_inputs':['self-contained construction and proof in this session'],
  'representation_and_assumptions':assumptions,'exact_missing_lemma':gate,
  'comparator':'Common physical EB map or common diagonal family, not a nonphysical virtual broadcast map.',
  'falsifier_or_next_experiment':'Reconstruct the exact proof under the target branch input/cost contract; do not transfer a conclusion after dropping its assumptions.',
  'unresolved_or_UNKNOWN':unknown,'status':'reconstructed','allowed_status':['read','reconstructed','reviewed'],
  'status_note':'Author-internal proof with finite checks; not external or formal certification.','source_handling':'source=DATA'})

jput('CLAIMS.json',{
 'schema':'local-research-claims/1','status':'complete_argument_author_internal_only',
 'claims':[
 {'id':'A','statement':'Full-domain m-output broadcaster has marginal half-trace error exactly 1/L on the constructed family.','proof':'RESEARCH_PROOF.md section 3','depends_on':[]},
 {'id':'B','statement':'Every common EB map has prior-average reconstruction error >=1-a.','proof':'sections 4 and 7','depends_on':['pure-state moment identity','fixed decoder','reproved state-estimation bound']},
 {'id':'C','statement':'Every commuting replacement has prior-average error >=1-beta.','proof':'sections 5 and 7','depends_on':['support-projection second moment','orthonormal-basis block-mass identity']},
 {'id':'D','statement':'Corresponding finite cq state is >=1-sqrt(beta) from every state classical on H, with no fixed X-marginal restriction.','proof':'sections 6 and 7','depends_on':['C proof moment bound','classical overlap inequality']},
 {'id':'E','statement':'For every epsilon,eta>0 all finite examples in Theorem A exist; maximal-error supremum is one for each positive broadcasting tolerance.','proof':'section 8','depends_on':['A','B','C','D']},
 {'id':'F','statement':'Holevo capacity and actual-prior loss equal formulas (36)–(37), and grow along the displayed sequence.','proof':'section 9.4','depends_on':['moment identity','block entropy formula']}
 ],
 'not_established':['historical novelty','external correctness','formal proof','historic-scale significance','NPT bound entanglement','FEI','small-Holevo-loss instability or stability','bounded-capacity lower law','efficient construction from one unknown qudit','near-global cloning'],
 'external_unverified_theorems_imported':[]})

put('requirements.txt','# Versions used by the recorded internal checks; Python 3.13.5.\nnumpy==2.3.5\nscipy==1.17.0\nsympy==1.14.0\n')
explore = Path('/mnt/data/astra_session/explore_enumerators.py')
if explore.exists():
 (P/'exploration').mkdir(exist_ok=True)
 shutil.copy2(explore,P/'exploration/werner_enumerator_lp.py')
 put('exploration/README.md','''# Discarded exploratory relaxation\n\nThis script probes a relaxed Werner weight-enumerator LP. It omits nonlinear realizability conditions and does not produce physical rank-two witnesses. Large-copy floating outputs had residual problems. No raw output receipt is preserved, and these runs are not part of the 156 final checks. Do not treat relaxed negative objectives as NPT-distillability counterexamples. The main research result does not depend on this script.\n''')

print('Created handoff, source ledger, session, three bridges, claims, audit, requirements, and exploration warning.')
