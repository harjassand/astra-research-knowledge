# P1 completed return

Chat: https://chatgpt.com/c/6af464b1-3360-83ec-8c1b-9b4b95c398ff
User turn: 265713a7-7851-42f5-ab2a-bb658513cda5; final: 49fc314e-eb80-561f-9150-afcf02698e1d; UI model: Pro.
Exact prompt source: work/astra-renewed-pro-programmes-20261103/P1_FULL_LOCAL_PARTICLE_ADAPTIVE_TRANSPORT_COMPILER_PRO_20261111.txt (SHA-256 feb7b8ec20e7684679d54b96447f3702e312206dc2492fe4ecb92a3d6f86079b; one terminal LF omitted at posting).
Capture: same-chat UI Copy; native first 20,000 characters match after whitespace and UI-citation normalization; visible ending present. No literal database-byte identity asserted. No output files visible in activity panel; ZIP availability unknown. The main activity text below is an excerpt; searched-web expansion and full helper panels are not captured. A helper panel was accessible, but its complete content was not collected in this handoff.

## Visible activity excerpt

I’ll work on the full compiler claim, with particular attention to whether the proposed coupling survives conditioning on hidden history. I’ll use the available subagents to check that argument, the exact graph and spatial balance requirements, and the polynomial cost accounting independently.

Coupling audit, Balance graph audit and Cost assembly started working. Analyzing the Provided Information. Verified the premise and checked proposal-history dependence. Constructed path and conditional couplings. Validated parameter choices. Searched 3 websites. Checked arXiv source path reachability and support. Verified drift change, event-counting bounds, and coordinate variation. Derived the covariance bound.

The key coupling step appears to work: at each proposal time, average over the current hidden positions before coupling the chemical channel. That allows the error bound to hold after every realised past history, even when faults respond to that history. I’m checking the clock and tolerance bounds next, especially their dependence on reaction order. Defined the decay envelope and bounded cube indicator mismatch. Combined expectation-error bounds.

Coupling audit and Cost assembly updated. Checked innovation, thinning, and gap conditioning independence. Checked compiler cost bounds using the available construction. Cost assembly updated. Checked R and involution. Searched the web. Checked arbitrary transport and PPP balance. Balance graph audit finished. Reconstructed paired-prefix structure and checked conversion normalization. Checked normalization bounds and encoding length. Cost assembly finished. Fixed compiler constants and established polynomial bit-length bounds. Coupling audit and Balance graph audit updated. Checked the conditional estimate and verified path coupling. Verified compensator sufficiency, Brownian representation, and increment independence. Proved independent increments and tested enlarged-filtration independence. Verified Brownian properties, joint independence, and conditioned Girsanov bounds. Derived and refined the explicit class-normalizer bound. Consolidated polynomial bounds and arithmetic operation costs. Chose computable constants.

The three checks agree on an affirmative construction using the supplied well-mixed compiler. The coupling can preserve the exact event times and all null and parallel marks; conservation gives the event and movement bounds for the actual untruncated process. The final cost check also closes: tightening the accuracy budget introduces a factor 4 D, but your charged Xi absorbs it into a universal polynomial bound. Checked coefficient notation and bounded mark discrepancy. Verified boundary-strip and heat-kernel bounds. Checked autonomous dynamics, variation, and displacement bounds. Checked coupling error bounds while preserving empty base cases. Clarified theorem dependence and checked nominal guarantees. Checked parameter bounds and bounded the universal constant. Derived drift shift and clarified reaction-rate cases. Verified reverse-split balance and checked Brownian conditioning. Checked normalized cost bounds and finalized the δ convention. Checked empty-case coverage and admissible realizations. Checked nonexplosion prerequisites and framed the conditional proof.

## Complete UI-copied final

## Verdict

**Yes, using the paid well-mixed compiler in your supplied construction 1 as a premise.** The spatial extension can satisfy the full contract, including the arbitrary predictable correlated-diffusion faults and total variation of the entire timed marked chemical path.

