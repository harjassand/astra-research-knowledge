# Selective memory thermalization: a constructive preparation escape

29 October 2026. Root mathematical receiver and full-record consequence.
This is an additional physical-operation model, not an apparatus claim.

## 1. A continuous state that stores an apparently memoryless record

Take (u,v) in [0,1)^2 with uniform baseline mu. Define the standard baker
map, apart from null binary-expansion ambiguities, by

 S(u,v)=(2u-b,(v+b)/2),          b=floor(2u),
 S^(-1)(u,v)=((u+c)/2,2v-c),    c=floor(2v).                 (1)

Both are supplied mathematical native operations. They preserve area:
each branch has determinant one and the two branch images partition the
square. In binary coordinates write

 u=.b_0 b_1 b_2...,       v=.b_(-1) b_(-2) b_(-3)... .

S shifts the binary origin forward by one, and S^(-1) shifts it backward.
Under mu all these bits are iid fair. The sole native visible read is
Y=b_0, xi=2Y-1. A forward record is exactly iid even though v stores its
past. The map is an idealized piecewise area-preserving operation, not the
smooth addressed diffusion of continuation3 and not a fabricated Hamiltonian
apparatus. Its actual duration, isolation and sensing would need suppliers.

For 0<a<1 the full target is

    nu(du,dv)=[1+a(2 floor(2u)-1)]du dv.                    (2)

With only (1), the root shift-coupling argument forces infinite square-root
moment for exact preparation, even when both directions and the full state
are known. Finite-error preparation has mean native cost Omega(1/epsilon),
and the root matching construction attains that order. Its future inverse
reads make the hidden-state accuracy consequential rather than a purely
unobservable mathematical demand.

## 2. The strong ordinary route and its precise failure

Execute S at least once. At each resulting endpoint accept with probability

    h(Y)=[1+a(2Y-1)]/(1+a).                                (3)

Otherwise execute S again and repeat. The actual current state is always
used; no copied proposal is restored. Every newly exposed forward bit is
independent of the previously exposed bits and the independent selector.
The acceptance probability per trial is s=1/(1+a). Thus the number T of
native calls is geometric with mean 1+a, and the accepted u coordinate has
EXACTLY the desired target density. Its unobserved future binary digits
remain independent fair bits. For a=1/3, low endpoints are accepted by one
fair coin and high endpoints always; all individual selectors are bounded.

This does not prepare (2). If T>=2, the previous endpoint was rejected and
therefore had Y=0. At the final state that previous bit is the leading bit
of v. Hence

 Pr(floor(2v_out)=1)=1/[2(1+a)],
 TV(Law(u_out,v_out),nu)>=a/[2(1+a)].                      (4)

At a=1/2 this error witness is 1/6, at a=1/3 it is 1/8. One supplied inverse
call and a visible read exposes it. Visible iid output does not justify iid
microscopic proposals or a fresh stationary restart after rejection.

More explicitly, with q=1-s=a/(1+a), the stored coordinate has density

    r(v)=sum_(k>=0) s q^k 2^k 1_[0,2^(-k))(v).            (5)

Its recent rejected zeros bias the stored past. The accepted current bit
and all its unobserved future digits are independent of this past. These
identities follow from the stopped iid bit stream, not from estimating a
hidden transition matrix.

## 3. A supplied operation that repairs exactly the affected coordinate

Add an actual operation R_t that keeps u fixed while v evolves as Brownian
diffusion on the unit circle, with generator D partial_v^2. Assume a
warranted lower mobility D>=D_min>0, noninvasive compatible control, and the
stated retained-record interface below. The rate need not otherwise be known.
This is a genuine additional selective actuator: fixing u while randomizing
v cannot be inferred from the availability of S or its inverse.

The heat kernel is

 p_t(v,w)=1+2 sum_(k>=1) exp(-4 pi^2 D k^2 t)
                          cos[2 pi k(w-v)].                (6)

Consequently, writing q_t=exp(-4 pi^2 D_min t),

 sup_v TV(R_t(v,.),Uniform)
    <=sum_(k>=1) q_t^(k^2) <=q_t/(1-q_t^3).                (7)

The last inequality uses k^2>=1+3(k-1). For 0<epsilon<=1,

    t_epsilon=log(2/epsilon)/(4 pi^2 D_min)                 (8)

is sufficient for (7)<=epsilon. For a physical circle of circumference ell
and diffusivity in length^2/time, multiply (8) by ell^2. This is a known
Fourier heat-kernel estimate, not a new thermalization law.

