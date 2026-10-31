# Finite-horizon retained telegraph simulator: assembled theorem candidate

31 October 2026. The full construction has received an internal independent mathematical-existence review, with the binding completions below. Review of the exact staged author-body version is being recorded separately. This is a theoretical finite-circuit construction, not an implemented compiler, a practical advantage measurement, or a novelty certification.

## Statement
Let H0 and A be bounded Hermitian operators supplied through controlled block encodings with known positive normalizations alpha0 and alphaA. The encodings are exact or can be supplied to every requested accuracy, and any precision-dependent implementation cost is charged. An unknown fixed encoding error does not support arbitrary output precision. Let lambda,gamma,T be nonnegative rational inputs of finite bit length. On [0,T], consider

H_xi(t)=H0+sqrt(gamma*lambda) xi(t) A,

where xi is a stationary symmetric telegraph process with flip rate lambda. Fix p intervention times with finite rational or certified input representations. The interventions themselves may be arbitrary quantum instruments on the system and retained ancillas, adaptive to all earlier physical outcome records. The simulator does not expose its random seed, Poisson count, tree nodes or private work registers.

Subject to the finite-bit source construction documented separately, there is a finite randomized quantum circuit whose visible controlled process differs from the exact averaged process by at most epsilon in output trace norm, uniformly over initial reference-entangled states and such interventions. It preserves the same simulated noise memory across all slots. Its total gate count, private space and random-bit consumption are bounded by a polynomial in

1+alpha0*T+p+alphaA*sqrt(gamma*T),
the input bit length and block-encoding register widths,
log(2+lambda*T), and log(1/epsilon),

with the supplied block-encoding gate costs charged multiplicatively. External intervention implementation costs are additional. This polynomial claim is deliberately not an optimal linear-resource estimate. Zero lambda, T, gamma or A cases are handled directly.

## Proof assembly
Write h=||H0||<=alpha0 and a=||A||<=alphaA. Choose total source/coupling failure budget eta=epsilon/64 and path accuracy d=epsilon/[64(1+alphaA)(p+1+alpha0*T)]. The constants leave ample slack rather than optimizing the final bound.

1. Construct the iid finite-word path source with cutoff Nmax, capped Poisson and integer-shape Gamma/Beta samplers, consistent dyadic tree splits, and path error at most d except with probability eta. Count truncation and all sampler/numeric failures are included in eta. The chronological parity-mass tree permits O(log(Nmax+2)) node evaluations per time query; the earlier two-prefix-tree binary search gives a valid O(log^2(Nmax+2)) alternative. Both have polynomial bit cost in log Nmax and the required precision, not in Nmax.

2. Use the deterministic amplitude bound from the stationary telegraph exponential moment with J=ceil(sqrt(lambda*T))+1 grid points and B=sqrt(gamma*T)[1+sqrt(2 log(2J/eta))]. The spacing makes path oscillation at most sqrt(gamma*T). The exact path stays in [-B,B] with probability at least 1-eta. Clip the finite oracle path to this range. On the exact-path good event, clipping does not enlarge its uniform distance from the exact path. B grows only as a square root of a logarithm in the switching rate, at fixed gamma,T. This normalized clipping bound is necessary: an additive unit independent of gamma*T would introduce an uncharged alphaA cost when gamma*T is tiny.

3. For each free interval use R(t)=exp(-iA W(t)) and simulate the bounded transformed Hamiltonian R(t)^dagger H0 R(t). Its norm is at most alpha0. The path is Lipschitz with constant sqrt(gamma*lambda), so the transformed Hamiltonian has Lipschitz constant at most 2alphaA*alpha0*sqrt(gamma*lambda), with conservative numerical slack. Clipping preserves this Lipschitz property for the continuous interpolated path, not for its rounded digital output. Charge the final oracle value/time rounding as a separate uniform Hamiltonian error before applying the simulation bound. A uniform-grid Hamiltonian approximation has operator error at most L*T^2/M by Duhamel; thus the number of time-grid bits is logarithmic in the rate and inverse error. Discrete Dyson truncation contributes the ordinary collision/truncation bounds. Low-Wiebe's finite truncated-Dyson circuit supplies this time-access-based simulation; no direct evolution through each telegraph flip is used.

4. Implement each transformed block encoding by computing the path value coherently, conjugating the H0 block encoding with simulated exp(-iAw), and uncomputing the path. Clipping bounds |w| by B, so ordinary Hamiltonian simulation of A has cost polynomial in alphaA*B and logarithmic inverse precision. No free fast-forwarding oracle is assumed. Partition into O(1+p+alpha0*T) segments, choose a conservative logarithmic Dyson degree, and assign per-call synthesis accuracy from the resulting deterministic outer query bound. Trace out or measure simulator-private failure work; if needed, use squared internal accuracy to bound the complete output channel rather than a postselected top block. This changes only logarithmic precision costs. The resulting number q of primitive source-word oracle calls is fixed before seed compilation and includes uncomputation.

