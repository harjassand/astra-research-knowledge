#!/usr/bin/env python3
"""Root-adjudicated FZ curation data from frozen repository evidence only.

This creates a reviewable input, technology opportunity and descriptive workflow
trace. It does not apply scientific registries or publish a canonical checkpoint.
"""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parents[2]
I='updates/FZ-positive-memory-genesis-20261016/'
BASE='3dde9ce74d829a93388e64032d27351b36dd2221'
F=I+'SELECTED_FREEZE.v0002.json'
freeze=json.loads((W/F).read_text()); selected={x['path']:x for x in freeze['files']}
original=json.loads((W/(I+'SOURCE_MANIFEST.json')).read_text())
originals={x['path']:x for x in original['files']}
sources=[];evidence={}
BOUND='Internal analytic proofs, exact finite checks, acquired primary evidence and source claims remain distinct. External correctness, historical priority, physical acquisition and practical advantage are UNKNOWN unless explicitly scoped otherwise; all new high-impact claims remain source_derived_unreviewed.'

def ref(key,name,scope,original=False):
    path=I+'package/'+('originals/' if original else 'derived/')+name
    b=(W/path).read_bytes();text=b.decode('utf-8');n=len(text.splitlines())
    item=(originals if original else selected)[path]
    assert hashlib.sha256(b).hexdigest()==item['sha256']
    sid='src-FZ-SIG-'+hashlib.sha256((path+'\0').encode()+b).hexdigest()[:16]
    if not any(x['path']==path for x in sources):
        sources.append(dict(path=path,research_relative_path=name,source_id=sid,
          sha256=item['sha256'],bytes=len(b),lines_total=n,title=Path(name).name,
          read_depth='Selected load-bearing proof, model, evidence and audit ranges read directly by root or designated same-team investigators; indexing is not proof review.',
          provenance_role=item['provenance_role'],contains_external_fulltext=False,
          contains_external_dataset_or_clone=False,selection_status='ROOT_FROZEN_EXACT_BYTES',
          source_origin='supplied_original' if original else item['source_origin']))
    evidence[key]=dict(path=path,sha256=item['sha256'],lines=[1,n],range_scope=scope,
      read_path=path,hash_kind='original_utf8_bytes',source_revision=None,source_id=sid,
      research_relative_path=name,status=BOUND)
    return key

