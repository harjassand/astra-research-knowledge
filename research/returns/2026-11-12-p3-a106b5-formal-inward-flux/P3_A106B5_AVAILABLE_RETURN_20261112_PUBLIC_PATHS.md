I continued the arbitrary-dimensional case. **I have not yet completed the universal compiler or an impossibility proof covering every allowed design.** There is, however, a new general structural result: the admission promise forces a **strictly positive, polynomially conditioned formal inward flux on every species participating in a nonconservative reaction**. This holds for every admitted input, with variable dimension and order.

I also obtained a broader all-time cost certificate using a nonlinear population function, and a polynomial bound for reversible internal service phases. The unresolved operation is converting these ingredients into an actual autonomous elementary network whose reverse initiations and conditional correlations remain controlled.

## 1. A general consequence of the admission promise

Write
\[
M_\omega=\max_{c\text{ an original complex}}\omega\cdot c.
\]

From each reverse pair that changes \(\omega\cdot x\), choose the orientation
\[
y_r\longrightarrow z_r,
\qquad
\Delta_r=\omega\cdot(z_r-y_r)>0,
\]
and put
\[
\nu_r=z_r-y_r.
\]
Let \(\mathcal I\) index these oriented pairs and define
\[
K_\omega=\operatorname{cone}\{\nu_r:r\in\mathcal I\}.
\]

Here the generators of \(K_\omega\) point in the direction of **increasing** \(\omega\)-population.

### Theorem

For every admitted input, **every source and product complex of an \(\omega\)-nonconservative pair belongs to \(K_\omega\)**.

Moreover, every such complex \(c\) has a representation
\[
\boxed{
c=\sum_{r\in\mathcal I}\gamma_r\nu_r,
\qquad
\gamma_r\ge0,
\qquad
\sum_r\gamma_r\le \omega\cdot c\le M_\omega.
}
\tag{1}
\]

The coefficient bound is numerical and explicit. It does not involve a determinant reciprocal, a stationary law, a class decomposition, or a minimum state probability.

### Proof

Let \(Y_i\) be independent Poisson variables with arbitrary means \(c_i>0\). The factorial-moment identity gives
\[
\mathbb E(Y)_{y}=c^y.
\]
Taking expectations in the supplied pointwise drift promise therefore gives
\[
F(c):=\sum_r k_r c^{y_r}\,\omega\cdot(z_r-y_r)\le A
\qquad(c>0).
\tag{2}
\]

For each selected pair, set
\[
\phi_r=k_ra^{y_r}=k_{\bar r}a^{z_r}>0.
\]
Detailed balance lets us rewrite (2) as
\[
F(c)
=
\sum_{r\in\mathcal I}
\phi_r\Delta_r
\left[
(c/a)^{y_r}-(c/a)^{z_r}
\right].
\tag{3}
\]

