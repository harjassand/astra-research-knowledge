# Scheduled atomic capture, long retention, and sparse physical-port errors
30 October 2026. New synthesis and soft-phase proof. V2 local working theorem awaiting independent whole-source review. The binding same-envelope refinement is TWO_PARAMETER_MOMENT_FAMILY.md; V1 is preserved as a rejected incomplete draft. It does not claim a quantum factory or native two-site implementation.

## 1. Exact contract
There are arbitrarily many records with genuine classical instrument outcomes m_j. Conditional on the full m vector, each physical raw bit starts in |m_j> and DATA/bath can depend arbitrarily on m. Raw latches are noisy thereafter. Target bits can start arbitrarily dirty and correlated. The fixed-size noisy seed/reset/copy contract and its joint bounds are those in GENUINE_CLASSICAL_SEED_RECEIVING.md plus SEED_MIXED_RESET_SUBSET_LEMMA.md.

Use the literal nested bounded-degree expander prefixes, strict external-edge-energy majority primitives, fixed physical root ports, and scheduled soft-reset/sharpen/copy stages in the reviewed source bundle. The atomic majority dissipators have fixed body d+1, fixed rates and bounded per-site incidence; d and rates may be enormous constants. This is the declared physical resource, not a two-site compilation. Capture needs O(log n) scheduled stages and O(n) sites/site-time per record. The final graph remains on autonomously for a prescribed retention horizon H.

Actual perturbations have the existing bounded-q system-leg, per-site incident-cb, identity-annihilating, normal joint-system/bath contract, and the TOTAL actual evolution is CPTP. Arbitrary common-bath correlations and distant bounded-number legs are allowed. No independence, Pauli trajectory or positive signed-fault expansion is assumed. A bounded number of actual quantum read couplings may use each root as a Z-diagonal control. These commute all classical diagonal tests; arbitrary retained DATA does not change the classical theorem. It DOES NOT follow that the quantum DATA remains correct.

The conclusion concerns the actual simultaneous computational-basis error observables at physical root ports, relative to the historical m. A separate final detector is not assumed perfect. No classical analysis reference is a physical protected register.

## 2. Retention cannot use the growth site-time bound
For the final n-site graph, let P be the original-bit basin H_err<=delta n, U its edge disagreement energy, and F=exp(sU). On this cut the accepted atomic calculation gives

 L_maj^* F <= -a U F,   N^*F <= rho eta n F,
 U>=h H_err,  a>0.                                         (T1)

The naive factor exp(rho eta n H) is unusable for long storage. Replace F by

 G=I+exp(-alpha n)F.                                      (T2)

Choose b>0, alpha>sb, and a b>rho eta. The scalar inequality

 U exp(sU) >= b n exp(sU) - exp(sb n-1)/s

is pointwise in the spectral variable U. Therefore, on the cut,

 L^*G <= -(a b-rho eta)n exp(-alpha n)F + epsilon_n I,
 epsilon_n=(a/s) exp[-(alpha-sb)n-1].                      (T3)

In particular L^*G<=epsilon_n G. This is a scalar functional-calculus inequality, not an operator Jensen assertion. Rates/constants below are reduced as needed to reserve separate root/noise budgets.

## 3. Actual product/root inequality
Fix a selected record set R and future-mark subset E. Use

 H_A=(product_(j in E)G_j)(product_(j in A)Z_j), A subset R,
 Z_j=1+K V_j.

This joint inequality must be calculated, not inferred from separate expectations. A nominal majority move decreases both U and the full rooted V. If r=exp(-s Delta U), r>=exp(-sd), then

 Delta(G Z)=Delta Z + exp(-alpha n)F[r Delta Z-(1-r)Z].

Thus a fixed fraction of the rooted negative credit survives, while the second term retains the phase credit. Additive rooted vacuum terms are retained. For arbitrary local noise, a telescoping product-orbit estimate gives a PHASE contribution at most

 C eta sum_(j in E) n_j [exp(-alpha n_j)F_j/G_j] H_A

and a ROOT contribution at most

 C eta sum_(j in A) [K W_j/Z_j] H_A.

