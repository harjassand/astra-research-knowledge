# Independent adversarial proof review

Date: 15 October 2026. Reviewer: adversarial_proof_review.

This is an independent reconstruction within the same research team. It is not external mathematical certification, a formal proof, or a historical-priority determination. No worker's agreement, checker receipt, or model report is used as a proof premise. The source repository and other workers' files were read without modification.

Repository pin checked directly: `00631610750c708263d5cf6d812ebbb8edc77335` at `/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange`.

## Findings at this checkpoint

1. The routing factorization and information identities reconstruct. Two qualifications were missing from the initial routing theorem: the necessity witness requires both register dimensions at least two, and its covariance averaging requires routing randomness independent of the input modules. The root researcher has incorporated both qualifications and preserved the initial draft. The current theorem has no further decisive gap identified here.
2. The finite-jet order-reduction proof, its determinant-affine support characterization, and its all-background polyconvexity equivalence reconstruct under the stated hypotheses. In particular, the high-frequency limit and subtraction of total derivatives are justified; there is no hidden growth assumption on the integrand.
3. The universal coefficient-linear nonlocal-selection obstruction reconstructs. Arbitrary profile functionals can be averaged because domination itself implies Lipschitz continuity on each smooth translation orbit. The cone-only linear extension is well defined. Degenerate boundary energies can legitimately be used even if initial domination is imposed only in the acoustic interior.
4. The fixed-copy quantum polynomial obstruction reconstructs, including nonconstant heralding success probability. Its final report's finite-error paragraph needed an explicit deterministic-output restriction. The worker preserved its frozen report and added `SCOPED_CORRECTION.md`; that correction is part of the reviewed result.
5. The strong critical-trace action-storage proof reconstructs under the independently supplied strict quasiconvexity premise. Its duration-independent coercivity is sufficient for the claimed local Lipschitz modulus. The proof explicitly allows Sobolev strips, moving means, arbitrary widths, and rough critical traces.
6. The continuous scalar-label adjacent-pairing bias bound reconstructs for expected local task scores under a supplied uniform channel Lipschitz certificate. All donor labels retain their population weight. This does not produce globally independent outputs or acquire the Lipschitz certificate.

No full-cone rank-one-convexity-to-quasiconvexity theorem, negative compatible closed cycle, or physical implementation follows from these findings.

## 1. Routing: exact correction and reconstruction

Files reviewed: `ROUTING_CORRELATION_THEOREM_v0001.txt` (initial authored statement) and `ROUTING_CORRELATION_THEOREM.md` (corrected statement).

### 1.1 Two scope corrections

The initial statement at lines 60–63 omitted a nontrivial-dimension hypothesis. If `dim E=1`, then every joint state is already a product and retaining all `k=N` inputs satisfies the intended target. The same counterexample applies when `dim X=1`. The fair-bit witness requires two distinguishable values in each register. The repaired current statement includes `dim X>=2, dim E>=2` at lines 60–65.

The initial randomized-routing wording used a parameter-independent route distribution. A parameter-independent marginal distribution is insufficient to infer that the conditional input bits remain iid fair after the route is fixed: a route may be selected from measured input data. The displayed covariance averaging argument requires routing selected independently of the prepared modules. The current statement makes this explicit at lines 62–64. This is a correction to the covariance proof's hypotheses; the separately reconstructed arbitrary-instrument polynomial argument supplies a broader exact-output lower bound.

These corrections were sent to the root researcher before the current version was read. No edits were made by this reviewer.

### 1.2 Tensor factorization and entropy

For a fixed route, define `D=pi(T)` and `m=|D intersect T|`. Each original iid factor contributes its complete `XE` state, only `X`, only `E`, or neither, depending on membership in `D` and `T`. Partial trace of a tensor product therefore gives the retained factorization at current lines 23–27. The reference `R` is included in logical `X`; this conclusion depends on the explicitly stated logical donor-reference bookkeeping and joint exchange premise.

There are `m` whole factors and `k-m` factors of each marginal. Consequently

    S(retained)=m S(XE)+(k-m)(S(X)+S(E)),
    I(X_D:E_T)=m I(X:E).

