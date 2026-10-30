# Joint volume-speed tracking of a spatial current program

30 October 2026. Central proof by Astra P1 root. It closes the missing joint
estimate for the changed, extensive elastic-carrier architecture. It is not
an assertion that the earlier dilute spatial outline was already proved.

## 1. Native information and physically evaluated target

Let B_y(s), y=1,...,N, be the signed sum of all horizontal native
displacements in row y. In the actual deployment filtration assume:

* each jump affects one row, has bounded size, and each row's total
  conditional intensity is at most C N;
* each row's predictable total drift is bounded by C;
* sensing and auxiliary forcing leave the native path law unchanged.

No independence of rows is assumed. Vertical exchanges and persistent hidden
memory may couple their states. Homogeneous horizontal exclusion rates within
each row supply the zero-force drift identity by telescoping. Bounded weak
fields F/N add bounded drift. Arbitrary heterogeneous reciprocal horizontal
edge rates do not automatically supply this interface.

Put h_y(t)=B_y(N^2t)/N^2 and use the step embedding h_N(y,t). Let S be a
fixed smooth convolution on the vertical circle with positive normalized
analytic kernel K. For example, take the Poisson kernel whose Fourier
multiplier is r^|j| with fixed 0<r<1. S_N is its integral against the actual
step embedding, sampled at row locations; row and column sums are one.

Choose a specified computable function psi(y,t,z), C^1 in t, C^2 in z,
smooth periodic in y, with bounded first and second derivatives and
psi(y,0,0)=0. The physical auxiliary target is

\[
 q_y(t)=\psi(y/N,t,(S_Nh(t))_y)-h_y(t),\qquad
 Z_y(s)=N^2 q_y(s/N^2).                                   \tag{1}
\]

Examples include psi=v(y)t+alpha tanh(z), and rational bounded-derivative
functions. An arbitrary abstract smooth function is not granted a free
evaluator. A Fourier truncation of S to O(log N) modes, with O(log N) bits
per relevant value and the stated evaluator, supplies o(1/K_N) error on
the polynomial count range used below. Its communication is charged in the
resource note. There is no dense instantaneous physical transformer.

### Why the smoothing changes the scientific program

The native current LDP normally uses a weak current topology. Pointwise
nonlinear composition h->psi(h) is not continuous there: rapidly oscillating
fields can converge weakly while their squares or bounded nonlinear images
have a different limit. S is therefore an actual information operation,
not a stronger topology silently assumed for native paths. The final map
uses psi(S h), not psi(h).

## 2. A vector source lemma

On macroscopic time, q has drift bounded in every coordinate by C, jumps
of Euclidean norm at most C/N^2, and for every predictable vector v its
martingale part satisfies the conditional exponential bound

\[
 \log E\exp\!\left[\theta\int v\cdot dM^q\right]
 \le {C\theta^2\over N}\int\|v(t)\|_2^2dt,
 \quad |\theta|\sup_t\|v(t)\|_2\le cN^2.                 \tag{2}
\]

The displayed form means the usual compensated exponential
supermartingale bound, also valid with predictable stopping. No conditioning
on a future good observation event is used.

Proof: the normalized native row bracket is at most C/N, with no simultaneous
cross-row jump. The Jacobian of (1) is diag(psi_z) S_N-I, of uniformly bounded
Euclidean operator norm. Exact jump quotients have the same Schur bound:
their absolute entries are bounded by C(S_N)_{yj}+delta_yj. The second-order
drift correction is at most C/N, because each row of S_N has bounded squared
sum. Bounded-jump exponential martingales then give (2). This explicitly
retains state coupling between different rows.

## 3. Executed delayed force

Use the finite-cell elastic supplier in the companion note, with N carriers
per row and common physical period p. Hold one force over L_N complete cells.
Let d_N=p L_N, delta_N=d_N/N^2, and t_m=m delta_N. At the start of block m,
apply the command based on the held record at t_(m-1):

\[
 F_{y,m}=\operatorname{clip}_{[-a_N,a_N]}
 \left[-{K_N\over N}\{e_{y,m-1}+\eta_{y,m-1}\}\right],
 \qquad e_y=A_y/N^2-q_y.                                  \tag{3}
\]

Set F_0=0. Here eta includes actual synchronized sensing, evaluation and
actuation-command error in normalized displacement units. Assume
max_{y,m}|eta|<=C/K_N outside a whole-protocol event of probability p_N,
where N^(-2)log p_N->-infinity. Commands remain capped even on that event.
They are selected before future thermal sources. Old records must respect
these actual conditional hypotheses if a conditional assertion is made.

