# Shared quantum spectator bath: what the guard certificate actually buys

31 October 2026. Separate candidate extension and consequence assessment. The reviewed occupation theorem, physical-unit corollary and executable qubit compiler are unchanged. This note is not yet independently reviewed. It is a mathematical admission corollary, not a protection-device construction or a new threshold theorem.

## 1. Exact additional interface

Let G denote the finite guard-qubit register, S the scheduled logical system and E a shared quantum spectator. Initially G,S,E and an arbitrary reference can be arbitrarily correlated. The loss/injection input fields remain initialized as in the specified Markov jump-history dilation. The extension does NOT admit arbitrary correlated incoming loss fields.

First take finite-dimensional E of unrestricted dimension. Permit an arbitrary bath-only Hamiltonian H_E(t), with no norm or spectral parameter in the admission bound. Replace scalar hopping coefficients by operators on E:

  H_transport(t) = sum_{i<j} [sigma_i^+ sigma_j^- tensor T_ij(t)
                             + sigma_j^+ sigma_i^- tensor T_ij(t)^dagger].

The physical bounds t_ij >= sup_t ||T_ij(t)|| are actually acquired. Set t_ji=t_ij and t_ii=0. With minimum guard loss lambda>0, require

  beta = max_i sum_j t_ij/lambda < 1/2,  gamma=1-2 beta.

Injection remains bounded by a per guard in physical units. The declared guard loss and injection operators act trivially on E. Additional Hermitian guard/bath terms that commute with every occupation n_i may be arbitrarily large; they do not contain an uncharged logical-system operation.

At each scheduled location l, of duration at most tau, permit

  K_l(t) = sum_{i in D_l} n_i tensor A_li(t) + Delta_l(t),

where A_li acts on the declared system patch AND E, is Hermitian, and has acquired norm at most c. Delta_l is a Hermitian residual on the same system patch and E, acts as identity on guards, and has integral norm at most epsilon_ctl. These are actual unwanted interactions. Intended gates are acquired system-only operations. Every idle and every residual logical interaction has a location; a source index has at most one simultaneous location assignment, |D_l|<=g. A shared E is not a license for undeclared system support or a global faulty controller. All unselected real interactions remain ON.

The constant c is the actual interaction strength, not a normalization guessed from an unavailable exact norm. Explicit bounded Pauli/operator expansions with certified coefficient norms suffice; input acquisition and hardware implementation remain charged.

## 2. The operator-valued transport inequality

For V_u=product_i(I+u_i n_i), 0<=u_i<=1, tensor identity on S,E, consider an edge i,j. On the guard 01/10 block its commutator has the form

  [[0, X], [X^dagger, 0]] tensor V_rest,
  ||X|| <= t_ij |u_i-u_j|.

For every bounded operator X, this Hermitian block is <= ||X|| I. This follows from 2 Re<a,Xb> <= ||X|| (||a||^2+||b||^2), and holds with arbitrary entangled spectator/reference vectors. Hence

  i[H_ij,V_u] <= t_ij(u_i+u_j)
       [n_i V_u/(1+u_i) + n_j V_u/(1+u_j)].

On 00 both sides vanish; on 11 the left side vanishes and the right side is positive. No commutation among distinct T_ij, no classical bath path and no stationary bath state are assumed. Noncommuting edges sharing E are summed as operator inequalities, not factorized.

Every real n_i A_li and every real Delta_l commutes with V_u, even when its E action fails to commute with H_E or another location's E action. H_E also commutes with V_u. Complexifying selected K_l by z_l, |z_l|<=R, contributes at most

  2 R c sum_{i in D_l} n_i V_u + 2 R ||Delta_l|| V_u

to the weighted non-TP adjoint evolution. These are exactly the terms of the original proof in physical units. The loss and injection calculations are unchanged.

## 3. Complete selected-history bound

Use a SINGLE common jump-history dilation for all complex z, including spectator E in its input and output. Bath-only evolution is not replaced by a classical random trajectory or traced out before defining amplitudes. Set v_i=2Rc at selected active incidences and zero elsewhere. In backward physical time choose

  dot u_i = -lambda u_i + (sum_j t_ij)u_i + sum_j t_ij u_j
            + v_i(1+u_i),   u(0)=0.

