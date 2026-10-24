# Counted longitudinal rods: a finite construction and its conventional competitor

24 October 2026. Physical owner `/root/passive_lag`. This is an owned
continuum boundary-value construction following the point-mass kernel in
`../../thermal/NONLOCAL_KERNEL_CONSTRUCTION.md`, not a claim to have fabricated
a thermal support. The scalar longitudinal field, ideal joints and independent
rod routing are declared assumptions. Transverse/torsional solid modes are
not included. The finite-contact problem is separately written in
`mark/FINITE_NONLOCAL_ROD_CONTACTS.md`; intrinsic channel counts below are not
substituted for finite-device transmission.

There are two constructive conclusions. A fully counted four-range rod graph
beats the same-mass/stiffness/material nearest-neighbour rod chain. A stronger,
equally counted ordinary pendant then beats that graph, absent a common
displacement constraint. Separately, the connector fields prevent unlimited
inheritance of the point-mass kernel's vanishing channel width as its reach
grows. These statements have different quantifiers and comparators.

## 1. Complete longitudinal field and mass ledger

There is a point mass `m>0` at each vertex of period `a`. For every positive
shift `n=1,...,N-1`, place one uniform rod per cell between vertices `l,l+n`.
Its length is `n a`, stiffness is

    kappa_n = 12 K (N-n) / [N^2 (N^2-1)],

and its area is `A_n=kappa_n n a/E`. All rods have common finite wave speed
`c=sqrt(E/rho)`. Every edge is counted once per cell. The exact resources are

    sum n^2 kappa_n = K,
    sum rho A_n n a = K a^2/c^2,
    M_total = m + K a^2/c^2.

Thus growing reach does not by itself require growing total rod mass. The
total geometrical rod length is `a N(N-1)/2`, however; area, routing and
junction costs are not inferred from the mass identity.

A rod with endpoint amplitudes `(u_0,u_L)` has the exact dynamic-stiffness map

    kappa theta/sin(theta) [[cos(theta), -1],[-1,cos(theta)]],
    theta=omega L/c.

For Bloch phase `q` and vertex amplitude one, the complete nonpole equation is

    D(omega,q) = -m omega^2
       + 2 sum_n kappa_n theta_n
                    [cos(theta_n)-cos(nq)]/sin(theta_n) = 0,       (1)
    theta_n=omega n a/c.

This solves the rod wave equation, including its distributed inertia. Its
small-frequency expansion is

    D=K q^2-M_total omega^2+O((|q|+|omega|)^4).

The physical acoustic velocity is consequently `a sqrt(K/M_total)`.

Off the countable rod poles, each eigenmode has a unique rod profile for its
vertex amplitude. A mode with vertex amplitude zero is then zero everywhere.
Equation (1) is a polynomial of degree `N-1` in `cos(q)`, with nonzero leading
coefficient. Hence there are at most `N-1` roots in `0<q<pi`. Each regular
root pairs with its time-reversed root at `-q`, giving exactly one right
mover per pair, including negative-slope branches. In particular

    N_R(omega) <= N-1 almost everywhere.                         (2)

This is a full crossing count, not a band union. The derivative of the solved
elastic-minus-inertial form at fixed vertex amplitude is

    dD/d(omega^2)=-m-sum_n integral rho A_n |u_n(s)|^2 ds <0.       (3)

No derivative of the minimizing/stationary rod profiles remains. This proves
that the nonpole roots are eigenmodes of the full positive field problem.
Critical frequencies form a measure-zero set: locally frequency branches are
analytic by (3), and no nonpole flat branch is possible because (1) has a
nonzero highest harmonic.

At a rod pole the uneliminated fields must be used. Vertex-zero combinations
of sine modes can be flat and fluxless. Compatible vertex-bearing pole modes
may carry flux, so it would be false to call every pole a nonpropagating mode.
These isolated frequencies do not alter a frequency integral. Bound (2) gives
the rigorous tail budget `(N-1) integral_tail g`.

We use the ideal Landauer functional

    J_theta = integral_0^infinity N_R(omega) g_theta(omega) d omega,
    g_theta(omega)=[omega/(2 theta)/sinh(omega/(2 theta))]^2,
    theta=k_B T/hbar.

The corresponding conductance is `k_B J_theta/(2 pi)` for ideal contacts.

