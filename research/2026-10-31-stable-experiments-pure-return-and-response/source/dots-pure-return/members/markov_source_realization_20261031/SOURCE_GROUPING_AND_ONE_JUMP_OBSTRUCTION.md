# Source grouping and a sparse-graph obstruction to one-jump return
31 October 2026. New mathematical construction/obstruction, not a whole compiler theorem or a novelty claim.

## 1. An explicit reversible extension
Let Q be an irreducible row generator, q_xy>=0 for x!=y, with known positive stationary pi and detailed balance pi_x q_xy=pi_y q_yx. Write psi_x=sqrt(pi_x), P=|psi><psi| and w_xy=pi_x q_xy.

For each source x define a single matrix
L_x=sum_(y!=x) [sqrt(q_xy)|y><x|-sqrt(q_yx)|y><y|].
Then L_x psi=0. The generator sum_x D[L_x], with no Hamiltonian term, preserves the diagonal algebra and restricts to Q. In particular its population rate from x to y is q_xy. For a diagonal projector at y, off-diagonal entries cancel: incoming columns from distinct source labels are orthogonal, while the diagonal-row cross term is -sqrt(q_xy q_yx), canceled by the anticommutator.

The total C=sum L_x^dagger L_x has
C_xx=2 sum_(y!=x) q_xy,
C_xz=-2sqrt(q_xz q_zx), x!=z.
Thus C is exactly the same additive-reversibilization Dirichlet operator as the earlier individual-edge completion. Grouping is a choice of quantum extension, not merely a unitary change of Lindblad representation of the same quantum generator.

The pure-return operator R=sum L_x^dagger P L_x equals B^2, where B is the real symmetric weighted Laplacian
B_xz=-sqrt(w_xz), x!=z,
B_xx=(1/sqrt(pi_x))sum_(y!=x)sqrt(pi_y w_xy).
Indeed B_{xz}=<psi|L_x|z>, Bpsi=0. This directly computes the changed return geometry.

For the reset generator q_xy=pi_y, this construction is EXACTLY
L_x=|psi><x|-sqrt(pi_x)I.
Then C=2(I-P), R=I-P. The dimension-free reset improvement is therefore a special case of source grouping, not an unexplained norm certificate.

For uniform pi=1/d and symmetric rates, B=L_sqrt(q)/sqrt(d), and R=L_sqrt(q)^2/d. On a unit-rate D-regular graph, Tr R=D(D+1), whereas Tr C=2dD. Connectedness gives positive return on the hidden subspace, but the normalization generally still loses d.

## 2. Universal obstruction, including multiplicity spaces
The following does not assume the source-grouped construction. Consider ANY finite quantum extension with mutually orthogonal classical projections P_x summing to I, whose Heisenberg generator satisfies
L^dagger(P_y)=sum_x q_xy P_x.
Allow arbitrary multiplicities of these classical projections, arbitrary Hamiltonian and any finite Lindblad representation. Suppose there is a pure stationary state psi with ||P_x psi||^2=pi_x>0.

Use a dark Lindblad gauge L_alpha psi=0. Such a gauge exists for a pure stationary state: stationarity of its purity implies each original L_alpha psi is proportional to psi, and subtracting that scalar identity with the compensating Hamiltonian shift preserves the generator. This changes the chosen jump record, so the obstruction is specifically about dark representations relevant to low-activity compilation.

Put phi_x=P_x psi/sqrt(pi_x), C=sum L_alpha^dagger L_alpha and R=sum L_alpha^dagger P L_alpha.

For x!=y, evaluating diagonal rates gives
sum_alpha ||P_y L_alpha phi_x||^2=q_xy.
Therefore q_xy=0 forces every such component to vanish. For distinct x,z both different from y, the off-diagonal matrix element of L^dagger(P_y) gives
sum_alpha <P_y L_alpha phi_x,P_y L_alpha phi_z>=0.
Neither the Hamiltonian nor anticommutator contributes to that matrix element.

Darkness projected into P_y gives the vector identity
P_y L_alpha phi_y=-sum_(x!=y)sqrt(pi_x/pi_y) P_y L_alpha phi_x.
Using the preceding orthogonality and stationarity,
sum_alpha ||P_y L_alpha phi_y||^2
=sum_(x!=y)(pi_x/pi_y)q_xy
=sum_(z!=y)q_yz=:r_y.
Thus <phi_x,C phi_x>=2r_x.

Let S_x={x} union {y:q_xy>0}, and let pi(S_x) be its stationary mass. Weighted Cauchy–Schwarz, together with the support restriction, yields
<phi_x,R phi_x>
=sum_alpha |<psi,L_alpha phi_x>|^2
<=pi(S_x) sum_alpha ||L_alpha phi_x||^2
=2r_x pi(S_x).

Consequently any global coercivity R>=a C must obey
a<= [sum_x r_x pi(S_x)]/[sum_x r_x].
For uniform pi and maximum out-degree D, this gives a<=(D+1)/d.

This statement covers enlarged multiplicity spaces as long as the SAME classical observable algebra is invariant exactly on all states. It is not an obstruction to every possible representation of a process from one special initial state, or to every different hidden-memory architecture.

## 3. Constant classical gap does not repair the one-step inequality
Take unit-rate random walks on fixed-degree undirected expanders. Their classical spectral gaps are bounded below and generator norms are bounded above independently of d, but every dark exact classical-algebra extension above has one-step return ratio a<=O(1/d).

Existence of such fixed-degree families is standard; the primary Friedman result bounds the second adjacency eigenvalue by 2sqrt(D-1)+epsilon for fixed D>2 and large random regular graphs: https://arxiv.org/abs/cs/0405020 . Choosing epsilon<D-2sqrt(D-1) yields a positive Laplacian gap. This invocation is only an existence source for the obstruction, not a free expander-generation or encoding oracle.

The simpler columnwise bound in a d-dimensional basis is Tr R<=(D+1)Tr C/d. A localized zero-sum vector also gives the weaker factor 2(D+1)/d ratio when its two-column support is used. The trace proof above is stronger and extends to classical multiplicities.

No conclusion about an optimal MULTISTEP return time follows. Hidden redistribution can potentially produce return after several jumps even when every uniform one-step coercivity constant is small. A compiler based on a finite-time Lyapunov potential is a different possibility.

## 4. Exact checks and acquisition limits
The accompanying check_source_grouping.py uses exact SymPy arithmetic for uniform resets of sizes2,3,4,5; unit-rate cycles of sizes4,5,6; and a nonuniform reversible three-state example. It verifies darkness, exact diagonal-generator closure, R=B^2 and the trace bound. The .json output records eight passing checks. These are finite diagnostics, not proofs of the universal statement or an implemented quantum compiler.

For an explicitly listed finite source, the L_x matrices and B are computable by finite arithmetic. This does not automatically earn efficient controlled encodings, source-state preparation or a succinct large-source compiler. Their actual list sizes, rates and precision costs must be paid. The sparse obstruction applies even before such acquisition questions.

Quantum extensions preserving commutative observable algebras are ordinary prior machinery. Bardet's primary paper explicitly studies this inverse-extension problem and classification: https://arxiv.org/html/1509.04849 . The bounded reading here supports that comparison, not a priority claim for either displayed formula.

The useful conclusion is two-sided: realization choice can genuinely improve return geometry on structured sources such as reset chains, but pi_min/d losses cannot always be removed from an all-sector ONE-JUMP return inequality merely by changing the pure extension. The next question is acquired multistep return, not a generic dimension-free norm assertion.
