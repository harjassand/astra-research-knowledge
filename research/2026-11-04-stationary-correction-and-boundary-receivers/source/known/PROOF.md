# Recovering a Markov generator from stationary barrier-intervention snapshots

4 November 2026. Research theorem draft, pending independent audit and literature-priority review. This is an exact identifiability result under strong controls, not a demonstrated instrument, a universal inference method, or a claim of a civilisation-changing capability. No Python used.

## 1. Model and operational assumptions

Let W be an irreducible continuous-time Markov generator on n≥3 fully observed, correctly specified states, in the column convention dp/dt=Wp. Thus 1ᵀW=0, off-diagonal W_ij≥0, and Wπ=0 for a unique positive normalized stationary distribution π. Let G be a known simple connected undirected graph whose edges each carry strictly positive rates in both directions. There are no unobserved parallel channels in the interpretation of thermodynamic currents.

For an oriented edge e=(a,b), define b_e=e_b−e_a, u_e=W_ba e_a−W_ab e_b and current j_e=u_eᵀπ. A barrier intervention multiplies both directed rates on just this edge by the same factor t_e>0, t_e≠1, leaving every other off-diagonal rate unchanged and maintaining column sums. Therefore

W^(e)=W+(t_e−1)b_e u_eᵀ.

Observe only π and the stationary distribution π^(e) of each intervened generator. Set d_e=π^(e)−π. The factors t_e need not be calibrated or even equal across experiments. Locality to the claimed edge, nontriviality, and stability of the state space are indispensable controls for the stated setup. Equal scaling in the two directions is required for the symmetric-barrier interpretation and the current-zero equivalence below, not for the inverse-ray uniqueness algebra; Section 11 explicitly relaxes it. This is not merely an arbitrary state-potential perturbation.

Assume the observed nonzero-current intervention edges contain a spanning subgraph E_* with connected cycle matroid: every two edges can be linked through a sequence of simple cycles with shared edges. A familiar sufficient case is a simple biconnected graph with nonzero stationary current on every edge. A single n-cycle with nonzero circulation satisfies the assumption. It is sufficient to use this spanning active subgraph, even if other unperturbed edges exist in the generator.

## 2. Exact finite-step response lemma

Subtract stationarity equations:

W d_e=−(t_e−1)(u_eᵀπ^(e))b_e.                 (1)

Let H={x:1ᵀx=0}. Irreducibility implies W maps H bijectively to itself: the only nullvector of W is π, which is not in H. Thus d_e lies on the line W_H^−1 b_e.

Moreover d_e=0 if and only if j_e=0. If d_e=0, π^(e)=π and (1) implies (t_e−1)j_e=0, hence j_e=0. Conversely j_e=0 implies W^(e)π=0, and uniqueness gives π^(e)=π. Therefore every active measured response is nonzero. These statements hold for finite interventions, not just a first-order approximation.

At infinitesimal log-barrier strength s=log t, r_e=(d/ds)π^(e)|_0 obeys W r_e=−j_e b_e. This identity belongs to established Markov static-response theory; the proposed contribution is the inverse identifiability argument below, whose priority remains unverified.

## 3. Incidence-ray rigidity lemma

**Lemma.** Let A:H→H be linear. Suppose A b_e=λ_e b_e for all edges of a spanning graph with connected cycle matroid. Then A=c I_H for some scalar c.

**Proof.** For a simple cycle C, consistently orient its edges around the cycle. The only linear dependence among their incidence columns is their signed cycle sum ∑_(e∈C) ε_e b_e=0, up to a common scalar. Applying A gives ∑ ε_e λ_e b_e=0. Uniqueness of that dependence forces all λ_e on C to coincide. Shared-cycle propagation gives the same scalar c on every edge of E_*. Since a connected spanning graph's incidence vectors span H, A=c I_H. ∎

This is elementary linear algebra on a graphic matroid, not an asserted new graph theorem.

## 4. Generator identifiability theorem

