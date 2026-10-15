# FZ structured memory regularization handoff

16 October 2026. Main artifact: `STRUCTURED_GRAM_REGULARIZATION.md`.

**Result:** an exact signed-GKSL Pauli-catalog theorem with constructive
scalar-rate Kraus jumps, sharp minimum proposal rate, a genuine structured
error neighborhood, and exact missing-direction countermodels. The full-patch
2^(-972) penalty is avoidable under a specified finite error catalog. It is
not removed for arbitrary maps on the entire 486-qubit patch.

For floor rates gamma_i, signed Kossakowski coefficient matrix C, and
H=sum_i h_i P_i, compute

    K=sum_ij C_ij P_j P_i=(tr C)I+sum_i k_i P_i,
    D=diag(gamma_i)+C,       a=-k/2-i h.

The exact finite CPTP proposal criterion is

    D>=0, a in range(D),
    r>=Gamma+tr C+a^dagger D^+a,       Gamma=sum_i gamma_i.

Factor D=VV^dagger and choose V conjugate(c)=a. The jumps
B_j=c_j I+sum_i V_ij P_i satisfy sum_j B_j^dagger B_j=r_min I and
sum_j D[B_j]=floor+E. This explicitly retains negative perturbation
coefficients until the total Gram block becomes positive. It avoids
diagonalizing the ambient patch Choi matrix.

For N catalog modes, the fixed floor gamma_i=nu/(2N) tolerates
max(||C||_op,|tr C|,||k||_2)<=nu/(8N) and ||h||_2<=nu/(4 sqrt(N))
within total proposal rate nu. A larger sharp Hamiltonian-only ellipsoid
is sum_i h_i^2/gamma_i<=nu-Gamma.

The most concrete restricted memory candidate reuses an already positive
one-face Pauli bath as the floor. For six data faces per owner cell and
equal bath rates gamma,

    r_cell=18 gamma+sum_(face,P) h_(face,P)^2/gamma.

No extra Pauli floor is needed for those continuous one-body Hamiltonian
errors. Zero bath rates obstruct the corresponding coherent directions,
and the deliberately completed correction channels are still required by
this proof. Therefore this does not establish robustness of the original
unmodified sweep generator or of every bath allowed by its theorem.

The main theorem requires the Pauli support of H and the anticommutator K
to lie in the catalog. For fixed jump Pauli weight k, including products
up to weight 2k is sufficient and polynomial in patch-qubit count, with
all channel multiplicities and rates charged. Low Pauli weight does not
automatically mean a jump has few-site support. General Gram-factorized
proposals may act on the whole union patch.

Run:

    python3 check_structured_gram_exact.py

`STRUCTURED_GRAM_CHECKS.json` records PASS_EXACT_FINITE_ALGEBRA_ONLY:

- A non-Pauli signed C on catalog (XI,YZ,ZZ), with a negative diagonal
  entry, becomes positive after the stated floor. Its exact minimum rate
  is 7279/11360, versus physical floor rate 3/5. All sixteen matrix units,
  the scalar-rate identity, Choi/Gram equality and TP are checked exactly.
- Independent single-site floors plus h ZZ have principal determinant
  -h^2 for every proposal rate r.
- Those floors plus the positive two-site jump |00><11| have principal
  determinant -1/64 for every r, because K requires a missing ZZ mode.
- The Pauli boundary and amplitude-damping-to-reset completion are exact.

Prior-art finding: the displaced-Pauli identity is not new. Primary
[Shang-Franca 2604.18533v1 Eq. (4)](https://arxiv.org/html/2604.18533v1)
and the gauge section suffice to derive it. Both inspected arXiv versions
have no acquired Appendix D. An explicit weighted Pauli Appendix D appears
in an unpinned author-uploaded ResearchGate PDF search result; do not cite
it as an acquired appendix of arXiv v1/v2. Random-unitary semigroups,
Choi/Kraus conversion, and the Schur-complement algebra are established
tools. Historical originality of this structured application is unestablished.

The exponential lifetime conclusion remains conditional on the inherited
single universal good-schedule support-recovery event, its common decoder,
and its rate/range probability estimate. Those were not verified by this
worker. The finite diagnostic establishes only the displayed algebra.
Physical model acquisition, floor fabrication/calibration, reservoir/reset
cost, noisy readout, 4D implementation and practical advantage remain open.

No producer/worktree/Git modification or nested agent was used. Only this
worker directory was written. Source and output hashes are in
`SOURCE_AND_ARTIFACT_PINS.json`.
