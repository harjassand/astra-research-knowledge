"""Save the scored cross review in the reviewer's owned directory."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[4]
here = Path(__file__).resolve().parent
def artifact(path):
    p = root/path
    return {'path':path, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
baseline_ids = ['c08_s01','c08_s02','c08_s03']
baselines = [dict(worker=x, **artifact(f'outputs/round6/frozen_initials/{x}/INITIAL.txt')) for x in baseline_ids]
origins = {x:artifact(f'work/cycle6/{x}/INITIAL.txt') for x in ['c08_l01','c08_l04','c08_l07','c08_l10']}
claims = []
def add(worker, cid, claim, overlap, proof_status, score, repairs, dependencies, cost, evidence, origin=None):
    claims.append(dict(worker=worker, claim_id=cid, exact_claim=claim,
        origin=origin or origins[worker], baseline_overlap=overlap,
        proof_status=proof_status, contribution_score=score,
        score_scale='0 unsupported/duplicate; 1 useful diagnostic; 2 reusable lemma/counterexample; 3 acquired gate closed; 4 broader audited candidate',
        repairs=repairs, source_dependencies=dependencies, cost=cost,
        exact_review_evidence=evidence, historical_priority='UNKNOWN', external_validation='UNKNOWN'))

common = ['Smooth-volume flow with natural-log entropy',
          'Already supplied normal-cocycle/Ruelle entropy bound and stationary strain-power identity']
all_duplicate = {x:'Already supplied transport power inequality and exact entropy/strain mechanism' for x in baseline_ids}
add('c08_l01','power-bound-replay',
    'For a smooth nonvanishing divergence-free steady 3D flow, W >= 4 nu V h_mu(phi_1)^2.',
    all_duplicate, 'ANALYTIC_AUDIT_PASS_DUPLICATE',0,[],common,
    'No acquisition or force implementation. Proof replay; primary-source review only.',
    'Full INITIAL derivation inspected: strain decomposition, Ruelle, Cauchy and work integration are correct; this is common baseline content.')
add('c08_l01','recent-turbulence-source-interface',
    'arXiv:2506.20973v3 concerns asymptotic material-line growth in 3D turbulent flow and does not supply the volume-KS entropy/work theorem.',
    {x:'No new mathematical theorem over this frozen baseline; additional adjacent primary-source diagnostic' for x in baseline_ids},
    'PRIMARY_SOURCE_SCOPE_CONFIRMED',1,[],
    ['https://arxiv.org/html/2506.20973v3, Section II equations (1)-(2), stochastic eigenvalue/orientation model and Appendix A'],
    'No numerical or hardware evidence used. Source model assumes iid stretching factors and CLT/lognormal approximation.',
    'Primary HTML inspected: definition uses material-line length growth; Appendix A introduces iid factors and CLT/lognormal modeling. The exact KS claim is not inferred from it.')

add('c08_l04','intermittent-strain',
    'On one fixed connected Sol suspension with fixed H=a,V, delta_eps=c(b_eps-eps B1) gives Delta=c^2(eps B2-eps^2 B1^2)->0 but sup|s-H|->c>0; curvature grows as eps^-1.',
    {'c08_s01':'Same warped Sol entropy/volume interface; new intermittent fixed-height strain bump rules out a deficit-only L-infinity modulus.',
     'c08_s02':'Different from the transverse C1-small curvature bump: here peak strain stays away from equality.',
     'c08_s03':'Does not challenge the cone theorem, which includes a uniform strain/rotation certificate.'},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_IMPORTS',2,[],common+['Hyperbolic toral automorphism entropy H=a; supplied smooth nonnegative bump'],
    'Explicit one-dimensional metric. Supremum force/second derivatives can diverge; no bounded-actuator conclusion. No metric compiler acquired.',
    'Full bump integral proof and warped metric curvature formulas inspected. Identity follows by zero mean and change of variables; width eps concentrates fixed strain deviation.')
add('c08_l04','high-frequency-curvature',
    'u_n=at+n^-3/2 sin(2 pi nt) gives Delta=2 pi^2/n and unbounded curvature despite uniform strain convergence.',
    {'c08_s01':'Duplicates INITIAL diagonal warped-Sol high-frequency Ricci mechanism up to parameterization.',
     'c08_s02':'Weaker geometric boundary than its C1-small transverse scalar-curvature sequence.',
     'c08_s03':'No contradiction to the rotation/strain persistence certificate.'},
    'ANALYTIC_AUDIT_PASS_DUPLICATE',0,[],common,
    'Formal residual force; finite symbolic fixtures not an entropy or acquisition certificate.',
    'Full sin/cos proof inspected against own frozen INITIAL; s-H is an oscillation of amplitude O(n^-1/2), while u double-prime is O(n^1/2).')
add('c08_l04','exact-equality-collapse',
    'A_n=[[n,1],[n^2-1,n]], n>=2, covolume-one eigenlattice and X=partial_t/log(n+sqrt(n^2-1)) give V=H=1,W=4nu, inj<=1/(2(n^2-1)^1/4)->0 and |K|=log(n+sqrt(n^2-1))^2->infinity.',
    {'c08_s01':'New exact-equality collapse with changing manifold/monodromy; own INITIAL fixes one manifold and unit speed.',
     'c08_s02':'New global collapse boundary; its INITIAL addresses a fixed manifold and C1-near metric.',
     'c08_s03':'Its homogeneous Sol examples fix geometry; this sequence varies geometry and speed.'},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_IMPORTS',2,[],common+['Standard entropy of hyperbolic toral automorphism and constant flow rescaling'],
    'Changing integer monodromy, increasingly curved metric, speed 1/a_n->0. Geometry fabrication cost uncharged.',
    'Full lattice/short-loop proof inspected. Independent exact checks verify det A=1, diagonalization, covolume and short-loop squared length 1/sqrt(n^2-1). Noncontractible loop gives injectivity bound.')
add('c08_l04','covers-diameter',
    'm-fold Sol suspension covers have fixed H=a and zero deficit but diameter>=m/2.',
    {x:'New elementary global compactness boundary; volume is not fixed and grows as m.' for x in baseline_ids},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_IMPORTS',1,[],common+['Base-circle projection is 1-Lipschitz; entropy scales for the roof-m suspension'],
    'Volume and total work grow linearly with cover degree; no fixed-volume diameter obstruction is proved.',
    'Full projection argument inspected. Projection onto a circumference-m circle is onto and 1-Lipschitz, hence diameter at least m/2.')
add('c08_l04','zero-set-and-rescaling',
    'Disconnected active Sol fraction alpha and zero-field remainder give H=alpha a, W/(4nuV)=alpha a^2, Delta=alpha(1-alpha)a^2; constant rescaling preserves equality.',
    {'c08_s01':'Duplicates active/passive mixture sharpness in frozen INITIAL and common support scaling.',
     'c08_s02':'No added acquired coding/volume result beyond standard entropy decomposition.',
     'c08_s03':'Consistent with homogeneous field examples; no new gate.'},
    'ANALYTIC_AUDIT_PASS_DUPLICATE',0,[],common,
    'Disconnected example and arbitrary clock rescaling; does not construct connected zero set or fixed rate.',
    'Exact entropy decomposition and quadratic work scaling inspected; absolute small gap with H->0 is not a fixed-entropy obstruction.')

add('c08_l07','general-sl2-equality',
    'For an orthonormal left-invariant frame [E0,E+]=-aE+, [E0,E-]=aE-, [E+,E-]=beta E0 and X=vE0, a,v>0,beta!=0, H=av, Def X=diag(0,av,-av), W/V=4nu a^2v^2 and Scal=-2a^2-beta^2/2.',
    {'c08_s01':'Concrete non-Sol equality supplement; no improvement to quantitative projective defect theorem.',
     'c08_s02':'Explicit curvature/force algebra complements its warning about equality classification; local sl2 bracket branch was already a common classification possibility.',
     'c08_s03':'Extends its homogeneous Sol calculations to sl2 with a free beta parameter.'},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_IMPORTS',2,[],
    ['Supplied cocompact PSL(2,R) lattice', 'Smooth-volume Pesin formula for exact adjoint exponents (+av,0,-av)', 'Stationary strain-viscosity law'],
    'Finite symbolic algebra; lattice, entropy theorem and metric are supplied. No force apparatus, entropy acquisition or finite-bit certificate.',
    'Full proof inspected. Independently derived Koszul connection, strain, divergence of strain, scalar curvature and power all match. Entropy input is clearly separated from those exact algebra checks.')
add('c08_l07','sasaki-curvature-scale-equality',
    'INITIAL claims standard Sasaki metrics of curvature -kappa^2 have |Def X|^2=2kappa^2 and W=32 pi^2 nu(g-1) for all kappa.',
    {x:'New specialization claim, but false away from kappa=1; cannot receive contribution credit.' for x in baseline_ids},
    'REFUTED_EXACT_FRAME_AND_STRAIN_COUNTERCHECK',0,
    ['E+ and E- have inner product (1-kappa^2)/(1+kappa^2); they are unit but not orthogonal unless kappa=1.',
     'In the true Sasaki orthonormal frame, S_HV=(kappa^2+1)/2, |S|^2=(kappa^2+1)^2/2 and W/V=nu(kappa^2+1)^2.',
     'With V=8pi^2(g-1)/kappa^2, W=8pi^2nu(g-1)(kappa^2+1)^2/kappa^2. Equality holds only at kappa=1.',
     'Alternatively declare the stable/unstable eigenframe orthonormal by changing the metric, then recompute its volume; it is no longer the stated Sasaki metric.',
     'Correction request sent to existing c08_l07; INITIAL preserved. Peer acceptance/correction pending at review write time.'],
    ['Stated Sasaki brackets [X,H]=-kappa^2V,[X,V]=-H,[H,V]=X','Standard Sasaki volume and geodesic-flow entropy'],
    'Peer PASS script checks transformed brackets but omits transformed Gram matrix; outward rational intervals cannot repair wrong metric algebra.',
    'Independent exact checks: kappa=2 eigenframe Gram off-diagonal=-3/5; actual W/V=25nu while claimed bound equality would be 16nu. Full symbolic residual is nu(kappa^2-1)^2. General sl2 construction remains unaffected.')
add('c08_l07','fixed-flow-fixed-volume-zero-deficit-curvature',
    'On a fixed compact Gamma\\PSL(2,R), E0=-H/(2n),E+=e,E-=-nf/2 orthonormal gives the same X=-H/2 and dVol=4 Haar, entropy 1,W/V=4nu,zero deficit,Scal=-2/n^2-n^4/2->-infinity.',
    {'c08_s01':'New zero-deficit fixed manifold/abstract flow/volume obstruction; complements C1-near warped Sol small-deficit example.',
     'c08_s02':'New exact-equality obstruction in a non-Sol branch; its C1-near example remains stronger in convergence topology.',
     'c08_s03':'Uses growing frame anisotropy; no contradiction to supplied cone/condition certificates.'},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_IMPORTS',2,[],
    ['General sl2 equality calculation above','Fixed cocompact lattice and Haar volume','Smooth-volume Pesin entropy formula'],
    'Metric condition number diverges; |X|_gn=n. F=(4nu/n^2)X and its norm=4nu/n, while work stays constant. No metric construction cost or bounded speed premise.',
    'Full revision03 proof inspected; independent exact checks verify determinant1/4, fixed generator, entropy-power algebra and scalar formula. This is a post-exposure revision explicitly comparing c08_s01/c08_s02; attribution remains Luna-origin construction, no causal model comparison.',
    artifact('work/cycle6/c08_l07/revisions/03_FIXED_FLOW_FIXED_VOLUME_CURVATURE_BLOWUP.txt'))

add('c08_l10','supplied-positive-volume-symbolic-factor',
    'Given an invariant positive-volume E of fraction alpha with an exact iid q-symbol factor at clock tau plus readout error epsilon, INITIAL derives W>=4nuV alpha^2 r_epsilon^2/(beta tau^2).',
    {'c08_s01':'Conditional coding bridge is absent from frozen INITIAL, but normal-cocycle/power step is shared. Own later coding revision is excluded from the frozen baseline comparison.',
     'c08_s02':'Its volume-cell obstruction is a distinct nonrepeating-configuration admission; neither acquires this iid factor.',
     'c08_s03':'Its noisy strain compiler could certify dynamics under supplied regularity, but no factor/readout is acquired here.'},
    'ANALYTIC_AUDIT_PASS_BUT_REDUNDANT_READOUT_PREMISE',1,
    ['The ideal iid factor D already implies h_muE(phi_1)>=log(q)/tau irrespective of Dhat or epsilon.',
     'Localize the nonnegative dissipation to invariant E: W>=4nu alpha V(log(q)/tau)^2 for every E subset U, even if alpha<beta. The INITIAL beta bound is valid but weaker.',
     'To make error dependent throughput load-bearing, remove the ideal factor and admit a finite-block randomized encoder/readout with consistent invariant marginal, rather than quietly supplying the entropy-bearing factor.'],
    common+['Entropy monotonicity under factors','Invariant restriction of volume and Ruelle','q-ary Fano inequality'],
    'Symbolic factor, iid law, positive volume and clock are supplied. No encoder, sensor, reset, actuator, force or metric acquisition cost.',
    'Full Fano/block-entropy proof inspected and correct. Stronger repair: Ruelle on mu_E and Cauchy give h_E^2<=(1/alpha) integral_E s^2 dmu; since |S|^2>=2s^2, localized work gives W>=4nu alpha V h_E^2. Factor entropy supplies log(q)/tau directly.')
add('c08_l10','beltrami-source-power-conversion',
    'For the Cardona-Miranda-Peralta-Salas robust tape-bounded T3 construction with curl v=lambda v, W=nu lambda^2/(1+lambda^2)||v||_H1^2 >=(nu A^2/2) exp(2 exp(exp(B s_b))).',
    {x:'New source-specific sustaining-work consequence; frozen baselines do not contain this robust Beltrami H1 cost conversion.' for x in baseline_ids},
    'ANALYTIC_AUDIT_PASS_CONDITIONAL_PRIMARY_THEOREM',2,[],
    ['https://arxiv.org/html/2111.03559v3, Theorem2 and Remark3, source-specific H1 lower bound',
     'Same primary source Theorem25 and Section6: positive odd integer curl eigenvalue lambda',
     'Flat periodic H1 norm convention and strain Laplacian identities'],
    'Construction-specific tape reachability bound, no general cost lower bound or symbol throughput. Controller/metric/eigenfield acquisition and per-step time uncharged.',
    'Full local conversion inspected: curl eigenfield gives Delta v=-lambda^2v, advection=grad(|v|^2/2), p=-|v|^2/2,F=nu lambda^2v and strain work identity. Primary HTML confirms Theorem2/Remark3 and positive odd eigenvalue in Theorem25. No proof replay of the primary triple-exponential theorem; theorem correctness remains an import.')
add('c08_l10','computation-mixing-interface-diagnostics',
    'Reachability/null Cantor coding, Hodge-viscous stationary universality and H-minus-one stirring bounds do not supply a positive-volume, fixed-clock strain-power theorem.',
    {x:'Mostly shared interface cautions with source-specific detail; no new acquired gate.' for x in baseline_ids},
    'PARTIAL_SOURCE_AUDIT_UNKNOWN_FULL_AMBIENT_ENTROPY',1,[],
    ['Primary references named in INITIAL; this reviewer verified the Beltrami branch only', 'Other primary theorem proofs and ambient volume entropy remain UNKNOWN'],
    'Literature audit; no simulation, encoder or force implementation.',
    'No unverified ambient zero-volume-entropy extension is promoted. Distinct entropy, mixing, metric and viscosity interfaces are retained.')

out = dict(worker_id='c08_s01', phase='phase2_cross_review',
    utc_time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
    initial_preserved=artifact('work/cycle6/c08_s01/INITIAL.txt'),
    frozen_baselines=baselines, origin_initials=origins,
    independence='No peer output was read before own INITIAL; phase2 cross exposure was explicitly authorized. All review outputs and new code are owned; no peer script executed or file changed.',
    assigned_luna_review=['c08_l01','c08_l04','c08_l07','c08_l10'], claims=claims,
    cost=dict(exact_algebra_checks=artifact('work/cycle6/c08_s01/reviews/claim_checks.json'),
              script=artifact('work/cycle6/c08_s01/reviews/check_claims.py'),
              observed_checks=21, runtime_seconds=0.1642118329996265,
              dependencies='Existing Python3/SymPy1.14.0; no solver, hardware, downloads or peer-script executions',
              primary_web_scope='Two primary HTML papers for source-interface validation; no broad priority/novelty clearance'),
    result='No score3/4 acquired gate. Exact Sasaki error flagged and corrected formulas supplied; useful new counterexamples scored2 with imported entropy/source assumptions explicit.',
    causal_model_comparison='NONE: origin labels and contribution scores are descriptive, not causal model evidence.')
here.joinpath('CROSS_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'path':str(here/'CROSS_REVIEW.json'),'claims':len(claims),'status':'SAVED','maximum_score':max(x['contribution_score'] for x in claims)},indent=2))
