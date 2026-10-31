# Acquired pure-return source: complete first-event receiving construction

31 October 2026. Full mathematical-existence candidate, pending independent whole review. No implementation, novelty, practical advantage or general learning claim. Existing frozen compiler results are unchanged.

## 1. Exact acquired interface

Receive an actual finite-register channel Stinespring isometry W, including a unitary extension, controlled forward/inverse circuits, a prepared vector c in its Kraus-output register, and a prepared pure source state psi satisfying

    W psi = c tensor psi.

Let P=|psi><psi|, Q=I-P. Reflection about P and its controlled version are acquired. An integer m>=1 is certified to satisfy the OPERATOR inequality

    (Phi^dagger)^m(Q) <= Q/16.

This is not total-variation mixing in an unrelated norm. State preparation, the return certificate and all circuit acquisition costs are paid; no exponential-dimensional table is given or inferred.

The physical source-system generator is

    L(rho)=-i[H0+sqrt(lambda)K,rho]+lambda[(id tensor Phi)(rho)-rho].

The source is initialized once in psi, possibly with an arbitrary system/reference input. H0 acts on the accessible system only. K is Hermitian, PKP=0, and has an acquired controlled normalization-b block encoding, b>0. H0 has an acquired normalization-alpha0 Hamiltonian encoding or a comparably priced controlled evolution algorithm. Actual controlled/inverse costs are paid. A norm bound alone is not access. Degenerate branches are explicit: T=0 applies only the prescribed zero-time instruments in their specified order; lambda=0 is ordinary H0 evolution with the source unchanged. Exactly b=0 with a ground source is ordinary H0 evolution, since Phi fixes psi. None of these branches invokes the positive bridge formulas.

There are p prescribed system-instrument slots, with arbitrary retained references, classical outcomes and subsequent adaptation on those outcomes. Their times are fixed; neither source nor private event records are exposed. Instrument implementation costs are external or added separately, not bounded by p. The source is never reset at a slot or after a jump.

The desired accuracy is epsilon in the induced controlled-process channel, uniformly over allowed instruments and system/reference inputs. The whole simulator is unconditional CPTP, including its cap/failure branches. No normalized rare postselection guarantee is asserted.

Root premise source: `PURE_RETURN_COMPILER_OPENING.md`, SHA256 `f8f9171554f327c9b324e8a6fd2c4fe93ba5009ff8c5e5248bedd07e0f747f36`; scoped source/return review `PURE_RETURN_AND_SIGNED_SHUFFLE_LOCAL_REVIEW.md`, SHA256 `52c5323ad246e2ae2538ce25c3f8a0a4e91e9964e428557fccb4a80293b9e9cd`. These local receipts do not substitute for whole review of this receiving body.

## 2. Exact dark completion, return kernel and activity

Define A=(<c| tensor I)W. Contractivity and A psi=psi imply A^dagger psi=psi, so P reduces A. Projecting the m-step dilation onto c^tensor m yields A^m. Its Q-output norm is bounded by total Q survival; hence ||A^m Q||<=1/4.

Writing W through Kraus operators K_j, the dark stack is

    Lstack=W-|c> tensor I,   L_j=K_j-c_j I,
    Henv=i(A-A^dagger)/2,
    C=Lstack^dagger Lstack=2I-A-A^dagger<=4Q.

Then -i[Henv,.]+sum D[L_j]=Phi-I and -iHenv-C/2=A-I. Lstack/2 is an acquired contraction via a two-term coherent sum. It keeps the ACTUAL source and Kraus-output registers; no enumeration of j is required. Lstack P=0, but its output need not lie in P.

The proof potential V=sum_(j=0)^(m-1)(Phi^dagger)^j Q satisfies Q<=V<=mQ and (Phi^dagger-I)V<=-Q/2. For kappa=e^theta-1<=1/(32m), use Z=I+32 kappa V. On the high-rate branch sqrt(lambda)>=64bm, the tilted dark-jump generator obeys

    G_theta^dagger Z <= 256 kappa b^2 m^2 Z.

