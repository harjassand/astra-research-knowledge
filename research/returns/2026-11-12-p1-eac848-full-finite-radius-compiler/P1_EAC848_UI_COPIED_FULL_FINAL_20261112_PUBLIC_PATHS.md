**Yes, using the accepted constructions in your question.** The remaining transport step can be closed by a polynomial Poincaré inequality for the dilute hard-ball configuration space. The useful construction is a geometric comparison of Dirichlet energies: a very small inward deformation, followed by a rank-based separation, followed by paths that move one particle at a time.

For a suitable **positive rational square** \(\rho=a^2\), the resulting bound is
\[
\boxed{
\operatorname{Var}_{\mu_{\mathcal K}} f
\le 2^{20}(1+N_0)
\int_{\mathcal K}|\nabla f|^2\,d\mu_{\mathcal K}.
}
\tag{1}
\]
Here \(\mathcal K\) is any labelled hard-ball configuration domain occurring under the conserved mass cap, and \(\mu_{\mathcal K}\) is its normalized uniform measure. A sufficient geometric restriction is
\[
\boxed{
a\le
2^{-30}\bigl(2+N_0+F+\kappa^{-1}\bigr)^{-20},
\qquad \rho=a^2.
}
\tag{2}
\]
Further shrinking \(a\) pays the required radius ceiling and stationary chemical bias.

I give the new estimate first, then assemble the compiler, including its parameter order, exact marks, faults, and actual costs. The deformations and random paths used in proving (1) are analytical integration devices. They add no force, relocation, sampler, optimizer, or preprocessing operation to the emitted particle system.

## 1. The hard-ball Poincaré estimate

Write \(N=N_0\). Fix a physical count and label its \(n\le N\) particles for this proof. Put
\[
r_i=\rho d_i,\qquad
\sum_{i=1}^n d_i\le N.
\]
The configuration domain is
\[
\mathcal K=
\left\{
q:
n_f\cdot q_i\le b_f-r_i,\quad
|q_i-q_j|\ge r_i+r_j
\right\}.
\]
The case \(n=0\) is trivial.

Use inward gap functions
\[
g_{if}(q)=b_f-n_f\cdot q_i-r_i,\qquad
g_{ij}(q)=|q_i-q_j|-r_i-r_j.
\]
There are at most
\[
J_c=nF+\frac{n(n-1)}2
\]
constraints. Your accepted near-contact construction supplies the common inward margin
\[
\alpha=\frac{\kappa}{2^{10}(1+N)^2}
\tag{3}
\]
for constraints whose gaps are at most \(\rho\).

The proof has three parts.

### 1.1 A tiny inward buffer with bounded volume distortion

Choose a nonnegative Lipschitz cutoff \(\chi\) satisfying
\[
\chi(u)=1\quad(u\le 1/4),\qquad
\chi(u)=0\quad(u\ge 1/2),\qquad
\operatorname{Lip}(\chi)\le 8.
\]

For a global definition, extend each pair-gradient vector by replacing
\[
\frac{q_i-q_j}{|q_i-q_j|}
\quad\text{with}\quad
\frac{q_i-q_j}{\max(|q_i-q_j|,\rho)}.
\]
Call the resulting constraint vectors \(b_j(q)\). They equal \(\nabla g_j(q)\) on \(\mathcal K\), because feasible pair separations are at least \(2\rho\). They have uniformly bounded norms and global Lipschitz constants at most \(C/\rho\).

Define \(V(q)\) as the unique minimizer of
\[
\frac12|v|^2+
8\alpha^{-2}
\sum_{j=1}^{J_c}
\chi\!\left(\frac{g_j(q)}{\rho}\right)
[1-b_j(q)\cdot v]_+^2.
\tag{4}
\]
Finally clip this minimizer to the ball of radius \(\alpha^{-1}\).

On \(\mathcal K\), the common inward direction divided by \(\alpha\) makes every nonzero penalty vanish. Comparing the minimizer with that vector shows that clipping changes nothing there and that
\[
|V(q)|\le\alpha^{-1}.
\]
For any constraint with \(g_j(q)\le\rho/4\), the same comparison gives
\[
8\alpha^{-2}[1-b_j(q)\cdot V(q)]_+^2
\le \frac1{2\alpha^2},
\]
hence
\[
\nabla g_j(q)\cdot V(q)\ge\frac34.
\tag{5}
\]

