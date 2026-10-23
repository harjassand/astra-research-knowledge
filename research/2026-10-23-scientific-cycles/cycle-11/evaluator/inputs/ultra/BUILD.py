#!/usr/bin/env python3
"""Actual producer layout assembler; REPLAY.py is the portable receiving path."""
from pathlib import Path
import hashlib,json,shutil,zipfile
BASE=Path(__file__).resolve().parents[2]
WORK=BASE/'work/Cycle10'
OUT=BASE/'outputs/Astra_Amplification_Cycle10_ULTRA_20261023'
NATIVE=BASE/'outputs/Astra_Amplification_Cycle9_ULTRA_20261022.zip'
PROOF_SHA='41776adc6c19232d2db53adf4e628c680f61f6b7cf08b6ddd24c612db3cb633c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,s):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n')
def copy(src,name):
 dst=OUT/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
def main():
 assert not OUT.exists(),'Preserve prior builds before rebuilding'
 assert sha(WORK/'root/PROOF.txt')==PROOF_SHA
 assert NATIVE.stat().st_size==10604540 and sha(NATIVE)=='0eb683200712cf4313d7e55da66df83ef02fece741e5c2633701a8be19e75925'
 OUT.mkdir(parents=True)
 copy(WORK/'root/PROOF.txt','PROOF.txt')
 for n in ['replay.py','RESULT.json']:copy(WORK/'root'/n,'calculations/principal/'+n)
 for n in ['UNRELEASED_INITIAL_PROOF.txt','UNRELEASED_BEFORE_RAW_INFORMATION_CORRECTION.txt','SCOPE_CORRECTIONS.json']:copy(WORK/'root'/n,'provenance/'+n)
 omitted=[]
 for branch in ['converse','coding','challenge']:
  for src in sorted((WORK/branch).rglob('*')):
   if not src.is_file():continue
   rel=src.relative_to(WORK/branch)
   if src.suffix=='.pdf':
    omitted.append({'original_owner_local_path':str(src),'bytes':src.stat().st_size,'sha256':sha(src),'reason':'External primary-paper PDF not duplicated; original URL and exact read receipt supplied. Not a replay input.'});continue
   copy(src,'studies/'+branch+'/'+str(rel))
 copy(NATIVE,'sources/'+NATIVE.name)
 common=WORK/'intake/Astra_Scientific_Amplification_Cycle10_20261023'
 for n in ['START_HERE.txt','ORIGINAL_SOURCE_ROUTES.json','prompts/04_ULTRA_CONTINUATION.txt']:
  copy(common/n,'contract/'+Path(n).name)
 copy(WORK/'intake/INTAKE_RECEIPT.json','contract/INTAKE_RECEIPT.json')
 write('EXTERNAL_REFERENCE_OMISSIONS.json',json.dumps({'external_reference_omissions':omitted,'scope':'Bounded original SOURCE_BINDINGS may describe owner-local external PDF reads. Use THIS root manifest/replay for this package; never interpret selected bindings as an installer or full native verifier.'},indent=2))
 write('README.txt',r'''
ASTRA CYCLE10 ULTRA — POOLED RATE / COMPLETE MEMORY / ACCESS BUDGET

Read PROOF.txt (governing final integrated proof), OUTPUT_INTERFACE.txt,
COMPARATOR.txt, CAPITAL_AND_CHANGE.txt, COSTS.json and FAILURES_AND_DECISION.txt.
DATED_STATUS_UPDATES.txt distinguishes preserved draft mistakes from current
authority. Three actual-source independent audits bind the exact main proof.

Main consequence on the unchanged source, fixed D and L, r iid COMPLETE queues:
the optimum zero-added-aid pooled fixed Bell-rank rate R has
 B-R=Theta_D(ln L), B=(L+1)lnD/2, with r->infinity FIRST and global error->0.
Thus R/B->1 as L grows. Unlike the closed pointwise pure-profile task, this
is fixed-rank usable entanglement decoupled from the ACTUAL complete residual.
Every clock, old-memory register, retained transcript/work and bad branch counts.

Finite resource converse, epsilon<1/2:
 (1-2epsilon)lnN <=min{rB,rU+I_acc/2}+E lnJ+g(epsilon),
 U=B-.5lnL+.5H(K|BellY), H(K|BellY)<=geometric_constant(D^-2).
The supplied-record conditional-product premise is explicit; internal records
or an inaccessible witness cannot be donated as initial access. The countable
expected-stock proof permits E J=infinity. Arbitrary catalysts require a proved
preparation bound. No broad catalytic advantage is asserted.

Portable Python3.10+ standard-library command:
 python3 REPLAY.py --output /absolute/path/cycle10_receipt.json
It hashes all source and three audit bindings, then executes ONLY four NEW
Cycle10 admission scripts in a disposable relocated copy. It DOES NOT run a
quantum distillation code, predecessor scientific suites, hardware or paid jobs.
Proofs import the KNOWN Devetak–Winter theorem; code construction/blocklength,
code selection/compilation costs and physical implementation remain UNKNOWN.

The FULL unchanged native Cycle9 source is embedded, including every previous
native dependency down to actual R1 proof/reservoir/replay. No historical
source is replaced by a selected fragment. The common Cycle10 packet was
verified with its OWN integrity verifier; our seven source files match the
actual original native ZIP exactly. External primary URLs/read receipts are
provided; one locally read primary PDF is not duplicated in this delivery.

No ordinary-stock supply, formation or computation advantage is established.
Historical novelty/external certification/practical use remain UNKNOWN.
Max's reading, scientific acceptance and integration are distinct from private
binary delivery. External receipts bind exact ZIP size/hash/private reference
and actual download; they are outside this ZIP to avoid self-reference.
BUILD.py is the actual producer-layout assembly record, not a portable installer.
''')
 write('OUTPUT_INTERFACE.txt',r'''
SOURCE AND OPERATION
The ACTUAL Omega, current inaccessible K clocks and complete old nu memory are
unchanged; r original COMPLETE queues are iid. Default apparatus factors from
the COMPLETE source. No added entangled aid, supplied correlated access or
shared seed. The accessible input is exactly rho_L^tensor r.

Run the actual Cycle8 deterministic receiver at fixed eta=L^-2 perqueue;
coherently compute LAST-NONZERO J into a local ancilla, uncompute scratch and
measure ONLY that ancilla (the stated Luders instrument), broadcast J, keep
C=(J-1)+ and reset the suffix. Do not measure retained prefix digits. This
observable length yields a good coherent-information comparison. Code the
ACTUAL resulting flagged iid state via a conventional finite-dimensional
Devetak–Winter code, with hardwired fixed final Bell rank N_r on every branch.
That code is an existence construction, not an executed efficient large code.

FINAL CONTRACT
Each Bell register has localdimension N_r. Reference is exactly
 Phi_(N_r) tensor ACTUAL_final_residual_Z.
Z includes all retained work, records, clocks, old memory and their correlations.
It can also include disposal environments for the purity proof. No output is
allocated to an original queue; no unsafe branch is counted as actual inventory.
There is ONE GLOBAL halftrace error tending to zero at fixed L as r grows.
Only later take L large. No simultaneous uniform rate/blocklength bound follows.

Intermediate reference coarse-J distribution may differ from ACTUAL J law.
Distance and conditional entropy compare these honestly; its eta error is never
tensorized r times. Final residual is actual, without this intermediate caveat.
Initializer error is GLOBAL COMPLETE-input error. A full retained-output channel
implementation error costs twice its halfdiamond error; Bell-marginal-only
control requires a fresh purity lift. No unproved hidden-memory accessibility.

OPTIONAL BUDGET
An actual finite/countable shared initial Z has p(z|Kvec), unchanged conditional
quantum sigma_Kvec and explicit full product preparation. Independent Phi_J
stock factors jointly from that preparation and pays E lnJ, not lnE J.
Theorem(13) permits consumption; demanded catalyst return is additional. Only
LOCC formation from declared stock is covered without another resource proof.
''')
 write('COMPARATOR.txt',r'''
MATCHED ORDINARY CONTROL AND SCIENTIFIC CONSEQUENCE
An equally informed ordinary-stock receiver gets the IDENTICAL rho_L, inaccessible
clock condition, all residual registers, allowed access/stock and global error.
It may execute exactly this preprocessing and coding, and obeys the same upper.
The queue is ordinary preselected entanglement with product nuisance filling.
Original supply B is fully charged. No preparation, formation, computational or
physical advantage over that ordinary control is claimed.

Strong conventional methods are the actual controls, not weak straw benchmarks:
1. Exact keepfirst: lnD nats/queue at zero error, no coding.
2. Raw full-queue one-way hashing: I_c=lnD-lnL+C_L; it fails at large L.
3. Periodic computational sampling: explicit receiver, exact actual output
spectra and ordinary hashing in studies/challenge; weaker O(sqrtL+logL) deficit
asymptotically, but BETTER finite guarantees than conservative Cycle8 constants
on some small L. D2,L100,b7 actual coherent information22.37658 nats/queue,
while B=35.00393; the main logarithmic bound there falls back to ln2.
4. Actual Cycle8 receiver plus coarse observable length and actual-state hashing:
B-O_D(logL), complete joint error vanishes. The root rate table shows its loose
constants and scopes scalar evaluation separately from any code experiment.
5. True supplied Kvec: rate B with a finite explicit concentration bound; initial
access entropy rlnL/symbol encoding is charged. This is a DIFFERENT access input.
6. Known squashed entanglement: half-mutual-information plus exact posterior
entropy gives finite-r upper and a necessary .5lnL-O_D(1) deficit.

The material new consequence is that near-total usable pooled recovery survives
with vanishing complete joint error, while nontrivial fixed-L uniform-r pointwise
profiles do not. Both are true under their different stated interfaces. The new
rate-minus-supply deficit and access budget are not a relabelled perqueue loss.
The unresolved coefficient between .5 and the conservative achieved constant is
not claimed sharp, nor is a fixed-error strong converse or efficient code known.
''')
 write('CAPITAL_AND_CHANGE.txt',r'''
ACTUAL CAPITAL RECEIVED
Cycle6 actual product-nu tail and inaccessible clock source: supplies commuting
Bell-label entropy with geometric posterior uncertainty. A chi-tail substitution
would change the entropy and hence both the resource budget and the rate.
Cycle8 actual zero-aid receiver: supplies a complete eta-comparison to pure
prefix profiles, with explicit algorithm/costs on composite integer D as well.
Cycle9 physical coarse LAST-NONZERO map: turns that comparison into an
OBSERVABLE output length while preserving a pure Bell prefix in the reference.
Cycle9 closed pointwise law: identifies precisely what pooled rank must change;
its theorem is not reopened or contradicted.

NEW SCIENTIFIC RECEIVING WORK
Root defined fixed pooled rank times ACTUAL complete residual, proved the
actual-flagged coherent-information bridge (including different reference-J law)
and integrated the supply-minus-rate order theorem. Root also developed the
global initial Shannon-access / expected-log-stock budget with explicit actual
conditional preparation, and full-access concentration comparator. Bounded work
supplied exact posterior/finite squashed converse, coding/purity audit and the
periodic measurement alternative. New exact calculations test these obligations.

KNOWN MACHINERY BOUNDARY
Squashed entanglement, hashing, conditional entropy continuity, classical
entropy/coding and pure-output decoupling are established tools, explicitly
credited. This does not invent a general new distillation method. Their specific
combination closes a previously unresolved meaningful source/interface question:
R/B->1 with complete memory while B-R remains order logL. Byte hashes, number
of workers and this source reuse are not evidence of recursive intelligence.
The next owned question is the sharp coefficient/resource boundary; no merely
positive pooled output is presented as the achievement.
''')
 write('FAILURES_AND_DECISION.txt',r'''
PRESERVED FAILURES / LIMITS
Raw hashing of rho_L has I_c=lnD-lnL+C_L, negative for large L; positive pooled
rate does not come from ignoring the unknown boundary. A draft wrote the wrong
raw formula lnD-C_L. The converse auditor caught it; both actual drafts and
SCOPE_CORRECTIONS are preserved. All MAIN theorem equations already used the
correct entropy expression; the final governing source and all audits use the
corrected failed-bridge formula.

Tensoring the eta reference produces r eta and is invalid in this limit. The
proof codes the actual iid output state instead. Appended reference J is not
the actual J law; no donated clock or postselected branch fixes that difference.
The natural dephased separable comparator gives only B-O_D(1), insufficient for
the logarithmic pooled obstruction. Its complete calculation is preserved.
Periodic sparse tests give an actual finite receiver, stronger on some finite
parameters but O(sqrtL) deficit, asymptotically weaker than the main construction.
No full quantum code was executed; exact scalar/finite receiver admissions do
not measure a large coding experiment, prove priority or yield cheap hardware.
Unrelated closed/protected programmes and original R1 are preserved unchanged.

DECISION
Close existence and logarithmic ORDER of complete-joint pooled recovery on this
source. Continue at the sharp logarithmic deficit coefficient or its corresponding
initial access/stock conversion with the SAME residual/resource contract. The
finite-error strong converse, effective blocklength/compilation and general
catalytic joint-return tradeoffs remain separate OPEN boundaries. Do not replace
these gaps with an unmeasured cross-domain application or claimed cost saving.
''')
 write('DATED_STATUS_UPDATES.txt',r'''
Only top-level PROOF.txt SHA41776adc6c19232d2db53adf4e628c680f61f6b7cf08b6ddd24c612db3cb633c
governs this release. All three FINAL_ROOT_AUDIT files bind that exact19592-byte
source. Earlier draft-root audits and quoted interim hashes are retained dated
evidence, not competing authority. Two actual unreleased drafts are preserved.
The first correction series makes dimensions, infidelity, countable proof and
implementation costs explicit. The second corrects the erroneous RAW failed-
bridge coherent-information formula and clarifies actual preparation/catalysts.
No main theorem equation changed. SCOPE_CORRECTIONS.json records exact bytes.
The challenge replay's historical 'no final root audit yet' limitation describes
that bounded replay file, superseded by the supplied final source-bound audit.
Coding's original independent audit and dated appendices show both identified
precision defects and their repairs; current final binding confirms the repair.
Primary-paper local SOURCE_BINDINGS describe a locally read PDF not redistributed
in this archive; EXTERNAL_REFERENCE_OMISSIONS explicitly lists it and its hash.
Use the root manifest/portable replay, not a selected directory as full installer.
''')
 write('REFERENCES.txt',r'''
PRIMARY REFERENCES ACTUALLY READ, AND THEIR ROLE
Igor Devetak and Andreas Winter, Distillation of secret key and entanglement
from quantum states, quant-ph/0306078v1, SectionIII/Theorem10 and Remark11;
AppendixB fidelity convention. https://arxiv.org/html/quant-ph/0306078
Known coherent-information achievability for actual finite iid state. We do not
infer efficient code construction, blocklength or circuit gate count from it.
The bounded coding source read receipt binds the exact original PDF bytes/hash.

Matthias Christandl and Andreas Winter, Squashed Entanglement—An Additive
Entanglement Measure, quant-ph/0308088v3, Definition1/Proposition3 and finite
output bounds. https://arxiv.org/html/quant-ph/0308088v3
Known LOCC monotone and upper via trivial/product extension. Our converse uses
a direct conditional-entropy proof rather than assuming its continuity.

Andreas Winter, Tight uniform continuity bounds for quantum entropies,
1507.07775v6, SectionII/Lemma2. https://arxiv.org/html/1507.07775v6
Known finite-A conditional-entropy continuity with dimension-independent B.
Root reproduces the binary-mixture/Jordan argument with its exact constants.

Source dependency: FULL unchanged native Astra_Amplification_Cycle9_ULTRA_20261022.zip
SHA0eb683200712cf4313d7e55da66df83ef02fece741e5c2633701a8be19e75925;
governing proof SHAa91d763e1526ffb934e5cfeb996c9bcb04bbdc624e2e4a93d175a51dfcad8bf2.
Its full Cycle8 source contains the actual receiver PROOF(2)—(10), explicit
integer algorithm and inherited known-method references. No predecessor science
was rerun this cycle. Historical priority of this source-specific combination
has not been exhaustively established and remains UNKNOWN.
''')
 observed={}
 for branch,file in [('root','RESULT.json'),('converse','RESULT.json'),('challenge','REPLAY_RESULT.json'),('converse','RESOURCE_RESULT.json')]:
  data=json.loads((WORK/branch/file).read_text());observed[branch+'/'+file]={k:data[k] for k in ['wall_seconds','cpu_seconds'] if k in data}
 costs={'observed_new_bounded_admissions':observed,'rate_scalar_table':json.loads((WORK/'root/RESULT.json').read_text())['rate_tables'],'finite_periodic_comparator':json.loads((WORK/'challenge/REPLAY_RESULT.json').read_text())['finite_actual_output_spectra'],'quantum_codes_executed':0,'predecessor_scientific_suites_executed':0,'hardware_calls':0,'paid_credits_or_purchases':0,'outreach_public_hosting_access_changes':0,'code_selection_compilation_blocklength':'UNKNOWN_NOT_EXECUTED','physical_source_preparation_and_reset_cost':'UNKNOWN','total_discovery_inference_cost':'UNKNOWN','scope':'CPU/wall are observed bounded arithmetic subsets; final fresh relocated replay external receipt. Scalar tables do not simulate large quantum systems.'}
 write('COSTS.json',json.dumps(costs,indent=2))
 claims={'governing_proof_sha256':PROOF_SHA,'internal_status':'COMPLETE_SCOPED_PROOFS_AND_SOURCE_BOUND_AUDITS','source':'ACTUAL unchanged Omega with product nu tail','main_result':'B-R_pool=Theta_D(lnL),fixedL first,r→infinity/globalerror→0,thenL→infinity','finite_budget':'(1-2eps)lnN<=min(rB,rU+Iacc/2)+ElnJ+g(eps)','joint_target':'fixedPhi_N tensor actualcompletefinalresidual','known_general_machinery':'squashed entanglement; conditionalentropycontinuity; DW hashing; puritydecoupling','new_receiving_steps':'exactsourceentropy;observablelength;actualstatecoding;initialaccess/expectedstockbudget','strong_converse_for_pooled_rate':'OPEN','sharp_logarithmic_coefficient':'OPEN','efficient_code_construction':'NOT_ESTABLISHED','ordinary_stock_supply_formation_computation_advantage':'NOT_ESTABLISHED','historical_novelty':'UNKNOWN','physical_usefulness':'UNKNOWN','recipient_acceptance_and_integration':'UNKNOWN'}
 write('CLAIMS.json',json.dumps(claims,indent=2,ensure_ascii=False))
 write('CHECKPOINT.txt','Complete source-specific pooled order theorem and finite access/stock budget; three actual-source audits. Broader mission ACTIVE. One next owned question: sharp logarithmic coefficient/resource boundary. No code implementation, formation advantage or physical usefulness achieved.')
 copy(WORK/'REPLAY.py','REPLAY.py');copy(Path(__file__),'BUILD.py')
 audits=['studies/'+b+'/FINAL_ROOT_AUDIT.txt' for b in ['converse','coding','challenge']]
 for n in audits:assert PROOF_SHA in (OUT/n).read_text()
 payload=[]
 for p in sorted(OUT.rglob('*')):
  if p.is_file():payload.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)})
 write('MANIFEST.json',json.dumps({'archive_filename':OUT.name+'.zip','principal_proof_sha256':PROOF_SHA,'actual_principal_audits':audits,'payloads':payload,'self_authenticating':False},indent=2))
 archive=OUT.with_suffix('.zip');assert not archive.exists()
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(OUT.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(OUT)))
 with zipfile.ZipFile(archive) as z:assert z.read('sources/'+NATIVE.name)==NATIVE.read_bytes()
 receipt={'status':'BUILT','archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'principal_proof_sha256':PROOF_SHA,'payloads':len(payload),'exact_full_native_C9_preserved':True,'outer_compression':'lossless DEFLATE; extracted native source bytes exact'}
 p=BASE/'outputs/CYCLE10_ULTRA_BUILD_RECEIPT.json';p.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