ref('positive_source','sources/positive_core_RESEARCH_REPORT.md','Incoming general-r exact singular/background calibration, proof and limitations.',True)
ref('positive_paste','sources/positive_core_report.txt','Incoming calibration report and missing verifier/source-reported run boundaries.',True)
ref('memory_source','sources/quantum_memory_report.txt','Incoming exact model, completed-CPTP extension and producer reconstruction claims.',True)
ref('reciprocal_source','sources/reciprocal_report.txt','Incoming reciprocal identities and degree-four/degree-six certificates; producer ZIP absent.',True)
ref('physical_source','sources/physical_report.txt','Incoming dynamic catalyst conditional calculation and proposed causal mechanism.',True)
ref('kinetic_source','sources/kinetic_investigation/REPORT.md','Supplied actual eight-site deadline model and numerical baseline, not a certified probability.',True)
for key,name,scope in [
 ('calibration','fz_positive_calibration_audit/AUDIT.md','Exact calibration identity, singular and open-cone QC, general-r constants and no-transfer proofs.'),
 ('calibration_checks','fz_positive_calibration_audit/EXACT_RECEIPT.json','54 exact identity groups; not universal finite-test validation.'),
 ('shear','fz_positive_representation_genesis/REPORT.md','Exact all-gradient acoustic shear elimination and unproved outer criterion.'),
 ('shear_scope','fz_positive_representation_genesis/ADDENDUM.md','Every quotient is Q>0; degenerate Q=0 case separate.'),
 ('shear_audit','fz_shear_elimination_audit/REPORT.md','Independent analytic reconstruction, mean-zero dual quotient and W2,4 potential qualification.'),
 ('conformal','fz_positive_conformal_genesis/REPORT.md','Attained divergence-free scalar stress dual, triangular margin and exact stronger-bound falsifier.'),
 ('fourier','fz_positive_conformal_genesis/EXACT_FOURIER_DIAGNOSTIC.json','Actual rational compatible map; ratio >2/3 but optimized Jensen energy positive.'),
 ('probability','fz_memory_probability_audit/AUDIT.md','Asynchronous envelope, forcing, stopped torus and homology reconstruction with explicit LSS/HT imports.'),
 ('memory_quantum','fz_memory_quantum_audit/REPORT.md','Quantum lift, CPTP completion distinction and sharp fixed-rate Choi calculations.'),
 ('bath','fz_memory_quantum_audit/PERSISTENT_BATH_THEOREM.md','Shared finite bath exact factorization and joint-input norm bound under exogenous schedules.'),
 ('bath_audit','fz_memory_bath_theorem_audit/DIRECT_PROOF_AND_AUDIT.md','Separate analytic bath/KL reconstruction, 94 finite checks and prior-art boundaries.'),
 ('bath_limits','fz_memory_bath_theorem_audit/COUNTERMODELS_AND_SCOPE.md','Fixed-decoder/location assumptions and continuous-bath Choi obstruction.'),
 ('receiver_audit','fz_memory_bath_theorem_audit/RECEIVING_SUPPORT_CERTIFICATE_AUDIT.md','Exact simultaneous event/fixed decoder quantifiers in source proof packet.'),
 ('choi','fz_memory_quantum_audit/SHARP_CHOI_RADIUS.md','Fixed-rate radius2nu/d² and optimized full-floor Hamiltonian rate, not maximal generator robustness.'),
 ('gram','fz_memory_structured_noise_genesis/STRUCTURED_GRAM_REGULARIZATION.md','Exact signed-GKSL catalog/range criterion and structured budget.'),
 ('gram_audit','fz_signed_gram_audit/SIGNED_GRAM_AUDIT.md','Independent complex/singular Schur reconstruction, constants and missing-product failures.'),
 ('memory_priority','fz_memory_priority_physical_audit/REPORT.md','Primary predecessor interfaces and bounded-density 3D range/routing lower bounds; priority remains UNKNOWN.'),
 ('reciprocal','fz_reciprocal_moment_genesis/REPORT.md','Exact order-two lower separator, degree certificates, passive embedding and stronger-incumbent limits.'),
 ('reciprocal_witness','fz_reciprocal_moment_genesis/EXACT_COUNTEREXAMPLE.json','Frozen denominator100000 functional, exact cut -897/10000.'),
 ('reciprocal_audit','fz_reciprocal_counterexample_audit/ANALYTIC_PROOF.md','Independent full moment/localizer/Bareiss/congruence proof, complex and passive embeddings.'),
 ('reciprocal_result','fz_reciprocal_counterexample_audit/EXACT_AUDIT_RESULT.json','Exact independent full-constraint audit, including36 bound products.'),
 ('reciprocal_cost','fz_reciprocal_moment_genesis/SPARSE_INTERFACE.md','Projected two-cone versus fourth-moment interface and complete unmatched solver costs.'),
 ('pglib','fz_reciprocal_moment_genesis/PGLIB_VERSION_COMPARISON.json','Recovered case/version generator changes; no solver run.'),
 ('kinetic','fz_kinetic_path_genesis/PROOFS.txt','Exact killed-envelope repair, acquisition/work limitations, full eight-site tail/nonexplosion and cap semantics.'),
 ('kinetic_integer','fz_kinetic_path_genesis/ADDENDUM_001.txt','K is a maximum over integer counts, not the real line.'),
 ('cap_audit','fz_kinetic_cap_certificate_audit/AUDIT.txt','Independent all-state diffusion, cubic tail, localized Dynkin and coupling/FSP proof.'),
 ('cap_exact','fz_kinetic_cap_certificate_audit/EXACT_AUDIT.json','Exact rational epsilon163<1e-9; no SSA or target-probability solve.'),
 ('deadline','fz_kinetic_obstruction_audit/FINITE_HORIZON.md','Finite-horizon replacements and exact failure of eventual-to-deadline transfer.'),
 ('kinetic_prior','fz_kinetic_obstruction_audit/PRIOR_ART.md','Exact primary antecedent for general work/second-moment inequality.'),
 ('physical_data','fz_catalysis_evidence_acquisition/authored/REPORT.md','Original workbook/SI acquisition, conditional reanalysis and corrected Wang regimes.'),
 ('physical_calculation','fz_catalysis_evidence_acquisition/authored/analysis_results.json','Recomputed chemical ratios and separate-waveform recorded terminal energy.'),
 ('causal','fz_catalysis_causal_genesis/CAUSAL_IDENTIFICATION.md','Conditional fresh-cohort theorem and hidden electronic/H/transport/retention countermodels.'),
 ('experiment','fz_catalysis_causal_genesis/EXPERIMENT.md','Proposed pre-admission pulse/sham common-read/chase, not executed.'),
 ('comparators','fz_catalysis_causal_genesis/COMPARATORS.md','Isotope/SSITKA and chemical product prior art; generic technique novelty stopped.'),
 ('capital','fz_current_capital_audit/AUDIT.md','Live main/PR content/head audit and actual external lift proof comparison.'),
 ('identity','fz_input_identity_luna/INPUT_IDENTITY_REPORT.md','47 supplied files and duplicate/missing-artifact identity audit only.'),
]:ref(key,'workers/'+name,scope)
for key,name,scope in [
 ('rate','STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0001.md','Root exact one-patch Pauli Choi minimum and box/ellipsoid theorem.'),
 ('rate_scope','STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0002.md','Zero-floor/range and receiving-cell qualification; versioned refinement.'),
 ('spatial','STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0003.md','Exact arbitrary-overlap common-cap spatial ellipsoid optimum; auditor refinement credited.'),
 ('synthesis','SCIENTIFIC_SYNTHESIS.v0001.md','Root substantive synthesis, priorities and methodology boundaries.'),
 ('adjudication','ADJUDICATION_ADDENDUM.v0002.md','Final scientific corrections and construction boundaries.'),
 ('scope','FINAL_SCOPE_NOTES.v0001.md','Exact independent continuation handoffs and current PR/source boundaries.'),
 ('workers','RESEARCH_INVESTMENTS.v0001.json','20Sol/1Luna actual assignments and unknown aggregate resource denominator.'),
]:ref(key,'root/'+name,scope)

