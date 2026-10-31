# Independent whole review: acquired noncommuting Gaussian capacity

31 October 2026. **Scoped mathematical and executable PASS** on the final repaired v2 extension. This is separate from the accepted scalar checkpoint and from the prior conditional matrix theorem. It covers the actual global polynomial family, raw acquisition, finite exact interval construction and task receiver. It is not a general kinetics solver, physical measurement certificate, sampling oracle, historical-priority finding or practical superiority claim.

## 1. Source binding and actual execution

The entire proof, implementation, receiver embedded in it, tests, cost/scope note and dependency manifest were read. Bound current files:

- `PROOF.md`: `35f57dc46bd64269528d1cb6c5afdbc2a29296f5f8cbcf9f303b1d5baff31dea`.
- `compile.py`: `df359ad38ac9a9c6ce478f9fcfc1dac494ab242a0e89271182790462bec29fc7`.
- `check.py`: `bfb4363bce9b34eb39fde6c5d339cbc1891cd2279e9bec0c75956fa2e0cfd484`.
- `COSTS_AND_SCOPE.md`: `07e7aff7b92bd2107a22bf387b0b7a50d424b3ed5ac39a6165b5043266918ad3`.
- `DEPENDENCIES.json`: `819302d61e67cabfa3d39eb3520b58ed319300810c24d853417d255848186eee`.

The conditional matrix theorem and its full receipt were actually read: `sources/MATRIX_MONOTONE_CAPACITY_CANDIDATE.md`, SHA `b82715562387da5e0b8549baf24c2d0187d3ca7f191342451b90c3b1fb92b1e9`, and `sources/MATRIX_MONOTONE_INDEPENDENT_REVIEW.md`, SHA `2add3cfddddce315acd232d6d139c67b949eb8ab7d522c3dc004a7d311ba3551`. Their acceptance did not automatically accept this constructor.

The inherited scalar arithmetic source remains pinned to `../capacity.py`, SHA `8ff7aeebe56217463b7976b389d9931c3952a5f4e51f1f3b55d8f54e27652131`; the parent proof and whole receipt are `9de2b84d...` and `2c3b024e...` as fully listed in DEPENDENCIES.json. The new module checks the arithmetic file hash before ordinary import. Review execution used a fresh copied directory with the exact pinned parent, not a modified arithmetic substitute.

All **681 author assertions** passed on a copied final source set, including recomputation of every saved high-dimensional and rotated certificate. A separate **225-check** suite passed. Independent files:

- `check_independent_review.py`: `cfb080bc7620c845a87bee8f76970af5d332627dd0e5081e11d37b87424126a9`;
- `independent_review_checks.json`: `40cf05f9b229f8c3af34a49d2b0a3454b9553b95279434c817af1ce51082b023`;
- `independent_author_replay.json`: `3ff2a78c31805bf2a2c51bee337761bd7c6b32352281b2ac6ea848cf2667b2ed`.

The independent script takes the extension source directory as its argument. Author originals and saved timing reports were not overwritten.

## 2. Noncommuting current and dimension-free estimate

For C=beta^-1 A^-1, multiplying SC+CS=C' on both sides by A gives AS+SA=-A'. Thus the stated symmetric Sylvester solve is correct, including the absence of an extra beta in that equation. Since A is positive, its Sylvester map is invertible. The eigenbasis used at a fixed y is analysis notation: no eigenvector derivative or common eigenbasis is assumed.

Pairing the i,j terms gives

    K = (1/(2 beta)) sum_ij |A'_ij|²/[lambda_i lambda_j(lambda_i+lambda_j)].

The lower eigenvalue bound gives K<=Tr(B²)/(4 beta a), B=-A^-1/2 A' A^-1/2. Loewner decrease makes B positive; therefore Tr(B²)<=||B||Tr(B). This is precisely the step that would fail for an arbitrary rotating isospectral family. A'(0)=0 and the curvature bound imply ||B||<=Ly/a, while Jacobi's identity gives -w'/w=Tr(B)/2. The resulting integral has the NONPOSITIVE boundary term -b w(b), yielding the displayed dimension-free loss 1+L/(2 beta a²).

