# S07 independent scientific adversary: loss-echo identification

16 October 2026. **Decision: exact, scoped structural identification survives; new foundational or practical Astra Ultra capability is NOT_ACHIEVED.** I verified S04's compact on–off–on theorem, supplied a finite positive-duration formulation, and found decisive model and conditioning boundaries. A close switched-system realization incumbent already owns the broad idea; no physical assay or equal-information performance advantage has been demonstrated. The selective-sink two-dose result is mathematically correct inside its narrower ideal model, but needs explicit raw-data checks and independently established selectivity.

## Target and exact theorem audit

Use column probabilities. Let $A$ be an $n\times n$ conservative Markov generator, $c={\bf1}^{\mathsf T}$, $b\ge0$, $cb=1$, and let the fixed known on-amplitude have generator $M=A-uD$, where $u>0$ and **$D$ is diagonal in the physical state coordinates**, with positive, pairwise distinct entries. The only measured output is total surviving mass. An uninterrupted on pulse gives $f(t)=ce^{Mt}b$; an on–off–on echo gives

\[
g(t_2,\tau,t_1)=ce^{Mt_2}e^{A\tau}e^{Mt_1}b.
\]

Set $C=[b,Mb,\ldots,M^{n-1}b]$, $O=[c;cM;\ldots;cM^{n-1}]$, and form $H_{ij}=cM^{i+j}b$, $H^+_{ij}=cM^{i+j+1}b$, and $K_{ij}=cM^i A M^j b$, with indices $0\le i,j<n$. These are derivatives of $f$ and $g$ at zero, to total order at most $2n-1$. Direct multiplication gives $H=OC$, $H^+=OMC$, $K=OAC$. If $H$ is invertible,

\[
H^{-1}H^+=C^{-1}MC,\qquad H^{-1}K=C^{-1}AC,
\qquad D_h=\frac{H^{-1}K-H^{-1}H^+}{u}=C^{-1}DC.
\]

Thus the algebra is correct, including the shared basis for the two generators. Invertibility of this square $H$ is **equivalent** to reachability of $(M,b)$ and observability of $(c,M)$. It is a sufficient gate for this small construction; it is not a consequence of simple $D$, nor a necessary condition for every richer switched-word realization. To recover physical coordinates, take eigenvectors $E$ of $D_h$. Pairwise distinct $D_i$ leave one scale per eigenvector; $c_h E={\bf1}^{\mathsf T}$, where $c_h=cC$, fixes those scales. Only a state permutation remains without externally attached labels. If $b$ is also known as a labeled physical preparation, it can restrict that permutation.

S04's exact [two-pulse replay](../s04_scientific_invention/two_pulse_echo_replay.py) passes: the three-state fixture has $\det H=-375$ and recovers its exact $A,D,b$. Its sharp two-state one-pulse collision also passes: $(a,r,d_1,d_2)=(2,1,2,3)$ and $(1,1,2,4)$ both give uninterrupted-on transform $(s+6)/(s^2+8s+14)$, while $cMAMb$ is respectively $10$ and $8$. The echo has genuinely additional information. For example, at $(t_1,\tau,t_2)=(0.2,0.3,0.2)$, their modeled endpoint survivals are $0.3917814646$ and $0.3861349759$. This is a model calculation, not a measured distinction.

Simple $D$ does not ensure this on-mode Hankel is invertible. The exact fixture $A=[[-2,1],[2,-1]]$, $D=\operatorname{diag}(1,3)$, $b=(1/2,1/2)^{\mathsf T}$ has $Mb=-2b$, hence $\det H=0$, but $\det[b,Ab]=1/2$, $\det[c;cM]=-2$, and $cMAb=-1$. Switching exposes a second state direction even though the compact on-only basis fails. These are exact checks in [pulse_gauge.py](pulse_gauge.py). This establishes a scope distinction, not an alternative full uniqueness theorem.

## Finite positive-duration repair and its precision limit

