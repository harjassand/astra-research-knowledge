#!/usr/bin/env python3
"""Generate the scoped FT capital intake from its frozen, hash-pinned package."""
from __future__ import annotations
import hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
UPDATE = ROOT / 'updates/FT-foundational-capability-20261015'
PACKAGE = UPDATE / 'package'
BASE = 'b7cada92d2eb304578be5ed974f1e44b10a89928'
STATUS_BOUNDARY = ('Source claims and internal reviews remain source-derived and unreviewed externally. '
                   'External mathematical correctness and historical priority are UNKNOWN. '
                   'No physical experiment or complete-resource advantage is established. '
                   'Indexing, hashes and deterministic checks establish only their recorded integrity scope.')

def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def jbytes(x) -> bytes: return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def write_json(path: pathlib.Path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(jbytes(obj))
def line_count(path: pathlib.Path) -> int: return len(path.read_text(encoding='utf-8').splitlines())
def source_id(rel: str) -> str: return 'src-FT-' + sha(rel.encode())[:16]
def ref(rel: str, scope: str, *, campaign=True, ref_id=None):
    if campaign:
        p = PACKAGE / rel
        repo_path = 'updates/FT-foundational-capability-20261015/package/' + rel
        sid = source_id(rel)
    else:
        p = ROOT / rel
        repo_path = rel
        sid = None
    b = p.read_bytes()
    r = {'id': ref_id or rel.replace('/','__').replace('.','_').lower(), 'path': repo_path,
         'sha256': sha(b), 'lines': [1, line_count(p)], 'range_scope': scope,
         'read_path': repo_path, 'hash_kind': 'original_utf8_bytes',
         'status': 'Exact bytes at the frozen source pin; source-reported/internal status retained; external correctness and priority UNKNOWN.'}
    if sid: r['source_id'] = sid
    r['source_revision'] = None
    return r

def append_jsonl(path: pathlib.Path, rows, key):
    old = path.read_bytes() if path.exists() else b''
    if old and not old.endswith(b'\n'): raise ValueError(f'refusing non-newline append: {path}')
    current = [json.loads(x) for x in old.decode().splitlines() if x.strip()]
    have = {x[key]: x for x in current}
    add = []
    for row in rows:
        if row[key] in have:
            if have[row[key]] != row: raise ValueError(f'identifier collision: {row[key]} in {path}')
        else: add.append(row)
    if add:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(old + b''.join((json.dumps(x, ensure_ascii=False)+'\n').encode() for x in add))

def card_text(cid, title, body, evidence, shared_context=()):
    ev = '\n'.join(f'- `{r["path"]}` (sha256 `{r["sha256"]}`): {r["range_scope"]}' for r in evidence)
    context = ''
    if shared_context:
        context = ('\n\nShared negative context (available evidence only; not premises of this card\'s theorem)\n'
                   + '\n'.join(f'- `{r["path"]}` (sha256 `{r["sha256"]}`): {r["range_scope"]}' for r in shared_context))
    footer = ('No physical demonstration of the proposed coupler-inclusive monitor is preserved; '
              'established SWS and transmon experiments remain prior evidence.' if cid.startswith('N847') else
              'No new physical demonstration or complete-resource advantage is established.')
    return (f'{cid} | {title}\n'
            'Status: source_derived_unreviewed. Mission status: NOT_ACHIEVED.\n\n'
            f'{body}\n\n'
            'External mathematical correctness and historical priority remain UNKNOWN. '
            f'{footer} '
            'The cited internal checks establish only their recorded bounded scope.\n\n'
            f'Evidence\n{ev}{context}\n').encode()

records = [
 {'id':'N843-finite-horizon-irrational-phase-state-complexity',
  'title':'Sharp finite-horizon stochastic memory law for a fixed irrational phase',
  'topics':['stochastic processes','automata','quantum information','complexity'],
  'evidence_paths':['workers/foundational_math/PHASE_CLOCK_THEOREM.md','workers/foundational_math/audit/AUDIT.md','root/INDEPENDENT_REVIEW.md','root/REPLAY_RECEIPTS.json','REPORT.md'],
  'proof_paths':['workers/foundational_math/PHASE_CLOCK_THEOREM.md','workers/foundational_math/audit/AUDIT.md'],
  'proof_class':'proof_text_located_not_completeness_audited',
  'internal':'The theorem source, separate same-team audit and root reconstruction are preserved. Root replayed the bounded phase diagnostic. None is formal or external certification.',
  'scope':'For the same fixed irrational phase alpha=(sqrt(5)-1)/2 throughout, p_k=(1+cos(2 pi alpha k))/2, arbitrary homogeneous n-state stochastic P, initial distribution mu and terminal readout f in [0,1]^n, with identical wait commands and one terminal read, N_alpha(T,epsilon)=Theta_(alpha,epsilon)(T^(1/3)) for each fixed 0<epsilon<1/4. The terminal readout receives only the evolved state and is not additionally handed k or an external lookup table. At zero error separately T<=N_alpha(T,0)<=T+1; an ideal qubit realizes the probabilities. This is not a runtime, physical clock, joint-output-process, or practical computing advantage. An ordinary counter/cosine uses O(log T) bits and phase/gate precision is O(log(T/epsilon)).',
  'status':'Source reports an internally proved state law only for each fixed 0<epsilon<1/4, with one fixed phase and no extra k/lookup input to terminal readout, plus a separate exact-error boundary; root reconstructed both and an independent same-team audit is preserved. External proof, formalization and novelty review remain open.',
  'gate_review':'Independently review the exact finite-horizon quantifiers, stochastic resolvent/Fourier lower bound, cyclic-shift construction, zero-error Cayley–Hamilton argument and nearest positive-realization/automata prior art.',
  'gate_cap':'Establish a costed, task-matched application only if a physical or computational implementation can exploit the state law after charging precision, calibration, preparation, reset, readout and an ordinary counter/cosine baseline.',
  'body':'''For one fixed computable irrational phase alpha=(sqrt(5)-1)/2, kept the same throughout the horizon, and terminal probabilities p_k=(1+cos(2 pi alpha k))/2, the preserved result concerns the minimum number of states in an arbitrary homogeneous stochastic model that approximates every terminal probability through horizon T at one fixed positive error 0<epsilon<1/4. The model receives the same wait command at each step and one terminal read; that readout receives only the evolved state and is not additionally handed k or an external lookup table. The source gives matching Theta(T^(1/3)) bounds. At exactly zero error the source gives T<=N_alpha(T,0)<=T+1 by a separate argument. An ideal qubit produces the probabilities exactly by repeated rotation and one final measurement.\n\nThe lower-bound mechanism uses stochastic positivity to control an approximate unit-modulus eigenvector, force an approximate phase return, and combine a resolvent estimate with a finite Fourier witness and the Diophantine return bound. The upper construction mixes two cyclic shifts at a continued-fraction denominator. The independent same-team audit and root reconstruction are preserved as distinct evidence.'''
 },
 {'id':'N844-finite-abelian-subgroup-sampler-and-implementation-boundaries',
  'title':'Conditional subgroup-query bound with cyclic-ring prototype and no measured speedup',
  'topics':['algorithms','probability','finite groups','sampling','complexity'],
  'evidence_paths':['workers/capital_routes/N610_AUDIT.md','workers/abelian_sampler_audit/INDEPENDENT_DERIVATION.md','workers/abelian_sampler_audit/REPORT.md','workers/capital_routes/n610_ring_sampler.py','root/HNF_REPLAY_RECEIPT.json','root/REPLAY_RECEIPTS.json','REPORT.md'],
  'proof_paths':['workers/capital_routes/N610_AUDIT.md','workers/abelian_sampler_audit/INDEPENDENT_DERIVATION.md'],
  'proof_class':'proof_text_located_not_completeness_audited',
  'internal':'The conditional derivation and independent audit are preserved; exact finite conditional distributions and HNF memberships were checked; root replayed the final sampler and benchmark. The prototype code hash is 6c164a5b0f75236d04735b26df828ff4fb20d1311f55d0d459d7a6fb5a390286. This is not an arbitrary-finite-abelian implementation or a performance proof.',
  'scope':'Preserve the expected subgroup-image bound under strict triangular layers and the stated shared-category/uniform-mask independence premise, plus the exact HNF/local callable prototype for cyclic Z/MZ. The implementation is cyclic only. N610 base-p digit inclusion is proved for prime-power moduli only; mixed-prime CRT needs joint categories and cross-component forcing, and generic finite-group access does not establish polynomial bit cost. In the matched root 3,000-draw Z/4 run, subgroup HNF used 5.760 fresh events and 3.195 s versus 7.013 events and 0.405 s for the digit incumbent. Fewer random events did not win on total measured time. No new output class or practical advantage is established.',
  'status':'Source-derived conditional theorem/implementation claim with independent internal audit and bounded root replay. Prime-power-only N610 inclusion and the mixed-CRT gap are explicit. External correctness, priority, generalized implementation and practical advantage remain open.',
  'gate_review':'Independently review the subgroup-growth induction, conditional independence of shared categories, HNF membership/sampling argument, expected-cost accounting and prior art.',
  'gate_cap':'Implement and measure complete acquisition/address/descriptor and arithmetic costs for general finite abelian groups. Compare prime powers with the optimized digit sampler and mixed-prime cases with a joint-CRT model preserving shared categories and cross-component forcing; do not infer speedup from event counts alone.',
  'body':'''For a finite abelian group G, strict triangular layer depth c, parent bound k, m requested coordinates and Haar-reset probability s, the source derives E Q <= (lambda(G)m/s) sum_{j=0}^{c-1}(1+lambda(G)kc^2/s)^j with lambda(G)=Omega(|G|), under its uniform-mask containment and independence conditions. This is an expected fresh-category bound, not a finite worst-case runtime guarantee. Acquisition, address, circuit and subgroup-bit costs remain charged.\n\nThe executable prototype is an exact HNF/local callable sampler for cyclic Z/MZ. It does not establish a general finite-abelian implementation. For prime powers, base-p digit layers already embed the output class into N610. For mixed-prime CRT, independent component runs are not justified when forcing couples components; joint category and cross-component forcing must be preserved. In the matched root replay, fewer fresh events did not offset HNF overhead. No new output class or practical advantage follows.'''
 },
 {'id':'N845-event-conditioned-isotope-renewal-with-unclosed-physical-gates',
  'title':'Event-conditioned isotope renewal in an ideal model with decisive physical gates open',
  'topics':['materials','isotopes','manufacturing','physics','acquisition'],
  'evidence_paths':['root/ISOTOPE_RENEWAL_OPERATION.md','workers/model_challenger/ISOTOPE_BOUND_AUDIT.md','workers/physical_path/DECISIVE_EXPERIMENT.md','workers/physical_path/REPORT.md','workers/physical_path/SOURCE_FILE_RECEIPTS.json','root/REPLAY_RECEIPTS.json','REPORT.md'],
  'proof_paths':['root/ISOTOPE_RENEWAL_OPERATION.md','workers/model_challenger/ISOTOPE_BOUND_AUDIT.md'],
  'proof_class':'proof_text_located_not_completeness_audited',
  'internal':'Root derived the fixed-dose bound and ideal event-conditioned renewal; an independent targeted audit and counterexample are preserved; the bounded model calculation was replayed. No laboratory experiment or same-atom event/reset demonstration occurred.',
  'scope':'At fixed deterministic cumulative fluence per attempted site and unconditioned occupied output, the blind writer has q*=p sigma_L/[p sigma_L+(1-p)sigma_H], while vacancy-history stopping is informative and outside that quantifier. In the ideal renewal, irradiate one fresh atom until ejection or screening fluence d; an ejection triggers independent fresh refill/restart, while a complete survivor is accepted and protected. Then q(d)=p exp(-sigma_H d)/[p exp(-sigma_H d)+(1-p)exp(-sigma_L d)]. At planning p=.01109 and central 95 kV cross sections sigma_L=56.6 mb and sigma_H=2.1 mb, the nominal 90% calculation gives EXPECTED costs of about 105 attempts, 104 refills and 1.959e13 target electrons/nm^2. Retry and dose tails are unbounded; finite caps reduce yield. These are conditional expectations at those inputs, not a general 90% cost. 0.298 J/nm^2 is incident kinetic energy per uniformly addressed area, not absorbed heat, per-site energy or wall-plug cost. Same-atom no-ejection record, independent fresh refill/composition, preserved repaired-site rates, neighbor protection, event/reset and final readout are unacquired.',
  'status':'Conditional internal mathematical/model construction only. The nominal 90% values are expectations at planning p=.01109 and central 95 kV cross sections sigma_L=56.6 mb, sigma_H=2.1 mb; retry/dose tails are unbounded and finite caps reduce yield. They are not a general 90% cost. The blind-dose theorem does not cover outcome-dependent stopping. Same-atom event/reset/protection and material response are not demonstrated; no experiment was performed.',
  'gate_review':'Independently review the fixed-dose quantifiers, renewal composition formula, stopping/reset assumptions, uncertainty treatment and CVD/post-growth isotope prior art.',
  'gate_cap':'In one frozen process acquire a same-atom no-ejection record despite between-frame refill, independent fresh reset and known incorporated composition, same post-repair rates, neighbor-damage/beam-tail control, accepted-site protection and source-labelled final isotope readout before any blinded renewal trial. Report the nominal 90% arithmetic only as expected cost at planning p=.01109 and central 95 kV sigma_L=56.6 mb, sigma_H=2.1 mb; include unbounded retry/dose tails and the yield loss under finite caps.',
  'body':'''The corrected blind fixed-dose result assumes one deterministic common cumulative fluence at each attempted site and unconditioned occupied output. It gives q*=p sigma_L/[p sigma_L+(1-p)sigma_H], while allowing vacancy-dependent refill timing. An independent bounded-adaptive counterexample shows why that bound cannot be extended to outcome-dependent stopping.\n\nThe ideal renewal operation screens one fresh atom to fluence d and observes either ejection or survival. Ejection triggers fresh refill and restart; a survivor is accepted and protected. Under the stated independent refill and fixed local-rate model, accepted heavy composition is q(d)=p exp(-sigma_H d)/[p exp(-sigma_H d)+(1-p)exp(-sigma_L d)]. At planning p=.01109 and central 95 kV cross sections sigma_L=56.6 mb and sigma_H=2.1 mb, the nominal 90% calculation gives EXPECTED costs of about 105 attempts, 104 refills and 1.959e13 target electrons/nm^2. Retry and dose tails are unbounded; finite caps reduce yield. These are conditional expectations at those inputs, not a general 90% cost. The 0.298 J/nm^2 value is incident kinetic energy per addressed area. The same-atom event, reset, repaired-site rate and protection interfaces are not jointly obtained. CVD/post-growth isotope methods remain substantial incumbents.'''
 },
 {'id':'N846-optical-loss-attribution-and-saturable-bucket-boundary',
  'title':'Optical loss flags do not identify target absorption; focusing result is conditional',
  'topics':['optics','measurement','control','identifiability','physics'],
  'evidence_paths':['workers/scientific_operation/REPORT.md','workers/scientific_operation/literature_audit/REPORT.md','workers/scientific_operation/verify_operation.py','workers/scientific_operation/verification_results.json','root/REPLAY_RECEIPTS.json','REPORT.md'],
  'proof_paths':['workers/scientific_operation/REPORT.md'],
  'proof_class':'proof_text_located_not_completeness_audited',
  'internal':'The source report contains the operational indistinguishability argument, passive-resonator counterexample and conditional two-power theorem. Its synthetic verifier passed and root replayed it. No optical experiment was run.',
  'scope':'Two passive systems can have identical accessible scattering and total-loss flags but exchange target/parasitic sink labels, so even adaptive external control cannot infer the hidden sink from that interface. A passive one-port resonator can reduce total loss while a new target sink absorbs positive energy. The positive finite-power saturable-bucket theorem is stated for 0<a<b and requires (ab)^(1/3)(a^(1/3)+b^(1/3))<=1, along with fixed delivered target-plane power, full complex control, complete energy collection, a qualified single-pass homogeneous saturable absorber, acquired response and reset. Nonlinear bucket and iTRAN methods are strong incumbents; no new demonstrated capability or practical advantage follows.',
  'status':'Conditional model theorem and counterexamples with bounded simulation only. The positive finite-power theorem assumes 0<a<b and (ab)^(1/3)(a^(1/3)+b^(1/3))<=1. Physical response, delivery, detector closure and matched experiment are unacquired. Priority and complete-resource advantage UNKNOWN.',
  'gate_review':'Independently review the accessible-instrument indistinguishability proof, resonator falsifier, and the finite-power convexity premise 0<a<b with (ab)^(1/3)(a^(1/3)+b^(1/3))<=1, plus the exact comparison with nonlinear-bucket/iTRAN prior art.',
  'gate_cap':'Qualify one stable diffuser/absorber specimen with measured response and recovery, fixed target-plane delivery, complete outgoing-energy collection, common linear detector response and held-out target-concentration validation. Test the positive finite-power theorem only for 0<a<b and (ab)^(1/3)(a^(1/3)+b^(1/3))<=1, then compare at equal total acquisition and exposure cost against nonlinear-bucket/iTRAN and transmission-matrix baselines.',
  'body':'''A total photon-loss flag measures extinction from the accessible interface. It does not reveal which unobserved internal sink received the energy. The source gives two target/parasitic sink assignments with the same accessible passive instrument, including under adaptive external control, and a one-port resonator counterexample in which total loss falls while a target absorber takes positive power.\n\nA separate positive two-finite-power construction is conditional: it assumes 0<a<b and (ab)^(1/3)(a^(1/3)+b^(1/3))<=1. After a fixed unitary target-plane map, a thin homogeneous saturable mask with acquired response and complete collection yields a convex loss deficit whose ideal full-control maximum concentrates delivered power into one mode. Variable delivery, phase-only control, powers outside the convexity condition, incomplete collection and response history invalidate broader interpretations. Existing nonlinear-bucket focusing and iTRAN are strong comparators. Only synthetic model checks were run.'''
 },
 {'id':'N847-dual-rail-erasure-monitor-prior-art-boundary',
  'title':'Dual-rail erasure monitoring proposal bounded by existing SWS and delayed-check results',
  'topics':['quantum information','error correction','measurement','erasure','hardware'],
  'evidence_paths':['workers/model_challenger/REPORT.md','workers/model_challenger/CANDIDATE.md','workers/foundational_math/REPORT.md','REPORT.md'],
  'proof_paths':[],
  'proof_class':'cited_source_inventory_available_proof_scope_unclassified',
  'internal':'Source-reported experimental literature and a proposed monitor design are preserved. The idea is bounded against reported delayed checks and a different-platform continuous-monitor result. No monitor experiment or new decoding capability was demonstrated.',
  'scope':'Dual-rail loss provides a known erasure sector, and the 2026 cavity SWS CZ is positive prior evidence. Loss during its coupler-target cross-Kerr can leave a correlated unknown partial phase even when a final erasure flag is known. The proposed coupler-inclusive monitor requires about an 8 ns event-time uncertainty for a stated small-angle phase-error budget whose infidelity contribution is quadratic in residual phase; the cited continuous-monitor experiment used a much longer integration window on a different transmon platform and does not demonstrate that timing for the SWS cavity path. Which-path dephasing, monitor-induced loss/backaction, full-circuit performance and matched cost remain open. Credit primary experimental authors; no new capability or quantum advantage is claimed.',
  'status':'Literature-grounded design screen and prior-art boundary. Published SWS and delayed-check results are established evidence distinct from the proposed cavity-path monitor. No physical demonstration of the proposed coupler-inclusive monitor, external review or practical advantage is claimed.',
  'gate_review':'Check the primary SWS, delayed-check and continuous-monitor source versions and the exact measured versus proposed platform, timing, flag/phase and error claims. Verify that the approximately 8 ns value is a derived small-angle phase-error budget whose infidelity contribution is quadratic in residual phase, not measured monitor resolution.',
  'gate_cap':'On the same SWS cavity path measure event-time posterior width against the derived small-angle phase-error budget with quadratic infidelity, missed/false flags, rail/coupler indistinguishability, added loss and correlated target phase; then compare full-circuit survival and decoding against the published delayed-check baseline at matched hardware and exposure cost.',
  'body':'''The preserved dual-rail proposal adds a continuous occupancy monitor to the temporary coupler rail during the SWS cavity controlled-Z gate. The source report states that loss during the cross-Kerr interaction leaves the target with an unknown partial controlled phase before the final erasure flag. A delayed flag alone does not identify the accumulated phase.\n\nThe approximately 8 ns timestamp target is a small-angle phase-error budget derived from the interaction rate and a target error threshold; the corresponding average gate infidelity is quadratic in the residual phase, not a first-order infidelity budget. It is not an observed monitor resolution. The cited continuous-monitor result is on a transmon dual-rail device and uses an integration window far longer than this target; it does not demonstrate timing correction on the cavity SWS path. Published delayed checks are a strong same-task comparator. Which-path information, monitor loss/backaction and full-circuit matched costs remain decisive gates. Primary experimental credit stays with the authors of the underlying experiments.'''
 }
]

def scoped_dependencies(cid: str):
    if cid.startswith('N843'):
        return [{'id':'N545-full-unitary-finite-horizon-markov-state-law','relation':'distinct_task_contract_only'}]
    if cid.startswith('N844'):
        return [{'id':'N610-rank-absorbing-stratified-exact-local-stationary-sampling','relation':'prime_power_comparison_and_mixed_prime_scope_boundary'}]
    if cid.startswith('N845'):
        return [{'id':'N792-covalent-isotope-fractionation-and-mixed-hazard-screen','relation':'distinct_process_and_access_model_only'}]
    return []

# Frozen source manifest and source-to-destination evidence mapping.
source_manifest_bytes = (PACKAGE/'SOURCE_MANIFEST.json').read_bytes()
source_manifest_hash = sha(source_manifest_bytes)
expected_hash = '1b953dbf369b7daec492037ab07086a52b881f3d27fd4caca75e28624fb4262b'
if source_manifest_hash != expected_hash: raise ValueError('frozen source manifest hash mismatch')
sm = json.loads(source_manifest_bytes)
if len(sm['files']) != 78 or sum(x['bytes'] for x in sm['files']) != 391572: raise ValueError('frozen source manifest count/bytes mismatch')
source_entries=[]
for x in sm['files']:
    source_entries.append({'source_path':x['path'],'preserved_path':'updates/FT-foundational-capability-20261015/package/'+x['path'],
                           'bytes':x['bytes'],'sha256':x['sha256'],'provenance':'Copied byte-identically from the frozen authored campaign manifest; the source claim status is preserved, not upgraded.'})
manifest_file = {'source_path':'SOURCE_MANIFEST.json','preserved_path':'updates/FT-foundational-capability-20261015/package/SOURCE_MANIFEST.json',
                 'bytes':len(source_manifest_bytes),'sha256':source_manifest_hash,
                 'provenance':'Exact campaign manifest copied as a 79th item; it declares the other 78 files.'}
source_entries.append(manifest_file)
write_json(UPDATE/'SOURCE_MANIFEST.json', {'schema':'astra.capital-preservation-source-manifest.v1','intake_id':'FT','source_handling':'source=DATA; exact frozen bytes retained',
 'campaign_source_root':sm['source_root'],'campaign_manifest_source_path':'research/2026-10-15-foundational-capability-v1/SOURCE_MANIFEST.json',
 'campaign_manifest_sha256':source_manifest_hash,'declared_file_count':78,'declared_bytes':391572,'copied_item_count':79,
 'files':source_entries,'exclusions':'No unlisted source files, raw third-party papers/data/images, or __pycache__ were copied.'})

# Build cards, typed evidence records, status sidecars and open gates.
all_refs={}
status_rows=[]; claim_rows=[]; catalog_add=[]; graph_nodes=[]; graph_edges=[]; gates=[]; cards_for_notice=[]
for i,r in enumerate(records,843):
    cid=r['id']; stem=cid; card_path='cards/'+cid+'.txt'
    evid=[ref(p, 'Whole source file preserved for this scoped claim; finer subclaim completeness is not asserted.') for p in r['evidence_paths']]
    located=[ref(p, 'Located source derivation/audit for the exact scoped statement; external completeness/correctness remain open.') for p in r['proof_paths']]
    shared_context=[]
    if cid.startswith('N843'):
        shared_context=[
          ref('workers/foundational_math/RANK_COLLAPSE.md','Shared rank-collapse negative/boundary evidence only; not a premise or evidence for the N843 phase-clock theorem.'),
          ref('workers/foundational_math/HIDDEN_SPECTRUM_COUNTEREXAMPLE.md','Shared hidden-transfer-spectrum counterexample and hypotheses boundary only; not a premise or evidence for the N843 phase-clock theorem.'),
          ref('root/REPLAY_RECEIPTS.json','Shared replay receipt for scoped negative checks only; not a premise or evidence for the N843 phase-clock theorem.',ref_id='root__replay_receipts_json__shared_negative_context')]
    for x in evid+located+shared_context: all_refs[x['source_id']]=x
    text=card_text(cid,r['title'],r['body'],evid,shared_context)
    cardfile=ROOT/card_path; cardfile.parent.mkdir(parents=True,exist_ok=True)
    if cardfile.exists() and cardfile.read_bytes()!=text: raise ValueError('card path collision '+card_path)
    cardfile.write_bytes(text); ch=sha(text)
    root_report=next(x for x in evid if x['path'].endswith('/package/REPORT.md'))
    status={
      'schema_version':1,'card_id':cid,'card_path':card_path,'card_sha256':ch,'title':r['title'],'topics':r['topics'],
      'claim_status':'source_derived_unreviewed','reported_status':r['status'],'status_authority':'Frozen FT source manifest plus its authored claim/review records and root synthesis; integration preserves rather than certifies the claim.',
      'proof_availability':{'classification':r['proof_class'],'classification_scope':'Frozen cited version and named internal evidence only; no exhaustive external proof, priority, or capability audit.','located_proof_sources':located,'available_evidence_sources':evid+shared_context,'shared_negative_context_sources':shared_context,'unavailable_or_unclassified':'External proof correctness and historical priority remain UNKNOWN; physical capability and complete-resource advantage are not established.','route_label':'FROZEN SOURCE AND INTERNAL REVIEW ROUTES'},
      'validation':{'internal':r['internal'],'external_correctness':'UNKNOWN','historical_priority':'UNKNOWN','formal_verification':'NOT_ESTABLISHED','empirical_confirmation':'NOT_OBTAINED','physical_capability':'UNKNOWN; no qualifying experiment is recorded','reported_status_evidence':[root_report]},
      'supersedes':[],'invalidates':[],'depends_on':[],'requires_external_validation':[
        {'target':'external:independent_correctness_and_prior_art_review','scope':r['gate_review'],'evidence':evid[:2]},
        {'target':'external:task_matched_capability_and_complete_cost_review','scope':r['gate_cap'],'evidence':evid[-2:]}
      ],'material_updates':[],'contrasting_blockers':[],
      'relation_coverage':'Only named comparison bridges and source-backed corrections are recorded; exhaustive dependency and prior-art search is UNKNOWN.',
      'reported_failed_attempts':[],'scientific_scope_status':r['scope']}
    status_rows.append(status)
    raw_status=ROOT/('frontier/cards/'+cid+'.json'); write_json(raw_status,status)
    wrapper=ROOT/('frontier/review_cards/'+cid+'.txt'); wrapper.parent.mkdir(parents=True,exist_ok=True)
    wrapper.write_bytes((f'FT source-derived review wrapper for {cid}. Exact current scope is in frontier/cards/{cid}.json.\n\n').encode()+text)
    # Intake mapping is auditable back to the primary authored file and all supporting paths.
    primary=evid[0]
    claim_rows.append({'id':cid,'source_id':primary['source_id'],'source_path':primary['path'],'source_sha256':primary['sha256'],
                       'status':'source_derived_unreviewed','statement':r['scope'],'evidence_paths':[x['path'] for x in evid],
                       'external_correctness':'UNKNOWN','historical_priority':'UNKNOWN','mission_status':'NOT_ACHIEVED'})
    catalog_add.append({'id':cid,'title':r['title'],'topics':r['topics'],'status':'source_derived_unreviewed','card_sha256':ch,
      'dependencies':{'depends_on':[],'scoped_dependencies':scoped_dependencies(cid)},
      'pointers':{'card_local':card_path,'current_status':'frontier/cards/'+cid+'.json','reviewed_card':'frontier/review_cards/'+cid+'.txt','read_local':'python3 tools/knowledge.py read '+cid}})
    graph_nodes.append({'id':cid,'node_kind':'claim'})
    for e in evid:
        sid=e['source_id']; graph_nodes.append({'id':sid,'node_kind':'source'})
        graph_edges.append({'from':cid,'to':sid,'kind':'provenance','raw_kind':'source_or_internal_evidence','source':'FT','composition':STATUS_BOUNDARY})
    for e in shared_context:
        sid=e['source_id']; graph_nodes.append({'id':sid,'node_kind':'source'})
        graph_edges.append({'from':cid,'to':sid,'kind':'context','raw_kind':'shared_negative_boundary_context_not_proof_premise','source':'FT','composition':STATUS_BOUNDARY})
    status_rows[-1]['card_path']=card_path
    cards_for_notice.append((cid,evid))
    for kind, suffix, question in [('REVIEW','REVIEW',r['gate_review']),('CAPABILITY','CAPABILITY',r['gate_cap'])]:
        evidence=evid if kind=='REVIEW' else evid[-3:]
        gates.append({'schema_version':1,'gate_id':f'G-FT-N{i}-{suffix}','priority_order':i,'title':f'Open {"review" if kind=="REVIEW" else "capability"} obligation: N{i}',
          'card_ids':[cid],'gate_kind':'explicit_proof_or_acquisition_obligation','question':question,
          'pass_condition':question+' Scope-matched evidence is required; metadata, hashes and finite checks do not close this gate.',
          'priority_rationale':'Stable route order only; not a predicted impact or readiness ranking.','status':'open','completion_evidence':[],
          'evidence':evidence,'validation_boundary':STATUS_BOUNDARY})

# Add scoped, source-backed correction notices to the new records only.
notices=[]
for cid, evid in cards_for_notice:
    key=cid.split('-',1)[0]
    if key=='N843': issue='Positive-error and zero-error phase regimes are separate.'; clarification='The Theta(T^(1/3)) statement is for each fixed positive epsilon<1/4; exactly zero error has the separate T-to-T+1 bound. No uniform epsilon(T), runtime, or physical clock conclusion is recorded.'; refs=[x for x in evid if 'PHASE_CLOCK_THEOREM' in x['path'] or 'AUDIT.md' in x['path']][:2]
    elif key=='N844': issue='The N610 digit inclusion and implementation scope must remain literal.'; clarification='Base-p digit inclusion is established for prime-power moduli only. Mixed-prime CRT requires joint category fields and cross-component forcing; generic finite-group access is not a polynomial-bit-cost implementation. The direct executable prototype is cyclic Z/MZ.'; refs=[x for x in evid if 'N610_AUDIT' in x['path'] or 'INDEPENDENT_DERIVATION' in x['path']][:2]
    elif key=='N845': issue='The fixed-dose isotope ceiling does not cover outcome-dependent stopping.'; clarification='Vacancy-history stopping conveys information. Keep the blind fixed deterministic dose theorem separate from the event-conditioned fresh-refill renewal construction and its unacquired same-atom/reset/protection interface.'; refs=[x for x in evid if 'ISOTOPE_RENEWAL_OPERATION' in x['path'] or 'ISOTOPE_BOUND_AUDIT' in x['path']][:2]
    elif key=='N846': issue='Total loss does not label the target sink.'; clarification='Accessible loss flags can be identical under distinct target/parasitic sink assignments. The positive finite-power focus theorem requires 0<a<b and (ab)^(1/3)(a^(1/3)+b^(1/3))<=1, plus fixed delivered power, full control, complete collection, acquired response and the stated single-pass model.'; refs=[x for x in evid if 'scientific_operation/REPORT' in x['path']][:1]
    else: issue='Prior experiments and a proposed monitor remain separate.'; clarification='The SWS cavity experiment, transmon continuous-monitor experiment and proposed coupler-inclusive SWS monitor are distinct evidence. The approximately 8 ns timestamp is a derived small-angle phase-error budget with quadratic infidelity, not demonstrated resolution; published delayed checks remain a strong comparator. No physical demonstration of the proposed monitor is claimed; established underlying experiments remain prior evidence.'; refs=[x for x in evid if 'model_challenger/REPORT' in x['path']][:1]
    notices.append({'notice_id':f'SN-FT-{key.lower()}-scope-boundary','card_ids':[cid],'issue':issue,'status':'source_derived_scoped_correction','clarification':clarification,
      'material_updates':[{'target':cid,'scope':clarification,'relation_status':'Scoped source-derived clarification; prior evidence and open gates retained.'}],
      'source_refs':refs,'whole_claim_invalidated':False})

# Append-only registries: refuse any changed existing identity.
append_jsonl(ROOT/'indexes/claims.jsonl',[
 {'id':r['id'],'title':r['title'],'path':'cards/'+r['id']+'.txt','topics':r['topics'],'status':'source_derived_unreviewed',
  'source_ids':[source_id(p) for p in r['evidence_paths'][:3]],'source_paths':['updates/FT-foundational-capability-20261015/package/'+p for p in r['evidence_paths']],
  'depends_on':[],'scoped_dependencies':scoped_dependencies(r['id']),
  'record_type':'curated_update_claim'} for r in records], 'id')
append_jsonl(ROOT/'frontier/CURRENT_CLAIM_STATUS.jsonl',status_rows,'card_id')
append_jsonl(ROOT/'frontier/OPEN_PROOF_GATES.jsonl',gates,'gate_id')
append_jsonl(ROOT/'agent/SEMANTIC_NOTICES.jsonl',notices,'notice_id')
# Catalog and graph preserve all existing records; only new identifiers are appended.
catpath=ROOT/'indexes/agent_catalog.json'; catalog=json.loads(catpath.read_text()); existing={x['id']:x for x in catalog['claims']}
for item in catalog_add:
    if item['id'] in existing and existing[item['id']]!=item: raise ValueError('catalog collision '+item['id'])
    if item['id'] not in existing: catalog['claims'].append(item)
catpath.write_bytes(jbytes(catalog))
gpath=ROOT/'indexes/agent_graph.json'; graph=json.loads(gpath.read_text()); nodeids={x['id'] for x in graph['nodes']}; edgekeys={(x['from'],x['to'],x['raw_kind']) for x in graph['edges']}
for n in graph_nodes:
    if n['id'] not in nodeids: graph['nodes'].append(n); nodeids.add(n['id'])
for e in graph_edges:
    k=(e['from'],e['to'],e['raw_kind'])
    if k not in edgekeys: graph['edges'].append(e); edgekeys.add(k)
gpath.write_bytes(jbytes(graph))

# Scoped bridge records: comparisons only; no implication or status promotion.
bridges=[
 {'id':'FT_phase_law_to_N545_task_contract','status':'CANDIDATE CONNECTION','kind':'contrast','cards':[records[0]['id'],'N545-full-unitary-finite-horizon-markov-state-law'],
  'alignment':'Both concern finite-horizon quantum-versus-classical descriptions, but N843 fixes one irrational phase and terminal-probability task while N545 has arbitrary supplied unitary words and density inputs.',
  'assumptions':['Distinct input/output contracts; no exponent or theorem transfer is claimed.','N843 positive-error and exact-error regimes remain separate.'],
  'acquisition':'No new input acquired by the bridge. Any application requires its own task-matched model and data.',
  'cost':'Compare acquired phase precision, calibration, preparation, reset and readout against an ordinary counter/cosine and the exact N545 baseline.',
  'falsifier':'A source review showing either task contract or claimed relation has been misstated.',
  'evidence':[ref('workers/foundational_math/PHASE_CLOCK_THEOREM.md','N843 fixed-phase task contract.'),ref('cards/N545-full-unitary-finite-horizon-markov-state-law.txt','Existing N545 task contract.',campaign=False)]},
 {'id':'FT_subgroup_bound_to_N610_prime_power_boundary','status':'CANDIDATE CONNECTION','kind':'scoped_comparison','cards':[records[1]['id'],'N610-rank-absorbing-stratified-exact-local-stationary-sampling'],
  'alignment':'The subgroup-image extension is compared with N610. The base-p digit construction preserves the N610 output class for prime-power moduli; no mixed-prime independent-component reduction is asserted.',
  'assumptions':['Prime-power inclusion only.','Mixed-prime CRT must preserve joint categories and cross-component forcing.','The executable prototype is cyclic Z/MZ; an arbitrary-finite-abelian implementation is not supplied.'],
  'acquisition':'General implementation requires acquired subgroup/forcing descriptors and their polynomial-bit-cost representation.',
  'cost':'Expected fresh-category bound is not worst-case runtime. Root matched Z/4 timing favored the digit incumbent.',
  'falsifier':'A counterexample to the stated prime-power digit embedding or a future joint-CRT theorem with all shared-category premises.',
  'evidence':[ref('workers/abelian_sampler_audit/REPORT.md','Independent audit states prime-power inclusion and mixed-prime CRT boundary.'),ref('cards/N610-rank-absorbing-stratified-exact-local-stationary-sampling.txt','Existing N610 interface and source-reported scope.',campaign=False)]},
 {'id':'FT_isotope_renewal_to_N792_process_contrast','status':'CANDIDATE CONNECTION','kind':'process_contrast','cards':[records[2]['id'],'N792-covalent-isotope-fractionation-and-mixed-hazard-screen'],
  'alignment':'Both concern isotope-material outcomes, but N845 is event-conditioned carbon knock-on/refill renewal; N792 is a distinct electrochemical H/D loading/stripping route.',
  'assumptions':['No hazard, selectivity, reset or physical-interface parameter transfers between the routes.','Generic isotope storage is not a novelty claim.'],
  'acquisition':'No new process data acquired by this bridge.',
  'cost':'Compare only after each process has its own source-labelled yield, reset, damage, acquisition and matched-baseline measurements.',
  'falsifier':'Evidence that the compared physical operations share a measured common event/reset interface; none is currently supplied.',
  'evidence':[ref('root/ISOTOPE_RENEWAL_OPERATION.md','N845 renewal and fixed-dose quantifier boundary.'),ref('cards/N792-covalent-isotope-fractionation-and-mixed-hazard-screen.txt','Existing N792 operation and scope.',campaign=False)]}
]
bridge_path=ROOT/'mechanisms/bridge_candidates.json'; bridge_doc=json.loads(bridge_path.read_text()); have={x['id']:x for x in bridge_doc['bridges']+bridge_doc['rejected_transfers']}
for b in bridges:
    if b['id'] in have and have[b['id']]!=b: raise ValueError('bridge collision '+b['id'])
    if b['id'] not in have: bridge_doc['bridges'].append(b)
bridge_path.write_bytes(jbytes(bridge_doc))

# Intake-level records and minimal preservation receipt.
write_json(UPDATE/'CLAIMS.json',{'schema':'astra.intake-claim-map.v1','intake_id':'FT','base_revision':BASE,
 'mission_status':'NOT_ACHIEVED','claims':claim_rows})
write_json(UPDATE/'BRIDGES.json',{'schema':'astra.scoped-bridge-set.v1','intake_id':'FT','base_revision':BASE,
 'status':'CANDIDATE CONNECTION; NO IMPLICATION OR STATUS PROMOTION','bridges':bridges})
write_json(UPDATE/'SCOPED_NOTICES.json',{'schema':'astra.scoped-notices.v1','intake_id':'FT','notices':notices,
 'shared_negative_results':['Rank-collapse exact cutoff and restricted-search boundary; no arbitrary-matrix no-go.','Hidden transfer-spectrum counterexample is restricted to the cited v2 hypotheses; observable scalar poles remain invariant.']})
write_json(UPDATE/'CAPITAL_PRESERVATION_RECEIPT.json',{'schema':'astra.capital-preservation-receipt.v1','intake_id':'FT','checked_main':'b7cada92d2eb304578be5ed974f1e44b10a89928',
 'live_remote_main':'b7cada92d2eb304578be5ed974f1e44b10a89928','open_pull_requests':[84,85,87,88],
 'collision_check':{'tag':'FT','ids':['N843','N844','N845','N846','N847'],'result':'no collision on checked main or open PR changed paths'},
 'latest_merged_records':{'pull_request':91,'cards':['N840-positive-directional-ground-states-and-phase-compatibility','N841-inventory-aware-decision-closure-and-joint-calibration','N842-load-qualified-momentum-transfer-and-terminal-metrology'],
   'gates':['G-FS-N840-REVIEW','G-FS-N840-CAPABILITY','G-FS-N841-REVIEW','G-FS-N841-CAPABILITY','G-FS-N842-REVIEW','G-FS-N842-CAPABILITY'],'all_open':True},
 'source_copy':{'campaign_manifest_sha256':source_manifest_hash,'listed_files':78,'listed_bytes':391572,'copied_items_including_manifest':79,'verified_byte_identical':True},
 'status_boundary':'source_derived_unreviewed; mission NOT_ACHIEVED; gates remain open. This receipt reports pin/collision/integrity checks only.'})

synthesis='''# Foundational capability intake — scoped synthesis\n\n**Mission: NOT_ACHIEVED.** The strongest mathematical result is a source-reported and internally reconstructed finite-horizon stochastic memory law. The physical paths remain conditional; none establishes a new experimentally validated operation or complete-resource advantage. Every new card is `source_derived_unreviewed`; external correctness and historical priority remain UNKNOWN.\n\n## Mathematical result and boundaries\n\nFor one fixed `alpha=(sqrt(5)-1)/2` throughout, terminal probabilities `p_k=(1+cos(2 pi alpha k))/2`, and arbitrary homogeneous `n`-state stochastic models with initial distribution, terminal readout and repeated identical wait command, the minimum state count for uniform error through horizon `T` is reported as `Theta_(alpha,epsilon)(T^(1/3))` for every fixed `0<epsilon<1/4`. The terminal readout receives the evolved state only; it is not additionally given `k` or an external lookup table. At zero error a separate argument gives `T<=N_alpha(T,0)<=T+1`. An ideal qubit generates these terminal probabilities exactly. The result is not a general computing or runtime separation: ordinary counter/cosine evaluation uses O(log T) bits and the phase precision cost grows O(log(T/epsilon)). Root reconstructed the proof; an independent same-team audit and bounded construction checks are preserved. Formal/external correctness and priority remain open. Rank-collapse and hidden-spectrum records are attached to N843 as shared negative/boundary evidence only, not as premises for this theorem. See N843.\n\nThe finite-abelian sampler report derives an expected subgroup-image query bound under strict-layer and shared-category independence conditions. Its executable HNF prototype is cyclic `Z/MZ`. The literal digit-layer inclusion into N610 is proved for prime-power moduli; mixed-prime CRT needs joint categories and cross-component forcing, and generic finite-group access does not prove polynomial bit cost. In the root 3,000-draw `Z/4` replay, HNF used fewer fresh events but took 3.195 s versus 0.405 s for the digit incumbent. This does not establish a new output class or practical speedup. See N844.\n\n## Conditional physical routes\n\nThe isotope result keeps two quantifiers separate. A blind writer at one fixed deterministic dose per attempted site and unconditioned occupied output has the ceiling `q*=p sigma_L/[p sigma_L+(1-p)sigma_H]`. Vacancy-history stopping is informative and lies outside that bound. An ideal event-conditioned renewal operation screens a fresh atom until ejection or screening fluence, restarts after ejection, and accepts/protects a survivor; its composition is `q(d)=p exp(-sigma_H d)/[p exp(-sigma_H d)+(1-p)exp(-sigma_L d)]`. At planning `p=.01109` and central 95 kV cross sections `sigma_L=56.6 mb`, `sigma_H=2.1 mb`, the nominal 90% calculation gives EXPECTED costs of about 105 attempts, 104 refills and `1.959e13` target electrons/nm². Retry and dose tails are unbounded; finite caps reduce yield. These are conditional expectations at those inputs, not a general 90% cost. `0.298 J/nm²` is incident kinetic energy per addressed area. Same-atom event detection, fresh known refill, preserved post-repair rates, neighbor protection, reset and final readout are not obtained; no experiment was performed. CVD and post-growth isotope methods are strong incumbents. See N845.\n\nThe optical loss record has a negative and a conditional positive side. Identical accessible instruments can hide different target/parasitic sink assignments, so an accessible total-loss flag does not identify target absorption; a passive resonator can reduce total loss while its target sink absorbs positive energy. The positive two-finite-power theorem requires `0<a<b` and `(ab)^(1/3)(a^(1/3)+b^(1/3))<=1`, as well as fixed delivered target power, full complex control, complete collection, a qualified single-pass saturable absorber, acquired response and reset. Nonlinear-bucket and iTRAN are strong incumbents. Only bounded synthetic checks were run. See N846.\n\nThe dual-rail record preserves the established erasure interface and 2026 SWS gate as prior evidence, then bounds a proposed coupler-inclusive monitor against delayed checks and a different-platform transmon monitor. Loss during the SWS cross-Kerr creates a correlated unknown partial phase; the roughly 8 ns event-time target is a derived small-angle phase-error budget whose infidelity contribution is quadratic in residual phase, not demonstrated monitor resolution. The cited monitor's integration window is far longer and does not qualify the SWS cavity path. Which-path dephasing, monitor backaction/loss and matched full-circuit cost remain open. No physical demonstration of the proposed monitor is claimed; the underlying SWS and transmon experiments are established prior evidence, with credit retained by their authors. See N847.\n\n## Shared negative and correction results\n\nThe branchwise rank-collapse argument has an exact binomial exterior-power cutoff and sharp trace-preserving family, but known automata/exterior-algebra overlap stopped it as a main lead. A restricted binary search failed to support an all-dimension extrapolation at `d=6`; root replayed `d=4`. No arbitrary-matrix no-go follows. The exact negative result and replay receipt are separately linked in N843 as shared context only, not premises of the phase-clock theorem.\n\nHidden transfer-spectrum boundary: two exact fair-iid QHMM presentations have different collision-transfer spectra `{1/2}` and `{1/2,1/4,1/8}`. This refutes unrestricted full-spectrum invariance only under the cited `arXiv:2412.12812v2` hypotheses; observable scalar poles remain invariant. This is a scoped realization correction, not a review of the full paper. The counterexample and exact replay receipt are separately linked in N843 as shared context only, not premises of the phase-clock theorem.\n\nThe sampler's early O(N) validation scan and uncounted descriptor request were corrected before the freeze. Prime-power inclusion, not mixed-prime independence, is the exact N610 comparison. The isotope blind-dose quantifier excludes outcome-dependent stopping. The phase cube-root law is fixed-positive-error only. All corrections and negative results remain source-linked in the frozen package.\n\n## Resources and evidence status\n\nThe frozen campaign reports 11 distinct workers plus root (5 gpt-6.1-sol max, 6 gpt-6-luna max), eight selected copy-first replays passing in 12.729 s across four subprocess slots, and a separate 0.654 s HNF/local-access check. These are bounded computation clocks, not model inference or experiment time. Token use, pure inference time, energy, aggregate compute and money are UNKNOWN. No lab experiment, paid compute, purchase or external message occurred.\n\nRoot checked the five primary results and source-level internal audits; this intake preserves those statuses without upgrading them. Hashes, view generation and validators report integrity/access only. The gates below remain open, and no mission-level capability is established.\n'''
(UPDATE/'SYNTHESIS.md').write_text(synthesis,encoding='utf-8')
(UPDATE/'RESEARCH_HANDOFF.md').write_text('''# Research handoff\n\nMission status: **NOT_ACHIEVED**. Five scoped cards N843–N847 are `source_derived_unreviewed`; all ten new review/capability gates remain open. Root's internal reconstructions and same-team audits are source-backed, not external verification.\n\nThe first mathematical handoff is independent proof and prior-art review of N843, preserving the fixed-phase, no-extra-k readout, fixed-positive-error and exact-error statements separately. Its rank-collapse and hidden-spectrum references are shared negative context, not phase-theorem premises. For N844, review the conditional shared-category proof and exact HNF prototype; any implementation extension must distinguish prime-power digit inclusion from mixed-prime CRT with joint categories/cross-component forcing and charge descriptor bit costs.\n\nFor N845, do not proceed to a blinded renewal trial until one process jointly qualifies same-atom no-ejection records, independent refill/composition, repaired-site rates, event/reset, neighbor control, accepted-site protection and final isotope readout. The fixed-dose ceiling does not cover event-conditioned stopping. Any nominal 90% arithmetic remains an expectation at planning p=.01109 and central 95 kV cross sections 56.6 mb and 2.1 mb, with unbounded retry/dose tails and cap-induced yield loss.\n\nFor N846, qualify fixed target delivery, complete energy collection, material response/reset and full control before comparing total cost with nonlinear-bucket/iTRAN and a transmission-matrix baseline. The positive finite-power theorem premise is 0<a<b and (ab)^(1/3)(a^(1/3)+b^(1/3))<=1. For N847, measure event-time resolution, flag/phase correlation, which-path backaction and added loss on the SWS cavity path, then compare the full circuit against delayed checks; the 8 ns target is a small-angle phase-error budget with quadratic infidelity, not a demonstrated monitor resolution.\n\nRank-collapse and hidden-spectrum results remain shared negative/boundary evidence in `SYNTHESIS.md`, not new standalone cards. Root owns final integrity review and any commit, push or PR.\n''',encoding='utf-8')

# Store a compact machine-readable gate list in the intake and append gates to capital registry.
write_json(UPDATE/'OPEN_GATES.json',{'schema':'astra.ft-open-gates.v1','intake_id':'FT','gates':gates})
# Add source metadata rows only for the exact source files used by current records.
metapath=ROOT/'indexes/source_metadata.jsonl'; existing_meta=[json.loads(x) for x in metapath.read_text().splitlines() if x.strip()]
meta_ids={x['source_id']:x for x in existing_meta if 'source_id' in x}; meta_rows=[]
for sid,e in all_refs.items():
    p=ROOT/e['path']; data=p.read_bytes(); rel=e['path'].split('/package/',1)[-1] if '/package/' in e['path'] else e['path']
    title=p.name+' [FT preserved source]'
    row={'source_id':sid,'path':e['path'],'title':title,'sha256':sha(data),'bytes':len(data),'date_version':'2026-10-15 / FT',
         'read_depth':'Whole frozen authored source file referenced for a scoped FT intake; external correctness and priority UNKNOWN.',
         'reported_verification':STATUS_BOUNDARY,'extraction':'original_utf8_bytes'}
    if sid in meta_ids:
        if meta_ids[sid]!=row: raise ValueError('source metadata collision '+sid)
    else: meta_rows.append(row)
if meta_rows:
    old_meta_bytes=metapath.read_bytes()
    if old_meta_bytes and not old_meta_bytes.endswith(b'\n'): raise ValueError('refusing non-newline source metadata append')
    metapath.write_bytes(old_meta_bytes+b''.join((json.dumps(x,ensure_ascii=False)+'\n').encode() for x in meta_rows))
# Derived manifest is finalized after access generation; mark selected owned files here.
print(json.dumps({'status':'GENERATED','cards':[r['id'] for r in records],'gates':len(gates),'bridges':len(bridges),'source_manifest_entries':len(source_entries),'base_revision':BASE},indent=2))
