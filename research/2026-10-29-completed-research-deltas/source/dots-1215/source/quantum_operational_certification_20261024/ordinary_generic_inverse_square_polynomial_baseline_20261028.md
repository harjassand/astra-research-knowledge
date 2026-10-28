# Generic ordinary acquisition with polynomial processing at inverse-square accuracy

28 October 2026. Explicit composition baseline, not a new fast-accuracy theorem. It uses received ordinary local tomography, positive-model fitting, retained frames and decoder SDPs. Its purpose is to state accurately what is already possible and what the live R²/(gamma epsilon) target must improve.

## 1. Scope and theorem

Use the fixed four-real-coordinate isometric encoder family, a stationary/reset CPTP source, a valid encoded Choi-rank bound R, and the paid finite-horizon common-frame compiler. The shared effective output dimension is k<=8R. Full CPTP decoders are allowed. All probes are ordinary; no sender reference or coherent encoder selector is introduced.

There is a generic pre-datum learner with deterministic source cap

    N=O_tilde(R²/epsilon²)

and polynomial known-control/classical processing in the charged dimensions, 1/epsilon and precision, whose averaged implemented loss obeys

    E ell_alg<=ell_star+epsilon
              <=(1+gamma)ell_star+epsilon.               (1)

The comparator ell_star is the unrestricted full-CPTP optimum over the supplied encoder family. This is NOT the target fast inverse-accuracy rate. It also does not reconstruct a microscopic source environment. Its fitted positive lift is only a bounded prediction/feasibility variable for the observable ordinary family; no Bures-close Choi completion is asserted.

## 2. Ten actual fixed source settings and their conditioning

Take anchors e_i (i=1,...,4) and (e_i+e_j)/sqrt2 (i<j), for ten encoders. At each anchor prepare the ordinary loss density

    T_x=(1/6)sum_l E_x(P_l) tensor(I-P_l)^T.

Each iid copy costs one ordinary source call; the input label is discarded after preparing the receiver-local anti-state. Its dimension is d=2k and rank at most min(2k,3R). All ten banks and future operations use ONE retained frame, not independently chosen support coordinates.

Every matrix quadratic obeys

    T_x=sum_i x_i² T_ei
         +2sum_(i<j)x_i x_j
            [T_(ei+ej)/sqrt2-(T_ei+T_ej)/2].              (2)

If two such families differ in trace norm by at most a at each anchor, then

    sup_(||x||=1)||T_x-T'_x||_1<=7a.                     (3)

Indeed the diagonal part costs a, each off-diagonal bracket costs2a, and sum_(i<j)|x_i x_j|<=3/2. This is an explicit constant-conditioned interpolation map. It is not a boundary-safe Bures interpolation statement.

Put delta=epsilon/1024 and m=delta²/8. Acquire each anchor density tau_x with root-infidelity at most m, using the received finite-Clifford/random-purification Bures query. Fuchs-van de Graaf gives

    ||tau_x-T_x||_1<=2sqrt(2m)=delta.

Allocate joint ideal failure at most beta=epsilon/16 across the ten banks. Each bank uses O(kR log(R/beta)/m) copies, so the total is O_tilde(R²/epsilon²), with a fixed horizon. Receiver storage, random seeds, all failed/unused samples, local ancillas and source controls count.

## 3. Finite feasible positive-model fit

Use the received compact lift H on C^4 tensor C^2 tensor C^k:

    H>=0, Tr_output H_ii=I_2/2,
    Tr_output(H_ij+H_ji)=0 (i<j), Tr H=4.

Its real contractions J_x(H)=sum_ij x_i x_j H_ij are normalized CPTP Choi matrices; T_x(H) is the known linear six-state map. The true source is included. Hidden antisymmetric control coordinates are nuisance variables; they need not be learned or exposed. No optional unknown complex source-overlap constraint is assumed free.

Fit H subject to ten trace-norm cuts

    ||T_z(H)-tau_z||_1<=2delta.                          (4)

This is a literal SDP: introduce E_z^+,E_z^->=0 with T_z(H)-tau_z=E_z^+-E_z^- and Tr(E_z^++E_z^-)<=2delta. The data densities and coefficients have finite rational descriptions from the received estimator.

Here is a quantitative Slater witness on the simultaneous good event. Let H_c=I_(8k)/(2k) and alpha=delta/4. The proof point

    H_mix=(1-alpha)H_true+alpha H_c