# The existing theorem is read at the pinned baseline; no duplicate source ID is invented.
oldcard=json.loads((W/'frontier/cards/N877-global-h-completion-projection-and-finite-range-test.json').read_text())
oldref=oldcard['proof_availability']['located_proof_sources'][0]
evidence['old_completion']={**oldref,'lines':oldref.get('lines') or [1,len((W/oldref['path']).read_text().splitlines())],
 'range_scope':'Existing finite-H existence theorem allows a changed coefficient; it is not fixed-coefficient QC.',
 'read_path':oldref['path'],'hash_kind':'original_utf8_bytes','source_revision':BASE}

C0='N880-positive-sharp-calibration-and-conformal-elimination'
C1='N881-autonomous-memory-structured-noise-and-bath-interfaces'
C2='N882-reciprocal-order-two-separation-and-sharp-degree'
C3='N883-eight-site-kinetic-tail-certificate-and-deadline-repair'
C4='N884-fresh-cohort-catalysis-and-acquired-source-boundaries'
cards=[]
def card(cid,title,topics,scope,statement,proofs,assumptions,cost,acquisition,obstruction,comparator,missing,next_step,spine,paragraphs=(),status='Internally derived/reconstructed scoped theorem and exact evidence; external correctness and historical priority UNKNOWN.'):
 cards.append(dict(id=cid,title=title,topics=topics,scientific_scope=scope,statement=statement,
  reported_status=status+' '+BOUND,proof_availability='provisional_manuscript_available',
  internal_proof_status='scoped_internal_proofs_and_separately_marked_open_obligations',
  proof_availability_scope='Exact preserved analytic proofs, witnesses and same-team audits for the stated scopes; central capability obligations are explicitly open.',
  assumptions=assumptions,proof_spine=spine,proof_refs=proofs,inventory_refs=['identity','synthesis','adjudication','scope'],
  costs=cost,information_acquisition=acquisition,obstruction=obstruction,comparator=comparator,
  missing_lemma=missing,next_decisive_step=next_step,read_review_depth='Load-bearing source derivations and countermodels reconstructed by distinct assigned investigators; parent adjudicated their assumptions and read decisive proofs. Same-team checks are not independent external validation.',paragraphs=list(paragraphs)))
card(C0,'Positive sharp singular calibration and exact conformal reductions',
 ['quasiconvexity','compatible gradients','sharp quartics','convex duality'],
 'Unchanged positive sharp J_r on real2x2 matrices, r>0, periodic or zero-boundary W1,4 compatible tests.',
 'The exact Gram/determinant calibration proves strict QC at every singular background and an explicit open full-rank cone for every r>0. At r1 it gives fourth-order margin1/32 on singular backgrounds. At I and diag(1,-1), nonlinear acoustic-shear elimination has an attained unique convex inner optimum and an exact outer inequality equivalent to the corresponding conformal QC. A separate attained scalar-row divergence-free stress dual is equivalent at I. The universal outer inequalities and all-affine positive sharp QC remain OPEN.',
 ['positive_source','calibration','calibration_checks','shear','shear_scope','shear_audit','conformal','fourier'],
 ['Exact unchanged coefficients alpha=3r/[8(r+2)], beta=r(r-1)/6; no extraH.',
 'All compatible W1,4 tests, no orientation or finite-bandwidth promise.',
 'Every quotient criterion quantified Q>0; Q0 handled separately.',
 'Mean-zero L4 dual quotient and W2,4 Hessian potential when that representation is used.'],
 'Theorems quantify continuum functions. Inner scalar root closures require acquired slice integrals and precision. No affordable universal optimizer or coefficient-acquisition oracle supplied.',
 'Original pasted/detailed reports supplied; missing producer verifier/ZIP not replayed. Exact new proofs/checks preserved.',
 'Supporting calibration fails at I. Scalar/cofactor and simultaneous-two-shear shortcuts fail; exact stronger Fourier constant8/3 is false, while its actual Jensen energy is positive.',
 'Classical null-Lagrangians, Fenchel/direct method and rank-one convexity; two-sided isotropic and degree-one-root transfers fail their hypotheses. Existing finite-H completion may change the coefficient.',
 'Prove or violate the all-compatible outer source/stress-cost inequality, then address other r and nonconformal backgrounds.',
 'Prove conformal workerEq22 or shearEq16 under its exact class, or reconstruct and independently certify an actual negative compatible map. Seek external calibration review.',
 ['Exact general-r PSD calibration and integrated determinant cancellation.',
 'Compatible shear decomposition; joint convexity, direct-method attainment and conjugate elimination.',
 'Separate row-convex stress dual; exact compatible Fourier falsifier and analytic failed-class exclusions.'],
 ['At r1 a separate mixed singular margin1/44 is stated; the full-rank ratio cone is sigma2/sigma1<=1-sqrt(sqrt13-3). No positive all-affine theorem or Morrey resolution follows.',
 'The rational compatible diagnostic has ratio0.693155287785>2/3 but actual optimized Jensen energy0.233568631102>0.'])