For completeness: fast drift is at most -16 kappa lambda Q; tilted recycling is at most 8 kappa lambda Q since C<=4Q and Z<=2I. The Q-Q coupling commutator is at most 64 kappa sqrt(lambda)bm Q<=4 kappa lambda Q. The P-Q cross form is bounded by

    64 kappa sqrt(lambda) bm ||Pv|| ||Qv||
      <= 4 kappa lambda ||Qv||^2
         +256 kappa b^2m^2 ||Pv||^2.

H0 and allowed system instruments preserve the source weight. Initially its expectation is one. Thus the EXACT physical dark-jump count obeys

    E exp(theta N_T) <= exp[256 b^2m^2 T (e^theta-1)].

No activity bound is assumed for the approximate algorithm. Approximate initial preparation is handled separately by channel contractivity.

Receive the independently reviewed kernel source `power_contraction_kernel_20261031/GROUPED_POISSON_KERNEL_CONSTRUCTION.md`, 14,750 bytes, SHA256 `150152b77d81cb47781d97d600f55d0b8d0d0a9c35a0891009cce58936792b4a`, and its review SHA256 `0605ac4ebb545e530cc8f8a12bdbd16301c1e84f3024cada3519d2940fc58e84`. It supplies, with actual finite arithmetic and query costs,

    F(s)=(1/2)e^(a s)e^(s(A-I))Q,
    a=(1-2^(-1/m))/2 >=1/(8m),
    ||F(s)||<=1, ||F'(s)||<=3.

Each call has normalization ONE, polynomial-m and logarithmic-error/time-bit overhead; the underlying W,c,P costs remain paid. A large s is not simulated by s iterations. Exact acquired-oracle/refinable unitary-synthesis conventions from that lemma remain binding.

## 3. Dimensionless branches and deterministic caps

Normalize time by T and put

    mu=lambda T, B=b^2 T, H=alpha0 T, c0=sqrt(mu B).

The high-rate branch is mu>=4096 Bm^2. Define

    r=a mu, delta=r-2c0,
    nu=sqrt(delta^2+8c0^2),
    s=(nu-delta)/2, d=(nu+delta)/2.

Then r>=8c0, delta>=6c0, s d=2c0^2, and s<=2c0^2/delta<=8B/(3a). Numerically evaluate s as 2c0^2/d, avoiding cancellation in nu-delta. Set

    tau_max=2^(-ceil(log_2(max(1,512mB)))),
    Wcap=ceil(1/tau_max)+p+1.

Partition the physical interval at all prescribed controls and additional fixed boundaries so each window is at most tau_max. Its remaining duration after events is tracked privately. This dyadic tau_max is at most min(1,a/(64B)) and within a constant factor of that bound, since 1/(8m)<=a<=1/(2m). We have s tau_max<=1/24. The ceiling here is acquired by exact comparisons to powers of two for finite rational B, not an exact transcendental oracle.

At theta=log(1+1/(32m)), the activity bound yields

    ell_error=ceil(log_2(1000/epsilon)),
    Mcap=ceil(64m[8Bm+ell_error])+1,
    Scap=Mcap+Wcap+2.

The exact probability of reaching Mcap jumps is <=epsilon/1000. There are at most Scap first-event calls before the jump cap and the fixed window boundaries. These are actual jumps, not virtual Dyson events.

Choose the integer power of two

    Aamp=256 * 2^(ceil(log_4 m)).

It lies in [256 sqrt(m),512 sqrt(m)) and will pad every complete first-event block. It is unrelated to the source contraction A.

## 4. Positive two-sector word, including every factor of two

The exact free Q dwell of normalized duration u is

    e^(mu u(A-I))Q = 2e^(-a mu u)F(mu u).

P dwells are identity on the source. H0 evolution commutes with these source-only factors and is included on each dwell. The P-Q interaction and Q-Q interaction blocks are actual projected K/b contractions. Every virtual interaction, in either direction or within Q, contributes the scalar phase -i; the whole word carries (-i)^Vvirtual.

Every Q dwell contributes scalar 2. Assign it to its incoming interaction, or the initial sector if initially Q. The exact scalar majorant is

    M=[[0,c0],[2c0,-r+2c0]],
    E(u)=exp(Mu) diag(1,2)
        =S exp(Msym u) S,
    S=diag(1,sqrt(2)),
    Msym=[[0,sqrt(2)c0],[sqrt(2)c0,-delta]].