The crucial step is a **coupling of conditional channel probabilities at a dominating Poisson clock**. That coupling averages over the motion since the preceding proposal, while retaining the actual spatial trajectory, reactant tuple, placement and subsequent fault policy. It does not require the faulty position distribution to become product-uniform.

Below I give the compiler, prove the required coupling, and account for the structural, numerical, binary and actual physical costs.

---

# 1. The compiler

Invoke the supplied well-mixed elementary compiler with accuracy
\[
\eta=\epsilon/4.
\]

Write its output as:

- the fine species and directed channels \(e=1,\ldots,M\);
- coefficients \(0<b_e\le 1\);
- activities \(\widetilde a_s\);
- decoder \(P\);
- the hidden/original label map and reverse involution;
- its paid clock \(H_{\mathrm{kin}}\ge1\).

We use its nominal complete-path guarantee. The predictable chemical faults will be paid directly in the spatial comparison below.

Define
\[
T=H_{\mathrm{kin}}\tau,
\qquad
v=(2r)^3,
\]
and
\[
\Lambda=\frac{2(1+M)(1+N_0)^2}{v},
\qquad
I=\frac2{d_0},
\qquad
J=1+\Lambda T.
\tag{1}
\]

The factor \(1+M\) covers an empty channel list.

Fix the universal numerical constant
\[
K=128.
\]

Choose the integer
\[
\boxed{
h=
\left\lceil
\frac{8K\Lambda I J}{\epsilon}
\right\rceil
}
\tag{2}
\]
and the positive rational
\[
\boxed{
\delta=
\min\left\{
\frac14,\,
\frac{\epsilon^2}
{64K^2J^2(1+hT)}
\right\}.
}
\tag{3}
\]

Emit the same chemical structure, decoder, activities and label/reverse maps, with
\[
\boxed{
c_e=b_e/h,
\qquad
H=hH_{\mathrm{kin}}.
}
\tag{4}
\]

Interpret every elementary channel using exactly the local anchoring and release rules in the question. Choose the first-reactant convention deterministically from the channel list.

These formulas are the entire additional numerical compilation. They use no transport profiles or particle positions.

I will prove the following spatial estimate, with \(S=hT\):
\[
\begin{aligned}
E_{\mathrm{sp}}
\le{}&
\frac{\Lambda I}{h}(1+\Lambda T)\\
&+64\Lambda T
\bigl[\delta^2(S+S^2)\bigr]^{1/3}
+\delta\Lambda T.
\end{aligned}
\tag{5}
\]

Here \(E_{\mathrm{sp}}\) is total variation between the **complete fine timed marked chemical paths** of the actual local process and the nominal well-mixed fine process slowed by \(h\). Every directed fine channel remains a separate mark.

---

# 2. The pair estimate survives the required conditioning

First work on a chemical-free interval of length \(g\), starting at any time \(s\). Condition on the full past at its beginning. The species and number of particles are fixed during this interval.

Let \(Q\) be the actual lifted motion. Starting from exactly the same positions, define \(Y\) using the same Brownian innovations, zero drift and the nominal covariance \(A_0\).

## 2.1 A dimension-independent displacement bound

Put
\[
S_A=\sqrt A,\qquad S_0=\sqrt{A_0}.
\]

The identity
\[
S_A(S_A-S_0)+(S_A-S_0)S_0=A-A_0
\]
and the Sylvester integral formula give
\[
\begin{aligned}
\|S_A-S_0\|_{\mathrm{op}}
&\le
\frac{\|A-A_0\|_{\mathrm{op}}}
{\lambda_{\min}(S_A)+\lambda_{\min}(S_0)}
\\
&\le
\frac{\delta d_0}
{\sqrt{(1-\delta)d_0}+\sqrt{d_0}}
\\
&\le \delta\sqrt{d_0}.
\end{aligned}
\tag{6}
\]

For two distinct particles \(i,j\), the difference-coordinate projection has rank three and operator norm \(\sqrt2\). Thus its projected squared Hilbert–Schmidt error is at most
\[
6\delta^2d_0.
\]

