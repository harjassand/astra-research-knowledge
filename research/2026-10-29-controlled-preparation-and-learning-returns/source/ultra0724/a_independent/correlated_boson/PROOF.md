# A globally correlated canonical receiver and a bounded-cut field sampler

29 October 2026. New construction; independent review pending. The earlier canonical positivity, phase-law obstruction, and initializer reviews are frozen. This proof changes the sampling operation, rather than the unused moments of an independent phase alphabet.

The output is a classical auxiliary-field law and canonical partition/finite-difference predictions for a declared bosonic Hamiltonian. It is not a quantum Gibbs-state preparation or a generic solution to frustrated matter. All rejection, number conditioning, normalization, precision, and finite-slice costs are retained. Ordinary HS, canonical characters, rejection, determinant calculus, lattice Fourier analysis, and recursive partition estimation are credited tools; priority and practical advantage are UNKNOWN.

## 1. Physical input and two useful classes

Let

`H=b†Tb+c†conjugate(T)c+sum_i U_i (n_bi-n_ci)^2`,

with `T>=0` Hermitian, `U_i>=0`, and separately fixed populations `K,K`. No site occupation cutoff is inserted. At finite size each flavor has `D_K=binom(M+K-1,K)` states; this physical canonical finiteness is different from truncating a grand-canonical Fock space. Fix `beta>0` and a finite symmetric slice count `L`. The intended exact continuous Gibbs trace is a separate product-formula target.

For phases `theta_(i,l)~N(0,2 beta U_i/L)`, a one-flavor history can be written cyclically as

`B_T=product_l exp[-(beta/L)T] diag(exp(i theta_(i,l)))`.

The trace of its symmetric power is unchanged by collecting the symmetric half hopping steps cyclically. Every factor is a contraction; `||B_T||<=1`. The companion flavor sees `conjugate(B_T)`. The EXACT finite-slice physical canonical trace is

`Z_(L,K)=E_base |h_K(B_T)|^2`, `h_K(B)=Tr Sym^K(B)`.

Two input admissions are useful:

* **Low whole trace:** `tau=Tr T=O(log M)`. The construction below has a polynomial full canonical cost at homogeneous finite `U_i=U`, fixed density `K/M=rho`, and a paid fugacity saddle.
* **Bounded recursive cut trace:** an explicit balanced binary decomposition is supplied, with
  `T_v=T_left directsum T_right+R_v`, `R_v>=0`, `Tr R_v<=b`, where `b` and leaf sizes are fixed. This supplies a polynomial conditional field sampler at every common phase, and a polynomial approximate joint-phase sampler/normalizer. A prescribed canonical `K` additionally consumes its acquired count probability. Section 9 supplies a nonempty dense-count class without assuming that probability for an arbitrary requested K.

An actual example of the second class is a one-dimensional triangular ladder with

`T=sum_(ij edge) j_ij (|i>+exp(i a_ij)|j>)(<i|+exp(-i a_ij)<j|)`.

Use nearest and next-nearest edges with bounded positive coefficients. A contiguous bisection cuts only a fixed number of edges, hence has bounded positive cut trace. All-positive off-diagonal triangles are frustrated: the product of their three hopping phases is positive, while three negative stoquastic hopping entries would have negative product. This is not a free gauge transformation to a sign-free occupation worldline model.

The physical PSD input matters. Adding a large scalar multiple of identity to make an arbitrary T positive changes the trace budget by `O(M)` and cannot be omitted from the cost. Its exact canonical scalar partition prefactor can be restored, but that alone does not retain these efficiency bounds.

## 2. A positive grand envelope, inside its actual convergence domain

Fix `0<r<1`. For any contraction B put

`g_phi(B)=|det(I-r exp(i phi)B)|^(-2)`,

`G_r(B)=integral_(-pi)^pi g_phi(B) dphi/(2pi)`.

All determinants are nonsingular, with least singular value at least `1-r`. Absolute convergence of the finite-dimensional inverse determinant series and Parseval give

`G_r(B)=sum_(n>=0) r^(2n)|h_n(B)|^2 >=1`.

Thus `r^(2K)|h_K(B)|^2<=G_r(B)`. This is a genuinely trace-convergent grand construction, not a finite-part continuation. Indeed `|h_n(B)|<=D_n` and

