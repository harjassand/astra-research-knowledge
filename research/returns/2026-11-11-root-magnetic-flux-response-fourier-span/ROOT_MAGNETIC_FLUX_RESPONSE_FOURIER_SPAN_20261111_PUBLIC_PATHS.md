Magnetic flux-response programming: a paid Fourier algebra and its physical gap
ROOT, 11 November 2026 Brisbane. Mathematical construction, not a compiler.

1. OUTPUT AND AN ACTUAL IDEAL-FLOW RESTRICTION

For a prescribed incompressible velocity, induction is linear in B. After an
eraser has reduced B to an unknown constant H, a meaningful additional output
is B_target(x)=Pi(x)H. Requiring mean Pi=I and divergence-free columns preserves
mean B=H and div B=0 for EVERY H. It also respects B0=h_B=0 invariance: H=0
then has target zero. A fixed nonzero target independent of H would fail this
invariant test. These necessary conditions do not prove reachability.

For a volume-preserving ideal flow Phi isotopic to identity, the three columns
of its response to constant fields are Phi_*e_j. They commute pairwise, because
pushforward preserves vector-field brackets, and their determinant is one.
General divergence-free mean-I matrix fields need satisfy neither restriction.
For example Pi=I+theta cos(2pi x_3)e_2 e_1^T has determinant one and admissible
columns, but [Pi e_1,Pi e_3]=2pi theta sin(2pi x_3)e_2 is nonzero. Thus even
this elementary target is not the three-column response of ONE ideal flow.
This is a boundary of the ideal representation, not a resistive obstruction.

2. EXACT DIFFUSION/INDUCTION COMMUTATOR

Use normalized operators D=(2pi)^-2 Delta and
 L_u b=(2pi)^-1[(b.grad)u-(u.grad)b].
This normalization removes known universal powers of 2pi; physical operators
are recovered by multiplying by those constants. Put e_k=exp(2pi i k.x),
u=a e_k, v=c e_l, with k.a=l.c=0. For b=z e_q,
 L_u b=i[a k^T-(q.a)I]z e_(q+k),
 [D,L_u]b=-(|k|^2+2k.q)L_u b.

Consequently on every CONSTANT H,
 [L_v,[D,L_u]]H=d r_k^T H e_m,
 m=k+l,
 d=(l.a)c-(k.c)a,
 r_k=|k|^2 k+(|k|^2+2k.l)l
    =|k|^2 m+2(k.l)l.                                      (2.1)
One has m.d=0. To verify signs without a formal control argument: the first
product L_v[D,L_u]H is |k|^2 d k^T H e_m. The second product
[D,L_u]L_v H is -(|k|^2+2k.l)d l^T H e_m. Their difference is (2.1).

Unlike the first-order direction L_(d e_m)H=i d m^T H e_m, (2.1) can have a
covector r_k not parallel to m. This is the additional algebraic operation.

3. RATIONAL POLYNOMIAL SPANNING OF EVERY ADMISSIBLE MATRIX MODE

Fix m in Z^3 minus {0}. Any matrix C with m^T C=0 decomposes as the THREE
column tensors (C e_j)e_j^T, with each d=C e_j perpendicular to m. We show
how to produce d e_j^T by a fixed number of algebraic directions.

If m is parallel to e_j, write m=m_j e_j. Then
 d e_j^T=(d m^T)/m_j,
so the first-order induction direction suffices. Its scalar division has a
nonzero integer denominator with |m_j|>=1.

Otherwise choose sigma=1 if m_j>=0 and sigma=-1 if m_j<0, and put
 k=m+sigma e_j, l=-sigma e_j.
Then k,l are nonparallel integer vectors, |l|=1, |k|<=|m|+1, and
 k.l=-sigma m_j-1 !=0,
 r_k=|k|^2 m+2(m_j+sigma)e_j.                              (3.1)
The integer |m_j+sigma|=|m_j|+1 is at least one.

For ANY desired d perpendicular to m, construct
 a=l-[(k.l)/|k|^2]k,
 t=l.a=|k cross l|^2/|k|^2,
 c=d/t+(k.d)a/t^2.                                       (3.2)
Then k.a=0, l.c=(l.d+k.d)/t=0 and
 (l.a)c-(k.c)a=d.
Moreover |a|<=1, t>=|k|^-2, |k.d|=|l.d|<=|d|, so
 |c|<=(|k|^2+|k|^4)|d|.
All quantities in (3.1)--(3.2) are rational if d is rational. Hence
 d e_j^T=[d r_k^T-|k|^2 d m^T]/[2(m_j+sigma)]              (3.3)
is one double-commutator direction plus one first-order direction.

The real sine/cosine version has only constant overhead. For a real bilinear
operator B(v,u), the identities
 Re B(v_c+i v_s,u_c+i u_s)=B(v_c,u_c)-B(v_s,u_s),
 Im B(v_c+i v_s,u_c+i u_s)=B(v_c,u_s)+B(v_s,u_c)
isolate the m=k+l frequency and cancel the difference frequencies. Split
complex target amplitudes into real and imaginary parts. Thus each sine/cosine
matrix mode needs only a universal constant number of real generators and
signed real scalar combinations. No complex physical field is requested.