Including the factor \(\sqrt2\) in the spatial SDE and the drift bound
\[
|v_i-v_j|\le2\delta,
\]
conditional Itô isometry gives the convenient estimate
\[
\boxed{
\mathbb E
\left|
(Q_i-Q_j)-(Y_i-Y_j)
\right|_{\mathrm{lift}}^2
\le32\delta^2(g+g^2).
}
\tag{7}
\]

The constant is independent of the particle number. The proof permits arbitrary predictable dependence and correlation in \(A\).

## 2.2 The nominal pair estimate permits anisotropic measurable profiles

For a nonzero Fourier mode \(k\in\mathbb Z^3\), the nominal pair-displacement characteristic multiplier has absolute value
\[
\exp\left[
-4\pi^2
\int_s^{s+g}
k^\top\!\left(D_{s(i)}(t)+D_{s(j)}(t)\right)k\,dt
\right]
\le
e^{-8\pi^2d_0g|k|^2}.
\tag{8}
\]

This calculation uses only deterministic measurability and the matrix inequalities. No temporal derivatives or common eigendirections are required.

Define
\[
b(g)=\exp\!\left[-(d_0g-1)_+\right].
\tag{9}
\]

For \(g\ge d_0^{-1}\), the nominal pair heat density \(p_g\) satisfies
\[
\|p_g\|_\infty\le2,
\qquad
\|p_g-1\|_\infty\le b(g).
\tag{10}
\]

For example, these inequalities follow by summing the Fourier bound (8); the sum over nonzero modes at \(d_0g=1\) is already less than one. Also,
\[
\int_0^\infty b(g)\,dg=\frac2{d_0}=I.
\tag{11}
\]

## 2.3 The discontinuous interaction kernel

Let \(C_r=[-r,r]^3\) on the torus. Its boundary strip of width \(w\) has volume at most \(12w\).

If the indicators of \(C_r\) differ for the actual and nominal pair displacements, either the nominal displacement lies in that strip or their lifted displacement difference exceeds \(w\). For \(g\ge d_0^{-1}\), therefore,
\[
\Pr\!\left(
1_{C_r}(Q_i-Q_j)\ne1_{C_r}(Y_i-Y_j)
\right)
\le
24w+\frac{32\delta^2(g+g^2)}{w^2}.
\]

Taking
\[
w=\beta(g):=\bigl[\delta^2(g+g^2)\bigr]^{1/3}
\]
gives
\[
\boxed{
\left|
\mathbb E\kappa_r(Q_i-Q_j)-1
\right|
\le
\frac{b(g)+56\beta(g)}{v}.
}
\tag{12}
\]

For \(g<d_0^{-1}\), the trivial bound \(1/v\) is covered by \(b(g)=1\).

This is a conditional pair expectation estimate. Different pairs may be dependent, and the boundary event may be dependent on the displacement error.

The remaining issue is ensuring that this estimate applies under the conditioning needed for a complete-path coupling.

---

# 3. An independent proposal clock for every admitted realization

For every actual history, conservation gives
\[
n(t)=|Z(t)|_1\le N_0.
\tag{13}
\]

A binary directed channel has at most \((1+N_0)^2\) eligible ordered tuples, and \(\kappa_r\le1/v\). Unary and global null channels obey the same upper bound. Since \(b_e\le1\) and \(1+\delta<3/2\), the total actual chemical intensity satisfies
\[
\lambda_{\mathrm{all}}(t)
\le
\frac{3M(1+N_0)^2}{2hv}
\le
\frac{\Lambda}{h}
=:\lambda.
\tag{14}
\]

This includes every hidden, null and parallel firing.

Take any admitted actual realization. Augment it, solely for the proof, with rejected proposals of predictable intensity
\[
\lambda-\lambda_{\mathrm{all}}(t),
\]
using an independent Poisson random measure. The combined proposal counting process \(N^\star\) has deterministic compensator
\[
\lambda\,dt.
\]

There is a useful stronger statement: **the future proposal and Brownian innovations are jointly independent of the full past, and independent of one another.**

