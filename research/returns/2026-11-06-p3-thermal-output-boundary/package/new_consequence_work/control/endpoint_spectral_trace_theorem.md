# Thermal raw-port obstruction: constructive proof and exact scope

Research date: 2026-11-05. This is the control-composition contribution to the parent manuscript. Earlier accepted bounded-factory and controller results remain at their stated scopes and are not re-audited.

## 1. Scientific question and endpoint contract

Can a known full-rank finite-temperature many-body state always be delivered to arbitrary global trace accuracy through a fixed imperfect local physical endpoint, if arbitrary upstream preparation, computation, cooling, calibration and classical randomization are allowed?

No: below is a connected nearest-neighbor planar family with norm-one positive local terms, a unique product ground state, a uniform spectral gap, and a fixed-temperature, fixed-noise strong converse. The last channel on each selected raw qubit is the fresh unheralded bit flip

\[
\mathcal E_p(X)=(1-p)X+pUXU,\quad U=U^\dagger,\quad U^2=I,\quad0<p<1/2.
\]

Selected ports are independent. All other output qubits may be perfect. Upstream states can be arbitrary and entangled across every cell, ancilla and retained record. An operation or usable fault flag after this final channel, an encoded output, or target-preserving thermalization avoiding this endpoint changes the contract. This is not an impossibility theorem for arbitrary analog Gibbs preparation.

Inverse positivity is established quantum error precompensation. Bouch's complex-time divergence and Pettinari's weak-Gibbsianity theorem already imply bare endpoint fragility. The additions developed here are the positive gapped product-ground model, quantitative normalized witness, and connected trace-distance strong converse against arbitrary upstream correlations. See Section 9 for the close primary comparison.

## 2. Exact criterion and a quantitative trace witness

For full-rank rho, the only candidate preimage is

\[
\sigma_* =\frac{(1-p)\rho-pU\rho U}{1-2p}.
\]

Conjugating its numerator by rho^(-1/2) proves

\[
\sigma_*\succeq0\iff p\le p_{\max}:=
\frac1{1+\|\rho^{-1/2}U\rho^{1/2}\|^2}.
\tag{2.1}
\]

For rho=e^(-beta H)/Z, put

\[
K=\|e^{\beta H/2}Ue^{-\beta H/2}\|,
\qquad\log K^2=D_{\max}(U\rho U\Vert\rho).
\tag{2.2}
\]

Exact inverse negativity alone does not give a useful error floor. For any rank-one projector P define

\[
O=(1-p)P-pUPU,\qquad F=(1-p)I-O.
\tag{2.3}
\]

The inequalities -pI<=O<=(1-p)I make F an effect. Direct calculation gives

\[
\mathcal E_p^*(O)=(1-2p)P\succeq0,
\quad\mathcal E_p^*(F)=(1-p)I-(1-2p)P\preceq(1-p)I.
\tag{2.4}
\]

If Tr(O rho)<=-delta<0, every obtainable output has F expectation at most 1-p, whereas the target has expectation at least 1-p+delta. Hence

\[
\inf_\sigma D(\rho,\mathcal E_p(\sigma))\ge\delta,
\qquad D(\rho,\tau)=\tfrac12\|\rho-\tau\|_1.
\tag{2.5}
\]

If P projects onto an eigenvector psi of energy E, the vacuum Omega has energy zero, and r=|<psi|U Omega>|^2, its vacuum contribution gives

\[
-\operatorname{Tr}(O\rho)\ge
\frac{pr-(1-p)e^{-\beta E}}Z.
\tag{2.6}
\]

The test is a mathematical witness. No efficient or free physical measurement is presumed.

## 3. Positive facilitated Hamiltonian and actual planar geometry

For a rooted tree T with n edges and N=n+1 sites, orient edges away from root o, put n_v=(I-Z_v)/2, and define

\[
H_T=\sum_v n_v+\frac12\sum_{u\to v}n_u(I+X_v).
\tag{3.1}
\]

Every displayed term is positive semidefinite, norm at most one, and annihilates the product vacuum Omega. Since H_T>=sum n_v, the ground is uniquely Omega and the gap is at least one. The root occupation commutes with H_T. Its computational-basis matrix is nonnegative. The onsite gauge product_v Z_v changes +X to -X and makes H_T stoquastic; it changes root X only by an irrelevant sign.