`sum_n r^(2n)D_n^2 <=(1-r)^(-2M)`.

The grand joint field/phase density is proportional to `p_base(theta) g_phi(B_T)`. Its field marginal is proportional to `p_base G_r(B_T)`. Once that marginal is sampled, accept a field with probability

`a_K(B_T)=r^(2K)|h_K(B_T)|^2/G_r(B_T)`.

The accepted field law is exactly the desired canonical one. Its acceptance is

`p_K=r^(2K)Z_(L,K)/Z_bal`,

where `Z_bal=E_base G_r(B_T)`. A grand sampler alone does not pay a small `p_K`.

## 3. The determinant comparison, including noncommuting hopping

Interpolate `T_s=T_0+sR`, with `T_0,R>=0`, and write `B_s` for the same phase history. Duhamel differentiation of each hopping exponential gives

`||dB_s/ds||_1 <= beta Tr R`.

Each other factor is a contraction; for a differentiated factor the Duhamel integrand has trace norm at most `Tr R`. No commutation of `T_0` and R is required. For `z=r exp(i phi)`,

`|d_s log det(I-zB_s)| <= r beta Tr R/(1-r)`.

Consequently, with `c_R=r beta Tr R/(1-r)` and `C_R=exp(2c_R)`,

`C_R^(-1) <= g_phi(B_1)/g_phi(B_0) <= C_R`.       (1)

The bound is simultaneous in all phases, M, and L. It follows from a norm-controlled inverse, not from diagonalizing a nonnormal B or assuming a gap between its eigenvalues.

For `T_0=0`, `B_0=D_total` is diagonal unitary. Integrating (1) over phi gives

`r^(2K)|h_K(B_T)|^2 <= C_T G_r(D_total)`,

with `C_T=exp[2r beta tau/(1-r)]`. Therefore the acquired zero-hopping grand field marginal is a direct canonical proposal: accept with

`f_K(theta)/C_T`, `f_K=r^(2K)|h_K(B_T)|^2/G_r(D_total)`.       (2)

Its mean acceptance is `r^(2K)Z_(L,K)/(C_T Z_bal,0)`. In particular this does not require sampling the unknown interacting field posterior by MCMC first.

## 4. Acquire the zero-hopping globally correlated proposal

Let `u_i=beta U_i` and let `Theta_i=sum_l theta_(i,l)~N(0,2u_i)`. Define

`q_i(phi)=E |1-r exp[i(phi+Theta_i)]|^(-2)`

`=(1-r^2)^(-1)[1+2 sum_(d>=1) r^d exp(-u_i d^2) cos(d phi)]`.

All Fourier coefficients are nonnegative, so `q_i(phi)<=q_i(0)`. First draw phi from the density proportional to `product_i q_i(phi)` by uniform rejection with acceptance `product_i q_i(phi)/q_i(0)`. This normalizer is not supplied by an oracle.

Put `C_r=sum_(d>=1)d^2 r^d=r(1+r)/(1-r)^3`. Since `1-cos(d phi)<=d^2 phi^2/2`,

`q_i(phi)/q_i(0)>=1-C_r phi^2`.

On `|phi|<=w=min(pi,[2M C_r]^(-1/2))` the product is at least `1/2`, by Bernoulli's inequality. The uniform stage therefore accepts with probability at least `w/(2pi)`, costing `O(sqrt M)` proposals at fixed r. It does not consume a local-limit theorem.

Conditional on phi, draw each total Theta_i independently from its normal law tilted by `|1-r exp[i(phi+Theta_i)]|^(-2)`. Normal rejection with envelope `(1-r)^(-2)` accepts with probability at least `[(1-r)/(1+r)]^2`. Generate the original L increments using a paid Gaussian bridge:

`theta_(i,l)=Theta_i/L+xi_(i,l)-average_l xi_(i,l)`,

with iid `xi_(i,l)~N(0,2u_i/L)`. This is the exact conditional Gaussian law. No per-site occupation is measured or collapsed. The common latent phi correlates all sites, and the conditioned total correlates all slices. Thus this law is outside the independent fixed-size-block class of the frozen phase-law barrier.