Indeed, the Brownian motion \(W\) and \(N^\star\) have deterministic joint characteristics. The continuous Brownian martingale and the compensated counting martingale have zero covariation. The exponential-martingale calculation gives
\[
\begin{aligned}
&\mathbb E\!\left[
e^{\,i\theta\cdot(W_{s+t}-W_s)
+i u(N^\star_{s+t}-N^\star_s)}
\mid\mathcal F_s
\right]\\
&\hspace{2cm}=
\exp\left(
-\frac{|\theta|^2t}{2}
+\lambda t(e^{iu}-1)
\right).
\end{aligned}
\tag{15}
\]

Iteration gives the corresponding statement for future path increments, including after proposal stopping times.

Consequently, after a proposal time:

- the next gap \(G\) is exponential with rate \(\lambda\);
- it is independent of future Brownian innovations;
- conditioning on \(G=g\) leaves the Brownian innovations valid on that gap;
- no chemical event occurs inside the gap.

This avoids conditioning directly on survival of the spatial reaction process, which would generally bias its motion. Absence of a **dominating proposal** has the constant survival factor \(e^{-\lambda g}\).

The rejected proposals are mathematical bookkeeping. They are not emitted chemical events and require no additional physical clock, particle or token.

---

# 4. Couple channel marginals while retaining the actual spatial process

Let \(\mathcal H\) contain the full actual past through a proposal time, together with previous coupling randomness. Condition also on the next proposal gap \(g\).

Suppose the actual and reference fine count states currently agree at \(u\).

For each channel \(e\), let
\[
K_e(u)=(u)_{\alpha_e}.
\]
This counts ordered distinct tuples for binary channels, eligible particles for unary channels, and one opportunity for a \(0\to0\) mark.

The nominal well-mixed proposal probabilities are
\[
q_e(u)=\frac{b_eK_e(u)}{\Lambda},
\qquad
q_0(u)=1-\sum_e q_e(u),
\tag{16}
\]
where \(0\) denotes rejection.

Let
\[
p_e(\mathcal H,g)
\]
be the actual probability of channel \(e\) at the next proposal, **after averaging over the intervening motion and predictable chemical multiplier**.

For a binary channel,
\[
p_e(\mathcal H,g)
=
\frac{b_e}{\Lambda}
\mathbb E\left[
\theta_e
\sum_{\text{eligible ordered pairs}}
\kappa_r(Q_j-Q_i)
\;\middle|\;\mathcal H,G=g
\right],
\tag{17}
\]
with \(1-\delta\le\theta_e\le1+\delta\).

Even if \(\theta_e\) depends on the positions and the entire past,
\[
\left|
\mathbb E\left[(\theta_e-1)\sum\kappa_r\right]
\right|
\le
\frac{\delta K_e(u)}v.
\tag{18}
\]

Combining this with (12), then summing over channels, gives
\[
\boxed{
\|p(\mathcal H,g)-q(u)\|_{\mathrm{TV}}
\le
b(g)+64\beta(g)+\delta.
}
\tag{19}
\]

The rejection probability causes no extra difficulty:
\[
|p_0-q_0|\le\sum_e|p_e-q_e|.
\]

### The coupling construction

This is the point where the order of conditioning matters.

First retain the actual spatial trajectory through the gap and its actual proposal outcome \(E\), including the actual tuple and placement. Let \(\pi(e,f)\) be a maximal coupling of the channel distributions \(p\) and \(q\).

Using an added independent uniform variable, draw the reference outcome \(F\) with
\[
\Pr(F=f\mid E=e,\mathcal H,G=g)
=
\frac{\pi(e,f)}{p_e}
\quad\text{when }p_e>0.
\tag{20}
\]

Then:

1. The actual trajectory, tuple, placement and future policy retain their original joint law.
2. Conditional on \(\mathcal H,G=g\), the reference channel has distribution \(q\).
3. The probability of different channels is exactly \(\|p-q\|_{\mathrm{TV}}\).
4. Agreement of channels preserves agreement of fine counts.

Thus the reference process has the nominal well-mixed marked law, slowed by \(h\).

The reference channel is **not** required to have distribution \(q\) conditional on the entire current spatial trajectory. That stronger statement would generally be false. The required statement conditions on the preceding full past and the next proposal gap.

