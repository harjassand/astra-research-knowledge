# Independent audit: complete affine-projector WH3 entropy theorem

2026-10-25. **PASS.** `wh3_all_two_level_inputs_entropy_theorem.md` proves Delta_N(aI+bP)>=0 for every finite-dimensional system-reference projection P and every a,b>=0, not both giving the zero operator. No flat reference marginal is assumed. The shifted interval is paid exactly; no concavity of Delta_N or free Jensen-gap removal is used.

The spectral scope is important: this is the affine-projector class, equivalently at most two full-space eigenvalues counting zero on the applicable product space. Two positive eigenvalues plus an additional nonproduct kernel generally give three spectral levels and do not follow.

## 1. Exact source interface is already acquired

The all-projector proof and its independent audit establish, on the dense maximal-marginal-rank class, 9B=X_1 with B=E(P),

X_r=[[rI+ZZ*,Z sqrt V],[sqrt V Z*,V]],
H=Z*Z, V>0, H+V<=8I.

The last bound comes from the projection complement index, not from equal trace. The independent operator-Schur audit checks the block inversion formula and genuine noncommutative integral comparison. These are the exact imported interfaces; there is no additional scalarization assumption.

## 2. Shifted logarithmic remainder

For c>=0, the ordinary logarithmic resolvent identity, with lower integration endpoint shifted by c, gives

Plog(X_r+cI)P-log(r+c)I
=Z integral_c^infinity [s/(r+s)]D_r(s)^-1 ds Z*,

D_r(s)=(r+s)(V+sI)+sH.

The integral converges in norm by the bound on its integrand I/(r+s)^2. This remains the same exact Schur remainder as in the unshifted theorem, not a replacement state.

With C=(P+3B)/4=X_4/12, tau>0, u=9tau and v=12tau=4u/3, the compressed expression

Plog(B+tau I)P-2Plog(C+tau I)P+log(1+tau)I

is exactly

g(u)I+Z[integral_u^infinity k_1(s)ds-2integral_v^infinity k_4(t)dt]Z*,

g(u)=log[(u+1)(u+9)/(u+3)^2].

The scale terms were independently checked; the coefficient log(1+tau) is necessary for this exact g.

## 3. The unmatched interval is real and fully paid

The audited unshifted positive transport is monotone and matches the tail starting at u to the tail starting at

t(u)=u-3+sqrt((u+1)(u+9)).

Restricting the positive operator integrand comparison to this tail gives integral_u k_1>=2integral_t(u) k_4. It does not justify dropping the interval from v to t(u). The latter endpoint is indeed at least v. In transport coordinates z=sqrt((u+1)/(u+9)), the exact difference is

t(u)-v=8(3z-1)/[3(1-z^2)]>=0.

For its cost, D_4(s)>=s[(s+4)I+H] by V>=0. Inverse monotonicity and congruence therefore give

Z k_4(s)Z* <= (1/(s+4)) Z[(s+4)I+H]^-1Z*
            <=8/[(s+4)(s+12)]I.

The second comparison follows by singular-value functional calculus: every nonzero eigenvalue is h/[(s+4)(s+4+h)] with 0<=h<=8. The function increases in h. This does not require H and V to commute.

The doubled integral of this bound over the missing interval is exactly

16 integral_v^t ds/[(s+4)(s+12)]
=2log[((t+4)/(t+12))((v+12)/(v+4))]
=log[(u+1)(u+9)/(u+3)^2]=g(u).

Thus the scalar baseline term pays the whole negative interval and proves the compressed inequality. Four fresh exact symbolic checks verify the cutoff factor, matched ratio, integral antiderivative and exponential form of this identity. The conclusion follows analytically from their positive domains, not from numerical quadrature.

## 4. Extension to arbitrary projections has no identity-enlargement error

The constructive maximal-marginal-rank projection approximants from the earlier theorem converge in a fixed enlarged reference space. For tau>0 the shifted matrices are uniformly faithful, so ordinary continuous functional calculus extends the compressed inequality directly. Its limiting compression is wholly inside the original reference block; the extra directions do not affect it. At tau=0 the earlier uniform supported-log tail proof applies.

This order of argument is safe: first extend the compressed source inequality, then differentiate the physical deficit in the original space. Alternatively, adding an identity on extra orthogonal reference directions would contribute exactly zero deficit by direct-sum additivity, but that alternative is not needed here. No arbitrary partial-trace monotonicity of Delta_N is used.

## 5. The derivative is an actual physical derivative

For A_r=I+rP, all A_r, N(A_r), E(A_r) are faithful for r>=0. Since E is self-adjoint and EN=E,

Delta_N(A_r)=Tr A_r log A_r+Tr E(A_r)log E(A_r)-2Tr N(A_r)log N(A_r).

Differentiation gives exactly

Delta_N'(r)=m log(1+r)+Tr B log(I+rB)-2Tr NP log(I+rNP).

The identity terms cancel because all three derivative traces are m. Self-adjointness of N and unital CP Jensen yield

Tr NP log(I+rNP)<=Tr P log(I+rN^2P)=Tr P log(I+rC).

Also Tr B log(I+rB)=Tr P log(I+rB), because the logarithm belongs to the range of E. Thus

Delta_N'(r)>=Tr P[log(1+r)I+log(I+rB)-2log(I+rC)].

For r>0 this is exactly the shifted compressed inequality with tau=1/r: all scalar log r terms cancel. Therefore Delta_N'(r)>=0. Integrating from Delta_N(I)=0 proves the whole ray I+rP. This is the derivative of the homogeneous deficit, not a derivative of its varying-trace normalization; no incorrect normalized monotonicity inference is made.

Positive scaling gives aI+bP for a>0. The zero-lower-level endpoint follows by entropy continuity or the already proved projector theorem. Normalizing afterward divides the homogeneous deficit by the positive total trace and preserves its sign.

## 6. Independent checks and final scope

`wh3_two_level_independent_checks.py/.json` contains four exact transport identities and nine bounded physical diagnostics: three reference dimensions/projection ranks, each at r=0.03,1,20. It independently implements the WH3 channel, physical deficit, derivative and compressed lower bound. All checks pass. These tests are diagnostics only; the proof above is the dimension-independent audit.

The theorem is a genuine nonflat spectral extension of the projector result and directly establishes the full target on its affine-projector class. It does not extend automatically through arbitrary spectral layer decompositions, mixtures or support truncations. General three-or-more-level inputs remain open. No historical novelty or engineering consequence is established by this mathematical audit alone.
