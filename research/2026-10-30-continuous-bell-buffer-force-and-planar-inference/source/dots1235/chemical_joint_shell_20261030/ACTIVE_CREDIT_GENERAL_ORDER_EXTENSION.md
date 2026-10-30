# General-order active credit: the gap q-m appears as the exact return exponent
Status: personally derived extension of ACTIVE_PHASE_CREDIT_TRACE_CANDIDATE.md; unreviewed. Local capped trace only, not a general global recurrence theorem.

Let k>=2 composition species include A, total N. Fast reactions form a finite strongly connected graph of homogeneous degree-m composition complexes, containing every pure mX_i, and all carry catalyst qB. Take integers q>m>=2 and connector

    0 -> A+B -> mA+qB -> 0.

All constants are fixed positive, or vary within fixed positive bounded intervals. Write h=q-m>0, and I=1 when a fast composition reaction is enabled. As before, fast jumps preserve I, adding A cannot disable it, and activation from any A>=1 lands active. Inactive states have N<=k(m-1).

Define the unscaled integer residual

    Z=B-N-h I.

Its only nonzero changes are:
- Activation while active: +h.
- Immigration that turns activity on: -h.
- Clearing whose target stays active: -h.
All other enabled reactions leave Z unchanged. In particular inactive activation is exactly neutral, and clearing that turns activity off is exactly neutral.

At an active state, a bounded-length complex path reaches mA and clearing. Normalized total rates are O(N^m), giving an earned polynomial absorption bound C(1+N)^ell/(B)_q. On a polylog cap N<=(log Z)^p, competing activation before clearing has probability Z^{-(q-1)+o(1)}, and mean active duration Z^{-q+o(1)}.

An inactive activation followed by clearing, if both residual-neutral, reduces N by one. Therefore a bounded number of such prescribed macrosteps reaches A=0 or a downward exit. From inactive A=0, at most m successive immigrations turn on activity; the first waits at a constant rate and the remaining m-1 each beat activation with probability at least c/Z. This gives downward success probability at least c Z^{-(m-1)} per bounded attempt block. Upward risk per block is at most Z^{-(q-1)+o(1)}. Large active states instead clear directly downward with probability1-o(1).

Positive renewal gives

    P(first residual exit is up and alive) <= Z^{-(q-m)+o(1)}=Z^{-h+o(1)},
    E(time to residual or cap exit) <= C Z^{m-1}.

For phi(Z)=Gamma(Z+1)^alpha times a compatible subexponential tilt, 0<alpha<1,

    E[phi(Z_next)1_alive]/phi(Z)
       <= Z^{-(1-alpha)h+o(1)}+O(Z^{-alpha h}) ->0.

The polynomially enlarged weight yields an actual finite stopped-cost value bounded by C(1+Z)^{m-1}phi(Z).

Only clearing can enter the cap from outside for large Z: fixed h gives L(Z+h)-L(Z)<=1, while activation adds m-1>=1 molecules and cannot cross inward from an already exterior integer N. Clearing gives a fixed-width collar L(Z)<N<=L(Z)+m. Threshold entry has finite support. On that collar B-Z=N+hI>=N, so the same factorial separation remains available IF an outer negative F margin has actually been earned.

The positive gap q-m is not an arbitrary convenient exponent: it is exactly the difference between the upward rare-event order q-1 and the forced downward order m-1. No statement is made here for q<=m; the credit orientation and comparison change, and this proof must not be extrapolated through that boundary.

The higher-composition-dimensional entropy/gluing obstruction identified in the cubic file remains. This structural trace result does not by itself close it.
