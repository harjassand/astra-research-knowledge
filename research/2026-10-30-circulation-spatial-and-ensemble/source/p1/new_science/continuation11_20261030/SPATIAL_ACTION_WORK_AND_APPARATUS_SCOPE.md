# Spatial constitutive law, true carrier work and the complete cost boundary

30 October 2026. Root's consequence and work derivation for the elastic
spatial program. Read the carrier theorem with its binding corrections and
the joint tracking theorem. Actual sensing and apparatus energy remain
explicit; the result does not claim a total-resource speedup.

## 1. The larger physical principle

The full macroscopic density-path law of an interacting native material does
not fix its composite spatial transport law when an actively driven,
relatively stiff physical carrier layer is allowed. This remains true with
order-volume **carrier force work** under sustained load. The new resource
is an extensive, low-compressibility translation layer, not a dilute
population with increasing work per transported charge-distance.

The complete composite density is rho_native+1. Every added charge is
counted, as is every displacement. Native density/current histories are
unchanged by isolation at the microscopic level. At volume speed N² the
added density becomes a deterministic uniform background, while its actual
horizontal flow becomes a prescribed function of a measured native field.

This is a theoretical operation on spatial constitutive laws. It does not
advect native particles, passively transfer work, or claim all divergence-free
two-dimensional fields. The row geometry supplies shear fields. A conveyor
with an ordinary governor uses the same principle; its name does not prove
the complete fluctuation, sensing or resource statement.

## 2. Nonlinear native action and a concrete spatial contraction

For homogeneous two-dimensional exclusion with fixed positive directional
rates D_x,D_y and actual weak force fields F_x/N,F_y/N, use its warranted
initial law. In the rate convention of right/left rates D_alpha exp(±F_alpha/2N),
the native action is

\[
 I(\rho,j)=I_{init}+\frac14\int dt\,dx\,dy\sum_{\alpha=x,y}
 \frac{[j_\alpha+D_\alpha\partial_\alpha\rho
                 -D_\alpha\chi(\rho)F_\alpha]^2}
      {D_\alpha\chi(\rho)},\qquad \chi(\rho)=\rho(1-\rho).
                                                               \tag{1}
\]

Continuity and the actual initial conditions are required. The literal
formula assumes density bounded away from zero and one; use its lower
semicontinuous extension otherwise. The unforced empirical-current LDP is
established by Bertini et al., https://arxiv.org/pdf/math/0512394; a smooth
weak force enters by the actual jump likelihood tilt. This formula is a
calculation in a known exclusion model, not a derivation of that model from
the nonlinear mechanical spring law.

Choose the implemented target psi(y,t,z)=v(y)t, including v=0. The output
row-integrated horizontal current must equal v(y). Native preimages are
j_x+u(y,t), j_y, with u unrestricted. Put

\[
 a_\alpha=j_\alpha+D_\alpha\partial_\alpha\rho
                 -D_\alpha\chi F_\alpha,\quad
 r(y,t)=\int_0^1{dx\over D_x\chi},\quad
 \ell(y,t)=\int_0^1{a_x\over D_x\chi}\,dx.
\]

Minimizing the native quadratic in u gives u_*=-ell/r and

\[
 \boxed{I_{out}=I_{init}+\frac14\int dt\,dy\left[
   \int dx\left({a_x^2\over D_x\chi}+{a_y^2\over D_y\chi}\right)
                  -{\ell^2\over r}\right].}                \tag{2}
\]

It is infinite if the output row-mean or continuity/initial conditions fail.
The measured density argument is rho+1; chi in (1)--(2) remains the native
exclusion mobility at rho. Replacing it by chi(rho+1) would be physically wrong.

A passive restriction of the *native* current to the same row means lacks
the subtraction in (2), and can alter the density-path cost. The active
operation preserves the entire native density-path rate after minimizing
over output current. Arbitrary nonlinear psi uses the full preimage
contraction proved in the companion note, not this special algebraic formula.

## 3. Second moments of the executed unknown-mobility governor