Its Metzler linear part has both row and column sums <= -gamma lambda. For 1<R<=gamma lambda/(8c), the same boundary and convolution arguments give

  sum_i u_i(initial) <= 4 R c g |S|/(gamma lambda),
  integral sum_i u_i(t)dt <= 4 R c g |S| tau/(gamma lambda).

The weighted CP non-trace-preserving evolution therefore bounds the common dilation by

  ||W(z)||^2 <= exp[ (4 R c g(1+a tau)/(gamma lambda)
                      + 2 R epsilon_ctl) |S| ].

The norm is on arbitrary G,S,E,reference inputs with the loss/injection fields initialized. Multivariate Cauchy extraction of at least one insertion at every selected location gives

  ||E(S)|| <= eta(R)^|S|,
  eta(R) = exp[R(2 c g(1+a tau)/(gamma lambda)+epsilon_ctl)]/(R-1).

Thus the already reviewed optimized physical-unit bounds remain valid. With epsilon_ctl=0 and R0=gamma lambda/[8 c g(1+a tau)]>=2,

  eta <= 16 exp(1/4) c g(1+a tau)/(gamma lambda).

With residuals use R=min(R0,1/(2 epsilon_ctl))>=2 and the previously proved max bound. The c=0 branch is the ordinary integrated residual bound, not division by zero.

This is an inclusive AMPLITUDE estimate, not a joint fault probability. The established initialized-isometry fault-tolerance receiver still needs actual gadgets, preparation, measurement, routing, controller support and entropy-removal implementation. No new numerical threshold is supplied.

## 4. Unlimited bath bandwidth is a domain statement, not a free oracle

For finite E, bounded measurable Hamiltonians suffice directly. Constants do not depend on ||H_E||, dim(E), its correlation time, Gaussianity or spectrum. The actual apparatus need not implement a numerical model of its spectator Hamiltonian to use a uniform norm certificate.

An infinite-dimensional E can be admitted only with an explicit existence premise: H_E(t) generates a strongly continuous unitary propagator, and the remaining E-valued coefficients are uniformly bounded and suitably strongly measurable. Pass to its interaction picture. The propagator acts only on E, commutes with V_u and preserves every acquired coefficient norm. The remaining bounded-perturbation/jump-history construction has the same compact-z bounds. This extends the estimate without asserting existence for an arbitrary unspecified unbounded time-dependent operator. The finite guard jump operators remain bounded. Unbounded T_ij or A_li are NOT admitted by declaring the spectator arbitrary.

Common jump-history analyticity is unchanged: after removing H_E, every z-dependent perturbation is bounded on finite time intervals, and the jump-sector squared-norm majorant is summable. The proof never asks for coherent access to exp(-it H_E), inverse bath fibres, bath state preparation or a spectral reconstruction.

## 5. A genuine limitation: a guard cannot be created by notation

Suppose the actual unwanted coefficient on an added guard is I_G tensor B, with B invertible on the degrees being encoded. It is invertible. Unitary conjugation preserves rank and kernel, so no unitary relabeling can turn it into Q_G tensor C with nonzero transparent P_G=I-Q_G. Appending a passive guard does not create a dark interaction sector. This is a restricted rank obstruction, not a no-go against engineered dissipative encoding, error correction, enlarged logical/bath decompositions or approximate decoupling.

A direct operational counterexample is an unguarded c Z_S tensor Z_E with E initialized in a Z eigenstate. Take guard injection and transport zero and let loss lambda grow without bound. At time pi/(2c) the system undergoes a Z error up to phase, independent of lambda. It must be included in Delta with integrated norm pi/2. Omitting it would manufacture a false arbitrarily small certificate. Spectator freedom therefore buys no suppression of generic unguarded bath noise.

More generally, for a declared expansion sum_alpha B_alpha tensor A_alpha, a sufficient transparent guard sector is the COMMON kernel of all Hermitian B_alpha. Individual small expectations or one stationary covariance do not identify it. A finite rational common-kernel computation can acquire this sector from a known local model; it cannot establish the correctness of that model from finite uncontrolled measurements.

Approximate structure needs care. A small residual on S,E that is guard-independent commutes with V_u and enters epsilon_ctl exactly. A small guard-CREATING residual does not commute with the weight: its REAL unselected part changes occupation and cannot be hidden in the selected-location epsilon budget. It needs its own generator/activation inequality, or another valid analysis. This is precisely why a raw local-operator drift verifier is a meaningful next acquisition task.

