# Independent audit of the finite-constant cluster cone

Audited against `comparators/cluster_uniform_cone.md` and its exact rational
receipt on 5 November 2026. No new numerical tests were needed.

## Physical fault compilation

The six data-fault layers are accounted for correctly. Reset and load data
faults give one-site label translations before H; after H, its outgoing Z/Y
faults give the same singleton label channel. Thus the first three layers
contribute c^3 at each singleton character. First-matching endpoints share
the group span(e_i,e_j), so their two channels compose to D_pair(c^2).
An unmatched odd last site contributes an extra singleton c.

Once the second CZ matching finishes, faults at i have label generators
e_i and e_(i-1)+e_(i+1). The second-matching and terminal faults therefore
compose to D_G_i(c^2), with boundary neighbors omitted. This agrees with
direct conjugation through the partial circuit; it is not inferred from a
terminal-only noise approximation.

For even N, endpoint factors lie within the endpoint coarse pairs. At N=2,
both endpoint factors and the first-matching factor combine to c^6. For odd
N, the final endpoint factor crosses the last pair/singleton boundary. The
two groups there can intersect in a nonzero translation, but identity gains
only positive beta^2 terms and the triangle-inequality bound on nonidentity
mass remains valid. N=1 is correctly handled separately by six singleton
factors. Its claimed positivity follows immediately at the displayed rate
from c^6(1-20p)>11/20.

## Local pair bounds and cone

Each local pair law is normalized and has min/max ratio bounded by the stated
R. For nonuniform u_i<=u_*, replacing both by u_* and a_j by c^6 only worsens
the bound. The odd singleton ratio is smaller than R.

The inverse coefficients alpha=(3+a)/(4a), beta=(1-a)/(4a) satisfy
alpha-3 beta=1. The corrected ratio r=(1-a)/(3+a) is the appropriate one.
The grouped link estimate zeta=6r+9r^2 is conservative both for disjoint
subgroups and for the odd endpoint intersection.

For messages with sum_nonzero |v(z)|<=kappa v(0), the stated inequalities

    v'(0) >= b(0) m (1-kappa R) v(0),
    sum_nonzero |v'(z)| <= b(0) zeta M (1+kappa) v(0)

follow directly. With kappa=1/(2R), the displayed condition
zeta<=1/(4R^2+2R) makes the cone invariant. The last scalar contraction is
strictly positive. This proves positivity uniformly in chain length, while
normalization follows from mass preservation of each exact inverse.

The exact rational receipt checks the correct constants. Their monotonicity
in p is also sound: u_* and 1-c^6 increase, which increase R; r and zeta
increase; the cone upper bound decreases. Thus the endpoint certificate
covers the entire claimed interval. Small-chain computations are correctly
labelled diagnostics rather than the all-N proof.

## Prefix sampler and metrology

For nonnegative true child masses, clipping absolute-delta approximations
preserves their delta error. Weighted conditional TV is at most 2 delta;
this remains valid when both approximate children vanish. The sequential
hybrid bound therefore gives the displayed exponential factor in absolute
tolerance. That tolerance costs only O(N+log(N/epsilon)) precision bits.
The constant-width signed network's bounded exponential absolute term sum
provides sufficient guard bits. Half-coarse-block prefixes merely require a
partial sum over the remaining local bit and do not increase width.

The faulty-voter root recursion and derivative bound are consistent: the
ideal majority derivative is at most 6(r+e), and arbitrary faulty truth
tables add at most 3v. Ten independent local bit-fault sites give a 10 eta
one-step parameter sensitivity. Geometric contraction then removes any
dependence on the entire tree size from acquisition precision. Calibration
error is propagated forward through the same positive estimated source,
which correctly avoids paying an inverse condition number in the final
physical-channel comparison.

## Timing clarification

The majority voter contains three sequential classical gates. Its first two
may execute before the data reset, with its final gate completing during the
reset slot. The root then immediately controls the next-slot CNOT. This
explicit overlap preserves six data-fault layers without requiring three
classical gates to fit into one primitive reset duration.

No mathematical defect was found. The finite stationary depolarizing model,
protected-classical export contract, reference-record treatment, timing and
all paid costs remain substantive. The quantum positivity rate alone does
not prove the classical reliability threshold or a total-resource advantage.