Suppose some outward source \(y_{r_0}\) lies outside \(K_\omega\). Separation from a finitely generated closed cone supplies \(v\in\mathbb R^d\) such that
\[
v\cdot\nu_r\le0\quad(r\in\mathcal I),
\qquad
v\cdot y_{r_0}>0.
\]
For a sufficiently small \(h>0\), the vector
\[
v'=v-h\omega
\]
still satisfies \(v'\cdot y_{r_0}>0\), while
\[
v'\cdot\nu_r<0
\quad(r\in\mathcal I).
\]

Now set
\[
c_i(t)=a_i e^{t v_i'}.
\]
Every summand in (3) is nonnegative. The selected summand is
\[
\phi_{r_0}\Delta_{r_0}
e^{t v'\cdot y_{r_0}}
\left(1-e^{t v'\cdot\nu_{r_0}}\right)
\longrightarrow\infty.
\]
This contradicts \(F(c(t))\le A\).

Thus every outward source belongs to \(K_\omega\). Its product does too, because
\[
z_r=y_r+\nu_r.
\]
Finally, applying \(\omega\) to any nonnegative conic representation gives
\[
\omega\cdot c=\sum_r\gamma_r\Delta_r.
\]
The conservation weights and stoichiometries are integral, so every \(\Delta_r\ge1\). This proves the coefficient bound in (1). ∎

This applies across arbitrary linkage classes and supports. Conservative and null pairs simply contribute zero to (3).

## 2. A strictly positive inward flux with a paid robustness margin

The conic result can be strengthened into a certificate with **no tiny retained coefficients**.

Assume \(\mathcal I\neq\varnothing\), and define
\[
u=\sum_{r\in\mathcal I}(y_r+z_r),
\qquad
I=\operatorname{supp}u.
\]
Thus \(I\) is exactly the set of species appearing in nonconservative pairs, and
\[
1\le u_i\le2mD\quad(i\in I).
\]

By summing the representations in (1), we obtain
\[
u=\sum_{r\in\mathcal I}\gamma_r\nu_r,
\qquad
\gamma_r\ge0,
\qquad
\sum_r\gamma_r\le2mM_\omega.
\tag{4}
\]

Set
\[
q=8mD,
\qquad
\widehat\gamma_r=
\frac{\lfloor q\gamma_r\rfloor+1}{q}.
\tag{5}
\]
The addition of \(1\) retains **every selected pair**, including pairs with \(\gamma_r=0\). We have
\[
\widehat\gamma_r\ge\frac1q,
\qquad
0<\widehat\gamma_r-\gamma_r\le\frac1q.
\]

Put
\[
v=\sum_r\widehat\gamma_r\nu_r,
\qquad
S=\sum_r\widehat\gamma_r.
\]
Since \(|\nu_{r,i}|\le D\),
\[
|v_i-u_i|
\le\frac{mD}{q}
=\frac18.
\]
Consequently,
\[
\boxed{
v_i\ge\frac78\quad(i\in I),\qquad
v_i=0\quad(i\notin I).
}
\tag{6}
\]
Also,
\[
S\le2mM_\omega+\frac1{8D}\le3mM_\omega.
\tag{7}
\]

Reversing the selected reactions gives the formal inward flux
\[
-\sum_r\widehat\gamma_r\nu_r=-v.
\]

It has an explicit perturbation margin. Take
\[
\delta_0=\frac1{16DS}.
\tag{8}
\]
For arbitrary independent multipliers
\[
\rho_r\in[1-\delta_0,1+\delta_0],
\]
we have
\[
\begin{aligned}
\sum_r\widehat\gamma_r\rho_r\nu_{r,i}
&\ge v_i-\delta_0\sum_r\widehat\gamma_r|\nu_{r,i}|\\
&\ge\frac78-\delta_0DS\\
&=\frac{13}{16}
\qquad(i\in I).
\end{aligned}
\tag{9}
\]

Thus the reversed formal flux decreases **every participating coordinate**, uniformly throughout this box.

All conditioning is paid:
\[
\max_r\widehat\gamma_r\le3mM_\omega,
\qquad
\max_r\widehat\gamma_r^{-1}\le8mD,
\qquad
\delta_0^{-1}\le48mDM_\omega.
\tag{10}
\]
Since \(M_\omega\le D\sum_i\omega_i\le W^2\), these imply
\[
\max_r\widehat\gamma_r\le3W^3,\qquad
\max_r\widehat\gamma_r^{-1}\le8W^2,\qquad
\delta_0^{-1}\le48W^4.
\tag{11}
\]

### Binary computation

Finding (4) is a rational linear-feasibility problem with polynomially many variables and constraints. Its matrix entries have magnitude at most \(D\), and its right-hand side has entries at most \(2mD\). A deterministic rational linear-programming algorithm can find a certificate with polynomial bit work; no optimization oracle is being assumed.

A basic rational certificate may have a large denominator, but its denominator has polynomial bit length. The rounding operation (5) removes that denominator from every reciprocal coefficient bound. The representation remains a list of at most \(m\) rational numbers.

This distinction matters under the resource contract: a large denominator need not be expanded into that many physical intermediates.

### Why this is still a formal certificate

The coefficients in (9) are prescribed flux weights. Actual mass-action currents contain different source propensities.

For example, the physical expression
\[
\sum_r \widehat\gamma_r\,\lambda_r(z)\,\nu_r
\]
need not have the sign of
\[
\sum_r \widehat\gamma_r\nu_r.
\]
Some \(\lambda_r(z)\) may be zero, and others may differ by unbounded factors.

Therefore, \(\delta_0\) is the tolerance of the **algebraic flux certificate**. It is not yet a valid output tolerance for a physical compiler.

## 3. Consequences for structure, logarithmic affinities, and actual reachability

### An \(R\)-only conservative preprocessing rule

Let
\[
S_R=\operatorname{span}_{\mathbb R}\{z_r-y_r:r\in R\}.
\]
Every linkage class of the finite complex graph lies in a single coset \(c+S_R\).

If that coset is nonzero, meaning \(c\notin S_R\), then **every reaction in that linkage class must conserve the supplied \(\omega\) for every admitted numerical input**.

Indeed, a nonconservative endpoint would belong to \(K_\omega\subset S_R\), contradicting its coset.

This gives a polynomial-bit preprocessing operation depending only on \(R\): rational linear algebra separates automatically conservative linkage classes from the zero-coset classes where nonconservative behavior can occur. The zero-coset part can still have cyclic interactions, so this is not yet a complete resource decomposition.

The same conic theorem applies after restriction to any reaction-closed species set. In particular, the Boolean reaction closure of each original source support can be computed by at most \(d\) support-expansion rounds. There are only \(m\) source closures to examine. These are support calculations; they do not replace the actual enabled-state graph.

### A paid affinity bound

For every real vector \(\ell\), equation (1) implies
\[
\boxed{
c\cdot\ell
\le
M_\omega\max_{r\in\mathcal I}(\nu_r\cdot\ell)_+
}
\tag{12}
\]
for every nonconservative complex \(c\).

Thus, if every outward nonconservative affinity satisfies
\[
\nu_r\cdot\ell\le\eta,
\]
then
\[
c\cdot\ell\le M_\omega\eta.
\tag{13}
\]
For concentrations \(x_i=a_i e^{\ell_i}\), this says
\[
\frac{x^c}{a^c}\le e^{M_\omega\eta}.
\tag{14}
\]

There is also a direct version for the ordinary paired-prefix lift. Give every fine species an arbitrary logarithmic coordinate \(\ell_s\). Suppose:

- every hidden reaction has absolute affinity at most \(\eta\);
- every outward nonconservative central reaction has affinity at most \(\eta\).

A hidden assembly word has length at most \(D+1\), so
\[
\left|\ell_{C_y}-y\cdot\ell_{\rm orig}\right|
\le(D+1)\eta.
\]
Hence
\[
\nu_r\cdot\ell_{\rm orig}\le(2D+3)\eta,
\]
and (12) yields
\[
\boxed{
\ell_{C_y}
\le
\bigl[(D+1)+(2D+3)M_\omega\bigr]\eta.
}
\tag{15}
\]

The loss in (15) is polynomially paid. This statement does not assume hidden equilibrium.

Its stochastic limitation is precise: **a large affinity does not necessarily carry a large current**. Both fluxes of the pair witnessing that affinity can be tiny. Equation (15) does not yet control occupation of a different, heavily populated pending species, or the correlations created by predictable faults.

### Why the formal drain does not supply an enabled controller

Let
\[
n_r=q\widehat\gamma_r=\lfloor q\gamma_r\rfloor+1.
\]
Then
\[
\sum_r n_r\le17m^2DM_\omega.
\tag{16}
\]

The reversed multiset can be executed from the buffer
\[
b=\sum_r n_r z_r.
\tag{17}
\]
Any ordering works: the initial state contains all reactants that will be consumed, even without crediting intermediate products. The final state is
\[
\sum_r n_r y_r,
\]
and every coordinate in \(I\) has decreased.

The numerical bounds are
\[
\sum_r n_r\le17W^5,
\qquad
|b|_1\le17W^6.
\tag{18}
\]

But this does not satisfy the compiler contract:

- The buffer in (17) is not present in canonical initialization.
- Its payload and the expanded word can depend on numerical input.
- Writing the word out can cost polynomially in \(\omega\), rather than polynomially in its bit length.
- An elementary reversible implementation must also pay the reverse initiations of its intermediate stages.

Even the admitted scalar pair \(X\rightleftarrows2X\) illustrates the enabling distinction. Its inward vector is \(-X\), but the reaction \(2X\to X\) cannot remove the last molecule. The classes \(\{0\}\) and \(\{1,2,\ldots\}\) remain distinct.

The formal flux therefore gives a conditioned direction in which a sufficiently supplied system can move. It does not authorize a reset or a transition unavailable in the actual graph.

## 4. A nonlinear certificate that pays the entire physical run

A useful extension of the common linear-drift approach is now checked.

Suppose an elementary realization has **no \(2\to2\) channels**, including binary null channels. Let \(n(z)=|z|_1\). Suppose a rational positive semidefinite matrix \(M\) satisfies
\[
n(z)^2\le z^\top Mz\le M_*n(z)^2
\qquad(z\ge0).
\]
Define
\[
V(z)=1+z^\top Mz,\qquad G(z)=\sqrt{V(z)}.
\]
Assume the entire instantaneous fault box satisfies
\[
L_tV(z)\le2C\sqrt{V(z)}.
\tag{19}
\]

Then square-root concavity gives
\[
L_tG(z)\le C.
\tag{20}
\]
Also,
\[
|G(z+\nu)-G(z)|
\le\sqrt{\nu^\top M\nu}.
\tag{21}
\]
Thus \(G\) has bounded jumps whenever the finitely many jump norms have a paid bound \(J_*\).

These pointwise statements apply directly to predictable, history-dependent faults.

### Paying every firing

Write \(F_0,F_1,F_2\) for the numbers of firings with source molecularity \(0,1,2\). Every source-two firing decreases physical population by at least one. Therefore,
\[
F_{\rm all}(t)\le n_0+3F_0(t)+2F_1(t).
\tag{22}
\]

With physical coefficients at most one and faults in \([1/2,3/2]\),
\[
\mathbb EF_{\rm all}(t)
\le
n_0+\frac92m_ft+
3m_f\int_0^t\mathbb En_s\,ds.
\tag{23}
\]
Equation (20) gives
\[
\mathbb En_t\le G(z_0)+Ct,
\]
so
\[
\boxed{
\mathbb EF_{\rm all}(t)
\le
n_0+\frac92m_ft+
3m_fG(z_0)t+\frac32m_fCt^2.
}
\tag{24}
\]

For the martingale
\[
\mathcal M_t
=
G(Z_t)-G(z_0)-\int_0^tL_sG(Z_s)\,ds,
\]
the expected quadratic variation is at most
\[
J_*^2\,\mathbb EF_{\rm all}(t).
\]
Doob’s inequality consequently gives
\[
\boxed{
\mathbb E\sup_{s\le t}(1+n_s)
\le
1+G(z_0)+Ct+
2J_*\sqrt{\mathbb EF_{\rm all}(t)}.
}
\tag{25}
\]

Equations (24)–(25) are exactly quadratic firing growth and linear expected population-supremum growth. Null and hidden events are included in (22)–(24).

Affine domination of upward population jumps supplies nonexplosion first. Applying the argument at finite stopping levels then removes any circular assumption about the moments being proved.

### An independently checked example

For the shared-prefix realization
\[
2X\mathrel{\mathop{\rightleftarrows}^{\alpha}_{K}}S,
\qquad
X+S\mathrel{\mathop{\rightleftarrows}^{\chi}_{K}}T,
\qquad
S\mathrel{\mathop{\rightleftarrows}^{p}_{q}}T,
\]
with decoder \(P=(1,2,3)\), take
\[
M=
\begin{pmatrix}
8&1&4\\
1&7&8\\
4&8&12
\end{pmatrix}.
\tag{26}
\]
Its leading principal minors are \(8,55,100\), and
\[
n^2\le z^\top Mz\le12n^2.
\]

For the forward reaction vectors,
\[
\begin{aligned}
M(-2,1,0)^\top&=(-15,5,0)^\top,\\
M(-1,-1,1)^\top&=(-5,0,0)^\top,\\
M(0,-1,1)^\top&=(3,1,4)^\top.
\end{aligned}
\tag{27}
\]
The corresponding squared jump norms are \(35,5,3\), so \(J_*<6\).

Under
\[
\alpha\le\chi/4,\qquad
\chi\le K,\qquad
p\le K/4,\qquad
q\le K,\qquad
K\ge18p^2/q,
\tag{28}
\]
the whole independent \([1/2,3/2]\) box satisfies
\[
L_tV
\le
10^9\left(
1+K+\frac{K^2}{q}+\frac{K^6}{\alpha^2q^3}
\right).
\tag{29}
\]

The decisive cubic cancellation is
\[
15\alpha\,x^2s-5\chi\,x^2s
\le-\frac54\chi\,x^2s.
\]
The remaining auxiliary quadratics are controlled using
\[
12pst\le2Ks^2+\frac{18p^2}{K}t^2
\le2Ks^2+qt^2.
\]
After the remaining Young inequalities, one obtains
\[
L_tV
\le
-15\alpha x^3+
\frac{1000K^2}{q}x^2+
729K+\frac{36K^2}{q},
\]
which implies (29).

Exact nominal balance is retained by the uniform-prefix choices
\[
\widetilde a_S=\theta U^{-2}a^2,\qquad
\widetilde a_T=\theta U^{-3}a^3,
\]
\[
\alpha=K\theta/U^2,\quad
\chi=K/U,\quad
p=Qk_+U^2,\quad
q=Qk_-U^3.
\]
Increasing \(K\) to satisfy (28), followed by common normalization, has polynomial cost.

This example remains within the already solved scalar scope. Its contribution is a checked **nonlinear bounded-drift mechanism**. I have not constructed a matrix or another bounded-jump function with comparable guarantees for arbitrary \(R\).

There is also a restriction on this approach: on an isolated inactive aggregation face \(2A\rightleftarrows S\), a globally bounded-drift quadratic norm must annihilate the aggregation direction,
\[
M(e_S-2e_A)=0.
\]
Thus a universal quadratic construction must preserve inactive resource directions exactly. A generic positive-definite choice cannot provide the required global certificate.

## 5. Reversible internal service phases can be conditioned polynomially

A separate operation removes a possible exponential loss inside a proposed controller.

Consider a tagged particle moving through \(J_s\) private internal species. Until absorption, every reaction consuming that tag is unary. Suppose the internal transitions are detailed balanced with activities in
\[
[G^{-1},G],
\]
every positive internal or absorption coefficient is at least \(r_->0\), and total marked outgoing rate at each internal state is at most \(R_s\).

Let \(h_i\) be the nominal mean absorption time. Then
\[
\boxed{
\max_i h_i\le H_{\rm svc}:=\frac{J_s^2G^2}{r_-}.
}
\tag{30}
\]

To prove this, attach an absorbing sink. Every positive conductance along a simple path to the sink is at least \(r_-/G\). If \(i_*\) maximizes \(h_i\), path Cauchy–Schwarz and the killed Poisson equation give
\[
h_{i_*}^2
\le\frac{J_sG}{r_-}\mathcal E_{\rm killed}(h),
\qquad
\mathcal E_{\rm killed}(h)
=\sum_i\widetilde a_i h_i
\le J_sG h_{i_*}.
\]
Canceling \(h_{i_*}\) proves (30).

Under arbitrary predictable faults,
\[
L_th\le-1+\delta R_sH_{\rm svc}.
\]
Consequently,
\[
\delta\le\frac1{2R_sH_{\rm svc}}
\]
gives
\[
\mathbb E[\sigma\mid\text{entry history}]\le2H_{\rm svc},
\qquad
\mathbb EJ_{\rm service}\le3R_sH_{\rm svc}.
\tag{31}
\]
Conditional blocks of length \(4H_{\rm svc}\) give geometric survival tails, hence polynomial bounds for every fixed service-time and event-count moment.

A desired exit probability requires an additional choice. Mean absorption alone does not suffice: a reversible line with a unit killing rate at every vertex can have exponentially small probability of reaching a specified terminal exit.

For an added service, make the total absorption rate at each internal state at most
\[
\beta\le\frac1{24H_{\rm hit}},
\qquad
H_{\rm hit}=\frac{J_s^2G^2}{r_-}.
\]
If a desired exit has coefficient at least \(b_{\min}\), then the same conditional hitting argument gives
\[
\boxed{
\Pr(\text{desired exit}\mid\text{entry history})
\ge
\frac{b_{\min}}{12(R_s+\beta)}.
}
\tag{32}
\]
All quantities can have polynomial reciprocals. Reverse exit coefficients can be assigned by the exact detailed-balance ratio.

The protection hypothesis is essential. An unbounded binary reaction consuming the tag is a competing exit and must be included in the analysis. Equations (30)–(32) pay service **after entry**; they do not pay the reverse binary initiations that create those entries.

## 6. The remaining all-time operation

The strongest unresolved issue is now more specific than a conditioning problem.

The conic construction supplies a robust inward **vector sum**. The internal-service construction supplies paid **conditional completion**. The nonlinear certificate shows one way to pay **actual whole-run costs**. What is missing is a polynomial-size, \(R\)-only physical construction—or a direct estimate for an existing construction—that connects these three statements.

One sufficient target for a realization without \(2\to2\) channels would be
\[
\boxed{
\sup_{\text{admitted faults}}
\mathbb E F_{\rm nc}(t)
\le C_{\rm nc}(1+t),
\qquad
C_{\rm nc}\le C W^p,
}
\tag{33}
\]
where \(F_{\rm nc}\) counts observed firings that change \(\omega\cdot PZ\).

This would pay all physical costs. Pathwise,
\[
\sup_{s\le t}\omega\cdot PZ_s
\le N_0+M_\omega F_{\rm nc}(t).
\]
Every decoder column is nonzero and \(\omega_i\ge1\), so
\[
|Z_s|_1\le\omega\cdot PZ_s.
\]
Thus (33) gives the required linear expected population supremum. Substitution into the exact count bound (23) then pays **every** hidden, null, unsuccessful, and observed firing quadratically in time. Since \(H\tau\) is already polynomially paid, the horizon firing bound follows too.

I have not proved (33), or an alternative common-drift estimate sufficient for the same purpose, for arbitrary input networks.

The central difficulty remains the conditional fine distribution. Hidden reactions conserve decoded mass exactly, but predictable faults can drive their internal distribution. The accepted thinning inequality controls nonconservative activity on the hidden-equilibrium subspace; extending it to the actual driven conditional distribution requires an additional argument. A large-affinity alternative such as (15) does not supply that argument by itself.

I also checked the recent measurable-rate deterministic permanence work. Its stated scope covers deterministic positive trajectories in a compact rate box, while §9.5 leaves effective extraction of its general geometric constants open; its stochastic comparison supplies a lower recovery bound. These statements do not provide the stochastic upper population and firing estimates required here. [hexagonmath.org](https://hexagonmath.org/pdf/2610.00321v1?utm_source=chatgpt.com) The established single-linkage binary recurrence theorem likewise has additional structural hypotheses and does not give this adaptive, universally polynomial compilation result. 

**The universal contract remains unresolved in this continuation.** The principal proved addition is the full-support inward-flux certificate (5)–(11), together with its fine affinity consequence (15). It eliminates an unpaid coefficient-conditioning issue, but I cannot yet turn its formal margin into a physical generator margin while retaining the required graph, initialization, exact balance, and all-time adaptive costs.
---

## Visible activity excerpts

Refined the source-pair library

I’m continuing. The conic argument now yields a strictly positive inward formal flux whose coefficients and perturbation margin have explicit polynomial bounds. I also checked a recent result on deterministic systems with measurably varying rates; its quantitative barrier data remain unspecified, so it does not supply the stochastic cost bound needed here. The remaining step is to realize or exploit the flux without supplying a buffer or leaving reverse initiations unpaid.

The new flux margin has passed an independent check, including retaining every nonconservative pair with a positive coefficient. The physical gap is precise: the coefficients multiply different source propensities, so their inward vector sum is not yet a generator inequality. A separate nonlinear population certificate also survived a full rate-box audit, but only for a scalar lift; it has not extended the universal result.

The expanded activity also displayed many short work labels and helper updates; those and the expanded helper contents are not captured here. Thirteen subagents were shown. Outputs: no outputs yet; archive availability is unknown.

Exact already-held full question: P3_FULL_DETAILED_BALANCED_AFTER_THINNING_AND_RESOURCE_COMPOSITION_PRO_20261112.txt, 15654 ASCII bytes, SHA-256 bc056150 (prefix), in this same directory. Latest user-role continuation bb92c873-7df8-4889-9ede-670bfeade01a says “continue”. Final a106b512-7a23-5d0d-a260-bbdb1d9e2307. Chat 6af3030c-e834-83ec-b294-ad6a7f60aa46; UI showed Pro. UI ending matches the copied final; complete database-byte identity is not asserted.
