# Independent receiving audit: adaptive cap and vanishing local-strength accuracy

2026-10-29 UTC. Auditor: `challenge_thermal_counting_consequence`.

## Verdict, including the failed stronger interpretation

**Mathematical/resource verdict: PASS.** The new adaptive-cap construction, relative gate rounding, local-strength product estimate, and sparse counting interface yield the stated randomized, logarithmically vanishing energy-density and variational-state-access consequence, conditional on the imported exact sparse-#3SAT theorem.

**Conceptual-superiority verdict: NOT ESTABLISHED.** An equally informed conventional symmetric imaginary-time Trotter / signed tensor-network / GapP / parsimonious-3-CNF approach, supplied the SAME counting theorem, reproduces this resource bound. This is a valid explicit quantitative conditional synthesis, not a new simulation principle or a demonstrated advantage over that comparator. The attempted interpretation as a distinct flagship algorithmic breakthrough is unsupported. This negative finding is part of the receiving result, not an incidental disclaimer.

The external counting theorem is an imported premise and was not re-audited or executed here. Earlier frozen receipts remain unchanged; this receipt is separate and covers the new cap and vanishing-accuracy interface. No historical novelty certificate is supplied.

## 1. Exact input contract and branches

Use the explicit fixed-k rational-complex Hermitian local matrices, nonempty supports, rational envelopes alpha_e, and fixed local-strength bound g from `LOCAL_STRENGTH_SPARSIFICATION_DRAFT.md`. Zero terms are discarded and scalar shifts are extracted/restored. Its computable entrywise envelope loses only a factor depending on fixed k, so a bounded actual per-site interaction-norm sum suffices without a norm oracle.

Let L=sum alpha_e<=ng and tau in (0,1] be rational. If L<=tau*n/4, return the zero effective Hamiltonian. Its maximally mixed state has energy excess at most 2||H||<=tau*n/2. The zero-Hamiltonian free-energy density is -ln(2)/beta, not zero. This branch also handles g=L=0 before divisions. Below assume L>tau*n/4, hence g>tau/4.

## 2. Adaptive sampling cap: all constants checked

Set a=512 L^2/(tau^2 n), q=ceil(a), J_s=L/q, lambda=qg/L. Since a>32n>=32,

    q <= (33/32)a = 528 L^2/(tau^2 n),
    tau^2/(528g) <= J_s < tau/128.

For D=ceil(9lambda)+ceil(log2(200g/tau)), both logarithmic and square-root ceilings throughout the construction can be obtained by integer/rational comparisons. The argument of this logarithm exceeds 50. With x=tau/g<4,

    D J_s <= 9g + J_s[log2(200g/tau)+2] < 10g.

Indeed x log2(200/x)+2x<=32+1+8=41<128; the elementary bound x log2(1/x)<=1 is valid for all positive x. The nontrivial branch therefore gives the claimed strict bound. Coloring retained support intersections needs at most k(D-1)+1<=kD colors, even with repeated sampled occurrences. Thus c J_s<10kg.

The older concentration proof is unchanged. For Y=h_e/p_e, ||Y-H||<=2L and E(Y-H)^2<=L^2 I, valid for indefinite complex Hermitian terms. Two-sided matrix Bernstein at target tau*n/4 gives failure at most 2^(n+1)e^(-9.6n)<0.00028.

For X_v~Bin(q,p_v), mu_v<=lambda, the exact tail identity is

    E[X_v 1{X_v>D}] = q p_v Pr(Bin(q-1,p_v)>=D).

Consequently this expectation is at most mu_v(e lambda/D)^D<=mu_v e^(-D). Here D>=9lambda>e^2 lambda; the q-1 tail's mean is no larger than lambda. The number of deleted occurrences is at most the sum of bad-vertex incidences, so its norm upper bound has expectation at most ng e^(-D)<=tau*n/200. There is no missing k: the incidence-strength sum is already bounded by ng. Markov contributes failure at most 0.02. The adaptive cap therefore preserves the sampling-plus-trimming norm guarantee tau*n/2 with success >0.9797.

Exact rational index sampling can use common integer weights and prefix sums. Each uniform-integer rejection draw accepts with probability at least 1/2. A cap of ceil(log2(1000q)) attempts per draw adds at most 0.001 total failure, leaving success >0.9787 and therefore >0.97. A cap failure may be flagged or replaced by a fixed valid fallback state and counted as failure of near-optimality. Rational denominator clearing, prefix construction, support indices, coloring, and all arithmetic are polynomial in input length and q; no 2^n matrix is constructed. The bounded-time claim concerns this preprocessing. Exact measurement sampling later still has its separately stated expected-time guarantee.

## 3. Relative rounding: no hidden volume precision

Take theta=tau/(4g)<1, beta=4/tau, Kbar=20k^2g, and the LEAST positive integer r obeying the two stated lower bounds. Let delta=beta/r and eta=delta*theta*J_s/16. Choose the SMALLEST sufficient nonnegative dyadic depth B with 2^(-B)<=eta/(2*2^k).

