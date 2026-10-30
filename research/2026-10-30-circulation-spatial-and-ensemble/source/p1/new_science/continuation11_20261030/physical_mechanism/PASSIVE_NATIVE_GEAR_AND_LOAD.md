# Passive coupling of the original material ports

30 October 2026. Constructive ordinary comparison by the existing physical
mechanism role. This is not a claim to invent Brownian gears or tight coupling.
It answers whether useful current locking and load delivery require isolated
auxiliary counterflow. They do not when an actual interaction between the
original carriers is supplied. It does **not** preserve their independent bulk
density histories.

The governing Astra mission was reread from the preserved exact source
`continuation_20261029/sources/MISSION_EXACT_SOURCE.json`. The completed round-10
result and `MAIN_THEOREM_CLARIFICATIONS.md` were read before this construction.
No earlier result, code or review is changed.

## 1. Actual operation and its established predecessor

Two physical rotors have unwrapped angular displacements $x_1,x_2\in\mathbb R$.
Their actual local conservative interaction is

\[
 V_\kappa(x_1-x_2)=\kappa[1-\cos(x_1-x_2)].                 \tag{1}
\]

Forces $f_1,f_2$ are actual torques, in units with $k_BT=1$. Work at port $a$
is $f_a\Delta x_a$. Rotation is not a reported linear combination of motions.
The interaction exerts equal and opposite torques; it has no runtime clock,
sensor, estimator or feedback controller.

For fixed unknown mobilities $d_a\in[d_-,d_+]$, the specified overdamped model is