## 2. A finite positive continuum construction, N=4

Set `K=M_total=theta=1` in fixed reference units and `a/c=1/sqrt(101)`.
The point mass is `m=100/101`, and

    (kappa_1,kappa_2,kappa_3)=(3/20,1/10,1/20).

All rods, including their infinitely many longitudinal modes, are retained.
The comparator has the same point mass, total mass, material speed, period
and relaxed stiffness: one length-`a` rod of stiffness one per cell. This
is the unadorned nearest-neighbour comparator, not the strongest conventional
resonant support.

### 2.1 Only the acoustic band occurs below the first rod pole

The form-domain constraint setting the one vertex amplitude to zero has
codimension one in every Bloch fiber. It leaves independent fixed-end rods.
Min-max interlacing therefore places the second and all higher full-fiber
eigenfrequencies at or above

    omega_D=pi sqrt(101)/3 > 21/2.

Below that pole, (3) and the static stiffness imply a unique lowest branch
`omega(q)`, starting at zero for `q=0`.

### 2.2 Bounds on every acoustic turning point

Put `y=cos(q)` and `B_n=kappa_n theta_n/sin(theta_n)>0`. Then

    D_q=2 sin(q) [12 B_3 y^2+4 B_2 y+B_1-3B_3].               (4)

Since `t/sin(t)` increases on `(0,pi)`, the constant term is negative.
The quadratic in brackets is positive at both `y=1` and `y=-1`; the latter
is `9B_3-4B_2+B_1>0`. It thus has one root in each of `(-1,0),(0,1)`.
Along either critical-root curve its total derivative in frequency is just
`D_omega<0`, because `D_y=0`. Each curve can therefore intersect the acoustic
dispersion at most once. The branch has at most two interior stationary
points, in the order maximum then minimum when both occur.

At zero frequency the exact stiffness polynomial is

    D_static(y)=4/5-(2/5)y^2-(2/5)y^3.

It is at most `4/5` everywhere and at least `20/27` on `[-1,0]`.

At `omega=23/25=.92`, with `z_max^2=9 omega^2/101`,

    D <= (4/5)/(1-z_max^2/6)-(100/101) omega^2 <0.             (5)

Here `sin z>=z(1-z^2/6)` and `cos z<=1` were applied to each rod. Thus every
acoustic frequency is below `.92`.

At `omega=21/25=.84` and `y<=0`, use

    z[cos z-C]/sin z
       = (z/sin z)(1-C)-z tan(z/2)
       >= (1-C)-z tan(z/2),
    tan(z/2) <= (z/2)/(1-z^2/8).

Together with `sum n^2 kappa_n=1`, this gives

    D >=20/27-omega^2 [(100/101)
                      +(1/101)/(1-9 omega^2/(8*101))] >0.     (6)

Consequently the negative-`y` acoustic minimum, if it exists, and the
`q=pi` endpoint are above `.84`. Equations (4)-(6) bound the complete
acoustic total variation by

    TV_[0,pi] omega <=3(.92)-2(.84)=1.08.                      (7)

The monotone case is bounded by `.92`, and the one-maximum case by `1.0`;
thus they obey (7) as well. Coarea counts every acoustic crossing, so its
weighted conductance is at most (7), since `0<g<=1`.

For `theta=1`, the elementary full Bose tail is

    integral_R^infinity g_1(omega) d omega
      <= exp(-R)(R^2+2R+2)/(1-exp(-R))^2.                     (8)

Equations (2), (7), (8) at `R=10.5` prove

    J_Fejer <1.092.                                          (9)

### 2.3 Same-resource nearest-neighbour comparator

The local rod has

    cos q=cos(alpha)-(m omega^2/2) sinc(alpha),
    alpha=omega/sqrt(101).

For `0<=omega<=2`, it lies between `1-omega^2/2` and one, hence in `[-1,1]`.
It has one propagating channel throughout that interval. Monotonicity of
the Bose weight and `sinh(1)<6/5` imply

    J_local >=2 g_1(2) >25/18 >1.388.

Thus (9) is a genuine finite positive *longitudinal continuum* improvement
over this counted local rod comparator. It does not assert a complete
material device advantage or an optimum among resonant supports.

