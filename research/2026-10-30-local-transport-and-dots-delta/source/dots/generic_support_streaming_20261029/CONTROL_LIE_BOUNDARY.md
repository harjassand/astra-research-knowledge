# Scoped algebra completion, not a new efficiency claim

2026-10-29. Author proof, independent receiving pending. This closes the algebraic outline already sent to root; it does not extend the generic search theorem or claim the controllability ingredient is new. Exact indirect-controllability results with accessor dimension at least three are established, e.g. D'Alessandro–Albertini–Romano, arXiv:1210.5449 / DOI:10.1137/130949816.

Let `A=C*(I,Δ_x,Δ_y,Δ_z)` on the carrier. Use a four-dimensional clean accessor with all traceless Hermitian local controls, and couplings `H⊗Δ_a`. Let S be the real vector space of carrier Hermitian operators X for which every `iH⊗X`, with H traceless Hermitian on the accessor, belongs to the generated real Lie algebra. It contains I and every Δ_a.

For X,Y in S, choose anticommuting accessor Paulis, e.g. X_1 and Y_1. Their tensor commutator produces a nonzero traceless Pauli factor tensored with `{X,Y}`. Local conjugation and linear span of the adjoint orbit of that nonzero traceless factor give every traceless accessor factor, hence `{X,Y}∈S`.

For the carrier commutator use commuting accessor Paulis Z_1 and Z_2. Their product Z_1 Z_2 is nonzero and traceless, and

`[iZ_1⊗X, iZ_2⊗Y]=−Z_1Z_2⊗[X,Y]`.

The same local-orbit argument gives `i[X,Y]∈S`. This step is precisely what a single clean-qubit accessor does not directly supply. Since S is closed under real sums, Jordan products and Hermitian Lie products, `S+iS` is a complex *-algebra containing the generators. Conversely it stays within A. Thus `S=Herm(A)`.

Write `A=⊕_j M_(n_j)⊗I_(m_j)`. Central projectors already belong to Herm(A), so the construction supplies independently `su(4)⊗Herm(M_(n_j))` on each simple summand. Commutators with the same accessor Pauli also supply `I_4⊗su(n_j)`. Together these spaces are exactly `su(4n_j)` on each summand, with identity on multiplicity. Missing scalar center phases are irrelevant: any desired block Stinespring isometry extends to a determinant-one unitary by adjusting its unused orthogonal completion.

For a qubit-output map on M_(n_j), Kraus rank is at most 2n_j. Two clean accessor qubits and the original n_j carrier therefore suffice: keep one accessor qubit as output, discard the other and the carrier. The initialized subspace has dimension n_j inside 4n_j, leaving enough unused completion to adjust determinant. The multiplicity space is discarded, not learned. Cross-block terms vanish when the physical carrier is traced out.

For any decoder R, composing it with the trace-preserving conditional expectation onto A preserves each Δ_a and hence the recovery objective. The induced block channels described above implement that composed decoder. This proves reachability/density of an optimal objective decoder by the generated controls, but says nothing polynomial about word length, total Hamiltonian time, number of source programs, or acquisition cost.

Each generator can be sample-simulated with the original same-source programs; negative time uses fresh programs. A finite-word enumeration plus compactness can establish a finite bound, but that brute-force memory/time trade has not shown a consequential total-cost advantage over the received polynomial banked learner. It is not promoted here as the answer to the efficient generic problem.