card(C1,'Autonomous quantum memory: exact structured-rate and persistent-bath interfaces',
 ['quantum memory','CPTP uniformization','structured noise','fault-path correction'],
 'Internally reconstructed asynchronous4D toric sweep; completed CPTP correctors, exact code initialization, one fixed perfect decoder, independent sparse Poisson locations.',
 'Conditional on the universal location-only simultaneous Pauli-history certificate, arbitrary supported CPTP faults sharing a finite persistent bath factorize as Id_L tensor Lambda_B on every good schedule, including joint entangled inputs, and give joint-input diamond error<=2p_bad. Signed GKSL catalog uniformization is exact iff D PSD, a in rangeD and r>=Gamma+trC+a*D+a. For diagonal Pauli floors the exact minimum is sum gamma+sumh²/gamma; common-cap spatial box and global-ellipsoid optima are2max_c sum epsilon and2max_c sqrt(sum b²), respectively.',
 ['memory_source','probability','memory_quantum','bath','bath_audit','receiver_audit','bath_limits','choi','gram','gram_audit','rate','rate_scope','spatial','memory_priority'],
 ['4D geometric local support, specified compatible sizes, exact correction/initialization/readout.',
 'Fresh exogenous state/outcome-independent location law; arbitrary finite shared bath only at charged locations.',
 'Signed catalog includes required K/anticommutator directions and actual range conditions.',
 'Coefficient box versus one acquired global ellipsoid are distinct contracts; all support incidence charged.',
 'LSS/HT probability imports and completed-generator distinction retained.'],
 'All rates, center multiplicities, supports, coefficient conversions, deliberate floors, preparation/correction/readout/reset charged. Huge coarse constants supply no useful threshold. Bounded-density3D edge rangeOmega(L^1/3); faithful graph-minor routing additionallyOmega(L^9/2)sites.',
 '29 authored located-capital proof files separately preserved. HT primary acquired; original LSS full theorem pages inaccessible. No physical bath/architecture/noise bounds acquired.',
 'Memory-only Choi floor cannot absorb arbitrary continuous shared-bath Hamiltonians. Missing catalog product directions defeat every rate. A native bath supplies floors only where strictly positive rates are justified.',
 'Knill-Laflamme/operator-span and Poisson/Choi tools are established; shifted-jump identity has Shang-FrancaEq4 prior art. Primary sweep/Gibbs/qLDPC/coherent comparators have different precise interfaces; historical priorityUNKNOWN.',
 'External proof review of asynchronous classical universal event; useful constants and an acquired architecture. Continuous bath coupling requires a separate operation.',
 'Externally reconstruct whole-slab support, stopped-torus and accumulated-homology chain first. Develop realistic paid local-rate/geometry targets; no device or threshold promotion from quantum lift alone.',
 ['Classical location-only simultaneous certificate, under named imports.',
 'One fixed decoder corrects the operator span; bath coefficients retain chronological noncommutativity.',
 'Normalized Choi block/range proof yields exact supported proposal budget and optimal floors.'],
 ['Source lifetime claim is min(2,A L^4(1+kappa T)e^-cL), allT, under its model. Quantum steps do not reprove this probability estimate.',
 'Fixed-rate generic HP Choi radius is2nu/d², not maximal generator robustness. Full-floor Hamiltonian tolerance improves to d^-1 under an optimized paid proposal rate.'])
card(C2,'Exact reciprocal order-two separator and sharp universal degree',
 ['AC optimal power flow','moment relaxations','exact certificates','reciprocal cuts'],
 'Original voltage-box/fixed-power algebraic model, including a separately stated connected passive endpoint-current embedding.',
 'A normalized rational degree-four functional satisfies full M2, all original voltage localizers/equality multipliers, complex embedding and36 scalar voltage-bound products, but its lower reciprocal cut is exactly-897/10000. Therefore original unaugmented real order2 does not universally contain the lower cut; the explicit degree6 certificate makes order3 sharp in this stated class. Localized current upper bounds lower the sufficient order to2. No selected complete electrical-instance separation or solver advantage follows.',
 ['reciprocal_source','reciprocal','reciprocal_witness','reciprocal_audit','reciprocal_result','reciprocal_cost','pglib'],
 ['xu=yv1;1<=x²,y²<=4;1/64<=u²,v²<=64; all equality multipliers throughdegree4.',
 'Full complex-as-real45x45matrix; realM2rank13; all8localizersPD.',
 'Passive pathx--w--t--y, w=x-u,t=y-v, positiveunitconductances and explicitly broad interior voltage boxes.',
 'Interior powers, branch/generator/operating constraints are additional, unverified hypotheses.'],
 'Exact finite Fraction/Bareiss/LDL arithmetic. Two direct2x2Hermitian cuts versus larger fourth-moment interface; full separation/setup/conditioning/dual certification/runtime/memory costs unmeasured.',
 'Recovered exact PGLib blob and changed-generator version receipts; missing original decision ZIP not replayed. No commercial solver installation or network OPF run.',
 'Pseudo-moment is not a physical feasible point. Scalar current bounds do not furnish current localizers. No all-level extension/nonliftability or named stronger-incumbent claim.',
 'Full/sparse moment-SOS, current-localizer augmentation, QC/RLT/OBBT and certified conic/MILP baselines retain equal-information access.',
 'Test full pinned instance and matched strengthened solver with verified dual lower bounds and same feasible upper reference.',
 'Preserve hierarchy theorem; continue only with exact casebytes/all constraints and certified matched performance or a new full-instance separation.',
 ['Degree4 upper and degree6 lower polynomial identities.',
 'Exact rational full relaxation feasibility and negative lower cut.',
 'Invertible passive network pullback and original-bound preordering checks.'],
 ['The exploratory SDP was optimal_inaccurate and is not evidence for an optimum. Final exact rational witness establishes only the separation.',
 'An earlier candidate changed during audit; final bytes were frozen and checked separately. Earlier transcribed table passes but its overwritten original raw hash is unavailable.'])