Let s=X_o Omega and y be all occupied. Then

\[
\langle y|H_T|y\rangle=1+3n/2,\qquad\|H_T\|\le2n+1.
\tag{3.2}
\]

### Explicit H-tree

T_0 is one root. For scale h, put L=2^(h-1), draw horizontal unit-edge paths from the root to (+/-L,0), vertical paths to (+/-L,+/-L), and attach four translated T_(h-1) trees at those endpoints. The descendant boxes lie in disjoint open quadrants. Inductively each tree meets its root vertical axis only at its root, so connectors do not cross subtrees. All links are unit square-lattice edges and maximum degree is three.

The physical counts are

\[
n_h=3(4^h-2^h),\quad N_h=n_h+1,
\quad\text{bounding-square sites}=(2^{h+1}-1)^2=(4N_h-1)/3.
\tag{3.3}
\]

Thus subdivision and planar area are counted: no hidden long links or exponential-density embedding. The pattern is not translation invariant.

### Activation orders and hook product

For descendant-subtree sizes s_v, define P(T)=product_(v!=o) s_v. The rooted-tree hook formula counts parent-before-child activation orders as n!/P(T), by recursively interleaving the child-subtree orders. This is prior combinatorial machinery, including Bouch's Lemma 6.2. Each order contributes 2^(-n) to a nonnegative matrix element, hence

\[
\langle y|H_T^n|s\rangle\ge\frac{n!}{2^nP(T)}.
\tag{3.4}
\]

For the H-tree, with N=N_(h-1), L=2^(h-1), V=2N+2L-1,

\[
P_h=P_{h-1}^4
\left[\prod_{k=0}^{L-1}(V+k)\right]^2
\left[\prod_{k=0}^{L-1}(N+k)\right]^4.
\tag{3.5}
\]

The bounds V+L<=6*4^(h-1) and N+L<=3*4^(h-1), summed over scales, give

\[
\frac{\log P_h}{n_h}\le\frac{\log54}{3}
+\log4\left(1-\frac h{2^h-1}\right)<\log16.
\tag{3.6}
\]

Thus P_h<=C^n_h with C=16. Parent and independent audit scripts check the explicit geometry and exact recurrence.

### Modular-norm bounds

The n-th Taylor term gives K>=(beta/(4C))^n. A stronger bound allows activation time t_0 followed by residence on the high diagonal. Semigroup entrywise positivity and scalar Jensen give, for t>=t_0,

\[
\langle y|e^{tH_T}|s\rangle\ge
e^{(t-t_0)(1+3n/2)}\frac{(t_0/2)^n}{P(T)}.
\]

At t=beta/2 and t_0=2/3 this becomes

\[
K^2\ge e^{\beta-4/3}
\exp\{n[3\beta/2-2-2\log(3C)]\}.
\tag{3.7}
\]

For C=16 the coefficient is positive for beta>6.495, so beta=8 proves exact-radius collapse. The main normalized trace theorem below uses beta=12. The weaker beta>64 condition from the single Taylor term is not the strongest conclusion.

## 4. Perron-Frobenius normalized witness

Restrict H_T to root occupation one, a 2^n-dimensional sector. Its graph is connected: activate all sites, then deactivate unwanted sites in reverse tree order. Its diagonal is positive since root occupation remains one. Its Perron eigenvector psi is strictly positive.

H_T preserves the cone of nonnegative coordinatewise increasing functions of descendant occupations. Onsite multiplication by x_v preserves it. An edge term maps

\[
f(x)\longmapsto\frac{x_u}{2}[f(x)+f(x^{(v)})],
\]

where x_u=1 for a root parent. The bracket is independent of x_v, nonnegative, and increasing in all other coordinates; multiplying by x_u preserves this. The normalized limit of H_T^k applied to the all-ones function is therefore increasing. Consequently

\[
\psi(y)\ge2^{-n/2},\qquad
1+3n/2\le E\le2n+1\le3n\quad(n\ge1).
\tag{4.1}
\]

By positivity, symmetry, and (3.4),