One concrete asymptotic choice is

\[
 K_N=\log\log(N+e^e),\quad a_N=N^{-1/4},\quad
 d_N=N\,\operatorname{polylog}N.                           \tag{4}
\]

More generally require K_N->infinity, K_N=o(sqrt N),
K_N delta_N->0, N a_N delta_N->0, and the cap-tail conditions proved below.
The controller knows no mu_y or current corrector. For large N the actual
loop gain alpha_y=(mu_y/p)K_N delta_N lies in (0,1/8).

## 4. Exact discrete reduction, with physical memory retained

Define the analytic normalized corrector
c_{y,m}=k_y^T(z_{y,mL}-z_{y,0})/N^2 and e'_{y,m}=e_{y,m}+c_{y,m}.
Summing the actual cell identity, before the first cap activation or sensing
failure, gives

\[
 e'_{y,m+1}=e'_{y,m}-\alpha_y e'_{y,m-1}
             -\beta_{y,m}+\xi_{y,m}
             +\alpha_y(c_{y,m-1}-\eta_{y,m-1}).              \tag{5}
\]

Here |beta_{y,m}|<=C delta_N is target predictable drift. xi contains the
target martingale increment and the actual fresh collective thermal sum;
for unit v its conditional variance proxy is C delta_N/N. The thermal
part is Gaussian. The native jump restriction in (2) remains. Parameters
alpha_y are fixed unknown row values, so the response kernels are
deterministic for the proof, although not known by the controller.

For 0<alpha<=1/8 the fundamental response of x_(m+1)=x_m-alpha x_(m-1)+u_m
is

\[
 g_j={r_+^{j+1}-r_-^{j+1}\over r_+-r_-},\qquad
 r_\pm=(1\pm\sqrt{1-4\alpha})/2.
 \tag{6}
\]

It is nonnegative, g_j<=C exp(-c alpha j), sum g_j<=C/alpha,
and sum g_j^2<=C/alpha, uniformly over all rows. These bounds follow directly
from r_-<=2alpha, r_+<=1-alpha and r_+-r_->=1/sqrt2.

Uniform stability of the physical two-coordinate cell and the hard force
cap give, on all adapted capped histories,

\[
 z_{y,k}=G_{y,k}+N\sum_{i<k}M_y^{k-1-i}d_yF_{y,i},
 \quad |z-G|\le C N a_N,
 \quad G_{y,k}\sim\mathcal N(0,NI).                        \tag{7}
\]

The reference G may be correlated with feedback; only its Gaussian marginal
and the pathwise bound are used. A union over rows and cells proves

\[
 P\{\max_{y,m}|c_{y,m}|>C/K_N\}
 \le\operatorname{poly}(N)\exp[-cN^3/K_N^2]                \tag{8}
\]

for (4), and the same estimate covers within-cell endpoints. Its exponent
is already super-volume. This corrector is never measured or subtracted
from the physical current or work.

## 5. The missing joint volume argument

Iterate (5). Drift, observation envelope and corrector envelope contribute
at most C/K_N in every coordinate. At a fixed block end, the remaining
noise vector U_m is a convolution with the diagonal kernels (6). For every
unit Euclidean v, (2) and sum g_j^2 delta_N<=C/K_N give

\[
 P\{|v\cdot U_m|>x\}
 \le2\exp\left[-c\min\{N K_N x^2,\ N^2x\}\right].         \tag{9}
\]

Different rows' drifts and jump intensities may remain fully dependent.
The proof uses the conditional vector bracket, not independent row laws.
Apply (9) to a 1/2-net of the Euclidean unit sphere, of size at most 5^N.
If ||U_m||_2>epsilon sqrt N, some net direction exceeds epsilon sqrt N/2.
Therefore

\[
 P\{\|U_m\|_2>\epsilon\sqrt N\}
 \le2\,5^N\exp[-c\min\{\epsilon^2N^2K_N,
                                    \epsilon N^{5/2}\}].   \tag{10}
\]

There are polynomially many blocks. The entropy of the directional net is
only O(N), whereas the error exponent is N^2 K_N. This is precisely why a
joint weak spatial error can be controlled at volume speed even though
the corresponding one-row exponent N K_N is insufficient.

### Stopping and the force cap

Use predictable stopping at the first bad readout or first command that
would exceed the cap. The martingale bounds apply to stopped increments;
we do not condition the noise on future success. Formula (5) applies until
that time. Equation (8) is separately valid for the globally capped physical
system, so its good envelope can be used as a deterministic error bound
without altering the martingale law.