All conditional probabilities and maximal couplings here are proof objects. The compiler evaluates none of them.

---

# 5. Summing errors without altering any firing time

Let
\[
S=hT,\qquad \mu=\lambda S=\Lambda T.
\]

Write the proposal gaps as \(G_1,G_2,\ldots\), their partial sums as \(S_j\), and let
\[
N=N^\star(S).
\]

For the mixing term, use
\[
\sum_{j=1}^{N}b(G_j)
\le
\sum_{j=1}^{N+1}b(G_j).
\]

The event
\[
\{j\le N+1\}=\{S_{j-1}\le S\}
\]
depends only on preceding gaps and is independent of \(G_j\). Hence
\[
\begin{aligned}
\mathbb E\sum_{j=1}^{N}b(G_j)
&\le
(1+\lambda S)\mathbb E b(G)\\
&\le
(1+\lambda S)\lambda I.
\end{aligned}
\tag{21}
\]

This avoids the invalid step of conditioning on the number of proposals and then treating the gaps as unchanged exponentials.

Because each gap ending before \(S\) is at most \(S\),
\[
\mathbb E\sum_{j=1}^{N}\beta(G_j)
\le\mu\beta(S),
\qquad
\mathbb E\sum_{j=1}^{N}\delta=\mu\delta.
\tag{22}
\]

A union bound on the first channel disagreement proves (5):
\[
E_{\mathrm{sp}}
\le
\frac{\Lambda I}{h}(1+\Lambda T)
+64\Lambda T[\delta^2(S+S^2)]^{1/3}
+\delta\Lambda T.
\]

On the event of no disagreement, both processes have **exactly the same accepted channel marks at exactly the same proposal times**.

In particular, this coupling:

- retains null and parallel marks;
- compares the initial waiting period;
- deletes no physical waiting time;
- introduces no time perturbation;
- permits every later fault decision to depend on the full actual history.

## The chosen parameters pay the error

Since \(K=128\), a convenient consequence of (5) is
\[
E_{\mathrm{sp}}
\le
KJ\left\{
\frac{\Lambda I}{h}
+[\delta^2(S+S^2)]^{1/3}
+\delta
\right\}.
\tag{23}
\]

Equation (2) makes the first term at most \(\epsilon/8\).

Equation (3) gives
\[
\delta^2(S+S^2)
\le
\frac{\epsilon^4}{4096K^4J^4},
\]
so
\[
KJ[\delta^2(S+S^2)]^{1/3}
\le\frac{\epsilon}{16}.
\]
Also,
\[
KJ\delta\le\frac{\epsilon}{64}.
\]

Therefore
\[
E_{\mathrm{sp}}
\le\frac{13\epsilon}{64}.
\tag{24}
\]

Apply the deterministic decoder and hide the auxiliary marks. Total variation contracts under this observation map. Combining (24) with the well-mixed compiler’s error \(\epsilon/4\) yields
\[
\boxed{
d_{\mathrm{TV}}\!\left(
\text{complete observed path of }Z(Ht),
\text{target marked path of }X_t
\right)
\le
\frac{29\epsilon}{64}
<\epsilon.
}
\tag{25}
\]

The bound is uniform over initial placements, the unknown matrix profiles, and every admitted predictable fault realization.

---

# 6. Exact nominal spatial balance

Let \(\Pi_{\widetilde a}\) be the independent Poisson point-process reference, with intensity \(\widetilde a_s\) for species \(s\).

Consider a paired binding/release
\[
A+B\ \rightleftarrows\ C,
\]
with \(A\) designated as the anchored reactant.

For a nonnegative test function \(\Phi\) of the pre- and post-event configurations, the ordered factorial Mecke identity writes the forward flux as
\[
\begin{aligned}
\mathcal F_e(\Phi)
={}&
c_e\widetilde a_A\widetilde a_B
\int\Pi_{\widetilde a}(d\eta)
\int_{\mathbb T^3}dx
\int_{\mathbb T^3}\kappa_r(z)\,dz\\
&\quad\cdot
\Phi\!\left(
\eta+\delta_{A,x}+\delta_{B,x+z},
\eta+\delta_{C,x}
\right).
\end{aligned}
\tag{26}
\]

