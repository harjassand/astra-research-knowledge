# Protected computation controlled by grade boundaries, not a global noise norm

Root construction, 29 October 2026. New representation; independent review recorded separately. Earlier energy-window results remain valid at their pinned scope. Their conservation and retirement premises are sufficient for that method, not necessities for every protected operation.

## 1. The consequential change

The graded proof propagates all motion inside a grade, and all motion after escape, unitarily. Only the edges between successive grades and the final escape edge need norm estimates. A bosonic interaction may therefore be globally unbounded, and actual occupations may grow without a uniform ceiling, while the protected operation still has a finite complete-channel error bound.

## 2. General edge theorem

Let \(P_0,\ldots,P_q,Q\) be orthogonal projectors summing to identity, with \(P=\sum_rP_r\). Memory is included in every sector. Assume the block-diagonal dynamics has normalized unitary propagators on these sectors. Add bounded, strongly measurable, locally integrable edges
\[
K_r(t)=P_rH(t)P_{r-1}\ (1\le r\le q),\qquad
K_{q+1}(t)=QH(t)P_q
\tag{1}
\]
and their adjoints, with no other off-diagonal edges. Define the physical evolution by this bounded interaction-picture perturbation of the direct-sum propagator. The comparison removes only \(K_{q+1}+K_{q+1}^\dagger\). Both are normalized. This specification handles unbounded diagonal generators without relying on formal block matrix elements or changing self-adjoint domains.

Set \(e_r(t)=\|K_r(t)\|\). Then, uniformly on the complete fresh input \(P_0\), including memory and references,
\[
\|(U(b,a)-\bar U(b,a))P_0\|
\le\int_{a<t_1<\cdots<t_{q+1}<b}
\prod_{r=1}^{q+1}e_r(t_r)\,dt_1\cdots dt_{q+1}.
\tag{2}
\]
For a common envelope \(e_r(t)\le h(t)\), with \(\Theta=\int_a^bh(t)dt\),
\[
\boxed{\ \|(U-\bar U)P_0\|\le
\Theta^{q+1}/(q+1)!\ }.
\tag{3}
\]
The complete-channel half-diamond distance is at most the minimum of one and this bound.

**Proof.** In the comparison define \(R_r=\sum_{s=r}^qP_s\). Its internal compressed dynamics is unitary, and its only incoming source is \(K_rP_{r-1}\bar U P_0\). Therefore
\[
\|R_r\bar U(t,a)P_0\|
\le\int_a^t e_r(s)\|P_{r-1}\bar U(s,a)P_0\|\,ds.
\]
Bound the first lower factor by one and subsequent factors by the preceding tail. Iteration supplies q ordered integrals. Bounded-perturbation Duhamel comparison has source only \(K_{q+1}P_q\bar U P_0\), since the comparison stays in P. The actual propagator multiplying that source has norm one, regardless of its Q dynamics. The last integral gives (2); the common-envelope simplex gives (3). Tensoring a reference does not change the norms. □

No bound on \(\|H\|,\|V\|\), or \(\|QHQ\|\) is used. Separately well-posed Hamiltonians with merely formal block identities are not enough: they must realize the specified bounded perturbation, including their domains.

## 3. Logical meaning and many lifetimes

On P require the reviewed factorization
\[
PHP=J[H_L(t)\otimes I_S+I_L\otimes H_{SM}(t)]J^\dagger.
\tag{4}
\]
The first term implements the intended logical gates, including inter-block gates. Memory can be strong, driven, correlated and non-Markovian.

During each fresh block lifetime, all other interactions and every implemented control preserve its grades as operators. The selected interaction supplies (1). Targets start in \(P_0\) before their exposure; holding and handoff times are included. The acquired logical handoff fixes the old logical factor and moves the unknown state to a fresh block.

The same lifetime telescope gives
\[
\boxed{\quad \tfrac12\|\mathcal E-\bar{\mathcal E}\|_\diamond
\le\min\{1,\sum_j\Theta_j^{q_j+1}/(q_j+1)!\}.\quad}
\tag{5}
\]
Common later evolution is resummed, not norm-bounded.

A retired block may return as memory and need not preserve its old energy or code space. Its interactions must still obey each currently active block's edge/control interface. An old oscillator driving a bounded spin bus is allowed; directly using its unbounded annihilator as the active coupling coefficient needs another estimate. Freshness cannot be supplied by restarting a clock. The channel domain includes the declared encoding and replacement admissions, not arbitrary unencoded bosonic inputs.

## 4. Explicit bosonic edge bound

Use the reviewed code with \(N=(q+1)^2\), all ladder words through length q, and admitted support in total numbers \(N-q,\ldots,N+q\). Projected ladders are logically blind and nearest-grade, and only the last grade can escape.