This is bookkeeping on the TWO known sector labels, not a basis representation of the source Q subspace. The endpoint factors are at most 2, not an omitted 2^word. Expanding the positive series verifies that initial Q gives 2, each P-to-Q transition gives 2c0, each Q-to-P transition c0, and each Q-Q insertion 2c0.

The scalar symmetric off-diagonal path measure conditional on endpoints is a two-state Doob bridge with rates 0->1 equal to s and 1->0 equal to d. On every fast interval of length ell, add independent Poisson(2c0 ell) self-insertions at ordered uniform relative positions. Resumming their positive weights changes -r to -delta. Undoing that Poisson normalization recovers the original Dyson dwell -r. The endpoint prefactors S_i S_j do not affect the conditional bridge law.

At time u, write

    aa=(d/nu)e^(su)+(s/nu)e^(-du),
    bb=(sqrt(2)c0/nu)(e^(su)-e^(-du)),
    dd=(s/nu)e^(su)+(d/nu)e^(-du).

Then E_00=aa, E_01=E_10=sqrt(2)bb, E_11=2dd. All entries are <=2e^(su), and stable elementary evaluation needs no growing exp(+nu u) intermediate.

## 5. Actual no-event and jump circuits

Let K0(u) be the true no-jump propagator of the dark realization, including H0 and K. It is a contraction. For each pair of sector labels i,j, sample the conditional bridge and its Q-Q insertions, apply the actual chronologically ordered word, then unprepare the INNER source seed/work. All product blocks have fresh success ancillas. This obtains the operator mean, not a measured trajectory on the unknown input.

The word includes its input/output projectors Pi_i and Pi_j. These are acquired from the reflection about P. Uniform superposition over FOUR pairs, followed by a scalar acceptance block E_ji(u)/(2e^(s tau)) for a window tau, gives a block encoding of K0(u) with normalization

    alpha_no(tau)=8e^(s tau).

One can implement the scalar acceptance as a controlled rotation with good amplitude equal to that ratio. Failure flags are orthogonal and remain coherent. No source-state basis is enumerated.

For an actual event at u, the Kraus-output amplitude is

    Jstack K0(u),    Jstack=sqrt(mu)Lstack

in normalized time. Only the pre-jump Q row is needed. Use a uniform superposition over TWO initial-sector labels i and the pre-jump endpoint fixed at Q; then apply the actual contraction Lstack/2. Its output source and Kraus register are retained. Do not project its output back into Q or reset it to psi.

The bounds

    E_10(u)<=2(c0/delta)e^(su),
    E_11(u)<=2e^(-delta u)+4(c0/delta)^2 e^(su)

and c0/delta<=1/6 imply E_1i(u)<=2e^(s tau)[e^(-delta u)+c0/delta]. Since sqrt(mu)c0/delta<=4sqrt(B)/(3a), the following squared envelope dominates the TWO-arm scalar acceptance, including the physical factor 2sqrt(mu):

    alpha_jump(u)^2
       =1024 e^(2s tau)[mu e^(-2delta u)+B/a^2].

Explicitly each of the two inner acceptance amplitudes is 4sqrt(mu)E_1i(u)/alpha_jump(u), which is at most one by the displayed inequalities. Conditional source blocks have normalization one, including F. Thus the inner good block is the actual Jstack K0(u)/alpha_jump(u).

The complete squared mass obeys

    alpha_no^2 + integral_0^tau alpha_jump(u)^2 du
      <= e^(2s tau){64+1024[mu/(2delta)+B tau/a^2]}
      <4096/a <=32768m < Aamp^2.

Here mu/(2delta)<=2/(3a), Btau/a^2<=1/(64a), and e^(2s tau)<=e^(1/12). The normalization is polynomial in the return horizon and independent of lambda and source dimension.

## 6. Complete outer source and isometry, not a normalized no-jump map

Prepare a no-event arm of probability alpha_no^2/Aamp^2. Split the event envelope into two positive time components:

    h_1(u)=1024 e^(2s tau) mu e^(-2delta u),
    h_2(u)=1024 e^(2s tau) B/a^2.

