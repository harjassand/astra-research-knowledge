# A finite-rate single-file gear for real load transfer

30 October 2026. A second, stronger ordinary comparison. It removes the
growing-barrier requirement of `PASSIVE_NATIVE_GEAR_AND_LOAD.md` by changing
the actual material geometry. This is a concrete exclusion device, not a
claim to invent tight coupling, single-file transport or unicyclic motors.

## 1. The physical cell and the complete current identity

Put two distinguishable original carriers (A,B) into a closed three-pocket
single-file track. Each pocket holds at most one carrier. The remaining pocket
is a vacancy. A carrier can move by one track step into the adjacent vacant
pocket. It cannot pass the other carrier, exchange places directly, leave the
track, or use a bypass. Count every actual signed carrier step, including steps
across the coordinate cut.

The six configurations, listed in their clockwise transition order, are

\[
 (A,B)=(0,1),(0,2),(1,2),(1,0),(2,0),(2,1).                 \tag{1}
\]

The forward steps alternately move (B,A,B,A,B,A), always clockwise. Reverse
steps undo the corresponding physical motion. Thus the configuration graph
is a six-cycle, derived from local exclusion, without an event-updated
controller bit or a hypothetical simultaneous move.

Choose unwrapped initial positions with $x_A-x_B\in\{-1,-2\}$. The order
constraint keeps this relative lift in that same set at every time. Therefore

\[
 J_A(t)-J_B(t)=r(S_t)-r(S_0),\qquad
 r(S_{2j})=-1,\quad r(S_{2j+1})=-2.                        \tag{2}
\]

In particular,

\[
 |J_A(t)-J_B(t)|\le1\quad\text{for every path and every }t. \tag{3}
\]

This identity is about the two original carriers. It is valid with arbitrary
waiting times and hidden histories, as long as every actual transition obeys
the declared no-passing geometry. It is not a statement about a sum containing
an unobserved compensating current. The vacancy is a material configuration,
not an independent reservoir of charged motion.

For $N$ separate cells, every time and every initialization obey

\[
 \sup_{t\ge0}\left|{\sum_iJ_{A,i}(t)-\sum_iJ_{B,i}(t)\over N^2}\right|
 \le {1\over N}.                                         \tag{4}
\]

No accuracy-dependent barrier, sensing, centralized communication or clock
synchronization is needed for (4). The material requirements are real: each
cell has a sealed single-file cycle, two original carriers and one vacant
pocket. This is a different native interface from two separated unrestricted
conductors. A finite overtaking channel invalidates the exact identity.

## 2. Unknown reciprocal clocks and actual force ports

To establish positive throughput and work, specify the following actual
finite-state supplier. Edge $e$ has an arbitrary frozen unknown reciprocal
prefactor $c_e\in[c_-,c_+]$, with $c_->0$. Let $a(e)$ be the species moved
by its forward step. Applying torque/step affinity $f_A,f_B$ gives

\[
 q(S_e,S_{e+1})=c_e e^{f_{a(e)}/2},\qquad
 q(S_{e+1},S_e)=c_e e^{-f_{a(e)}/2}.                       \tag{5}
\]

The force acts on the actual carrier displacement. All six edges are local
track transitions, and the maximal escape rate is at most
$2c_+e^{\max|f_a|/2}$. The whole cell has fixed size and fixed response rates
when the force range is fixed. Each frozen device can have six different
unknown $c_e$; no rate fitting is performed.

The complete cycle affinity is

\[
 \mathcal A=3(f_A+f_B).                                   \tag{6}
\]

Let $I$ be stationary clockwise configuration-cycle flux. Its sign is the
sign of $\mathcal A$. One elementary proof iterates

\[
 I=a_e\pi_e-b_e\pi_{e+1},
 \quad a_e=c_e e^{f_{a(e)}/2},\quad b_e=c_e e^{-f_{a(e)}/2},
\]

around the cycle. The coefficient multiplying $I$ is a strictly positive
sum, and the numerator has the sign of
$\prod_ea_e-\prod_eb_e$. No cycle-kinetics estimate enters this sign argument.
Both real carrier velocities are

\[
 v_A=v_B=3I.                                             \tag{7}
\]

At $f_A+f_B=0$, the work on an edge is the state difference
$f_A[r(S_{e+1})-r(S_e)]$. The exact equilibrium law is

\[
 \pi_e^{\rm stall}\propto e^{f_A r(S_e)}.                 \tag{8}
\]