\[
 dx_1=d_1[f_1-V_\kappa'(r)]dt+\sqrt{2d_1}\,dW_1,
 \qquad
 dx_2=d_2[f_2+V_\kappa'(r)]dt+\sqrt{2d_2}\,dW_2,
 \quad r=x_1-x_2.                                         \tag{2}
\]

The bath inputs are independent. The mobilities may be arbitrary frozen hidden
parameters. They are not inferred by the operation. Arbitrary time-dependent
hidden mobilities or an unknown additional substrate potential are not covered
by the exact reduction below.

This is a direct ordinary predecessor class. Lathouwers, Lucero and Sivak,
*Nonequilibrium Energy Transduction in Stochastic Strongly Coupled Rotary
Motors*, J. Phys. Chem. Lett. **11**, 5273–5278 (2020),
[DOI](https://doi.org/10.1021/acs.jpclett.0c01055),
[full primary paper and supporting derivations](https://arxiv.org/pdf/2004.01837),
derive the equal-friction sum/difference reduction in supporting Eqs. (18)–(26)
and analyze real input/output work and slippage. Their barrier-bearing examples
also show why taking coupling to infinity need not maximize power. The present
comparison credits that mechanism; its added derivation is a uniform finite
barrier, whole-current-path scaling argument with unknown bounded mobilities.
No priority claim is made for that scaling argument either.

## 2. Exact separation, without estimating the mobilities

Put

\[
 a=d_1+d_2,\qquad m={d_1d_2\over a},\qquad
 C={d_2x_1+d_1x_2\over a},\qquad
 f={d_1f_1-d_2f_2\over a}.
\]

Then, exactly,

\[
 dC=m(f_1+f_2)dt+\sqrt{2m}\,dW_C,
 \qquad
 dr=a[f-V_\kappa'(r)]dt+\sqrt{2a}\,dW_r.                  \tag{3}
\]

The two Brownian noises are independent: their covariance is

\[
 {d_2\over a}(2d_1)-{d_1\over a}(2d_2)=0.
\]

The reconstruction is

\[
 x_1=C+{d_1\over a}r,\qquad x_2=C-{d_2\over a}r.         \tag{4}
\]

$C$ is an analytical coordinate. The device does not calculate it, and no
unknown-weight sensing port is used. Its mobility satisfies

\[
 d_-/2\le m\le d_+/2.                                    \tag{5}
\]

Thus raising the relative barrier does not reduce common-coordinate mobility
in this deliberately barrier-free native-rotor model. This conclusion fails
if an added substrate potential acts on the common coordinate. That failure
is present in the primary coupled-rotor literature, not an omitted technicality.

## 3. The relative cell, including its exact corrector

Let $\ell=2\pi$, $Z_\pm=\int_0^\ell e^{\pm V_\kappa(x)}dx$, and

\[
 \delta_\kappa={\ell^2\over Z_+Z_-}=I_0(\kappa)^{-2}.
                                                               \tag{6}
\]

The equilibrium relative density is $\rho_0=e^{-V}/Z_-$. The exact zero-force
winding diffusivity is $a\delta_\kappa$. This is the classical Lifson–Jackson
cell formula, not new acquired information. See Lifson and Jackson,
J. Chem. Phys. **36**, 2410–2414 (1962),
[DOI](https://doi.org/10.1063/1.1732899), and the actually read primary derivation
of its relation to the hopping formula in Kalnin and Berezhkovskii,
J. Chem. Phys. **139**, 196101 (2013),
[full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4108624/).

For a nonzero constant $f$, define

\[
 D_f=\int_0^\ell e^{V(x)-fx}
              \int_x^{x+\ell}e^{-V(y)+fy}\,dy\,dx,
 \qquad
 v_f={a\ell(e^{f\ell}-1)\over D_f}.                       \tag{7}
\]

All formulas at $f=0$ mean their continuous limits. Set

\[
 q_f(x)={\ell\over D_f}
 e^{V(x)-fx}\int_x^{x+\ell}e^{-V(y)+fy}\,dy.              \tag{8}
\]

Then $q_f>0$, $\int_0^\ell q_f=\ell$, and direct differentiation gives

\[
 q_f'+(f-V')q_f=v_f/a.                                   \tag{9}
\]

Choose the periodic primitive $\chi_f'=q_f-1$. Its oscillation is at most
$\ell$: the integral of the positive $q_f$ over every subinterval is at most
$\ell$, and its integral over a whole period is exactly $\ell$. Consequently

\[
 r_t-r_0+\chi_f(r_t)-\chi_f(r_0)=v_ft+M_t,
 \quad
 dM_t=\sqrt{2a}\,q_f(r_t)dW_t.                            \tag{10}
\]

The corrector is uniformly bounded even when the barrier grows. It is not a
physical memory or a replacement current; actual work continues to use $r_t-r_0$.

Let $\rho_f$ be the forced circle stationary density. The elementary integral
formula for this density and (7)–(8) imply, with numerical constants depending
only on the period,

\[
 e^{-C|f|}\rho_0\le\rho_f\le e^{C|f|}\rho_0,
 \qquad e^{-C|f|}q_0\le q_f\le e^{C|f|}q_0,               \tag{11}
\]

\[
 |v_f|\le a|f|\delta_\kappa e^{C|f|},\qquad
 \int q_f^2\rho_f\le e^{C|f|}\delta_\kappa,
 \qquad \|q_f^2\|_\infty\le C e^{C|f|}(1+\kappa).         \tag{12}
\]

For example, the ratio bound in the first part of (11) follows by writing the
stationary density as a normalized

\[
 e^{-V(x)}\int_0^\ell e^{V(x+y)-fy}\,dy.
\]

Every factor $e^{-fy}$ lies between $e^{-|f|\ell}$ and
$e^{|f|\ell}$. The $q_f$ bound is the analogous normalized integral with
$e^{fy}$. At zero force,

\[
 q_0={\ell e^V\over Z_+},\qquad
 \int q_0^2\rho_0=\delta_\kappa,\qquad
 \sup q_0={e^\kappa\over I_0(\kappa)}\le C\sqrt{1+\kappa}.
\]

No small-noise asymptotics are needed for these inequalities.

## 4. A complete whole-path locking theorem

Consider $N$ independent physical pairs. Pair $i$ has unknown frozen
$d_{a,i}\in[d_-,d_+]$, the same supplied barrier $\kappa_N$, and actual
torques $f_{a,i}=F_a/N$. Fix bounded $F_1,F_2$ and $T<\infty$. Initially the
relative phases have product density $\rho_0$, independently of future bath
increments, conditional on all frozen device parameters and the retained
pre-deployment record. This is an actual initialization contract, not a
consequence of retaining fewer bits.

Define the two actual aggregate currents

\[
 J_a^N(t)={1\over N^2}\sum_{i=1}^N
             [x_{a,i}(N^2t)-x_{a,i}(0)],\quad 0\le t\le T.
                                                               \tag{13}
\]

Suppose

\[
 \kappa_N\longrightarrow\infty,
 \qquad \kappa_N=o(\log N).                               \tag{14}
\]

Let $G_N=N^{-2}\sum_i\Delta C_i$. Then, uniformly over all the declared hidden
mobilities, for every $\varepsilon>0$,

\[
 \limsup_{N\to\infty}{1\over N}
 \log\Pr\!\left[\max_{a=1,2}\sup_{t\le T}
                   |J_a^N(t)-G_N(t)|>\varepsilon\right]
 =-\infty.                                                \tag{15}
\]

This is a whole physical-current path statement. It is not a bound on a
reweighted estimator or on just the final mean.

### Proof of the exponentially small residual

In $L^2(\rho_f)$, the real part of the relative generator form is exactly

\[
 \operatorname{Re}\langle u,L_fu\rangle
   =-a\int |u'|^2\rho_f.
\]

The stationary circulation contributes only an antisymmetric term. Comparison
with the circle Poincare inequality, (11), and $\operatorname{osc}V=2\kappa$
gives a symmetric-part gap

\[
 g_\kappa\ge c e^{-2\kappa-C|f|}.                         \tag{16}
\]

We use an elementary Feynman–Kac estimate. If a stationary Markov generator has
this form gap $g$, and $0\le h\le H$, with mean $\bar h$, then for
$sH\le g/4$,

\[
 \sup\operatorname{Re}\operatorname{spec}(L+sh)
 \le s\bar h+C s^2H^2/g.                                 \tag{17}
\]

Indeed write a unit vector as its mean plus a centered vector. The centered
quadratic part costs at least $g\|u-\bar u\|^2$, the cross term is bounded by
$2sH\|u-\bar u\|$, and completing the square proves (17). The same numerical
range bound controls the semigroup norm even if $L$ is not self-adjoint.

For an initial density $\rho_0$, the $L^2(\rho_f)$ prefactor is at most
$e^{C|f|}$. For a martingale in (10), Cauchy–Schwarz applied to the exponential
martingale at parameter $2\theta$ gives

\[
 E e^{\theta M_t}
 \le\left[E\exp\!\left(4a\theta^2\int_0^tq_f^2(r_s)ds\right)\right]^{1/2}.
                                                               \tag{18}
\]

This step is valid because $q_f$ is bounded for each finite $N$, so the
exponential martingale is integrable. Apply (17) to $h=q_f^2$, use (12), and
multiply the independent-pair bounds. For any fixed weights $|w_i|\le1$,
putting $t=N^2T$ and $\theta=b/N$ yields

\[
 \log E\exp\!\left({b\over N}\sum_iw_i M_i(N^2T)\right)
 \le C+C_T b^2N\delta_{\kappa_N}
       +C_T b^4{(1+\kappa_N)^2e^{2\kappa_N}\over N}.       \tag{19}
\]

The validity condition in (17) follows from (14), for each fixed $b$.
The initial-density prefactors contribute $\sum_i O(|f_i|)=O(1)$.

Doob's inequality for the positive submartingales
$\exp[\pm(b/N)\sum_iw_iM_i(t)]$ gives the same terminal bound for the
corresponding running maximum. The deterministic drift in (10), divided by
$N^2$, is at most $C_T\delta_{\kappa_N}$, and the sum of corrector endpoints
is bounded by (C N). Therefore the logarithmic probability divided by $N$
is at most $-b\varepsilon+o(1)$. First take $N\to\infty$, then $b\to\infty$.
Use the weights $d_{1,i}/(d_{1,i}+d_{2,i})$ and
$-d_{2,i}/(d_{1,i}+d_{2,i})$ in (4). This proves (15).

### Exact common path and its action

Let $\bar m_N=N^{-1}\sum_i d_{1,i}d_{2,i}/(d_{1,i}+d_{2,i})\to\bar m>0$.
The analytical common current has exactly the law

\[
 G_N(t)=\bar m_N(F_1+F_2)t+\sqrt{2\bar m_N/N}\,B_t.        \tag{20}
\]

The full joint current-path rate at speed $N$, in the uniform path topology,
is therefore

\[
 I(j_1,j_2)=
 \begin{cases}
 \displaystyle {1\over4\bar m}\int_0^T
       [\dot j-\bar m(F_1+F_2)]^2dt,
       &j_1=j_2=j,\ j(0)=0,\ j\text{ absolutely continuous},\\
 +\infty,&\text{otherwise}.
 \end{cases}                                               \tag{21}
\]

This follows from the Gaussian path rate for (20) and (15), rather than from
integrating a terminal approximation. It includes rare counter-rotating
histories: their cost diverges on this scale. It does not alone identify every
finer fluctuation law; no such inference is used.

## 5. Real input work, useful load and initialization

Take $F_1>0$, $-F_1<F_2<0$. The output rotor works against its applied torque.
The exact finite-time first moments from (10) have endpoint errors at most a
constant per pair. Equations (7), (12) and (4) then give

\[
 {E W_{\rm in}\over N}\to
       F_1\bar m(F_1+F_2)T>0,
 \qquad
 {E W_{\rm out}\over N}\to
       -F_2\bar m(F_1+F_2)T>0.                            \tag{22}
\]

Here $W_{\rm in}=(F_1/N)\sum\Delta x_{1,i}$ and
$W_{\rm out}=-(F_2/N)\sum\Delta x_{2,i}$; the signs refer to the actual
external reservoirs. Operating efficiency tends to $-F_2/F_1<1$.
The sum of port work, less the change of the actual interaction energy, is
heat. There is no additional actively driven counterflow source.

For fixed finite loads, (7)–(12) also give a quantitative finite-barrier engine.
For example, with $f_1>0>f_2$, $f_1+f_2>0$,

\[
 v_2=m(f_1+f_2)-{d_2\over a}v_f,
 \qquad
 0<v_f\le(d_1f_1-d_2f_2)\delta_\kappa e^{C|f|}.           \tag{23}
\]

Choosing the known barrier so that the last upper bound is less than
$d_1(f_1+f_2)$ guarantees $v_2>0$, uniformly over the specified mobility
bounds. A uniform stricter factor gives a positive power lower bound. Unknown
mobilities alter power but not the limiting gear ratio or its thermodynamic
stall. At finite barrier there is genuine slip and finite-barrier stall need
not occur at exactly $f_1+f_2=0$.

Preparing the equilibrium coupling is not free. From uncoupled uniform phases,
the equilibrium free-energy change per pair is

\[
 \Delta\mathcal F_\kappa
   =-\log\left({Z_-\over2\pi}\right)
   =\kappa-\log I_0(\kappa)
   ={1\over2}\log(2\pi\kappa)+o(1).                       \tag{24}
\]

This is a quasistatic minimum, not an asserted finite-time protocol. A literal
sudden switch of (1) on from uniform phases has expected work $\kappa$ per
pair and is bounded by $2\kappa$ on every pair. It must be followed by paid
thermal relaxation if the theorem's conditional Gibbs initialization is
invoked. An actual warranted initializer can instead supply that law at its
own charged cost. The coupling energy range is $2N\kappa_N$, its equilibrium
mean is $O(N)$, and its fabrication/control energy is not inferred from
either number.

The smooth supplier's maximum interaction torque is $\kappa_N$, and its local
overdamped restoring rate grows like $a\kappa_N$. Thus (14) pays increasing
force range and response bandwidth, however slowly. A fixed-mass microscopic
apparatus cannot be declared overdamped uniformly in this limit without a
compatible inertia/bath separation. At fixed finite barrier it remains a
finite-response, finite-error ordinary engine. The separate finite-rate
single-file construction below removes this growing-barrier requirement by
using actual exclusion geometry instead; that is a different material port.

## 6. The honest comparison with round 10 and with bulk preservation

For a sustained order-one aggregate counterflow for time $N^2T$, the round-10
isolated $R_N\ll N$ carrier port paid order $N^2/R_N$ drive work. This native
gear uses order $N$ original pairs and order $N$ actual interactions. Its
weak-load operating work is order $N$. It transfers input work into a useful
opposing load instead of adding a compensating branch current.

Even a sudden preparation cost $O(N\kappa_N)$ can be smaller than
$N^2/R_N$ by selecting $\kappa_N\to\infty$ so slowly that
$\kappa_N=o(N/R_N)$, in addition to (14). This is an asymptotic resource
comparison under different **material access**, not an apparatus-speedup
claim. The native coupling ports, the number of pairs, fabrication, phase
preparation, bath and response requirements must all be counted.

It does not solve the root's stronger selected task: preserve *all native bulk
density histories* while changing actual transport. Already (3) changes the
relative native dynamics. At strong coupling, the mobility matrix of the two
unwrapped ports tends to

\[
 m\begin{pmatrix}1&1\\1&1\end{pmatrix},
\]

whereas the uncoupled matrix is $\operatorname{diag}(d_1,d_2)$. A force on the
first material now moves the second material. A process preserving the full
separate native path laws could not have this response. Applying such bonds
along two extended conduits also constrains their relative density profiles.
It cannot silently be reduced to a harmonic-only operation.

The resulting selection boundary is concrete. Direct reciprocal material
coupling already supplies efficient load transfer and robust current locking.
Preservation of arbitrary native bulk histories is an additional operation
that this ordinary gear does not supply.

## 7. Record and hidden-state scope

Every torque, phase trajectory, slip, bath exchange and initialization event
remains real. No apparatus key is discarded to manufacture independence.
The stated conditional initialization allows a retained record correlated with
the frozen mobility parameters, provided the conditional relative phase law
and independent future bath contract are actually met. It does not allow
postselection on an entire exposed future bath trajectory.

The large-deviation statement is conditional on any fixed allowed mobility
sequence. A mixture over classes is also uniformly locked, but its common
current rate is generally a mixture/infimum of class rates; it is not obtained
by silently substituting an average mobility. Infinite-dimensional unknown
kinetics with changing memory is outside the exact common-coordinate proof.

An unknown native corrugation, hydrodynamic state-dependent mobility, bypass
path or a faulty physical coupling can reintroduce slow response or slip. None
is repaired merely by equilibrium weights. These are the precise limitations
behind retaining this unit as a strong ordinary comparison, rather than
presenting it as the new central invention.