\[
E^n\psi(s)=\langle s|H_T^n|\psi\rangle
\ge\frac{n!}{2^nP(T)}\psi(y).
\]

Use n!>=(n/e)^n and P(T)<=C^n to obtain

\[
r:=|\psi(s)|^2\ge A^{-2n},\quad
A=6eC\sqrt2=96e\sqrt2,\quad a:=2\log A\approx11.82184356.
\tag{4.2}
\]

Since H_T>=sum n_v, eigenvalue min-max and scalar monotonicity give

\[
Z\le z^{n+1},\qquad z=1+e^{-\beta}.
\tag{4.3}
\]

This does not invoke the false operator monotonicity of matrix exponentiation. Equations (2.6), (4.1)--(4.3) imply the explicit positive margin

\[
-\operatorname{Tr}(O\rho)\ge\delta_n(p):=
\frac{pe^{-an}-(1-p)e^{-\beta}e^{-3\beta n/2}}{z^{n+1}}
\tag{4.4}
\]

whenever the numerator is positive. Put kappa=3beta/2-a and c=a+log z. At beta=12, kappa approximately 6.17815644>0. If

\[
e^{\kappa n}\ge2(1-p)e^{-\beta}/p,
\tag{4.5}
\]

then

\[
\delta_n(p)\ge\frac p{2z}e^{-cn}>0.
\tag{4.6}
\]

Choose the smallest eligible H-tree. Consecutive positive H-tree sizes have ratio at most six, so n=O(1+log(1/p)). Trace-gap and repetition costs are bounded by powers of p with explicit but very unfavorable constants. This is not a useful engineering threshold.

The same eigenvector yields

\[
K^2\ge re^{\beta E}\ge e^{\beta+\kappa n},\qquad
p_{\max}\le[1+e^{\beta+\kappa n}]^{-1}.
\tag{4.7}
\]

## 5. Strong converse without upstream independence

For m independent final root channels, let the upstream state sigma be arbitrary, including entanglement across cells and retained records. Test each cell with the effect F of (2.3), and put b=1-p. Conditional on any previous cell outcomes, the remaining cell is still the image of its own final channel: local operations elsewhere commute with that channel and condition only its input. Thus every conditional success probability is at most b. Equivalently, for t>=0,

\[
\mathbb E_{\rm out}e^{t\sum_iY_i}
=\operatorname{Tr}\sigma\bigotimes_i
[I+(e^t-1)\mathcal E_p^*(F)]
\le[1+(e^t-1)b]^m.
\tag{5.1}
\]

The output probability of an empirical mean at least b+delta/2 is at most exp(-m delta^2/2). A product target has independent test means at least b+delta, so the probability of the opposite event obeys the same Hoeffding bound. Hence

\[
\inf_\sigma D\!\left(\rho^{\otimes m},
\mathcal E_p^{\otimes m}(\sigma)\right)
\ge1-2e^{-m\delta^2/2}.
\tag{5.2}
\]

A small strictly positive one-cell separation is thereby amplified to nearly orthogonal global outputs against every correlated upstream preparation. This is a channel-image strong converse, not a circuit-depth lower bound.

## 6. Connected planar amplification with fixed-strength interactions

Disconnected tensor products are unnecessary. Place fixed eligible H-tree cells in a row with disjoint bounding squares. Each meets its root vertical axis only at the root. Through that empty axis, add occupation-qubit wires to a horizontal spine above the cells. Add

\[
H_{\rm wire}=\sum_{w\in\mathrm{wire}}n_w
+\eta\sum_{\{u,v\}\in\mathrm{wire\ or\ attachment}}n_un_v,
\qquad0<\eta\le1.
\tag{6.1}
\]

The resulting graph is connected, planar and nearest-neighbor. Maximum degree remains three: each root has two tree edges and one attachment; a spine junction has left, right and downward edges. Wire length is O(sqrt N) per cell, and both total occupied vertices and enclosing row area are Theta(mN). Every term has norm at most one. H_total>=sum_all n_v still proves unique product vacuum and gap at least one.

Condition on the complete wire occupation string; all those occupations commute with the Hamiltonian. The target cells are then independent Gibbs states with Hamiltonians