**Theorem.** Under Section 1, the baseline stationary distribution and finite intervention response vectors determine W up to a single positive scalar. Both directed rates on every graph edge, all rate ratios, the direction of each stationary current, and dimensionless cycle affinities are determined. Absolute rates and entropy production per unit physical time are not determined without one clock calibration.

**Proof.** Let V be any other irreducible valid generator compatible with the same π and response lines. From (1), for nonzero numbers α_e and β_e,

W_H d_e=α_e b_e,   V_H d_e=β_e b_e.

Thus A=V_H W_H^−1 obeys A b_e=(β_e/α_e)b_e. The rigidity lemma gives V_H=cW_H. Every x∈R^n decomposes uniquely as x=h+(1ᵀx)π with h∈H. Because Vπ=Wπ=0, Vx=cWx for all x. The scalar must be positive: both generators have a positive off-diagonal entry, and multiplying a nonzero generator by a negative number violates the nonnegative-rate condition. ∎

The argument actually proves uniqueness in a larger class: any linear V with 1ᵀV=0, Vπ=0 and Vd_e parallel to b_e must be cW, even if some parallelism coefficients vanish. Indeed A need not be invertible for the rigidity lemma. Consequently the homogeneous reconstruction system below has exactly a one-dimensional nullspace, with no hidden singular candidate solutions.

## 5. Explicit linear reconstruction

Use n² real unknown entries V_ij. Impose:

1. 1ᵀV=0.
2. Vπ=0.
3. For every selected e=(a,b), (Vd_e)_i=0 for every i not equal to a or b.

Because of condition 1, the last constraint also implies (Vd_e)_a+(Vd_e)_b=0; hence it is exactly parallelism with b_e. Known absent-edge entries may be set to zero but are not needed for the uniqueness theorem. Fix −tr V=1 to choose an arbitrary time convention. A valid nonzero generator has negative trace, so the normalized solution is unique. Verify its off-diagonal positivity and the declared sparsity; violations in exact data refute the model/control assumptions.

All constraints are linear in V, despite the uncalibrated intervention sizes. Polynomial-size linear algebra reconstructs V from exact rational input. This statement concerns arithmetic input size, not the physical cost of obtaining exact probabilities.

If an intervention response is exactly zero, Section 2 supplies the additional equation V_ba π_a−V_ab π_b=0. Merely inserting d_e=0 into the ray equations discards this information. In noisy data, thresholding a small response as exactly zero is unjustified without an uncertainty analysis.

## 6. Explicit triangle and direction recovery

Take forward rates 2 on 1→2→3→1 and reverse rates 1. Then

W = [−3,1,2; 2,−3,1; 1,2,−3],    π=(1,1,1)/3.

Doubling only the two rates on edge {1,2} yields

π^(12)=(10,13,12)/35,

d_12=(−5,4,1)/105,

W d_12=(1,−1,0)/5.

Reverse all currents by interchanging forward and backward rates. The stationary distribution is still uniform, but the same edge intervention yields d'_12=(4,−5,1)/105, which is not collinear with d_12. Thus the method distinguishes circulation direction even though the unperturbed histogram cannot. Global positivity selects the sign of the reconstructed generator; an arbitrary sign convention for response rays does not create a physical time-reversal ambiguity.

For the first model, the cycle affinity is log[(2·2·2)/(1·1·1)]=log 8. The current magnitude is 1/3 in the arbitrarily chosen time unit. Without a clock, only its normalized magnitude and sign are identifiable.

Exact BigInt rational calculations independently instantiate the algebra for this triangle, its reversed circulation, an asymmetric K4, a figure-eight graph, an equilibrium triangle and a tree. See EXACT_CHECK_RESULTS.txt. These are exact arithmetic checks, not floating-point simulations or an independent proof audit.

## 7. Sharp blind spots and qualifications

### Absolute time

For any c>0, replacing W and every W^(e) by c times themselves leaves all stationary distributions invariant. No number of stationary interventions can identify this common clock. One independently measured positive rate, stationary event count per time, mean first-passage time or relaxation time can calibrate c if correctly matched to the inferred model. Such a measurement must be paid, not silently supplied by a numerical normalization.

### Equilibrium