Fourier sums are absolutely convergent and have elementary geometric tails. The normalized phase integral can be acquired by a positive grid or the positive Laurent-convolution construction actually executed in `acquire.py`. Neither density evaluation nor the Gaussian bridge receives a free continuous random-number oracle in the finite-bit operation of Section 10.

## 5. The finite-slice canonical floor

Let `T_many=b†Tb+c†conjugate(T)c>=0` on the finite K,K sector and set `delta=beta/L`. The positive transfer

`C=exp(-delta V/2) exp(-delta T_many) exp(-delta V/2)`

has the same power trace as the original symmetric transfer. For each occupation basis vector alpha, scalar spectral Jensen twice gives

`Tr C^L >= sum_alpha C_aa^L`

`>=sum_alpha exp[-beta V_alpha-beta <alpha|T_many|alpha>]`.

When U is homogeneous, its diagonal canonical reference has equal site means `K/M`; all off-diagonal one-body means vanish. A final ordinary Jensen bound therefore gives

`Z_(L,K)>=Z_diag,K exp[-2 beta(K/M) tau]`.         (3)

Also `C<=exp(-delta V)`, because `exp(-delta T_many)<=I`. Eigenvalue min--max implies `Tr C^L<=Tr exp(-beta V)=Z_diag,K`. These claims hold for EVERY finite positive integer L; no unbounded-operator Trotter limit or ALT inequality is imported.

Combining (2) and (3), the low-trace sampler has acceptance at least

`exp[-2 beta tau(r/(1-r)+rho)] p_K,diag`,

where `p_K,diag=r^(2K)Z_diag,K/Z_bal,0` is acquired, rather than guessed.

At fixed homogeneous finite u and rho, this count probability is `Theta(M^(-1/2))` when r is tuned to the onsite density saddle. A self-contained effective Fourier argument is given in `COUNT_AND_PRECISION.md`; its constants are computable but can be poor. Thus `tau=O(log M)` gives a polynomial full canonical receiver with no mixing hypothesis. The actual source compiler reuses the frozen M64 diagonal interval and separately acquires its grand normalizer and count probability by exact rational bounds.

## 6. Recursive rejection: total trace need not be small

Now use the explicit bounded-cut tree in Section 1. Fix phi. At a parent, independently sample the two child conditional field laws

`p_child(theta|phi) proportional to p_base(theta) g_phi(B_child)`.

Combine their fields, compute the parent propagator B on the SAME fields, and accept with probability

`g_phi(B_parent)/[C_v g_phi(B_left)g_phi(B_right)]`,

where `C_v=exp[2r beta Tr R_v/(1-r)]`. Equation (1) proves this is at most one and at least `C_v^(-2)`. On rejection draw BOTH children afresh. On acceptance the output is exactly the parent's conditional field law. The leaf sampler is the one-site tilted-normal operation of Section 4, at the given phi. Positive onsite hopping at a leaf is included by replacing its r by `r exp(-beta T_ii)`.

For `C_v<=C=exp[2r beta b/(1-r)]`, the expected work obeys

`W(m)<=C^2[W(m_left)+W(m_right)+poly(m,L,precision)]`.

For balanced bisections this is polynomial, with fixed exponent at least `1+4r beta b/[(1-r)ln2]` and the local arithmetic degree. The exponent and constants can be impractical at low temperature or r near one. There is no assertion uniform as beta grows with M. A supplied tree, native positive cut decomposition, and all rejected branches are charged.

This is an exact-real conditional sampler, not a local Markov chain and not a count of passing finite instances. It remains valid when total `Tr T=Theta(M)`, where one whole-system rejection envelope would be exponentially poor.

## 7. Acquire the unknown common-phase normalizers

Write `Z_v(phi)=E_base g_phi(B_v)`. For every merge, its acceptance mean is

`mu_v(phi)=Z_v(phi)/[C_v Z_left(phi)Z_right(phi)] in [C^(-2),1]`.

This mean is acquired from independent child samples by an ordinary bounded-mean estimate. To obtain all parent logs at one phi to error eta, allocate relative error `O(eta/M)` and failure probability `delta/M` to every merge. Hoeffding uses `poly(M,1/eta,log(1/delta),C)` child samples; the conditional sampler in Section 6 pays each such sample. Sum the logs of all leaf normalizers, C_v, and acquired mu_v. No estimate is multiplied through an exponentially small acceptance event, and the number of precision bits is polynomial.