Thus the exact thermodynamic stall is known without knowing any clock. This
does not set the useful speed away from stall: the positive clock bounds are
necessary for a quantitative throughput guarantee.

The reciprocal prefactors in (5) are part of the supplied native kinetics.
An arbitrary hidden drive that changes their forward/backward ratio is not
covered. Identity (2) survives such a drive, but the passive work conclusion
would not.

## 3. Exact weak-force mobility and finite response

At zero force the invariant configuration law is uniform. Linearize the
stationary edge current around $f_A=f_B=0$, writing
$\pi_e=1/6+u_e+O(|f|^2)$. Then

\[
 I=c_e\left[u_e-u_{e+1}+{f_{a(e)}\over6}\right]+O(|f|^2).
\]

Divide by $c_e$, sum the six edges, and use telescoping. The result is

\[
 v_A=v_B=m_c(f_A+f_B)+O(|f|^2),\qquad
 m_c={3\over2\sum_{e=0}^5c_e^{-1}}.                       \tag{9}
\]

Uniformly over every supplied unknown device,

\[
 c_-/4\le m_c\le c_+/4.                                  \tag{10}
\]

The remainder is uniform because the finite generators form a compact
uniformly irreducible family. In particular this is a useful load port, not
merely a kinematic current identity with unspecified zero throughput.

The equilibrium diffusion coefficient of the common real current
$C=(J_A+J_B)/2$ equals the same $m_c$. For completeness, let $Y$ count
forward minus reverse configuration steps, so $C=Y/2$. The periodic corrector
for $Y$ minimizes

\[
 D_Y={1\over6}\min_{\sum_eg_e=6}\sum_ec_eg_e^2
     ={6\over\sum_ec_e^{-1}}.                            \tag{11}
\]

The minimizer has $c_eg_e$ constant. Dividing by four for $C=Y/2$ gives
$D_C=m_c$, including the correct factors of two. This is the conventional
conductance formula for a periodic hopping chain.

## 4. Loaded operating work and full weak-field current law

Take $N$ independent cells and fixed forces
$f_A=F_A/N, f_B=F_B/N$, with $F_A>0>F_B$ and $F_A+F_B>0$. Let
$\bar m_N=N^{-1}\sum_im_{c,i}\to\bar m>0$. On physical time $N^2T$,

\[
 {1\over N^2}E\sum_iJ_{A,i}(N^2T)
 ={1\over N^2}E\sum_iJ_{B,i}(N^2T)
 =\bar m(F_A+F_B)T+o(1).                                 \tag{12}
\]

This is uniform over starting configurations; the finite-state transient
changes each expected integrated current by a bounded amount. The output
works against its load:

\[
 {EW_{\rm in}\over N}\to F_A\bar m(F_A+F_B)T,
 \qquad
 {EW_{\rm out}\over N}\to -F_B\bar m(F_A+F_B)T.           \tag{13}
\]

Each source work is its actual force times its actual carrier displacement.
At finite force the stationary efficiency is **exactly** $-f_B/f_A$, by (7),
when the common current is positive. In particular it tends to one only as
the total affinity and, under bounded clocks, the power tend to zero. No
finite-power reversible engine is being asserted.

The full joint weak-field path law also has a simple limit. For

\[
 X_a^N(t)=N^{-2}\sum_iJ_{a,i}(N^2t),
\]

the speed-$N$ rate, on finite time intervals, is

\[
 I(x_A,x_B)=
 \begin{cases}
 \displaystyle {1\over4\bar m}\int_0^T
       [\dot x-\bar m(F_A+F_B)]^2dt,
       &x_A=x_B=x,\ x(0)=0,\ x\text{ absolutely continuous},\\
 +\infty,&\text{otherwise}.
 \end{cases}                                               \tag{14}
\]

Here is a short finite-state proof, rather than an inference from the mean.
For a single cell let $\lambda_c(q;f_A,f_B)$ be the leading eigenvalue of the
generator tilted by the actual common-current increment $\pm1/2$.
Uniform irreducibility and compact bounded $c_e$ make its small-parameter
eigenvalue and eigenvectors uniformly analytic. Equations (9)–(11), and the
exact zero current for every $f_A=-f_B$, identify the expansion

\[
 \lambda_c(q;f_A,f_B)
   =m_c[q^2+(f_A+f_B)q]
       +O((|q|+|f_A|+|f_B|)^3).                          \tag{15}
\]

