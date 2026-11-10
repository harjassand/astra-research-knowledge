# P2 Xi completed return — Fourier escape continuation

Source https://chatgpt.com/c/6af1715f-dbc4-83ec-a58c-3bca5bb0fe65; response 64106fb8-69fe-4cdd-a750-02a5e3dbe4b6; latest human continuation df2331cf-6680-475e-b7ae-b0019a1e9a4d (“continue”).
Exact question reference: work/astra-renewed-pro-programmes-20261103/P2_FULL_BODY_FORCE_AFTER_E155_XI_20261110.txt; source SHA256 5b0762ae52d59ca799ac17cde6e13761870cd0d0efe851a1306fc03132875b76. Model at generation: GPT-6 Standard Extra High. No ZIP identified.
Native read is capped at 20,000 characters and ends within a word; the remaining visible tail below is transcribed with formatting reconstructed.

## Available visible activity

Previous “please continue”: Researched controllability limits and tested invariant structures. Analyzed polarization transfer, strain mechanisms, realizability, and Fourier squeezing constraints. Assessed squeezing mechanisms. Searched the web. Analyzed commutator-induced mode contraction.

Latest “continue” — worked for 20m 56s: Developed rigorous progress through invariant and mode analysis. Analyzed invariant subspaces, contraction, mixing, and Fourier modal leakage. Searched the web. Proved one-sided Fourier leakage for Euler linearization. Strengthened modal and Fourier leakage analysis. Developed Fourier observability and leakage analysis. Searched the web.

ChatGPT said: The frequency-raising determinant leads to a stronger finite-dimensional statement: for every prescribed finite Fourier preparation space, a finite set of iterated physical-generator responses must escape that space, with a word-length bound and an exact rational positive-definiteness certificate. I’m checking what this proves about controllability—and, importantly, what it does not prove about L2 contraction.

Assessed algebraic consequences and finite-mode leakage. Developed finite leakage.

## Native response, first 20,000 characters

# P2 — Further continuation: Fourier escape and the limits of linear squeezing

**The full common additive-force compiler remains open.** This continuation establishes a stronger algebraic property of the twelve physical Euler generators: they have no nonzero finite-Fourier invariant subspace, and their individual frequency-raising interactions satisfy an explicit quantitative lower bound.

This removes a potential finite-dimensional obstruction to the weighted squeezing programme. It does not establish squeezing, because transferring a perturbation to higher Fourier frequencies is different from reducing its total \(L^2\) energy.

## 1\. Exact one-sided Fourier escape theorem

Let \(\kappa=2\pi\) and write

\[
\mathcal L_Fv
=\mathbb P[(F\cdot\nabla)v+(v\cdot\nabla)F].
\]

Complexify the divergence-free Fourier space for the calculation, and define

\[
F^+_{ij}(x)=e_i e^{i\kappa x_j},
\qquad i\ne j.
\]

These are not additional real actuators: each is the complex linear combination \(F^c_{ij}+iF^s_{ij}\) of two of the permitted twelve fields.

For a Fourier coefficient \(v_ke^{i\kappa k\cdot x}\), where \(k\ne0\) and \(k\cdot v_k=0\),

\[
\mathcal L_{F^+_{ij}}
(v_ke^{i\kappa k\cdot x})
=
i\kappa T^+_{ij}(k)v_k\,
e^{i\kappa(k+e_j)\cdot x},
\]

where

\[
\boxed{
T^+_{ij}(k)
=
P_{k+e_j}
\bigl(k_iI+e_ie_j^\top\bigr)
\big|_{k^\perp}.
}
\tag{1}
\]

The Leray projector at zero frequency is interpreted as zero.

### Exact transverse determinant

Suppose \(k_i\ne0\), \(i\ne j\), and put

\[
r=|k|^2,\qquad p=k+e_j.
\]

For \(r\ge2\), \(p\ne0\)\. The determinant of (1), between the two-dimensional divergence-free polarization planes, satisfies

\[
\boxed{
\left|\det_{\perp}T^+_{ij}(k)\right|
=
\frac{k_i^2(r-1)}{\sqrt r\,|k+e_j|}.
}
\tag{2}
\]

To verify this, set

\[
A=k_iI+e_ie_j^\top.
\]

Since \(i\ne j\),

\[
\det A=k_i^3,
\qquad
A^{-\top}k=\frac{k-e_j}{k_i}.
\]