Strong convexity in \(v\), together with the Lipschitz bounds on the coefficients of (4), gives the safe global estimate
\[
\operatorname{Lip}(V)\le
L_V:=
\frac{2^{16}(1+J_c)^2}{\alpha^3\rho}.
\tag{6}
\]
This uses only fixed powers. For example, before clipping, comparison with \(v=0\) bounds the minimizer by \(4\sqrt{J_c}/\alpha\); applying strong monotonicity to the two minimizer equations then gives (6).

Set
\[
\eta=
64\rho^3(1+N)^5\kappa^{-2}.
\tag{7}
\]
Let \(B_s\), \(0\le s\le1\), be the flow of \(V\) for time \(2\eta s\).

Equation (5) implies both forward invariance of \(\mathcal K\) and
\[
B_1(\mathcal K)\subseteq
\mathcal K_\eta:=\{g_j\ge\eta\ \text{for every }j\}.
\tag{8}
\]
Indeed, a gap below \(\rho/4\) increases at rate at least \(3/4\), and a gap already above \(\eta\) cannot cross downward through \(\eta\).

The flow is injective. Its inverse is \(e^{2\eta L_V}\)-Lipschitz, so every intermediate volume distortion is bounded by
\[
\exp(6nL_V\eta).
\]
Put \(G_{\rm geo}=2+N+F+\kappa^{-1}\). Under (2),
\[
6nL_V\eta
\le 2^{55}\rho^2G_{\rm geo}^{21}<\log 2.
\tag{9}
\]
Thus
\[
(B_s)_\#\mu_{\mathcal K}\le 2\mu_{\mathcal K}.
\tag{10}
\]

The corresponding energy cost is small:
\[
\int_{\mathcal K}
|f(q)-f(B_1q)|^2\,d\mu_{\mathcal K}
\le
8\eta^2\alpha^{-2}
\int_{\mathcal K}|\nabla f|^2\,d\mu_{\mathcal K}.
\tag{11}
\]

The purpose of this first step is precise: it creates enough clearance for the next deformation while changing volume density by only a universal factor.

### 1.2 Rank separation with controlled density

For a buffered configuration \(x\), sort its first coordinates. Let
\[
k_i=\operatorname{rank}(x_{i1})-\frac{n+1}{2},
\]
using labels to resolve ties. Define
\[
\theta=\frac{4an}{\kappa},
\qquad
S_s(x)_i=(1-s\theta)x_i+s\theta c+sa k_i e_1,
\qquad 0\le s\le1.
\tag{12}
\]

This contracts slightly toward the certified interior point and separates particles according to their first-coordinate ranks.

**Wall feasibility.** Since \(|k_i|\le n/2\),
\[
\begin{aligned}
b_f-n_f\cdot S_s(x)_i-r_i
&\ge
(1-s\theta)\eta
+s\theta(\kappa-r_i)-sa|k_i|.
\end{aligned}
\tag{13}
\]
The small-radius conditions imply \(\kappa-r_i-\eta\ge\kappa/2\), so the right side is at least \(\eta\).

**Pair feasibility.** For a pair, let \(z=x_i-x_j\) and \(k=k_i-k_j\). Sorting gives
\[
z_1k\ge0,\qquad |k|\ge1.
\]
Consequently,
\[
\begin{aligned}
|S_s(x)_i-S_s(x)_j|^2
&\ge (1-s\theta)^2|z|^2+s^2a^2k^2\\
&\ge
\frac{|z|^2}{1+\theta^2|z|^2/(a^2k^2)}.
\end{aligned}
\tag{14}
\]
The final expression is increasing in \(|z|^2\). Taking
\[
|z|\ge R+\eta,\qquad R=r_i+r_j\le\rho N,
\]
and using (7) shows that (14) is at least \(R^2\). The possible loss is of order
\[
n^2R^3/\kappa^2,
\]
which is exactly what the buffer pays.

At the endpoint,
\[
|(S_1x)_i-(S_1x)_j|
\ge
|(S_1x)_{i1}-(S_1x)_{j1}|
\ge a.
\tag{15}
\]