Let
\[
V_j=a_j^\dagger C_a+a_jC_a^\dagger+
    b_j^\dagger C_b+b_jC_b^\dagger ,
\tag{6}
\]
with bounded bath coefficients on the complete supplied memory. They need not lower a conserved bath charge and may be unequal, noncommuting or driven. Exact ladder norms on the source support imply
\[
\|V_j(t)P_j\|\le
[\sqrt{N+q}+\sqrt{N+q+1}]
[\|C_a(t)\|+\|C_b(t)\|].
\tag{7}
\]
Memory is not truncated. Each edge is a compression of \(V_jP_j\), so (7) is a common envelope. Put
\(G_j=\int_{\text{lifetime }j}(\|C_a(t)\|+\|C_b(t)\|)dt\).
Then
\[
\tfrac12\|\mathcal E-\bar{\mathcal E}\|_\diamond
\le\min\left\{1,\sum_j
\frac{\big([\sqrt{N+q}+\sqrt{N+q+1}]G_j\big)^{q+1}}
{(q+1)!}\right\}.
\tag{8}
\]

The physical source need not remain in the number band. The band is the domain of \(V_jP_j\), not an invariant space for \(V_j\). The comparison stays admitted and (2) charges actual escape.

Since \(N+q+1=(q+1)(q+2)\le\tfrac32(q+1)^2\),
\[
\Theta_j\le\sqrt6\,G_j(q+1).
\tag{9}
\]
For \(G_j\le G\) and \(e\sqrt6G<1\), the designated contribution is at most \(W(e\sqrt6G)^{q+1}\). This is a sufficient regime with acquired controls and supply, not a device threshold. Removal of the global norm-domain obligation is the central change.

## 5. Well-posed driven and returning-bath realization

Take finitely many bosonic blocks for a finite workload and a finite spin bus. Allow bounded piecewise-continuous spin driving, including excitation-nonconserving terms. Contacted blocks couple through (6) with bounded piecewise-continuous spin coefficients. Retired blocks may recontact the bus. No per-wire bath-charge conservation or permanent decoupling is required.

Free oscillator motion and acquired ET controls conserve total photon number. In every finite total-number sector they define finite Hermitian matrices and normalized propagators. Their direct sum, with spin driving, is a strongly continuous base propagator. The canonical arbitrary-q ET extension is bounded; the explicit q=1 conserving polynomials also define finite matrices in each number sector.

A direct existence argument avoids a physical cutoff. In the base interaction picture, the total ladder interaction changes total photon number by at most one and has norm at most \(C(t)\sqrt{n+1}\) on support through n. Here C is a finite sum of supplied coefficient norms. On an input supported through \(n_0\), its kth Dyson term is bounded by
\[
\frac{(\int_a^b C(t)dt)^k}{k!}
\sqrt{\frac{(n_0+k)!}{n_0!}}.
\tag{10}
\]
The ratio tends to zero, so the series converges on every finite interval. Finite total-number cutoffs obey the same bound. Fixed-order terms agree with the untruncated terms once the cutoff is high enough. Propagators and reverse-time adjoints thus converge strongly on the dense finite-number domain, and then on the whole Hilbert space; their limit is unitary. Pinched comparisons have the same number-growth estimate because their projectors commute with total number.

This constructs exact propagators and adds no finite truncation error to (8). The edge proof can be applied at finite cutoffs and passed to the limit with a bound independent of cutoff. A workload may concentrate energy without a uniform global occupation ceiling.

## 6. Universal control and actual readout

The logical X,Z, handoff and number-preserving inter-block ZZ constructions remain at their acquired ET Hamiltonian interface. They commute with every active grade globally, including when another block is inadmissible. Multi-wire composition therefore satisfies (5) without the individual-charge condition of the earlier energy-window method. A common driven spin bus, or correlated bounded-coefficient buses, can remain quantum throughout.

This supplies a conditional H,T,CNOT circuit interface with renewed logical support. It does not show that selective or inter-block controls are cheap, or that their imperfections have the same noise algebra. The complete final counting instrument, collection noise, conditional memory changes and flag costs remain attached to actual readout. A returning missed field cannot be retired by changing its Kraus representation.

## 7. Reach and retained limits

**Coherent protection can be controlled by finite interaction edges touching a protected error hierarchy even when the full noise Hamiltonian and reachable energy support are unbounded.** Logical gates, renewal and returning memory fit the same complete comparison.

The earlier energy-localization theorem remains useful for direct interaction estimates and excitation accounting. Its driven-bath and returning-donor negatives invalidate that global-support method; they do not invalidate this bounded-edge construction.

The obligations remain: fresh encoding, coherent grade-preserving controls throughout execution, bounded coefficients at the complete memory interface, no unmodeled shortcuts across grades, and compatible preparation, holding, measurement and reuse. Unbounded bosonic bath coefficients, white-noise singular limits, early-escape differential-number noise, and unprotected elementary-gate compilation are outside this realization.

There are \(N=O(q^2)\) photons per block and WN across W lifetimes. Growing q can increase control duration and G. Preparation, delivery, model error, readout and logical compilation remain separate contributions to total workload error.

ET gates, graded error spaces, coherent recovery, non-Markovian norm comparisons, energy-constrained methods and unitary resummation are established ancestry. Historical novelty of this bounded-edge formulation is not established. Its value is the proved removal of a false global-norm obstruction, composed with explicit control, handoff and record interfaces. The separate primary-source ledger compares stronger conventional CV fault-tolerance results at their actual noise and acquisition assumptions.
