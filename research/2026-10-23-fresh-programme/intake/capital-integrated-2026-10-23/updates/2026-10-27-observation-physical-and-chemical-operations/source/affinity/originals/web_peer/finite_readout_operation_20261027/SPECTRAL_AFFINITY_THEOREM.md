# A non-Gaussian, sensor-phase-robust cycle-affinity bound

Derived 27 October2026. This is a replacement target for the failed covariance-only **rate** floor. The existing three-channel covariance functional can instead bound the driving force per microscopic cycle. No physical achievement or historical priority is asserted. The finite inference/readout construction is recorded separately.

## Source contract and the established sector input

The source is an irreducible finite-state continuous-time Markov chain, stationary, with positive bidirectional rates on its edges. Microscopic states/observables are time-even; no fixed unreversed odd control or coherent quantum generator is included. Physical observables are arbitrary real functions of the source state. Their labels and the stationary probabilities need not be observed by the inference operation.

Let Amax be the maximum absolute affinity over oriented simple cycles, where a cycle affinity is the log product of its forward rates divided by reverse rates. Define Amax=0 for a cycle-free network, whose bidirectional dynamics obey detailed balance and have A=0. If local detailed balance is supplied, it is entropy delivered to the reservoirs per traversal in k_B units. Without that physical identification it remains a dimensionless Markov rate-ratio quantity.

Use the stationary real Hilbert space, remove constants, and write the backward generator as `L=-S+A`, with S symmetric positive definite and A skew-symmetric. Define

`K=S^(-1/2) A S^(-1/2)`, `kappa=||K||_2`.

The short-lag normalized cross-correlation asymmetry of real observables a,b is exactly `<b,Aa>/sqrt(<a,Sa><b,Sb>)`. Its supremum over a,b is kappa. Ohga, Ito & Kolchinsky, PRL131,077101(2023), Eq3 therefore gives the **established** input

`kappa <= max_c cot(pi/n_c) tanh(F_c/(2n_c)) <= Amax/(2pi)`.

The published main theorem/system/derivation were read in full. The source is finite-state, stationary and uses state observables. Its published finite-time-lag extension was a conjecture; it is not used here. Exact supplementary assumptions and adjacent later work are being checked separately, not silently supplied by the word 'universal'.

## Uniform spectral cone: complete proof

On the full centered state-function space the covariance kernel is represented by L. Its spectral matrix is

`C_full(w)=R(w)+R(w)^dagger=2 R(w)^dagger S R(w)`,

`R(w)=(S-A+i w I)^(-1)`.

This is a covariance identity for a Markov chain, not a claim that its paths are Gaussian. The same identity also constructs a covariance-matching OU process if desired.

Write the Hermitian precision P=C_full^(-1)=P_R+i P_I, where the subscript R denotes real symmetric and I real skew-symmetric parts. Direct expansion gives

`2P_R=S-A S^(-1)A+w^2 S^(-1)`,

`2P_I=w(A S^(-1)+S^(-1)A)`.

Apply the real congruence S^(-1/2) and put B=w S^(-1). Then

`2P'_R=I-K^2+B^2`, `2P'_I=KB+BK`.

For any real vectors x,y,

`2 x^T P'_R x=||x||^2+||Kx||^2+||Bx||^2`,

`2 x^T P'_I y=-(Kx)·(By)+(Bx)·(Ky)`.

For kappa>0 set `alpha=sqrt(1+kappa^(-2))`. Since `||Kx||<=kappa||x||`, the first expression is at least `alpha^2||Kx||^2+||Bx||^2`. Apply Cauchy–Schwarz to the two block vectors `(alpha Kx,Bx)` and `(alpha Ky,By)`, with the skew block matrix having norm 1/alpha. This gives

`||P_R^(-1/2) P_I P_R^(-1/2)|| <= kappa/sqrt(1+kappa^2)`.

The kappa=0 case has A=0 and zero imaginary part.

The canonical imaginary norm is invariant under real nonsingular congruence and **under Hermitian inversion**. To see the latter, whiten the real part to write P=I+iJ with J real skew. Then

`P^(-1)=(I-iJ)(I+J^2)^(-1)`.