The two-dimensional area transformation from \(k^\perp\) to \(p^\perp\) is therefore

\[
\frac{\left|p\cdot(\det A)A^{-\top}k\right|}
{|p||k|}
=
\frac{k_i^2|(k+e_j)\cdot(k-e_j)|}{|p||k|},
\]

giving (2).

Because \(r\) is an integer, \(r\ge2\) implies \(r-1>0\)\. Hence every such frequency-raising map with \(k_i\ne0\) is **injective on the entire two-dimensional divergence-free polarization space**\.

This is stronger than showing that some polarization happens to escape.

### Explicit quantitative bound

Choose \(i\) so that

\[
|k_i|=\max_{a=1,2,3}|k_a|.
\]

Then \(k_i^2\ge r/3\)\. Since

\[
\|T^+_{ij}(k)\|\le\sqrt r+1,
\qquad
|k+e_j|\le\sqrt r+1,
\]

the smallest singular value obeys, for every \(r\ge2\),

\[
\begin{aligned}
s_{\min}(T^+_{ij}(k))
&\ge
\frac{\sqrt r(r-1)}
{3(\sqrt r+1)^2}\\
&\ge\frac{\sqrt r}{18}.
\end{aligned}
\tag{3}
\]

The remaining case \(r=1\) is explicit. If \(k=\pm e_i\), then \(v_k\) has its two components in the directions \(j,\ell\ne i\)\. The raising map associated with \(j\) kills only the \(e_j\) polarization, while that associated with \(\ell\) kills only the \(e_\ell\) polarization. Consequently,

\[
\|T^+_{ij}(k)v_k\|^2+
\|T^+_{i\ell}(k)v_k\|^2
=\|v_k\|^2.
\]

Combining the two cases gives the all-frequency estimate

\[
\boxed{
\sum_{i\ne j}
\|T^+_{ij}(k)v_k\|^2
\ge
\frac{|k|^2}{324}\|v_k\|^2.
}
\tag{4}
\]

Since the shift \(k\mapsto k+e_j\) is injective for each fixed \(j\), Fourier orthogonality yields

\[
\boxed{
\sum_{i\ne j}
\|\mathcal L_{F^+_{ij}}v\|_2^2
\ge
\frac1{324}\|\nabla v\|_2^2
}
\tag{5}
\]

for every divergence-free mean-zero trigonometric polynomial \(v\), with extension to \(H^1\)\.

Equation (5) is a *one-sided* version of the earlier physical-generator coercivity theorem. Unlike the earlier sine–cosine sum, it uses only frequency-raising complex shifts.

## 2\. No finite-Fourier invariant subspace

### Theorem

There is no nonzero finite-dimensional subspace consisting of finite-Fourier-support divergence-free fields that is invariant under all twelve real physical Euler generators.

**Proof.** Suppose such a subspace \(X\) exists. Choose a basis and let \(K\subset\mathbb Z^3\setminus\{0\}\) be the finite union of their Fourier supports.

Select \(k\in K\) maximizing

\[
k_1+k_2+k_3.
\]

Choose \(v\in X\) with \(v_k\ne0\)\. By (4), at least one pair \(i\ne j\) satisfies

\[
T^+_{ij}(k)v_k\ne0.
\]

But \(k+e_j\notin K\), since its coordinate sum is larger than the maximum.

The coefficient of \(\mathcal L_{F^+_{ij}}v\) at \(k+e_j\) is nonzero. This contradicts invariance of the complexification of \(X\) under \(F^c_{ij}+iF^s_{ij}\)\.

Therefore \(X=\{0\}\)\.

### What this establishes

The twelve physical generators cannot collectively trap a nonzero finite set of Fourier modes, even if the trapped space were allowed to rotate its basis internally.

This strengthens the earlier common-kernel theorem\:

\[
\bigcap_F\ker\mathcal L_F=\{0\}.
\]

A family can have no common kernel and still possess nontrivial invariant finite-dimensional subspaces. The new result excludes those finite-Fourier invariant subspaces as well.

It does **not** exclude invariant spaces with infinite Fourier support, nor does it prove weak mixing, terminal energy contraction or the weighted condition (WE).

## 3\. Finite-jet observability with a computable certificate

The preceding escape theorem can be strengthened from an algebraic statement into a finite, quantitative certificate.

