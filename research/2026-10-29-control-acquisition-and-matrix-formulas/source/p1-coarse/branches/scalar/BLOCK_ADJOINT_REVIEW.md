# Scoped review: nonsymmetric blocks and physical reversed adjoints

28 October 2026. Reviewed only the new block extension, building on the
completed primitive signed-correction and uniform-certificate reviews.

**Finding:** the nonsymmetric-block identities, the row/column noise bound,
and the reported exact matrix witnesses are sound under the declared real
Hilbert-space, physical-adjoint and simultaneous-interval premises. No new
mathematical defect was found.

Reviewed hashes:

- `core/block_echo_compiler.py`:
  `a7b73bf3e0286530c7d4b37de87ed0f1703416a48f69af22493a245512ce5e4a`.
- `core/run_block_experiment.py`:
  `d45cf00d9d685b5f27e099b801d90625d6453fc05045ae73262031b332d9b16d`.
- `results/BLOCK_EXPERIMENT.json`:
  `fd6e0c2fc1bdad25a6fd3d9c23271b417f0c0c744dba17985712b6e0ad5a2e45`.

## 1. Correct order of the acquired block moments

A known chronological primitive word v defines an unknown operator B_v.
Each primitive is actually selfadjoint, so the physically executable reverse
word defines B_v^*. This does not assume access to a generic opaque adjoint.
In a real Hilbert space, the raw scalar f(w) is invariant under reversal,
which justifies the compiler's canonical raw-word keys.

With dictionary column operator V, the required objects are

    G=V^*V, M_i=V^*B_iV,
    N_fi=V^*B_i^*B_iV, N_bi=V^*B_iB_i^*V.                   (1)

M_i need not be symmetric. In chronological word notation, v+reverse(v)
implements B_v^*B_v, while reverse(v)+v implements B_vB_v^*. The new code
uses these orders correctly and acquires both forward and adjoint moments.

Let forward and backward coefficient proposals be T_i and S_i. Define

    E_fi=B_iV-VT_i, E_bi=B_i^*V-VS_i,
    D_i=M_i-GT_i,
    R_fi=N_fi-M_i^*T_i-T_i^*M_i+T_i^*GT_i,
    R_bi=N_bi-M_iS_i-S_i^*M_i^*+S_i^*GS_i.                  (2)

The code's forward/dual residual expressions equal E_fi^*E_fi and
E_bi^*E_bi, respectively. Both are symmetric PSD, so the earlier symmetric
row-radius residual enclosure remains valid. In particular it would be
incorrect to reuse the forward residual for the dual unless separately
justified; the implementation does not make that substitution.

## 2. Signed correction and uniform bound

For a target block word i_1,...,i_H, use T for the forward prefix alpha_t
and S for the reversed-adjoint suffix beta_t. The signed correction remains

    ftilde=c0^*G alpha_(H+1)+sum_t beta_t^*D_(i_t)alpha_t.

Forward telescoping and adjoint-suffix telescoping give the exact remainder

    f-ftilde=sum_(t<s) (E_b,(i_s) beta_s)^*
       B_(i_(s-1))...B_(i_(t+1)) (E_f,(i_t) alpha_t).         (3)

No identity between S_i and a W-adjoint of T_i is required. They are separate
approximate trajectories. Since each true B_i is a contraction, the middle
product has norm at most one.

If both T_i and S_i satisfy the same checked contraction inequality with
W positive definite and 0<=rho<1, and both residual forms are bounded by
epsilon²W, the previous pair-count proof applies unchanged:

    |f-ftilde_true|<=||c0||_W² epsilon²/(1-rho)².             (4)

The code takes the largest epsilon² over every forward and backward residual,
which safely bounds their product. Separate forward/backward maxima could
sometimes sharpen this but are not needed for validity.

Only the forward mixed moment M_i enters the signed scalar correction.
Hence midpoint noise requires the Gram and forward-M bounds, while the
backward moment uncertainty is already paid in R_bi. No missing extra
midpoint-noise term for S_i is required: its entries are fixed computational
proposal coefficients, and its true trajectory discrepancy is E_bi.

## 3. Nonsymmetric noise domination is valid