The phase fraction cannot be replaced by1 before applying (T3). It follows directly because N^*I=0 and the local relative oscillation of G_j is bounded by C exp(-alpha n_j)F_j/G_j; a term touches only a fixed number of factors. The rooted oscillation is the accepted localized estimate. This works for bath-coupled HP maps in the same complete-orbit convention; it does not put their distant legs into the expander graph.

After absorbing those two noise terms and choosing all constants with reserve, the actual killed generator obeys

 L^* H_A <= (sum_(j in E)epsilon_nj)H_A
            -sum_(j in A)gamma_j H_A
            +sum_(j in A)gamma_j z_*j H_(A without j),      (T4)

where gamma_j>0 and 1<=z_*j<=M, with fixed M close to1 when the rooted parameters are chosen accordingly. For j belonging to both E and A, deleting its root factor leaves G_j in H_(A without j). This is why the entire subset family is used.

The two-parameter positive-block norm in TWO_PARAMETER_MOMENT_FAMILY.md retains EVERY phase subset and root subset with one envelope pair. Normalizing each phase factor by w_j(t)=w_j(0) exp(epsilon_nj t) gives a contracting complete CP interval. Equivalently a selected phase subset pays <=exp(H sum_(j in E)epsilon_nj). Root moments do not accumulate a factor M at every stage or unit time. No quantum witness has been appended.

