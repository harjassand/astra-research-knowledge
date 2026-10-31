# Dark-sector excursions for a general finite Markov source

Root construction, 31 October 2026. Unreviewed compiler candidate. It builds on the separately proposed pure stationary completion, whose formulas and activity bound are still under independent review. No cheap general-source Kraus oracle is assumed.

## 1. Explicit source costs and centering
The finite source Q, positive stationary pi and its pure vector psi are explicitly available. Let P=|psi><psi| and Qperp=I-P. The free reservoir no-jump generator is lambda D0, with D0 P=P D0=0 and D0+D0^dagger=-C0. A certified source gap C0>=c Qperp, c>0, is charged. Other source costs include dimension d, the source matrix norms, the jump norms le=||L_e/sqrt(lambda)||, their sum of squares S_L, and pi_min^-1. No efficient oracle access to an exponentially large unlisted source graph is granted.

Let K=sum_j A_j tensor diag(f_j), after subtracting its stationary system mean. Thus PKP=0. A computable normalization b>=||K|| may be the sum of the supplied Ai normalizations times their centered source-function sup norms. A removed nonzero mean is added to H0; its actual physical simulation cost is paid and may itself grow with sqrt(lambda).

The no-jump generator is
D=-iH0+lambda D0-i sqrt(lambda)K.
The fast reservoir block Df=Qperp D0 Qperp has Hermitian part at most -c/2.

## 2. Low-rate branch is ordinary
If lambda<64b^2/c^2, ordinary quantum Lindblad simulation has generator normalization bounded by a polynomial in b,c^-1,H0 and the explicitly supplied source norms. This is not a large-lambda cost: lambda is bounded by the declared physical/source threshold. Its high-precision operator-encoding costs remain charged. The proposed special construction is needed only above that threshold.

## 3. Positive two-sector majorant at high rate
For lambda>=64b^2/c^2, factor the fast free propagation on Qperp as

exp(lambda Df u)=exp(-lambda c u/2) F(u),
F(u)=exp[lambda(Df+cI/2)u], ||F(u)||<=1.

Remove H0 in the usual interaction picture. Expand K into its ground-to-fast, fast-to-ground and fast-to-fast blocks. There is no ground-to-ground block after centering. Every normalized insertion has norm at most one when divided by b. A ground/fast transition has scalar coefficient g=sqrt(lambda)b. A fast self-insertion has the same coefficient but does not change the sector.

Sum the positive self-insertion scalar weights on each fast residence interval. This produces exp(g*u), which combines with the fast decay into exp(-kappa*u), where

kappa=lambda c/2-g>=3lambda c/8.

The remaining two-sector path majorant is
M=[[0,g],[g,-kappa]].
Its Perron value s=(sqrt(kappa^2+4g^2)-kappa)/2 satisfies s<=g^2/kappa<=8b^2/(3c). Its Doob upward and downward rates are s and dfast=kappa+s. The standard two-state conditional bridge acquisition already developed therefore applies to the macro-sector path, with no number of macro events proportional to lambda*T.

Conditional on a fast residence of length u, independently acquire a Poisson(g*u) number of self-insertions and uniform ordered insertion times. This is not an omitted normalization: the Poisson probability contributes exp(-g*u), which precisely compensates the exp(g*u) already included in the scalar majorant. Insert Qperp K Qperp/b and the intervening normalized F propagators in chronological order. Ground/fast transitions insert the corresponding projected blocks of K/b. All products remain contractions.

## 4. The extra self-insertions also have a rate-independent cap
The high-rate threshold gives g/dfast<=1/3. During an unconditioned fast visit, extend its lifetime to a full Exp(dfast) sample. The number of rate-g marks before that return has a geometric generating function dfast/[dfast-g(exp(theta)-1)]. At theta=log2 it is at most 3/2.

Use a rate-s proposal up-clock over the whole window. Give each proposal an independent extended fast lifetime and its Poisson marks, even if that proposal arrives during an already fast period and is ignored. Accepted visits are a subset. Add one possible initial fast visit. Thus the combined macro-transition/self-insertion count is bounded by a compound Poisson construction with constant exponential mark moment and rate s, plus one initial geometric mark. It has exponential tails controlled by O(s*tau+1), uniformly in lambda. Endpoint conditioning divides by the two-state endpoint probability, whose logarithm is priced as in the earlier bridge construction.

