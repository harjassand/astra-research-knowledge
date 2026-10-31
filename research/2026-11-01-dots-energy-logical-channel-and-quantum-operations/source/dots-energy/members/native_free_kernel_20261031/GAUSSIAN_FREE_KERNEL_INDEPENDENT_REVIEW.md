# Independent local review: ordinary Gaussian source-only contraction

31 October 2026. Verdict: PASS as an acquired source-kernel operation for the stated open zero-field chain, conditional on the explicitly paid certified finite matrix and gate arithmetic. It is not a whole simulator, an implemented Gaussian gate backend, or a claim that the coupled system is Gaussian.

## Source and corrections bound

I read the complete initial source `OPEN_CHAIN_GAUSSIAN_FREE_KERNEL_CANDIDATE.md`, SHA `7e84da11a125ea3475e85e976a2d373f4e01b33623c22cb75c21952178e36a9a`, then the full amended 10,267-byte source, SHA `9ce21bcf4b035f5d14b3804057a948b49ffae6d7b98525bb43e0bde5d1bcd97f`. This receipt binds the latter.

Two finite-error clarifications requested during review are now explicit: positive approximate frequencies stay at least 3g/4, not an unspecified fraction of g, and the residual includes the scalar offset when the approximate vacuum energy is set to zero. The final source also isolates the two exact endpoint Majoranas and sets an explicit small residual budget. These are meaningful binding conditions; no uncharged negative attenuation exponent or discarded energy shift is accepted.

## 1. Exact parent and auxiliary sector

The diagonal interior heat-bath rate is half of one minus tanh(J_L Z_L+J_R Z_R). Its odd binary expansion has exactly the stated a,b coefficients. The simultaneous-flip magnitude is c+d Z_L Z_R. Since Z_L Z_R X_L X_R = -Y_L Y_R, multiplying by the negative flip gives -c X_L X_R+d Y_L Y_R with the displayed sign. The left flip changes the global bit and first wall; the right flip changes only the last wall. Their stated boundary terms therefore follow. Rational edge ratios give the claimed rational or algebraic coefficients without exponential state enumeration.

Adding one |+> work qubit changes the right single-X term into a two-qubit XX term. H_ext commutes with its X, and the + sector is exactly the original parent in domain-wall coordinates. Product Z on all original qubits preserves every Z and XX/YY term except the boundary single-X term in the restricted description, proving equivalence of the two auxiliary sectors. Positivity and the original nonzero gap follow, as does a two-dimensional ground space. The separate n=1 expression is consistent.

This is a prepared-sector dilation, not a replacement of the physical source by an arbitrary augmented initial state. The final work-qubit projection is part of the block interface and is essential.

## 2. Quadratic normal form and acquisition

The stated Jordan–Wigner identities have the correct signs. For example an XX coefficient -c corresponds to the antisymmetric-matrix entry 2c on its neighboring odd/even Majoranas. The resulting matrix is real antisymmetric, has size 2(n+1), and has only O(n) nonzero entries.

In the displayed ordering c_0 and c_(2N-1) do not appear at all: there are no endpoint Z fields or boundary YY terms. They give one exact complex zero mode. The known two-dimensional ground space and parent gap exclude further zero modes. Quadratic diagonalization then has n positive frequencies, each at least g, and one zero frequency. Its exact constant is zero because the parent ground energy is zero; equivalently the exact positive-frequency sum is n. The orientation of a zero Majorana can correct an orthogonal determinant without changing H_ext, so ordinary Gaussian-unitary synthesis can be used.