For a derangement every retained site's marginal is `rho_X tensor rho_E`, so summing site entropies and subtracting the retained entropy gives the stated total correlation. If there are `f` retained fixed points, exactly `f` copies of `I(X:E)` are inside a site and the intersite total correlation is `(m-f) I(X:E)`. This checks current lines 31–56.

With independent fair bits `Z_j`, sums over donor and environment index sets have covariance

    sum_(a in D,b in T) Cov(Z_a,Z_b)=m/4.

Conditional means given an independently drawn route are `k/2`, so the total-covariance identity adds no between-route term and yields `E[m]/4`. Product-target covariance is zero. Since `m>=0`, it must vanish almost surely; two disjoint size-`k` subsets need `N>=2k`. This checks current lines 73–83. The independent routing hypothesis is used precisely at the conditional-law step.

The historical/experimental references in this file were not independently audited in this review.

## 2. Finite-jet rigidity: independent analytic audit

File: `workers/higher_order_rigidity/PROOF.txt`.

The relevant hypotheses are unrestricted smooth periodic `U,V:T->R^2`, unconstrained profile means, smooth density on the whole finite-dimensional jet space, finite derivative order, and universal domination. Integrand continuity plus differentiability at `B` suffices for the stated conclusions. Restricted profile libraries, bounded derivative tests, and restricted velocities would not suffice for this proof.

### 2.1 Bounded Euler derivative, lines 51–75

For fixed `U`, periodic integration by parts gives `DP(U)[V]=E e_p.V`. The smooth velocity `V_eta=e_p/sqrt(|e_p|^2+eta^2)` has norm at most one. Since `F` is bounded on the compact set of matrix columns with `|V|<=1, |U'|<=R`, domination bounds the left side by `M_R`. Pointwise convergence and the fixed profile's integrable smooth Euler derivative justify `eta->0`, giving

    E|e_p|<=M_R.

No estimate of `V_eta'` is needed: the action contains `V`, not its transverse derivative. If domination is originally stated for strips, one first takes the short-strip limit for each fixed smooth `U,V`; only afterward are high-frequency profiles introduced. No uniform short duration in the frequency is needed.

### 2.2 Oscillation and arbitrary jets, lines 77–106

For `e=C(j^(r-1)U) U^(r)+R(j^(r-1)U)`, take

    U_N=U_0+N^(-r+epsilon) h sin(Ny), 0<epsilon<1.

Every derivative through `r-1` converges uniformly to its counterpart for `U_0`; the largest perturbation among these has size `N^(-1+epsilon)`. In particular the first derivative is bounded when `r>=2`. The lower-jet remainder is uniformly bounded because the lower jets remain in a compact set. After dividing by `N^epsilon`, its contribution vanishes uniformly. The bounded contribution from `U_0^(r)` also vanishes, and the remaining principal term is

    C(j^(r-1)U_0(y)) h sin(Ny+r*pi/2)+o(1).

The norm factors as `|C(y)h| |sin(...)|`. Periodic averaging against a continuous coefficient gives the limit `(2/pi) E|C(y)h|`. The Euler `L1` bound makes this zero. Continuity then gives pointwise vanishing on the chosen profile. A local Taylor polynomial times a compactly supported bump realizes any prescribed finite jet in a circle chart; hence the coefficient vanishes on the entire jet space. Localization does not assume the target jet repeats periodically.

The condition `r>=2` is essential. At `r=1`, this amplitude would make `U_N'` grow, so the method does not eliminate the first-order skew area term. The proof retains that term correctly.

### 2.3 Highest coefficients and order descent, lines 108–149

In `sum_j (-D)^j p_(q_j)`, the only derivative of order `2k` comes from the `j=k` term and has coefficient `(-1)^k p_(q_k q_k)`. All other terms involve jets at most `2k-1`. The preceding oscillation forces this Hessian to vanish, so

    p=a(q_0,...,q_(k-1)).q_k+b(q_0,...,q_(k-1)).

For this affine density, only `(-D)^k a` and the `q_(k-1)` derivative of `a.q_k` contribute to order `2k-1`. Their coefficients are respectively `(-1)^k Da` and `(-1)^(k-1) Da^T`. Terms in which derivatives hit the coefficient have maximal jet order `2k-2`, even when they are nonlinear products of lower derivatives. Thus the stated principal coefficient is exact.