Fast residence intervals can additionally be capped at lambda*u<=O(c^-1 log(Kcap/(eta Pendpoint))). The full return-time tail is exponential at rate dfast>=3lambda c/8. This cap costs only a logarithmic precision/source budget and ensures that no normalized fast-matrix evaluation runs for a lambda-sized numerical interval.

Global near-endpoint/near-coincidence exclusions, raw-uniform CDF inversion, conditional-duration TV stability and chronological ordering are mandatory. They now include the Poisson self-insertion times. Their rates may be large, but only logarithms of those rates enter the timing mesh. All virtual counts, not merely the number of ground/fast transitions, must be capped.

## 5. Actually implementing a normalized fast propagator
F(u) acts only on the explicitly described d-dimensional reservoir, not on the exponentially large system. On the retained fast-duration cap, its matrix exponential can be evaluated reversibly by finite matrix arithmetic at cost polynomial in d, ||Df||/c, input bits and logarithmic error. A simple scaled Taylor/product scheme can use a number of stages proportional to the source-conditioned argument bound, not lambda*T. Uniform arithmetic error is charged separately from timing perturbations.

Do not block encode F with a sqrt(d) normalization at EVERY interval: that could produce an exponential path normalization. Instead construct a norm-one unitary dilation of the known contraction matrix. Compute F to certified absolute accuracy, rescale it slightly to keep norm at most one, and form its Julia unitary using sqrt(I-FF^dagger) and sqrt(I-F^dagger F).

The required matrix square roots have a polynomial-bit algorithm without a gap assumption. For positive M with norm<=1, Newton iteration X0=I, X_(k+1)=(X_k+M X_k^-1)/2 has eigenvalue error at most 2^-k and X_k>=2^-k I. Use O(log(1/error)) iterations with polynomially many guard bits; inverses have only exponentially large CONDITION NUMBERS in the iteration index, whose logarithms are polynomial. Round at each step rather than allowing exact rational denominators to grow unchecked. Finite unitary decomposition into elementary rotations then costs polynomial in d and precision. Near-zero rotation pivots are clipped only with a charged absolute error. Angle registers can be synthesized through binary-controlled rotations, not a table over all possible u.

This supplies a concrete small-reservoir computation route; it is not a claim of fast-forwarding an arbitrary large black-box dissipative matrix. A full proof must make the guard-bit and unitary-decomposition bounds explicit enough for the promised polynomial cost.

## 6. Complete first-event instrument, not a lone contraction
The two-sector expansion gives K(t) from at most four sector paths, with total scalar normalization bounded by a constant times exp(s*t). Sector projectors and projected K blocks have norm-one block encodings; no rank-one identification of the whole fast sector is needed.

Every actual jump L_e annihilates the ground vector. Thus L_e K(t) uses only the fast output row of the scalar majorant, followed by the normalized known jump L_e/(sqrt(lambda)le). The same two-by-two formulas bound this row by a constant times

le [sqrt(lambda) exp(-kappa*t)+b/c] exp(s*t).

Its squared time envelope integrates to O(le^2/c + le^2 b^2*tau/c^2) times exp(O(s*tau)). Sum over the explicitly listed source edges. Choose windows tau=O(c/b^2), and the complete first-event instrument therefore has a normalizer polynomial in S_L/c and source conditioning, independent of lambda.

Prepare its no-event and event/time arms using the corresponding exponential/uniform envelope mixtures, retain only the outer Kraus coordinates, unprepare all inner virtual paths, and amplify the COMPLETE first-event isometry. The earlier common-uniform L2 time comparison and count-augmented private-time hybrid are required. State-dependent holding times are generated by the quantum instrument itself, not evaluated from an unknown system state.

The new actual-event cap comes from the pure-completion activity bound, with explicit c^-1 and pi_min^-1 costs. Reservoir state is retained across every jump, no-event window and system instrument. No reset to psi is assumed at these boundaries.

## 7. Unresolved scope
This is a candidate constructive route to removing the global switching multiplier lambda for an explicit finite correlated/nonreversible Markov source, at polynomial cost in its declared dimension/conditioning resources and the system's physical coupling scales. It is not yet accepted. The normalized fast-matrix circuit, full virtual self-event/bridge error ledger, actual first-event envelopes and source-conditioned amplification still require independent checking. Small count alone does not establish the compiler.

For a source described implicitly on exponentially many states, matrix construction or gap/stationary acquisition may be the dominant hard problem. For independent bit sources the previously completed factorized theorem avoids that explicit-state cost; this general source route must not silently claim the same advantage.
