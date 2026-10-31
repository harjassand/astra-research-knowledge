# Energy-resolved native receiving and a deterministic activity schedule

31 October2026. Separate candidate refinement. It does not change the frozen native proof, its practical resource ledger, or its accepted interpretation. The statement below is high-rate, certificate- and access-dependent. The ordinary low-rate fallback remains a global-action algorithm.

## 1. Inputs: three different quantities, not one renamed norm

Receive the exact acquired inputs of ../native_lyapunov_source_20261031/NATIVE_FULL_FIRST_EVENT_RECEIVING.md (f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192), with its whole receipt0fa56f50ca5160cbbbe9dc51c360f2b34b9e9e301894dc49c9ce6288d8cafeed. In particular G=sum D[L_a], L_a psi=0, H=sum L†L/2, gQ<=H<=hQ, G†H<=-kappa H, and PKP=0. Actual acquired stack and energy normalizations alpha_L,alpha_H remain paid.

In addition receive certified upper bounds

    0<rho<=b,  ||QKP||<=rho,
    e²>=||PKHKP||,
    a_E>=||H_Q^(-1/2) Q i[K,H] Q H_Q^(-1/2)||.

The inverse is a statement of a quadratic-form certificate, not an assumed inverse-H oracle. The original acquired K/b supplies the QQ block QKQ/b. Offdiagonal blocks QKP/(2rho) and PKQ/(2rho) must be ACTUALLY acquired as explained next. These parameters have distinct roles: e prices energy injection and physical jump activity; rho prices virtual excursions; b still prices QQ interactions, high-rate admission and generic offdiagonal acquisition. They cannot be substituted for each other throughout the old proof.

One may tighten e² to min(e²,h rho²), since H<=hQ implies PKHKP<=h PKQKP. Likewise the ordinary bound a_E<=2hb/g is available as a certified fallback, so a supplied larger a_E need not worsen admission. No optimal norm computation is assumed.

The accepted energy count addendum is ../native_lyapunov_source_20261031/ENERGY_WEIGHTED_ACTIVITY_ADDENDUM_CANDIDATE.md SHAac06ea4451f653db3824792b259a553057ca053639e59a784c87b6a2cbb320f3, with ENERGY_ACTIVITY_AND_RESOURCE_INDEPENDENT_REVIEW.md SHA4bb1b450ae3ba82b527655eabbbc97c5bc3034b92f173a70e35d10d9b5a68a48. Only its mathematical count/certificate portion is used; historical ledger labels do not affect this proof.

## 2. Actual offdiagonal operation and its cost

For a generic supplied K/b, use P/Q reflections to acquire QKP/b. If 2rho>=b, attenuation acquires QKP/(2rho). Otherwise ordinary slack singular-value amplification multiplies this block by b/(2rho). Its target norm is <=1/2, leaving uniform slack. The required polynomial degree is O(max(1,b/rho) times a polynomial logarithm of the requested error), and the original block precision is tightened by the robust transformation degree before use. Controlled inverses and phase synthesis are charged. The adjoint gives PKQ/(2rho). Thus an input rho is not automatically a cheap encoding: the factor max(1,b/rho) is real.

A separately acquired port can replace this generic SVA operation. OPEN_CHAIN_VARIANCE_NORMALIZED_PORT.md provides one concrete candidate: an open zero-field chain with individual A_i blocks, q_A²=sum alpha_i², and chi=40/39 admits a port of normalization chi q_A through an explicit domain-wall frame and a finite Neumann weighted-shift LCU. Attenuating gives normalization2rho, with rho=min(b,chi q_A) and branch-specific acquired access. Its gate costs include actual individual-operator SELECT, coefficient lookup, source preparation, index erasure and all precision work. A black-box K/b does not inherit that structural operation merely because its norm happens to be smaller on P/Q.

The rest of this receiving statement is conditional only on whichever offdiagonal interface is actually acquired. Zero rho is not treated by a nonexistent endpoint sampler: if the offdiagonal block is certified zero but b>0, use any supplied positive upper bound, such as rho=b, and pay it. If K is certified zero use the frozen B=0 branch. No exact operator-zero test is introduced.

## 3. Scaled parameters, physical count and admission

Use the same gap normalization H->H/g,L->L/sqrt(g),lambda->lambda g,K->K/sqrt(g), and unit time interval as the frozen theorem. To keep formulas unambiguous define from the ORIGINAL physical parameters

    mu=lambda g T,
    B_diag=b²T/g,
    R=rho²T/g,
    B_off=4R,
    C_E=e²T/kappa²,
    Hs=alpha_0 T.

The energy parameters and acquired encodings inside the normalized kernels are h/g,kappa/g,alpha_H/g,alpha_L/sqrt(g). Denote these by hN,kappaN,alpha_HN,alpha_LN. The allowed tilt is unchanged: u=min(1,kappa/(16h)), theta=log(1+u).

