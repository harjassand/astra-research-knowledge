# Count-acquired encoder selection in a growing real selector dimension

28 October 2026. **New constructive candidate; independent receiving in progress.** No sampled source experiment. All received locality and finite-time manuscripts remain unchanged. This addresses a growing known selector-state family, not arbitrary nonconvex circuit encoders. The conventional benchmark is active effect tomography/eigenvalue selection for a frozen receiver, not generic circuit optimization.

## 1. Actual ordinary interface

Let m>=1 be the selector dimension. For every known real unit vector x in R^m the learner can prepare the selector state |x> (or its explicitly supplied equivalent encoder V_x) at its actual known synthesis cost, freeze one physical receiver D, execute the ordinary global logical-state test, and receive ONE Bernoulli outcome y with

    Pr(y=1|x)=p(x)=x^T A x,  0<=A<=I_m.                  (1)

A is unknown. Counts, not its entries or expectation values, are supplied. Fresh reset calls make outcomes independent conditional on the chosen inputs and past history. In the common-algebra architecture this is the actual random-global-Clifford/stabilizer test of the frozen q-logical receiver, with p(x)=[2^q/(2^q+1)]ell(D E_x). Positivity and quadratic dependence imply a real PSD effect A; no PSD fitted estimator is assumed.

Given rational0<epsilon,gamma,beta<1, we seek p(x_selected)<=(1+gamma)lambda_min(A)+epsilon with high probability and a polynomial finite count/control cap. Known A would make this an ordinary eigenvalue problem. The issue is acquiring sufficiently accurate boundary information from actual Bernoulli records without an exponential sphere grid or a supplied low-loss region. The same procedure is available to the strongest equally informed conventional learner.

## 2. An efficiently sampled even fourth-moment design

Independently on every query, choose z by:

* with probability2/(m+2), choose a uniformly random coordinate vector e_i;
* otherwise choose m independent fair signs and put z=s/sqrt(m).

For m=1 the redundant mixture is harmless. This is an even/projective fourth-moment design, not literally an unsigned spherical4-design: odd moments are not used. An additional global sign on coordinate vectors would fix odd moments without changing physical pure states. Direct calculation gives

    E z_i z_j=delta_ij/m,
    E z_i^4=3/[m(m+2)],
    E z_i^2 z_j^2=1/[m(m+2)] for i!=j,

and every fourth monomial with an odd coordinate multiplicity averages to zero. Define

    T(z)=m(m+2)zz^T/2−mI/2,
    L_m=m^3(m+3)/4.                                    (2)

For every real symmetric F,

    E[(z^T F z)T(z)]=F,
    E T(z)^2=m^2(m+3)I/4,
    ||T(z)||_F^2=L_m.                                  (3)

Its support may be exponential, but SAMPLING is not: draw one uniform integer in{0,...,m+1}; two values select the coordinate branch, followed by one uniform coordinate index, while other values select m independent signs. No exponential list is generated or scanned.

## 3. Rational preconditioning and the exact acquired moment

Maintain an exactly rational positive envelope B with certified tau I<=B<=4I, where tau is a known dyadic floor. On the statistical good event it will also dominate the unknown A. Put Q=I−B/4 and choose integer

    K+1=(4/tau) ceil log2(32/tau),
    C=(1/2)sum_(k=0)^K [binom(2k,k)/4^k] Q^k.           (4)

The expression for K is integral because the floors below are dyadic. All matrices in(4) are exactly rational, and C COMMUTES with B because it is a polynomial in B. This commutation is needed for the following product inequalities; an arbitrary noncommuting C below B^(−1/2) would not suffice. The binomial series and0<=Q<=1−tau/4 imply

    0<C<=B^(−1/2),
    ||B^(−1/2)−C||<=1/16,
    (49/64)I<=CBC<=I,  C^(−2)<=2B.                      (5)

Indeed the tail is bounded by(2/tau)exp[−tau(K+1)/4]<=1/16. The construction computes a known input preconditioner, not a source inverse or hidden logical frame. Its O(tau^−1 log(1/tau)) rational matrix products are charged classical processing.