The derivative theorem does not itself grant access to high derivatives from noisy laboratory endpoints. There is, however, an exact **finite positive-duration** version. Choose on step $Δ>0$ and dark duration $τ>0$. Write $P=e^{MΔ}$, $Q=e^{Aτ}$, and measure one-pulse values $m_k=cP^k b$, $0\le k\le2n-1$, plus echo values $e_{ij}=cP^i QP^j b$, $0\le i,j<n$. With $H^{(P)}_{ij}=m_{i+j}$, $H^{(P)+}_{ij}=m_{i+j+1}$, and $K^{(Q)}_{ij}=e_{ij}$, the same factorization gives

\[
(H^{(P)})^{-1}H^{(P)+}=C_P^{-1}PC_P,\qquad
(H^{(P)})^{-1}K^{(Q)}=C_P^{-1}QC_P,
\quad C_P=[b,Pb,\ldots,P^{n-1}b].
\]

There are $2n-1$ nontrivial one-pulse lengths and at most $n^2$ echo settings; $m_0=1$ is known. This is endpoint survival, with no derivatives or state-resolved sensor. It still assumes a known $n$ and nonsingular sampled Hankel. Matrix logarithms become the remaining issue. If an independent upper bound $R$ on every transition exit rate is known and $Δ,τ<\pi/R$, column Gershgorin disks give $|\operatorname{Im}\lambda(A)|,|\operatorname{Im}\lambda(M)|\le R$. The principal logs of the recovered $P,Q$ then equal $Δ M,τ A$ in the shared basis, so the preceding physical-axis recovery applies. This is a sufficient **branch-uniqueness** condition, not a noise bound.

There is also an exact no-rate-cap uniqueness variant. From the same $\Delta_1$ Hankel, acquire $cP_1^iP_2P_1^j b$ for $P_2=e^{M\Delta_2}$, and two echo arrays using $Q_\ell=e^{A\tau_\ell}$, all with $0\le i,j<n$. These recover $P_1,P_2,Q_1,Q_2$ in **one** basis. Because $P_1$ and $P_2$ commute, the second on grid needs only the $2n-1$ distinct durations $\Delta_2+k\Delta_1$, $0\le k\le2n-2$; each dark duration can require up to $n^2$ echo settings. If both $\Delta_2/\Delta_1$ and $\tau_2/\tau_1$ are irrational, equality of each pair of exponentials for two candidate generators implies equality at every signed integer combination of the two times. Those combinations are dense in real time; continuity and differentiation at zero force the generators to be equal. This proves ideal exact uniqueness without selecting a log branch. It does **not** provide a stable numerical inversion: exact irrational timing and exact endpoint probabilities are idealizations, and using near-canceling large signed powers amplifies measurement error. For $D=dI+\varepsilon E$, all pulse survival values at $\varepsilon=0$ equal $e^{-udT_{\rm on}}$ independent of $A$; on any fixed bounded schedule they differ from that limit by $O(\varepsilon)$. Thus simple $D$ at every nonzero contrast gives no uniform conditioning.

The [finite-grid replay](finite_echo.py) reconstructs S04's three-state fixture using endpoint matrices at $Δ=0.25,τ=0.4$; its Euclidean errors in $A,D,b$ are $4.66\times10^{-12},1.20\times10^{-12},1.31\times10^{-13}$. It also recovers second grids with ratios $\sqrt2,\sqrt3$ in the same basis. Yet even this exact-model numerical fixture has $κ(H)=1.73\times10^4$; at $Δ=0.5$, $κ(H)=8.79\times10^5$. These are conditioning diagnostics, not experimental precision or worst-case guarantees. Another direct obstruction to a uniform precision claim is $A_r=[[-r,r],[r,-r]]$, $D=\operatorname{diag}(1,2)$, $b=e_1$, fixed $u$: every finite $r>0$ meets simple $D$ and on-mode minimality, but every fixed positive-duration pulse panel approaches its fast-mixing limit as $r\to\infty$, whereas $\lVert A_r-A_{2r}\rVert\to\infty$. Thus even two incommensurate grids cannot uniformly resolve unbounded rates at finite precision. Without a bound or a second incommensurate duration, matrix-log ambiguity remains a general Markov embedding concern; joint $A,D$ constraints may resolve some individual grids, but that requires a separate proof. [Casanellas, Fernández-Sánchez, and Roca-Lacostena](https://arxiv.org/abs/2005.00818) treat the Markov matrix embedding problem and enumeration of possible generators.

