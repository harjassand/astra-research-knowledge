# Independent derivation: count-only growing-sphere selection by certified Loewner envelopes

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

## 1. Scope and canonical protocol

The unknown real symmetric matrix obeys0<=A<=I_m. A real unit input x yields an actual Bernoulli observation y with mean p(x)=x^T A x. Calls independently reset. The task is to find a near-minimum direction from these bits and known controls, not from exact probabilities, matrix entries or supplied eigenspaces.

The canonical finite protocol here is the **rational-C** version. At each stage its C is an explicitly computed rational matrix polynomial in the learned rational envelope B. It queries normalized Cz and uses the rational weight ||Cz||^2. It does NOT use B^(-1/2) input states with C-derived weights, nor mix the two moment identities. Exact square roots are only a motivation or a separately valid alternative after its own finite congruence-error allocation.

Let0<gamma,epsilon<=1, c=gamma/16, tau_j=2^(-j), J=ceil log2(8/epsilon), and a=1/(1−2c). Initially B_0=2I. The intended simultaneous invariant is

    A+tau_j I<=B_j<=aA+2tau_j I.                         (1)

All actual histories additionally enforce tau_j I<=B_j<=4I, or terminate with a prescribed unit-vector output. Every executed query on a terminated history is charged. An abort is not postselection.

## 2. An efficiently sampled exact real projective2-design

Sample z by the following mixture:

- with probability2/(m+2), choose a uniform standard basis vector e_i;
- with probabilitym/(m+2), choose independent uniform signs s_i and put z=s/sqrt(m).

The design has a large formal support, but the learner never enumerates it: sampling needs O(m) sign bits plus bounded integer sampling for the mixture and basis index. The matrix P=zz^T is rational in either branch. Its second and fourth moments are

    E P=I/m,
    E[z_i z_j z_k z_l]
      =(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)/(m(m+2)).

Indeed the mixed fourth moment for distinct coordinates is1/[m(m+2)], while the diagonal fourth moment is3/[m(m+2)]. Odd sign moments vanish; the basis branch has no unwanted mixed terms.

Define

    T(z)=m(m+2)P/2−mI/2.

For any real symmetric F,

    E[(z^T Fz)T(z)]=F.                                  (2)

T has one eigenvalue m(m+1)/2 and m−1 eigenvalues−m/2. Thus its Frobenius norm squared is constant,

    L_m=||T||F^2=m^3(m+3)/4<=m^4.                       (3)

The formal exponential design support is therefore not an exponential search grid.

## 3. A rational, uniformly conditioned local whitening matrix

On every nonterminated history B is rational and tau I<=B<=4I. Put Q=I−B/4, with spectrum in[0,1−tau/4]. The binomial series gives

    B^(-1/2)=(1/2)sum_(k>=0) a_k Q^k,
    a_k=binom(2k,k)/4^k, 0<a_k<=1.

Take an integer N with

    N+1>=(4/tau)ceil log2(32/tau)

and let C be the finite rational sum. Since the tau_j are dyadic, the minimal stated choice can be computed exactly as N_j=4*2^j*(5+j)−1. The omitted tail obeys

    0<=B^(-1/2)−C
      <=(2/tau)(1−tau/4)^(N+1) I
      <=(2/tau)exp[−tau(N+1)/4]I<=I/16.

C commutes with B and C>=I/2. Since sqrt(B)<=2I,

    (7/8)I<=C sqrt(B)<=I,
    (49/64)I<=CBC<=I,
    C^(-2)<= (64/49)B<2B,
    C^2<=B^(-1)<=I/tau.                                 (4)

These are bounds on a learned, known matrix with an algorithmically enforced floor. They are not a minimum-eigenvalue assumption on A or on a source state.

The exact rational polynomial costs polynomial work in m,1/tau and the current matrix bit length. Its degree O(tau^(-1)log(1/tau)) must be paid; it is not a source call or a free unknown inverse. Exact rational inversion of C is well conditioned because C>=I/2.

## 4. Exact actual-input moment and variance

For a sampled z set

    s_z=z^T C^2 z,  x=Cz/sqrt(s_z),
    Y=y s_z T(z),  F=CAC.