Prepare the actual known selector

    x=Cz/sqrt(s),  s=||Cz||^2,

obtain its one Bernoulli y, and record the rational matrix

    Y=y s T(z).                                         (6)

Both s and zz^T are rational even on the sign-vector branch. Thus Y is EXACTLY rational, although its normalized physical pure state is prepared to finite gate accuracy. On every good prior history A<=B, so F=CAC satisfies0<=F<=I. Conditional on that history,

    E Y=F,
    E||Y−F||_F^2<=E||Y||_F^2<=L_m/tau.                 (7)

To see the second inequality, use y^2=y and E[y|z]=(z^T Fz)/s. Then E||Y||_F^2=L_m E[s(z^TFz)]<=L_m/tau. No rare eigenvalue of the unknown A or source gauge is divided out. The only inverse floor is the learner-chosen tau. This is an actual acquisition law, not a synthetic whitening fixture.

## 4. Finite count confidence and matrix update

Set

    c=gamma/16, J=ceil log2(8/epsilon),
    tau_j=2^(−j), B_0=2I,
    b=smallest odd integer >=ceil log2(2J/beta).          (8)

At stage j=1,...,J use B=B_(j−1),tau=tau_(j−1), and independently collect b batches, each of

    n_j=ceil[2304 L_m/(tau_(j−1)c^2)]                    (9)

real source queries of(6). A batch mean is within Frobenius radius r=c/12 of F except with probability at most1/16 by Chebyshev and(7). Choose the FIRST batch mean having at least(b+1)/2 neighbors, INCLUDING itself, at squared Frobenius distance<=4r^2. If no such mean exists, abort to a prescribed encoder e_1. If a strict majority are good, such a mean exists and the selected Fhat is within3r=c/4 of F. Exact rational squared distances and a fixed tie rule make the decision finite without a numerical separation assumption. Independence of the fresh batches and an elementary binomial bound make the stage failure at most2^(−b); union over J adaptive stages costs at most beta. This is conditional on previous good histories, not an assertion of independence of the learned envelopes.

Reconstruct Ahat=C^−1 Fhat C^−1 exactly rational. On a good stage,

    −(c/2)B<=Ahat−A<=(c/2)B.                            (10)

Form Ahat+cB+tau_j I and symmetrically round it to the largest dyadic entry-grid step h_j<=c tau_(j−1)/(2m), explicitly h_j=2^(−ceil log2[2m/(c tau_(j−1))]). Nearest-entry rounding then has operator norm error<=c tau_(j−1)/4<=(c/4)B. Call the resulting rational candidate Bnew. Accept it only if exact rational PSD tests certify

    tau_j I<=Bnew<=4I.                                  (11)

If either test fails, safely abort to e_1; no infeasible physical preconditioner is ever used. On every good stage these tests pass. This is not a claim that spectral clipping preserves an unknown noncommuting Loewner inequality.

## 5. Uniform envelope invariant and final optimization

Let a=1/(1−2c). Inductively, on simultaneous statistical success,

    A+tau_j I<=B_j<=aA+2tau_j I.                         (12)

It holds at j=0 because A<=I. Equations(10) and the rounding reserve place the next B between A+(c/4)B+tau_j I and A+(7c/4)B+tau_j I. The lower side is strictly above the required floor. The looser upper coefficient2c closes(12):1+2ca=a and, with tau_(j−1)=2tau_j,4c*(2)+1<=2 because c<=1/16. Good-event matrices remain below4I, so the certificate guard does not truncate a successful history.

This is a UNIFORM matrix inequality on the entire selector sphere. It excludes the one-point-sign/whitening fixed-point shortcut: no guessed low-risk direction is silently assumed to contain the optimum. Full-rank positive envelopes keep every direction accessible throughout acquisition.

Finally compute a known unit vector x with certified Rayleigh slack

    x^T B_J x<=lambda_min(B_J)+tau_J/2.