The ordinary conditional-transport Dirichlet/Thomson sandwich then receives this current for the FULL isotropic diffusion. Full-fiber boundary data are essential. The actual projected coordinate is not assumed Markov, and neither a fiber mixing time nor an equilibration limit enters the lower bound. Global evenness, not just slab symmetry, is required to identify right-tail MA with the left-basin mass; the actual polynomial family supplies it exactly.

For v=(1-y²)², H1>0 and H2>=0, A'=v'(H1+2vH2)<=0 on [0,1/2]. The second derivatives obey |v''|<=4 and |(v²)''|<=8 there. Exact acquired bounds H_i<=u_i I therefore give a=1 and L=4u1+8u2. The factor 1+(2u1+4u2)/beta follows without commutativity or a hidden trace/dimension factor. With u1=u2=1 it is7 at beta1, not the old scalar17/9 factor.

## 3. Global diffusion and physical tail

The actual family is globally SPD because A>=I+vH1>=I. It is smooth and even in y. For the degree-four scalar coefficient v, v+(y/2)v' is bounded below by -1/3. For v² the analogous polynomial is (1-y²)^3(1-5y²), bounded below by -4: its negative region is y² in (1/5,1), where the stated conservative bound applies. Therefore x.grad F>=-(u1/3+4u2)|x|². The stopped quadratic Lyapunov argument gives nonexplosion of the locally Lipschitz SDE.

The Gaussian marginal is integrable because, on the PHYSICAL m-dimensional fiber, A>=vH1 and determinant monotonicity gives q<=det_+(H1)^-1/2(y²-1)^(-m) outside |y|>1. This determinant inequality does not require H1,H2 to commute. The inherited analytic tail integral is consequently valid. No reflecting wall, high-degree tail extrapolation or omitted longitudinal normalization is introduced. Conservative divergence-form reversibility then supplies the finite invariant Gibbs law as in the parent proof.

The determinant of I+tH1+t²H2 may have degree2m or an intermediate degree when H2 is rank deficient. That degree is NOT the physical fiber dimension. The code correctly overwrites both the inherited integrator's tail exponent with m=n-1 and its tail leading determinant with det(H1+Pi)=det_+(H1). Independent rank-one H2 tests check both parameters and the resulting exact tail formula. Reusing the old degree as m here would have been an invalid stronger tail; the final code does not do so.

## 4. Acquisition from actual degree-ten coefficients

The generic path extracts the actual quadratic Hessian Q=P+H1+H2, whose unique null direction follows for admitted fibers. It acquires a rational representative u and physical orthogonal projector Pi=uu^T/(u^Tu); the unit direction may be irrational. The two polynomial divisions are correct: the degree-ten part isolates s^4*x^T H2 x/2 and the degree-six part isolates s²*x^T(H1+6H2)x/2, where s=x^T Pi x. Remainders and quadratic degree are checked. Recovered matrices must be symmetric, annihilate u, and satisfy the ENTIRE polynomial identity. Lower/odd-degree corruptions cannot pass by matching only the Hessian or highest degree.

The aligned fast path also checks the complete monomial dictionary. It does not assume the first coordinate is the distinguished direction; an independent nonfirst-axis test passed. The actual joint nonzero graph supplies the connected components; no block basis or matrix partition is handed in. Dense rotated inputs pay the full symbolic/division/identity bill.

Exact Schur elimination correctly handles PSD zero pivots: a zero-diagonal off-diagonal obstruction is eventually rejected, and a wholly zero remaining block is accepted only in the semidefinite case. Strictness of H1+Pi ensures the required positive fiber. Independent 4x4 rational tests compared PSD decisions to all principal minors and strict decisions to Sylvester's criterion. Cases with a positive quadratic Hessian but an invalid H1 or H2 are rejected, not rescued by the top-degree fit.