Use the actual delayed force in the tracking theorem. Its causal response
kernels have sum O((K delta)^(-1)) and squared sum O((K delta)^(-1)).
Bounded target drift and readout error C/K therefore contribute O(K^(-2))
to E e_y². The vector martingale covariance contributes O((N K)^(-1))
per row. The analytic mechanical corrector contributes at most
C[a_N²/N²+log(N)/N³]. Thus, off the stopped failure comparison and uniformly
at control times,

\[
 E e_{y,m}^2\le {C\over K_N^2}+{C\over N K_N}
           +C\left({a_N^2\over N^2}+{\log N\over N^3}\right)
           +\varepsilon_N,                               \tag{3}
\]

where epsilon_N is superpolynomially small. To obtain the unconditional
bound, use the globally capped process, the super-volume probability of
first cap/readout failure, and polynomial second/fourth moments of native
counts and the stable mechanical state. This avoids conditioning martingale
increments on future successful tracking. The same argument covers force
errors in the readout envelope; arbitrary unbounded force faults do not.

From F=-(K/N)(e+eta), with the actual cap,

\[
 E F_{y,m}^2\le C/N^2+C K_N/N^3+o(N^{-2}).                 \tag{4}
\]

The small cap-failure contribution is bounded by a_N² times its probability.
The controller needs a positive response interval but no estimate of the
unknown mu_y. Neither gain calibration nor a learned native generator is
hidden in (3)--(4).

## 4. Exact physical work with retained thermal memory

Let there be B complete held blocks of L cells and physical horizon B L p.
Use z for the actual aggregate mechanical state, not target q. For row y
write Q_y=M_y^L, v_y=sum_(j=0)^(L-1) M_y^j d_y and
w_y=k_y^T(I-Q_y). The preserved partial-refresh work identity, applicable
because commands are one full block old and F_0=0, is

\[
\begin{split}
 E W_y={}&N(\mu_yL-k_y^Tv_y)\sum_m EF_{y,m}^2\\
 &+Nw_yv_y\sum_m E(F_{y,m}F_{y,m-1})
 +\sum_{m\ge1}E[F_{y,m}w_yQ_y z_{y,(m-1)L}].
\end{split}                                               \tag{5}
\]

The last old-state correlation is not zero and has no assigned sign.
Uniform cell stability bounds it by poly(N)exp(-cL), even after summing
over N rows. Consequently, with S_y=sum_m E F_{y,m}²,

\[
 E W_y=N\mu_y L S_y+O(N S_y)+O(\operatorname{poly}(N)e^{-cL}).
                                                               \tag{6}
\]

Since B=O(N²/L), (4) yields

\[
 \boxed{E\sum_y W_y=O(N^2+N K_N)=O(N^2).}                  \tag{7}
\]

This is true signed force work on the charged particles. The asymptotic
noise-control term is at most O(N K_N); it is lower order when K_N=o(N).
Exact finite-block nonnegativity has not been asserted. A short terminal
interval can have zero applied force; its real motion remains counted and
is negligible by the within-block estimates.

For a sustained mean auxiliary flow define v_y^A=E A_y/N². The same exact
current identity, Cauchy--Schwarz in time and (6) imply

\[
 E\sum_yW_y\ge cN\sum_y (v_y^A)^2-o(N²).                  \tag{8}
\]

Thus a nonzero mean square flow over a positive fraction of rows costs
Omega(N²) at this force port; (7) attains its order. The dilute architecture
with R_N carriers per row instead pays order N³/R_N for the same task.
The new layer contains N² carriers rather than N R_N and has increased
stiffness. This is a real resource trade, not a free reduction in dissipation.

Equation (8) is an unconditional or correctly conditional sustained-mean
statement. It is not applied after selecting a rare future current history.
Unforced rare-event action, typical fluctuation laws, and active loaded
experiments remain distinct. No CLT is inferred from (2), and this always-on
spatial program does not inherit round10's rare-arming TV comparison.

## 5. Sensing, communication, actuation and reliability ledger

The information required is the **total signed displacement in each row**,
for native and auxiliary charges, at common held timestamps. One cut counter
does not supply this without its polarization term. Summing unsynchronized
latest readings across a long row would invalidate the drift argument.