\[
H_T+t_i n_o,\qquad t_i\in\{0,\eta\}.
\tag{6.2}
\]

The Perron vector psi lies wholly in root sector one and X_o psi in sector zero. With u_1=<psi|e^(-beta H_T)|psi> and u_0=<X_o psi|e^(-beta H_T)|X_o psi>, the conditional mean of O is

\[
\frac{(1-p)e^{-\beta t_i}u_1-pu_0}{Z(t_i)}.
\tag{6.3}
\]

The numerator is no greater than the original negative numerator. Root occupation commutation gives Z(t_i)<=Z(0), so this mean is still at most -delta_n(p), uniformly over all wire strings. Target tests are independent conditional on the wire string, so the same Hoeffding bound survives averaging. The arbitrary-upstream bound (5.1) is unchanged, even when sigma entangles every cell and wire.

Therefore

\[
\boxed{\displaystyle
\inf_\sigma D\!\left(\rho_{m,n}^{\rm connected},
(\mathcal E_p^{\otimes m}\otimes\mathrm{id})(\sigma)\right)
\ge1-2\exp[-m\delta_n(p)^2/2].}
\tag{6.4}
\]

At fixed beta=12 and p>0, choose n by (4.5), then m>=2 delta_n(p)^(-2) log(2/epsilon) makes the distance at least 1-epsilon. Neither temperature nor connector strength vanishes with the array size. The proof applies to any classical connector graph inducing nonnegative root fields; the row supplies the fully explicit bounded-density layout.

### 6.1 One graph sequence independent of p

Use scale h cells with n_h edges and m_h=ceil(exp[(2c+1)n_h]) cells. This sequence depends on fixed beta, not on p. For every fixed p>0, (4.5) eventually holds and

\[
m_h\delta_{n_h}(p)^2\ge\frac{p^2}{4z^2}e^{n_h}\longrightarrow\infty.
\]

Thus one specified connected planar target sequence has trace distance tending to one from the entire attainable image for every fixed nonzero endpoint rate.

### 6.2 One fixed infinite local interaction pattern

The independently checked refinement in `../bounded/planar_endpoint_independent_audit.md` uses cell j of type

\[
h(j)=1+\lfloor v_2(j)/3\rfloor.
\]

Align each H-tree's bounding-box bottom at height two, run its root wire downward through the empty axis to a common spine at height zero, and put consecutive boxes in disjoint horizontal intervals. This defines one locally finite, nearest-neighbor, degree-three aperiodic Hamiltonian with the same local terms and fixed eta. It is independent of p.

Among J=8^m cells, type h<=m occurs exactly 7J/8^h times; the last cell has type m+1. Since N_h<=3*4^h, total tree qubits are at most 33J. Wires and horizontal span are O(J), maximum height is O(J^(1/3)), and a containing rectangle has O(J^(4/3)) sites. Unoccupied fabrication area is not silently free.

For each fixed p>0 choose one eligible type h*. Its occurrence count tends to infinity at positive asymptotic frequency. Apply the witness only to that type. The uniform conditional target bound and arbitrary-input output bound still hold, so trace distance tends to one along consistent finite-volume prefixes of this same interaction. This establishes zero size-uniform terminal-BSC tolerance for one fixed local pattern, rather than selecting a new Hamiltonian after p is known.

## 7. Consequences that a local mixedness argument misses

### Local marginals remain uniformly interior

For any local Hamiltonian split H=I_S tensor H_far+K with ||K||<=J_S. For every unit local a and eigenvector j of H_far, scalar Jensen gives

\[
\langle a,j|e^{-\beta H}|a,j\rangle
\ge e^{-\beta J_S}e^{-\beta E_j}.
\]

Eigenvalue min-max bounds Z<=d_S exp(beta J_S) Z_far. Summing over j proves

\[
\rho_S\succeq e^{-2\beta J_S}I_S/d_S.
\tag{7.1}
\]

For the degree-three norm-one models here, J_S<=4|S|. Every fixed-size marginal thus has a volume-independent interior bound, while a single root noise channel has exponentially vanishing global positivity radius. Marginal full rank does not supply the correlated apparatus preimage.