For `k>=2`, `2k-1>=3`, so oscillation forces `Da=Da^T` in the highest lower-jet fiber. On that full Euclidean fiber, set

    h(lower,x)=integral_0^1 a(lower,tx).x dt.

Differentiating in `x`, symmetry changes the integrand into the derivative of `t a_j(lower,tx)`; integration gives `h_x=a`. The dependence on lower jets remains smooth. Thus `D_y h` cancels exactly `a.q_k`; the residual has order `k-1`. Since `h` is a single-valued smooth function of periodic jets, its total derivative has integral zero. Its functional and first variation both vanish, so domination transfers to the reduced density without any approximation or continuity of `P` on nonsmooth profiles. Repetition gives the claimed first-order form, with the sum of removed primitives of order at most `k-1`.

No topological obstruction occurs: the relevant fibers and profile-value target are Euclidean, and the proof does not assert the same representation for manifold-valued profiles or non-single-valued primitives.

### 2.4 Freezing and rare-phase localization, lines 168–217

The first-order Euler calculation gives `grad c(U).V+kappa(U)det(V,U')` with the sign in line 176. Constant profiles and both signs of constant infinitesimal velocity force `grad c=F_1(B)`.

For a smooth mean-zero `q=w'`, the profiles `U_N=z_0+w(Ny)/N` converge uniformly to `z_0`, while `U_N'=q(Ny)`. The action average is unchanged by integer dilation. Continuity of `kappa` on the bounded profile-value range and boundedness of fixed `v,q` justify freezing `kappa` at `z_0`.

For arbitrary `v_0,q_0`, use a two-phase test with the desired pair on fraction `theta` and `(0,-theta q_0/(1-theta))` elsewhere. At each fixed `theta`, periodic convolution preserves the mean and stays in a fixed compact set, so the smooth tests converge to this piecewise-constant test under the continuous integrand. Only afterward let `theta->0`. The compensating phase contributes `-F_2(B).q_0` after dividing by `theta`, by differentiability at `B`. This yields exactly the global determinant-affine supporting inequality.

The proof correctly distinguishes existence of a constant-curvature replacement from constancy of the curvature of every initial density. The example `F(X)=|X|^2`, `kappa(z)=sin(z_1)` at lines 214–216 verifies why the stronger assertion would be false.

### 2.5 All backgrounds and finite convex lift, lines 225–253

The determinant expansion gives the displayed supporting affine functions on `(A,det A)`. Their supremum is convex and agrees with `F` on that graph. It is finite off the graph: choose `X` with `det X=t-det A`; then `(A,t)` is the midpoint of `(A+X,det(A+X))` and `(A-X,det(A-X))`. Every supporting affine function is bounded above at the midpoint by the average of the two finite `F` values; any one affine support supplies a finite lower bound.

Conversely, a proper convex lift finite on the determinant graph is finite on its entire convex hull, which is all of the lifted space by the same midpoint identity. A subgradient therefore exists at every graph point. Testing both signs of an infinitesimal matrix displacement identifies `M+kappa cof B=DF(B)`, and the supporting inequality supplies the storage. This repairs a possible extended-value-domain concern explicitly; it is not left implicit.

### 2.6 Trace and connector scope, lines 260–350

The explicit negative-entry action is consistent with direct integration of `(1/4+r^2)^2-(4/sqrt(3))(1/4+r^2)r/2` over `x=2r`. The critical profile difference has fourth power `16 N^-3 sin^4(Nh/2)`, giving the stated `N^(4s-3)` seminorm factor. At `s=3/4`, boundedness plus strong `L4` convergence and reflexivity imply weak convergence to zero. The two signed storage bounds rule out weak lower and upper semicontinuity separately. They do not rule out strong continuity in the critical topology.

Closed concatenations are continuous piecewise smooth maps with matching traces, hence belong to `W^(1,4)` despite jumps of normal derivatives. Quartic polynomial action is continuous under strong `W^(1,4)` approximation by Hölder's inequality. This makes a separately assumed quasiconvexity theorem applicable to the closed concatenation; it does not derive that theorem from the open-strip inequalities.