The schedule gives delta Kbar<=1/2 and delta J_s<1. Hence every exact local exponential has minimum eigenvalue greater than 1/2. A rational Taylor approximation followed by rational Hermitian grid rounding achieves norm error eta; no decision about an exact transcendental rounding tie is required. Since eta<1/4, every rounded G_e is strictly positive. The resolvent integral for the operator logarithm on matrices bounded below by I/4 gives

    ||log G_e-log exp(-delta h_e/2)|| <= 4 eta,
    ||h'_e-h_e|| <= 8 eta/delta <= theta J_s.

Thus, with m'<=q retained occurrences,

    ||H'-Htilde|| <= m' theta J_s <= theta L <= n tau/4,
    ||h'_e|| <= 2J_s,       sum_e ||h'_e|| <= 2ng,
    K'=k sum_layers max_e ||h'_e|| <= 2kcJ_s <= Kbar.

The equality qJ_s=L is what removes a possible extra factor of q or n. Gate identities are shared mathematically between repetitions; errors are interpreted as a nearby Hamiltonian, not accumulated as independently perturbed full-volume matrix products.

Here is an explicit precision lower bound rather than only asymptotic notation. For fixed k,g, put

    C=2+8Kbar+(32/3)Kbar(g+1).

Using sqrt(g)<=g+1 and tau<=1, minimality of r implies r<=C tau^(-3/2). Therefore delta>=4 sqrt(tau)/C, and

    eta >= tau^(7/2)/(8448 C g^2).

Consequently B=O_{k,g}(log(2/tau)), with NO log n term. Numerator magnitudes use B+O(1) bits because delta J_s<1. Evaluating the fixed-size local exponentials to this precision takes polynomial input-bit work; h'_e is only a mathematical definition and is not computed by a matrix-log oracle.

## 4. Independent check of the received local-strength physics

I read the actual `PHYSICS_LOCAL_STRENGTH_THEOREM.md` and `PHYSICS_LOCAL_STRENGTH_AUDIT.md`, not merely their reported conclusions. The coefficient argument is valid: before commutator number p a branch has at most kp sites; the local-strength branch bound produces p!, and the symmetric scalar majorant over the ordered simplex contributes exactly 1/p!. Disjoint colored pulses give K=k sum J_j. For Hermitian h, Ad_U(h)^dagger=Ad_{U(-t)}(h), so only even coefficients enter the Hermitian part. The relative generator R'R^(-1), R=Q exp(tH/2), has two tails with an outer factor 1/2, hence no additional factor of two. Two-sided singular-value Gronwall and monotonicity of log give the claimed bound. No power-monotonicity assumption or uncontrolled BCH truncation is used.

For the rounded Hamiltonian, the effective generator A=-(r/beta)log P satisfies

    ||A-H'||/n <= 2(L'/n) K'^2 beta^2/[3r^2(1-(K'beta/r)^2)]
                 <= 16g Kbar^2 beta^2/(9r^2) <= tau/4.

The last inequality uses r^2 >= (64/9)Kbar^2 beta^2 g/tau. Together with the successful sampling error tau*n/2 and rounding error tau*n/4, this proves ||A-H||<=n tau. Importantly, the local-strength theorem does NOT itself replace sum of layer maxima by max of local sums; the adaptive cap above supplies the needed premise.

## 5. Witness, scalar and probability budgets

The exact positive rational product defines sigma=P^r/Tr(P^r), the Gibbs state of A at beta. The entropy bound for n qubits gives

    Tr(H sigma)-E0(H) <= 2||A-H||+n ln(2)/beta
                       <= (2+ln(2)/4)n tau < 9n tau/4.

At tau=epsilon/4 this is strictly below n epsilon, with slack. The effective free energy also determines E0(H)/n within (1+ln(2)/4)tau, before any separately budgeted numerical logarithm evaluation. Exact evaluated witness energy avoids that last logarithm altogether and supplies a scalar additive-density estimate from above.

Every produced sigma remains a valid full-rank density matrix even on an unsuccessful sparsification event; hence its exact energy is ALWAYS an upper bound on E0(H). Only near-optimality is randomized. Independent repetition followed by selection of the least evaluated energy amplifies success without knowing which sampling event succeeded.

Expand each original fixed-k term in its rational Pauli basis, using at most 4^k coefficients. For an original list of m terms, at most O_k(m) signed-count queries evaluate Tr(H sigma) exactly. This is polynomially many queries in the explicit input size, even when m is dense. The original high-precision coefficients enter external rational arithmetic, not extra precision bits at every thermal gate. Count outputs, their differences, and the final rational energy all have polynomial bit lengths. Specified distinct-site product-Pauli prefix masses likewise use the earlier signed-count encoding. Exact rational Bernoulli sampling requires expected polynomial random-bit overhead; no lower bound on prefix mass is needed. This is classical statistical access, not physical preparation or true-Gibbs total-variation approximation.

## 6. Boolean size and conditional runtime

