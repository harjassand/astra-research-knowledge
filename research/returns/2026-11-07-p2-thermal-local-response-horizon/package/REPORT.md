# A finite-temperature information horizon for local spin response

Date: 2026-11-07.

## 1. Question selected and result

The selected question is: **How much noisy scalar imaginary-time information is sufficient, and necessary, to predict a local real-time thermal response over a growing time horizon—even for explicitly realizable nearest-neighbor spin chains?**

This deliberately changes the access contract from the unresolved microscopic-input nucleation problem. The predictor receives scalar correlation observations from an unknown source, together with its declared structural class. It does not receive the source's Hamiltonian coefficients. The lower-bound constructor does produce complete finite microscopic descriptions; the learner is not told which of two possible descriptions is present. Supplying that identity or the actual coefficients changes the problem.

The result is a matching information law at fixed temperature, bandwidth, accuracy, and confidence. In units with inverse temperature \(\beta=1\), one-particle bandwidth parameter \(\Omega=1\), and Gaussian readout variance \(v=1\), let \(M_*(T)\) denote the smallest worst-case number of scalar readings needed to return a finite response record with

\[
\Pr\left\{\sup_{0\le t\le T}|\widehat R(t)-R(t)|\le1/64\right\}\ge2/3.
\]

The source class consists of open nearest-neighbor XY chains with explicitly counted \(N\le\lceil T\rceil+1\) sites, a positive one-particle matrix with spectrum in \([1/2,1]\), and the known observable \(A=X_1\). Site-dependent coefficients are allowed. The learner may additionally know the entire one-particle spectrum. Each raw query at a chosen \(\tau\in[0,1]\) returns the thermal scalar correlator plus an independent unit-variance Gaussian. Private randomness and adaptive query choices are permitted, with a fixed worst-case query budget.

For sufficiently large \(T\),

\[
\boxed{\log(1+M_*(T))=\Theta\!\bigl(T\log(2+T)\bigr).}
\tag{1}
\]

The upper bound applies to every normalized positive transition measure in the declared band. The lower bound already holds for a pair of local, gapped, explicitly encoded free-fermion chains. The pair has the same complete many-body spectrum and the same partition function at every temperature. Every mode has endpoint spectral weight at least \(1/(4N)\), and every hopping has an inverse-polynomial lower bound.

The equivalent fixed-accuracy horizon for a budget \(M\) is

\[
T_*(M)=\Theta\!\left(\frac{\log M}{\log\log M}\right).
\tag{2}
\]

This is a worst-case law for the specified observation channel. It is not a claim that every system saturates it, that all Monte Carlo observations have this noise law, or that the Hamiltonians are hard to simulate when supplied explicitly.

### What is inherited and what is constructed here

Astra N724 already develops a scalar zero-temperature growing-time horizon, an isospectral Jacobi realization, a coupling-floor argument, and a matching reconstruction at its return-probability contract. Those ideas are credited, not presented again as a new zero-temperature discovery.

Astra N1725 already proves the normalized fixed-temperature scalar obstruction. Its bounded-total-norm qubit realization contains an interaction acting on all qubits; its source explicitly does not establish fixed-body geometric locality. Its target and access contract also do not automatically import N724's upper bound.

The central operation here is a **thermal change of spectral weights followed by finite inverse Jacobi construction**. It realizes the thermal obstruction with two-body nearest-neighbor interactions and a one-site observable, preserves exact isospectrality under a finite algebraic encoding, and supports a separately proved matching upper bound for the thermal response itself. Inverse Jacobi theory, Jordan–Wigner/free-fermion reduction, engineered XY chains, finite differences, interpolation, Gaussian testing, and concentration are classical machinery. No historical-priority claim is made.

## 2. Microscopic source and exact thermal formula

Let \(J\) be a real symmetric \(N\times N\) Jacobi matrix with diagonal \(d_i\), positive neighboring entries \(b_i\), and spectrum in \([\Omega/2,\Omega]\). Define the open spin chain

\[
H=\sum_{i=1}^N d_i\frac{I-Z_i}{2}
  +\frac12\sum_{i=1}^{N-1}b_i(X_iX_{i+1}+Y_iY_{i+1}).
\tag{3}
\]