For the general spiral, `v=-J a_2/n` gives `nJv=a_2` and `det(v,a_2)=n|v|^2`. Hence `alpha=det A/(n|v|^2)>0`; the claimed gradient is exact. A fixed-width smooth cutoff at large negative `x` has derivative energy `O(exp(-4 alpha T))`, so the finite negative entry follows from the negative half-cylinder limit. Simultaneous reversal of `x,y` negates the full gradient and preserves homogeneous quartic energy.

No decisive proof gap was identified in these portions. The cited historical trace/null-Lagrangian literature was not independently reread for this review.

## 3. Nonlocal coefficient-linear selector: independent audit

File: `workers/nonlocal_compensation/NO_LINEAR_SELECTOR.md`.

### 3.1 Exact map hypotheses

The theorem at lines 74–81 is about a single real-linear map from all nine integrand coefficients to finite real profile functionals, normalized at zero, whose values dominate all finite smooth strips for every cone energy. It does not assume locality, Fourier truncation, differentiability, full-profile continuity, or translation invariance. Additive positively homogeneous selection on the entire cone is equivalent to such a linear extension for this purpose. A nonlinear integrand-dependent selection is outside the theorem.

### 3.2 Averaging arbitrary potentials, lines 83–110

For a fixed smooth `U`, the path `U(y+theta+sign(h)x)` over width `|h|` joins two translation-orbit points. Both orientations have finite action bounded in absolute value by `C(F,U)|h|`. Domination in both directions yields a Lipschitz orbit function. Thus ordinary integration in `theta` is justified without assuming measurability of arbitrary profile functionals in advance.

This initially applies only to energies that dominate. For an arbitrary quartic `f`, homogeneity bounds the Hessian by `C_f |A|^2|R|^2`, whereas the Hessian of `H=|A|^4` is at least `4|A|^2|R|^2`. A sufficiently large `MH+f` is convex, as is `MH`. By coefficient linearity, `P_f` is their difference and also has a Lipschitz orbit. Therefore every coordinate functional can be averaged. The averaged assignment stays linear, normalized and dominating because the action is transverse-translation invariant.

This is stronger than simply declaring a Haar average: it proves the required integrability for every coordinate. No unproved whole-space regularity is hidden here.

### 3.3 Even components, lines 112–143

For `R_t=|X+tY|^4`, the compatible drift strip `Phi_T(x,y)=psi(x/T,y-tx)` satisfies `Phi_x+t Phi_y=T^-1 psi_s`. Its action is `T^-3` times a fixed finite integral. Translation invariance removes the final shift. Both endpoint directions force the averaged storage for `R_t` to be constant, hence zero.

The same slow strip without drift gives determinant-square action of order `T^-1`. The determinant is affine on rank-one matrix lines, so its square is rank-one convex and can be used. It is not required to be convex as a function of all matrix entries.

The coefficients of `R_t` are the five directions `u^2, uw, uv+2w^2, vw, v^2`. A Vandermonde argument shows they lie in the span of these energies, and `q^2=uv-w^2` supplies an independent sixth direction. Thus the even invariant subspace's averaged assignment vanishes.

### 3.4 Odd components, lines 145–186

Complex multiplication by `t+i rho` is a real linear map, so `|X+(t+i rho)Y|^4` is convex. Its even/odd decomposition at lines 153–154 has the correct sign for `q=Im(conj X Y)`.

The strip `Phi_rho(x,y)=psi(rho x,y-tx)` has duration `1/rho` and satisfies

    Phi_x+(t+i rho)Phi_y=rho(psi_s+i psi_y).

Its action is therefore `rho^3` times a fixed finite quantity. The surviving assigned odd term is `-4rho Delta K_t-4rho^3 Delta P_(qv)`. Divide domination by `4rho` and let `rho->0+`; the result is `Delta K_t>=0`. Reversing the endpoint path gives the opposite sign. Finiteness of each fixed endpoint value suffices; no profile compactness or passage of an operator limit through an unknown functional is occurring. Then `t=0,1,-1` kills all three odd directions.

### 3.5 Contradicting witness and cone extension, lines 188–228

