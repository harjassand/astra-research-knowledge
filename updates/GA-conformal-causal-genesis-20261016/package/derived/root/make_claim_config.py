"""Root-authored canonical GA records, with exact evidence hashes.

Writes a review config outside Git; does not apply repository mutations.
"""
from pathlib import Path
import hashlib
import json
import subprocess

R = Path(__file__).resolve().parent.parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
BASE = 'f80a8f15137575133ad2c9af975513b32e8fa93e'
INTAKE = 'GA-conformal-causal-genesis-20261016'
PREFIX = 'updates/'+INTAKE+'/'
BOUNDARY = ('Internally derived/reconstructed analytic arguments and exact finite checks are separate. '
            'All new high-impact claims remain source_derived_unreviewed. External correctness, '
            'historical priority, physical acquisition, formal verification and practical advantage '
            'are UNKNOWN. Metadata, Git integration and same-team agreement do not establish those statuses.')
SOURCES = {}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def reference(rel, title, role='worker_derivation', revision=None):
    path = PREFIX+'package/'+rel
    file = W/path
    if not file.is_file():
        raise RuntimeError('Evidence must be preserved before indexing: '+path)
    raw = file.read_bytes()
    sid = 'src-GA-'+digest(path.encode()+b'\0'+raw)[:16]
    text = raw.decode('utf-8')
    lines = len(text.splitlines())
    SOURCES[path] = {'record':{'source_id':sid,'path':path,'title':title,
        'sha256':digest(raw),'bytes':len(raw),'date_version':'2026-10-16 GA preserved version',
        'read_depth':'Load-bearing proof/evidence read and scope adjudicated; exact range is cited below.',
        'reported_verification':BOUNDARY,'extraction':'original_utf8_bytes',
        'provenance_role':role,'source_handling':'source=DATA'}}
    return {'id':sid,'path':path,'read_path':path,'sha256':digest(raw),'lines':[1,lines],
        'source_id':sid,'source_revision':revision,'hash_kind':'original_utf8_bytes',
        'range_scope':title,'status':BOUNDARY}