Let \(K\subset\mathbb Z^3\setminus\{0\}\) be any finite set of Fourier wavevectors, and let \(E_K\) be the complex divergence-free space supported on \(K\)\. Write

\[
D=\dim_{\mathbb C}E_K=2|K|.
\]

Let \(P_K\) be the orthogonal Fourier projection and \(Q_K=I-P_K\)\.

Normalize the six raising generators by

\[
C_{ij}=\kappa^{-1}\mathcal L_{F^+_{ij}},
\qquad i\ne j.
\]

Every Fourier matrix coefficient of \(C_{ij}\) is a Gaussian rational: its entries lie in \(\mathbb Q(i)\)\.

For a word \(\omega=(a_1,\ldots,a_m)\) in these six generators, let

\[
C_\omega=C_{a_m}\cdots C_{a_1}.
\]

Define the finite-jet escape Gramian

\[
\boxed{
\mathsf G_K=
\sum_{m=1}^{D}
\ \sum_{\omega\in\{1,\ldots,6\}^m}
P_KC_\omega^*Q_KC_\omega P_K
\big|_{E_K}.
}
\tag{6}
\]

Although the ambient Fourier space is infinite, this sum is finite. A word of length \(m\) changes a Fourier index by at most \(m\) in each coordinate.

### Theorem — Positive finite-jet Gramian

For every finite \(K\),

\[
\boxed{\mathsf G_K\succ0.}
\tag{7}
\]

Equivalently, there is a strictly positive rationally computable constant \(c_K\) such that

\[
\boxed{
\sum_{m=1}^{D}\sum_{|\omega|=m}
\|Q_K C_\omega v\|_2^2
\ge c_K\|v\|_2^2
\quad\text{for all }v\in E_K.
}
\tag{8}
\]

The maximum required generator-word length is at most \(D\)\. It does not come from an unbounded search.

### Proof

Define

\[
Z_m=
\left\{
v\in E_K:
Q_KC_\omega v=0
\text{ for all words }|\omega|\le m
\right\},
\]

with \(Z_0=E_K\)\.

These are nested complex-linear subspaces\:

\[
E_K=Z_0\supseteq Z_1\supseteq Z_2\supseteq\cdots.
\]

Suppose \(Z_m=Z_{m+1}\ne\{0\}\)\.

For any \(v\in Z_m\) and any generator \(C_a\), the first-order condition gives \(C_av\in E_K\)\. Furthermore, for every word \(\omega\) of length at most \(m\),

\[
Q_KC_\omega(C_av)=0,
\]

because the concatenated word has length at most \(m+1\)\.

Thus \(C_av\in Z_m\)\. Therefore \(Z_m\) is a nonzero finite-Fourier invariant subspace under all six generators.

This contradicts Section 2.

Every nonzero stage of the descending sequence must consequently decrease its dimension strictly. Starting from dimension \(D\), the sequence reaches zero by stage \(D\)\:

\[
Z_D=\{0\}.
\]

But \(Z_D\) is precisely the kernel of the positive-semidefinite Gramian (6). Therefore \(\mathsf G_K\) is positive definite.

### Exact rational lower bound

Choose any rational Fourier polarization basis for \(E_K\)\. Let \(G\) denote the matrix of \(\mathsf G_K\) and \(G_0\) the corresponding positive-definite \(L^2\) Gram matrix.

Both have entries in \(\mathbb Q(i)\); their Hermitian determinants and traces below are rational.

A fully explicit lower bound is

\[
\boxed{
c_K=
\frac{\det G/\det G_0}
{\bigl[\operatorname{tr}(G_0^{-1}G)\bigr]^{D-1}}
>0.
}
\tag{9}
\]

Indeed, if \(\lambda_1,\ldots,\lambda_D\) are the positive generalized eigenvalues, then

\[
\lambda_{\min}
=\frac{\prod_a\lambda_a}
{\prod_{a\ne\min}\lambda_a}
\ge
\frac{\prod_a\lambda_a}
{(\sum_a\lambda_a)^{D-1}}.
\]

No floating-point eigenvalue approximation is needed.

### What the finite computation costs

For the cube \(|k|_\infty\le N\), excluding zero,

\[
D=2\bigl((2N+1)^3-1\bigr).
\]

The direct algorithm evaluates at most