5. Replace the iid source table, conditional on the separately sampled private N and sign, by a 2q-wise independent finite-field polynomial. Store its coefficients as a private seed. Horner evaluation costs O(q) field operations per source query, yielding a charged O(q^2 poly(w)) total seed-oracle overhead. A capped exact irreducibility test supplies the field with separately budgeted failure probability. The standard quantum polynomial argument makes the averaged visible output exactly equal to the iid finite-word algorithm's output. It does not equate their full latent path laws. All iid source-error bounds are applied before this replacement.

6. On the coupled good event, the fixed-time intervention telescope gives output trace-norm error at most 4alphaA[(p+1)+alpha0*T]d. Bad events contribute at most twice their total probability. Add the separately budgeted simulation and finite-field setup errors. The budgets can be chosen to sum to less than epsilon. This bound is independent of the chosen instruments, their retained memory and initial external reference, so it is a controlled-process guarantee, not merely agreement of the one-time marginal channel.

Every loop in the source construction is bounded by a polynomial in the listed logarithmic precision parameters, with no loop over Nmax. A full conceptual tree is used only for coupling analysis. Finite-field seed generation, samplers, arithmetic, path addressing, coherent comparison, A conjugations, H0 calls and returned private memory are all charged. The separate sampler arithmetic and ordinary simulation interfaces have been mathematically reviewed under these conventions. This establishes the stated existence/resource form, without an executable circuit validation.

## Boundary of the claim
- Fixed prescribed intervention times; adaptive outcomes/operations are covered. Arbitrary adaptive intervention times or unrestricted continuous control Hamiltonians require further timing and query-budget analysis.
- One fixed noise operator A. Noncommuting multiple noise directions need additional time-ordering information.
- Finite horizon and compiled query budget. Keeping one seed is necessary, but unlimited future use is not certified.
- Errors are for unconditional output states including physical records. Normalizing an arbitrarily rare postselected branch may amplify error.
- Inputs are specified generators/rates and block encodings. Inferring real device noise or building those encodings from unavailable data is a separate acquisition problem.
- Observable estimation still pays ordinary sampling costs. The theorem is not a one-sample high-precision estimator.

## Strong comparators and credit
Low and Wiebe, arXiv:1805.00675, already supply derivative-efficient coherent time-dependent simulation. Li et al., AISTATS 2020, https://proceedings.mlr.press/v108/li20i.html, and Jelinčič, Foster and Kidger, arXiv:2405.06464, already supply lazy single-seed Brownian paths and integrals. Constant-acceptance Poisson/log-concave sampling and quantum limited-independence are established machinery. The candidate adds their explicit finite-bit telegraph source/controlled-simulation connection, if the full accounting holds.

For small system dimension the exact two-component stochastic-Liouville generator can already be handled by dense matrix exponentiation with logarithmic dependence on large norm through scaling and squaring. No universal speedup over that or all quantum Lindblad algorithms is claimed. Literature novelty and any useful practical regime remain unresolved.

## Additional spectral comparator
Bouland, Dandapani and Prakash, arXiv:2303.06719, already construct efficient quantum amplitude representations of stochastic paths. Their individual-value readout interface is different from the reversible digital same-path oracle required here. This difference alone does not prove historical novelty or an unconditional practical speedup.

## Direct ordinary trajectory comparator
Borras and Marvian, Quantum 10, 2063 (2026), https://quantum-journal.org/papers/q-2026-04-13-2063/, apply to the sign-register dilation H_ext=H0 tensor I+sqrt(gamma*lambda) A tensor Z with jump sqrt(lambda) I tensor X. Its total jump square is lambda I, meeting their scalar-rate condition. The sign register must be retained across interventions. Their ordinary jump trajectory construction is a direct informed comparator; processing a typical lambda*T jump list is the source burden removed by this compact-path construction. This is not a lower bound on all alternative methods.

An, Onwunta and Yang, Quantum 10, 1986 (2026), https://quantum-journal.org/papers/q-2026-01-27-1986/, treat strictly dissipative linear ODE state preparation. The full trace-preserving sign dilation has a stationary zero mode, so the strict-dissipativity theorem does not immediately give its controlled CPTP process. Adaptations remain possible. Gao, Ji and Liu, PRL137,160405 (2026), https://doi.org/10.1103/qy4b-gzlq, establish Hamiltonian twirling fast-forwarding for Levy-Khintchine families; only the accessible abstract was used here, not authorization-restricted full text.
