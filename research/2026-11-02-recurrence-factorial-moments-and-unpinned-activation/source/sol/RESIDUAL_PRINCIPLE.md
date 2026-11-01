# Availability-residual potential and the actual neutral-layer problem

For a fixed nonnegative direction p and the ACTUALLY enabled source complexes at x, define

    M_p(x)=max_(source y<=x) p.y,
    R_p(x)=p.x-M_p(x).

At a state with no enabled source define the value separately; such a state is a singleton graph class. If a reaction y->y' fires from a source maximizing M_p(x), then y' is enabled at its true destination x'=x-y+y'. Therefore

    R_p(x') <= p.(x'-y') = p.(x-y) = R_p(x).              (1)

This exact pathwise inequality accounts for newly enabled sources and all evolving inventories. It needs no frozen fiber, phase equilibrium, neighboring Green entry or comparison of clocks. The correction p.x-R_p(x) is bounded by the fixed source list.

It suggests a general residual lift: replace a geometric count potential G(x) by min_(source y<=x) G(x-y). A firing from a minimizing source cannot increase that residual potential. The primitive is distinct from the banked failed ADJOINT residual-factorial softmax. It is a primal availability construction.

## The first tested claim is false, and the failure identifies the next operation

Equation (1) is not enough to make the generator negative. In the weakly reversible conservative cubic cycle

    A+2B --4--> 2B+C --1--> B+2C --7--> A+2B,
    0 <-> A (unit rates),

take p=(0,1,0) and x=(1,n,0), n>=3. The maximal-source reaction A+2B->2B+C has rate 4n(n-1) and changes R_p by exactly zero. Immigration also changes it by zero. Death of the last A copy removes the available B-level-two source and changes R_p by +2 at rate one. Consequently

    L R_p(1,n,0)=2

on an infinite boundary ray. This exact calculation, not a numerical slope, falsifies the naive global residual ansatz. At its actual fast destination (0,n,1), however, the next reaction has a strictly decreasing residual jump. The missing operation is a physical-clock correction through the NEUTRAL layer, with its real last-copy entrances and unpinned outputs.

On the former Ultra's coupled rank-two prototype the same residual has LR=2 at (2,n,0), LR=0 on several other low-C rays, and strict negative values elsewhere. Its scalar-port obstruction is therefore not repaired merely by naming a multivariable residual. `residual_potential_search.py` preserves the exact source, phase and polynomial calculations.

This remains a positive approach: strict source-order descent is already pathwise, and the adverse lower-order residual terms are identified explicitly. A valid completion must acquire the neutral-layer correction for the full finite source geometry and prove that subsequent layers terminate or close. Borrowing a negative margin from a supplied global boundary law would be circular.