For the stronger comparison below we also need a lower bound on this
Fejer graph. The acoustic endpoint exceeds `.84`, so continuity gives at
least one channel on `[0,.84]`. The series inequality
`sinh(t)/t<=1/(1-t^2/6)` gives `g_1(omega)>=1-omega^2/12` there. Therefore

    J_Fejer >=.84-.84^3/36=.823536.                           (10)

## 3. A counted ordinary pendant is a stronger competitor

Retain `K=M_total=theta=1`, `a/c=1/sqrt(101)`. Use one backbone rod per cell,
one backbone point mass `m_b=1/1000`, and a side point mass connected by a
rod of length `.4a` and stiffness `k=2/5`. Its mass is `.064/101`; set

    m_s=1-m_b-1/101-.064/101 >0.

Both rods have the same material speed. At nonpoles define

    alpha=omega/sqrt(101), s=.4 alpha,
    A=k s cot s, B=k s csc s,
    Z_eff=-m_b omega^2+A-B^2/(A-m_s omega^2),
    cos q=cos(alpha)+sinc(alpha) Z_eff/2.                      (11)

This is the exact two-node/rod Schur complement, not a massless pendant
approximation. With one intercell rod, (11) implies `N_R<=1` almost
everywhere, including all high internal-rod bands.

For `.65<=omega<=5.8`, `m_s(.65)^2>k>=A`, so the side denominator is
strictly negative and `Z_eff>A-m_b omega^2`. Since `0<s<pi/2`,

    A-m_b omega^2 >= k[1-(.4)^2(5.8)^2/(2*101)]-m_b(5.8)^2
       > [(5.8)^2/101]/[1-(5.8)^2/(8*101)]
       >= 2 alpha tan(alpha/2).                             (12)

Every comparison in (12) is a strict rational inequality after using
`sin t<=t`, `cos t>=1-t^2/2`. Equations (11)-(12) prove `cos(q)>1` on the
whole interval: it is a complete stopband, not a missed optical branch.
The one-channel bound and (8) now give

    J_pendant <=.65+integral_5.8^infinity g_1
              <.8 <.823536 <=J_Fejer.                        (13)

No fine numerical integration is needed to establish this winner in the
stated resource class.

The pendant rod area is `.16 K a/E`, while the three Fejer rod areas are
`.15,.20,.15` times `K a/E`. The pendant therefore does not win by a
smaller minimum rod area. Its per-cell total rod length is `1.4a` versus
`6a`, and its maximum rod length is `a` versus `3a`. Its additional rod
mass was subtracted from its point masses. Total mass and static stiffness
match exactly. Its very light backbone point mass can, however, incur
substantial quantum motion or fail a real joint-volume requirement. A
range-matched physical comparison must calculate those costs for both
complete fields. Neither topology is declared feasible by this algebra.

## 4. Why increasing reach no longer makes full rod heat vanish

This independent derivation follows the interval mechanism jointly checked
with the warm thermal owner. Normalize `x=omega a/c`,
`mu=K a^2/(m c^2)`, `b_l=B(N-l)`,
`B=12mu/[N^2(N^2-1)]`. Equation (1) becomes

    Dbar=-x^2+sum_l T_l,
    T_l=2 b_l l x [cos(lx)-cos(lq)]/sin(lx).

Assume `0<mu<=.01`, initially `N>=12` divisible by 12. For integers
`2N/3<=n<=3N/4`, put

    x_n=pi/n, I_n=[x_n+b_n/x_n,x_n+2b_n/x_n].

These intervals are disjoint, avoid all rod poles and have upper endpoints
at most `X_N=3pi/(2N)+3mu/N^2`. Set `q_j=j pi/n` for `j=0,...,n`.

Here are full uniform remainder bounds. At `x_n`, pair rods `n-ell,n+ell`.
Their trigonometric numerators coincide, while

    (n-ell)(N-n+ell)-(n+ell)(N-n-ell)=2(2n-N)ell.

Using `sin(pi ell/n)>=2ell/n`, their total absolute contribution is at
most `4pi B(2n-N)(N-n)<=(pi/2)BN^2`. The remaining indices are
`1<=l<=2n-N`; the chord bound
`sin(pi l/n)>=3sqrt(3)l/(4n)` gives contribution at most
`(2pi/sqrt(3))BN^2`. Hence, for `R_n=sum_(l!=n)T_l`,

    |R_n(x_n,q_j)|<64mu/N^2.                                 (14)