## 6. Constructive mixed transparent sector, with the price visible

A finite test device has a qutrit guard with Q=|2><2| and P=|0><0|+|1><1|. Actual unwanted interactions are Q tensor A_SE, with bounded A_SE. Two guard loss operators sqrt(lambda/2)|0><2| and sqrt(lambda/2)|1><2| give G^dagger Q=-lambda Q. Injection sqrt(a)|2><0| is ongoing, not omitted. An arbitrary Hamiltonian acting within P tensor E and within Q tensor E commutes with Q, including a very large ground-sector mixing term and fully non-Markovian spectator dynamics. No pure state within P needs to be prepared.

For V=I+uQ, loss is -lambda uQ and injection is a u|0><0| <= a uV. The one-cell certificate follows directly. A family of such guards with admitted transport satisfies the same type of bound. This example explains what local operator acquisition would recognize: a transparent mixed/gauge sector and a dissipative drift, not a supplied pure reference.

It is still a DECLARED apparatus. Creating the Q-controlled coupling, selective loss with rate lambda, bounded injection and actual logical gates is a real physical requirement. No circuit in this note converts an unknown system-bath interaction to this form. A passive basis change cannot do so in the full-rank example above. Ordinary dark-state/DFS engineering, dissipative stabilization, decoupling and error-correcting encodings receive the same operator data and must be compared at their real implementation costs.

## 7. Strong ordinary comparison and decision

Arbitrary bath memory and unknown bath Hamiltonian are already admitted by conventional local non-Markovian threshold results; this is not new merely because E is shared. Ng--Preskill explicitly contrasts arbitrary-bath operator-norm conditions with its Gaussian correlation criterion (introduction and Eq27). Preskill's many-body noise condition likewise allows general bath dynamics while paying locality-weighted interaction norms. See the primary sources:

- https://preskill.caltech.edu/pubs/preskill-2009-gaussian.pdf
- https://arxiv.org/html/1207.6131v2
- https://arxiv.org/html/quant-ph/0504218v3

The distinction here is the acquired microscopic admission scale: a guarded coupling of size c can have a large raw c tau but a small all-selected amplitude proportional to c(1+a tau)/lambda, provided its actual loss/injection/transport and guard structure are certified. Gaussian/Wick or bath-spectrum acquisition is unnecessary under these different premises; conversely unbounded oscillator couplings handled by a Gaussian theorem are outside this norm-bounded spectator statement. Neither result dominates wholesale.

Previously read Astra N951 already retains an arbitrary shared bath and actual finite-key control errors; N1467/N1483 already provide other signed-path/code receivers. Their precise hashes and scopes are in PRIMARY_COMPARISON_AND_CONSEQUENCE_BOUNDARY.md. This extension does not recreate those bridges or establish superiority over their strongest physical admissions. The exact requested latest P2 commutator-sensitive card remains unlocated; no priority conclusion is inferred.

Judgment: the spectator extension is a useful, straightforward operator-valued corollary of the existing weight proof. Its potentially meaningful information saving is conditional: local guard/transport/injection norm certificates suffice without reconstructing an arbitrary spectator spectrum or initial state. It supplies NO generic hardware method for earning those certificates. Further work should target acquiring and checking the local transparent sector plus drift from actual local operators, including charged source creation, or a concrete physical implementation with an ordinary comparator. Another bath family or a stronger adjective for arbitrary memory would not close that gap.

### Leakage-removal comparator precision

Aliferis--Terhal, *Fault-Tolerant Quantum Computation for Local Leakage Faults*, https://arxiv.org/abs/quant-ph/0511065 , already treats coherent local leakage with actual leakage-reduction units such as teleportation. Its primary abstract was inspected for this note; no new full-body resource audit is claimed. Guard occupation is not necessarily leakage of the DATA qubits, so the two physical interfaces should not be equated, but calling cooling or transparent sectors new would ignore this strong alternative.

Battistel--Varbanov--Terhal, https://arxiv.org/abs/2102.08336 , and Marques et al., https://arxiv.org/abs/2302.09876 , provide concrete leakage-removal/control alternatives. Only their primary abstracts were inspected here. They motivate paying real removal pulses, residual computational-subspace disturbance and control time; they do not establish that the present guarded apparatus is realized or advantageous. No quantitative hardware comparison is inferred from the abstracts.