card(C3,'Full eight-site kinetic tail certificate and finite-deadline repair boundaries',
 ['rare events','chemical master equations','Lyapunov certificates','finite-horizon sampling'],
 'Unbounded open2x4Schloegl network, eight counts initially50, firstentrymax<=15 byT1; exact decimal mathematical generator.',
 'V=sum(161/100)^ni gives a universal diffusion/local-cubic drift bound. Exact integer maximization through110 and a negative shifted cubic tail prove nonexplosion andP(any countreaches163 by1)<=7.569068427447863e-10<1e-9. Retaining0..162 gives a certified absolute truncation budget. Defect-killed supercaloric h-transform proposals give constant-weight Bernoulli estimators, but envelope acquisition and successful-path work remain. Eventual moment/work obstructions do not transfer to deadline1.',
 ['kinetic_source','kinetic','kinetic_integer','cap_audit','cap_exact','deadline','kinetic_prior'],
 ['Birth2.676n(n-1)+108.102;death.040n(n-1)(n-2)+37.881n; symmetricdiffusion8.2207nsource.',
 '20 directed open edges, maximumdegree3; rational decimal rates, notIEEE implementation.',
 'Integer K maximum at103; firstoverflow163, retained inclusivecap162.',
 'Killed-envelope theorem needs positive supercaloric g and exact hazards/terminal treatment.'],
 '111 scalar rational evaluations suffice for global bound. Retained box163^8=498311414318121121states remains too large directly. Envelope/derivative/successor acquisition and successful-path work are charged.',
 'Actual supplied model/baseline preserved; no billion-eventSSA rerun. Neither eight-site certified probability nor approximate accurate envelope acquired.',
 'Suppressed outward transitions give absolute-bias coupling, not one-sided FSP lower bound. FiniteT moments remain finite; the sourceeventual instability barely grows atT1. Missing efficient interior solve is central.',
 'Standard Lyapunov/FSP, killedhtransform/Snell/FeynmanKac, tensor/CME and splitting incumbents. General work-secondmoment inequality has exact Cugini-Atif-SubasiTheorem1prior art.',
 'Certified compressed finite-horizon interior representation/envelope and numerical residual/roundoff, with matched cost/accuracy.',
 'Use the new global tail budget to certify an inside solver; compare complete acquisition, memory and runtime to equally informed FSP/tensor/splitting. Park more eventual small-chain examples.',
 ['All-state pairwise diffusion inequality and local cubic negative-tail proof.',
 'Finite stopped-chain Dynkin and nonexplosion limit.',
 'Coupling/FSP semantics; killed-envelope likelihood cancellation and explicit boundary-risk/work costs.'],
 ['Reported source splitting mean~3.8e-8 has37%empiricalSE, not a certified reference. NeuralM85 distribution output is unmatched.',
 'No supplied IEEE sampler error bound, target probability, runtime superiority or physical parameter calibration is established.'])
card(C4,'Fresh-cohort catalyst causal test and acquired primary-data boundaries',
 ['experimental catalysis','causal identification','isotope tracing','energy accounting'],
 'Primary dynamicPdacetylene hydrogenation data and a proposed postwrite fresh-carbon cohort experiment; no new laboratory run.',
 'Original SI/workbooks reproduce conditional ethane ratio.2211756904, equivalent suppression7.766125527s and2.484329497events/Pd. A separate10s/1sV/Itrace integrates to.278055400742J; optimum10s/.1swaveform energy remains unavailable. Pulse/sham before fresh labelled feed with commonread/chase and completefate can exclude directoldproductpurge/conservative delay, but electronic memory remains nonidentified by exact hiddenH/transport/retention countermodels.',
 ['physical_source','physical_data','physical_calculation','causal','experiment','comparators'],
 ['Conditional carbonbalance, calibrated label attribution/exposure and complete chase closure for causal theorem.',
 'Acquired workbook aggregates are not raw chromatograms/siteinventory.',
 'Separate waveform, throughput, stability and electrolyte regimes not combined.',
 'Finite-record missingtag/error allowances applied before interpreting a freshcohort effect.'],
 'Switching/generator/feed/gas/solvent/heat/separation/reset and replacement costs remain distinct from recorded terminalVI. Complete matched usefuloutput and lifetime costs unmeasured.',
 'OriginalXuSI/Fig2/Fig6workbooks and separate5kHztrace acquired. Wangarticle/SI acquired;200hat2sccm is not100sccm two-cell regime. Optimumwaveform work, raw chromatograms and common-regime cohort intervention not acquired.',
 'HiddenH, reactive transport, retainedfreshproduct and localexposure remain observationally equivalent to electronicstate. Trace saturation and source caption/condition inconsistencies persist.',
 'Old carbontracer/SSITKA/subsurfaceH-C primary work; WangChem2026continuous polymer-grade product comparator. Generic isotope technique novelty STOP.',
 'Execute calibrated preadmission pulse/sham freshcohort commonread/chase; acquire completefate/exposure and matched optimum switching work/usefulproduct costs.',
 'Prioritize decisive freshcohort fate experiment and heldout preparations. Do not promote retained electronicstate or energyadvantage before complete measurement/cost gate.',
 ['Acquire exact originalprimaryworkbooks/SI and rederive condition-specificflux/work.',
 'Prove conditional freshcohort purge/delay exclusion with finite-record bounds.',
 'Construct hiddenstate countermodels; compare strongest source product regimes separately.'],
 ['No physical operation, calibrated transient kinetic model or useful technological advantage was acquired. Externalfulltexts/workbooks/rawarrays remain outside publicGit; sanitized hashes/URLs and authored analysis preserved.'],
 status='Acquired primary evidence and internally derived conditional causal test; experiment remains unperformed.')

