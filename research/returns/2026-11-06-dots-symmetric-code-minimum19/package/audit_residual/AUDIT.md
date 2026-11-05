# Independent adversarial audit: no fully symmetric 18-qubit two-error code

5 November 2026. Verdict: the final witness has a rigorously verified positive contradiction margin. The exclusion is not inferred from CLARABEL's status, a small negative eigenvalue, or a feasibility tolerance.

The mathematical scope is a rank-two code subspace contained in Sym^n(C^2), correcting arbitrary errors on up to two physical qubits, equivalently detecting all physical operators of weight at most four. No restriction to real codewords, a parity-separated ansatz, nondegeneracy, or a particular decoder is imposed. The SDP conditions are necessary, not equivalent to code existence; their infeasibility is sufficient for exclusion.

## Result and exact margin

For n=18 the independently recomputed certificate has:

- constant term approximately 0.00006908572623995704;
- enumerator residual penalty less than 9.334e-10;
- moment-matrix residual penalty less than 2.801e-12;
- a strict contradiction margin greater than 690847/10000000000 = 0.0000690847.

The exact larger rational lower bound is recorded in interval_certificate.json. Every decision uses integer or Fraction comparisons. Decimal fields are display approximations.

The certificate excludes n=18. The independently replayed rational MacWilliams LP certificates exclude n=9,...,17. Quantum Singleton excludes n<9 for a rank-two distance-five code. A separate algebraic certificate verifies the known n=19 construction. Together these establish minimum length 19 within this fully symmetric rank-two definition.

This is a computer-assisted mathematical certificate, not peer-review certification. A targeted literature check found no earlier unrestricted n<=18 exclusion through 5 November 2026; that negative search is not exhaustive, so publication-level novelty must remain qualified.

## Why a physical code supplies the constrained variables

Let H be spin j=n/2, dimension D=n+1, and P its rank-K=2 code projector. Collective rotations preserve the space of errors of each physical weight. On fully symmetric states, compressed weight-at-most-four errors span the irreducible spin tensor operators of ranks r=0,...,4. Thus the physical Knill-Laflamme condition implies

P T_rq P = Tr(P T_rq) P/K, for r<5.

Use Hilbert-Schmidt orthonormal spin tensor operators and define a_r=(D/K^2) sum_q |Tr(P T_rq)|^2. Then a>=0, a_0=1, and sum a=D/K. The intrinsic MacWilliams identity gives b=K M a, where

M[k,l]=(2k+1)(-1)^(n+k+l) {j j k; j j l}.

Cauchy-Schwarz gives b>=a, with equality on the detected ranks r<5. The code checks G a>=0 and (G a)[1:5]=0 for G=2M-I. The r=0 equality already follows from normalization. These are existing intrinsic-enumerator facts, not a new framework.

Let X2=integral P_g tensor P_g and X3=integral P_g tensor P_g tensor P_g over collective SU(2) rotations. Decompose the first pair into spin l and then couple the third spin to total J. In this basis,

X2=direct sum_l [w_l/(2l+1)] I_l,
X3=direct sum_J I_(2J+1) tensor R_J,
w=(4/D) M diag((-1)^l) a.

Hence w>=0, sum w=4, sum_J (2J+1) Tr(R_J)=8, and

sum_J (2J+1) R_J[l,l] = 2 w_l.

The verifier independently recomputes every M entry by exact factorial Racah arithmetic, proves it equals the saved rational entry, and checks the exact column-sum normalization used for the trace bound.

## Copy symmetry, complex codes and frames

X3 commutes with permutations of its three copies. Since rank(P)=2, the alternating S3 component vanishes: wedge^3(range P)=0. Let U represent the copy-23 transposition and V the copy-12 transposition. In the coupled basis,