For all phi, `|d_phi log Z_root(phi)|<=ell=2Mr/(1-r)`. This follows by differentiating each positive determinant kernel and then averaging; no signed observable appears. Also `Z_root(phi)<=Z_root(0)`: its Fourier coefficient at difference n-m is the positive finite-slice physical trace in the UNEQUAL sector n,m, summed with positive fugacity powers. Absolute convergence justifies that rearrangement. These facts can pay a uniform phase envelope, but the following finite-grid construction is simpler.

Partition the phase circle into `Q=O(ell/epsilon)` bins. Estimate every positive midpoint normalizer to relative error `O(epsilon)`, with union failure probability delta. Sample a bin from these approximate positive weights, then choose phi uniformly within that bin. The derivative bound makes this phase density epsilon-close to the target: throughout a bin its log density varies by at most `ell pi/Q`. Finally call the exact conditional sampler at the ACTUAL chosen phi. Conditional sampling cannot increase the phase-marginal TV error.

The grid weights and within-bin phase are finite-precision operations with a stated output rounding. Normalizer acquisition has polynomial randomized cost, not an exact arithmetic oracle. Statistical failure, coefficient rounding and the total runtime cap each receive explicit error budget. This yields a polynomial approximate JOINT grand field/phase sampler and a relative grand balanced normalizer at every fixed r in the admitted bounded-cut class. The exactness claim applies only to the ideal conditional-phi recursion, not this finite estimated phase marginal.

## 8. Prescribed canonical counts: an honest remaining qualification

For joint field error delta, discard phi, compute `G_r(B)` and apply the canonical filter of Section 2. If the true prescribed count mass is at least b_K, taking `delta=O(epsilon b_K)` gives epsilon canonical output error; the expected production count is `O(1/b_K)`. Estimate b_K by independent bounded filter observations with a declared simultaneous confidence budget. A global production cap and explicit failure output prevent a rare bad estimate from creating an uncharged expected-runtime claim.

The theorem therefore gives a polynomial prescribed-K operation when a polynomial count floor is supplied AND ACQUIRED, or otherwise independently proved. It does NOT assume that every density can be reached efficiently. Phase coexistence or another count bottleneck is not removed by the conditional field sampler. The low-trace homogeneous class already pays this gate by Section 5; no general bounded-cut equivalence-of-ensembles theorem is being inferred from it.

## 9. A nonempty dense canonical family without a count oracle

One can nevertheless obtain some exact balanced canonical count proportional to M, reporting the selected count explicitly. Suppose `max_i T_ii<=d0`, a fixed constant. The same finite-slice Jensen proof and the equal-occupation configurations give, for every K,

`Z_(L,K)>=exp(-2 beta d0 K) Z_diag,K >=exp(-2 beta d0 K) D_K`.

Thus with `a=r^2 exp(-2 beta d0)>0`,

`Z_bal>=sum_K a^K D_K=(1-a)^(-M)=exp(lambda0 M)`.

On the other hand `Z_(L,K)<=D_K^2`, since both positive transfer factors are contractions. For a sufficiently small fixed c>0,

`sum_(K<=cM) r^(2K)Z_(L,K) <=(cM+1) exp[2M s(c)]`,

`s(c)=(1+c)ln(1+c)-c ln c`,

and choose `2s(c)<lambda0/2`. Its normalized low-count mass is exponentially small beyond a computable fixed M0. For any `r<r'<1`,

`sum_(K>=CM) r^(2K)Z_(L,K) <=(r/r')^(2CM)(1-r')^(-2M)`.

Choose fixed C large enough to make this exponentially small. Hence for all sufficiently large M, at least half the balanced grand mass lies in `cM<=K<=CM`. At least one of these O(M) counts has probability Omega(1/M).

This count is ACQUIRED using the bounded Rao--Blackwell probabilities

`w_n(B)=r^(2n)|h_n(B)|^2/G_r(B)`.