For component j prepare probability integral h_j/Aamp^2, then a private uniform coordinate v mapped to the truncated-exponential or uniform quantile on [0,tau]. The remaining outer probability selects a zero good-block arm. Conditional on either event component use the SAME normalized inner block Jstack K0(u)/alpha_jump(u). Summing the two refined record components gives integral Jstack K0^dagger Jstack K0 exactly, since h_1+h_2=alpha_jump^2. Kraus/color registers come from Lstack itself and are not separately enumerated or classically sampled.

No-event plus all event times form the exact complete first-event isometry: K0(tau)^dagger K0(tau)+integral K0(u)^dagger Jstack^dagger Jstack K0(u)du=I on every source/system input. Thus the outer good block equals this isometry divided by Aamp. All source, projection, contraction, scalar-acceptance and product success ancillas stay coherent until amplification of this WHOLE isometry.

For integer Aamp, attenuate by c_A=Aamp sin(pi/(4Aamp+2))<1 and apply Aamp Grover iterations. The ideal good singular value becomes exactly one. The selfadjoint-dilation/Chebyshev proof bounds perturbation of the degree-d_A good-block polynomial by d_A^2 eta, d_A=2Aamp+1, when the original block error is eta. Leakage is O(d_A sqrt(eta)). This is a noncommutative polynomial telescoping bound, not a scalar derivative claim. Actual attenuation/phase synthesis is separately budgeted. Calls are O(Aamp), not a constant hidden in m.

## 7. Concrete uniform error allocations and private-time floor

Take

    e_step=epsilon/(1000 Scap), d_A=2Aamp+1,
    beta=(e_step/(10^6 d_A^2))^4,
    sigma=(beta/(100 Aamp))^4.

All displayed ceilings involving elementary reals are implemented using a certified upper interval of width at most one and then an integer ceiling; this adds at most two cap slots and never requires deciding equality to an irrational threshold. Positive probability lower bounds are replaced by certified positive dyadic lower bounds within a factor two, while rate/derivative upper bounds are rounded upward. Use these actual rounded bounds consistently in later allocations. Relative constant-precision acquisition uses the displayed stable formulas, finite input lengths and priced lower duration bounds. These fixed-factor changes do not alter any resource claim. The finitely many error categories below each receive at most beta/100, with subdivisions among their capped operations as stated. A larger fixed universal numerical safety factor may replace 100 when changing equivalent norm conventions; no input-dependent constant is suppressed.

A bound for the normalized physical generator, also up to an absolute factor for its count-augmented frozen version, is

    Lphys=1+2H+2c0+12mu.

The source Hamiltonian has norm<=mu and dark jump square<=4mu I; this bounds the count-augmented generator without source or count dimension. Put x_min=min(1,e_step/(100Lphys)). A remaining window shorter than x_min is advanced to its fixed boundary by identity, with the charged channel error. Every other call has tau>=x_min.

Remove the uniform-coordinate endpoints of width sigma for each event component. Give outer arm/component probability approximations total absolute error much less than beta^2; their square-root amplitude error is charged, without dividing by a tiny arm probability. Removed-coordinate mass O(sigma) causes O(sqrt(sigma)) Stinespring error. A finite uniform midpoint grid contributes an additional endpoint-bin mass of the same order.

For a retained truncated-exponential or uniform coordinate, both u and tau-u are bounded below by

    t0=(sigma/4) min(x_min,1/(1+2delta)).

The inverse exponential has derivative at most tau/sigma on this retained interval. Its formula uses stable log1p/expm1 evaluation of -log[1-v(1-exp(-2delta tau))]/(2delta), with the uniform limit handled separately.

The exact normalized event operator N(u)=Jstack K0(u)/alpha_jump(u) has norm<=1 and derivative at most the conservative bound

    Lout=1+delta+a sqrt(mu/B)(H+c0+2mu).

Indeed ||Jstack||<=2sqrt(mu), ||K0'||<=H+c0+2mu, alpha_jump>=32sqrt(B)/a, and |alpha_jump'/alpha_jump|<=delta. Choose outer representative-time error

    du <= min(t0/10, beta/[100(1+Lout)], e_step/[100Lphys]).