At detailed balance every j_e=0, so every symmetric edge-barrier intervention leaves π unchanged, including finite simultaneous positive edge scalings. Arbitrarily many equilibrium conductances share the same entire data family. A triangle has three undetermined edge conductances before overall normalization. The method is specifically powered by nonequilibrium circulation, not universally improved by proximity to equilibrium.

### Bridges and articulation blocks

Every bridge has zero stationary current. Its rate ratio is fixed by stationary probabilities but its conductance cannot be obtained by merely scaling that barrier. Two driven triangles sharing only a vertex provide an exact counterexample to a single global clock: the speed of either triangle can be multiplied independently without changing any stationary single-edge intervention distribution. Each triangle has zero net divergence at the shared vertex separately. Scaling its complete generator contribution preserves all stationarity conditions, before and after an intervention. Exact reconstruction has nullity two for the displayed figure-eight example.

The theorem does not assert a complete classification for arbitrary partial interventions or zero-current nonbridge edges. A spanning, cycle-connected set of nonzero response edges is sufficient. Extra topology or calibrated interventions may identify cases outside this sufficient condition.

### Hidden channels and states

Observing an aggregate state does not guarantee that it evolves as a Markov state. Hidden states, memory, parallel reservoir channels, intervention-induced new states and common-mode drift can invalidate the generator or thermodynamic interpretation. In particular, an aggregate generator does not resolve entropy production dissipated in invisible parallel channels.

### State-energy intervention is not interchangeable

If an operation multiplies every outgoing rate from a state a by a common factor t, its stationary distribution is proportional to π with π_a replaced by π_a/t. This contains no new transition-structure information. It follows directly by writing W'=W D and π' proportional to D^−1π. Thus ordinary changes in state residence energy cannot be advertised as the required edge-barrier control.

## 8. Conditioning and finite sample cost

Let L be the real linear constraint matrix from Section 5, including column conservation and stationarity but excluding trace normalization. Under the theorem ker L=span(vec W). Normalize w=vec W/||W||_F. Let σ>0 be L's smallest nonzero singular value in the declared unweighted row convention. With estimated constraint matrix Lhat=L+E, ||E||_2≤ε, choose a unit vector what minimizing ||Lhat what||. Since w is feasible with residual at most ε, ||L what||≤2ε. Decomposing what along w and its orthogonal complement gives

sin angle(what,w) ≤ 2ε/σ.

After selecting the consistent sign, ||what−w||_2≤2√2 ε/σ when the bound is informative. This does not assume a well-conditioned physical experiment; σ explicitly records its failure. Trace normalization adds its own division sensitivity. Relative error for an extremely small individual rate is not controlled by a global Frobenius error alone.

For m interventions and one baseline, suppose each stationary distribution is estimated from M independent state samples. Hoeffding and a union bound imply, with probability at least 1−α, every probability-coordinate error is at most

η = sqrt{log[2n(m+1)/α]/(2M)}.

Each response-coordinate error is at most 2η. For the above row construction, an upper bound is

||E||_2 ≤ ||E||_F ≤ η sqrt{n²+4mn(n−2)}.

This conservative bound pays the common baseline error without assuming independent response vectors. It applies to the nonzero-response theorem, not discontinuous classification of uncertain zero edges. Effective independent samples require equilibration and correlation control; M camera frames are not automatically M samples. Each intervention has a mixing/settling cost. Near equilibrium response magnitudes and the usable σ can collapse, so sample cost can diverge. No noise-independent or near-equilibrium advantage is claimed.

## 9. Strongest prior methods and actual physical opening

Established Markov static-response theory already provides response identities and incidence-based topology constraints (Aslyamov and Esposito, PRL 133,107103, 2024). Exact finite-edge changes in steady probabilities are covered by mutual-linearity results (Bebon and Speck, PRL 136,137401, 2026). Modular response analysis has inferred normalized network interactions from steady-state perturbations since 2002 and has a substantial identifiability/noise literature. General stationary-moment parameter inference also predates this construction. The theorem is therefore not evidence that inference from stationary perturbations is a new concept. Whether this specific incidence-ray inverse uniqueness statement is already published remains open.

