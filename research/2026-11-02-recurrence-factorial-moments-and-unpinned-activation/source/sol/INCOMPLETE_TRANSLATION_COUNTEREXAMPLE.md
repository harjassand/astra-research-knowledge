# Why inward finite cells do not alone imply recurrence

This is an author-derived CTMC construction. It is NOT a mass-action counterexample. Its purpose is to locate a real limitation of the proposed global representation. No historical novelty is asserted.

The construction has all of the following simultaneously: a finite set of bounded jump directions, polynomially bounded rates and a positive lower bound on nonzero rates; a factorial product-Poisson reference which is nonexplosive and positive recurrent; actual/reference edge-rate ratios in [1,16]; and from every large state a one-step, zero-barrier coordinate deletion cell with stationary endpoint preference 1/x_i. Nevertheless the actual process has positive probability of finite-time explosion.

What it lacks is the FULL TRANSLATION-COMPLETE, fixed finite polynomial source list of a mass-action network. Thus it disproves a tempting coarse reduction, rather than weak-reversibility recurrence.

## States, reference, and fast corridor

On N^3 include ordinary births x->x+e_i at rate 1 and deaths x->x−e_i at rate x_i. These alone have mu(x)=1/(x_1!x_2!x_3!) as a reversible finite measure. They provide one-step deletion words and local inward cells at every positive coordinate.

For every EVEN n>=20, define n^2 grid states

    v_n(i,j)=(n+i,n+j,3n−i−j),  0<=i,j<n.

Every grid has total count 5n; distinct n give disjoint grids. Take a Hamiltonian path from (i,j)=(0,0) to (0,1): first visit (0,0), then snake over columns i=1,...,n−1 across rows j=0,...,n−1, and finally return up column i=0 from j=n−1 to j=1. Since n is even the last snake point is (1,n−1), adjacent to the first point of that last column. Within-grid increments are drawn from ±(1,0,−1), ±(0,1,−1). Connect the last point of grid n to the first point of grid n+2; the fixed increment is (2,1,7). Concatenation gives an infinite simple path v_0,v_1,... . No corridor edge overlaps an ordinary birth/death edge.

For each forward corridor edge v->w, with lower grid parameter n, let r=mu(w)/mu(v), and set

    q0(v,w)=n^20 r/(1+r),   q0(w,v)=n^20/(1+r).

These two-state blocks are exactly mu-reversible. Within a grid, 1/4<=r<=4. Across grids,

    r=1/[(n+1)(n+2)^2 product_(k=0)^6(3n+k)],

so (6n)^−10<=r<=n^−10. All reference rates are polynomially bounded in total count. Reference total stationary activity is finite: the corridor contribution is bounded by a constant times sum_n n^22/(n!)^3. Thus the reference CTMC is nonexplosive and positive recurrent, with normalized mu. This implication can also be seen by constructing its stationary embedded chain with probability proportional to mu(x)q0(x), whose mean holding time is positive and finite.

Define the ACTUAL corridor rates by multiplying every forward rate by 16, leaving all reverse and ordinary rates unchanged. The full actual/reference ratios are in [1,16]. The rates remain polynomially bounded and nonzero rates have a positive global lower bound. The state-dependent corridor selection is the crucial non-mass-action feature.

## Actual restricted-corridor explosion

First suppress ordinary births/deaths. This gives a birth-death chain on path index k>=0, reflected at 0. Its unnormalized speed weights satisfy

    m_k = 16^k mu(v_k)/mu(v_0).

Write T_k=(sum_(j=0)^k m_j)/m_k and let lambda_k be its forward rate. The elementary finite hitting-time recursion gives

    E_0[tau_(k+1)−tau_k] = T_k/lambda_k.             (1)

Here tau_k is the first hitting time of index k; (1) follows by solving the finite birth-death Poisson equation, or by induction from m_k lambda_k=m_(k+1) mu_(k+1), with mu_(k+1) denoting the reverse RATE in this identity.

On tangent edges m_(k+1)/m_k>=4 and lambda_k>=3 n^20. Therefore T contracts by T_next<=1+T/4. On a cross-grid edge,

    T_start(next)<=1+(6n)^10 T_end/16.

If T_end<=2 in the preceding grid, then throughout the next grid T<=6^10 n^10, and at its final point

    T_end <= 4/3 + [1+6^10 n^10/8] 4^−(n^2−1) < 2.

The same bounds hold in the first grid, where T_start=1. For n>=20 the final strict inequality follows, for example, from n^10<=2^(n^2/2). Thus by induction all grid endpoints have T<=2. The distinction between the preceding n and the next n+2 only improves the polynomial upper bound.

Summing (1) over one grid and its outgoing cross edge gives

    E[time to advance through grid n] <= C(n^−8+n^−10),

with a finite explicit C (6^10 suffices after harmless enlargement). Across the outgoing edge lambda>=8 n^10/6^10. The series over even n converges. Hence the minimal restricted-corridor chain reaches infinity in finite expected time, and therefore in finite time almost surely.

## Restore every ordinary competitor

Before the first hit of the next path index, every state visited has total count at most the next grid's 5(n+2). The ordinary-jump hazard there is 3+|x|_1<=6n for n>=20. Multiplying the preceding time bound by 6n still gives a convergent series. Consequently, on the restricted corridor path

    E integral_0^T [3+|X_s|_1] ds < infinity,

where T is its explosion time. The integral is finite almost surely. Use independent ordinary-jump clocks along that path. Conditional on it, the probability of no ordinary event before T equals exp(−integral[3+|X_s|_1]ds), which is strictly positive. Its expectation is also strictly positive. On that event the FULL actual CTMC follows the exploding corridor. Since ordinary births/deaths make the graph irreducible, this is a genuine irreducible explosive chain.

Every state x with x_i>0 still has its unchanged two-state ordinary cell {x−e_i,x}; its exact stationary ratio is pi_cell(x)/pi_cell(x−e_i)=1/x_i. Its deletion word has length one, no count or factorial-energy overshoot, and removes any selected large coordinate. Therefore neither the strengthened deletion geometry nor the inward finite-cell odds controls the full dynamics without an additional global structural operation.

## Consequence for the live programme

The actual word clock and the constant-size cell comparison remain valid useful operations. A proposed proof that thereafter uses only polynomial rate bounds, bounded edge-rate distortions, finite inward cells, and linear monotone descent paths is false. A successful recurrence proof must exploit the complete raw translation list, fixed source monomials, or an equally strong additional identity. This construction supplies no obstruction to that genuinely chemical step, and is not a reason to abandon the recurrence question.