The Dacorogna–Marcellini acoustic square identity and two-sided rotational invariance give rank-one convexity in all directions. Adding `H/1000` gives an acoustic lower bound `(1/250)|A|^2|R|^2`, so the witness lies inside the coefficient cone. Its explicit negative open-strip action contradicts the forced zero averaged storage.

For cone-only assignment, if `F-G=F'-G'`, then `F+G'=F'+G`. Additivity gives equal functional differences. Since the cone generates the full vector space by the convex decomposition above, the difference extension is well defined everywhere, and positive real homogeneity makes it real linear. There is no assumption that individually chosen storages have a unique canonical representative.

If domination is initially imposed only in the strict acoustic interior for an already linear map, `F+epsilon H` is interior for every cone energy `F`. For each fixed strip and endpoint pair, both sides of the domination inequality are exact affine expressions in `epsilon`. Letting `epsilon->0` legitimately extends domination to the boundary energies used in the proof.

The same argument also covers additive positively homogeneous assignment defined only on the interior: the interior generates the vector space by differences, the well-defined extension uses sums that remain interior, and then the displayed boundary limit applies. This last combined variant is an immediate additional deduction, rather than a new regularity assumption.

No decisive proof gap was identified in the no-selection theorem. Its conclusion is a restriction on a universal linear assignment, not a contradiction to quasiconvexity or to nonlinear nonlocal storage.

## 4. Quantum fixed-copy polynomial obstruction and finite-error scope correction

Files: `workers/quantum_information_operation/REPORT.md`, Section 4, lines 134–173; `workers/quantum_information_operation/SCOPED_CORRECTION.md`, lines 11–39. Both must be read together.

For the iid classical-quantum family

    rho_t=t|00><00|+(1-t)|11><11|, 0<t<1,

the `N`-copy input expands in computational-basis projectors with coefficients `t^a(1-t)^(N-a)`. Every effect probability after a fixed parameter-independent completely positive map is linear in the input matrix, hence polynomial in `t` of degree at most `N`.

For `m` exact mutually independent product-marginal outputs, the all-zero effect probability is `t^(2m)`. Equality on an open interval forces equality as polynomials, yielding `N>=2m`.

For a heralded trace-nonincreasing success map, its success probability `q(t)` is a polynomial of degree at most `N`. The corresponding unnormalized all-zero probability must be `q(t)t^(2m)`. If the success map is nonzero on the input family, then `q` is a nonzero polynomial; its product with `t^(2m)` has degree `deg q+2m`, with no possible leading-term cancellation. Thus

    N>=deg q+2m>=2m.

It is sufficient that success be positive at any interior parameter and correctness hold whenever success occurs: continuity gives an interval of positive success, and polynomial identity on that interval suffices. A success event defined using the unknown parameter itself would not be one fixed instrument and is not covered.

Adaptive measurements and stopping with a deterministic total copy budget at most `N` produce a single parameter-independent CP instrument on `N` copies after unused copies are ignored. The proof still applies. An unbounded-copy protocol with only an expected-copy guarantee is not represented by a fixed degree-`N` polynomial and is outside this argument. Approximate product output, merely correct one-output marginals, known-parameter state preparation, correlated initial copies, and input side information identifying the parameter are also outside the exact stated theorem.

The same nontrivial-dimension condition as in routing is required to embed this family. A register of dimension one is an immediate exception to a blanket `2m` necessity claim.

The finite-difference estimate in the frozen report's lines 165–171 is valid for deterministic CPTP output with error measured by half the trace norm. Every effect probability then differs by at most the trace-distance error. If `d=2m`, the order-`d` difference on the grid `j/d` annihilates any degree-at-most-`d-1` output polynomial and takes the value `d!/d^d` on `t^d`. The absolute binomial weights sum to `2^d`, giving the displayed lower bound `d!/(2^d d^d)`.

That proof does not apply to a normalized heralded output: its effect probability is `f(t)/q(t)`, generally rational. This scope gap was sent to the quantum worker. The added correction explicitly restricts the approximate-output statement to deterministic CPTP maps and provides a valid one-copy rationality example: success probabilities `1` and `1/2` on the two classical input bits give normalized zero probability `t/(1/2+t/2)`, whose second finite difference on `0,1/2,1` is `-1/3`. This is a counterexample to a polynomial premise for normalized heralded outputs, not a counterexample to the exact no-go or to an independently proved approximate heralded bound.