At a first cap activation some |e+eta| exceeds N a_N/K_N. Apply the scalar
version of (9), and (8), to this first occurrence. For a_N=N^(-1/4),

\[
 P\{\hbox{cap activates before the horizon}\}
 \le p_N+\operatorname{poly}(N)
 \left(e^{-cN^3/K_N^2}+e^{-cN^{5/2}/K_N}\right).             \tag{11}
\]

The small bounded source drift and initial zero block change only the
C/K_N envelope. Both exponents in (11) dominate N^2. Thus using an unbounded
ideal linear force is unnecessary. A fixed total-loop force range, by
contrast, does not supply this superexponential conclusion.

### Between held timestamps

Over a block, bounded force changes normalized corrected current by at most
C N a_N delta_N=o(1) per row. Source drift contributes C delta_N. Use (2)
and a sphere net for the vector martingale maximum over that block; its
variance proxy is C delta_N/N, so a fixed spatial L2 error has exponent at
least c min{epsilon^2 N^2/delta_N,epsilon N^(5/2)}. Both dominate N^2.
Finite-cell endpoint corrections are covered by (8). Union over the
polynomially many blocks proves the full-time result

\[
 \boxed{\limsup_N N^{-2}\log P\left\{
 \sup_{t\le T}\Big[N^{-1}\sum_y|A_y(N^2t)/N^2-q_y(t)|^2\Big]^{1/2}
 >\epsilon\right\}=-\infty.}                              \tag{12}
\]

This is the required joint volume-scale argument. It proves neither a CLT
nor preservation of ordinary output-current fluctuations.

## 6. Physical path map and receiving LDP

Let h(y,t)=integral_0^1 W_x(x,y,t) dx. Define

\[
 \mathcal T(\rho,W)=
 \left(\rho+1,\ W+\{\psi(y,t,(S h)(y,t))-h(y,t)\}e_x\right).
                                                               \tag{13}
\]

The auxiliary current Y is also retained as the displayed added field.
The native macroscopic current is W_out-Y; no fine apparatus logs are
claimed reconstructed by this subtraction. Equations (12) and the elastic
density/current theorem establish exponential equivalence at speed N^2
between the actual composite paths and (13), in the compatible weak density
and negative-Sobolev current path geometry.

The smoothing is continuous from that current distribution geometry into
smooth vertical functions; multiplication/composition by the specified psi
is then continuous on compact sets. The raw -h term is linear and continuous.
Discrete quadrature and Fourier approximation are uniformly vanishing on
the native exponentially tight sets. Alternatively, the bounded activity
gives a polynomial total-count range with super-volume failure probability,
and exponential Fourier accuracy controls it directly. Thus the discrete
program has the stated continuous limiting map.

If the actual native paths have a good speed-N^2 LDP with rate I, the
composite paths have rate

\[
 I_{out}(\rho+1,W^{out})
 =\inf\{I(\rho,W):\mathcal T(\rho,W)=(\rho+1,W^{out})\}.      \tag{14}
\]

The native source bounds alone do not prove an LDP. Homogeneous two-dimensional
exclusion with its warranted initial law is a concrete receiving example;
the established empirical-current theorem is Bertini et al.,
https://arxiv.org/pdf/math/0512394. A frozen unknown kinetic class can be
handled conditionally; an unexplained mixture does not inherit one fixed
class's action.

Minimizing (14) over output current yields exactly the native density-path
rate at rho, with the physical uniform offset retained. This preserves
every macroscopic native density history, including rare ones. It is a
pushforward achieved by actual added motion, not restriction of the native
current action to a constraint surface.

## 7. Consequence and limits

The output row-current field is psi(y,t,S h). Choosing psi=v(y)t writes
a prescribed spatial shear circulation, whose vorticity is -v'(y), without
changing the native density history. Choosing nonlinear psi gives a causal
spatial law responding to a measured, smoothed native current history.
These are actual charge currents of the complete composite. The native
branch flow itself is unchanged, and there is no claim to advect native
particles, transfer work passively, or realize arbitrary two-dimensional
solenoidal fields with this row architecture.

The ordinary uncalibrated integral governor is a direct alternative using
the same port. Current feedback and finite-delay virtual potentials have
direct predecessors: Brandes, https://arxiv.org/pdf/1503.03672, and
Jun--Bechhoefer, https://arxiv.org/pdf/1212.4588. The scientific addition
claimed here is the physical composition and joint spatial theorem, not
a new basic feedback algorithm or a historical-priority certificate.