For a shift `0<=delta<=3mu/N^2`, let `h_l=min(l,|l-n|)` for `l!=n`.
The centre sine bound and its Lipschitz estimate give

    |sin(l(x_n+delta))| >=(2-9mu/4)h_l/n >=h_l/n.

No other pole occurs on this segment. Direct differentiation gives

    |T_l'|<=4 b_l l [1/|sin(lx)|+lx/sin^2(lx)].

Each positive value of `h_l` occurs at most three times; thus
`sum 1/h_l<=3N` and `sum 1/h_l^2<=pi^2/2`. With `lx<3pi/2` and
`n<=3N/4`,

    sum_(l!=n)|T_l'|
      <=[108+(81/4)pi^3] [N^2/(N^2-1)] mu <768mu.

Combining with (14),

    |R_n(x,q_j)|< [64mu+2304mu^2]/N^2 <.06x_n^2.             (15)

For `x in I_n`, write `epsilon=n(x-x_n)`. The nth term is

    2 b_n n x cot(epsilon/2)  (j even),
    -2 b_n n x tan(epsilon/2) (j odd).

The even term is at least `1.5x_n^2`, the odd term nonpositive, and
`x^2<1.002x_n^2`. Equation (15) therefore gives alternating strict signs
of `Dbar` at `q_0,...,q_n`. There are at least `n` distinct roots in
`(0,pi)`. Equation (3) and time reversal turn them into at least `n`
right-moving channels almost everywhere. The degree is `N-1`, so this
does not assert that these roots exhaust all channels.

Finally,

    sum_n n |I_n| = (B/pi) sum_n n^2(N-n) >=mu/(9pi).

Consequently, for every fixed dimensionless temperature
`theta_bar=(k_B T/hbar)a/c>0`,

    Jbar_N >=[mu/(9pi)] g_(theta_bar)(X_N).                   (16)

For arbitrary `N>=13`, use `ceil(2N/3)<=n<=floor(3N/4)`; the same bounds
hold and the width factor in (16) becomes
`[N^2/(N^2-1)](1-12/N)`. It tends to one, closing the unrestricted
sequence rather than just the multiples-of-12 subsequence. Therefore

    liminf_N J_N >= (c/a) mu/(9pi)>0.                        (17)

The intervals have width `O(mu/N^2)`, but each contains `O(N)` channels,
and `O(N)` distinct rods provide them. This complete-field effect is missed
by the point-mass bandwidth. It does not rule out finite useful suppression,
as Section 2 demonstrates, nor rule out other nonlocal connector designs.

## 5. Review and physical boundary

`certify_distributed_comparisons.py` checks the strict rational inequalities
in Sections 2-3 and exponential tails using exact `Fraction` bounds, without
quadrature or SciPy. The warm thermal owner independently reconstructed
Section 4 in `../../thermal/DISTRIBUTED_ROD_CHALLENGE.md`, including the
all-integer sequence extension. Its 55-digit finite tests are supporting
diagnostics, not the proof of the uniform estimates.

The established nonlocal-dispersion mechanism has strong primary ancestry:
Kazemi et al., PRL 131,176101 (2023), arXiv:2302.00591, and Chen/Kadic/Wegener,
Nature Communications 12,3278 (2021), DOI 10.1038/s41467-021-23574-2. The latter
explicitly shows long-beam resonances absent from a lumped dispersion model.
`sources/NONLOCAL_KERNEL_PRIMARY_PHYSICAL_AUDIT.md` records the full-source
read and distinguishes driven elastic spectra from measured heat transport.

Uniform axial rods are a deliberate complete *longitudinal* realization.
Its long-link routing, positive point masses, rod fields and ideal joints
are explicit. A full solid needs all polarizations, actual contacts and
material constraints, not a repetition of this scalar count. In the distinct
same-material Fourier-conduction regime, edge heat conductance is
`(kappa_thermal/E)` times edge stiffness, so relaxed macro conductivity is
proportional to `sum n^2 kappa_n=K`, not to `sum kappa_n`. No diffusive
thermal advantage is inferred. Sections 2 and 3 identify the conventional
winner in the displayed longitudinal class, while the fair quantum-motion
and real-junction comparison remains separate.