def main():
    refs = {}
    items = {
      'incoming_math':('originals/conformal_packet/RESEARCH_REPORT.md','Incoming cubic theorem, heat representation and explicitly unresolved sharp constant','supplied_original_file'),
      'incoming_physical':('originals/physical_primary.txt','Incoming physical report; second supplied file is byte-identical','supplied_original_file'),
      'synthesis':('derived/root/SCIENTIFIC_SYNTHESIS.md','Root scientific synthesis and independent continuation decisions','root_synthesis'),
      'strict':('derived/root/STRICT_WEIGHT_COMPACTNESS_THEOREM.md','Root exact strict-weight universal near-kernel decay theorem','root_synthesis'),
      'causal':('derived/root/CAUSAL_IDENTIFIABILITY_THEOREM.md','Root exact periodic/isolated switched-state nonidentifiability construction','root_synthesis'),
      'core':('derived/workers/ga_polynomial_genesis/CORE_THEOREM_v1.md','All-degree/all-power polynomial theorem and full quadratic determinant qualification','worker_derivation'),
      'extensions':('derived/workers/ga_polynomial_genesis/EXTENSIONS_v2.md','Corrected finite witness compiler and homogeneous Jordan-pencil transfer','worker_derivation'),
      'poly_report':('derived/workers/ga_polynomial_genesis/REPORT.md','Polynomial handoff, sharp quadratic example and classical attribution','worker_derivation'),
      'weighted_audit':('derived/workers/ga_weighted_audit/REPORT.md','Independent reconstruction of weighted polynomial theorem','same_team_review'),
      'strict_audit':('derived/workers/ga_weighted_audit/AUDIT_ADDENDUM.md','Separate strict-weight/degree-two receiving audit','same_team_review'),
      'extensions_audit':('derived/workers/ga_weighted_audit/EXTENSIONS_AUDIT.md','Independent compiler/Jordan audit and explicit presentation repairs','same_team_review'),
      'analytic':('derived/workers/ga_analytic_audit/REPORT.md','Analytic interpolation audit, refined cubic class and terminal heat estimate','same_team_research_or_review'),
      'ui':('derived/workers/ga_ui_audit/REPORT.md','Independent 15-dimensional cubic proof and isolated compatible witnesses','same_team_review'),
      'concentration':('derived/workers/ga_concentration_genesis/REPORT.md','Domain equality, quantitative concentration, diffuse clouds and moment closure','worker_derivation'),
      'concentration_audit':('derived/workers/ga_concentration_audit/REPORT.md','Independent local tail/area and cloud proof, including packing quantifiers','same_team_review'),
      'physical':('derived/workers/ga_physical_causal_audit/REPORT.md','Actual FZ originals, version reconciliation, acquired Lim prior art and causal gates','acquired_primary_literature_receipt'),
      'causal_audit':('derived/workers/ga_physical_causal_audit/AUDIT.md','Separate analytic audit of root switched-state theorem','same_team_review'),
      'priority':('derived/workers/ga_primary_math_prior/REPORT.md','Full primary Muller/interpolation/OpenAI Math proof comparison','capital_comparison'),
      'separated_prior':('derived/workers/ga_primary_math_prior/SEPARATED_SUBCLASS_PRIOR_ADDENDUM.md','Classical triangular-measure predecessor and two-profile scope blocker','capital_comparison'),
      'source_replay':('derived/workers/ga_source_replay/REPORT.md','Original ZIP manifest/verifier replay and exact calibration overlap','root_or_worker_executable_check'),
      'stress':('derived/workers/ga_sharp_invention/REPORT.md','Exact r1 nonlinear stress, rational Gram margin and full remaining mixed source','worker_derivation'),
      'stress_audit':('derived/workers/ga_nonlinear_stress_audit/AUDIT.md','Independent Fraction algebra and Sobolev audit of r1 calibration','same_team_review'),
      'mixed':('derived/workers/ga_sharp_invention/MIXED_SOURCE_CONTINUATION.md','Exact general mixed source and reserve-floor falsifier','worker_derivation'),
    }
    for key, (path,title,role) in items.items():
        refs[key] = reference(path,title,role)
    parametric = W/(PREFIX+'package/derived/workers/ga_parametric_stress_genesis/REPORT.md')
    if parametric.exists():
        refs['all_r'] = reference('derived/workers/ga_parametric_stress_genesis/REPORT.md','Exact all-positive-r nonlinear calibration and rational Gram certificate')
        refs['all_r_proof'] = reference('derived/workers/ga_parametric_stress_genesis/ALL_R_THEOREM_PROOF.txt','Complete analytic all-r stress-conservation theorem and exact identity')
        refs['all_r_certificate'] = reference('derived/workers/ga_parametric_stress_genesis/ALL_R_STRESS_EXACT_CERTIFICATE.json','Exact constant rational Q0/Q1 Gram certificate for every r>0','root_or_worker_executable_check')
        refs['all_r_audit'] = reference('derived/workers/ga_nonlinear_stress_audit/ALL_R_AUDIT.md','Independent exact all-r polynomial and positivity audit','same_team_review')

    specs = [
      ('N885-weighted-compatible-polynomial-and-strict-defect-classification',
       'Weighted compatible polynomial estimates and strict near-kernel decay',
       ['compensated compactness','compatible gradients','polynomial estimates','nonconstant rank'],
       'Fixed sigma>0; exact periodic gradients; nonzero homogeneous degree m>=3; finite 1<p,s<infinity; alpha/p+(m-alpha)/s=1, 0<alpha<=m.',
       'With weights b0,a1,c2,q2, the signed and absolute estimate has a finite constant iff the smallest exact monomial weight is >=2alpha. Universal uniformly integrable near-kernel little-o holds iff that weight is >2alpha. Degree-two signed estimates require quotient by the full gradient determinant. A corrected finite-frequency compiler constructs compatible exclusions; a fixed homogeneous double-characteristic pencil transfers by conditioned linear changes.',
       ['core','extensions','poly_report','strict','weighted_audit','strict_audit','extensions_audit','analytic','ui','priority'],
       'Seek scope-matched external review and closest priority; no optimal admissible constant or endpoint theorem supplied. The target alpha3/2 uses L6 and does not discharge the sharp L4 inequality.'),
      ('N886-critical-compatible-concentration-and-diffuse-clouds',
       'Critical compatible concentration and diffuse extremizing clouds',
       ['quasiconvexity','concentration','compatible gradients','defect measures'],
       'Fixed r>0; unchanged coercive J_r; A_r=1, Q_r>0; exact periodic or zero-boundary W1,4 gradients; one common integration measure.',
       'A nonvanishing normalized cubic requires fixed quartic energy at gradient amplitude comparable to Q_r^(-1/2) on a selected set of measure comparable to Q_r^2. Sharp ratio suprema agree across periodic/compact/zero-boundary domains. Disjoint exact clouds retain ratios and can approach diffuse measures without nonzero norm-preserving spatial profiles. The sharp Gamma_r<=1 obligation remains open.',
       ['concentration','concentration_audit','analytic','ui','incoming_math'],
       'A full sharp proof must retain fine-scale distributions or justify another selection operation. The cloud refutes an automatic finite-profile reduction, not quasiconvexity.'),
      ('N887-periodic-catalysis-causal-horizon-and-source-reconciliation',
       'Periodic catalysis causal horizons and acquired-source reconciliation',
       ['causal identification','dynamic catalysis','experimental acquisition','palladium'],
       'Observation interface: comparable static endpoints and representative periodic means; missing randomized common-hold products and independently bounded state/conditioning dynamics.',
       'Bounded positive stable one-state models exactly match static endpoints and a fixed periodic mean while both isolated and conditioned-next-pulse contrasts tend to zero over every fixed hold and conditioning time diverges. Acquired FZ source workbooks remain available despite the incoming run-local download failure. Fresh 2021 primary prior art stops generic prepare-then-react novelty. No new physical operation or technology advantage acquired.',
       ['causal','causal_audit','physical','incoming_physical'],
       'Acquire actual exposure, conditioning/withdrawal/recovery horizons, randomized fresh-carbon fate with complete chase, net ethylene benefit and full conditioning/read/reset work before mechanism or capability promotion.'),
      ('N888-nonlinear-separable-conformal-calibration',
       'Nonlinear separated-coordinate conformal calibrations',
       ['quasiconvexity','nonlinear stress','sum of squares','conformal backgrounds'],
       'Unchanged J_r for every r>0, every real s, periodic phi=(F(x)+H(y),g(x,y)); arbitrary W1,4 F,H and unrestricted compatible W1,4 g. A broader stress-conservation class is quantified at its fixed r,s.',
       'Exact nonlinear row stresses and rational positive Gram identities prove Jensen gap >=5r<|Dphi|^4>/[4096(r+2)]+r*s^2<a^2+c^2+d^2>/[512(r+2)] for every r>0. The separate r1 certificate gives the stronger bounds 1/256 and s^2/128. The stresses are divergence-free for the stated two-profile first potential. A one-phase nonseparated example has prior qualitative triangular-support coverage. Exact general mixed sources and a reserve-floor falsifier are preserved; no unrestricted positive-core QC theorem follows.',
       ['stress','stress_audit','mixed','separated_prior']+(['all_r','all_r_proof','all_r_certificate','all_r_audit'] if 'all_r' in refs else []),
       'Construct a nonlocal or richer correction controlling the exact general mixed-source pairing against the full Gram budget, or exhibit a compatible negative Jensen field. Seek external review/priority. Separation cannot be silently removed.'),
    ]
    cards=[];gates=[]
    for cid,title,topics,scope,statement,keys,obligation in specs:
        evidence=[refs[key] for key in keys]
        body=(f'{cid} | {title}\nstatus=source_derived_unreviewed; supplied claims and internal work remain externally unreviewed.\n\n'
              +scope+'\n\nExact statement: '+statement+'\n'
              +'Proof spine: See exact hash-pinned analytic derivations, independent receiving audits and separately scoped finite certificates below.\n'
              +'Costs and information: Continuum exact-gradient estimates do not supply a sharp solver or acquired physical parameters. Rational witness enumeration is exponential; full conditioning, precision, acquisition and reset costs remain charged.\n'
              +'Comparator/originality: Classical interpolation, Hodge/null-Lagrangian/SOS tools and primary predecessors are credited; no historical novelty clearance.\n'
              +'Failure and missing obligation: '+obligation+'\n\n'+BOUNDARY+'\n\n'
              +'Exact proof routes: '+' ; '.join(ref['path'] for ref in evidence)+'\n')
        status={'schema_version':1,'card_id':cid,'card_path':'cards/'+cid+'.txt','card_sha256':digest(body.encode()),
            'title':title,'topics':topics,'claim_status':'source_derived_unreviewed','reported_status':BOUNDARY,
            'scientific_scope_status':scope,'status_authority':'GA source-preserving internal research; '+BOUNDARY,
            'proof_availability':{'classification':'provisional_manuscript_available','classification_scope':scope,
                'internal_proof_status':'scoped_internal_proofs_and_separately_marked_open_obligations',
                'internal_status_boundary':BOUNDARY,'located_proof_sources':evidence},
            'validation':{'internal':'Distinct analytic constructions/audits and root adjudication; finite certificates have their stated algebraic scope.',
                **{key:'UNKNOWN' for key in ['external_correctness','historical_priority','physical_capability','formal_verification','empirical_confirmation']},
                'reported_status_evidence':[evidence[0]]},
            'depends_on':[],'supersedes':[],'invalidates':[],'material_updates':[],'contrasting_blockers':[],
            'requires_external_validation':[{'target':'external:scope_matched_review_and_capability','scope':obligation,
                'relation_status':'open; metadata/integration do not close it','evidence':[evidence[0]]}],
            'relation_coverage':'Selected exact interfaces; no exhaustive or topic-based implication.','reported_failed_attempts':[]}
        cards.append({'id':cid,'title':title,'topics':topics,'card_text':body,'status_record':status})
        for kind,question in [('REVIEW','Independently review exact proofs and closest prior art.'),('CAPABILITY',obligation)]:
            gates.append({'schema_version':1,'gate_id':'G-GA-'+cid.split('-')[0]+'-'+kind,'card_ids':[cid],
                'gate_kind':'explicit_proof_or_acquisition_obligation','title':kind.title()+' obligation: '+cid.split('-')[0],
                'question':question,'pass_condition':question+' Exact scope-matched evidence is required.',
                'status':'open','completion_evidence':[],'evidence':[evidence[0]],
                'priority_order':int(cid.split('-')[0][1:]),'priority_rationale':'Stable navigation order only; no impact ranking.',
                'validation_boundary':BOUNDARY})
    oldmath='N880-positive-sharp-calibration-and-conformal-elimination'
    oldphys='N884-fresh-cohort-catalysis-and-acquired-source-boundaries'
    notices=[]
    for suffix,ids,issue,text,keys in [
       ('original-verifier-now-available',[oldmath,cards[0]['id']],'Original supporting verifier availability',
        'The newly supplied nested ZIP contains exactly the FZ calibration report bytes and its original 24-group verifier now replayed; the previous missing-producer statement remains historical. Finite replay does not prove the analytic theorem.', ['source_replay']),
       ('norm-and-sharp-boundary',[oldmath,cards[0]['id'],cards[1]['id'],cards[3]['id']],'Fixed-coefficient sharp receiving boundary',
        'Finite compatible estimates, L6 decay and exact concentration theory do not supply Gamma_r<=1. The positive nonlinear calibration covers its explicit separated first-potential class; the general mixed source remains open.', ['core','concentration','stress']),
       ('physical-horizon-and-acquired-data',[oldphys,cards[2]['id']],'Acquired originals and causal horizon',
        'FZ originals were acquired; incoming download failure is execution-local. Static/periodic aggregates do not bound a one-pulse response or conditioning horizon. Generic pulse sweeping has 2021 primary prior art; causal acquisition and useful-output gates remain open.', ['physical','causal'])]:
        notices.append({'notice_id':'SN-GA-'+suffix,'card_ids':ids,'issue':issue,'status':'unreviewed_scoped_update',
            'clarification':text,'material_updates':[{'target':cid,'scope':text,
                'relation_status':'Reciprocal scoped update in this appended notice; old card/status bytes unchanged.'} for cid in ids],
            'source_refs':[refs[key] for key in keys],'source_revision':BASE,'whole_claim_invalidated':False})
    bridges=[]
    for bid,state,ids,src,dst,missing,keys in [
       ('L6_to_sharp_L4','INCOMPATIBLE ASSUMPTIONS',[cards[0]['id'],oldmath],
        'Finite alpha3/2 defect estimate with full-gradient L6 budget.',
        'Unchanged J_r all-compatible L4 quartic sharp discriminant constant.',
        'An exact constant-preserving L4 energy budget; no L6 promise is available for arbitrary W1,4 tests.', ['core','incoming_math']),
       ('cloud_to_finite_spatial_profiles','REFUTED TRANSFER',[cards[1]['id']],
        'Ratio-preserving disjoint compact clouds with diffuse limits and vanishing maximal local energy.',
        'Claim that nonzero/extremizing near-kernel loss automatically has finitely many nonzero critical spatial profiles.',
        'Such profile extraction needs an additional selection/renormalization theorem; explicit grid clouds refute the automatic statement.', ['concentration','concentration_audit']),
       ('periodic_mean_to_single_pulse','REFUTED TRANSFER',[cards[2]['id'],oldphys],
        'Comparable static endpoints and a representative periodic product average.',
        'A positive minimum isolated/conditioned single-pulse effect or finite conditioning/washout horizon.',
        'Acquired transient dynamics/state bounds; exact positive stable switched models refute the aggregate-only inference.', ['causal','causal_audit']),
       ('nonlinear_stress_to_separated_Jensen','PROVEN LOGICAL DEPENDENCY',[cards[3]['id'],oldmath],
        'Exact rational positive residuals and nonlinear row stresses for every unchanged J_r, r>0.',
        'Conformal Jensen positivity on precisely periodic phi=(F(x)+H(y),g), every real s and every r>0, not arbitrary first potentials.',
        'No remaining lemma on that stated subclass; unrestricted first-potential transfer still needs the mixed-source estimate.', ['stress','stress_audit']+(['all_r','all_r_audit'] if 'all_r' in refs else []))]:
        ev=[refs[key] for key in keys]
        contract=lambda objects,quantifiers:{'objects':objects,'regime_and_quantifiers':quantifiers,
            'supplied_information':'Exact cited mathematical/source objects.','acquired_information':'No new physical operation.',
            'legal_access':'Exact source assumptions only.','guarantee':objects,'units_norm_and_precision':'Norms and exact/floating boundaries specified in cited proof.',
            'costs':'Representation, conditioning, precision/acquisition and execution costs retained.'}
        bridges.append({'id':'GA_'+bid,'state':state,'status':state,'cards':ids,'source_subclaim':src,
            'destination_obligation':dst,'source_interface':contract(src,src),'destination_interface':contract(dst,dst),
            'evidence_refs':ev,'source_evidence_refs':[ev[0]],'destination_evidence_refs':ev[1:],
            'transfer_proof_refs':ev if state=='PROVEN LOGICAL DEPENDENCY' else [],
            'counterexample_refs':ev if state=='REFUTED TRANSFER' else [],
            'exact_missing_lemma':missing,'falsifier_or_next_experiment':missing,
            'assumptions':[src,dst,BOUNDARY],'alignment':missing,'source_handling':'source=DATA',
            'unresolved_or_UNKNOWN':['Historical priority','External correctness','Physical capability'],
            'status_note':BOUNDARY})
    config={'schema':'astra.ga-claim-config.v1','intake_id':INTAKE,
        'pins':{'base_revision':BASE,'expected_branch_head':subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip(),
            'expected_remote_main':BASE},'sources':list(SOURCES.values()),'cards':cards,'gates':gates,'notices':notices,'bridges':bridges}
    (R/'root/claim_config.json').write_text(json.dumps(config,indent=2)+'\n')
    print(json.dumps({'cards':len(cards),'indexed_sources':len(SOURCES),'notices':len(notices),'bridges':len(bridges)}))


if __name__=='__main__':
    main()