## Physical-state and model-validity adversaries

The diagonal-control assumption does real identifiability work. In [pulse_gauge.py](pulse_gauge.py), take $A=[[-2,3],[2,-3]]$, $D=\operatorname{diag}(1,2)$, $b=(1/2,1/2)^{\mathsf T}$, and $T=[[9/10,1/10],[1/10,9/10]]$. It has $cT=c$ and $T^{-1}b=b$. The transformed model has

\[
A'=T^{-1}AT=\begin{bmatrix}-15/8&25/8\\15/8&-25/8\end{bmatrix},\qquad
D'=T^{-1}DT=\begin{bmatrix}79/80&-9/80\\9/80&161/80\end{bmatrix}.
\]

Both $A'$ and $M'=A'-D'$ have positive off-diagonal rates; $M'$ has positive state-dependent loss. They are physically valid off/on generators with a control that also changes transitions. Every on/off pulse survival is **identical** to the diagonal-control model by similarity, although $A'\ne A$. Thus simple spectrum alone does not identify chemical state axes; the intervention must be independently shown to add only diagonal loss. An uncalibrated on-amplitude also identifies only its product with $D$. Baseline leakage violates $cA=0$; an uncontrolled or pulse-dependent preparation invalidates the common-$b$ model, although an unknown but fixed $b$ is reconstructed under the theorem's assumptions. Model order greater than the probed minimal order remains possible through hidden lumpable states.

The physical interface would require a single reproducible on/off loss mechanism that leaves all interconversion rates unchanged, a conserved and accurately counted total before activation, a stable labeled preparation, and dose/clock calibration. On and off switching must not itself reset populations. Those are acquired control and validation costs, not supplied by the symbolic theorem. Test independent on-state kinetics, dark recovery, dose linearity, detector loss, off-target transition changes, pulse-history dependence, and held-out timing. A physical discriminator would randomize unknown kinetic rates in an engineered finite-state system, blind the inference, acquire the required endpoint panel and controls, then test held-out pulse schedules or state-resolved kinetics. Compare against a constrained joint likelihood fit of $A,D,b$ receiving **the same** endpoints and calibration data. No such experiment has been performed.

S04's [local Fisher audit](../s04_scientific_invention/two_pulse_fisher.py), replayed here, uses 64 synthetic echo settings with $10^4$ independent Bernoulli trials each. Its two-state rate $r$ has local Cramér–Rao fractional standard-deviation floor about $0.624$, even though the noiseless echo design has full rank. The 20-setting one-pulse design is rank deficient. These are dimensionless model-generated calculations with a finite-difference Jacobian; they show that structural identifiability is far short of practical quantitation and do not benchmark an actual joint-fit estimator. The fair joint fit uses the same 64 outcomes and positive-generator constraints, and no lower-cost or more accurate echo estimator is shown.

## Secondary two-dose selective-sink audit and narrower target

For separate ideal target $i$ assays with $A-u k_i e_ie_i^{\mathsf T}$, conservation gives $q_u(s)=[1-sY_u(s)]/u=F_i(s)/(1+uH_i(s))$, where $F_i=k_i e_i^{\mathsf T}(sI-A)^{-1}b$ and $H_i=k_i[(sI-A)^{-1}]_{ii}$. Two doses algebraically recover $F_i,H_i$. Across all $n$ labeled targets, $n$ distinct positive frequencies, known $b$, and full Krylov rank, conservation calibrates $k_i$ and gives unique $A$. I checked S04's exact [selective-sink replay](../s04_scientific_invention/selective_sink_replay.py). The theorem is valid under those exact assumptions. It should check **all original dose signals** after reconstruction, rather than promote a positive $A,k$ inferred only from $F_i$.