There is also a useful density property. On each rank chamber, \(S_s\) is affine with Jacobian
\[
(1-s\theta)^{3n}.
\tag{16}
\]
The output ordering recovers the input ranks, so different chambers have disjoint images. Condition (2) ensures that (16) is at least \(1/2\).

The rank map is discontinuous across ties, but this causes no loss in the integral argument: ties and their preimages under the buffer flow have Lebesgue measure zero. No summation penalty of \(n!\) appears.

Its squared speed is bounded by
\[
B_1^2:=2^{10}\rho n^3\kappa^{-2}.
\tag{17}
\]
Combining the two density distortions gives, for
\[
T=S_1B_1,\qquad \lambda=T_\#\mu_{\mathcal K},
\]
the bounds
\[
\lambda\le4\mu_{\mathcal K},
\tag{18}
\]
and
\[
\int |f(q)-f(Tq)|^2\,d\mu_{\mathcal K}
\le
\left(
16\eta^2\alpha^{-2}+8B_1^2
\right)
\int|\nabla f|^2\,d\mu_{\mathcal K}.
\tag{19}
\]
Every configuration in the support of \(\lambda\) has pair separations at least \(a\).

### 1.3 Coordinate paths through a common random intermediate configuration

Let
\[
\Omega_i=\{x:n_f\cdot x\le b_f-r_i\ \text{for all }f\},
\]
and let
\[
\nu=\bigotimes_{i=1}^n\operatorname{Unif}(\Omega_i).
\]
Then
\[
\mu_{\mathcal K}=\nu(\,\cdot\mid\mathcal K).
\]
The dilute feasibility estimate gives
\[
\nu(\mathcal K)\ge\frac12.
\tag{20}
\]
Also, each \(\Omega_i\) contains a ball of radius at least \(\kappa/2\).

Draw \(z\sim\nu\). Starting from an \(a\)-separated configuration \(u\), move particle \(1\) along \([u_1,z_1]\), then particle \(2\), and so on. Every wall constraint holds along these segments by convexity of \(\Omega_i\).

There are two collision estimates.

For an as-yet unmoved particle \(j>i\), the obstacle \(u_j\) is fixed and at distance at least \(a\) from \(u_i\). The endpoints \(z_i\) whose segment intersects the exclusion ball lie in a three-dimensional solid-angle cone. Thus
\[
\Pr\bigl([u_i,z_i]\cap B(u_j,r_i+r_j)\ne\varnothing\bigr)
\le
\frac{C(r_i+r_j)^2}{\kappa^3a^2}.
\tag{21}
\]

For an already moved particle \(j<i\), condition on \(z_i\). The bad locations of \(z_j\) lie in a three-dimensional tube:
\[
\Pr\bigl(\operatorname{dist}(z_j,[u_i,z_i])<r_i+r_j\mid z_i\bigr)
\le
\frac{C(r_i+r_j)^2}{\kappa^3}.
\tag{22}
\]

The payload bound gives
\[
\sum_{i<j}(d_i+d_j)^2
=(n-2)\sum_i d_i^2+\left(\sum_i d_i\right)^2
\le N^3.
\]
Therefore the probability that the entire coordinate path fails is at most
\[
\beta
\le
2^9\kappa^{-3}\rho^2N^3(1+a^{-2})
\le C\kappa^{-3}\rho N^3.
\tag{23}
\]
The radius ceiling makes \(\beta\le1/4\). For **any two** separated endpoints \(u,v\), a common \(z\) supports both coordinate paths with probability at least \(1/2\).

It remains to bound energy along these paths. From (18) and (20),
\[
\lambda\le \frac4{\nu(\mathcal K)}\,\nu.
\]
During the movement of coordinate \(i\), the current point is
\[
w=(z_1,\ldots,z_{i-1},(1-s)u_i+sz_i,u_{i+1},\ldots,u_n).
\]
For \(s\le1/2\), change variables from \(u_i\) to \(w_i\). For \(s\ge1/2\), change variables from \(z_i\) to \(w_i\). The Jacobian penalty is at most
\[
2^3=8.
\tag{24}
\]
All other unused coordinates integrate out. The valid-path indicator ensures \(w\in\mathcal K\).

This is the decisive dimension calculation: only one **three-dimensional** coordinate is interpolated at a time. There is no \(2^{3n}\) congestion factor.