A gap-free finite known-matrix eigensolver and paid state synthesis suffice; no empirical eigenvalue gap is assumed. Since a<=1+gamma/7 and tau_J<=epsilon/8,

    p(x)<=a lambda_min(A)+(3/2)tau_J
          <=(1+gamma)lambda_min(A)+3epsilon/16.           (13)

Thus the ideal-record high-probability target holds with substantial additive reserve. A bounded loss on exceptional histories and a separately paid whole-process operational discrepancy convert this into the desired averaged one-payload statement when beta and the discrepancy are allocated inside the total error target. Any final payload call is additional to the training cap below.

## 6. Complete finite resources, not merely an expectation oracle

The deterministic training upper cap is

    T_max=b sum_(j=1)^J n_j
       <=b[J+36864 L_m/(c^2 epsilon)]
        =b[J+9437184 L_m/(gamma^2 epsilon)].              (14)

Every attempted source call counts; aborted histories may use fewer calls but no observations are refunded. The source scale is O_tilde(m^4/(gamma^2 epsilon)), not a claimed optimal dependence on m or gamma. The important points are the fast inverse-epsilon dependence and polynomial dimension without an exponential action grid. This is a conventional active effect-tomography construction for a PSD quadratic, not a generic nonconvex-encoder algorithm.

For a finite random-bit cap, each uniform-integer rejection draw accepts with probability at least1/2. There are at most2T_max such draws. Truncate each at R=ceil log2(2T_max/nu_rng) attempts, abort safely on exhaustion and charge that probability to ONE operational budget. The random-bit upper bound is

    2T_max R ceil log2(m+2)+m T_max.

This includes the sampled exponentially supported sign branch without enumerating it. No rejected source observations or optional stopping are used.

All records, inverse matrices, moments and medoid comparisons are rational. The known preconditioner has lambda_min(C)>=7/16 and a polynomial-bit finite series. Dyadic update rounding resets stored-envelope bit length; all-history ||Fhat||<=m(m+1)/(2tau) bounds even bad arithmetic inputs. Exact rational PSD elimination, inverses and fixed finite matrix multiplication give polynomial arithmetic caps in m,1/epsilon,1/gamma and input bits. The displayed classical series cost is polynomial in1/epsilon, not falsely logarithmic. Exact ideal normalized rational vectors can be approximated to a prescribed trace-distance budget with known state-preparation circuits.

A dimension-m selector occupies ceil log2 m qubits after known padding, but arbitrary amplitude synthesis generally costs O(m) known two-level rotations before native compilation/routing and precision overhead; it is NOT poly(log m) control. Source-input V_x cost, all q-logical global-Clifford tests, the frozen physical D, classical processing and final eigenvector synthesis are paid. The total preparation/control/transcript discrepancy across T_max queries and one payload must be allocated in advance; for example a per-query trace discrepancy O(nu/T_max) makes the total O(nu). Finite rejection failures, rotation compilation, memory/control errors and final output preparation belong in that same ledger, not extra unreported failure events. No entangled reference crosses the source.

## 7. End-to-end transfer to the common-algebra family

For a genuinely growing physical selector, replace the old four-dimensional selector by a known m-dimensional real pure-state input, measured by the source in an UNKNOWN real orthonormal basis. Let its unknown branch Pauli probabilities and mixed gauge states define positive matrix-valued quadratics G_alpha(x), while the same unknown common logical U, local/approximately-local generator promise and global identity dominance remain. A unique perfect selector direction can be hidden among m branches; the learner does not receive that direction, the basis or the gauge matrices.

Every old uniform FOUR-anchor transfer must change. Define Gbar=(1/m)sum_(b=1)^m G(e_b). For any gauge vector v, positivity makes v^dagger G(x)v a PSD real quadratic form. Its largest eigenvalue is at most its trace, proving

    G(x)<=m Gbar.                                       (15)