Uniform-bit precision and certified inverse arithmetic achieve this with logarithmically many precision bits. Only logarithms of inverse B enter numerical precision; b>0 is an explicitly represented normalization, not an unpriced continuously specified real. Time components have no inverse Kraus-probability factor.

## 8. Exact conditional bridge and a global virtual cap

Put g=2c0. For the two-state Doob chain, the number of potential upward points is dominated by an independent Poisson(s tau) clock. Each fast visit lasts no longer than an independent Exp(d) mark. Its self-insertion count Z has E 2^Z=d/(d-g)<=2, because g/d<=1/3. The number of off-diagonal transitions is at most twice the number of potential upward points plus one. Assign independent full-visit marks even to unused potential points. This gives, uniformly in the initial sector,

    E 2^(Vvirtual) <=4 exp(7s tau).

Endpoint conditioning divides this bound once by the actual endpoint probability. For all durations >=t0 the latter is bounded below by

    p0=s t0/(1+nu t0)>0.

Indeed P_01(t)=(s/nu)(1-exp(-nu t))>=s t/(1+nu t); P_10 and both diagonal minima are no smaller. Set eta=beta/10^4 and

    Kcap=ceil(log[4 exp(7s tau_max)/(eta p0)]/log 2).

Overflow of the TOTAL virtual count, including self-insertions, has conditional probability <=eta. Every loop and work register is capped/padded accordingly; overflow selects zero contraction. Kcap depends on log(1/p0), not its inverse as a number of iterations.

For the off-diagonal bridge at state i, endpoint j and remaining duration t, first-event survival is exp(-q_i u)P_ij(t-u)/P_ij(t). Its density is q_i exp(-q_i u)P_(1-i),j(t-u)/P_ij(t). The no-event atom is present only for i=j. The SAME raw uniform first selects whether it lies in the atom and otherwise inverts the FULL, unconditioned event CDF. Do not divide by a possibly tiny event mass.

## 9. Ties, duration stability and finite source compilation

Let qrate=nu+g, which bounds total off-diagonal-plus-self intensity before endpoint conditioning. Choose

    zeta <= min(t0/20, eta p0/[100(1+qrate+qrate^2)]).

A dominating Poisson clock bounds endpoint-near events and pairs within zeta by O((qrate+qrate^2 tau_max)zeta). This includes QQ insertions. Divide once by the ORIGINAL endpoint probability p0. Together with the count cap, the conditional removed mass is O(eta). On the remaining paths recursive durations are >=zeta/2 after small rounding. Define

    pz=s(zeta/2)/(1+nu zeta/2),
    Lker=16(1+qrate)^2/pz^2.

Direct differentiation of the first-event density, its no-event atom and its moving endpoint bounds total-variation change of the first-event kernel by Lker |Delta t|. All matrix entries have derivatives bounded by nu, their denominator is >=pz, and tau_max<=1. This is a polynomial bound used through its logarithm, not a number of operations proportional to 1/pz.

Compile source uniforms as finite coherent WORD registers. Capped reversible arithmetic maps endpoint labels, duration and seed to a path/work transcript. SELECT preserves them; UNPREPARE gives the operator mean. First-event inverse CDFs use fixed-depth bisection. With J_bisect levels, at most 2^(J_bisect+1) possible comparison thresholds occur. Excluding uniform strips of width at most eta/[100(Kcap+1)2^(J_bisect+3)] around them charges the ambiguous comparisons. The necessary precision is O(J_bisect+log(Kcap/eta)); the circuit performs J_bisect comparisons, not 2^J_bisect. Evaluate all exponentials with nonpositive arguments or stably combined expressions.

For every fast interval ell, sample its Poisson(g ell) count by a finite CDF scan through the remaining Kcap slots, sending all remaining mass to overflow. Compute exp(-z+n log z-log(n!)), n<=Kcap, z=g ell, with the z=0 branch explicit. Values below the allocated absolute-error threshold are clipped to zero; a large mean is not sampled by z iterations. Integer factorial/log arithmetic and negative-exponential range reduction have polynomial bit cost in Kcap, input lengths and precision. Each interval's CDF/threshold error is at most eta/[100(Kcap+1)], subdivided among its Kcap+1 entries. Overflow is already in the GLOBAL virtual-tail event.