notices=[
 dict(notice_id='SN-FZ-SIG-positive-sharp-still-open',card_ids=[C0,'N867-sharp-contact-face-and-quasiconvex-boundary','N877-global-h-completion-projection-and-finite-range-test'],issue='Unchanged positive sharp scope versus singular calibration and existential completion',clarification='New calibration proves exact unchanged J_r QC at singular backgrounds/open cone. Finite-H existence and two exact conformal reductions do not settle unchanged all-affine positive sharp QC or Morrey. Every1/Qcriterion hasQ>0 withdegeneratecase separate.',ref_ids=['calibration','shear_scope','shear_audit','old_completion']),
 dict(notice_id='SN-FZ-SIG-noise-interface-and-native-floor',card_ids=[C1],issue='Completed generator, input-independent clocks and structured floor scope',clarification='Bathfactorization and structured-rate formulas receive one universal simultaneous event with the fixed full decoder. Completed correctors, catalogrange/product closure, all proposalrates/incidence and actualpositive floors are required. Continuous bathHamiltonians and original allowedzero-rate baths are not silently admitted.',ref_ids=['bath_audit','bath_limits','gram_audit','rate_scope','spatial']),
 dict(notice_id='SN-FZ-SIG-order-two-lower-correction',card_ids=[C2],issue='Unsettled lower containment is now exactly separated in the displayed algebraic class',clarification='Final witness cut=-897/10000 passes all originalM2/localizers/equalities and a connected passiveendpoint embedding. Order3sufficiency is sharp for universalcontainment; pinnedcompleteOPF/strongerincumbents remainUNKNOWN.',ref_ids=['reciprocal_audit','reciprocal_result']),
 dict(notice_id='SN-FZ-SIG-eventual-deadline-and-cap-semantics',card_ids=[C3],issue='Finite deadline and absorbing versus suppressed cap',clarification='Eventualinfinitevariance/work do not transfer todeadline1. Exactdecimaloverflow163bounds retained0..162; suppressedcap hasabsolute bias, absorbingoverflowFSP hasone-sidedbracket. NoIEEE or insideprobability certificate.',ref_ids=['deadline','cap_audit','cap_exact']),
 dict(notice_id='SN-FZ-SIG-condition-specific-physical-evidence',card_ids=[C4],issue='Same-waveform and same-regime physical evidence',clarification='Separate10s/1s energy is not optimum10s/.1schemistry work. Wang200h/2sccm and100sccm/two-cell outputs are separate. Freshcohort test is planned, isotope method old, electronicstate notidentified.',ref_ids=['physical_data','causal','comparators'])]

def interface(objects,regime,information,guarantee,cost,access='Exact cited derivation under its source assumptions',acquired='No new physical operation acquired',units='Exact mathematical convention stated in cited proof'):
 return dict(objects=objects,regime_and_quantifiers=regime,supplied_information=information,
 acquired_information=acquired,legal_access=access,guarantee=guarantee,units_norm_and_precision=units,costs=cost)
bridges=[]
def bridge(slug,state,cids,source,destination,src,dst,align,missing,falsifier,srefs,drefs,proofs=(),counter=()):
 bridges.append(dict(id='FZ_SIG_'+slug,state=state,cards=cids,source_subclaim=source,
 destination_obligation=destination,source_interface=src,destination_interface=dst,alignment=align,
 missing_lemma=missing,falsifier=falsifier,source_ref_ids=srefs,destination_ref_ids=drefs,
 transfer_proof_ref_ids=list(proofs),counterexample_ref_ids=list(counter),ref_ids=list(dict.fromkeys(srefs+drefs+list(proofs)+list(counter)))))
bridge('finite_H_is_not_fixed_sharp','INCOMPATIBLE ASSUMPTIONS',[C0,'N877-global-h-completion-projection-and-finite-range-test'],
 'One finite ROCcompletion iff one finite QCcompletion, withcoefficients allowedtodiffer.',
 'QCofunchangedpositive sharpJ_r atallbackgrounds.',
 interface('Quartic quotientmodH','ExistenceafterdeletingH','Existingfinite-Htheorem','SomefiniteQCcoefficient','Completion magnitude/precision charged'),
 interface('FixedJ_r','Allcompatiblegradients/allaffineB','Exactsourcecoefficients','SamecoefficientQC','Noextracoefficientallowed'),
 'Existential projection cannot supply a fixed coefficient; singular QC and conformal equivalences preserve the open fibre.',
 'Prove unchanged all-gradient inequality or actual compatible negative map.',
 'A valid changed-coefficient proof cannot by itself discharge unchangedcoefficient conclusion.', ['old_completion'],['calibration','shear','conformal'])