Whitening this inverse's real part gives canonical imaginary matrix -J, because the real part is a function of J^2 and commutes with J. Thus for every w,

`r(C_full):=||Re(C_full)^(-1/2) Im(C_full) Re(C_full)^(-1/2)||`

`<= r0:=kappa/sqrt(1+kappa^2)`.

Real observable projections preserve this bound by restriction of the quadratic-form inequality. Adding any real PSD covariance also preserves it. Equivalently the cone is given by the **linear matrix inequalities**

`r0 Re(C) + i Im(C) >= 0`, `r0 Re(C) - i Im(C) >= 0`.

The cone is closed under positive averaging. No Gaussian assumption occurs in these statements.

## Finite window and unknown sensor response

For a common known real finite gate w(t), define `Z_i(v)=integral w(t) f_i(X_t) exp(i v t) dt`. Center means in the covariance. Stationarity gives

`Cov Z(v)=integral |W(v-u)|^2 C_f(u) du/(2pi)`.

Every physical spectral matrix C_f(u) lies in the same cone. The finite-window covariance therefore does too. Arbitrary common sample times and real sample weights also give a nonnegative squared-window kernel, so sampling/alias averaging does not require a bandlimit for this particular uniform-cone implication.

The gate must be **before** every unknown separate temporal filter whose phase is being removed, and its complete response must be captured or an acquired tail error charged. Then the finite Fourier record satisfies `Y_i=H_i(v)Z_i` in a pathwise LTI model, or the same relation holds for conditional means in the photon-counting operation below. No smoothed output spectrum is substituted for a true filtered source spectrum.

Real cross-channel PSD covariance noise **before the distinct filters** is permitted when its covariance satisfies the stated real-cone contract and source cross-terms vanish. After the filters, independent diagonal read noise is permitted. Arbitrary real correlated noise added **after** them is not interchangeable: pulling it through distinct unknown phases generally makes it complex and can fake the source signal. A common camera's correlated error does not automatically qualify.

Writing H=U D with U diagonal unitary and D real nonnegative, the actual inverse phase gauge takes the measured covariance into a real congruence of a cone element plus allowable real PSD noise. Thus its canonical imaginary norm is at most r0. Filter zeros reduce information; no lower gain bound is needed for validity, although power can disappear.

## Three-channel affinity operation

For any positive-definite three-channel covariance C, let

`T(C)=tr[(C^T)^(-1) C]-3`,

`F(C)=min_diagonal_unitary_U T(U C U^dagger)`.

These are matrix functionals; no physical Gaussian path law is being inferred. If the real part is whitened, the 3x3 skew imaginary part has eigenvalues 0,+i r,-i r. Directly,

`T(C)=4r^2/(1-r^2)`.

Choosing the actual inverse sensor phase gauge therefore gives

`F(C_Y)<=4 kappa^2 <= Amax^2/pi^2`.

Consequently the positive operation is

**`Amax >= pi sqrt(F(C_Y))`.**

F has the exact complex 3x3 SDP representation proved in the previous unit, with exact rational dual certificates available. The simpler closure bound also gives

`Amax >= (2pi/sqrt(27)) |Im(C12 C23 C31)/(C11 C22 C33)|`.

The stronger exact point-input bound does not by itself supply finite-data confidence. Confidence sets must be transported without assuming Gaussian trajectories. The rare-active-cycle counterfamily is compatible with this theorem: its rate tends to zero but its maximum cycle affinity tends to 3 log2, whereas its covariance F stays positive.

## Matched ordinary comparator and unresolved priority

Ohga/Ito/Kolchinsky already infer affinity from calibrated short-lag state-observable correlations; their cycle/sector theorem is not rediscovered here. Later finite-time cross-correlation and total-cycle-affinity work must also be compared at its exact input contract. They receive all the same physical records, gate, noise and mixing information. A known raw observable or calibrated filter can give an ordinary method a stronger bound; no uniform superiority is claimed.

The distinct candidate bridge is: unknown separate response phases, non-Gaussian photon/readout records, finite pre-filter gates/full tails, and a source cycle-force floor with no microscopic labels or Gaussian-rate conversion. Historical same-operator priority is UNKNOWN. A conditional theorem and finite acquisition mathematics are not a demonstrated working instrument or discovery multiplier.