Each palindrome contains O(q) fixed-k gates and there are r repetitions. Only local wire segments are introduced, not all n wires at each gate. Their support indices are encoded in formula structure and need not be nondeterministically guessed. The already checked bounded-fanin lookup/comparator/phase circuits cost O_k(B) per gate; exact-equivalence Tseitin clauses have one unique auxiliary extension. Thus

    N=O_k(n+qrB)=O_{k,g}(n tau^(-7/2)log(2/tau)),
    clauses=O_k(N),

with clause density independent of tau, r and B. Magnitude selectors count integer weights exactly, phase bookkeeping retains complex signs, and the final real contraction is a difference of two exact counts. Exponential cancellation therefore changes neither required gate precision nor Boolean variable count.

For epsilon_n=1/ceil((ceil log2(n+2))^(1/8)) and tau=epsilon_n/4,

    N=O(n(log n)^(7/16)log log n),
    time=poly(input length,n) 2^{O(n log log n/(log n)^(1/16))}.

Space is polynomial. More generally a<1/7 is sufficient for logarithmic exponent a; the endpoint is not implied. This is subexponential in physical n **up to polynomial input-length overhead** (and truly 2^{o(n)} for polynomial or subexponential input length), not a claim that arbitrary-length coefficients cost only a single reading pass. Sampling/trim preprocessing makes this randomized. Exact rational product-measurement sampling additionally has expected, not worst-case bounded, running time.

## 7. Same-premise comparator and primary source checks

I read `INFORMED_TROTTER_GAPP_COMPARATOR.md` and checked the principal cited locations directly. Its conspicuous no-separation verdict is correct.

- [Childs et al., A Theory of Trotter Error](https://arxiv.org/pdf/1912.08854), Theorem 8, gives exact error representations. Theorem 11/Eq. (54) retains an extensive imaginary-time exponential, so its displayed black-box bound alone does not establish a constant-volume step size. It would be wrong to cite that formula while silently deleting the exponential. The standard exact framework can instead be specialized using local-strength bounds.
- [Kuwahara, Mori and Saito](https://arxiv.org/pdf/1508.05797), Appendix B, Lemma 3/Eqs. (B2),(B6), already give the different-generator local-strength nested-commutator estimate used here. [Arad, Kuwahara and Landau](https://arxiv.org/pdf/1406.3898), Lemma 3.1, is direct short-imaginary-time locality precedent. Our explicit even-part/relative-generator/log estimate is a transparent composition of established machinery, not a newly established locality principle.
- [Fortnow and Rogers](https://arxiv.org/pdf/cs/9811023), Theorem 2.2 and Lemma 3.2's proof, give GapP closure and denominator-cleared signed path sums. [Schuch et al.](https://arxiv.org/pdf/quant-ph/0611050), Section IV, treats normalization, expectation values and general complex tensor contraction via counting. These are genuine primary precedents, not claims that their published polynomial reductions automatically have our precise linear variable bound.

The equally informed comparator uses the same sparse approximant, symmetric thermal product, nearby-Hamiltonian rounding, local signed path sums, binary comparator and unique-extension CNF compilation. It therefore has the same q,r,B,N, the same imported counting runtime, and the same variational witness and specified-measurement access. Those last outputs are not a separation either.

**Interpretation:** once standard short-time local-norm machinery and resource-aware compilation are supplied, the counting-enabled consequence is a direct quantitative corollary. The checked composition is useful because naive generic polynomial reductions or extensive-norm precision bounds do not suffice. No independently new simulation mechanism has been identified. No claim is made that an earlier paper printed the full combined statement verbatim, nor that the adaptive cap's exact constants previously appeared.

## 8. Actual executions and boundaries

1. Copied `check_local_strength.py` into `independent_replay/adaptive_cap/`, executed it, and compared its summary JSON and both CSV files byte-for-byte with the producer outputs: identical. This covers 128 coefficient/parity checks and 48 step bounds, up to 64 colors, with equal and nonuniform complex-Hermitian weights. It is double-precision finite-matrix evidence, not the analytic proof.
2. Independently wrote and executed `independent_replay/adaptive_cap/check_adaptive_arithmetic.py`: **945 exact rational schedule cases PASS**, n up to 10^9, k in {1,2,7}, varied rational g,tau,L, including near the nontrivial-branch boundary. It checks both J_s bounds, adaptive D J_s, exact minimal r and B, rounding/error budgets and bounded-randomness arithmetic. It does not sample exponentially rare tails or materialize enormous sampled term lists. The initial diagnostic implementation unnecessarily tried constructing 2^D for a huge D; it was stopped and replaced with the exactly equivalent integer logarithm-ceiling comparison before the successful replay. This was a diagnostic resource mistake, not a failure of the mathematical cap.
3. Earlier frozen CNF and witness checks are reused through their receipts, not relabeled as a new full #SAT implementation. No imported solver, physical quantum hardware, or end-to-end large-n simulation was executed.

No unreceived extension is folded into this result. In particular, no inverse-polynomial total-energy guarantee, spectral-gap simulation, ground-space trace-distance statement, practical numerical superiority, or historical priority follows. The requested receiving loop is closed; further exponent or Hamiltonian-family extensions are not recommended as the next research goal.