The eigenvalue vanishes at $q=0$ for all forces, so there are no pure-force
terms. Insert $q=\theta/N, f_a=F_a/N$, run for $N^2\Delta t$, and multiply
the $N$ independent cell moment-generating functions. After division by
$N$, the remainder vanishes. For a fixed finite time partition, successive
leading eigenvectors differ from the un-tilted ones by $O(1/N)$; their
products produce only $O(1)$ total log-prefactors. This gives the limiting
finite-dimensional cumulant

\[
 \sum_k\Delta t_k\bar m[\theta_k^2+(F_A+F_B)\theta_k].
\]

The same positive tilted eigenfunctions furnish exponential martingale bounds
for a running increment on an interval of length $\delta$. For each fixed
$\theta$, the log bound divided by $N$ is at most
$C\delta(\theta^2+|\theta|)+o(1)$. Chernoff optimization, followed by
$\delta\downarrow0$, gives exponential tightness of the modulus of continuity;
single aggregate jumps have size $1/(2N^2)$. The finite-dimensional Legendre
transforms therefore yield the scalar action in (14). Finally (4) is a
deterministic uniform-path bound, so both actual currents have the stated
joint rate. Arbitrary initial configurations and retained records cause only
the same (1+O(1/N)) single-cell eigenfunction factors, provided future clocks
are supplied independently conditional on the fixed device parameters.

This standard small-tilt finite-state argument is included to show that the
device competes at a full current-history objective, not just average power.
It is not a new large-deviation method.

## 5. Why this is an ordinary alternative and what it costs

Single-file transport is precisely the non-passing material constraint used
here. Ryabov and Chvosta, *Single-file diffusion of externally driven particles*,
Phys. Rev. E **83**, 020106$R$ (2011),
[DOI](https://doi.org/10.1103/PhysRevE.83.020106),
[primary full text](https://arxiv.org/pdf/1203.0777), explicitly analyze that
constraint and actual work/heat. Their exact continuous propagator assumes
identical drifts and diffusivities; it is **not** being applied to the unequal
forces and unknown edge clocks in this note. The discrete construction above
is derived directly.

The unicyclic current and conductance calculation is established hopping
theory: Derrida, J. Stat. Phys. **31**, 433–450 (1983),
[DOI](https://doi.org/10.1007/BF01019492). The actually read primary comparison
of its diffusion formula to Lifson–Jackson is Kalnin and Berezhkovskii,
[J. Chem. Phys. 139, 196101 (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4108624/),
especially Eqs. (3), (10), (11). The original Derrida author's PDF site timed
out; no claim of a full read of that original paper is made. These are close
predecessors, not novelty evidence from a failed search.

Hardware and operation remain explicit:

- $N$ closed microscopic tracks, (2N) original carriers, $N$ vacancies,
  and actual species-selective drive/load ports;
- fixed local hopping bandwidth, with force-modified rates (5);
- material loading and confinement, plus any sensing used to verify delivery;
- no controller arithmetic, no repeated read/erase cycle and no global
  event broadcast;
- thermal jump events and contact dissipation are not free energy sources.

No runtime sensing is needed for the coupling proof. If input/output work is
metered, the meters and their records are additional real resources. The
identity is valid with the full native transition log retained.

The ideal exclusion graph is an actual model premise, not an experimental
certification of an apparatus. A narrow hard-particle track supplies its
geometric content; a generic soft repulsion with nonzero overtaking probability
does not. Hopping wells are an idealized finite-rate supplier. A real continuous
track can contain additional no-passing motions without spoiling (2), but its
exact six-rate speed formula must then be replaced by that actual dynamics.

## 6. The preserved-bulk boundary remains

This construction conclusively defeats the broad claim that real current
locking or load transfer must use active auxiliary counterflow. It does not
defeat the root's stronger round-11 task.

The two carriers have been placed in the same exclusion geometry. Their
conditional motion, tagged densities, relative relaxation and response to
separate forces are changed. $N$ microscopic gears are not a hidden way of
preserving the full density histories of two extended unrestricted conductors.
Each track contains a fixed pair; it is not an arbitrary spatial transport
program. Replacing the original conductors by these tracks is a material
redesign that must be stated, not a harmless current-counting convention.

This is why the useful stronger target is: retain arbitrary native bulk
histories while paying thermodynamic-order operating work for actual altered
transport. Ordinary native gearing already solves the less constrained load
task with fixed local rates; it does not supply that stronger preservation.