Apply R_(t_epsilon) once after (3) accepts. Since its bound is uniform over
the actual input v and leaves u fixed,

    TV(Law(final actual state),nu)<=epsilon.               (9)

The native-call mean is 1+a; the additional thermalization time is
O(log(1/epsilon)). With actual fixed native duration Delta, the mean time
apart from charged sensing/selection/switching overhead is

    (1+a)Delta+t_epsilon.                                 (10)

In contrast, the orbit-only lower bound requires mean time
Omega(Delta/epsilon) at fixed a. This is a change of physical resources,
NOT a same-resource speedup: selective hidden-coordinate diffusion is what
removes the old obstruction. A conventional algorithm supplied with R_t
can execute exactly this procedure. A genuine independent full baseline
initializer is another strong ordinary escape with its own preparation cost.

The protocol remains valid if a forward native call advances a bounded
positive number of binary positions chosen independently of the unexposed
bit stream and past state, with a fixed supplied state-independent law.
The jump law can be unknown: exposed endpoint bits are still iid fair and
unexposed future bits remain independent after acceptance. Its actual jump
duration and control interface must be charged; no arbitrary state-dependent
skip or kinetic family is included by that observation.

## 4. Complete retained preparation records and later adaptive programs

Let D be a retained old record such that the initial (u,v) law conditional
on D is the warranted mu. Let R contain D, all visible preparation reads,
all selector values, the rejection count, and completion timestamps from
the declared compatible protocol. It may contain extra randomness independent
of the unexposed bit stream. The final observed bit Y is a function of R.
For fixed (1), the native duration is fixed, so its timing reveals no further
unexposed digits. More general timing needs the same actual information
condition, not just a nominal kernel.

By independence of unread iid bits at a stopping time, conditional on R
the accepted u is uniform on its observed half interval. The stored v can
have any conditional distribution and can be correlated with u. Define a
reference joint law by keeping exactly the actual R and accepted u, then
replacing v by an independent uniform coordinate. Its state marginal is nu;
conditional on R its state law is nu conditioned on the already retained Y.
The reference is a positive comparison law, not an asserted exact physical
initializer supplied for free.

Uniformity in (7) proves the joint bound

 TV(Law(R,u,v_after_Rt), Law(R,u,V_uniform))<=epsilon.       (11)

Thus ANY later actual adaptive program, including choices depending on R,
has complete output-record discrepancy at most epsilon relative to that
reference. There is no factor growing with later observation depth. The
proof is contraction of TV under the common physical continuation kernel,
on the joint retained-record/physical-state space.

This is not independence from the record: R already contains Y. Nor does
it admit arbitrary prior calibration that changed the conditional initial
law. If D contains information about unread binary digits, the stated
conditional baseline premise can fail and must be repaired or analyzed.

### The thermalizer's instrument matters

The supplied heat operation above has no retained record of its individual
bath kicks; its retained timing is the deterministic chosen t. Future bath
innovations have the declared Markov independence. Any additional apparatus
state affecting subsequent operations belongs in the physical model.

If a thermalizer exposes an additional retained record A, its actual JOINT
instrument must satisfy an appropriate uniform analogue of (7); a marginal
heat kernel is not enough. For example, revealing the Brownian displacement
modulo one makes v_out=v_in+A. Conditional on A and a known initial v there
is no uniform randomization at all, even when the marginal heat kernel is
near uniform. One cannot count the heat noise as inaccessible in (11) while
giving its record to the later controller. This failure is part of the
supplier boundary, not an optional disclaimer.

## 5. What the construction establishes

The counter's bounded stationary control, critical matching's actual
preparation, and selective thermalization have different suppliers and costs.
The latter prepares a reusable full state with a complete-record guarantee
because it removes the physical history that ordinary stopping leaves behind.
It does so without reconstructing the hidden kinetic dynamics, but it needs
the added isolated thermalizer and a warranted mobility/instrument contract.

No energy advantage, practical speedup, finite-precision apparatus or general
reset of arbitrary hidden systems is established. The baker map and its
binary representation are standard; thinning and heat mixing are ordinary
methods. The investigated consequence is the explicit precision/resource
separation and the physical record conditions under which the escape works.
The four-state complementary theorem shows that universal exact preparation
can also fail under uniformly rapid microscopic mixing, while its own
finite-error and added-sensing alternatives remain available.