An exact mixed-sink witness in [exact_adversary.py](exact_adversary.py) shows why. For $A=[[-2,3],[2,-3]]$, $b=e_1$, target-1 sink $D_1=\operatorname{diag}(1,0)$, and purported target-2 sink $D_2=\operatorname{diag}(1/4,1)$, the two-dose $F$-only inversion at $s=1,2$, $u=1,2$ returns a **positive** apparent generator with rates $11362/1649$ and $547/97$, and positive efficiencies $485/357,3395/3496$. Nevertheless its predicted target-2 raw signal differs from an observed one by $-13715/10327613$ already at $(s,u)=(1,1)$. A third dose supplies a one-site falsifier: for any genuinely rank-one sink, $1/q_u(s)$ is affine in $u$; here at $s=1$ its values for doses $1,2,3$ are $41/13,30/7,27/5$, with nonzero second difference $-8/455$. Affinity is necessary, not by itself proof of selectivity.

A narrower observable survives when full $A$ does not. At a single selective site,

\[
\mathbb E_b[e^{-s\tau_i};\tau_i<\infty]
=\frac{[(sI-A)^{-1}b]_i}{[(sI-A)^{-1}]_{ii}}
=\frac{(u_2-u_1)q_{u_1}(s)q_{u_2}(s)}{q_{u_1}(s)-q_{u_2}(s)}.
\]

The first equality is the classical first-hit/return renewal identity; the second follows from the two-dose rank-one law and cancels unknown sink efficiency. It needs neither known $n$ nor full Krylov rank. In S04's symmetric three-state branch, full generator reconstruction fails rank, yet the target-2 first-hit transform is $(s+1)/(s^2+3s+1)$, giving $2/5$ at $s=1$ and $3/11$ at $s=2$, as replayed. The mixed-sink witness falsely reports $91/103,35/43$ for target 2 where the actual first-hit values are $2/3,1/2$. The one-site first-hit result is a useful target-specific scientific discriminator **only after** selectivity is established. Its renewal basis is standard; see [Régnier et al., *Nature Communications* 2023](https://www.nature.com/articles/s41467-023-36233-5).

## Prior owner and decision

[Petreczky, *Systems & Control Letters* 2007](https://doi.org/10.1016/j.sysconle.2007.04.006) develops realization theory and minimality for continuous-time linear switched systems, including restricted switching sequences. [Petreczky and van Schuppen's partial-realization paper](https://arxiv.org/abs/1010.5160) supplies finite Markov-parameter/Hankel algorithms. [Gross et al., *SIAM Journal on Applied Mathematics* 2019](https://epubs.siam.org/doi/10.1137/18M1204826) and [Ovchinnikov et al., *SIAM Journal on Applied Algebra and Geometry* 2022](https://epubs.siam.org/doi/10.1137/21M1389845) cover compartmental and multi-experiment identifiability frameworks. These sources do not by themselves settle priority for S04's exact conservative-diagonal two-pulse specialization, but they preclude presenting the broad switched realization, perturbation, or Hankel operation as new. No exhaustive novelty review was attempted.

**Promote only the scoped theorem, exact collision/discriminator, and finite-grid repair as internal mathematics.** Require independent confirmation of diagonal physical control, measured conditioning and held-out outputs, and superiority against the same-data positive joint fit before a scientific capability claim. Current physical/mission status: `NOT_ACHIEVED`.

Receipts: [exact_adversary.py](exact_adversary.py), [finite_echo.py](finite_echo.py), [pulse_gauge.py](pulse_gauge.py), and [REPLAY.txt](REPLAY.txt). All calculations are model-generated; no external data, physical test, deployment, or publication.