I directly inspected [Jiang et al., Section IV and Appendix A](https://arxiv.org/html/1711.05395). They describe quadratic diagonalization and implementation of arbitrary fermionic Gaussian transformations, not just preparation of one Gaussian state. The required polynomial preprocessing and O(n^2) Gaussian/Givens circuit machinery is an ordinary prior component. No inaccessible Glauber source was fetched or retried.

No positive-positive eigenvalue spacing is needed by this construction. An approximate orthogonal normal form with a certified operator residual suffices; rotations inside a nearly degenerate positive cluster do not alter the desired scalar spectral function. Certified matrix arithmetic must actually produce and verify that residual, rather than treating a floating eigensystem as an oracle. The exact zero coordinates and known positive gap remove an uncertain zero-eigenvalue classification.

## 3. Scalar-inclusive residual and contraction filter

For a real antisymmetric matrix difference Delta A, the quadratic many-body term has norm at most (N/2)||Delta A||. This follows by its canonical 2-by-2 blocks: the many-body eigenvalues are signed half-sums of their singular frequencies. Hence the explicit certificate

 |n/2-sum omega_tilde/2| + (N/2)||A-O A_diag O^T||

does bound the complete H_ext minus the approximate zero-vacuum-energy Hamiltonian. The first term cannot simply be dropped. The amended source correctly includes it and pays clipping changes inside the same residual.

In occupation coordinates, the excited projector is the presence of at least one occupied positive-frequency mode. The zero mode alone is still ground and must not trigger the filter. On the excited subspace, marking its first occupied positive mode subtracts g/2 from exactly one occupied energy. The product of the stated acceptance amplitudes is therefore exp[-s(E-g/2)], with zero output on the ground space. All marked exponents remain nonnegative: exactly they are at least g/2, and in the amended approximation at least g/4.

Fresh success flags for the contraction factors and reversible marker computation yield an operator block, not normalized postselection. Undoing the Gaussian change of basis and compressing onto the work-qubit |+> sector gives exactly the requested source Q exp[-s(H-gQ/2)]Q. Multiplying by one half retains the original F normalization and factor-two word convention. There is no free reset or exposure of the work qubit.

## 4. Uniform finite error and time cost

For the exact kernel, ||F(s)|| <= exp(-sg/2)/2. Thus the large-s zero branch has the claimed absolute error and limits active times to O(log(1/eta)/g), irrespective of lambda. Threshold and physical-time conversion are finite arithmetic, not an online exponential oracle.

For xi <= g/8, the approximate ground/excited projectors differ by O(xi/g). This can also be seen directly by applying the exact inverse of H on Q as a mathematical bound to its action on an approximate ground vector; it does not supply an inverse-H circuit. With approximate positive energies at least 3g/4, both shifted generators are nonnegative. Duhamel then gives contractive semigroup error O(s xi), including the O(g||Q-Q_tilde||) shift correction. The final xi <= eta*g/[100(1+log(1/eta))] budget, tightened as necessary by fixed constants, controls all active times uniformly. Positive-mode gaps between each other never enter this estimate.

For represented binary s, the exponential acceptance coefficients can be precomputed per mode and per time bit. Their products are the desired exponential for that represented time. The O(n B_time) controlled filters use fresh flags; Gaussian basis changes add O(n^2) ordinary rotations with paid synthesis/routing. Very small amplitudes are approximated in absolute error, never divided by. Approximation of the Gaussian unitary, scalar coefficients, marker circuitry and time representation receives the actual finite operation-count subdivision. Normal-form numerical certification is preprocessing, not an executed circuit claim.

The exact successful operation preserves the auxiliary + sector. Approximate leakage is charged to the operator error and the final + projection remains a success flag. This does not assert the same source operation for an unprepared auxiliary state.

## 5. Independent diagnostics and scope

I read and independently reran `check_glauber_quadratic_kernel.py` in memory while intercepting its output writer, leaving the saved JSON unchanged. The six n=1,...,6 restricted-parent and spectrum comparisons had maximum residual 7.87e-15. The n=128 diagnostic used a 258-dimensional Majorana matrix, with one zero frequency and ground-offset numerical residual about 7.1e-15. These are sanity checks, not certified gap acquisition, a synthesized Gaussian circuit or a final resource count.

No further load-bearing correction is required to the amended source. Its kernel can replace generic LCHS only after the downstream receiver binds this actual operation and its finite errors/costs. The physical jump stack, noncommuting system coupling, interaction words, complete first-event amplification and private-clock assembly remain separate. Neither the whole dissipative source nor the coupled system is asserted to be a freely solvable Gaussian process. The result credits ordinary quadratic-fermion machinery and makes no integrability novelty, practical advantage, or whole sharp-ledger amendment claim.