The observable is \(A=X_1\), with \(A^2=I\) and norm one. Open-chain Jordan–Wigner transformation gives

\[
H=\sum_{i,j}J_{ij}c_i^\dagger c_j,\qquad A=c_1+c_1^\dagger.
\]

If \(\nu=\sum_j\nu_j\delta_{\omega_j}\) is the endpoint spectral measure of \(J\), then \(\nu_j>0\), \(\sum_j\nu_j=1\), and

\[
C_\nu(z)
=\frac{\operatorname{Tr}(e^{-(\beta-z)H}A e^{-zH}A)}
       {\operatorname{Tr}e^{-\beta H}}
=\sum_j\nu_j
 \frac{e^{-z\omega_j}+e^{-(\beta-z)\omega_j}}
      {1+e^{-\beta\omega_j}}.
\tag{4}
\]

To obtain this identity, diagonalize \(J\), expand \(c_1\) in the normal modes, and use their independent Fermi occupations. Only one mode changes occupation under each term of \(A\). All other modes cancel from the normalized trace. Thus (4) is the actual canonical Gibbs correlator of (3), not a separately postulated spectral oracle.

The real-time output is

\[
R_\nu(t)=-\operatorname{Im}C_\nu(it)
=\sum_j\nu_j\tanh(\beta\omega_j/2)\sin(t\omega_j)
=\frac{i}{2}\langle[A(t),A]\rangle_\beta.
\tag{5}
\]

This fixes the sign and normalization. A conventional linear-response convention may include an overall sign or factor two; the output here is exactly (5).

The many-body ground state is the unique fermion vacuum. Its gap is at least \(\Omega/2\). The full energy spread is at most \(N\Omega\), not a size-independent constant. The strict transition-band promise is earned for this observable and this quadratic model. Bounded local interactions alone would not establish the same strict transition cutoff for arbitrary interacting Hamiltonians.

## 3. The central thermal realization operation

Suppose \(\mu\) is any probability measure on positive frequencies. Set

\[
W_\mu=1+\int e^{-\beta\omega}\,d\mu(\omega),\qquad
d\nu(\omega)=\frac{1+e^{-\beta\omega}}{W_\mu}\,d\mu(\omega).
\tag{6}
\]

Then substituting (6) into (4) gives

\[
C_\nu(\tau)
=\frac{C_\mu(\tau)+C_\mu(\beta-\tau)}
       {1+C_\mu(\beta)},\qquad
C_\mu(s)=\int e^{-s\omega}\,d\mu(\omega).
\tag{7}
\]

Likewise,

\[
R_\nu(t)
=\frac{\int(1-e^{-\beta\omega})\sin(t\omega)\,d\mu(\omega)}
       {1+C_\mu(\beta)}.
\tag{8}
\]

For finitely many distinct atoms, orthogonalizing the monomials for \(\nu\) constructs a Jacobi matrix with precisely that endpoint measure. Formula (3) then realizes (7) and (8) with nearest-neighbor interactions. The thermal factor in (6) is necessary: constructing the Jacobi matrix directly from \(\mu\) generally gives a different thermal normalization.

This operation also separates thermodynamics from local response. For fixed frequencies, varying their endpoint weights changes the Jacobi coefficients but leaves its eigenvalues unchanged. The many-body spectrum is the multiset of all subset sums of those frequencies, and

\[
Z(\beta')=\prod_{j=1}^N(1+e^{-\beta'\omega_j})
\tag{9}
\]