\[
\sum_{m=1}^D6^m<6^{D+1}
\]

generator words. All intermediate wavevectors lie in

\[
|k|_\infty\le N+D.
\]

Each word is evaluated by rational Fourier multiplication and the rational Leray matrices

\[
P_k=I-\frac{kk^\top}{|k|^2}.
\]

Constructing the Gramian, taking determinants and testing positive definiteness therefore requires finitely many exact integer and rational operations, with all Fourier dimensions and word counts known before computation.

For a concrete complete-bit envelope, put \(R=N+D\) and

\[
Q=\prod_{\substack{|p|_\infty\le R\\p\ne0}}|p|^2.
\]

Each normalized word of length at most \(D\) has rational coefficient denominators dividing \(Q^D\)\. Consequently, the Gramian entries can be stored with a common denominator \(Q^{2D}\)\. Standard integer matrix arithmetic then gives a conservative bit-work and memory bound of

\[
\boxed{
2^{1000(D+1)^3(R+2)^3
\lceil\log_2(R+3)\rceil}
}
\tag{10}
\]

for this direct construction, including exact positive-definiteness and the rational lower bound.

This bound is enormous but finite and computable. It pays for the exponentially many generator words rather than hiding them in a qualitative observability argument.

**Result\:** Every finite Fourier preparation space admits a finite, rationally certified set of physical Euler generator interactions that necessarily creates some response outside that space.

## 4\. A minimax equivalence for the fast-return construction

There is a second consequence of the accepted E155 transference theorem.

Previously, weighted Euler squeezing was established as a **sufficient** route to common-force contraction. Within the fast-return scaling, it is also an asymptotically **necessary** condition.

### Theorem — Uniform worst-case singular limit

Fix \(M,\nu>0\) and one smooth zero-return background path \(w\in\mathcal W\)\.

For each sufficiently small \(\delta>0\), prescribe the ideal fast-return force

\[
f_\delta(t)=
\delta^{-2}[w_s+\mathcal B(w,w)](t/\delta)
-\nu\delta^{-1}\Delta w(t/\delta).
\]

Define the worst-case endpoint energy norm

\[
\mathfrak R_\delta(w;M)=
\sup_{\substack{\|U_0\|_{H^1}\le M\\
U\text{ admitted Leray--Hopf}}}
\|U(\delta)\|_2,
\]

with zero additive disturbance.

Then

\[
\boxed{
\lim_{\delta\downarrow0}
\mathfrak R_\delta(w;M)
=
M\|S_w(1)\|_{H^1\to L^2}
=
M\|S_w(1)J\|_{2\to2}.
}
\tag{11}
\]

This equality holds without assuming uniqueness of three-dimensional weak solutions.

### Proof

Let \(E_w(\delta)\) be the explicit all-weak comparison error from E155. For fixed \(w,M,\nu\),

\[
E_w(\delta)=O_w(\sqrt\delta).
\]

For every initial datum and every corresponding admitted weak realization,

\[
\|U(\delta)-S_w(1)U_0\|_2\le E_w(\delta).
\]

Taking suprema and using the triangle inequality gives

\[
\mathfrak R_\delta(w;M)
\le M\|S_wJ\|+E_w(\delta).
\]

Conversely, a Leray–Hopf realization exists for each admissible initial datum and the prescribed force. For any such realization,

\[
\|U(\delta)\|_2
\ge\|S_w(1)U_0\|_2-E_w(\delta).
\]

Taking the supremum over initial data gives

\[
\mathfrak R_\delta(w;M)
\ge M\|S_wJ\|-E_w(\delta).
\]

Therefore

\[
\boxed{
\left|
\mathfrak R_\delta(w;M)-M\|S_wJ\|
\right|
\le E_w(\delta),
}
\tag{12}
\]

and (11) follows.

### Consequence for varying return paths

Suppose we choose a sequence of paths \(w_n\), durations \(\delta_n\), and rational force approximations with errors \(E_n\to0\)\.

Equation (12), applied separately to each path, implies

\[
\boxed{
\mathfrak R_{\delta_n}(w_n;M)\to0
\quad\Longleftrightarrow\quad
\|S_{w_n}J\|_{2\to2}\to0.
}
\tag{13}
\]

This equivalence assumes that the *actual explicit comparison errors* \(E_n\) tend to zero; merely requiring \(\delta_n\to0\) is insufficient when the strain budgets of \(w_n\) grow.