The reverse release flux, with the configuration pair reversed, is the same integral with prefactor
\[
c_{\bar e}\widetilde a_C.
\]

The inherited chemical identity
\[
c_e\widetilde a_A\widetilde a_B
=
c_{\bar e}\widetilde a_C
\tag{27}
\]
therefore proves equality of the full spatial flux measures.

**For \(A=B\), the ordered factorial identity produces \(\widetilde a_A^2\), without a factor \(1/2\).** This agrees with the prescribed ordered-distinct binding convention.

Unary channels obey the same calculation. Global \(0\to0\) marks have flux \(c_e\Pi_{\widetilde a}\); their reverse-label equality is inherited as well. A null event remains a real marked flux even when it leaves the configuration unchanged.

The common division by \(h\) preserves every detailed-balance identity.

For diffusion, periodic integration by parts gives, at every time where the measurable coefficients are represented,
\[
\int f\left(\sum_iD_{s(i)}(t):\nabla_i^2g\right)
=
-\sum_i\int
(\nabla_i f)^\top D_{s(i)}(t)\nabla_i g.
\tag{28}
\]

Thus each instantaneous nominal diffusion generator is symmetric under the uniform position reference.

Conditioning on an invariant chemical class preserves both properties: reaction endpoints remain in the same class, and diffusion leaves the counts fixed. The compiler does not evaluate a class normalizer.