One declared architecture has local held counters at the N² native sites
and local auxiliary pickups, rowwise aggregation, followed by vertical
aggregation/broadcast of O(log N) Fourier coefficients. Pipelined local
addition and finite-precision evaluation take N polylog(N) physical latency.
That latency is already in d_N. Counters of polynomial range need O(log N)
bits. Total native jump opportunities are O(N^4) on the N² horizon; all
event sensing is counted even if analog integration avoids one digital
operation per event. Local tree arithmetic/broadcast adds polynomially many
bit operations and O(N² polylog N) logical storage. It is not free because
the final program has only a few displayed formulas.

A finite-response pickup can be represented by the actual, calibrated law
tau dr=-r ds+dQ and dC=r ds, so C=Q-tau r. Its endpoint term, timing skew,
measurement noise, quantization and evaluator error must together supply
the C N²/K raw count envelope. The preserved local-counter construction
describes such a port; its noninvasiveness and noise bounds are physical
premises, not inferred from a low-frequency spectrum. The present proof
requires failure at **volume speed N²**, stronger than the earlier speed-N
contract. Fixed calibration confidence does not meet it.

An acquired supplier therefore needs actual conditional noise tails, paid
calibration and a whole-protocol logical failure probability p_N satisfying
N^(-2)log p_N->-infinity. No end-to-end logical hardware with that guarantee
has been built in this round. A theorem conditional on that readout contract
is justified; a completed experimental capability or reliable instrument is
not. Ordinary controllers receive the same contract in the comparison.

The drive is a supplied uniform tangential force within each row, switched
only on the declared held blocks and capped at N^(-1/4). Distributed local
force elements or a characterized nonconservative field must supply it.
Its maximum loop affinity is N^(3/4), even though its per-carrier force
vanishes. A fixed total loop voltage is not this range. Command distribution,
force uniformity, field energy and switching losses must be measured or
bounded by the actual supplier. The mechanical links have the additional
worst-case force and response ranges in `ELASTIC_LAYER_CORRECTIONS.md`.

For the finite-cell implementation there are O(N^4) fresh thermal
coordinates and retirements over the horizon, each at a finite rotation
frequency. Freshness, source preparation and capacity cannot be inferred
from the unchanged relative Gibbs law. Positions have N² initial placements
at kappa^(-1/2) precision; velocity/neutral preparations are also charged.

The complete budget is therefore

\[
 W_{total}=W_{carrier\ drive}+W_{position/thermal\ preparation}
 +W_{sensing}+W_{clock}+W_{logic/communication}
 +W_{switch/field}+W_{reliability}+W_{retirement},             \tag{9}
\]

with any energy recovery and double counting resolved by a real apparatus
energy ledger. Equation (7) controls only the first term. No bound O(N²)
for (9), practical energy advantage, or free always-running apparatus is
claimed. This limitation changes the scientific conclusion: the completed
gain is a physical-model path-law principle and a carrier-work tradeoff,
not an end-to-end efficient machine.

## 6. Same-resource alternatives and what is new

The ordinary governor provided by the complementary role uses the same
unknown-positive-response port without calibration and ties (7). Jun and
Bechhoefer's actual feedback traps explicitly retain measurement delay,
exposure and update time: https://arxiv.org/pdf/1212.4588. Brandes's channel
feedback is also a direct predecessor: https://arxiv.org/pdf/1503.03672.

The other complementary construction drives one tracer through a
single-file native material. It causes collective motion and a nonflat
native density profile with order-volume force work. Passive slow gates
change a native diffusion law. A local passive gear or tight-coupling cell
transfers work to a load without sensing or global communication. These
are stronger for those tasks and prevented selecting transport or current
locking alone as the advance. They give up preservation of independent
native bulk histories. Their exact files and primary credit are retained.

The candidate addition is the conjunction of local finite-duration carrier
motion, a locally prepared stiff density layer, joint volume-scale tracking,
the physically executed smoothing/nonlinear map, preserved interacting bulk
path laws and the extensive carrier-work bound. No historical priority for
this conjunction has been established. Its possible reach is constitutive
design and limits of inference from bulk fluctuations; a useful apparatus
still needs the full budget and actual measurement/reliability supplier.