It continues to hold for rational approximations whose integrated residual errors enter those same vanishing bounds. Allowing a uniformly bounded additive disturbance does not change the limiting equivalence, because zero disturbance is included and its contribution to the short-pulse comparison tends to zero.

**Interpretation\:** within this singular fast-return regime, nonlinear three-dimensional dynamics cannot provide extra universal contraction that is invisible to the homogeneous weighted Euler propagator, once the transference error is negligible.

This makes (WE) an exact limiting criterion for this particular programme, rather than merely an artifact of an overly restrictive proof technique.

It does not make (WE) necessary for the original question. A control exploiting viscosity at leading order, with no vanishing-error inviscid approximation, could succeed by a different mechanism.

## 5\. From formal Fourier derivatives to actual admissible Euler paths

The finite-jet theorem concerns derivatives of solution operators. It can also be converted into a statement about genuine, finite-duration control paths—not merely formal operator words.

### Theorem — A finite menu of common Fourier-escape paths

For every finite \(K\), there exist at most \(D=2|K|\) rational piecewise-polynomial, zero-return paths

\[
w^{(1)},\ldots,w^{(s)}:[0,1]\to\mathcal W,
\qquad s\le D,
\]

and a positive computable rational \(c'_K\), such that

\[
\boxed{
\sum_{\ell=1}^{s}
\left\|
(I-P_K)S_{w^{(\ell)}}(1)v
\right\|_2^2
\ge c'_K\|v\|_2^2
\quad
(v\in E_K).
}
\tag{13}
\]

Each path uses only the twelve allowed first-harmonic backgrounds, and each could be realized by the accepted fixed 36-field additive-force construction.

### Proof of existence

Let \(\mathscr G\) be the group of operators generated by finite products

\[
e^{t_m\mathcal L_{F_m}}\cdots
e^{t_1\mathcal L_{F_1}},
\qquad t_j\in\mathbb Q,
\]

where \(F_j\) ranges over the twelve real fields. The signs of the rational times are unrestricted.

Suppose a nonzero \(v\in E_K\) satisfies

\[
(I-P_K)Tv=0
\qquad\text{for every }T\in\mathscr G.
\]

Then the linear span of its orbit,

\[
X=\operatorname{span}\{Tv:T\in\mathscr G\},
\]

lies inside the finite-dimensional space \(E_K\)\.

This span is invariant under all rational-time generator flows. Strong continuity and differentiation at zero make it invariant under all twelve physical Euler generators.

That contradicts Section 2.

Therefore, for every nonzero \(v\in E_K\), some \(T\in\mathscr G\) has

\[
(I-P_K)Tv\ne0.
\]

Start with \(V_0=E_K\)\. Select such an operator for a nonzero vector in \(V_0\), and set

\[
V_1=V_0\cap\ker[(I-P_K)T_1].
\]

The dimension decreases. Repeating this construction gives

\[
V_s=\bigcap_{\ell=1}^{s}
\ker[(I-P_K)T_\ell]=\{0\}
\]

after at most \(D\) steps.

Hence the sum of the \(s\) squared exterior norms is strictly positive on the unit sphere of \(E_K\)\. Compactness supplies a positive minimum.

Finally, each exponential \(e^{t\mathcal L_F}\) can be implemented by a smooth rational pulse proportional to \(F\) with prescribed rational integral \(t\)\. Concatenating these pulses gives a rational piecewise-polynomial path that vanishes at both endpoints. The signs are chosen so its homogeneous Euler propagator equals the required product.

This proves (13).

### Effective selection

The theorem has an algorithmic version.

Enumerate finite lists of rational pulse paths of length at most \(D\)\. For each list, use the established finite Fourier/Galerkin/Picard interface to approximate its endpoint propagators on \(E_K\), with a certified operator-error bound.

Test a rational positive-definiteness inequality for the sum of the exterior-output Gramians. Dovetail candidate lists and precision levels so that every individual test is finite.

Because a strictly positive Gramian exists, some finite candidate with sufficient precision passes. The search therefore terminates.

This gives a total finite-arithmetic selector for the finite menu, with a computable uniform resource bound for every specified finite \(K\)\.

The distinction from the full question is important: the theorem supplies **several alternative paths**, together guaranteeing that every initial direction escapes under at least one path. It does not yet supply one path that contracts every initial direction.

## 6\. Why these results do not yet imply universal contraction

The distinction can be made mathematically precise.

Consider the bilateral shift \(T\) on \(\ell^2(\mathbb Z)\)\:

\[
Te_n=e_{n+1}.
\]

For every finite-support space \(E_K\), a sufficiently large power \(T^m\) sends the entire space outside its original support\:

\[
P_KT^mP_K=0.
\]

The shift has no nonzero finite-support invariant subspace. It satisfies stronger Fourier-escape properties than those proved above.

Nevertheless, \(T\) is unitary\:

\[
\|T^mv\|=\|v\|.
\]

For any positive compact diagonal Sobolev weight \(J\),

\[
\boxed{
\|T^mJ\|=\|J\|,
\qquad\text{for every }m.
}
\]

Thus even **perfect simultaneous escape from every original low-frequency mode** does not imply weighted \(H^1\)\-to-\(L^2\) contraction.

This identifies the additional property required of the physical Euler dynamics: not just migration of Fourier support, but reduction of the *velocity amplitude* associated with those migrated modes.

The physical linearized Euler generators are not unitary, so the shift example does not obstruct them. Their stretching can produce either amplification or attenuation. The missing theorem must establish that suitable time-dependent backgrounds make attenuation dominate uniformly on the whole weighted preparation ball.

Alternatively, a construction can retain physical viscosity during the frequency-transfer process. Then Fourier escape becomes useful because the heat semigroup genuinely destroys the high-frequency energy. But that approach must control physical stretching and nonlinear three-dimensional interactions while diffusion operates; the accepted scalar-sector bounds do not yet supply the full result.

## 7\. Relation to the existing controllability results

Nersesyan's linear-test theorem relates finite-dimensional additive controllability of three-dimensional Navier–Stokes equations to controllability of Euler equations linearized about suitable trajectories. Its approximate-controllability conclusion does not establish a single homogeneous propagator contracting every unknown initial condition. citeturn951978search0

Shirikyan's results likewise establish approximate controllability and exact controllability in finite-dimensional projections, rather than the present common-force, all-weak terminal-energy requirement. citeturn951978search2turn951978search5

The results above introduce a different finite-dimensional interface: **universal escape observability for the uncontrolled homogeneous linearized evolution**, with an effective bound on the required generator-word length.

That is meaningful progress toward the operator problem, but it is not equivalent to the controllability assertions in those papers.

## 8\. Final research status

| Result | Status |
|--------|--------|
| Exact transverse determinant for physical frequency-raising maps | Proved |
| Quantitative one-sided all-frequency coercivity | Proved |
| No nonzero finite-Fourier invariant subspace for the twelve physical generators | Proved |
| Finite-jet observability, maximum word length \(2\|K\|\) | Proved |
| Exact-rational Gramian and computable positive lower bound | Constructive |
| Finite menu of actual rational zero-return paths separating every finit

## Visible response tail, transcribed (continues the truncated word)

e Fourier preparation space | Proved |
| Exact minimax fast-return limit (11) | Proved using accepted E155 transference |
| One Euler path producing arbitrarily small weighted H1 to L2 norm | Open |
| A viscous multidirectional construction with full nonlinear all-weak control | Open |
| Full fixed-family additive-force compiler and complete-bit bounds | Open |

### Principal conclusion

This continuation establishes that the twelve physical Euler generators have a strong algebraic escape property: every finite Fourier preparation space can be separated from itself through finitely many genuine, rationally realizable generator evolutions, and that fact has an exact computational certificate. The minimax theorem then sharpens the role of weighted Euler squeezing. If a sequence of accelerated zero-return controls has vanishing nonlinear comparison error, its worst-case terminal response converges to the corresponding weighted linearized Euler norm. A successful fast-return strategy must therefore solve the weighted operator problem, not merely show Fourier mixing. The full question is still unresolved. There is no proved single control that contracts the entire three-dimensional preparation ball, and consequently no justified unconditional compiler runtime, output-size or force-amplitude bound. The next decisive mathematical step is to convert the finite-menu Fourier-escape property into either one genuinely L2-squeezing homogeneous Euler propagator or a viscosity-assisted common contraction with uniform nonlinear control. The present results give a finite, computable algebraic foundation for investigating that step, but do not assume its conclusion.

