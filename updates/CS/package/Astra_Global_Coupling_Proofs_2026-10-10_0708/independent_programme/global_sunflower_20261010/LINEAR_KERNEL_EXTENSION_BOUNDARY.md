# Why high-rank binary blocks require a nonlinear extension

Date: 2026-10-10.

## Scope

The root record `../root_additive_sunflower_20261010/` proves a native F_4-kernel coupling for additive binary codes whose observed output blocks each have F_2-rank at most two. This note is a precise obstruction to extending that specific *linear-kernel* construction unchanged. It does not refute an exponential bound for arbitrary additive codes, or a nonlinear constant-cost coupling.

## Exact obstruction already for one identity block

Let the only observed block be the identity on F_2^r. Write a difference parameter in F_4^r as z=u+omega v, with u,v in F_2^r. A triple (a,a+u,a+v) is valid precisely when u=v=0 or when u,v are distinct and nonzero.

Suppose W is an F_4-linear subspace of F_4^r such that every z in W gives a valid triple. In particular,

    W intersect F_2^r = {0},

since a nonzero real-binary z has v=0 and gives exactly two equal replicas. Viewing both spaces as F_2-linear subspaces of the 2r-dimensional binary ambient space gives

    2 dim_F4(W) + r <= 2r,
    dim_F4(W) <= floor(r/2).                       (1)

This is sharp: for even r, take W to be all coordinate-paired vectors

    (t_1, omega t_1, ..., t_{r/2}, omega t_{r/2}).

For odd r append a zero coordinate. Each nonzero t=s+omega t' produces two binary coefficient vectors whose two-bit pair is independent: multiplication by omega has no nonzero eigenvector over F_2. Thus every nonzero vector of this W is valid.

If a is uniform on F_2^r and z is uniform on a d-dimensional W, the resulting triple is uniform on 2^r 4^d outcomes. Its KL divergence from three independent uniform rows is

    (3r-r-2d) log 2 = 2(r-d) log 2 >= r log 2.

Even allowing a nonuniform distribution on W cannot improve this lower bound, since its entropy is at most 2d log 2. Thus a uniformly bounded number of F_4-linear kernel constraints cannot handle arbitrary output ranks at a constant cost per observed coordinate. The genuine one-coordinate optimum is at most log 4 by the local entropy theorem, so the growing loss is a limitation of the linear-subspace support ansatz.

The rank-at-most-two root construction escapes this obstruction because its binary output dimension is at most two. An extension for high-rank blocks must use nonlinear admissible difference supports, a different coupling family, or another structural operation. This note makes no claim against any such extension.