### Conditional and unconditional endpoint concentration

The additional concentration proof at report lines 183–249 also reconstructs. Conditional on all labels and independently selected route randomness, pair/triple components use disjoint original preparations and independent local continuations/readouts. A component of size `ell` contributes a bounded sum in `[0,ell]`; Hoeffding's lemma pays `ell^2`. Thus `sum ell^2<=3N` gives the conditional exponent `3N lambda^2/8`.

The conditional mean is `mu(C)=sum_c g_c(k_c)`, with `g_c(1)=o_c` and `g_c(k)=k d_c` for `k>=2`. A single count increment is `o_c`, `2d_c-o_c`, or `d_c`, lying in `[-1,2]`; one label change decrements one count and increments another, giving sensitivity at most `3`. This is attained by a count-two group with `(o,d)=(1,0)` and a count-one group with `(o,d)=(0,1)` when one label is transferred between them. McDiarmid's mgf bound therefore pays `9N lambda^2/8`. Combining conditional and label variation gives `12N lambda^2/8`, hence two-sided tail `2 exp(-BN t^2/6)` for `B` independent batches and the stated four-arm union-bound radius.

The actual recorded score must have range `[0,1]`. A bounded desired expectation alone is insufficient for a signed or readout-corrected recorded estimator. Correlated preparations, cross-component gates, or shared measurement noise are outside the local-product proof, as the report states.

## 5. Positive strict-certificate transfer to strong critical-trace storage

File: `workers/external_machinery/HEAT_TO_CRITICAL_TRACE.md`, Sections 2–9. The reviewed version explicitly defines incoming paths in `W^(1,4)` at lines 50–60. Source conversion read: repository `updates/FE/synthesis/quartic/QUARTIC_AUDIT_AND_PROOF.md`, lines 77–158.

### 5.1 Input premise and path space

The required input is global quasiconvexity of `F-epsilon |A|^4`, with `epsilon>0`, not rank-one convexity alone and not merely quasiconvexity at zero. The positive theorem is conditional on this strict premise. The source heat argument converts a rational compatible-jet margin `rho` into `epsilon=rho/24`, because the compatible Hessian energy of `|A|^4` is at most `24|A|^2|z|^2`. The source analytic conversion was reconstructed; this review did not independently expand every entry of the inherited rational 24-by-24 Gram identity.

The Sobolev incoming class is necessary: for a nonsmooth critical trace, a class of globally smooth paths with that exact endpoint could be empty. For smooth endpoints, subtracting a smooth boundary lift and approximating the resulting zero-trace Sobolev map gives smooth paths with exactly the same endpoints and convergent quartic action. This closes the regularity gap without pretending that smoothing a rough endpoint preserves it.

The adjusted action removes `DF(B):D Phi`. Its integral over a general open strip is `F_1(B)` times the change of transverse mean. Restoring this term gives the original-action storage. The adjusted incoming value is invariant under adding a constant to the endpoint because a long ramp to that constant has adjusted action tending to zero; paths with moving means remain admissible. Projecting every path to mean zero would be a different, unjustified restriction.

### 5.2 Critical extension

For a fixed linear lift `EU(-t)=chi(t)(eta_t*U)`, differentiated mollifier kernels have zero integral and size `t^-2` on an interval of length `O(t)`. Jensen's inequality gives the fourth-power derivative estimate `C t^-5 integral_(|h|<=t)||Delta_h U||_4^4 dh`. Tonelli integration in `t` changes this into the critical kernel `|h|^-4`. Cutoff terms are controlled by `||U||_4^4`. A trace estimate and the zero value at the opposite boundary give the reverse norm bound. Thus `e_4(U)=||D EU||_4` is an equivalent strong critical-trace norm on the mean-zero subspace, with constants tied to the selected lift.

The fixed slab has normalized measure one, so `e_2<=e_4`. No finite bandwidth, single-mode approximation, or weak compactness assertion is involved in this extension.

### 5.3 Coercivity uniform in strip duration

For `H(A)=|A|^4`, normalize `|A|=1` and decompose `B=tA+B_perp`. Its affine remainder is `6t^2+2|B_perp|^2+4t+1`. Subtracting `(1/4)(|B|^2+1)` gives

    (23/4)(t+8/23)^2+(7/4)|B_perp|^2+5/92,

