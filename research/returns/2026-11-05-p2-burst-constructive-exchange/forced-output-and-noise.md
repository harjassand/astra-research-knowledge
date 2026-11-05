# Forced-output semantics and the actual burst recurrence

This page maps the proof in the [complete P2 return](P2_CONSTRUCTIVE_EXCHANGE_20261105_RETURN.txt). The [positive theorem and model contract](README.md) and [finite encoding/readout costs](implementation-and-resources.md) govern its scope.

## Deterministic local gadget

The fixed physical basis is identity, resets to 0 and 1, and adjacent binary gates

\[
\mathrm{COPY}(x,y)=(x,x),\quad
\mathrm{SWAP}(x,y)=(y,x),\quad
\mathrm{SORT}(x,y)=(x\wedge y,x\vee y).
\]

The theorem chooses `D=11`, `t=2D=22` and `n=8D+1=89`. Each level-`k` cell has `B` child cells, including `n` designated data children, a disjoint fresh-output bank and workspace. A level-0 cell is valid for `b` precisely when its physical bit is `b`. A level-`k` cell is valid for `b` when at least `n-t` designated children are valid for `b`. The other children and all workspace may be arbitrary.

The required contract is partial: whenever specified valid inputs force an output of the Boolean gate, a good encoded gate makes that output valid. COPY with a valid source forces both outputs despite an arbitrary destination. SWAP transports each valid input separately. A valid zero forces SORT's first output; a valid one forces its second. RESET forces its constant. Arbitrary inputs need not have consistent logical interpretations across operations.

Each output replica has its own computation row. The schedule resets reusable workspace, copies original source replicas, sorts those copies monotonically to compute majorities, computes the selected output component and stores it in a dedicated fresh output cell. After all rows, adjacent swaps commit the fresh bank and retire old records. Both outputs of COPY and SWAP are rebuilt; retaining an old source bank would accumulate errors.

Four rules control fault spread: at most one live parent-level value per child cell; original sources used only as COPY sources or SWAP passengers before commitment; no intermediate results shared between output rows; and protected identity operations on live sources and completed outputs during other work. Routing, row and lineage labels describe the immutable compiler schedule and the proof, rather than immune mutable device records.

## Why malformed blocks do not leave a semantic gap

Associate valid 0 with `[0,0]`, valid 1 with `[1,1]`, and arbitrary input with `[0,1]`. The monotone gates propagate bounds. A strict valid majority for `b` forces both endpoint evaluations to `b`, even if arbitrary blocks behave inconsistently between uses. Lower-level forced-output contracts therefore suffice recursively.

At most `D` bad child operations contact at most `2D` original source lineages and `2D` output-row identities. Every valid input retains at least

\[
n-t-2D=4D+1=(n+1)/2
\]

valid original replicas throughout the gadget. Untouched output rows are forced correct, and at most `2D=t` output replicas can be contaminated. Every forced output is consequently valid at level `k`. Decoder records are protected by the same recursion as other workspace.

For fixed `n`, prescribed positions in a width-`B` block can be routed by `O(B)` adjacent swaps. All templates, including identity, are padded to a common child-clock duration `A=C(n)B`, for a computable constant. The original code gives the loose bound `C(n)=100 n^3`; the theorem may pad to it. Set

\[
L_k=B^k,\qquad \tau_k=A^k,\qquad
\kappa=\log_B A=1+\frac{\log C(n)}{\log B}.
\]

Choose `B` large enough that `1 < kappa < a-1`. Routing and idle costs are included, rather than supplied for free.

## Separated Poisson sources, rather than independent repair cones

A level-0 operation is bad when a burst hits its participating registers during its clock interval. A level-`k` operation is bad when it has more than `D` bad child operations. Active and idle locations both count. This recursive event depends only on the hit pattern; validity handles persistent incoming corruption separately.

Let `p_k` be the supremum bad-operation probability over types and placements. A parent contains at most `S=2BA` child locations. Exclude radius at least `L_(k-1)` bursts intersecting the parent. In the remaining process, a child anchored at `p L_(k-1)` can be reached only by centers within

\[
[(p-1)L_{k-1},(p+3)L_{k-1}]
\]

during its child-clock interval. Different time intervals, or spatial anchors separated by at least five child lengths, have disjoint truncated Poisson source regions. More than `D=11` child locations force two with such disjoint regions. Their truncated bad events are independent and, by monotonicity in the hit set, are contained in their corresponding full-process bad events. A union bound over pairs gives `S^2 p_(k-1)^2`. The earlier Toom interaction counterexample is not assumed away; this is a different construction and independence statement.

For larger marks, all centers that can hit a parent footprint of length at most `2L_k` have length at most `2L_k+2rho`. Hence

\[
\mu_k\le\lambda_1 A^k\int_{L_{k-1}}^\infty
(2L_k+2\rho)a\rho^{-a-1}\,d\rho
=C_{\rm tail}\lambda_1\theta^k,
\]

where

\[
\theta=AB^{1-a},\qquad
C_{\rm tail}=2B^a+\frac{2a}{a-1}B^{a-1}.
\]

The resulting proved recurrence in the supplied return is

\[
p_k\le S^2p_{k-1}^2+C_{\rm tail}\lambda_1\theta^k.
\]

Because `a>2` and `A=C(n)B`, choose `B` so `theta <= 1/4`. With

\[
c_a=2+\frac{2a}{a-1},\quad
C_p\ge\max(c_a,2C_{\rm tail}),\quad
\lambda_1\le\frac{\theta}{2S^2C_p},
\]

the base bound `p_0 <= c_a lambda_1` and induction yield

\[
p_k\le C_p\lambda_1\theta^k.
\]

All architectural and intensity constants are fixed before choosing the requested horizon. This proof covers the stated Pareto process. It does not extend the conclusion automatically to every law with a finite critical moment.