bridge('universal_schedule_to_persistent_bath','PROVEN LOGICAL DEPENDENCY',[C1],
 'Same fixeddecoder corrects every Pauliword ononegoodlocation schedule.',
 'Joint-input factorization and2p_baderror forpersistent finitebath faults.',
 interface('Completed sweep and Pauli histories','Simultaneousovereveryhistory, exogenouslocations','Sourceuniversalcertificate andnamedprobabilityimports','Fixeddecoder scalaridentityoneachdecodedKraus','Allchargedlocationrates/geometry'),
 interface('Memory pluspersistentfinitebath','Everyjointlogicalbathreferenceinput','ArbitrarysupportedCPTP faultpolicies','Id_LtensorLambda_B ongoodh; diamond<=2p_bad','Freshlocationlaw retained; nocontinuousbath conversion'),
 'Operator-valuedPauli expansion preserveschronologicalbath products; fixedrecovery suppliescorrectablespan.',
 'Externalclassicalcertificate review andphysicalrealization remainmissing; no internalquantumlift lemma remains.',
 'State-dependentclocks, separatelychosen decoders orunscheduleddata interactions breakreceiver.', ['receiver_audit','probability'],['bath'],['bath_audit'])
bridge('signed_catalog_to_memory_rate','ESTABLISHED COMPATIBLE INTERFACE',[C1],
 'ExactChoi block givesCPTPproposal iffDPSD/arange/ratebound.',
 'AdmitstructuredHamiltonian/signeddissipativefaults atchargedPoissonrates.',
 interface('FixedfinitePauli catalogwithKclosure','FinitepatchsignedHermitianC/scalarh','Acquiredcoefficients/floors/supports','ExactCPTPuniformization andminimalrate','Allproposalratescounted'),
 interface('Universalgood-schedule memoryreceiver','Completedcorrector/exogenousbounded-supportproposals','Samegeometry/supportincidence','Inherited2p_bad bound','No usefulnumericalthreshold orfreephysicalfloor'),
 'Exactsupportedchannel representation suppliesreceiver, withfullrate andincidence conversion.',
 'Acquirecorrector/floors/noisebounds; externallyreviewprobabilitytail. MissingKdirectionsnotadmitted.',
 'Negativekernel/principalminor examples defeatmissingproductrange atanyrate.', ['gram','rate','spatial'],['receiver_audit'],['gram_audit','rate_scope'])
bridge('order_two_does_not_imply_lower','REFUTED TRANSFER',[C2],
 'Fulloriginalvoltage/fixedpowerorder2 anddegree4boundproducts.',
 'Universallowerreciprocalcutcontainment.',
 interface('Normalizeddegree4complexvoltagefunctional','AlloriginalM2/localizers/equalities','Exactrationaltable','Legalrelaxationpoint','Fraction/Bareiss arithmetic'),
 interface('Lowercutq²-z²','Sameoriginalalgebraicclass','Noextra currentlocalizers','WouldrequireLcut>=0','NofullPGLib/strongerincumbentclaim'),
 'The final legalfunctional hascut=-897/10000, includingconnectedpassiveendpoint embedding.',
 'Fullselectedcaseconstraints andpracticalbaseline remainunresolved; degree6sufficiencyretained.',
 'Executedexactnegativecut is the scopedfalsifier.', ['reciprocal_source'],['reciprocal'],counter=['reciprocal_audit','reciprocal_witness'])
bridge('global_tail_to_capped_deadline','ESTABLISHED COMPATIBLE INTERFACE',[C3],
 'AllstateexactdecimalgeneratorLyapunovoverflow<1e-9.',
 'Certifiedabsolute firsthit truncationerror forretained0..162.',
 interface('Unbounded8countCTMC','T1,init50,symmetricopen2x4','Exactdecimalrates','Poverflow163<=7.569068427e-10','111scalarevaluations'),
 interface('AbsorbingoverflowFSP orcoupledsuppressedcap','Same target/deadline/generatorinsidebox','Exactcapsemantics','FSPbracket orsuppressedabsolutebias','163^8statesandinsideaccuracy stillcharged'),
 'Couplingup tooverflow preserveshitdecision; absorbing andsuppressedversionshavedistinctdirections.',
 'Certifiedcompressedinsidesolve andIEEE/residualerror.',
 'Differentcapinclusion,unsymmetricdiffusion orchangedrates require anewbound.', ['kinetic'],['cap_audit'],['cap_audit','cap_exact'])
bridge('eventual_is_not_deadline_instability','REFUTED TRANSFER',[C3],
 'EventualPerronsecondmomentdivergence andeventual1/kappawork.',
 'Samequantitativeobstructionforfixeddeadline1.',
 interface('Eventualhittinglikelihoodestimator','Infinitehorizon','Exactsmallchain rates','Eventualmoment/workstatement','Expectedworkmayinfinite'),
 interface('Fixeddeadlineestimator','T1samefinitechain','Integratedmatrixexponential','Finitemoments;conditionalwork->1+lambdaT/2','Actualfirsthitoutput/relativeaccuracyretained'),
 'Finite-horizonmomentintegrals andsameparametercounterfamily disprove thenamedinference; sourceeventualtheoremretained.',
 'Anactualdeadlinework/variance/acquisitiontheorem matchedto8siteoutput.',
 'AtillustrativeparamsT1 growth1.00039912, noteventualinfinity.', ['kinetic_source'],['deadline'],counter=['deadline'])
