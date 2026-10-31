# Independent local review: ordinary mixing and scaled fast-kernel acquisition

## Exact source and verdict

I read Sections 3–4 of `PRIMARY_COMPARISON_AND_ORDINARY_KERNEL.md`, including the final acquired-normalization, robust-amplification and scaled-time-derivative completions. Final source: 19,772 bytes, SHA-256 `4360e7ccdb5fead0a34115eb8292d647c67755e3e0b7398f080d2883d59623d9`.

**PASS, at the stated local mathematical-construction scope.** Section 3 earns the source-only shortcut and its limited counterexamples. Section 4 earns a finite operator block for the exponentially rescaled no-jump semigroup from acquired dark-generator operators and an actual return certificate. This is a genuine ordinary alternative to the special grouped-Poisson kernel. It does not, by itself, earn a low-activity realization, complete first-event instrument, or generalized interacting-source compiler. This receipt does not certify every literature comparison elsewhere in the report, an implemented circuit, practical efficiency, or novelty.

## 1. Source-only return and mixing

For a pure fixed state with projection P, positivity gives Phi-dagger(Q)<=Q. The supplied m-step bound iterates to 16^{-floor(n/m)}Q. For arbitrary source/reference input, projecting the output onto P costs at most 2 sqrt(p), where p is its Q population. The missing projected reference marginal is positive with trace p, so replacing it by the unchanged reference marginal costs another p. The stated diamond bound 3*4^{-floor(n/m)} follows uniformly over references.

Poissonization and 4^{-floor(n/m)}<=4(4^{-1/m})^n give the displayed 12 exp[-lambda t(1-4^{-1/m})] estimate. Below the mixing cutoff the Poisson mean is polynomial in m and log(1/epsilon); above it, source reset is an ordinary implementation. Prescribed-control composition is ordinary diamond telescoping.

The driven reset example is consistent: fair sign refresh at rate lambda gives coherence equation f''+lambda f'+4 lambda b^2 f=0, with f(0)=1 and f'(0)=0. Its fixed-time large-rate limit is exp(-4b^2 t), not the identity. It rules out the naive centered-mean replacement, not stronger effective models. The inverse reset-semigroup formula likewise correctly exhibits exponential growth on reset-annihilated directions and failure of a naive unitary inverse-frame substitution.

## 2. Actual return implies no-jump contraction

With JP=0 and Hermitian Hs satisfying HsP=0, both P and Q reduce D=-iHs-J-dagger J/2. Its exponential is contractive, and Q inputs remain in Q under no-jump evolution. The no-jump CP map is a positive summand of the actual Lindblad channel. Therefore the supplied survival inequality exp(m G0-dagger)(Q)<=Q/16 implies ||exp(mD)Q||<=1/4. A spectral-gap label alone would not justify this implication or acquire the needed operations.

## 3. Ordinary operator LCHS and finite coefficient preparation

I checked the LCHS kernel against the accessible primary An–Childs–Lin text, equations (32)–(33), and its operator block in equation (101): https://arxiv.org/html/2312.03916v2 . This is an operator construction, not merely a normalized-state solution guarantee. The present receipt uses the conservative quadrature proof, not the optional optimized-quadrature citation.

On the real axis the Hamiltonian factors are unitary and the kernel tail decays as exp(-c sqrt(R)). On |Im k|<=1/2, the kernel has no pole or branch crossing. The logarithmic norm of the continued exponential is at most ||C||/4, so its norm for u<=m is bounded by exp(m||C||/4), independently of ||Hs||. Fixed-width panels admit a uniform Bernstein ellipse. Analytic polynomial approximation and positive Gaussian quadrature then yield the asserted finite rule with q polynomial in m alpha_C and log(R/eta), using an acquired alpha_C>=||C||.

The positive quadrature weights sum to the interval length. Bounded real-axis kernel values therefore give O(R) coefficient normalization. Nodes, weights and complex coefficients can be approximated by finite arithmetic and explicit polynomial-sized state preparation. Small coefficients require absolute/squared-tolerance preparation, not division by an unearned lower bound. SELECT charges the acquired Hamiltonian normalization alpha_Hs+R alpha_C/2 and actual controlled binary-duration simulations. The jump-stack product supplies alpha_C=alpha_J^2 when no tighter certificate is available. There is no exact operator-norm oracle.

Both desired amplified blocks have norm at most one half. Thus standard singular-value amplification with slack is appropriate. The final source explicitly distinguishes raw block error from output error: using the conservative robust SVT bound O(d sqrt(eta_raw)), eta_raw<=(eta_out/(100d))^2 and phase precision O(eta_out/d) suffice. Conservative polynomial choices for the quadrature cutoff and amplification degree close the logarithmic dependence of precision on degree. No exact amplification at the unit-singular-value boundary is invoked.

## 4. Grouping and time rounding

For t=km+r, reduction by Q gives B^k R_r=2^{k-1} exp(tD)Q. Multiplication by (1/2)exp(a't)2^{-k} therefore gives exactly F_D(t)=(1/4)exp(a't)exp(tD)Q. The scalar is at most 1/sqrt(2); B and R_r are contractions with norm at most one half. The displayed estimate ||F_D(t)||<=exp(-a't) follows directly from the m-step contraction. Consequently above the logarithmic decay cutoff the zero block is valid; below it only O(log(1/epsilon)) factors are required.

Fresh block ancillas and ordinary contraction-product telescoping justify error O(epsilon/(k+1)) per factor. These are powers of an acquired operator, not singular-value powers. The grouped formula is the same smooth function across k-boundaries. Its derivative is (a'I+D)F_D, bounded by the acquired alpha_Hs+alpha_C/2+a', so finite timestamp rounding is priced for the scaled block itself. The hard zero cutoff adds only its explicitly budgeted discarded norm.

## 5. Resource and interpretation boundaries

Costs are polynomial in the supplied certificate time m, acquired source/Hamiltonian normalizations, register and arithmetic sizes, and log(1/epsilon), with the queried duration represented in finite bits. If a certificate is initially supplied at a time smaller than one, it may be padded to time one: pure dark stationarity makes survival nonincreasing, preserving the certificate. No unexamined inverse-small-m complexity is required.

Query bounds do not imply gate bounds for opaque oracles; actual encoding, state-preparation, controlled-inverse and Hamiltonian-simulation costs remain charged. The construction improves the ordinary comparator at precisely the scaled-kernel interface. Extending it to a whole coupled source requires independently earning activity, integrable event envelopes, complete CP/isometry assembly, private-clock continuation and controlled error composition. No such promotion is made here. Earlier accepted source compilers and their frozen proofs remain unchanged.