Cauchy–Schwarz over the \(n\) segments, followed by conditioning the common intermediate configuration on validity, gives
\[
\operatorname{Var}_{\lambda}f
\le1536n
\int_{\mathcal K}|\nabla f|^2\,d\mu_{\mathcal K}.
\tag{25}
\]
Using (19),
\[
\operatorname{Var}_{\mu_{\mathcal K}}f
\le
\left(
32\eta^2\alpha^{-2}
+16B_1^2
+3072n
\right)
\int_{\mathcal K}|\nabla f|^2\,d\mu_{\mathcal K}.
\tag{26}
\]
Condition (2) absorbs the first two terms and proves (1).

The argument initially applies to smooth functions. The accepted local cone geometry makes \(\mathcal K\) a Lipschitz domain; qualitative Sobolev density extends it to \(H^1(\mathcal K)\). No quantitative chart-cover factor enters (26).

## 2. Consequences for unknown transport and predictable faults

For each fixed fine count, the nominal instantaneous Dirichlet form is
\[
\mathcal E_t(f,f)
=
\int_{\mathcal K}
\nabla f^\top A_0(t,q)\nabla f\,d\mu_{\mathcal K}.
\]
Uniform ellipticity and (1) give
\[
\mathcal E_t(f,f)
\ge
\frac{d_0}{C_P}\operatorname{Var}_{\mu_{\mathcal K}}f,
\qquad
C_P=2^{20}(1+N).
\tag{27}
\]
The invariant measure is the same uniform measure for every \(t\). Applying the energy identity to the actual time-ordered evolution therefore gives
\[
\|P^0_{s,t}f-\mu_{\mathcal K}f\|_2
\le
e^{-d_0(t-s)/C_P}
\|f-\mu_{\mathcal K}f\|_2.
\tag{28}
\]
Self-adjointness of the whole time-ordered evolution is unnecessary.

### All-start mixing without a population-dependent numerical exponent

Use the accepted short-time nominal smoothing estimate, uniformly over counts and profiles. Let \(\ell>0\) be its paid time scale and \(G\) a paid Lipschitz bound.

The local cone gives, in dimension \(m=3n\), a small-ball lower bound of the form
\[
\mu_{\mathcal K}\bigl(B(q,u)\cap\mathcal K\bigr)
\ge
\left(\frac{c\alpha u}{\sqrt m}\right)^m
\]
on a controlled local scale. If a \(G\)-Lipschitz function has supremum \(M\), this implies
\[
\|f\|_2^2
\ge
\frac{M^2}{4}
\left(\frac{c\alpha M}{G\sqrt m}\right)^m.
\tag{29}
\]
Taking the \(1/(m+2)\) power and using (28) gives an all-start mixing envelope
\[
\sup_q|P^0_{s,s+g}f(q)-\mu_{\mathcal K}f|
\le b(g),\qquad \|f\|_\infty\le1,
\tag{30}
\]
with
\[
\int_0^\infty b(g)\,dg\le I,
\tag{31}
\]
where \(I\) is a computable polynomial in the supplied numerical bounds and \(\rho^{-1}\).

The dimension enters the decay-time multiplier and polynomial prefactor. It does not become an exponent on \(R_{\rm num}\).