Direct generator inference from well-resolved trajectories estimates counts of each transition divided by residence time, obtains absolute rates and works at equilibrium. It requires neither independent control of every edge nor m separate stationary settings. Given those measurements at comparable precision, our method has no established information or total-cost advantage.

The potential narrower opening is a system whose individual states can be sampled but whose transitions are too fast, destructive to follow, or inaccessible to continuous monitoring, while its individual bidirectional barriers can be changed without changing the rest of the dynamics. A driven three-state mesoscopic transport circuit is a possible model platform, not a demonstrated implementation here. A real experiment must establish selective barrier control, full state observability, model validity, baseline stability and a cost advantage over ensemble transient-response or correlation measurements. Strong endpoint control is not free.

## 10. Earned scope

The result supplies an explicit inverse theorem, finite-step reconstruction, sign recovery, exact small-network checks, degeneracy examples and a conditional statistical stability bound. It does not yet supply novelty clearance, physical controls, experimentally validated reconstruction, or an exceptional practical capability. Those are the next decisive gates, rather than further algebraic expansion of the same ideal model.

## 11. Stronger-control corollary and reset comparator

The incidence-ray inverse theorem extends beyond symmetric barriers. Suppose an intervention changes only the two directed rates between a and b by arbitrary amounts Δk_+ and Δk_− while preserving a valid irreducible generator. Then

W'=W+b_e(Δk_+ e_a−Δk_− e_b)ᵀ,

and exact subtraction again gives W(π'−π) parallel to b_e. Whenever the measured response is nonzero, the same reconstruction applies with no knowledge of the two perturbation magnitudes. A change of just one directed positive rate by a nontrivial factor guarantees a nonzero response, because the corresponding source-state stationary probability is positive. Therefore equilibrium blindness in Section 7 is specifically a limitation of symmetric barrier control, not of localized interventions generally. Directed edge control can recover an equilibrium generator on a cycle-connected spanning graph up to its global clock. This is a stronger physical intervention that generally changes affinities; it is not a passive barrier adjustment. Exact rational checks include this case.

A strong competing operation uses Poisson resetting. If one can reset the system from every state to a chosen state i at a known rate r, the modified generator is W+r(e_i1ᵀ−I). Its stationary distribution p_i satisfies (rI−W)p_i=re_i. Collecting n such stationary vectors into P gives

P=r(rI−W)^−1,     W=rI−rP^−1.

This elementary consequence of established stochastic-resetting resolvent theory obtains absolute rates, works at equilibrium and does not require a cycle-connected original graph. It uses only stationary populations but requires global reset control and a known physical reset clock. This is an analytical comparator, not a claim that a particular published instrument implements the inversion. It sharply limits any assertion that our construction newly makes dynamics observable from snapshots. The possible distinction is weaker and uncalibrated *local* edge control, with a narrower topology class and an unavoidable remaining clock ambiguity.

## 12. Exact finite-intervention consistency check

Ray consistency is necessary but does not alone certify the promised symmetric barrier experiment. After reconstruction, for each nonzero response calculate α_e from Wd_e=α_e b_e and D_e=u_eᵀπ^(e). Symmetric scaling compatibility requires D_e≠0 and

t_e = 1−α_e/D_e >0,    t_e≠1.

These quantities are invariant under the unknown overall scale of W. If they hold, substituting the recovered t_e gives [W+(t_e−1)b_eu_eᵀ]π^(e)=0 exactly. Its rates are positive on the original irreducible graph, so π^(e) is indeed its unique stationary distribution. Thus the test is sufficient as well as necessary for each symmetric finite-edge intervention. It complements generator positivity, state normalization and topology checks. Nonzero responses with D_e=0, or a reconstructed nonpositive t_e, refute symmetric-barrier consistency even if the response rays fit. They may still fit the broader edge-local intervention model, which must be stated separately.

For an exact zero response under a known nonunit symmetric intervention, j_e=0 is necessary and sufficient; its amplitude cannot be recovered from unchanged stationary data. Finite sample errors require a tolerance/confidence analysis rather than exact division near D_e=0.