The high branch requires BOTH

    sqrt(lambda)>=64b/g,
    sqrt(lambda)>=8a_E/kappa.

Use certified overlapping branch intervals as in frozen Section11, not exact comparisons to arbitrary reals. The second inequality is the energy-count condition; the first supplies the scalar virtual-word separation, irrespective of how small e or rho is. The count receiver gives for arbitrary initial source/system/reference and p prescribed joint instruments

    E exp(theta N(T))<=2^(p+1) exp(32u C_E).

Thus take

    M=ceil(((p+1)log2+log(1000/epsilon)+32u C_E)/theta)+2.

The leading driven term is O(C_E), whereas the initial-state, intervention and tail term remains O(max(1,h/kappa)[p+log(1/epsilon)]). The initial source is not assumed dark, and interventions may inject energy. Their cost is not erased by replacing the global count coefficient with e.

## 4. New scalar majorant, not a global b substitution

Let

    c_off=sqrt(mu B_off)=2sqrt(mu R),
    c_diag=sqrt(mu B_diag), r=mu/2, delta=r-2c_diag,
    nu=sqrt(delta²+8c_off²), d=(nu+delta)/2,
    s=2c_off²/d.

The acquired fast source kernel remains EXACTLY the frozen

    F(z)=(1/2)Q exp[-z(H/g-Q/2)]Q.

It is unchanged by the coupling normalization. Its derivative, LCHS cutoff and precision costs are the same.

P/Q crossings have scalar weight c_off times their acquired norm-one blocks; a QQ insertion has scalar weight c_diag times QKQ/b. Every Q dwell still has factor2. Therefore the exact positive endpoint word sum is

    Mpos=[[0,c_off],[2c_off,-r+2c_diag]],
    E(t)=exp(Mpos*t) diag(1,2)
        =diag(1,sqrt2) exp([[0,sqrt2*c_off],[sqrt2*c_off,-delta]]t)
                          diag(1,sqrt2).

Every interaction insertion, including QQ, carries (-i). Actual damping jumps do not receive an extra phase. The only changed coefficient in the fast diagonal is c_diag, NOT c_off.

Because rho<=b and mu>=4096B_diag, c_off<=2c_diag, delta>=15mu/32, c_off/delta<=1/15, and 2c_diag/d<=1/15. In particular all the weaker frozen inequalities c_off/delta<=1/6 and self/down ratio<=1/3 hold. Also

    s<=16 B_off/3.

The exact E entries from the frozen proof hold with c0 replaced by c_off and delta as above. Consequently the same scalar bounds give

    alpha_no=8exp(s*tau),
    alpha_jump(t)^2=256alpha_LN² exp(2s*tau)
                                      [mu exp(-2delta*t)+4B_off].

The physical event is still sqrt(mu)(L/sqrt(g)) K0(t), with its actual source/color output. When tau<=1/(128B_off), the integrated proposal mass is <256(1+2alpha_LN²), so the SAME padded Aamp and complete-isometry amplification apply. Neither the physical stack normalization nor its h/g dependence has disappeared.

## 5. Deterministic schedule and actual H0 action

Choose

    D=128B_off+M+p+log(100/epsilon)+4,
    1/(2D)<=tau_max<=1/D

as a certified dyadic window. Split additionally at prescribed controls. Set W=ceil(1/tau_max)+p+1 and S=M+W+2. Then S=O(D) and, directly,

    S*tau_max <=1+(M+p+4)*tau_max <=2.

Changing ceiling safety margins by a fixed number only changes this absolute bound by a constant. In particular the total call count remains linear in the same capped activity; smaller windows have not introduced an extra factor M. They preserve the envelope condition because D>=128B_off. The count/error counter is global and PRIVATE; the source is never reset.

For every one of the Kcap+1 padded word intervals, implement a B_time-bit H0 duration by B_time controlled fixed binary-fraction evolutions. Their durations sum to at most T*tau_max PER SLOT, independent of the realized path. With a qubitization-capable H0 block, its query action across S*dA base calls is bounded by

    O(alpha_0*T * dA*(Kcap+1)),

using S*tau_max=O(1), plus the actual per-piece synthesis/query overhead O(S*dA*(Kcap+1)*B_time*polylog(1/error)). This is worst-window accounting, not the unproved claim that coherent pathwise durations can be added for free. Each fixed-time Hamiltonian query's gate cost remains paid.

## 6. Re-bound finite source, precision and private-clock ledger

The two-state Doob bridge now has up rate s and down rate d from Section4. During each fast residence add Poisson(2c_diag*ell) QQ points. Thus the self-count parameter is gself=2c_diag, while the offdiagonal bridge is controlled by c_off. Since gself/d<=1/3, the same independent-full-visit domination yields E2^V<=4exp(7s*tau). For endpoint duration>=t0, p0=s*t0/(1+nu*t0) remains valid. Hence the frozen conditional cap Kcap and no-rejection finite bridge sampler apply with these ACTUAL rates.

