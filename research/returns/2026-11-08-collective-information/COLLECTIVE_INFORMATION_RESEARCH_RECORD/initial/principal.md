# Independent principal investigation: relative-energy coarse dynamics

Frozen initial construction, 7 November 2026. No peer initial report read. This is a scoped construction, not the broad breakthrough.

## Strongest operation targeted
Retain a collective coordinate carrying phase coexistence; eliminate only conditionally fast hidden motion. Seek a bound uniform in observation horizon and WITHOUT the inverse gap of the macroscopic dynamics. Then acquire local kinetic data once, synthesize the collective generator and evaluate new preparations/drives including metastable behavior without microscopic simulation. Distinguished physical limitation: the initially explicit implementation uses fast stirring and known stationary macro weights. It does not solve generic liquids/glasses or arbitrary thermodynamic drives.

## Relative-form stability lemma (proved here, priority unassessed)
Let A(t), C(t) be measurable finite-dimensional positive self-adjoint generators in a single fixed real Hilbert space. Suppose
|<v,(A-C)w>| <= d <v,Cv>^(1/2)<w,Cw>^(1/2), 0<=d<1,
uniformly in t. The respective forward evolution operators satisfy
||U_A(T,0)-U_C(T,0)|| <= d/(2 sqrt(1-d)) for EVERY T, with NO commutation, gap or mixing assumption. (The factor may be larger than trivial 2; cap.)
Proof: the form hypothesis implies A>=(1-d)C. Duhamel paired with f,g has integrand bounded by d/sqrt(1-d) sqrt(E_A(h_t))sqrt(E_C(k_t)), where h_t=U_A(T,t)^*g, k_t=U_C(t,0)f. The forward/backward contraction energy identities bound the two integrals respectively by ||g||^2/2 and ||f||^2/2. Cauchy-Schwarz proves the assertion. Approximation handles piecewise continuous bounded coefficients. This is an elementary parabolic energy estimate, not a claim of a new physical principle.

## Coarse-graining consequence
Let L(t)=-(F+B(t)) on finite microscopic states, reversible in a fixed stationary law pi. F>=0 is fast and ker F is a supplied retained subspace P, namely conditional expectations on a partition. Q=I-P. F>=gamma Q. B(t)>=0 is a slow reversible generator with ||B(t)||<=Lambda. Let C(t)=PBP + QAQ. It is block diagonal. Since PBQ comes only from B,
|<p,Bq>| <= sqrt(<p,Bp>)sqrt(<q,Bq>) <= sqrt(Lambda/gamma) sqrt(<p,Cp>)sqrt(<q,Cq>).
The complete off-diagonal form therefore has relative norm d=sqrt(Lambda/gamma). Consequently for all T and arbitrary time-dependent kinetic controls B(t),
||P U_A(T,0) P - U_(PBP)(T,0)|| <= d/(2sqrt(1-d)).
In fact ||U_A P-U_C P|| has the same bound. For initial microscopic density f=dmu/dpi and a retained |g|<=1, prediction from the initial collective distribution has error <=||f||_L2(pi) d/(2sqrt(1-d)). No macro gap. For phase-conditioned equilibrium preparations of probability>=a, ||f||<=a^(-1/2). For a sharply specified improbable microscopic source, this warmness factor can be exponential; do not hide it.

The Markov reduced generator PBP has conditional mean jump rates. It is not an unknown MZ memory functional, but it is still unconstructed unless those conditional averages can be acquired or calculated. Fast equilibration inside the supplied partition is not a learned universal representation-discovery theorem.