The spectral norm bounds are earned by checking uI-H_i>=0, starting at1 and doubling. This avoids a dense-rotation row-sum dimension penalty. The finite search performs at most129 candidate PSD tests, corresponding to128 doublings; the repaired cost wording now states that correctly. Exhaustion is UNKNOWN, not a statement that the true model lacks any usable bound.

Exact block determinants produce D(t); all coefficients are checked positive, supporting the inherited monotone rational Horner backend. The physical null direction contributes a determinant factor1. The genuine commutator diagnostic is a sum of real rational squares, appropriate for these real symmetric input matrices. It is not a claim that every accepted model must be noncommuting.

## 5. Numerical receiver, budgets and scope

The pinned parent supplies exact determinant-point arithmetic, dyadic square-root enclosures, monotone Darboux sums, safe diagnostic displays and explicit unresolved-seed/cutoff/grid/precision/point/Horner-budget UNKNOWN behavior. The new code uses those operations with the correct physical tail parameters. All external beta/tolerance/budget arguments are checked before construction. The final interval takes the conservative reciprocal product bounds and applies the new factor only to the lower endpoint.

The receiver reruns the ENTIRE adaptive construction from the external raw input and task parameters. It does not trust supplied H matrices, graph, direction, tail determinant, norm certificates or fitted intervals. A differently constructed but valid interval may be refused; this is explicitly sound incomplete receiving. It binds physical basin meaning, observable, beta, numerical method parameters and exact interval endpoints. Capacity/mass is still not arbitrary-start MFPT, finite-deadline hitting probability or an exact projected generator.

One real typed-binding defect was caught in frozen v1: changing acquired component sizes [1,2] to [True,2] passed shallow Python list equality. The exact interval was still recomputed correctly, but the advertised typed acquisition metadata was not fully bound. Final v2 uses recursive type-and-value comparison of the entire acquisition record except its documented timing field. Bool/float aliases and extra acquisition fields are rejected. The old version is preserved and does not inherit this receipt.

Outer diagnostic displays, timings and operation proxies are not proof fields and are not authenticated merely by PASS. The determinant-rational bit count is not total peak symbolic memory or every final reciprocal/output bit. All those costs remain real. Matrix norm search, dense symbolic acquisition and the inherited numerical budgets can reject a valid but difficult input. No polynomial-in-input-bit guarantee for arbitrary ill-conditioning is asserted.

## 6. Executed evidence and fair consequence

The independent suite covered exact PSD/strictness, dense irrational unit geometry, a nonfirst aligned axis, genuine noncommutation, rank-one H2 with determinant degree3 but physical m2, invalid fiber matrices despite an acceptable Hessian, degree0/odd polynomial corruption, nested typed aliases, external budgets/tolerances, tail-degree spoofing, basin changes and interval tampering. Every saved scaling certificate was independently recomputed in the author replay, including the65D case and the1791-term rotated5D case. Times in the saved author reports remain one-run diagnostics, not universal performance or sampler-acquisition claims.

The meaningful mathematical continuation is Loewner-monotone precision with bounded curvature implying controlled integrated transport resistance even without commuting fibers. Ordinary Gaussian transport, Sylvester solves, potential-theoretic variational principles, matrix positivity and exact interval arithmetic retain their credit. Giving an ordinary method this newly derived certificate lets it reproduce the computation; that is not an independent prior-art proof or a competitive speedup. This receipt does not perform a new exhaustive primary-literature search.

No further load-bearing correction found. The result remains an exact declared-polynomial, acquired-full-fiber equilibrium capacity/mass certificate, not a general nonlinear/nonequilibrium rare-event method, empirical model learner, physical intervention capability, historical-priority finding or civilisation-scale claim. The old scalar proof/compiler remain separately frozen and accepted.