Their sum is one, every entry is in [0,1], and the same geometric tail controls n beyond O(M+log(1/epsilon)). Simultaneous absolute accuracy O(1/M) for O(M) candidate entries costs polynomially many independent grand samples. Select a large empirical entry, verify its lower confidence bound, and use INDEPENDENT production samples for its canonical filter. Accounting for the simultaneous failure budget avoids winner's-curse reasoning.

The selected K is an actual part of the output contract. This is not success on a previously prescribed K, and no density is silently changed. It establishes a nonempty fixed-density-SCALING canonical family for the extensive bounded-cut class, with actual positive physical weights and no occupation truncation. Finite exceptional sizes can be handled by their finite exact sectors or by retaining the explicit count-acquisition boundary.

The companion `OCCUPATION_INTERFACE.md` also gives a physical local-occupation tail and a Gibbs-variational cap-replacement theorem. A competent tensor/MPO comparator receives these inputs; they are not withheld to favor the field method.

## 10. Acquisition, precision and scope

For a contraction B, `|h_n(B)|<=D_n`. With any r'>r, the uniform tail

`sum_(n>J) r^(2n)|h_n(B)|^2 <=(r/r')^(2J)(1-r')^(-2M)`

pays all infinite number sums in O(M+log(1/eta)) retained terms. Alternatively a periodic analytic trapezoid pays G_r: on the strip `|Im phi|<=-ln(r)/2`, its analytic continuation is bounded by

`A_r^M`, `A_r=[(1-sqrt r)(1-r^(3/2))]^(-1)`.

Q equally spaced phases have absolute error at most `2 A_r^M exp[-Q|ln r|/2]/[1-exp(-Q|ln r|/2)]`. Thus Q=O(M+log(1/eta)) suffices at fixed r, without assuming the sampled phases avoid coincident poles. Since G>=1 this also controls relative denominator error. In the actual rational input, r<.71, `A_r<18<2^(17/4)` and `|ln r|/2>3/20`; Q=2094 gives uniform ideal absolute error below 2^-40 for M64.

Determinant log magnitudes are uniformly conditioned: `I-r exp(i phi)B` has singular values in `[1-r,1+r]`. Matrix exponentials, rational Hermitian/Gram bounds and determinant evaluation can therefore be acquired in polynomial bit work. Canonical h_K needs absolute, not relative, accuracy near its zeros. Bounds `|h_K|<=D_K` and the symmetric-power derivative `<=K D_K ||dB||` give O(M+log(1/epsilon)) precision bits at fixed density, rather than a free well-conditioned character evaluation.

For a fully finite-bit operation, couple truncated dyadic normal quantiles to the ideal normals; retain a tail budget over the explicit expected number of attempts. Round phase/hopping factors finely enough that the uniform log-determinant and absolute-character errors change all Bernoulli decisions by at most the allocated total error. Use a single total work cap at the known expected bound divided by its failure budget. Output a specified rounded history law; a discrete output is not asserted TV-close to a continuous distribution on unrounded reals. Section 8's canonical conditioning spends the extra factor 1/b_K. These are specified polynomial precision/cost routes, not claims that the binary64 run implements them.

All statements so far concern the EXACT finite-slice physical law Z_(L,K). The previously frozen bounded-sector Strang/principal-log theorem supplies, with `R=||T_many||+||V||`,

`|log Z_(L,K)-log Z_Gibbs,K|<=128 beta^3 R^3/L^2`, for `L>=8 beta R`.

Here `||T_many||<=2K||T||` and `||V||<=2K^2 max U_i`; the sufficient L is polynomial at fixed density and requested log-partition tolerance. The determinant and recursive rejection bounds do not worsen with L, although generating and propagating all L phases costs polynomially more. The actual L16 receipt does NOT satisfy a useful all-model continuum tolerance merely because this existence/cost theorem is available.

Bounded partition predictions are acquired from positive bounded filter means and the acquired grand normalizer. Thermodynamic derivatives can be queried by finite changes in the declared Hamiltonian, with canonical norm-controlled finite-difference bias and the corresponding increased statistical precision charged. Arbitrary AFQMC ratio estimators near character zeros are not assumed bounded. Physical devices, material phases, native measured advantage, generic extensive-dimensional graphs, a useful low-temperature polynomial exponent, and historical novelty remain unestablished.