For an accepted count, draw finite uniform relative positions and sort reversibly. Pad all slots to Kcap. Global tie removal guarantees the noncommuting word order is stable. If an interval changes length by h, its Poisson law changes in TV by at most g|h|. When counts couple, reuse identical relative uniforms, so event times change additively with endpoint/interval errors.

Choose inner time accuracy h satisfying

    h <= min(zeta/[100(Kcap+1)],
             eta/[100(1+Lker+g)(Kcap+1)^2],
             beta/[100(1+H+3mu)(Kcap+1)^2]).

Across capped recursive calls, duration mismatches grow by at most O(Kcap h); summed kernel/count discrepancies are O((Lker+g)Kcap^2 h). There is NO exponentially iterated inverse-quantile Lipschitz product. The timing error of the operator word is O((H+3mu)(Kcap+1)^2 h): H prices system intervals and 3mu is the derivative bound of F(mu ell). Omitting this fast-kernel term would be incorrect.

Each F invocation, projected K/b encoding, actual jump stack, H0 interval, projector and scalar acceptance receives synthesis error at most beta divided by 10^4 times the total capped number of such operations. Source basis/c preparation and elementary phases have the same subdivision. Calls to F use the reviewed finite-time kernel algorithm at that precision; its discontinuous implementation cutoff is harmless because its approximation to the exact differentiable F is uniform. Actual unknown source inputs are not read or reinitialized.

Controlled H0 evolution for a B_time-bit duration in [0,tau] uses B_time controlled fixed-time evolutions at tau/2^j. Charge every one of the Kcap+1 padded interval slots separately with the real Hamiltonian encoding costs and precision. No time oracle or table of all binary durations is assumed. Every virtual insertion includes the exact (-i) phase; residual synthesis is charged.

## 10. Whole finite-bit error conjunction

Uniformly over both sectors, retained times and arbitrary physical inputs, the capped INNER mean-block error is below beta/10 after the subdivisions above. Bad path probabilities enter linearly for operator means; no source-state-norm conclusion is inferred from that fact. If a coherent source-state norm bound is used instead, its square-root bad-mass conversion must be paid.

For the OUTER first-event map, compare exact and finite constructions in the SAME uniform-coordinate Hilbert space. The finite midpoint register can be embedded by attaching a private uniform remainder within its bin. This gives an L2 Kraus-amplitude comparison. Removed coordinates cost their square-root mass; finite amplitude error, inner-block error and Lout du are added. After allocation the base block error is <=beta.

Continuous and discrete public timestamps are not close in total variation. None is exposed here. The outer type/component/uniform/Kraus registers remain private; only their induced physical continuation matters.

Complete-isometry amplification gives good-block error <=d_A^2 beta and leakage O(d_A sqrt(beta)), below e_step after the displayed conservative budgets. Attenuation and all O(Aamp) phase/primitive calls receive an additional total e_step/100 synthesis budget. On failure, keep/trace the flagged output by a fixed CPTP rule. No branch is normalized after postselection.

After the amplified first-event instrument, privately store/read its event time and retain the actual source/Kraus output. A no-event arm advances to the fixed window boundary; a jump arm updates the remaining duration and continues. Do not reset to psi even if a classical source motivation originally suggested resetting.

## 11. Count-augmented future comparison and controls

For the proof, augment the EXACT dark process by a classical jump counter and freeze it after Mcap. Its generator norm is bounded by a fixed multiple of Lphys independent of counter/source dimensions. Therefore its future channel is diamond-Lipschitz in remaining duration, with that bound. Composing later prescribed system instruments is contractive, including their retained records and arbitrary references.

A backward hybrid over at most Scap calls compares the approximate call with the exact future at its own representative remaining duration. It charges per-call Stinespring error, Lphys du, and short-window identity error Lphys x_min. This is the required private-time continuation argument; it does not presume trace-distance closeness of continuous and finite timestamp records.

The exact MGF bounds the probability of hitting the count cap uniformly in system/reference input and allowed instruments. The discarded tail is a CP subchannel whose effect is bounded by that probability, so replacing it by a fixed continuation costs at most twice the bound in diamond norm. No separate approximate-process MGF or exceptional-path mean is needed. Approximate initial psi preparation is given epsilon/1000 and charged by contractivity.