so the lower bound by `(1/4)(|B|^2|A|^2+|A|^4)` is correct. Quartic polynomial growth and its derivative provide the stated `C0,C1` estimates, including the mixed cubic terms by Young's inequality.

Close any incoming path by the reversed fixed lift of its endpoint. Matching traces suffice for `W^(1,4)` gluing and periodic closure; normal derivatives need not match. Strict quasiconvexity bounds the total adjusted action below by `epsilon/4` times the closed derivative energy. Bounding the return action in absolute value by `C0 C_B(U)` yields the stated coercivity of the incoming path. Its constant does not depend on the incoming width. The fixed incoming lift gives the complementary upper bound, hence finiteness and normalization of the value. A near minimizer's full derivative energy is bounded even if its widths diverge. No minimizer or compactness on the union of widths is asserted.

At zero background the quartic remainder is exactly `H(A)`, so the improved factor `epsilon` is valid. For `M=113/40` and `epsilon=1/12000`, the near-minimizer factor is `2M/epsilon=67800`.

### 5.4 Terminal-slab perturbation and strong continuity

Pad a near-minimizing path at its zero start to width at least one. Add `E(W-U)` only on the final unit slab, extended by zero before it. This changes the endpoint to `W` while keeping exact compatibility at the left seam. The fundamental theorem of calculus, the derivative bound, Hölder, and Minkowski give

    |Delta action| <= C1[|B|^2(||A||_2+||Z||_2)||Z||_2
                          +(||A||_4+||Z||_4)^3||Z||_4].

The near-minimizer coercivity controls the old full-strip norms. Let the optimizing error tend to zero, repeat with the endpoints exchanged, and obtain the claimed modulus. At `B=0` this yields the displayed cubic bracket times `e_4(W-U)`. On a bounded strong critical ball the coefficient is bounded, proving local Lipschitz continuity. This argument genuinely uses the strict positive margin; a merely finite incoming value would not by itself control the gradients of optimizing paths.

### 5.5 Fstar constants, concentration, and finite approximation

The retained formula gives `Fstar(I)=-3/10`. Writing `s=u+v`, `t=q/s`, and using `w^2<=s^2/4-q^2` gives the stated lower envelope `-3/40` and upper envelope `113/40` for `Fstar/s^2`. Differentiating the terms yields gradient bounds `4,4,7/2,29/5` times `|A|^3`, summing to `173/10`.

For the two-piece radius, the first action is `23/1920`; on the exponential piece `r'=r` and the action is `(-3/10)*(15/64)=-9/128`. Their sum is `-7/120`. The path is `W^(1,4)` and in fact has matching first derivatives at the join. The Sobolev statement gives the exact value; smooth exact-endpoint approximation gives the same endpoint storage bound as a limit. Simultaneous reversal of both coordinates preserves any homogeneous quartic under total gradient negation and supplies the opposite-winding return.

Critical concentration keeps these actions fixed, while the profiles converge weakly to zero and retain bounded critical norm. Thus any dominating storage, including the strongly locally Lipschitz incoming value, fails weak lower and upper semicontinuity at zero. At nonzero background, the adjusted cubic contribution vanishes by transverse sign symmetry and the quadratic correction is `O_B(N^-1/2)`, so the same obstruction persists. This is consistent with strong critical continuity because the sequence does not converge strongly there.

Every fixed finite Fourier measurement sees both sufficiently high-frequency winding profiles as zero. Their storage values are separated by at least `7/60`, forcing uniform approximation error at least `7/120` on a critical ball containing the sequences. Per-profile strong Fourier convergence is still valid, with the actual critical tail charged. The report correctly avoids asserting equality of free-time values under frequency replication on one fixed torus; unrestricted minimizers could break the smaller period.

No decisive gap was identified in this conditional positive theorem or its stated Fstar analytic application.

## 6. Continuous informative labels and adjacent-pair routing

File: `workers/exchange_robustness/PROOFS.md`, lines 139–181, with the task-channel contract at lines 80–116.