Explicitly, for an isolated H-tree the root sectors obey H_1=H_0+V with I<=V<=3I. Eigenvalue monotonicity gives

\[
\frac1{1+e^{3\beta}}\le\Pr_\rho[n_o=1]
\le\frac1{1+e^\beta}.
\tag{7.2}
\]

The one-qubit marginal has a bit-flip precompensation radius bounded below uniformly in volume; the actual correlated Gibbs state does not.

### Bounded mean disturbance versus an extensive worst-direction divergence

For a Gibbs state and involution U,

\[
D(U\rho U\Vert\rho)=\beta\operatorname{Tr}\rho(UHU-H).
\]

Only the root onsite and two outgoing terms change under X_o, giving

\[
D(X_o\rho X_o\Vert\rho)\le3\beta,
\quad
D_{\max}(X_o\rho X_o\Vert\rho)\ge\beta+\kappa n.
\tag{7.3}
\]

The connected wire raises the mean bound by at most eta beta<=beta. Bounded local energy disturbance, bounded ordinary relative entropy, uniform ground gap and uniform local full rank do not imply size-independent global endpoint tolerance. The ground gap alone does not establish finite-temperature clustering or absence of all thermal phase transitions.

### Strong upstream methods and genuine bypasses

The infimum in (6.4) ranges over every density matrix. It already grants more upstream resources than ordinary fault tolerance, qLDPC interfaces, optimum precompensation SDPs, ideal Gibbs sampling, autonomous preparation, or classically randomized noisy factories. Their preparation time, calibration, routing and energy cannot overcome this unavoidable channel-image boundary at the same raw endpoint. The theorem is not a total-resource advantage for a competing preparation algorithm.

A physical bypass must change an actual interface: make the effective terminal rate decrease with size, recover after the stated channel, obtain a usable fault flag, deliver an encoded representation, or use target-preserving final thermalization instead of this residual noise channel. Those alternatives are not ruled out. Earlier one-dimensional bounded-factory preparation remains intact at its actual source/channel/control scopes.

## 8. Separate translation-invariant bulk corollary

This optional corollary uses Pettinari's full-square spanning-tree lemma. It does not inherit the connected root-field amplifier, because the root occupation here need not commute with H.

For an open dyadic square of N=L^2 sites, L=2^k>=2, use the fixed translation-invariant bulk interaction

\[
H_\Lambda=\sum_i n_i+
\frac14\sum_{i,j:\ \mathrm{ordered\ nearest\ neighbors}}n_i(I+X_j).
\tag{8.1}
\]

The two directions on each edge together have norm at most one and are positive. Again H>=sum_i n_i, yielding unique product ground and gap at least one. An onsite Z gauge makes it stoquastic.

The nonempty-configuration sector is irreducible: any seed reaches all occupied and vice versa while retaining a suitable occupied ancestor. Extend its Perron vector by zero at vacuum. The same increasing-cone argument applies, so psi(all occupied)>=2^(-N/2). Put m=N-1. Its top eigenvalue satisfies

\[
1+3m/2\le2N-\sqrt N\le E
\le3N-2\sqrt N\le4m.
\tag{8.2}
\]

Pettinari's Lemma 2.5 supplies a corner-rooted spanning tree with hook product at most C_0^N, where

\[
C_0=2^{9/2}6^{1/4}\approx35.41382143.
\]

The exponent is N, not N-1; its prefactor must be retained. Each activation path contributes 4^(-m). The same eigenvector argument gives

\[
r\ge B_0A_{\rm TI}^{-2m},\qquad
B_0=(2C_0^2)^{-1},\qquad A_{\rm TI}=16eC_0\sqrt2.
\tag{8.3}
\]

Since 2 log A_TI approximately 15.37252898, fixed beta=16 gives kappa_TI=3beta/2-2log A_TI approximately 8.62747102>0. A final corner bit flip has

\[
p_{\max}\le[1+B_0e^\beta e^{\kappa_{\rm TI}m}]^{-1},
\tag{8.4}
\]

and, whenever positive, the trace gap

\[
\delta\ge
\frac{pB_0A_{\rm TI}^{-2m}-(1-p)e^{-\beta}e^{-3\beta m/2}}
{(1+e^{-\beta})^{m+1}}.
\tag{8.5}
\]