All errors sum to less than epsilon with the stated safety budgets. Fixed caps, overflow flags and unconditional failure handling define a finite CPTP circuit on every input, not just typical inputs.

## 12. Explicit ordinary low-rate branch

For mu<4096Bm^2, no dark fast-kernel method is needed. The original source generator lambda(Phi-I) has the EXACT state-independent Poisson-channel unraveling: at rate lambda apply Phi by the acquired W; between events evolve under H0+sqrt(lambda)K. Keep the source and all private Stinespring outputs. This identity follows directly by the ordinary chronological Dyson expansion in channel insertions and is valid for noncommuting K.

Cap a Poisson(mu) count at O(mu+log(1/epsilon)), compute its capped CDF by a finite scan, and conditionally sample/sort uniform event times. The mean mu is polynomial in B,m on this branch, so this scan and number of W calls are genuinely polynomial. Merge the prescribed instrument times. Rounding an event across a prescribed control is excluded at cost O(mu p h_clock); other interval timing errors telescope under the Hamiltonian norm bound. Choose h_clock so both this probability and O((H+sqrt(mu B))M_low h_clock) are below the assigned error. Only logarithmic precision bits are needed. Overflow is given an arbitrary CPTP continuation and costs its Poisson tail.

The acquired Hamiltonian encoding has action at most H+sqrt(mu B)<=H+64Bm. Ordinary high-precision Hamiltonian simulation and coherent binary-duration control are paid on each interval. There is no reliance on an unexplained general Lindblad stack oracle, no enumeration of source Kraus labels, and no claim that physical small rate is free.

## 13. Resource statement and centering exclusions

For the high branch,

    Scap=O(Bm^2+m log(1/epsilon)+Bm+p+1),
    Aamp=O(sqrt(m)).

All virtual caps and precision-bit counts are polynomial in m, input lengths, log(2+mu), log(1/epsilon), log(2+B+H+p) and the corresponding encoded positive-parameter logarithms. There is no inverse p0 loop or source-dimension sum. Each of O(Scap Aamp) base calls has polynomial source arithmetic, Kcap projected coupling operations, Kcap+1 finite-kernel/H0 interval calls, and uncomputation. Each finite kernel has polynomial-m and logarithmic-precision query cost in W, c and P. The low branch has the polynomial bounds just given.

Thus total overhead is polynomial in m, 1+B+H+p, input/register bit lengths, log(2+lambda T), log(1/epsilon), multiplied by the ACTUAL supplied controlled operator/state-preparation costs. Large source dimension is allowed only through succinct acquired operations. This is not a free oracle from a matrix norm, not a practical gate count, and not an optimal asymptotic exponent claim.

If PKP is not zero, subtracting its mean requires acquired mean-Hamiltonian access and paying its sqrt(lambda) physical action. It cannot be hidden in an unpriced H0 or estimated to arbitrary precision for free. An OPTIONAL different model may add a fair sign qubit: use Phi tensor reset_|+>, psi tensor |+>, and K tensor Z. The same m-step return certificate holds because the sign is reset after one channel application and the source survival bound is unchanged. The new coupling is exactly centered with the same b. Its preparation, reset dilation and one-bit operator are paid. This creates signed noise; it is NOT a faithful centering transformation of an arbitrary original process.

## 14. Scope of the resulting candidate

The construction receives an acquired pure-return channel and a quantitative survival horizon, not an arbitrary classical Markov generator or a learned source. It simulates the retained PRIVATE source process at prescribed controls. A separate invariant-observable-algebra proof is required to identify a desired classical-source process. Physical bath measurements, source-path disclosure, heat/count statistics of a different unraveling, arbitrary-time interventions, postselected normalization, nonvacuum initial-source activity bounds and acquisition of W/c/psi/the certificate remain outside scope.

The grouped-Poisson kernel already has an ordinary contour-functional-calculus competitor. The value here is its concrete complete first-event receiving interface, with actual jump output and physical clock, rather than a claim of novel nonnormal fast forwarding. Whole acceptance requires independent reading of THIS conjunction and its exact source premises.