has minimum eigenvalue at least delta/(8k), and its anchor discrepancy is at most delta+2alpha=3delta/2. Take the positive/negative parts of each discrepancy and add delta I_d/(16d) to BOTH. They are strictly positive with eigenvalue at least delta/(16d), while their total trace is at most13delta/8<2delta. All variables are bounded by the trace constraints. Thus the affine SDP has a polynomial-bit inner radius and compact outer radius.

The actual solver need not know this witness. Received finite weak SDP feasibility/optimization with these margins produces a rational exactly feasible Hhat, allowing cuts enlarged to at most3delta after certified arithmetic/affine rounding. Positivity and the TP affine equations are preserved by the same center-mixing/inward-rounding construction; an exact-real optimizer or unbounded condition number is not assumed. On bad histories the routine may return INCONCLUSIVE and deploy a fixed full-CPTP replacement. Its probability is charged.

Therefore, on the good event,

    ||T_z(Hhat)-T_true,z||_1<=4delta

at every anchor, and (3) gives a uniform trace-norm error at most28delta. Importantly, Hhat may be any feasible completion in the OUTER prediction class. It need not be the true global hardware Choi matrix.

## 4. Uniform task transfer and finite decision optimization

For any full decoder Choi C, ||C||<=2, so its actual loss difference satisfies

    |ell_true(x,C)-ell_Hhat(x,C)|
       <=(3/2)||C|| ||T_true,x-T_x(Hhat)||_1
       <=84delta.                                      (5)

This is simultaneous over ALL full CPTP decoders and all encoders. The loss coefficient remains positive because Hhat predicts a valid channel at each real x.

Optimize the KNOWN model on a normalized rational cube-face grid of chord radius h<=sqrt(epsilon/64). The grid has O(epsilon^-3/2) points and xx^T rational. At every point solve the full-CPTP decoder SDP to certified objective error at most epsilon/64, keeping a genuinely feasible decoder. Its strict feasible center C=I/2 and the received finite decoder-synthesis contract supply polynomial conditioning and executable known controls.

At a joint model minimizer (x*,C*), the fixed-C* loss is a nonnegative quadratic x^T B x, 0<=B<=I, and x* is a least-eigenvalue vector. A nearby grid point therefore costs at most h². This is a comparator discretization argument; no quadratic regularity is claimed for an arbitrary nonsmooth minimax landscape.

The selected ideal policy consequently obeys

    ell_true(selected)
       <=ell_star+168delta+epsilon/32 <ell_star+epsilon/4. (6)

Classical processing is polynomial in k,1/epsilon, the data/coefficient bit lengths and the number of acquired records: ten confidence cuts, a polynomial-size encoder list and polynomial-size SDPs. There is NO exponential decoder enumeration. The known source control and decoder circuits use the same retained frame and paid precision.

Bad records add at most beta=epsilon/16 because actual completed Bell loss is bounded by one. Allocate the remaining error budget to finite whole-record experiments, frame/compiler and deployed decoder/source controls, at the appropriate confidence or final operational scale. For example a total final loss debit epsilon/8 leaves ample slack in (1). The hidden mathematical frame is not an exposed support basis, and a record-averaged guarantee is not posterior quality for every exposed transcript.

## 5. Comparators and the precise open target

Together with `ordinary_full_decoder_exponential_menu_baseline_20261028.md`, the generic ordinary programme already has:

- O_tilde(R²/epsilon²), polynomial processing, by the fixed ten-anchor trace-precision route here;
- O_tilde(R⁴/(gamma epsilon)), fast accuracy but potentially exponential decoder-menu/design processing;
- sharper R²/(gamma epsilon) rates in the separately received structural families, and generic stronger-access/bootstrap routes under their paid seed/reference promises.

The unresolved generic strict-ordinary target combines fast accuracy, rank-squared dimension dependence and efficient global design/processing. New efficient matrix responses, paired Loewner envelopes and coherent row cones must be compared against these actual conventional baselines, not against full-environment tomography or a deliberately impoverished count learner. They currently improve available local interfaces; a valid encoder-dependent rank/error amortization theorem remains needed.

The received nonadaptive lower-bound family at fixed rank is consistent with this baseline: it requires inverse-square/log scaling for source-independent encoder settings and does not rule out an adaptive fast route.

## Evidence and dependencies

This is a transparent composition of `ordinary_bures_matrix_query_confidence_20261027.md`, `ordinary_convex_matrix_confidence_update_20261027.md`, the direct finite decoder/Bures recovery proof, and the paid common-frame contracts. It does not newly re-receive these imports. Its companion checks verify the factor7 interpolation, feasible-mixing margins and actual random physical encoder families. No simulated source bank, hardware execution or new optimality claim is asserted.