The smooth-boundary derivative-formula ingredient underlying this type of short-time estimate is available for time-dependent reflecting diffusions; here its use at corners and its polynomial constants are precisely the accepted local smoothing construction in your premises. [arxiv.org](https://arxiv.org/html/1211.3623v2?utm_source=chatgpt.com)

### The robust conditional occupation estimate

Combine (30)–(31) with the accepted short reflected comparisons and summable conditional telescoping.

For successful-channel predicates, use Lipschitz upper and lower approximations. Their discontinuity sets consist of cube faces, shifted walls, and pair-distance surfaces involving affected particles. Under feasible-uniform measure, their boundary tubes have polynomial bounds: feasible-uniform measure is dominated by a constant times product volume, and each individual tube estimate is three-dimensional.

Consequently there is a computable polynomial \(W\), uniform over fine counts, starting times, initial configurations and full past histories, such that the required normalized channel observables satisfy
\[
\boxed{
\left|
\mathbb E[f(Q_{s+g})\mid\text{past}]
-\mu_{\mathcal K}f
\right|
\le b(g)+W\delta^{2/9}.
}
\tag{32}
\]
One can obtain a stronger fractional power by directly sandwiching the terminal predicates; \(2/9\) is sufficient and matches the accepted interface.

All local comparison estimates are conditioned on the full past. They use the operator-norm covariance bound and predictable martingale estimates. Thus (32) permits correlated covariance errors, arbitrary switching, external randomness, and policies depending on every hidden mark.

The constants \(\ell,G,I,W\) are obtained by evaluating fixed rational majorants in
\[
1+N+F+\kappa^{-1}+\rho^{-1}+d_0^{-1}+\Lambda+r^{-1}.
\]
The compiler evaluates those majorants. It does not solve a configuration-space PDE or calculate an invariant normalizer.

## 3. The deterministic compiler and its parameter order

Use the accepted conservative well-mixed elementary compiler with error budget \(\epsilon/8\). Denote its:

- coefficients by \(b_e\);
- activities by \(\widetilde a_s\);
- decoder by \(P\);
- fine clock by \(H_{\rm kin}\);
- fault tolerance by \(\delta_{\rm kin}\).

Its base channels may be restricted to the already available \(2\leftrightarrow1\), unary, and global null channels. The permitted binary null channels are used for rejection branches.

Add exactly the structural rejection branches described in your accepted construction. Let \(M\) be the resulting directed-channel count, and put
\[
T=H_{\rm kin}\tau,\qquad v=(2r)^3.
\]

Compute \(V\) and the point-particle boundary normalization
\[
q=\frac1V
\int_{\Omega}\int_{\Omega}K_r(y-x)\,dy\,dx
\]
by the accepted fixed-dimensional rational volume algorithm. In particular,
\[
q\ge\kappa^6/4096.
\tag{33}
\]

Choose the rational proposal and statistical majorants
\[
L_*=
\frac{2^{10}(1+M)(1+N)^2(1+8/v)}q,
\qquad
J=1+L_*T,
\qquad
B_*=2^{10}L_*.
\tag{34}
\]
These have ample slack for ordered pairs, unary and global events, success/rejection branches, and the factor \(1+\delta\).

### Choose the radius before the new spatial clock

A concrete choice is
\[
a=\min\left\{
2^{-30}(2+N+F+\kappa^{-1})^{-20},
\frac{\min(\kappa,r)}
     {2^{16}(1+N+P_{\max})},
\frac{\epsilon\kappa^3}
     {2^{20}JB_*(1+N)^4},
\frac12
\right\},
\qquad
\boxed{\rho=a^2.}
\tag{35}
\]
Every quantity here is rational.

Because \(\rho\le a\le1\), this satisfies the required radius ceiling and (2). Moreover,
\[
\zeta_{2N}(\rho)
=
\frac{6\rho N}{\kappa}
+\frac{16\rho^3N^4}{\kappa^3}
\le
32\rho(1+N)^4\kappa^{-3},
\]
so
\[
JB_*\zeta_{2N}(\rho)\le\epsilon/64.
\tag{36}
\]
The reciprocal of \(\rho\) is polynomially bounded.

Now evaluate the polynomial majorants \(I,W\) from Section 2 for this chosen radius. Set
\[
h=
\left\lceil
\max\left\{
1,q^{-1},\frac{64L_*IJ}{\epsilon}
\right\}
\right\rceil,
\tag{37}
\]
\[
\boxed{
\delta=
\min\left\{
\frac14,\frac{\delta_{\rm kin}}2,
\left[\frac{\epsilon}{64J(1+W)}\right]^9
\right\},
\qquad
H=hH_{\rm kin}.
}
\tag{38}
\]

This order closes the dependency: \(\rho\) is chosen using the logical kinetic horizon and proposal budget; \(h\) is chosen afterward. No condition involving smallness of \(\rho hT\) is used.

### Emit the coefficients

For each binding/release reverse pair, emit
\[
c_e=\frac{b_e}{hq}.
\tag{39}
\]
For ordinary unary and global channels, emit
\[
c_e=\frac{b_e}{h}.
\tag{40}
\]
A rejection branch receives the same nominal coefficient as its underlying attempt.

Since \(h\ge q^{-1}\), all coefficients lie in \((0,1]\). Both members of every non-null reverse pair receive the same scaling, so
\[
c_e\widetilde a^{\alpha_e}
=
c_{\bar e}\widetilde a^{\beta_e}
\]
remains exact.

Chemical structure, decoder and label maps are unchanged apart from the structurally determined rejection loops. They depend only on the labelled reaction structure and its involution.

## 4. Complete timed-path accuracy

Augment any admitted actual realization with rejected proposals to the deterministic physical proposal rate
\[
L_*/h.
\]
Use the accepted conditional-channel coupling, retaining the actual tuple, placement, rejection subtype, continuous trajectory, and future fault policy.

For a chemical-free proposal gap:

- (32) controls the difference between the actual conditional channel probabilities and feasible-uniform averages;
- the supplied dilute estimate controls the difference between those averages and the point-normalized well-mixed probabilities;
- chemical multipliers contribute the direct \(O(\delta)\) term.

Integrating the transient envelope against the independent proposal gap contributes at most \(L_*I/h\) per expected proposal opportunity. Thus a conservative bound for the entire observed path is
\[
\begin{aligned}
d_{\rm TV}
\le {}&
\frac{\epsilon}{8}
+\frac{JL_*I}{h}
+JW\delta^{2/9}
+J\delta
+JB_*\zeta_{2N}(\rho).
\end{aligned}
\tag{41}
\]
Equations (35)–(38) make this strictly less than \(\epsilon\).

This is a coupling of complete marked paths. The physical proposal times become fine logical times after division by \(h\), and the final observation applies \(H_{\rm kin}\). Whenever the coupled channel categories agree, their rescaled times agree exactly.

The first proposal gap is included in the transient term in (41). Initialization remains the given original particles at their given feasible positions.

### Rejected attempts and original null marks

At a proposal, keep every base successful channel—including each genuine original null and parallel label—as its own category. Remaining outcomes are hidden.

The actual rejection subtype and its effect on the future policy remain in the coupled history. A reference process can carry these extra hidden marks without changing its chemical count law or observed marked law. Computing an equilibrium rejection intensity is unnecessary.

True original null channels retain identity placements. In the paired-prefix construction, the observed unary step for a decoded null has equal source and target payload, hence equal radius. Such an observed null is not converted into a steric rejection.

Independent faults on success and rejection branches are covered separately by the dominating rate and conditional comparison.

## 5. Exact balance, graph properties and existence

### Spatial balance

For a binding \(A+B\to C\), the common forward/reverse geometric factor is
\[
K_r(y-x)\,
\mathbf1_{\mathcal K}(\eta+A_x+B_y)\,
\mathbf1_{\mathcal K}(\eta+C_x).
\]
The forward Palm coefficient is
\[
c_e\,\frac{\widetilde a_A\widetilde a_B}{V},
\]
and the reverse coefficient is
\[
c_{\bar e}\,\frac{\widetilde a_C}{V}.
\]
They agree by the emitted algebraic activity identity. The placement transformation has Jacobian one. The ordered-distinct convention gives the stipulated falling factorial for \(2A\), with no division by two.

Unary and retained-slot binary reverses have the analogous equality; rejection fluxes are diagonal. Restriction to the mass cap or an actual invariant class preserves the equality.

The nominal diffusion generator is
\[
\sum_i\operatorname{div}_{q_i}
\bigl(D_{s(i)}(t,q_i)\nabla_{q_i}\bigr)
\]
with precisely the specified block-conormal walls and pair contacts. Its instantaneous symmetry follows from its divergence form. Neither a class normalizer nor a count-dependent hard-core normalizer is evaluated.

### Graph and support

The accepted paired-prefix construction supplies the all-count abstract decoder graph. Rejection channels add only hidden loops.

The radius in (35) satisfies the stronger dilution conditions required by the accepted finite-radius qualitative construction. Therefore every count under the mass cap has strictly feasible configurations, and every finite allowed fine path has positive-probability spatial realization from every feasible starting placement after finite waits.

Only structurally possible rejection branches are included. The tiny radius does not remove their open realizations: releases can create overlap, and a growing retained slot can be placed sufficiently close to a wall to make its attempted replacement fail.

### Existence from touching configurations

The accepted configuration-core estimates supply nominal reflected existence and identification from all feasible configurations, including simultaneous contacts. The same estimates give the short conditional clock moments used in Section 2.

The present Poincaré proof adds a global quantitative estimate to that local theory. It imposes no new reflection convention and no additional physical dynamics.

## 6. Actual event, movement, wall and pair-work costs

Conservation and positive decoder weights give, pathwise,
\[
|Z(t)|_1\le N.
\tag{42}
\]
The total physical chemical intensity, counting every success, failure and null mark, is at most \(L_*/h\). Hence
\[
\boxed{
\mathbb E F_{\rm all}(t)\le\frac{L_*}{h}t,
\qquad
\mathbb E F_{\rm all}(H\tau)\le L_*T.
}
\tag{43}
\]
This proves chemical nonexplosion and pays the entire actual run. Together with the accepted global reflected existence between events, it gives the required full nonexplosion statement.

The continuous movement charges follow directly from the stated characteristics:
\[
\text{particle-time}\le Nt,
\qquad
\text{continuous coordinate quadratic variation}\le9Nt,
\]
\[
\text{perturbing-drift variation}\le\delta Nt,
\qquad
\text{intrinsic-drift variation}\le3\Lambda Nt.
\tag{44}
\]
Successful placements have displacement at most \(\sqrt3\,r\) per event. A channel changes at most four radius contributions, so
\[
\text{placement displacement}\le\sqrt3\,rF_{\rm all},
\qquad
\text{radius-change variation}\le4\rho P_{\max}F_{\rm all}.
\tag{45}
\]

Substituting (43) into your accepted actual push-work inequality gives
\[
\boxed{
\begin{aligned}
\mathbb E[W_{\rm wall}(t)+W_{\rm pair}(t)]
\le C\bigg[
&\rho\left(1+\frac{L_*t}{h}\right)\\
&+\frac{N(1+N)^4(1+\Lambda)^3}
{\kappa^2\rho d_0^7}\,t
\bigg].
\end{aligned}
}
\tag{46}
\]
Every coefficient is polynomially bounded. This holds for every physical \(t\), every admitted policy and every admitted clock decomposition. It pays actual accumulated push lengths, including all contact excursions.

## 7. Universal polynomial and binary accounting

The emitted quantities are obtained in this order:

1. Run the accepted binary kinetic compiler and the fixed-dimensional geometry algorithm.
2. Evaluate \(T,L_*,J,B_*\).
3. Evaluate the rational minimum (35) and square it.
4. Evaluate fixed polynomial transport majorants \(I,W\).
5. Evaluate (37)–(40).

There is no iteration over particles, populations, classes, rank chambers, configuration volumes, or spatial profiles.

The rank sorting, inward flow, and random intermediate configurations appear only in the proof of the universal inequality (1). Their analytical use does not require an implementation of (4), an eroded-container volume, or any \(3n\)-dimensional operation.

Every numerical dependency is a fixed composition of the accepted polynomial bounds and fixed powers. In particular,
\[
\rho^{-1},\quad I,\quad W,\quad h,\quad H,\quad H\tau,\quad\delta^{-1}
\]
are polynomial in \(R_{\rm num}\). For a paired coefficient,
\[
c_e^{-1}=\frac{hq}{b_e}\le\frac h{b_e},
\]
and ordinary coefficient inverses are \(h/b_e\). Activities and decoder entries retain the accepted kinetic bounds.

The universal constants are effectively obtainable by ordinary polynomial-majorant bookkeeping. Start with the explicit majorants of the accepted kinetic, geometry and local-transport constructions; substitute (33)–(40) into the displayed event and work bounds; replace minima by maxima of reciprocal bounds and each ceiling by \(1+\) its argument. This produces a finite polynomial majorant with nonnegative rational coefficients. Its degree and one plus the sum of its coefficients supply universal \(p,C\). The same procedure applied to the rational arithmetic and accepted compiler bit bounds gives
\[
C(1+L+R_{\rm num})^p
\]
for bit work, memory, output size and individual descriptions.

Thus the construction pays \(\rho^{-1}\) explicitly, chooses the final clock after the radius, preserves all original timed marks, and covers the actual untruncated dynamics. **The new Poincaré estimate closes the quantitative transport step needed for the full finite-radius compiler under the accepted premises.**