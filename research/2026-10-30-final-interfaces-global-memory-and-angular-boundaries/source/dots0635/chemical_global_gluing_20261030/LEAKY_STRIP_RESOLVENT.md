# Exact finite-phase elimination for genuinely leaky lifted blocks

Status: newly derived candidate, awaiting audit. This is a local boundary-strip theorem with supplied explicit external forcing; it does not close global boundary feedback.

## Setup
Let phases r range over a fixed finite set J. Complexes are (r,a), a∈N^m, with fixed positive edge coefficients k_e. Internal edges (r,a)→(s,b) shift the unbounded count by b−a and change phase. Killing edges leave J and have ordinary outgoing rate k_e(u)_a. Assume EVERY lifted complex vertex can reach a killing edge by an internal directed path. This is stronger than frozen phase-chain transience and must be checked on the lifted complex graph.

Write a_a(u)=(u)_a, positive when all u_i exceed a fixed threshold. Define the ideal factorial-tilted phase matrix M_alpha(u) by adding

    internal edge r→s: k_e a_a^(1−alpha) a_b^alpha to entry(r,s),
    every edge: −k_e a_a to entry(r,r).

Same-phase internal edges contribute both terms to the diagonal. Killing edges have no positive term. This is a Metzler matrix, not generally a Markov generator.

## Uniform relative coercivity
Apply the finite killed-generator lemma to the lifted COMPLEX graph. For sufficiently small fixed alpha>0, p=1/alpha, and all f≥0, put z_(r,a)=f_r^p a_a. Homogeneity gives exactly

    sum_r f_r^(p−1)(M_alpha f)_r
       ≤−eta sum_r W_r(u) f_r^p,
    W_r=sum_(a:(r,a) a vertex) a_a.

Every phase is assumed to contain a vertex; unused phases are removed. Let D_r=sum_(edges sourced at phase r)k_e a_source, so cW_r≤D_r≤CW_r with fixed positive constants. Choose epsilon>0 small enough that

    B(u)=M_alpha(u)+epsilon diag(D(u))

retains the same kind of strict coercivity. Every principal submatrix does too, by setting omitted f coordinates to0.

For a principal index set I, D_I^(−1)B_I is strictly dissipative in the weighted l^p norm with weights D_I, hence all its eigenvalues have real part≤−gamma for a fixed gamma>0. For complex vectors, Metzler domination reduces the real-part estimate to absolute values. Therefore

    det(−B_I)≥gamma^|I| product_(r∈I)D_r>0.

Thus B and all its principal restrictions are nonsingular M-matrices after changing sign. No phase stationary law or recurrence assumption is used.

## Uniform logarithmic derivative bounds despite signed determinant expansions
All off-diagonal entries are positive sums of fixed generalized monomials in the positive falling factorials, so their logarithmic u_i derivatives are bounded by C/u_i. Let d_r=−B_rr>0. Coercivity gives d_r≥c'D_r, while the construction gives d_r≤D_r; since the positive same-phase tilted terms sum to at most D_r, also |partial_i d_r|≤C D_r/u_i≤C'd_r/u_i.

For a nonsingular M-matrix, the product of off-diagonal entries around any directed cycle is at most the product of its diagonal magnitudes. One proof normalizes by diag(d): the nonnegative off-diagonal matrix has spectral radius<1, hence every cycle product<1. Every determinant permutation therefore has absolute weight≤product d_r≤product D_r. Differentiating the finitely many determinant terms yields

    |partial_i det(−B_I)|≤C_I product_(r∈I)D_r/u_i.

The lower determinant bound above gives |partial_i log det(−B_I)|≤C/u_i. This is the step that is NOT available from positivity alone.

Each inverse entry has the positive simple-path expansion

    (−B)^−1_rs = [sum_(simple paths r→s)
        (product path off-diagonal entries)
        det(−B_complement(path vertices))] / det(−B),

including the empty path for r=s and empty minor1. Consequently every nonzero inverse entry has logarithmic derivative bounded by C/u_i. For any everywhere-positive C1 forcing F with |partial_i F_r|≤C F_r/u_i,

    v(u)=(−B(u)^T)^−1 F(u)>0

has |partial_i log v_r|≤C/u_i uniformly throughout the high-count orthant. In particular, for every fixed count shift nu,

    v_r(u−nu)/v_r(u)=1+O(1/min_i u_i).

Integrating the derivative bounds also gives polynomial upper/lower growth in the coordinates. The constants can be enormous and depend on the fixed phase graph; no uniformity as J grows is claimed.

## Return to the actual adjoint
Set mu(u,r)=(product_i u_i!)^(−alpha) v_r(u). The exact factorial identity from the bulk proof and the just-proved v shift bound give the ideal adjoint M_alpha^T v plus relative O(1/min u) incoming errors. Since

    M_alpha^T v=−F−epsilon Dv,

and the sum of all ideal positive incoming terms is at most D_r v_r, the total shift error is≤C D_r v_r/min u. Choose the target threshold additionally so every fixed incoming predecessor remains in the high-count domain of v. Thus for min u sufficiently large the actual restricted adjoint satisfies

    L_J^*mu≤−(u!)^(−alpha)F−(epsilon/2)(u!)^(−alpha)Dv.

An explicit nonnegative external incoming forcing g(u,r) can be absorbed by taking F≥g/(u!)^(−alpha), provided F satisfies the stated positive derivative bound. For example incoming flux from a fixed fractional-factorial bulk boundary value is a finite positive sum of exact factorial-ratio terms and satisfies that bound. The resulting mu and mu times polynomial jump rates are summable over u.

## What this does not settle
1. Closed lifted complex components violate the leaky hypothesis even when the frozen phase chain reaches an exit; they require a separate elimination step.
2. The altered strip values send flux BACK into the bulk. Solving the strip with bulk forcing does not prove that this feedback is absorbed by the bulk's margin.
3. The small-alpha threshold depends on the finite strip. The bulk threshold K depends on alpha. Choosing K from the bulk and then shrinking alpha for the strip can be circular; no compatible fixed choice has been established.
4. When some of the remaining u coordinates are small, another stratum is reached. Recursive termination alone does not establish compatible forcing or parameter choices.

These are explicit missing obligations, not hypotheses silently declared true.