The ideal-reference input x is a known normalized rational-direction state; the finite physical preparation is charged separately below. Both s_z and Y are rational even in the sign-vector branch. The observation mean is

    E[y|z]=x^T A x=(z^T Fz)/s_z.

Consequently E Y=F exactly by(2). No source expectation is supplied to the algorithm.

On a good prior history A<=B. Then0<=F<=CBC<=I and s_z<=1/tau, so

    E||Y||F^2
      =L_m E[s_z(z^T Fz)]<=L_m/tau.                     (5)

The variance scales as1/tau, not the looser1/tau^2 obtained by squaring the maximum weight. This is where the uniform PSD envelope is essential. On a statistically bad history the moment identity remains true, but this improved variance need not; conditional first-failure analysis uses it only while(1) holds. All-history processing still has fixed finite size because s_z<=1/tau and Y is bounded.

## 5. Elementary Frobenius median estimator

Within stage j freeze B_j and all measurement rules. For each of b independent batches collect

    n_j=ceil[2304 L_m/(tau_j c^2)]

independent y,z observations and form the arithmetic mean M_l. From(5),

    E||M_l−F||F^2<=L_m/(n_j tau_j).

Chebyshev gives failure probability at most1/16 for radius r=c/12. Choose b to be the smallest odd integer at least ceil log2(2J/beta). Select the FIRST batch mean having at least(b+1)/2 means, including itself, within distance2r; if none exists, abort safely. Squared Frobenius distances and the rational threshold4r^2 suffice for every comparison.

If a strict majority lies within r of F, any good center has a qualifying2r-neighborhood. The first qualifying neighborhood intersects the good set, giving selected error at most3r=c/4. Independence of batches and a union bound over subsets imply probability at most2^(-b) that half or more batches fail. Thus each stage has conditional failure at most beta/J while earlier stages are good. No independence across adaptive stages is asserted.

The resulting symmetric rational Fhat satisfies

    ||Fhat−F||op<=||Fhat−F||F<=c/4                     (6)

on simultaneous success. It is not required to be PSD.

## 6. Rational update, exact guard, and the invariant

Set Ahat=C^(-1)Fhat C^(-1). From(4),(6),

    −(c/2)B<=Ahat−A<=(c/2)B.

Form Btemp=Ahat+cB+(tau/2)I, and symmetrically round its entries to the largest dyadic grid step h<=c tau/(2m), equivalently h=2^(-ceil log2[2m/(c tau)]). Entry error at most h/2 implies Frobenius, hence operator, error at most c tau/4. Thus the actual rounded Bnext differs from A+cB+(tau/2)I by at most3cB/4 in Loewner order, and

    A+(c/4)B+(tau/2)I<=Bnext
                         <=A+(7c/4)B+(tau/2)I.         (7)

The upper bound is at most A+2cB+(tau/2)I. Given(1), this is

    (1+2ca)A+(4c+1/2)tau I<=aA+tau I,

because a=1+2ca and c<=1/16. The lower bound is at least A+(tau/2)I. This proves(1) inductively.

Every good update lies strictly inside the guard tau_next I<=Bnext<=4I: the lower margin is at least c tau/4 and the good upper bound is at most a+1<=15/7 after the first update. The initial B=2I is also valid. Exact rational PSD tests can accept or terminate safely on every history. They can be implemented by pivoted Schur-complement/LDL recursion, with the all-zero-diagonal case checking that the whole matrix is zero. Enumerating all principal minors is unnecessary. No numerical eigenvalue-sign oracle or source gap is used.

Rounding the whole update resets its description length. An accepted B has entries bounded by4 and is a multiple of h, giving bit length polynomial in log m, log(1/c), log(1/tau) and the rational input precision. Intermediate polynomial-C, inversion, medoid and update calculations have deterministic polynomial bit caps. Bad histories do not trigger an unbounded fallback solver.

## 7. Final selection and complete query cap

Use a certified finite known-matrix routine to output a real unit vector x with

    x^T B_J x<=lambda_min(B_J)+tau_J/2.

A backward-error eigensolver suffices; a spectral gap is not needed. From(1),

    p(x)<=a lambda_min(A)+(3/2)tau_J
         <=(1+gamma/7)lambda_min(A)+3epsilon/16.         (8)

