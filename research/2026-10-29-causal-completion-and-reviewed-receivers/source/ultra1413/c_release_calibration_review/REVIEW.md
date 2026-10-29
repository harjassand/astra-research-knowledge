# Independent whole challenge: nominal-to-actual reference margin

30 October 2026. **ACCEPTED at the displayed all-finite-reference mathematical
scope, conditional on a qualified nominal release and an acquired deterministic
entry-error promise.** Physical or statistical acquisition of that promise
is not established. The argument is ordinary weighted norm perturbation;
no novelty or new privacy semantics are inferred.

I read the entire root_release_calibration/PROOF.md, all of compile_margin.py
and the actual MARGIN.json. I did not import, execute or edit root code, rerun
the release solver, sample a channel, introduce a new case or recompute an
existing numerical experiment. This receipt binds the source/version read;
the whole proof challenge below supplies the mathematical review.

## 1. Weighted block map and noncommuting references

Let v=Lu and W_y=sum_i L_yi Q_i. With B=E L^-1, Eu=Bv is exact for vectors
in any finite complex Hilbert space. No commutation, choice of basis for Q_i,
or bound on reference dimension enters this identity. Strict positivity gives
ell_y I<=W_y<=u_y I on the entire effect simplex, including its boundary.

Set z_y=W_y^-1/2 v_y. The perturbation in these coordinates is the block map

    T_yz=B_yz W_y^-1/2 W_z^1/2.

This multiplication order matters and is the order used in the proof. Its
operator norm is bounded by

    |B_yz| sqrt(u_z/ell_y)
    <=delta [sum_i L_yi |(L^-1)_iz|] sqrt(u_z/ell_y).

Triangle inequality in each Hilbert block bounds T by the nonnegative scalar
matrix of these block bounds. Its spectral norm is at most its Frobenius
norm, delta sqrt(S). Hence the central perturbation estimate is valid for
all noncommuting effects and all complex vectors, without a dimension factor.
Using the whole direct sum rather than its zero-sum tangent only makes the
bound conservative. There is no missing stochasticity or positivity premise
for B itself: B is a signed algebraic error map, not a stochastic channel.

## 2. Comparison of the actual free form

The scalar entry promise implies the ordered operator inequalities

    (1-delta)W_y <= W'_y <= (1+delta)W_y.

Inversion reverses these inequalities. Therefore, with a=delta sqrt(S)<1,

    F_L' >= (1+delta)^-1 ||v+Eu||_(W^-1)^2
          >= (1+delta)^-1(1-a)^2 F_L,

and the matching upper is (1-delta)^-1(1+a)^2 F_L. These are multiplicative
form inequalities. They do not subtract unrelated entropy continuity errors,
require a lower bound on a particular source's J_L, or divide by an unknown
small distinguishability. Zero-denominator cases are therefore covered by
the inequality itself.

Combining the lower inequality with the qualified nominal F_K<=c F_L gives
the root's factor c(1+delta)/(1-a)^2. The accepted general free-Umegaki
representation transfers it to the exact conditional/equal-reference
semantics at the shared classical input boundary. No unproved assertion
about pointwise equality of different quantum Fisher metrics is being used.
The actual L' need not be separately supplied with an inverse in this step.
In fact a<1 also prevents loss of tangent injectivity; a nonzero Lu cannot
be cancelled by Eu in this norm. Positivity of L' is already guaranteed by
delta<1 and the entry premise; stochasticity of L' is an explicit input.

The theorem remains confined to defined finite conditional-entropy
differences. It does not interpret infinity minus infinity. Common support
regularization at the admitted boundary is inherited from the same free
representation, not from a newly assumed well-conditioned source state.

## 3. The literal finite compiler

The code reads only the nominal rational reference and budget from the saved
SOURCE.json. It checks strict positivity, column stochasticity, square shape
and the exact inverse identity. Its indexing of row extrema and u_z/ell_y
in S matches the block proof above.

For nonnegative rational S, floor(sqrt(floor(S)))=floor(sqrt(S)). Thus the
integer-isqrt step followed by an exact square comparison produces a genuine
integer ceiling of sqrt(S); taking the maximum with one is safe. With this
B0, delta=1/(32 B0) implies a<=1/32. At nominal c=1/2,

    c_robust <= (1/2)(33/32)/(31/32)^2 =528/961 <3/5.

The actual receipt records B0=39, delta=1/1248 and the exact upper
19984/37479. Its SOURCE hash matches the frozen release source. The displayed
decimal is a display; the exact rational is the certified returned number.
No numerical eigenvalue or rounded square root determines any sign.

The compiler appropriately says it does not requalify K or its optimum.
Reading nominal budget 1/2 out of SOURCE is not, by itself, a proof that any
supplied K meets that budget. Its conclusion is conditional on the separate
nominal certificate, which is precisely what the proof and status declare.
The .00836s receipt is margin arithmetic after imports, not the cost of
learning L', preparing inputs or performing a calibration experiment.

## 4. Operational guard

The additional premise is a simultaneous deterministic bound on EVERY
actual reference entry, with the same classical symbols and stochastic
normalization as the nominal model. A fitted calibration table, average
error, per-entry marginal interval or a few test inputs does not automatically
give that promise. Any statistical calibration would need its own joint
coverage, reset/sampling/readout and error model. None is granted here.

This robustifies the SAME one-use information budget. It does not turn it
into differential privacy, guessing dominance, adaptive disclosure security
or a constant factor for arbitrary correlated blocks. It also supplies no
utility or speed advantage: every ordinary/source-aware design receives
the same perturbation receiver. No correction is requested at its declared
scope, and no additional numerical case was needed to reach that conclusion.