Thus full-decoder regret transfer is m ell0_joint, not4ell0_joint. The supplied operator-margin assumption is still Hbar_ji>=kappa Gbar. In a special fixed-gauge scalar nonnegative-quadratic model, a PERFECT encoder gives aggregate visibility at least1/m rather than the former1/4. More generally the bound is the actual useful encoder visibility divided bym, not automatically1/m. This scale must be substituted into all inverse-kappa costs. A useful encoder alone does not automatically give that operator margin for arbitrary matrix-valued gauges.

The factor m can be genuinely necessary: take the proof-only identity-noise family E_x(omega)=omega tensor |x><x|, whose average gauge is I_m/m. A decoder applying logical Z only on gauge |e_1><e_1| has anchor-average virtual loss1/m but maximum regret1, exactly m times larger. This is a boundary witness, not an inverse/decoder supplied to the learner. Also, a perfect branch on gauge |0> and a depolarizing branch on orthogonal gauge |1> can have zero operator visibility on the latter sector; perfect recoverability somewhere does not license a positive global kappa.

The received approximate-local acquisition uses the ordinary m-anchor average, the same pooled-bank law and the same finite local controls.

Here its defining marginal is the NEW rho=U[(I/2^q) tensor Gbar]U^dagger, using the m-anchor Gbar in(15). Both operator margins and weighted proxy errors Tr rho(B−V)^2<=tau^2 are promised with respect to THIS marginal, not a former four-anchor state. A state-independent operator-norm tail, such as the received unitary locality bound, implies the new weighted promise directly. With that interpretation, the unchanged virtual bound is

    ell0_joint<=1980qA_geom tau^2/kappa+(225/2)qA_geom eta,

where A_geom is the received cone parameter, not the unknown selector effect in(1). Choose eta=epsilon/(4096m q A_geom), so its statistical decoder regret is225epsilon/8192<epsilon/20 and its structural floor is1980m qA_geom tau^2/kappa. Fine Bures tolerance becomes mu=kappa^2 eta/512; do not confuse mu with selector dimension m.

After this receiver is frozen, replace the old fixed-dimension scalar encoder learner by Sections1–6, using its actual global-test effect. If d=2^q, pass primitive tolerance[d/(d+1)]epsilon/8 so that conversion back to Bell loss costs at mostepsilon/8, and allocate decoder acquisition failure<=epsilon/16, selector statistical failure<=epsilon/16 and whole-process discrepancy<=epsilon/8. The resulting conservative averaged bound is

    E ell <=(1+gamma)ell_star+epsilon
                   +(1+gamma)1980m qA_geom tau^2/kappa.   (16)

The complete source cap replaces N_count, rather than adding a redundant old selector learner:

    2q c_loc N0+4C_loc c1 N_B
          +C_loc(R_max−1)N_pair+T_max+1.                 (17)

The coarse/fine/comparison constants are the received ones evaluated at the new eta and confidence allocations; the comparison term is zero when R_max=1. The final+1 is one q-logical payload. Each call consumes q logical input qubits PLUS ceil log2 m selector qubits in the literal realization, with the actual arbitrary-state synthesis cost just described, and n physical outputs. Same-information conventional learners get this entire architecture.

Section6's random-bit bound counts only the active selector primitive. The complete acquisition additionally uses uniform m-anchor draws, logical probe signs and global-Clifford sampling. Apply capped exact finite samplers to their predeclared complete call/control count as well, and charge every exhaustion or synthesis discrepancy within the SAME whole-process nu allocation. These extra private bits and controls are not covered for free by the primitive's displayed bit formula.

For exact local generators tau=0, this closes a polynomial growing-selector common-decoder construction. For the received finite-time local-evolution family, the tail must instead shrink with m qA_geom. A conservative transfer replaces q by m q in the already paid rational width cap and retains its full4^w cost; no fixed-width or linear-q/m reliability claim survives automatically. Arbitrary circuit-encoder families, unpromised global dominance, unknown model violations and non-reset predictive recovery remain outside the construction.