## 4. Retention exit has an exponentially large SOFT weight
A bounded-q' leg crossing P has an incoming source on at least one ket/bra with H_err>=delta n-q'. On P, (T1) gives

 G >= exp[(s h delta-alpha)n - s h q'].

Choose alpha<s h delta. The signed union-J insertion estimate in the simultaneous moment norm is therefore bounded by

 C_local product_(j in J) exp[-(s h delta-alpha)n_j/2+s h q'/2].  (T5)

The actual insertion incidence integrates to O(n_j H). The exact D-dependent nonnegative norm generating-SUM argument, not positive fault probabilities, gives a per-record retention-mark bound of the form

 p_ret(n,H) <= C(1+nH) exp[-c_ret n+H epsilon_n],             (T6)

with c_ret>0 and fixed C. An optional terminal cut contributes the same type of factor with no H. All constants include the ket/bra sector count and fixed primitive incidence. Equation (T6) is valid uniformly in the number of unselected records. Choose n so both H epsilon_n<=1 and (1+nH)exp(-c_ret n) are small. Thus n=O(log(H/epsilon)+log log(H/epsilon)) suffices for p_ret<=epsilon; an ordinary O(log(H/epsilon)) bound with a larger fixed coefficient also suffices. This is a theorem with potentially very unfavorable constants, not a practical overhead claim.

## 5. Receiving growth into the soft retention metric
The actual global growth phase transport is exp(rho_g n) per selected future-mark record, where rho_g=C_growth(epsilon_init+C eta), with the seed cost separately paid. Choose parameters in this order:

 0<rho_g<alpha<s h delta,
 0<sb<alpha,
 eta small enough for a b>rho eta and all root/growth reserves.

At the last growth endpoint, expand G=I+exp(-alpha n)F for every selected record. The JOINT TWO-PARAMETER growth moment family bounds every expansion term with the SAME positive envelope pair, including its rooted factors. Root-only normalization stays M^|A|; a phase subset C has extra normalization product_(j in C)w_j, with w_j<=C_seed exp(rho_g n_j). Consequently the extra per-record soft-phase cost is at most

 1+C_seed exp[-(alpha-rho_g)n],                            (T7)

rather than exp(rho_g n) charged throughout retention. Here C_seed is the fixed seed phase-moment constant, uniform on all subset indices. The exact identity for each output test is H_new_(B,A)=sum_(C subset B)e^(-alpha sum_C n_j) H_old_(C,A). Applying the SAME two diagonal envelopes term by term gives the displayed product bound, and defines the new w_j. Controlling only a single phase product would NOT suffice; that flaw is explicitly corrected in TWO_PARAMETER_MOMENT_FAMILY.md. This reception cannot be replaced by separate marginal moments.

The true current phase cut is retained when switching F to G. Records marked during growth have their phase metric dropped already and incur no retention phase cost.

## 6. Growth and initial marks
The reviewed seed supplies the initial union-mark factor p_init=3 sqrt(p_seed), with actual simultaneous envelopes as in the receiving note. The actual scheduled global phase/root proof and PRE-to-POST endpoint give

 p_grow <= C_seed sum_(k>=0) C(1+n_k)exp(-c_g n_k),          (T8)

where n_k grows geometrically, and c_g is the MINIMUM continuous-old-cut and new-endpoint exponent after paying attachment/noise prefix costs. The old-cut size is n_(k-1), so the bounded growth ratio is included in c_g. The sum is independent of final stage count. The seed size n0 is fixed first; then reset calibration and eta are chosen to make the exponentially weighted seed cost small. Increasing n0 without paying that seed cost is not allowed.

For every current remaining set, retain ALL phase subsets B and root subsets A in ONE simultaneous positive-block norm. A newly marked set J shifts the incoming phase index from B to B union J, charging product_J w_j and its source barriers, while leaving the root index A unchanged. Thus only newly marked records pay their pre-mark phase budget; unmarked records do not. Continuous insertions, stage endpoints, and the seed sector resolution use these SAME envelopes. The corrected flag counting argument and (T7) give

 ||v_D(T)||_(root family on S\D;M) <= p_mark^|D|,
 p_mark <= C[p_init+p_grow+p_ret(n,H)],                    (T9)

where fixed seed/soft-entry constants have been absorbed in C and the respective summands. It is not necessary to sum norms over flags outside S: the exact expansion coarsens to S by its verified algebraic consistency. This is a compatible family of signed-map bounds, not a positive distribution of permanent bad blocks.

## 7. Extract a POSITIVE physical-port error law
Let E_j be the actual projector that root j differs from m_j at the final time. Within its good phase cut, the rooted witness gives Z_j>=z_bad E_j, z_bad=1+K v0. Fix D subset S, U=S\D. For any simultaneous positive envelopes of v_D,

 Tr[(product_(j in U)E_j)Y_L,R]
    <=(M/z_bad)^|U| ||v_D||.

Weighted positive-block Cauchy--Schwarz therefore gives

 |Tr[(product_(j in S)E_j)v_D]|
    <=(M/z_bad)^|S\D| p_mark^|D|.

Sum the EXACT signed expansion rho=sum_D v_D. The left side for rho is an actual nonnegative measurement probability, and the binomial identity yields

 Pr(all ports in S are wrong relative to m)
    <= [p_port]^|S|,
 p_port = M/z_bad + p_mark.                              (T10)

This conversion is legitimate precisely because it is applied to the final physical commuting error projectors, after bounding each signed contribution. It does not assign probabilities to v_D. No marginal gentle-error sum appears. Averaging over genuine m preserves (T10), since every conditional estimate was uniform on m and its arbitrary conditional bath.

Choose rooted parameters to make M/z_bad small; choose n0/reset/noise as above to make capture marks small; choose n for the declared H to make retention marks small. Thus a sufficiently small but NONZERO fixed tolerance exists for every chosen fixed target port-error parameter. Hardware parameters are fixed independently of H and total record count. The source instrument, scheduled gates and primitive noise must satisfy the explicit model; no uniform claim survives arbitrary added read fanout or uncontrolled global noise.

## 8. Consequence and limits
This gives a concrete conditional-in-model classical resource: noisy physical raw outcomes can be captured by scheduled bounded-strength stages, retained for exponentially long declared horizons in their final block size, and exposed at fixed local ports whose simultaneous error distribution is local-stochastic with a tunably small constant. The hardware uses actual local majority/reset/copy operations; the animal sums, phase cuts and signed flags are proof objects.

The classical theorem permits actual Z-controlled reads and arbitrary common quantum DATA/bath, but does not establish correct quantum computation under those reads. A quantum receiver must handle their time correlation and strong marked-port histories, not merely consume (T10) as if faults were independent in time. Native two-site/onsite-reset compilation, autonomous acquisition scheduling, external detector qualification, the coherent-pointer-input variant, practical advantage and historical novelty remain unproved. This synthesis is a local working result pending an independent whole-proof review.
