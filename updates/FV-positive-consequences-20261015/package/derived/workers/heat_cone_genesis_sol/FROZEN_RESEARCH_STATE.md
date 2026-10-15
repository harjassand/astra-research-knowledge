# Frozen research state: rational exposed ray and heat obstruction

Repository pin: `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`.
Date: 2026-10-15. Worker: heat_cone_genesis_sol. No repository files changed.

The main exact candidate is

\[
F=u^2+v^2+\frac{166}{3}uv-\frac{460}{9}w^2
 -\frac{52}{9}q(u-v),
\quad (u,v,w,q)=(a^2+c^2,b^2+d^2,ab+cd,ad-bc).
\]

Exact calculations acquired and preserved:

1. A rank-four rational acoustic Gram certificate; the four positive block
   weights are `8/3,4/3,8/9,4/9` in the construction being written in the
   standalone verifier.
2. Four real acoustic contacts are parameterized by
   `P(k)=17k^4-314k^2+17=0` and
   `A(k)=(203-17k^2,k(85k^2-1551),2k(944-51k^2),134)`.
   The determinant derivative in direction `e1 tensor (1,k)` reduces to
   `4(8-k^2)`, nonzero at every contact.
3. `exact_extremality.py` passes: the 20-by-9 contact criticality map has
   exact rank eight. A rational exposing functional, in the coefficient
   order `(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)`, is
   `(910741,1453621,324775,321232,0,0,244987,-432907,0)`.
4. The complete local null-correction space is classified by
   `verify_null_corrections.py`, a stdlib-only checker. It reconstructs all
   maps and certifies their ranks with nonzero modular minors. Full null
   dimension is 45; left-SO(2)-invariant null dimension is 15.
5. Exact contact-kernel conditions plus the candidate's finite symmetries
   leave one parameter `t` in an identity-diffusion closed-form correction.
   The rational jets
   `A=(1,0,0,2), H=(0,1,0,0,0,-1)` and
   `A=(1,-1,0,2), H=(0,0,1,-1,0,0)` impose the incompatible bounds
   `t >= 96130/1233` and `t <= 6280/293`.
   This is a pointwise-positivity obstruction, without an SOS restriction.
6. The candidate's input/output reflection and column-swap symmetries
   average any nonzero positive scalar input heat metric to a multiple of
   the identity. Together with item 5 this excludes every such heat metric.
7. At the acoustic contacts, any nonnegative determinant-square subtraction
   is forced to zero by item 2 and rank-one convexity. Thus adding that
   particular polyconvex ray cannot repair the heat obstruction.

The exact exposed-ray property implies: in a finite positive decomposition
of F into left-invariant heat-certified quartics and arbitrary polyconvex
quartics, collect all polyconvex pieces into P. This collected P is
left-invariant; the exposed-ray property applies to P and the invariant heat
pieces. Since F itself has no heat certificate, every heat summand must be
zero, leaving P=F. Therefore this proposed construction works for F if and
only if F itself is polyconvex. This does **not** prove that F is nonpolyconvex
or that the original noninvariant PC pieces are individually proportional.

Status retained: F polyconvexity UNKNOWN; F quasiconvexity UNKNOWN; full cone
equality UNKNOWN; external correctness and historical priority UNKNOWN.
The obstruction is to a stated certificate operation, not a compatible
negative Jensen field. The pointwise jet atoms are not a gradient law.

An optional extension allowing the skew-output mixed diffusion that survives
symmetry averaging is still exploratory; it is not a premise of the scalar
input metric theorem.

Primary machinery read: Bruno–Pasqualotto arXiv:2608.06367v1, Theorem 2,
Sections 2–3, Appendix A; Ball–Currie–Olver (1981), Sections 3–4;
Olver–Sivaloganathan (1988), differential-form representation discussion.
The null-space calculation is a constructive specialization of established
null-Lagrangian machinery, without a historical novelty claim.

Previous G input certificate was copied byte for byte into `inputs/` and
its seven exact verification groups passed. Its SHA256 remains
`4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000`.