The premise is a known observed scalar `t(c) in [a,b]` and an acquired uniform half-diamond bound `eta_a(c,c')<=L|t(c)-t(c')|` for every relevant pair and each policy actually scored. Conditioning on the entire list of fine observed records leaves the joint preparations as a tensor product of their conditional states, under the iid cq input contract. Sorting those records does not destroy this conditional factorization.

For an adjacent pair with labels `c,c'`, donor `c` is evaluated with its own full record, reference and specified policy against recipient bath `tau_c'`; the ideal comparator uses `tau_c`. The diamond bound applies to arbitrary reference entanglement and gives score error at most `L gap`. The other donor gives the same upper bound, so the pair contributes at most `2L gap` to the sum. Ordered disjoint adjacent intervals have total length at most `b-a`, yielding conditional average bias at most `2L(b-a)/N`.

Every donor is retained exactly once. Thus the sample average of its ideal fine-record score has the original population expectation, and averaging the conditional bound yields the stated population bias. Unique fine records cause no problem under this certificate. Keeping one native singleton when `N` is odd pays at most `1/N`; discarding it would change the target. Pair output blocks can remain correlated, so this expected local-score result does not evade the exact `N>=2m` lower bound for globally independent product outputs.

The important acquisition and selection boundaries are real:

- A smooth numerical record does not imply smooth conditional channels. An additional fine hidden bit can select orthogonal environmental states independently of `t`; a future controlled gate can then have order-one response differences between arbitrarily close scalar labels. No finite `L` follows from the scalar alone.
- For donor-dependent policy `a(c)`, the same policy must be compared under both bath states. A bound only for the recipient's resident policy does not establish the stated donor target.
- Uncertainty in `t`, the response Lipschitz constant, or channel calibration must enter the bound. A certificate for a true unobserved coordinate cannot silently be used for a noisy recorded coordinate.
- Data-dependent minimum-cost route selection is justified only by simultaneous valid edge bounds over all candidate matches, or a valid held-out selection protocol. Pointwise confidence intervals chosen after looking for the best edge are insufficient.
- Physical interchangeability, independent joint preparations conditional on the records, local continuation/readout, allowed pair connectivity, and buffer/latency costs remain supplied or acquired premises.

These qualifications are already retained in the worker's stated scope. No additional correction was required.

## 7. Optional convex-tilt value calculation

File: `workers/nonlocal_compensation/EXACT_TILTED_CONVEX_ACTION.md`, lines 34–98.

For `C_(t,rho)=|X+(t+i rho)Y|^4`, the group action `exp(-ik theta)Phi(x,y+theta)` preserves the circular boundary mode and the energy. Convex Jensen averaging removes every other transverse mode without increasing action. This step would be invalid for a general nonconvex rank-one-convex energy, and the supplement does not claim that transfer.

For the retained mode, the phase gauge `r=exp(-ikt x)z` gives action `integral |z'-rho k z|^4`. The endpoint is a linear weighted integral of its control. Hölder with exponents `4,4/3` yields the exact fixed-width bound; the displayed exponential control achieves equality. Taking the explicit width limits gives incoming value `(64/27)rho^3(-k)_+^3|a|^4` and return value `(64/27)rho^3(k)_+^3|a|^4`. For nonzero amplitude every finite-width value is strictly above the respective limiting infimum. The claimed nonattainment and orientation are correct, including the zero-frequency case.

This supplies a valid convex-family calibration model with arbitrary-frequency interiors. It supplies no missing lower bound for negative-valued full-cone integrands.

## 8. Verification boundary and final review state

The substantive checks above are analytic reconstructions. No original scientific script was executed or changed for this review. No external literature was used to certify novelty or correctness. The final report should retain the distinctions between source claims, internally derived statements, same-team criticism, and independent external review.

The final quantum theorem, its separate finite-error scope correction, the strict-certificate action-storage argument, and the adjacent scalar-pairing proof have now been reviewed. No required proof-scope correction remains unrecorded in the reviewed files or their explicit supplements. Historical references, full original Gram expansion, physical gates and full-cone quasiconvexity remain outside this review's established conclusions.

Memory was used only for source-preservation and scope conventions, not as a mathematical premise: `MEMORY.md` lines 24–29, 36–37. All mathematical statements evaluated here were reconstructed from current files.