## Explicit strong-interaction model
N binary spins on a connected finite graph with swap Laplacian gap lambda_graph. Energy U(k), k=number of up spins, may be nonconvex and of Curie-Weiss scale N; bounded increments |U(k+1)-U(k)|<=J ensure slow individual flip rates have bounded positive prefactors. Fast nearest-neighbor swaps at rate kappa preserve k. Conditional equilibrium on each k shell is exactly uniform, irrespective of the phase coexistence induced by U(k). Use a symmetric local mobility b_i(neighbor spins,u) in [bmin,bmax], unchanged on flipping spin i, and rate b_i exp[-beta(U(k')-U(k))/2]. Arbitrarily many local mobilities can be unknown; require a finite local dictionary and homogeneous/shared coefficients to transfer sizes.

Swaps have conditional spectral gap kappa*lambda_graph (Aldous/SEP spectral gap is an external dependency to verify). Slow generator norm <=2N bmax exp(beta J/2). Then gamma/Lambda controls uniform all-time coarse error. On D-dimensional side-L grid, lambda_graph~L^-2: kappa=O(N L^2/epsilon^2) for fixed warmness. THIS IS A LARGE PHYSICAL RESOURCE, not free cooling. Total fast event rate is O(N kappa), to be charged during real acquisition/physical prediction.

Macro weights are known pi_k proportional binomial(N,k) exp[-beta U(k)]. The reduced birth/death rates are explicit hypergeometric averages of local b_i over uniform k shells. Thus a learned finite table b(local pattern,u) produces all macro rates for any N by combinatorics, not equilibrium simulation. The same table predicts NEW macroscopic initial distributions with a stated warmness bound and arbitrary time-dependent kinetic drives that preserve the same U, provided the mobility family/control interpolation is acquired and its relative accuracy is certified. Arbitrary new field U(t,k) changes stationary weights and is not yet covered by the horizon-free theorem.

No claim that this model is outside all previously tractable classes: exchangeability plus averaging has classical predecessors. Its purpose is to test a genuine end-to-end theorem including metastable slow modes and all-time error, and expose precisely what a more general physical bridge must replace.

## Acquisition and learned dynamics
For a known stationary pi and same-edge learned reversible slow generator Bhat(t), if each microscopic mobility has relative error eta, form comparability gives relative error <=eta. Projection preserves it. The stability lemma bounds the reduced learned dynamics uniformly in time by eta/(2sqrt(1-eta)). Add coarse error; do NOT use a path-KL bound growing T if the stronger common-equilibrium form hypothesis applies.

Controlled local calibration of b: prepare a specified neighbor pattern and k shell, record an elementary flip over a short interval h. Known lower/upper rates, O(h^2) multiple-event bias and calibrated readout give confidence error. There is no exponential waiting when single-spin energy increments are bounded; a shell or representative pattern may require O(N) preparation/reset per shot. If continuous control dependence is arbitrary, no finite acquisition suffices: require a declared bounded finite-dimensional basis, Lipschitz mesh, or analytic dependence and charge the coverage. Micro observation time h must include fast-swap contamination: calibration must switch off/stall stirring, or use event-resolved rate estimation with charged resolution. Unknown control of stirring is a missing apparatus premise, not something the theorem grants.

After acquisition, evaluating a birth/death matrix of size N+1 has polynomial memory and arithmetic. For a piecewise-constant drive with K pieces, stable matrix exponential with certified rational precision costs poly(N,log T,log(1/epsilon),input bits), subject to verifying an actual numerical algorithm and conditioning; stochastic positivity plus scaling/squaring avoids exp(T) work but requires per-squaring precision O(log T). New arbitrary continuously specified drives require their description/variation and integration costs; no free binary-horizon guarantee.

## Obstructions and follow-ups
1. Small local marginal error cannot control long-time macro source behavior (previous source obstruction capital). Need retain phase/history or a verified conditional mixing bound.
2. No finite calibration determines an arbitrary function of an unseen continuous drive; coverage/regularity must be part of physical assumptions.
3. Retaining k only fails at finite stirring unless gamma/Lambda is controlled. The derived resource may destroy practical advantage.
4. Exponentially long metastable times cannot generally be acquired by observing unforced rare transitions; count-clamped local kinetics and known combinatorics avoid that only in the specified model.
5. Thermodynamic drive changes pi, projection and warmness; extending horizon-free reuse to genuinely extensive new fields is decisive and unresolved here.
6. Unknown arbitrary interactions U or site disorder cannot be replaced with the known U/shared local dictionary without acquisition costs. The actual endpoint requires discovering a sufficient partition with controllable conditional mixing and computable conditional averages beyond exchangeable models.