The placement-flux issue is consistent with the reversible-binding framework studied by Zhang and Isaacson. Their work derives spatial detailed-balance constraints for a reversible binding pair; the adaptive complete-path coupling above supplies the additional argument needed here. [open.bu.edu](https://open.bu.edu/items/4b8fb255-7254-4f87-b928-00ff3ef2594b?utm_source=chatgpt.com)

---

# 7. Exact graph, local support and initialization

## 7.1 The all-state chemical graph

The emitted species, channels, decoder, label map and reverse involution are those of the supplied compiler. Every coefficient stays strictly positive.

Consequently its exact all-state property persists:
\[
\boxed{
u\leadsto v
\quad\Longleftrightarrow\quad
Pu\leadsto Pv.
}
\tag{29}
\]

This applies to every finite fine count state, including states outside the initialized mass sector. No states or channels are removed using \(N_0\).

Hidden channels preserve \(P\), observed channels have their required decoded increments and enabling conditions, and the exact communicating-class preimages are inherited.

## 7.2 Every finite allowed count path remains spatially possible

Uniform ellipticity survives the faults:
\[
A(t)\succeq(1-\delta)d_0I,
\qquad
A(t)\preceq(1+\delta d_0)I.
\tag{30}
\]

For any fixed finite particle collection, any starting configuration and any open target set of positions, the adapted motion can reach that set with positive probability during a sufficiently short chemical-free gap.

A direct support proof uses a drift-only Girsanov change of measure. Choose a bounded deterministic lifted velocity \(b\) carrying the starting positions to a point inside the target set. The predictable Brownian drift shift
\[
\theta(t)
=
(\sqrt{2A(t)})^{-1}(b-v(t))
\tag{31}
\]
has bounded finite energy on the chosen finite interval.

Under the equivalent measure, the lifted drift is \(b\), while the remaining motion is a martingale with bounded quadratic variation. On a sufficiently short interval, Doob’s inequality gives positive probability of staying in a tube around the chosen path. Equivalence transfers positivity back to the original law.

This is a support argument, not a force applied by the compiler. The independent proposal-gap representation justifies making it on a chemical-free interval.

For a desired binding, choose an open target set placing an eligible pair strictly inside the interaction cube. Its channel then has strictly positive acceptance probability, because \(c_e>0\) and \(1-\delta>0\). Unary, release and global null channels already have positive enabled intensities. Iterate over the finite requested count-channel path.

This establishes the required count-path support without requesting exact hitting of a continuous point configuration.

## 7.3 Initialization

Initialization is precisely \(x_0\) original particles and zero auxiliary particles.

The estimates begin at time zero from arbitrary deterministic positions. Coincident distinct particles cause no singularity, since the kernel is bounded by \(1/v\).

If \(N_0=0\), conservation forces the population to stay empty. Any enabled zero-source original reaction is necessarily \(0\to0\), and its real marks are covered by the same argument.

The chemical structure and its maps depend only on the original reaction structure and reverse involution. Population, accuracy, horizon, radius and transport lower bound enter the numerical choices.

---

# 8. Actual event and movement costs, for all physical times

These bounds hold directly for the actual process; they use no equilibrium or averaging estimate.

Conservation and \(w_s\ge1\) give, pathwise,
\[
\sum_s w_sZ_s(t)=N_0,
\qquad
|Z(t)|_1\le N_0.
\tag{32}
\]

The deterministic intensity bound (14) proves nonexplosion and
\[
\boxed{
\mathbb EF_{\mathrm{all}}(t)
\le\frac{\Lambda t}{h}
\quad\text{for every }t\ge0.
}
\tag{33}
\]

At the observation horizon,
\[
\boxed{
\mathbb EF_{\mathrm{all}}(H\tau)
\le\Lambda T.
}
\tag{34}
\]

Every actual chemical firing is counted, including hidden and null firings.

Particle-time satisfies
\[
\boxed{
\int_0^t|Z(s)|_1\,ds\le N_0t.
}
\tag{35}
\]

Since \(A\preceq\frac32I\), the sum of continuous coordinate quadratic variations over actual lifetimes is
\[
\boxed{
\int_0^t2\,\operatorname{tr}A(s)\,ds
\le9N_0t.
}
\tag{36}
\]

Likewise, summed drift-path variation is
\[
\boxed{
\sum_{\text{lifetimes}}
\int_{\text{lifetime}\cap[0,t]}|v_i(s)|\,ds
\le\delta N_0t.
}
\tag{37}
\]

The specified reaction-placement displacement has length at most \(\sqrt3r\) per local event, so its accumulated charge is at most
\[
\boxed{\sqrt3\,rF_{\mathrm{all}}(t).}
\tag{38}
\]

These are the requested particle, quadratic-variation, drift and local-displacement accounts.

---

# 9. Universal polynomial numerical and binary bounds

There are two quantitative details to handle explicitly: variable order when the accuracy budget changes, and the distinction between a numerical bound and a bound that also depends on input bit length.

Write
\[
R=\mathsf R_{\mathrm{num}}.
\]

## 9.1 Tightening the kinetic accuracy remains polynomially paid

Let \(U_\epsilon\) denote the \(U\) in the question. Then
\[
U_{\epsilon/4}\le4U_\epsilon,
\]
and therefore
\[
\Gamma_{\epsilon/4}\le4^D\Gamma_\epsilon.
\tag{39}
\]

But
\[
\Xi
=
2+\left(2+\sum_i(a_i+a_i^{-1})\right)^{2D+2}
\ge4^{D+1}.
\]

Hence
\[
\boxed{
\Gamma_{\epsilon/4}
\le\Xi\Gamma_\epsilon
\le R^2.
}
\tag{40}
\]

The other changed charge is \(\epsilon^{-1}\), multiplied by four. Thus the numerical charge of the invoked kinetic instance is at most \(5R^2\), while its complete input length increases by only a constant.

The factor \(4^D\) is explicitly paid by the supplied numerical charge.

## 9.2 The channel count has a bound in \(R\) alone

The paired-prefix implementation can provide a structural channel-count bound directly. There is also a way to obtain the needed bound using only the stated structural independence and binary-cost guarantee.

For analysis, consider the same reaction structure and reverse involution with
\[
k_r=1,\quad a_i=1,\quad x_0=0,\quad
\tau=1,\quad\epsilon_0=1/16,
\]
retaining the supplied conservative weights.

This is an admitted input, and it produces exactly the same chemical structure. Its
\[
U_0=4098\le2U_\epsilon.
\]

Furthermore,
\[
\sum_rU_\epsilon^{|y_r|}
\le
\left(\max_rk_r^{-1}\right)
\sum_rk_rU_\epsilon^{|y_r|}
\le R^2,
\]
and
\[
2^D\le\sqrt\Xi\le\sqrt R.
\]

Its numerical charge and canonical binary input length are therefore bounded by universal multiples of \(R^3\). The kinetic compiler’s output-bit bound on that hypothetical instance bounds its channel count by a fixed power of \(R\).

This hypothetical instance is used only to prove the bound. The actual compiler does not run it.

## 9.3 Explicit universal exponents

Fix the supplied kinetic compiler and its computable universal constants once. Let its exponent be \(p_{\mathrm{kin}}\). We can take
\[
q=3p_{\mathrm{kin}}+2
\]
and a computable universal \(C_0\ge1\) so that
\[
M,\ H_{\mathrm{kin}},\
\max_e b_e^{-1},\
\max_s(\widetilde a_s+\widetilde a_s^{-1}),\
\max_{i,s}P_{is}
\le C_0R^q.
\tag{41}
\]

The displayed compiler formulas then give the following safe bounds.

| Quantity | Universal-constant multiple of |
|---|---:|
| \(\Lambda\) | \(R^{q+5}\) |
| \(I\) | \(R\) |
| \(T\) | \(R^{q+1}\) |
| \(J=1+\Lambda T\) | \(R^{2q+6}\) |
| \(h\) | \(R^{3q+13}\) |
| \(H\) | \(R^{4q+13}\) |
| \(H\tau=hT\) | \(R^{4q+14}\) |
| \(\max_e c_e^{-1}\) | \(R^{4q+13}\) |
| \(\delta^{-1}\) | \(R^{8q+28}\) |
| \(\mathbb EF_{\mathrm{all}}(H\tau)\) | \(R^{2q+6}\) |

Thus, after increasing a computable universal constant,
\[
\boxed{p=8q+30}
\tag{42}
\]
is a common exponent for the requested bounds.

For clarity, constants for the numerical part can be propagated by the explicit recursion
\[
\begin{aligned}
C_\Lambda&=1+C_0,\\
C_J&=1+C_\Lambda C_0,\\
C_h&=1+16K C_\Lambda C_J,\\
C_S&=1+C_hC_0,\\
C_\delta&=4+64K^2C_J^2C_S.
\end{aligned}
\tag{43}
\]

Together with the fixed kinetic compiler and elementary arithmetic constants, these yield an explicitly computable universal \(C\).

The final exponent depends on the fixed primitive compiler, not on the input reaction order, dimension, population or transport history.

## 9.4 Binary implementation and precision

The additional computation uses exact rational sums, products, comparison, integer ceiling and coefficient scaling.

In particular:

- \(N_0=\omega\cdot x_0\) is computed in binary.
- No particle population or communicating class is enumerated.
- The compiler reads the finite emitted network to obtain \(M\).
- All new rational descriptions have bit lengths polynomial in the inherited output length and the original input length.
- Standard exact arithmetic gives polynomial bit operations and working memory.
- No conditional probability from the proof is computed.
- No invariant normalizer, PDE solution or continuous-path sampler is supplied as an oracle.

Increasing \(C\) if necessary, (42) bounds bit operations, working-memory bits, total output bits and individual description lengths by
\[
C(1+L+R)^p.
\]

The numerical table and (33)–(38) give the required bounds in \(CR^p\), including the all-time untruncated event bound.

---

# 10. What has been established

**The full spatial operation follows from the supplied paid elementary kinetic compiler.** The added theorem is a robust local lift whose complete timed marked-path error is controlled by
\[
\boxed{
\frac{\Lambda I}{h}(1+\Lambda T)
+
64\Lambda T[\delta^2(hT+(hT)^2)]^{1/3}
+
\delta\Lambda T.
}
\]

The decisive justification is the proposal-clock construction and conditional channel coupling. It applies after every realised past, preserves the actual hidden spatial process and fault policy, and couples accepted channel times exactly.

With the explicit rational choices (2)–(4), the resulting compiler satisfies the requested accuracy, nominal balance, exact graph and spatial-support properties, initialization, structural independence, and universal polynomial binary and actual physical costs.