# Different geometry acquired, but candidate rejected as a new mechanism

## Result

`rank_one_riccati.py` acquires a symmetric-matrix Riccati representation directly
from scalar quadratic equations. It receives no matrix basis, matrix size,
measurement direction, unit, Lax pair or decoder. Exact coefficient tests admit
the result. Its common-Hessian-kernel/symmetric-square construction is sound and
complete for unknown invertible linear-coordinate copies of rank-one symmetric
Riccati dynamics. The independent proof is in `JORDAN_PRIOR_ART.md`.

The scientific anchor is the continuous-observation slow–fast filtering model of
[Berry and Harlim](https://pmc.ncbi.nlm.nih.gov/articles/PMC4032560/), Eq. 2.1.
We choose epsilon=1/10, with the paper's displayed drift/noise parameters, and
derive its transient covariance equation using standard Kalman–Bucy theory.
Eq. 2.2 in the paper is a **steady-state algebraic** equation; its Figure 1 uses
discrete observations. We reproduce neither that experiment nor its nonlinear
Lorenz-96 filtering models. Our full-state decoder means the full original
covariance ODE state, not an estimated stochastic signal from observations.

The raw scalar equations are

    p' = −2p+2q+2−2p²,
    q' = r−10p−11q−2pq,
    r' = −20q−20r+20−2q².

From these alone, the algorithm acquires the matrix chart

    X=[[8p,4q],[4q,2r]],
    A=[[-1,2],[-5,−10]], Q=diag(16,40), R=diag(1/4,0),
    X'=AX+XA^T+Q−XRX.

The exact block-linear flow

    [U;V]'=[[-A^T,R],[Q,A]][U;V], [U(0);V(0)]=[I;X0],
    X=VU^−1

and the acquired inverse chart recover all three original coordinates. This
matrix/Grassmannian geometry is different from the prior scalar projective chart.

## A proved blind spot of the previous route

For symmetric m×m Riccati dynamics on d=m(m+1)/2 scalar variables, write
`u=tr(RX)`. The homogeneous quadratic part obeys `D_2 u=−u²`, while canonical
`q=−div f/(d+1)` has linear part `alpha u`, with

    alpha=(m+1)/(d+1),  0<alpha<1 for m>=2.

Inductively, the top homogeneous part of `T^k1`, `T=D+q`, is

    [product_(j=0)^(k−1)(alpha−j)]u^k.

It never vanishes. The old cyclic-one projective route therefore cannot close on
this class, even though the newly acquired matrix decoder exists. This is an
algebraic obstruction, not a budget failure. `canonical_divergence_obstruction.json`
checks the first seven degrees for the published-model anchor; the induction,
not that finite check, proves nonclosure.

## Acquisition mechanism and exact controls

1. Extract the homogeneous quadratic tensor and its common derivative kernel.
2. Acquire a quotient B of dimension m. Factor the quadratic map as
   `K[(Bx)(Bx)^T]`, checking K invertible and the full polynomial identity.
3. Recover X=K^−1x. Check by linear equations that `BK(X)=Xr`.
4. Check the transformed affine drift is `AX+XA^T+Q` by another linear solve.
5. Verify the entire raw-to-matrix identity exactly; construct the block decoder.

The rank-one product has no identity element under partial observation. This
invalidates a naive unit-first implementation, but **does not create novelty**.

Adversarial controls reject: a quadratic map that does not have the contraction
structure; a linear drift outside the Lyapunov form; and rank-two measurement
(outside this selected recognizer, not evidence of nonintegrability). A rational
linear-coordinate mixing of the same scientific model passes. It is a robustness
stress test, not another scientific discovery.

## Strong conventional comparator: decisive rejection of novelty advantage

The independent `audit/bernstein_peirce_comparator.py` uses the identical raw
Hessian and no producer imports. It computes a classical Bernstein trace weight,
constructs an idempotent rationally, obtains the 1, 1/2 and 0 Peirce spaces, and
forms the matrix chart from products. It then fits the same Riccati drift and uses
the same block exponential. It acquires the original and mixed anchor and a
six-variable stress case, rejects the same controls, and independently verifies
the producer's eight matrix-component identities.

These are standard algebraic operations from the primary literature documented
in `JORDAN_PRIOR_ART.md`. The identical packaged quotient algorithm was not located
in that search, but this does not establish historical priority. Ordinary Kalman
software also starts with the physical matrix model already known; hiding that
model from a comparator would be particularly unfair.

**Verdict:** preserve as an exact recognition/decoder capability. Reject as a new
algorithmic mechanism, filtering speedup, or broad scientific advance. No further
rank-one benchmarks are justified by the current evidence.

## All computational costs and boundaries

Dense tensor extraction, common-kernel and quotient linear algebra, K inversion,
coefficient checks, Lyapunov fitting, rational coefficient height, and numerical
matrix-exponential/linear-solve conditioning are payable. These recognition
operations have polynomial rational-linear-algebra cost in the dense coefficient
input size; this is not a short-circuit general inversion theorem.

For Q positive semidefinite and PSD initial X, standard Riccati theory prevents
forward finite-time blowup; no such global statement holds for arbitrary
initial data/backwards time. Algebraic absence of a pole is not numerical
conditioning. The saved naive double-precision block frame reaches condition
about 2.38e9 by t=4, with observed error about 3.75e−8 against accurate time
stepping. Short-time errors are around 1e−13. No large-time speed benefit follows;
stabilized Riccati/Grassmannian algorithms are the necessary conventional baseline.

## Next attack, not an acquired result

Automatic Lax discovery itself is already performed by
[SILO](https://arxiv.org/abs/2503.00645). Its
[2026 follow-up](https://arxiv.org/abs/2607.01493) shows why compatibility and even
conservation-law output do not guarantee the intended inverse spectral geometry.
The materially harder operation is to acquire a usable full-state inverse
spectral or factorization decoder from discovered operators, charging its cost.
Finding a valid Lax pair, or verifying a supplied textbook pair, does not complete
that operation. This target is under investigation, not a claim delivered here.