bridge('fresh_cohort_to_purge_exclusion','ESTABLISHED COMPATIBLE INTERFACE',[C4],
 'Conditionalcompletefresh-cohortfateafterpreadmissionpulse/sham/commonread.',
 'Separatechangedfreshfeedprocessingfromdirectpurgeofoldcarbon/conservative downstreamdelay.',
 interface('Label-resolvednewfeedcohort','Allfreshcarbonadmittedafterwrite,commonread/chase','Calibratedexposure,tagclosure/errors','Oldproductcannotcarryfreshlabel','Acquisition/chase/calibrationpaid'),
 interface('Chemicaldecision','Sameconditionsandcompletefate','Distinctethylene/acetylene labels','Conditionalpurge/delayexclusion, notuniquelyelectronicstate','Work/reset/isolatedproductcomparisonstillrequired'),
 'Conditionalcarbonchronology andconservation supplythenarrowcausalcontrast; noexperimentexecuted.',
 'Acquirecommon-regime measurement/exposure/completefate; hiddenH/reactivetransportremainalternatives.',
 'Missingtag,changedexposure or retainedfreshproduct countermodels defeatwiderinference.', ['causal'],['experiment'],['causal'])

gates=[]
for slug,cids,title,question,passcond,refs in [
 ('UNCHANGED-POSITIVE-QC',[C0],'Unchanged positive sharp compatible inequality','Does the exact outer source or stress-cost inequality hold for every admitted compatible map?', 'Completeall-gradientproofatunchangedcoefficient, or independentlycertifiednegativecompatibleprimal map. Restrictedclasses,dualvaluebelow2, extraH orfiniteFourierminimado notpass.', ['shear','shear_scope','conformal']),
 ('MEMORY-CLASSICAL-EXTERNAL',[C1],'External reconstruction of asynchronous universal certificate','Does external review accept whole-slab support, stopped torus and accumulated homology with exact LSS/HT imports?', 'Reviewallload-bearingclassical/topologicalstepsatpinnedversions andquantifiers. Quantumspan/finitechecks do notsubstitute; keepinit/corrector/readoutmodel andnumericalconstants separate.', ['probability','receiver_audit','memory_priority']),
 ('MEMORY-ACQUIRED-NOISE',[C1],'Acquire structured corrector/noise/geometry','Can actual positive floors, completed correctors and supported coefficient promises coexist below a useful paid rate budget?', 'Samearchitecturecontrol/noiseacquisition, allincidence/preparation/reset/readout/3Dresources, usablethresholds andmatchedmemorycomparison; nomathematicalmodelpromotion.', ['gram_audit','spatial','memory_priority']),
 ('FULL-INSTANCE-OPF',[C2],'Identical full-instance certified comparator','Does the lower cut improve a fully specified identical electrical instance beyond matched strengthened methods?', 'Exactmodelbytes/allconstraints, verifiedduallowerandfeasibleupperbounds, matchedprecision/setup/separation/memory/runtime; standalonepseudo-momentisnotfullinstanceevidence.', ['reciprocal_audit','reciprocal_cost','pglib']),
 ('KINETIC-INSIDE-ACQUISITION',[C3],'Certified compressed finite-horizon interior','Can a compressed interior solve acquire the actual deadline probability/envelope under the global overflow budget?', 'Certifiedresidual/roundoffandabsolute/relativeoutputcontract, identicalgenerator/target/deadline, fullacquisition/evaluation/memory/runtime againststrongestequallyinformedFSP/tensor/splitting.', ['kinetic','cap_audit','deadline']),
 ('FRESH-COHORT-AND-WORK',[C4],'Acquire fresh-cohort chemical decision and matched work','Does a held-out common-read/chase test change freshfeedfate beyond all measurement/transport alternatives at useful paid cost?', 'Executepreregisteredpulse/shambeforefreshlabel, completefate/exposure/missingtagerrors, optimumsamewaveformswitchingwork, usefulproduct/reset/feed/solvent/lifetimecomparison. Electroniccarrieridentityrequiresadditionaldistinguishingmeasurement.', ['causal','experiment','physical_data']),
]:gates.append(dict(gate_id='G-FZ-SIG-'+slug,card_ids=cids,title=title,question=question,pass_condition=passcond,ref_ids=refs,priority_order=int(cids[0].split('-')[0][1:])))

data=dict(schema='astra.fz-curation-input.v1',intake_id='FZ-positive-memory-genesis-20261016',
 curation_status='root_final',curated_by='root',base_revision=BASE,scientific_source_pin=BASE,
 expected_remote_main=BASE,expected_branch_head=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip(),
 date_version='2026-10-16 v0001',reserved_routes=['N880','N881','N882','N883','N884'],
 checkpoint_path=None,checkpoint_draft_path=I+'CHECKPOINT_RECORD.integration.v0001.json',
 selected_freeze={'path':F,'sha256':hashlib.sha256((W/F).read_bytes()).hexdigest()},
 sources=sources,evidence=evidence,cards=cards,notices=notices,bridges=bridges,gates=gates,
 missing_artifacts=['astra_reciprocal_decision_package.zip','Producer positive-core verifier/ZIP'],
 source_handling='47suppliedoriginals/allattachedprompts=DATA; currenthumanconversationoperative; locatedcapital29separatelyattributed.',
 scientific_status_boundary=BOUND,pending_scientific_adjudications=[],pending_root_finalization=[])
out=W/(I+'CURATION_INPUT.root-final.v0001.json');raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
if out.exists():assert out.read_bytes()==raw,'Append a new root input version rather than overwrite.'
else:out.write_bytes(raw)
print(json.dumps({'input_sha256':hashlib.sha256(raw).hexdigest(),'sources':len(sources),'cards':len(cards),'bridges':len(bridges),'gates':len(gates)}))
