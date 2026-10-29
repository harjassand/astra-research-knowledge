# Why separately exact finite observations do not yet give a continuous point

Let beta=3/4, M the standard3-normal density, D=1/3200. The frozen positive
cell completion requires A(C)=int_C M>=D B(C), B(C)=int_C M^beta.
It provides an exact cell LABEL, not the proposal point used to select it.
Retaining that proposal point would have the wrong within-cell density.

## 1. General fixed-D refinement obstruction

Under probability measure q_beta=M^beta/Z_beta,

    A(C)/B(C)=E_qbeta[M^(1-beta)|C].

Suppose nested finite/countable partitions all have valid non-null cells
and generate the full Borel sigma-field modulo q_beta null sets. Their
conditional expectations of the positive continuous function M^(1-beta)
are then >=D at every level. Martingale convergence would imply
M(v)^(1-beta)>=D for q_beta-almost every v. This is false: that function
decreases to0 and has a positive-measure tail below D. Thus no such sequence
of valid-cell partitions can generate the full target coordinates.

For pathwise adaptive cells of diameter tending to0 at a finite point v,
the same conclusion needs no fixed/random-partition assumption: the ratio
lies between the infimum and supremum of M^(1-beta) on the shrinking cell,
so tends to M(v)^(1-beta). A path converging in the tail must eventually
violate the cell criterion. The actual positive hard-sphere solution has
positive density there; that event cannot be discarded as null. Wild
nonshrinking/random coding schemes are not ruled out by this path statement.

This proves failure of the CURRENT fixed-D completion as a full refinement
operation, not a no-go for all positive samplers. It identifies the missing
tail/conditioning operation rather than assuming a coupling of marginals.

## 2. Inside a paid compact region, continuous conditional output is already possible

On the admitted cube[-4,4]^3, M>D M^beta pointwise. One can sample the
target conditional on that cube by a known proposal proportional to
M+D M^beta there, query H_t(v) AT that proposed point, and accept with
probability [M(v)+M(v)^beta H_t(v)]/[M(v)+D M(v)^beta]. Every realization
is nonnegative; the accepted point has conditional f_t law. The cube flag
itself is exactly sampled by the frozen two-cell completion. This gives
a continuous conditional point plus an honest overflow event, not full
continuous output. Adaptive refinement inside the cube is unnecessary.

## 3. Rare overflow does not automatically remove exponential work

Let an exact unconditional full-velocity sampler cost C_t in mean, and let
A be overflow with true target probability p>0. Drawing it repeatedly until
inside A costs C_t/p in mean (attempt cost can correlate with its own hit;
the stopped-sum identity still holds). Choosing that fallback only on an
exact overflow event of probability p therefore contributes EXACTLY C_t
to unconditional mean work. Rarity cancels the rejection penalty. This
specific hybrid does not compress the old exponential lineage at all.

Similarly, independently rerunning unconditional fine-cell samplers until
they match a previously accepted prefix costs inverse prefix probability.
Correct marginals alone do not provide a free projective coupling or a
finite-mean real-output representation. A true coupling/conditional oracle
needs its own construction and precision cost.

## 4. Strong prior and scope

General exact sampling from computable measures and lazy real outputs is
established; computability alone is not a useful finite-mean cost bound.
Jacob--Thiery2015 (arXiv:1309.6473, DOI10.1214/15-AOS1311) also rules out
generic nonnegative-unbiased conversion under its stated black-box premises.
That general theorem is not applied as an impossibility result for this
fully specified kinetic model; its analytic structure is additional input.
The elementary arguments above directly govern the actual cell mechanism.