for every inverse temperature \(\beta'>0\). The common frequency list and subset-sum/product formulas describe this information compactly; no exponentially long list of many-body energies is required.

## 4. Positive, isospectral local pairs

Let \(n\ge1\) be odd and \(N=n+1\). Define

\[
h=\frac{2\Omega}{4n+1},\quad
\omega_j=\frac{\Omega(2n+1+2j)}{4n+1},\quad
w_j=2^{-n}\binom nj,\quad
u_j=\frac1{n+1}.
\]

All frequencies lie in \((\Omega/2,\Omega]\), separated by \(h\). Put

\[
\mu^\pm_j=\frac{u_j}{2}
            +\frac{w_j}{2}\bigl(1\pm(-1)^j\bigr).
\tag{10}
\]

Both are probability measures on exactly the same atoms. Every weight is at least \(1/(2N)\). Their difference is the signed binomial measure

\[
\mu^+_j-\mu^-_j=(-1)^j w_j.
\]

This positive common background is adapted from the prior finite-difference construction. Its purpose is to exclude reliance on exponentially small endpoint overlaps.

### Uniformly small imaginary-time difference

Write

\[
D(s)=\sum_j(-1)^jw_j e^{-s\omega_j}
=2^{-n}e^{-(n+1/2)hs}(1-e^{-hs})^n\ge0.
\tag{11}
\]

Let \(C_\pm\) denote the Laplace transforms of \(\mu^\pm\), \(W_\pm=1+C_\pm(\beta)\), and apply (6). Define

\[
d_n=\left(\frac{\beta\Omega}{4n+1}\right)^n.
\tag{12}
\]

For \(\tau\in[0,\beta]\),

\[
0\le D(\tau)+D(\beta-\tau)
\le2^{-n}h^n\{\tau^n+(\beta-\tau)^n\}\le d_n,
\]

and \(0\le D(\beta)\le d_n\). Each normalized correlator is between zero and one. The exact normalization identity is

\[
C_{\nu^+}(\tau)-C_{\nu^-}(\tau)
=\frac{D(\tau)+D(\beta-\tau)-C_{\nu^-}(\tau)D(\beta)}
       {W_+}.
\]

Both terms subtracted in its numerator lie in \([0,d_n]\), and \(W_+\ge1\). Consequently,

\[
\boxed{\sup_{0\le\tau\le\beta}|C_{\nu^+}(\tau)-C_{\nu^-}(\tau)|\le d_n.}
\tag{13}
\]

This holds for the entire allowed continuum of query times.

### Constant late-time response difference

At \(T_n=\pi/h\), \(\sin(\omega_jT_n)=(-1)^{n+j}\). Let \(C_w,C_u\) be the Laplace transforms of \(w,u\), and put

\[
C_0=(C_u(\beta)+C_w(\beta))/2,\quad W_0=1+C_0,\quad
B=1-C_w(\beta).
\]

Since \(n\) is odd, the uniform measure has zero alternating sum and

\[
D_u(\beta)=\sum_j(-1)^ju_j e^{-\beta\omega_j}
=\frac{e^{-(n+1/2)h\beta}
       (1-e^{-(n+1)h\beta})}{N(1+e^{-h\beta})}>0.
\]

Let \(A_0=-(D_u(\beta)+D(\beta))/2\le0\). Removing a common sign, the two responses are

\[
\frac{A_0+B/2}{W_0+D(\beta)/2},
\qquad
\frac{A_0-B/2}{W_0-D(\beta)/2}.
\]

Their difference has magnitude

\[
\frac{B W_0-A_0D(\beta)}
     {W_0^2-D(\beta)^2/4}
\ge\frac B{W_0}
\ge\tanh(\beta\Omega/4).
\tag{14}
\]

The final step uses \(C_w(\beta),C_0\le e^{-\beta\Omega/2}\).

### Nonvanishing local couplings

After the thermal tilt, every endpoint weight is at least \(1/(4N)\). The elementary inverse-Jacobi coupling lemma used in N724 states: with eigenvalue spacing at least \(h\) and endpoint weights at least \(\alpha\), each neighboring coupling satisfies \(b_i\ge h\sqrt\alpha/3\).

For clarity, its mechanism is short. Split the matrix at a bond. The left block has fewer eigenvalues than the whole matrix, so some full eigenvalue is at distance at least \(h/3\) from that block's spectrum. Its eigenvector equation bounds the left component by \(3b_i/h\), whereas its endpoint component has magnitude at least \(\sqrt\alpha\).

Thus the present pair satisfies

\[
\boxed{\frac{h}{6\sqrt N}\le b_i\le\frac{\Omega}{4},\qquad
       \frac\Omega2<d_i\le\Omega.}
\tag{15}
\]

The upper hopping bound follows by subtracting the midpoint of the spectral interval and bounding an off-diagonal entry by the operator norm. Locality, a many-body ground-state gap, a common full spectrum, polynomially bounded inverse hoppings, and polynomially bounded inverse endpoint weights therefore coexist with (13)–(14).

## 5. Exact finite encoding and construction cost

The ideal tilt contains exponentials. Treating them as costless exact input numbers would leave a representation gap. The following finite construction closes it while preserving exact isospectrality.

Use the rational lower bound

\[
\gamma_0=\frac{\beta\Omega}{4+\beta\Omega}
\le\tanh(\beta\Omega/4),
\qquad
\xi=\min\{d_n/64,\gamma_0/64,1/32\}.
\]

Choose \(p=\lceil\log_2(1/\xi)\rceil\). Compute dyadics \(r_j\in[0,1]\) with

\[
|r_j-e^{-\beta\omega_j}|\le2^{-p}\le\xi.
\]

This is a finite operation: range-reduce the exponent to \([0,1]\), bound its alternating Taylor series, and square with outward dyadic rounding. The supplied implementation uses only exact integer/rational arithmetic. The number of arithmetic steps and their bit lengths are polynomial in \(p\) and the binary exponent description.

Replace the ideal weights by exact rationals

\[
q^\pm_j=\frac{\mu^\pm_j(1+r_j)}
               {\sum_\ell\mu^\pm_\ell(1+r_\ell)}.
\tag{16}
\]

They satisfy

\[
\|q^\pm-\nu^\pm\|_1\le2\xi,\qquad q^\pm_j\ge\frac1{4N}.
\tag{17}
\]

For the first inequality, subtract the normalized vectors; the unnormalized total error and the normalizer error are each at most \(\xi\), and the approximate normalizer is at least one.

Construct the Jacobi matrices from the exact atoms and exact rational weights (16). In the monic recurrence,

\[
P_{k+1}(x)=(x-d_k)P_k(x)-b_k^2P_{k-1}(x),
\]

\[
d_k=\frac{\langle xP_k,P_k\rangle_q}{\langle P_k,P_k\rangle_q},
\qquad
b_k^2=\frac{\langle P_k,P_k\rangle_q}{\langle P_{k-1},P_{k-1}\rangle_q}.
\tag{18}
\]

All \(d_k\) and \(b_k^2\) are rational. The microscopic format explicitly stores \(d_k\) and the positive square root of rational \(b_k^2\). Each local coefficient has an ordinary finite algebraic description; it is not a free real-number oracle. Both matrices still have exactly the supplied rational eigenvalues. Hence the complete many-body spectra and all partition functions remain exactly equal.

The exact encoded pair obeys

\[
\sup_\tau|C_+(\tau)-C_-(\tau)|
\le d_n+4\xi\le\frac{17}{16}d_n<2d_n,
\tag{19}
\]

and its response separation at \(T_n\) is at least \(15\gamma_0/16\).

No irrational query-time input is needed. Certified Machin-formula bounds for \(\pi\) produce a dyadic \(t_n\) with

\[
|t_n-T_n|\le\frac{\gamma_0}{16\Omega}.
\]

Because \(|R'(t)|\le\Omega\), the exact encoded pair at this binary query time satisfies

\[
\boxed{|R_+(t_n)-R_-(t_n)|\ge\gamma_0/2.}
\tag{20}
\]

At fixed \(\beta,\Omega\), \(p=O(n\log n)\), and \(t_n\) needs \(O(\log n)\) bits.

### Bit bounds

For \(\Omega=1\), the atom denominator is \(D=4n+1\). The weights in (16) have a common integer denominator with
\(P\le n+p+\lceil\log_2 N\rceil+4\) bits. Moments through degree \(2N\) have a common denominator with at most
\[
L=P+2N\lceil\log_2 D\rceil+2
\]
bits. The associated integer Gram matrices have entries of at most \(L\) bits. Hadamard's determinant bound and Cramer's rule bound the numerators and denominators of their monic polynomial coefficients and norm ratios by
\[
O\bigl(N(L+\log N)\bigr)
\]
bits. Positivity guarantees the required determinants are nonzero; no exponentially costly precision search is used.

The value-form recurrence in the implementation uses \(O(N^2)\) exact rational operations. Its intermediate values and partially accumulated norms have the same polynomial bit bounds, since the polynomial coefficients have a common determinant denominator. A conservative schoolbook bound for the complete constructor, including elementary-function enclosures, is
\[
O\bigl((n+p+B+2)^{12}\bigr)
\]
bit operations, where \(B\) is the binary length of rational \(\beta,\Omega\). The exponent is deliberately loose. For fixed parameters the resulting local Hamiltonian description has \(O(n^3\log n)\) bits. Square-root coefficients can be evaluated to \(b\) additional bits by integer square-root bounds in polynomial work.

This is a polynomial construction of counterexample sources. It does not convert the learner's restricted scalar data into their coefficient descriptions.

### Setting precision and robustness

Exact algebraic models do not imply cheap laboratory realization. With the observable fixed, a Hamiltonian perturbation \(V\) obeys
\[
\sup_{0\le\tau\le\beta}|C_{H+V}(\tau)-C_H(\tau)|
\le2\beta\|V\|,
\]
\[
|R_{H+V}(t)-R_H(t)|\le2(\beta+|t|)\|V\|.
\tag{21}
\]

The first bound follows by differentiating the Gibbs trace and applying Schatten Hölder to the inserted perturbation; all imaginary-time factors have nonnegative lengths summing to \(\beta\). Normalization adds a second term of the same bound. The second combines the Gibbs-state trace-norm bound with real-time Duhamel.

If every onsite and hopping coefficient is set with error at most \(r\), then \(\|V\|\le(2N-1)r\). Preserving the tiny Euclidean ambiguity therefore requires \(r=O(d_n/N)\) at fixed temperature; preserving only the late-time response gap requires much less precision. This is \(O(n\log n)\) coefficient-fidelity digits, not inexpensive physical setting or acquisition. Independent perturbations generally destroy the exact common spectrum; exact thermodynamic side information is asserted for the exact encoded pair.

The archive also retains a binomial-background variant valid at every \(n\). It has the stronger floor \(b_i\ge\Omega/(15\sqrt n)\), obtained by comparison with the Krawtchouk recurrence, but does not have the uniform-background variant's polynomial floor for every endpoint weight. The main theorem uses the uniform-background pair.

## 6. Lower bound for every estimator using this channel

Give the learner the two explicit possible models, their common spectrum, and their common partition-function formula if desired. Only the identity of the source remains unknown.

At any chosen \(\tau\), the means of the Gaussian observations differ by at most \(2d_n\). The chain rule for relative entropy, including adaptive queries and private random seeds, gives for an algorithm with at most \(M\) readings

\[
D_{\rm KL}(\mathsf P_+\Vert\mathsf P_-)
\le\frac{M(2d_n)^2}{2v}.
\tag{22}
\]

At a common transcript, the algorithm's next query is the same under both hypotheses; therefore the uniform all-\(\tau\) bound applies conditionally. Subsequent computation cannot increase this information.

If the algorithm estimates \(R(t_n)\) to error smaller than half the gap in (20), with failure probability at most \(\alpha<1/2\) for each source, its output gives a binary test. Pinsker's inequality yields

\[
\boxed{M\ge\frac{v(1-2\alpha)^2}{d_n^2}.}
\tag{23}
\]

The confidence-sensitive binary relative-entropy bound also gives
\[
M\ge
\frac{v}{2d_n^2}(1-2\alpha)
\log\frac{1-\alpha}{\alpha}.
\tag{24}
\]

At \(v=1,\alpha=1/3\),
\[
\boxed{M\ge\frac19
\left(\frac{4n+1}{\beta\Omega}\right)^{2n}.}
\tag{25}
\]

For deterministic readings with adversarial absolute error at least \(d_n\), the midpoint of the two exact correlators is compatible with either source at every query. No number of such readings can guarantee a response interval shorter than the gap in (20).

Quantizing or clipping the Gaussian observations does not weaken the lower bound, by data processing. Exact partition functions are uninformative for this pair because they are identical. Other observables, response measurements at additional temperatures, energy labels, correlated vector data, or source coefficients are different access contracts.

For a horizon \(T\), choose an odd \(n=\Theta(\Omega T)\) with \(t_n\le T\). For example, at \(\Omega=1\) the largest positive odd \(n\le T/8-1\) works for all sufficiently large \(T\), using \(\pi<4\). Then \(N\le\lceil T\rceil+1\), and (25) proves the lower half of (1).

## 7. Matching constructive upper bound

This argument predicts the response directly. It does not first recover a spectral density.

For every positive probability measure in the stated band, the correlator (4) is entire. For every integer \(k\ge0\) and \(0\le\operatorname{Re}z\le\beta\),

\[
|C^{(k)}(z)|\le\Omega^k.
\tag{26}
\]

Indeed the numerator is bounded in modulus by
\(\omega^k(e^{-s\omega}+e^{-(\beta-s)\omega})\), with \(s=\operatorname{Re}z\), and
\[
e^{-s\omega}+e^{-(\beta-s)\omega}\le1+e^{-\beta\omega}.
\]

Choose \(m+1\) rational nodes \(\tau_j=j\beta/m\), \(j=0,\ldots,m\), with \(m\ge1\). Let \(P_m\) interpolate the exact node values. The complex divided-difference integral formula, applied within the convex hull of these nodes and \(it\), gives

\[
\sup_{0\le t\le T}|C(it)-P_m(it)|
\le\frac{[\Omega(\beta+T)]^{m+1}}{(m+1)!}
=:E_m.
\tag{27}
\]

The entire convex hull lies in the strip used in (26). The simplex integral has volume \(1/(m+1)!\), and each interpolation distance is at most \(\beta+T\).

The absolute sum of the Lagrange evaluation coefficients is bounded by

\[
A_m=\frac{[2m(\beta+T)/\beta]^m}{m!}
\le[6(1+T/\beta)]^m.
\tag{28}
\]

For the first bound, the denominator of the \(j\)th basis polynomial is
\((\beta/m)^m j!(m-j)!\); sum their reciprocals and use the binomial theorem.

Thus if each supplied node estimate has error at most \(\eta\),

\[
\boxed{\sup_{0\le t\le T}
|\widehat R(t)-R(t)|\le E_m+A_m\eta,}
\tag{29}
\]

where \(\widehat R(t)=-\operatorname{Im}\widehat P_m(it)\).

Choose \(m\) by exact rational comparisons until \(E_m\le\epsilon/4\), and set
\[
\eta=\frac{\epsilon}{4A_m}.
\tag{30}
\]

One may take
\[
m+1\ge6\Omega(\beta+T)+\lceil\log_2(4/\epsilon)\rceil+2,
\]
so \(m=O(\Omega(\beta+T)+\log(1/\epsilon))\). The implementation chooses the first adequate degree after \(m=1\), which is often smaller.

### Acquisition, quantization, calibration, and confidence

Use
\[
r=\left\lceil8v\eta^{-2}
\left\lceil\log_2\frac{4(m+1)}{\alpha}\right\rceil\right\rceil
\tag{31}
\]
raw readings per node, with at least one reading. Gaussian tail bounds and a union bound make all unquantized sample-mean errors at most \(\eta/2\) except on an event of probability at most \(\alpha/2\).

Allow at most \(\eta/4\) readout quantization error and at most \(\eta/(4\Omega)\) setting error, with actual settings in \([0,\beta]\). The derivative bound makes the setting contribution at most \(\eta/4\). Together these fit the node-error allowance in (29).

The displayed schedule assumes the declared inverse temperature is the actual one. If inverse-temperature calibration is also imperfect, the kernel obeys \(|\partial_\beta C|\le\Omega\) at fixed \(\tau\) in the common thermal interval. The same systematic-error allocation is valid when \(\Omega(|\Delta\tau|+|\Delta\beta|)\le\eta/4\). Establishing either calibration bound physically remains a paid acquisition condition.

To make the reading representation finite even for unbounded Gaussian tails, let \(M=(m+1)r\), choose
\[
L_c=\left\lceil\log_2\frac{4M}{\alpha}\right\rceil,
\qquad
K=2+\left\lfloor\sqrt{\lceil2vL_c\rceil}\right\rfloor,
\]
and clip to \([-K,K]\). Since the exact correlator lies in \([0,1]\), the probability that any reading is clipped is at most \(\alpha/2\). On the complementary event, clipping adds no error. Round the reading to a dyadic grid with spacing at most \(\eta/4\). Combining the two failure allowances proves the advertised confidence.

Every acquired reading is charged. The number of settings is \(m+1\), and the total raw reading count is
\[
M=(m+1)r
=O\!\left((m+1)vA_m^2\epsilon^{-2}
\log\frac{m+1}{\alpha}+(m+1)\right).
\tag{32}
\]

Each reading has
\[
O\bigl(\log(1/\eta)+\log(K+1)\bigr)
\]
bits. Summing \(r\) dyadics adds \(\log r\) accumulator bits. Interpolation and later evaluation use exact rational arithmetic or outward rounding at explicitly bounded precision.

The output is a finite polynomial in \(t\), of degree at most \(m\), together with the uniform error certificate (29). Its coefficient bit lengths and evaluation work are polynomial in \(m\), the input/record bit lengths, and the binary length of a requested \(t\le T\). Total digital work includes processing all \(M\) readings; preprocessing and interpolation do not hide that cost.

At fixed \(\beta,\Omega,v,\epsilon,\alpha\),
\[
\log M=O(T\log(2+T/\beta)).
\tag{33}
\]

This proves the matching upper half of (1). The dependence claimed to be sharp is the growing-time exponential order at fixed accuracy and confidence; a sharp joint minimax law in all parameters is not claimed.

The finite program includes a schedule generator, exact rational record compiler, evaluator, and a routine that consumes the full charged finite stream. The enormous theoretical Gaussian budgets were not executed. A Gaussian oracle is a stated observation model, not an acquired experimental instrument. State preparation, decorrelation, acquisition latency, and physically achieving the required setting/readout precision add their actual costs. Even though the precision digit count is polynomial in the numerical horizon, the horizon can itself be exponential in its binary description length.

## 8. Consequences and boundaries

**Exact thermodynamics can be insufficient for local dynamics.** The two local sources have identical spectra, gaps, all partition functions, and derived global thermodynamic functions. Their local dynamical response differs by a constant. The missing information is in observable-dependent spectral weights.

**Locality and favorable static spectral properties do not automatically repair the scalar data channel.** The lower bound survives geometric nearest-neighbor locality, a uniform ground-state gap, a fixed transition band, inverse-polynomial hoppings, and inverse-polynomial endpoint weights. Its microscopic descriptions are finite and constructible.

**The obstruction is independent of the reconstruction algorithm.** Positivity, adaptive imaginary-time placement, nonlinear reconstruction, statistical learning, and unlimited subsequent computation cannot distinguish the supplied pair with substantially fewer observations under this noise model. A warranted prior can help if it excludes the alternatives; the prior is then substantive additional information.

**Precision and acquisition are different resources.** Required numerical digits scale as \(T\log T\); producing those digits by independent constant-variance readings takes \(\exp(\Theta(T\log T))\) observations. Compact output and polynomial-precision arithmetic do not make that acquisition inexpensive.

**Complete microscopic source access changes the answer.** For the explicit quadratic chains, \(R(t)=[\tanh(\beta J/2)\sin(tJ)]_{11}\). Given \(J\), finite matrix algorithms evaluate this in polynomial work in \(N\), coefficient precision, requested output precision, and binary time length at fixed band/temperature. Scaling and squaring uses \(O(\log(1+t\Omega))\) stages and correspondingly increased arithmetic precision. No many-body Hilbert-space enumeration is required. The present lower bound therefore cannot be used as a full-Hamiltonian computational-hardness theorem or a quantum-advantage claim.

**This is a designed worst-case family.** The source changes as the horizon grows. Arbitrary fixed systems need not remain hard indefinitely, and uncontrolled microscopic errors may remove the carefully canceled Euclidean difference. The required setting precision is quantified in (21).

**Physical and other scientific endpoints remain distinct.** The full two-dimensional finite-temperature nucleation predictor remains unresolved, as does unrestricted polynomial-bit exact QUBO. The new theorem supplies neither of those algorithms nor a lower bound against all possible approaches to them. No statement here concerns P=NP.

## 9. Executed checks and delivered operation

The implementation executed 1,892 exact rational assertions across thirteen finite pair constructions, including both background choices and non-unit temperature/bandwidth cases. The checks include:

- exact characteristic polynomials equal to the common product over the specified atoms;
- endpoint moments from a rational matrix similar to each Jacobi matrix;
- positive weights, applicable weight/coupling floors, and spectral bounds;
- rational exponential enclosures and the binary target-time certificate;
- certified late-time gap bounds and nine-point interval checks of the all-time inequality;
- exact interpolation and 303 rational-interval response checks using synthetic bounded-error records.

The universal all-time and complexity statements follow from the proofs above, not from these finite tests.

Four independent full-spin matrix diagnostics, up to Hilbert dimension 32, check the Gibbs trace, real-time response, and common many-body spectra using floating arithmetic. Their largest absolute discrepancy was \(2.67\times10^{-15}\). They are explicitly labeled diagnostics, not interval proofs.

Illustrative uniform-background cases at \(\beta=\Omega=v=1\), confidence \(2/3\):

| Sites | Binary query time, shown in decimal | Certified response gap, rounded down | Gaussian raw-reading lower bound |
|---:|---:|---:|---:|
| 4 | 20.419921875 | 0.361 | \(>5.36\times10^5\) |
| 8 | 45.552734375 | 0.358 | \(>3.30\times10^{19}\) |
| 16 | 95.818359375 | 0.358 | \(>4.03\times10^{52}\) |

These are dimensionless model times and specified-channel lower bounds. No physical data or astronomical reading budget was acquired.

The core module uses the Python standard library. The optional full-spin diagnostics use the already available NumPy package. An initially attempted optional mpmath diagnostic was unavailable; it was replaced with exact rational sine/exponential interval checks, without installing dependencies. This changed no theorem.

## 10. Sources and credits

1. Astra N724, “Scalar imaginary-time information horizon,” governing original at commit d490a9d4429a8152902cebb32fd67c1e4c9285b2: [original source](https://github.com/harjassand/astra-research-knowledge/blob/d490a9d4429a8152902cebb32fd67c1e4c9285b2/updates/EH/package/genesis_scalar_horizon/ORIGINAL_PASTED_SOURCE.txt). Source SHA-256: 712b239d261bbf1576e8115a167394ea1c59c9d2db739032fef356de7400b23d.
2. Astra N1725, “Fixed-temperature obstruction at growing real time and fixed transition bandwidth,” same pinned repository: [governing fixed-temperature proof](https://github.com/harjassand/astra-research-knowledge/blob/d490a9d4429a8152902cebb32fd67c1e4c9285b2/research/2026-11-04-quartic-fibers-and-scoped-response-proofs/source/substantive/Euclidean_Response_Fixed_Temperature_Proof.md). Source SHA-256: 0650016822c9d418e55efea89edebbc38abea9165551378e5f4f8692f3fc5c52.
3. Fritz Gesztesy and Barry Simon, “m-Functions and inverse spectral analysis for finite and semi-infinite Jacobi matrices,” Journal d'Analyse Mathématique 73 (1997), 267–297. [Primary author record](https://authors.library.caltech.edu/records/zvw7k-jcq35), DOI 10.1007/BF02788147. Classical inverse spectral context.
4. R. Chakrabarti and J. Van der Jeugt, “Quantum communication through a spin chain with interaction determined by a Jacobi matrix,” [arXiv:0912.0837](https://arxiv.org/abs/0912.0837). Primary derivation of the XY/Jacobi relationship and Krawtchouk-chain formulas.
5. M. Christandl, N. Datta, A. Ekert, and A. J. Landahl, “Perfect state transfer in quantum spin networks,” Physical Review Letters 92, 187902 (2004), [arXiv:quant-ph/0309131](https://arxiv.org/abs/quant-ph/0309131). Engineered nearest-neighbor spin-chain precedent.

The governing Astra originals were read through the approved public repository tool. No held original attachment or live peer construction was used. There was no peer contact, new worker, infrastructure, physical experiment, spend, or outreach. Earlier archives are retained byte for byte; their scientific scopes and unresolved questions are not enlarged by this result.