The distinctions in the finite-error ledger are load-bearing:

* Compute e_step,beta,sigma,eta from the NEW S and unchanged dA. The source energy count replaces only M.
* Physical generator norm uses the REAL full coupling: Lphys=1+2Hs+2c_diag+2mu alpha_LN². It is not reduced by replacing b with rho.
* The outer proposal's decay is 2delta and its floor is proportional to sqrt(B_off). Thus use Lout=1+delta+sqrt(mu/B_off)(Hs+c_diag+mu hN). All positive-parameter inverse factors enter numerical precision through their logarithms, as in the original source.
* Use qrate=nu+gself in the near-boundary/tie cut, and gself in Poisson interval TV changes. Use the original endpoint probability only once in conditional tail and tie bounds; do not multiply marginal bad-event estimates.
* Recursive duration TV stability and finite CDF/bisection source compilation are unchanged after this explicit rate replacement. Global QQ-plus-crossing virtual count is capped; overflow selects zero without resampling.
* Word timing still costs Hs+mu(alpha_HN+1), because the fast kernel is unchanged. It is NOT replaced by the smaller rho or e. Every interval kernel receives its actual finite LCHS precision.
* Each offdiagonal call's error budget must include its real SVA degree/normalization or the actual structural-frame operation count. Its tighter raw precision and gates are added, not hidden by changing a scalar coefficient in the proof. QQ calls keep the original K/b access cost.
* Continuous and rounded timestamps are compared through the SAME outer uniform coordinates and L² amplitudes. The complete first-event isometry is amplified while contraction failures remain coherent. Afterwards only private continuation uses the sampled time, with the count-augmented future-channel Lipschitz bound Lphys. Actual source output and prescribed instruments are retained.

All remaining numerical expressions (xmin,t0,du,zeta,pz,Lker,h_time and per-operation subdivisions) are exactly those of frozen Sections7–8 with these explicit variable assignments. Every hypothesis used there has been checked above: positive rates, original endpoint floor, bounded window, geometric self-count, acquired contractions, source derivative, actual stack, uniform physical count and complete isometry. The same proof therefore gives complete trace error <=epsilon. This is an explicit receiving substitution, not an inference from a smaller expected number of jumps alone.

The logical access costs are paid even when the quantities appearing only logarithmically in Kcap are very small. In particular generic offdiagonal SVA costs b/rho, not log(b/rho); the structural source construction is a separate way to avoid that factor. b=0, lambda=0 and T=0 use the frozen direct branches. A certificate rho=0 without zero K does not invoke these branches; use a positive upper bound as in Section2.

## 7. What near-linear activity means here

Let

    Z=1+C_E+R+max(1,h/kappa)[p+log(1/epsilon)].

Then M+B_off+p+log(1/epsilon)=O(Z), hence S=O(Z). The virtual cap and source precision are polynomial logarithms of S,1/epsilon,2+mu and the encoded positive parameters. The fast-kernel cost is polynomial in the acquired source conditioning and logarithmic requested precision, not in lambda*T. Therefore the high-branch query/gate bound has the form

    source_conditioning_polynomial * polylog(parameters,error)
       * [Z * actual_base_operator/source_cost
          + alpha_0*T * actual_H0_query_cost],

with the explicit Aamp=O(1+alpha_L/sqrt(g)) and Kcap factors retained in those products. A generic supplied K encoding contributes its real max(1,b/rho) offdiagonal amplification cost. The concrete open-chain frame contributes its own near-linear-n lookup/preparation cost instead. The bound is near-linear in the displayed extensive activity and H0 action only AFTER those source and access factors are fixed or explicitly multiplied. It is not a near-linear total-n circuit theorem, an optimal exponent, or a practical gate estimate.

Initial source energy capacity h, arbitrary controls, source preparation/reflection, source-kernel alpha_H/g, actual jump normalization alpha_L/sqrt(g), and coefficient/lookup costs remain. These may dominate. The frozen billions-of-stages ledger is not retrospectively revised by this separate theorem candidate.

## 8. Low-rate and ordinary-comparator boundary

Below either high condition, use the original finite-action Taylor/complete-isometry low branch. Its action includes sqrt(lambda)bT and lambda alpha_L²T. It is polynomial in the original acquired parameters under the explicit admission threshold, but is NOT automatically near-linear in Z. Using a_E<=2hb/g as a fallback recovers a polynomial global-action threshold if the supplied a_E bound is loose. No all-rate variance-only complexity claim is made.

The refined high theorem does not prove that a small source/system observable needs this machinery. In the frozen n4 benchmark, ordinary dense CQ evolution and a tiny effective generator already win. Better certified effective models, tensor/memory representations and model-specific exact channels must retain the same inputs, outputs and controls in any fair comparison. The refinement identifies how known energy injection and actual P/Q access can replace an unnecessarily global b²T driver in one acquired circuit; it does not establish a practical or civilisation-scale consequence.