U[l,l'] = (-1)^(n+l+l') sqrt((2l+1)(2l'+1)) {j j l; j J l'},
V[l,l] = (-1)^(n-l).

The standard Racah recoupling identities identify these as the actual permutation representation. The symmetric, alternating and standard projectors are the corresponding S3 group averages Ps, Pa and Pt=I-Ps-Pa.

For exact dyadic seed matrices Zs and Zp, define

Qs=Ps Zs,
Qp=Pt (I+V) Zp/2,
Qm=(I-V) U Qp/sqrt(3).

Every admissible real commutant block has the form

R_J=Qs Xs Qs^T + Qp Xp Qp^T + Qm Xp Qm^T,

with reduced Xs,Xp positive semidefinite. The standard pair uses the same multiplicity matrix. This remains true for non-orthonormal frames: positivity is preserved by congruence, and their full span is certified by exact projector ranks plus positive Gram lower bounds. Projector traces are integers; the directed intervals isolate those integers uniquely and match the seed-column counts. Every resulting Gram Gershgorin lower bound is positive, with the smallest above 0.999999999999998.

Restricting this necessary-condition relaxation to real matrices does not exclude complex codes. Complex conjugation preserves the rank-r tensor-operator space and the KL condition. In the real Clebsch-Gordan basis, average the valid moments of P and its complex conjugate. All real linear constraints, PSD constraints and partial-transpose constraints are preserved. This averaging need not produce one code projector, which is irrelevant for a necessary-condition relaxation.

## Lifted KL and PPT necessity

Before averaging, partial tracing the third copy of

P^tensor3 (Swap23-I/K) (I tensor I tensor T_rq)

gives P tensor [P T_rq P-Tr(P T_rq)P/K], hence zero for r<5. Recoupling and averaging gives the linear equations used in the certificate:

sum_J (2J+1) (-1)^(l'+j+J+r) {l j J; j l' r}
  [R_J (U_J-I/K)]_(l',l) = 0.

Only the valid triangle range and r=0,...,4 are used. Common nonzero reduced-matrix-element factors can be dropped from these homogeneous equations.

Partial time reversal on copy 3 is partial transpose followed by a fixed local unitary. X3 is separable across its three copies, so its partial time reversal is PSD. The verifier recomputes the original tensor-rank-sum transform, with local rank-r eigenvalue (-1)^r. It does not assume the constructor's faster single-6j shortcut or the numerical omission of coefficients smaller than1e-15.

Furthermore,

X2 tensor I-X3 = integral P_g tensor P_g tensor (I-P_g)

is positive and separable. In coupled blocks X2 tensor I is B_J=diag_l(w_l/(2l+1)). Therefore both B_J-R_J and B_J-PPT3(R)_J are PSD. These are the additional complement inequalities used here. No stronger unsupported condition on physical codes is inserted.

Earlier independent checks compared the PPT transform to direct full-matrix partial time reversal at n=1,...,4. More decisively, a genuine n=19 code is now constructed and checked against exactly these lifted constraints, as described below. Those checks are sanity checks of the representation formulas, separate from the rigorous final arithmetic certificate.

## Residual-based dual proof

The witness contains nonnegative scalar/vector inequality multipliers, unrestricted equality multipliers, and135 PSD dual matrices. Every PSD dual is defined exactly as L L^T with dyadic L, so no floating eigenvalue test is used to assert its sign.

Form the Lagrangian at zero PSD slack, with a minus sign on every positive-semidefinite primal expression. On any actual code's feasible variables it is nonpositive. Recompute the complete Lagrangian as

L(a,X)=c+r_a dot a+sum_(J,label) Tr(H_(J,label) X_(J,label)).

Its stationarity residuals need not vanish exactly. Since a>=0 and sum a=D/2,

|r_a dot a| <= (D/2) ||r_a||_infinity.

For each reduced variable let Gamma=Qs^T Qs or Qp^T Qp+Qm^T Qm. A rigorous Gershgorin bound g>0 gives Gamma>=g I. Because all X are PSD and the weighted total trace of R is8,

|sum Tr(H X)| <= 8 max_(J,label) [||H||_operator / ((2J+1) g)].

The verifier bounds ||H||_operator by an interval-enclosed maximum absolute row sum of the symmetric H. Therefore a strictly positive value of

c-(D/2)||r_a||_infinity
 -8 max_(J,label)[||H||_operator/((2J+1)g)]

contradicts L<=0. The final exact rational bound is positive by more than0.0000690847. This is the exclusion certificate.

## Arithmetic and export audit

The verifier uses192-bit directed integer intervals. Addition is exact at the chosen grid. Multiplication and matrix multiplication bound all cross-radius terms and round outward. Square roots use integer isqrt with exact rational comparisons. Wigner6j coefficients use the factorial Racah formula, not floating SymPy evaluations. All sparsely dropped physical coefficients are restored.

Exact endpoint tests cover1,426 operations, including nonzero input radii and all256 endpoint combinations of two2x2 interval matrices. A separate constructor-side check reports4,900 exact-Fraction comparisons. Neither test suite substitutes for the arithmetic proof, but both catch implementation errors. The verifier needs NumPy only as a container for Python arbitrary-precision integer matrix operations, not an SDP solver.

A first attempted dual check correctly failed. Its cause was an exporter orientation: CVXPY1.9.3 represented the sparse/dense marginal equality as2w-MargR, although the source visually wrote MargR==2w. The final witness explicitly negates only equality multiplier6 to use the canonical equation MargR-2w=0. Equality multipliers are unrestricted, so this defines a valid new witness. All residuals are then recomputed independently. No physical constraint, primal model or solver outcome was changed. Both uncorrected and corrected witness files and logs are preserved.

## Genuine19 positive control

The positive control is Aydin-Alekseyev-Barg's19-qubit example, not the21-qubit fallback in audit_lift.py. The separate audit_positive19 directory contains an exact algebraic amplitude definition with a rational isolating box. A standard-library Fraction replay proves existence and uniqueness, all50 reduced four-qubit KL polynomial identities, and a nonzero five-site Z witness, so distance is exactly5.

The normalized20-by-2 Dicke matrix produces coupled three-copy blocks whose maximum lifted KL residual is2.25e-16. Direct versus recoupled partial time reversal differs by at most1.69e-16. Minimum PSD/complement eigenvalues are between about-6e-17 and-1e-18, consistent with roundoff. Thus the known physical code passes the proposed relaxation, rather than merely an unrelated SDP returning near-feasibility.

## Reproduction and files

From the workspace root:

pi_code_bound_20261105/venv/bin/python pi_code_bound_20261105/audit_residual/verify_interval_dual.py pi_code_bound_20261105/audit_residual/dual_witness_corrected.json

python pi_code_bound_20261105/audit_positive19/replay_certificate.py

pi_code_bound_20261105/venv/bin/python pi_code_bound_20261105/audit_independent/check_certificates.py

The dual witness SHA256 is0fec2978c5c7141ea7d119fce811c237dbb817a819c494041d8802bfa1ebdbd9. Final script and report hashes appear in SHA256SUMS. The certificate JSON records the exact contradiction margin, each Gram bound and every reduced residual norm bound.

Timing values are individual internal execution intervals, not one cold end-to-end research cost. Solver reruns, failed export attempts, interval replays, physical positive-control construction and literature checking all remain separate costs. Do not quote a successful8-second replay as the total discovery cost.

## Sources and novelty limits

- Intrinsic MacWilliams framework and physical-distance correspondence: https://arxiv.org/html/2604.16023v2
- Explicit Racah transform: https://arxiv.org/html/2605.15372v1
- Known19 construction: https://arxiv.org/html/2310.05358v3#S7 and https://doi.org/10.22331/q-2024-04-30-1321
- Numerical/conjectural prior search: https://arxiv.org/abs/2603.10981

The current primary records checked through5 November2026 did not reveal an earlier unrestricted minimal19 theorem. This is a scoped literature check, not proof of originality. The underlying MacWilliams transform, KL equations, twirling, PSD/PPT relaxation ideas and residual-bound certification techniques are prior mathematics; the evaluated18-qubit exclusion is the concrete consequence supported by these artifacts.