Thus a fixed translation-invariant bulk interaction with positive terms, uniform gap, product ground and a full-square physical layout has exponentially vanishing exact endpoint radius and a nonzero finite-volume trace gap. This is not a claim that trace distance tends to one on one growing square. Independent copies amplify but do not preserve global translation invariance. Root occupation does not commute with (8.1); the H-tree connected-field argument cannot be imported without a new proof.

## 9. Strongest primary comparison and actual novelty scope

**Zhang, Li, Lu, Yuan, Duan, Quantum error pre-compensation for quantum noisy channels**, arXiv:2309.01434; Physical Review A 106, 042440. Primary PDF: <https://arxiv.org/pdf/2309.01434>. Inverse-channel feasibility and optimal approximate precompensation through convex optimization are prior. Equations (2.1)--(2.6) specialize that established mathematics.

**Bouch, Complex-Time Singularity and Locality Estimates for Quantum Lattice Systems**, arXiv:1011.1875; Journal of Mathematical Physics 56, 123303. Primary PDF: <https://arxiv.org/pdf/1011.1875>. It supplies lattice-tree growth orders and a translation-invariant two-dimensional imaginary-time divergence. The complex-time growth obstruction is prior. Its finite-range one-dimensional locality theorem is compatible with the accepted earlier 1D preparation result; one must not extend the all-complex-time statement to arbitrary exponentially decaying interactions without its own assumptions.

**Pettinari, A Finite-Range, Translation-Invariant Counterexample to Weak Gibbsianity**, arXiv:2610.41871v2, 2 November 2026. Primary PDF: <https://arxiv.org/pdf/2610.41871v2>. The retrieved full text is `weak_gibbs_2610_41871.pdf` and its text extraction in this directory. The model J sum_(ordered nn) n_i X_j, using rho proportional to e^(+beta H), already has positive facilitated growth and vacuum rare-event amplification. Remark 2.8 immediately gives a bare endpoint corollary: if b is vacuum probability and a is probability of only the designated boundary-root excitation, its finite-volume inequality gives

\[
a+b\ge e^{c|X|-2J\beta}b.
\]

Positivity of the bit-flip preimage on vacuum forces

\[
p\le\frac b{a+b}\le e^{2J\beta-c|X|}.
\tag{9.1}
\]

Thus discovering an exponential local endpoint threshold alone would fall short of this primary. Section 8 directly uses its Lemma 2.5 and preserves the C_0^N bookkeeping. Pettinari's facilitated growth and rare-event mechanism must be credited; its displayed model is not a positive Hamiltonian with the claimed unique gapped product ground.

The contribution developed here is therefore the conjunction of positive norm-bounded local terms, unique gapped product ground, stoquastic gauge, quantitative normalized error margin, fixed-strength connected planar amplification against all entangled upstream states, and the explicit failure of local mixedness and average disturbance to certify endpoint feasibility. This is not a discovery of inverse feasibility, facilitated growth, or exponential operator-order ratios in isolation. The primary texts checked do not supply this full conjunction; that scope comparison is not an exhaustive historical priority claim.

The full comparator analysis is in `../comparator/endpoint_and_fermion_primary_comparison.md`. It also records why a fermionic lightcone route does not survive freely permitted measurement-generated classical feedforward without new causal resource accounting; that discarded route is not used here.

## 10. Verification and retained limitations

Parent and independent scripts verify the H-tree coordinates, edges, degree, physical counts and hook recurrence. The spectral inequalities, Perron monotonicity, normalized witness, correlated-input strong converse and connected-wire proof were independently checked in `../bounded/planar_endpoint_independent_audit.md`. These are algebraic arguments, not extrapolations from a finite numerical spectrum.

The temperature in norm-one units, eligible cell sizes, witness gaps, repetitions, physical occupied volume and enclosing area remain explicit. Constants can be enormous and are not hidden in efficiency language. This result claims no practical experiment, favorable engineering threshold, energy advantage, general sampling hardness, or universal obstruction to analog thermalization. It requires no new experiment, spending or external worker. The previously earned preparation, controller, register, passive-bath and other results retain their original scopes.