For modes of |m|<=N, generator frequencies are <=N+1, scalar sizes and
polarization norms are polynomial in N and the target coefficient size.
Rational numerator/denominator bit lengths are O(b+log(2+N)) for coefficient
bit length b, with a universal constant multiplier. The explicit construction
uses O(1) fixed-dimensional rational operations per input matrix mode. It does
not require a small-divisor, spectral or exact-real oracle. Enumerating all
frequencies <=N, when wanted, costs O((1+N)^3); reading an explicit sparse list
and discarding larger binary frequencies costs its actual binary input size.

If ||Pi||H1<=K and |H|<=M, discarding modes |m|>N gives
 ||(Pi-Pi_<=N)H||L2<=C MK/N.
Thus N>=C MK/epsilon pays the desired L2 target truncation numerically; modes
with huge binary indices can be rejected by integer comparisons. This is a
target approximation and algebraic acquisition bound, not a control cost.

4. A CONCRETE NON-GRADIENT RESPONSE DIRECTION

For m=e_3 and output d=e_2, take k=e_3+e_1, l=-e_1,
a=(-e_1+e_3)/2, c=2e_2. Then t=1/2 and
 [L_v,[D,L_u]]H=2e_2(H_1+H_3)e_(e_3).
Subtracting the available first-order H_3 response leaves a nonzero multiple
of H_1 e_2 e_(e_3). Its real quadrature is the noncommuting-column example in
Section 1. Both its divergence condition and the extra covector are explicit.

5. WHAT POSITIVE DIFFUSION MIGHT ADD, AND WHAT IS NOT PROVED

For a SINGLE transverse Fourier shear u, one has L_u^2 H=0 and
 [L_u,[D,L_u]]H=0 on constants. Indeed L_u takes H to a mode parallel to a;
applying it again multiplies by k.a=0. The same argument applies after D.
For u+v the second double-commutator on constants therefore consists only of
cross terms. Their symmetric sum is
 [L_v,[D,L_u]]H+[L_u,[D,L_v]]H
   =d(r_k-r_l)^T H e_m,
 r_k-r_l=(|k|^2-|l|^2)m+2(k.l)(l-k).                      (5.1)
With (3.1), the component of (5.1) transverse to m has a nonzero e_j
coefficient. Replacing v by -v reverses these cross terms on constants while
the two self terms remain zero there. Symmetric conjugations of POSITIVE heat
by opposite ideal displacements suggest a way to cancel odd terms without
ever using a negative heat interval. This supplies an opening, not an emitted
schedule, a convergence theorem or a uniform unknown-resistivity operation.

The following gaps are material:
 - A Lie commutator formula often presumes negative drift time. Physical
   resistivity is positive and unknown; inverse heat is unavailable.
 - D does not vanish on already written nonconstant magnetic modes. Accumulated
   diffusion, cross terms and mode leakage must be paid for the WHOLE output.
 - rho(t) may change independently between legs. Algebraic cancellation at a
   fixed scalar weight does not yield a coefficient-blind ensemble compiler.
 - The displayed u,v need arbitrary polarizations and modes. The actual force
   has only twelve fundamental momentum actuators. A velocity ENDPOINT writer
   does not automatically realize an arbitrary prescribed velocity trajectory.
 - The physical velocity depends on H and B through Lorentz work. Prescribed-
   velocity induction and linearity in H do not remove this feedback.
 - One ideal flow has the restrictions in Section 1; sums of formal directions
   or linear combinations of separately run experiments are not physical
   realizations of their sum in a SINGLE fluid.
 - The previously accepted joint eraser destroys nonconstant B. It cannot be
   inserted freely after magnetic writing. Any velocity reset preserving the
   growing magnetic memory needs its own actual estimates.
 - Finite-dimensional spanning alone proves no positive-time density, uniform
   polynomial approximation, all-H simultaneous output or all-weak robustness.

Closed ideal words do return EVERY smooth vector field to itself, not merely
constants. Therefore extending short velocity reset estimates around known
smooth magnetic references Pi H is a specific possible bridge: the proof may
use H without the emitted force observing it. Smooth Pi-dependent residuals,
reference norms, unknown-coefficient errors, Lorentz terms and compositions
must all be bounded first. This bridge remains unconstructed here.

6. PRIMARY COMPARATOR AND SCOPE

Rissel, arXiv:2306.03712v2, https://arxiv.org/html/2306.03712v2,
Section 1.1 equations (1.3)--(1.6), Theorem 1.2 and Problem 1.4 were actually
read. The theorem uses known C^(m,alpha) data in a 2D doubly-connected domain,
localized controls in BOTH equations and zero first-cohomology magnetic
projection. Its nonzero common-projection question is left open there. It is
not the periodic resistive twelve-momentum-actuator ensemble considered here.
No unobserved theorem, alternative held source or generic topology obstruction
for the present 3D positive-resistivity compiler is imported.

The present result is EXACT Fourier GENERATOR spanning with rational costs
and a concrete ideal-representation boundary. It supplies neither arbitrary
Pi H programming nor a general impossibility. Those remain the full physical
and computational research question, with all representations open.