The exact-reference event has probability at least1−beta. If the whole finite sampler/control implementation differs by at most nu in the agreed operational metric, bounded risk gives average excess at most the right side plus beta+nu, using the conservative loss-transfer convention. For example beta,nu<=epsilon/8 leave ample room for a stated(1+gamma)lambda_min+epsilon objective. Applications converting Bernoulli risk to a different task loss must additionally pay that known conversion factor.

Since sum_(j=0)^(J−1)tau_j^(-1)=2^J−1<16/epsilon and c=gamma/16, the total probe count is bounded by

    T<=b[J+9437184 L_m/(gamma^2 epsilon)].               (9)

All probes are real Bernoulli calls. Safe early termination can use fewer, but never refunds an executed observation. This is O_tilde(m^4/(gamma^2 epsilon)), not a claimed minimax-optimal m dependence.

## 8. Native finite controls and information boundary

The exact rational mixture/index sampler can be coupled to fixed-retry binary rejection with failure probability allocated across the predetermined cap. A failed seed draw gets a prescribed fallback design point and is charged to the whole-process discrepancy; no source call occurs on a fictitious rejected input. Signs use exactly m independent bits. The formal reference sampler is exact, while the implemented one has an explicit finite bit horizon.

For a basis design point the known query direction is C e_i; for a sign point it is C s, since the1/sqrt(m) cancels on normalization. Normalization is stable because ||Cz||>=1/2. Known-state preparation and gate synthesis are approximate, with per-operation tolerance allocated over a worst-case cap for every history. There is no free arbitrary-vector state preparation or unknown source inverse. If the input family is realized by an m-dimensional selector, its ceil(log2 m) qubits and dense O(poly(m)) preparation work must be paid, alongside the logical probe and frozen decoder/readout. The coefficients used in the update remain exact rational functions of the actual observed bits and prescribed controls.

This global guarantee is not a one-point learned-whitening fixed-point claim. The initial envelope is valid for every direction; every successful update retains a uniform Loewner certificate relative to the unknown A. It therefore cannot silently exclude an unvisited low-risk direction while satisfying the proof event. Conversely, if the risk is not a quadratic PSD form on the full real sphere, the mechanism has not established a global discovery theorem.

## 9. Growing-anchor quantum composition and a sharp boundary

For any positive matrix-valued real quadratic G(x) and uniform standard-anchor average Gbar=(1/m)sum_a G(e_a), scalarizing by any gauge vector v gives a PSD real quadratic matrix M_v. Hence

    v^dagger G(x)v=x^T M_v x<=Tr M_v=m v^dagger Gbar v,

so G(x)<=m Gbar. The earlier four-anchor decoder-regret multiplier4 must therefore become m. The decoder must be acquired at proportionally finer virtual Bell accuracy; merely replacing the encoder stage while preserving the old decoder budget is invalid.

The factor is sharp. Take G(x)=|x><x| on an m-dimensional gauge, with Gbar=I_m/m. For an identity-Pauli source E_x(omega)=U[omega tensor G(x)]U^dagger, consider the proof decoder that undoes U and applies logical Z conditional on gauge projector |e1><e1|. Its Bell loss is|x1|^2, unrestricted optimum is zero, and anchor-average virtual loss is1/m. Thus sup_x regret=m ell0=1 exactly. The inverse here only defines a counterexample comparator; it is not supplied to the algorithm. These gauges are generally noncommuting.

The same count-learning construction is available to an equally informed conventional learner. No quantum speedup, supplied matrix oracle, independent-sign-bank assumption, or environment reconstruction is claimed.

## 10. Deterministic evidence

`growing_sphere_loewner_selection_independent_check_20261028.py` verifies the exact real-design second/fourth moments for m=1,...,5, the rational-C conditioning certificate, unbiased F=CAC and its second-moment bound on noncommuting A/B fixtures. It also checks54 prescribed rounded Loewner updates,51 noncommuting with A, rational median geometry, six dyadic cap cases and sharp m-anchor examples.

These prescribed error histories are NOT an acquired learner experiment. No Bernoulli outcomes were sampled; the script evaluates exact analytic moments and adversarial matrix inequalities. Source calls and RNG draws are both zero. General confidence, complexity and error statements follow from the analytic argument above, not from finite tests.
