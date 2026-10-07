"""Assemble the resumable research index and explicitly scoped validation record."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'

ledger = json.loads((ROOT/'work/claim_ledger.json').read_text())
cards = {c['id']: c for c in ledger['cards']}
cards['C03']['status'] = 'Exact local and finite-chain certificates implemented and independently reviewed; rational existence conditional on C01'
cards['C03']['limits'] = 'Finite local safety and supplied-initial-set chains are recognized. A complete finite recognizer of classwide global absorption on arbitrary unbounded classes is not established.'
cards['C04']['report'] = 'work/agents/statistical_mechanics/jump_safety.md'
cards['C05']['report'] = 'work/agents/pde_physics/chemical_jump_certificate.md'
cards['A02']['status'] = 'Retuned detector/contour dependency independently reviewed conditional on exact source identities; headline remains unvalidated'
cards['A02']['limits'] = 'Normalized theta/Whittaker reflection identities remain the decisive unverified gate. Exact schedule checks do not validate the proposed zero-free region or general-field extension.'
cards['A07']['result'] = 'Small Wigner-Yanase and weighted commutators yield a candidate finite classical Gibbs archive; spectral-gap obstruction; elementary common-width rounding exponent 1/(2^k-1).'
cards['A07']['limits'] = 'Worker proof only; independent full audit and priority unresolved. Unrestricted ground-component/Fock factorization is unproved.'
cards['V02']['report'] = 'work/agents/reaction_control_prior/FINAL_REVIEW.md'
cards['V02']['status'] = 'Full final cold review and targeted primary-source search; no substantive gap identified, no external correctness or priority certification'
ledger['cards'].extend([
    dict(id='C06', title='Finite molecular compartment graph safety', worker='pde_physics',
         report='work/agents/pde_physics/chemical_graph_certificate.md',
         status='Complete conditional certificate transfer, root analytic reconstruction and 200 exact corners replayed',
         result='Full-dimensional common inward polytope, equal local volume, common species hopping coefficient and bounded degree give an explicit sites-prefactor exponential finite-time exit bound.',
         limits='Certificate collars narrow with hopping strength. Unequal species diffusion has an exact counterexample. Mesh refinement degrades this bound; no continuum PDE or general graph absorption theorem.'),
    dict(id='A13', title='Even-walk sampler for gauge-nonnegative pure GBS', worker='combinatorics_complexity',
         report='work/agents/combinatorics_complexity/nonnegative_gbs_sampling.md',
         status='Complete construction and finite-bit implementation; independent internal audit passed; standard Markov loop-soup ancestry identified',
         result='The collision-inclusive photon law for explicit rational symmetric entrywise-nonnegative contraction B is a compound Poisson sum of even closed walks; TV-epsilon sampling has bit cost polynomial in encoded B, mode count, numerical mean photon number E, and 1/epsilon.',
         limits='Standard intensity-1/2 Markov loop soup on a bipartite double cover is the exact mechanism. Gauge supplied/acquired; numerical E charged. General phases excluded; conditioning amplifies TV error by inverse acceptance. GBS-specialization priority unresolved.')
])
ledger['cards'][-1]['independent_audit'] = 'work/agents/quantum_coding/nonnegative_gbs_audit.md'
ledger['cards'][-1]['audit_sha256'] = hashlib.sha256((ROOT/ledger['cards'][-1]['independent_audit']).read_bytes()).hexdigest()
ledger.update({
    'campaign_status':'Research snapshot complete; scientific conclusions retain the per-card status below.',
    'primary_deliverable':'outputs/endotactic_permanence.tex',
    'source_pins':{
       'astra':'2aa99b272ec720af587cf6cd6fb1822e15433ce1',
       'openai_math':'adc7f1241b42e322a6451854ab7e4b4c146bf78a'},
    'team':{'workers':26,'model':'gpt-6.1-sol','reasoning_effort':'max',
            'audit_limit':'Separate same-model reconstructions are not independent external validation.'},
    'status_semantics':{
       'internal proof':'A written mathematical derivation reviewed within this campaign; not externally certified.',
       'conditional':'The stated premise or released identity remains unvalidated.',
       'diagnostic':'Finite program execution supports exactly its tested interface, not a universal theorem.'}
})
for c in ledger['cards']:
    p=ROOT/c['report']
    assert p.is_file(), c
    c['report_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/'RESEARCH_INDEX.json').write_text(json.dumps(ledger,indent=2)+'\n')

replays = json.loads((ROOT/'work/root_replay_results.json').read_text())
validation={
 'date':'2026-10-07',
 'scope':'Integrity, compilation and finite diagnostics only; none certifies theorem correctness or novelty.',
 'main_source':{'path':'outputs/endotactic_permanence.tex',
  'sha256':hashlib.sha256((OUT/'endotactic_permanence.tex').read_bytes()).hexdigest(),
  'native_compiler':'success',
  'meaning':'The final standalone source compiled successfully with the desktop editor compiler.'},
 'root_replays':replays,
 'additional_root_checks':[
  '256 exact switched-reaction facet checks passed.',
  'Smooth proper-loss symbolic identities reconstructed with exact algebra.',
  'Finite graph chemical safety: 200 rational corners replayed; root reconstructed generator, hopping noise, stopped bound and unequal-diffusion counterexample.'
 ],
 'reported_worker_checks':[
  'Reaction certifier: 36 targeted tests, positive/fractional examples, wider-rate rejection, candidate search and finite chain.',
  'Stochastic closed example: 16610 factorial checks including 4847 insufficient-count cases; 28004 activity and 3656 collar checks.',
  'Stochastic linear example: 16 exact rational corners.',
  'Spatial graph certificate: 200 exact corners and unequal-diffusion counterexample.',
  'Rounded Gaussian archive: 2364 bin checks, 111 primitives, all 5250 compact codes; costs retained.',
  'GBS walk law: 322 exact low-degree coefficient identities; seeded sampler diagnostics are empirical only.'
 ]
}
(OUT/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps({'cards':len(ledger['cards']),'reports_present':True,'manuscript_sha256':validation['main_source']['sha256']}))