Let Delta be an arbitrary real matrix with |Delta_jk|<=r_jk. Set

    row_j=sum_k r_jk, col_k=sum_j r_jk,
    d_j=max(row_j,col_j), D=diag(d).

For all vectors x,y, weighted Cauchy-Schwarz gives

    |x^*Delta y| <=sum_jk r_jk |x_j||y_k|
      <=sqrt(sum_j row_j x_j²) sqrt(sum_k col_k y_k²)
      <=sqrt(x^*D x) sqrt(y^*D y).                           (5)

Thus if the exact checker verifies D<=gamma W, then

    ||W^-1/2 Delta W^-1/2||<=gamma.

This is precisely the row/column maximum diagonal used by the implementation.
A row-only diagonal would not in general justify the same bilinear norm
bound for a nonsymmetric moment matrix. The returned gamma_G and gamma_M
therefore support the earlier uniform midpoint contribution

    ||c0||_W² [gamma_G+(gamma_M+rho gamma_G)/(1-rho)].         (6)

## 4. What the dephasing fixture establishes

The declared Bloch matrices are the orthogonal projections P_j=n_j n_j^T,
where n0=(3/5,0,4/5), n1=(0,3/5,4/5). Their norms are exactly one, so the
primitive dynamics have no strict contraction factor. The overlap is
n0^Tn1=16/25. Each two-step block P1P0 or P0P1 has operator norm exactly
16/25. This explains the meaningful representation change from primitives
to mixed blocks, with a checked computational rho=7/10.

The uniform block theorem covers **arbitrary finite sequences of the chosen
blocks (01 and 10)**. It does not automatically certify every arbitrary
primitive schedule, such as unrestricted repetitions of only primitive 0.
Changing the operation language is a substantive part of the construction,
not merely a new matrix notation. Additional prefix/suffix handling or source
identities would need their own proof before widening this domain.

The qubit interpretation is algebraically consistent: dephasing about n_j
maps a Bloch vector to P_j times that vector, and preparation/readout along z
gives survival probability (1+f)/2. The identity component is known and
separated from the centered amplitude. This is a supplied physical-model
interpretation of a synthetic execution, not an operated qubit device.
Physical reversibility here is the ability to apply the constituent
selfadjoint channels in reverse order, not inversion of a dissipative map.

## 5. Independent exact replay and cost scope

`review_block_certificate.py` imports neither the root block compiler nor
its PSD checker. Starting from the saved decoded intervals, it independently
reconstructs every new forward/dual residual expression and its uncertainty
matrix, verifies all common contractions and dominance inequalities by all
principal minors, verifies the nonsymmetric row/column noise enclosures, and
recomputes the final uniform bound.

All four residual witnesses and all matrix inequalities pass. The verified
uniform centered-amplitude bound is exactly

    80556563695072938114571 / 4536000079199999420000000000
      = 1.7759383220575353e-5.

The saved record contains 32 distinct source words, two calibration standards,
34 total readings, and 122 primitive executions. The additional unsuccessful
primitive contraction attempt reuses the same recorded acquisition. The
receipt is `BLOCK_CERTIFICATE_REVIEW_CHECKS.json`.

The Hoeffding formula is correct for its explicitly labelled hypothetical
IID binary receiver: amplitude radius a corresponds to probability radius
a/2, and a union bound over K means uses

    ceil(log(2K/failure_probability)/(2(a/2)²))

shots per mean. These shots were not executed. The chosen illustrative radius
1e-6 is a separate specification from the executed synthetic raw-error bound
1e-8; its shot count must not be described as an executed cost or as the
verified cost of obtaining the reported 1.77594e-5 final certificate. Calibration,
preparation, all primitive executions per shot and physical timing remain
additional costs in an actual receiver implementation.

Completed scope: new block/adjoint proof and code-path review, exact replay
of the matrix witnesses from decoded intervals, algebraic fixture and count
checks. Not covered: raw-standard decoding re-audit, device operation,
shot-level experiment, universally successful numerical proposals, discovery
of useful blocks for arbitrary systems, or a full physical comparative cost
claim. The established DWR machinery and acquisition contribution boundary
from the preceding reviews remain unchanged.
