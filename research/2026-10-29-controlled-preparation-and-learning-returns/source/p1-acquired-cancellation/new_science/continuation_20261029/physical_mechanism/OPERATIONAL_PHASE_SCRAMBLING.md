# Operational phase scrambling: a physical finite-record compiler

29 October 2026. Complementary P1 construction. This note changes the actual
service calls by inserting a warranted nuisance-coordinate scrambling operation.
It is not a strengthening for the unchanged operation menu in the handoff.

## 1. Consequence and close predecessor

A physically implemented conditional randomization can turn an otherwise
non-Markov visible process into an exactly Markov controlled process. The
hidden system can retain a frozen variable that affects its unscrambled
dynamics. Fresh independent randomization removes that variable's influence on
the admitted endpoint records, without resetting the variable itself.

Group averaging and conditional-expectation projections are established
machinery. Choi, Lim and Wang, *Group-averaged Markov chains II*,
arXiv:2512.13067v1 (15 December 2025), explicitly study orbit Gibbs kernels and
their GPG sandwiches, spectral comparison, information projection and exact
sampling. Boyd, Diaconis, Parrilo and Xiao, *Symmetry Analysis of Reversible
Markov Chains* (revised 29 November 2004), give classical orbit lumping under
automorphism groups. This note does not claim to invent either construction.
The additional scoped calculation is a finite-bit physical phase-randomization
interface, retained-history-safe record bound, and acquisition without initial
hidden equilibrium. Whether this package is historically novel is unresolved.

Primary sources read:

- https://arxiv.org/html/2512.13067v1 (abstract and introduction, lines 41--72).
- https://web.stanford.edu/~boyd/papers/pdf/symmetry_analysis.pdf
  (title, introduction and orbit discussion).

## 2. Exact conditional randomization

Let the hidden state be X=(Y,U,S), where Y has k visible values, U lies in a
compact group with normalized Haar law h, and S is arbitrary untouched memory.
For clarity the main example uses U on the circle. Assume the ACTUAL operation

    R : (y,u,s) -> (y,u+V,s),       V independent and Haar,

is available. The randomization key is not retained or used later. Conditional
on any complete old record Z and present (Y,S), the new U is Haar and independent
of (Z,Y,S). This is a physical operation, not a projection inferred from data.

Let T_j be any available hidden-state kernel. Assume its Haar-averaged visible
row does not depend on untouched memory:

    p_j(y,a) = int T_j((y,u,s), {Y'=a}) h(du),     all s.        (1)

The output hidden memory may change under T_j. Equation (1) must hold for every
memory state reachable under all admitted calls, or uniformly on a warranted
invariant set. No reversibility or equilibrium premise is needed here.

A service stage chooses j from the complete visible history (including Z),
executes R then T_j, and reads the new Y. Then, for every actual initial joint
law of (X,Z),

    P(Y_(t+1)=a | Z,Y_0,...,Y_t,j_t) = p_(j_t)(Y_t,a).       (2)

Thus the complete adaptive endpoint record has exactly the law of the positive
k-state controlled Markov model with matrices p_j, jointly with the SAME old
record Z and actual initial Y_0. Arbitrary initial densities, point masses and
arbitrarily informative retained old records are allowed. This avoids a cold
hidden-equilibrium calibration premise only because R is additional physical
access.

Proof: condition further on the complete current hidden state and the past.
The fresh Haar shift yields the same conditional U law for every input u.
Integrating the next visible event gives (1), independent of s and all earlier
data. Average that identity over the conditional hidden state and induct on
the record length. Randomized policies can be conditioned on their independent
retained policy keys. The scrambling keys themselves cannot be retained under
this theorem: conditioned on a known shift, no averaging has occurred.

It suffices that U lie in a homogeneous group orbit and R sample the orbit
measure. Additional orbit invariants belong in S; (1) is substantive. Merely
preserving visible labels does not make a randomization sufficient.

## 3. Approximate scrambling: complete records accumulate only local error

Replace R by an actual operation A preserving Y,S with

    sup_(y,u,s) TV(A((y,u,s),dU'),h(dU')) <= delta.            (3)

Every conditional next-label distribution differs from p_j(y,.) in TV by at
most delta, by data processing. Even after arbitrary history-dependent choices,
the complete n-stage records therefore satisfy

    TV(actual record, positive Markov record)
       <= 1-(1-delta)^n <= n delta.                          (4)

This holds jointly with arbitrary Z and Y_0. Couple the two next-label rows
maximally while the visible histories agree. Their prescribed actions then
agree. The conditional chance of a new mismatch is at most delta. Multiplying
the conditional survival bounds proves (4). No hidden-state coupling across
models is assumed.

If the law in (1) varies by at most xi from a chosen p_j uniformly in s, replace
delta by min(1,delta+xi). If an acquired positive transition model has row-TV
error eta, the complete model error is bounded using delta+xi+eta. Real sensor
and actuation errors must be bounded at this conditional interface too.

An extra initial label read is already Y_0 in this construction: its exact
joint law with Z is preserved. There is no omitted branching factor because
the local condition is pointwise in the complete physical state, not an L2
subspace residual.

## 4. Finite random bits plus short diffusion

Ideal continuous Haar randomness is not a finite implementation. On the
circle, take M=2^b equally spaced shifts and then run a calibrated angular
diffusion with generator D partial_theta^2 for time tau, holding Y and S fixed.
The shift index uses b fresh independent uniform bits, discarded after the
actuation. Let A_M be this ACTUAL composite operation. Its conditional angle
density relative to Haar is

    k_M(theta) = 1 + 2 sum_(ell>=1)
                         exp[-D tau ell^2 M^2] cos(ell M theta).

The input angle only translates this density. Integrating its absolute
deviation gives the rigorous uniform bound

    delta_M <= sum_(ell>=1) exp[-D tau ell^2 M^2]
             <= exp[-D tau M^2]/(1-exp[-3D tau M^2]).        (5)

The first inequality uses |cos|<=1, not a numerical Fourier truncation. The
second follows from ell^2>=1+3(ell-1). Thus for a prescribed n-stage error
epsilon it is sufficient to choose M so that the right side is <=epsilon/n.
At fixed positive D tau this uses b=O(log log(n/epsilon)) fresh random bits
PER STAGE. M must be a power of two. This counts distinct ideal phase options,
not total physical precision. In particular it does NOT imply that angular
accuracy merely on the order of 1/M preserves the exponentially small error.
Bit count does not pay actuation accuracy, phase-reference stability, diffusion
calibration, waiting, work, or sensor cost.

Suppose the implemented relative grid points each differ by at most eta_phase
from an ideal grid, up to any common phase offset. Coupling the indices and
using the TV distance between translated real heat kernels, then wrapping to
the circle, adds at most

    eta_phase / [2 sqrt(pi D tau)]                            (5b)

to delta_M, capped at one. The real Gaussian has variance 2D tau, and its
L1 derivative norm is 1/sqrt(pi D tau), proving the translation bound. A common
offset does not cost anything because the bound in (5) is translation-invariant;
independent errors in relative angles do. If the implemented random index has
TV bias rho from uniform, add rho. A warranted lower bound on D tau may replace
the exact value in (5); non-heat imperfections need a separate bound. Thus the
actual per-stage record error is bounded by

    delta_eff <= min(1, delta_M + eta_phase/[2sqrt(pi Dtau)]
                           + rho + delta_other).

At fixed Dtau and program length n, generic actuation error can require
eta_phase=O(epsilon/n). The inexpensive ideal random-bit scaling therefore
does NOT establish inexpensive total acquisition or execution. The numerical
table in the checker reports ideal-grid bounds only.

For finite shifts without the diffusion, the conditional angle measure from a
point input is atomic and has TV distance ONE from Haar for every finite M.
Hence finite quadrature is not a hidden-state TV reset. The short physical
diffusion is indispensable to (5). An alternative proof using smooth next-call
effects could support a weaker endpoint-only interface, but is not substituted
here.

## 5. A reversible switching-diffusion source with frozen memory

Take y in {0,1}, theta on the circle and s in a finite set, with s frozen
forever. Available native service call j runs for a fixed time t_j under

    L_(j,s) f(y,theta)
      = D_serv partial_theta^2 f(y,theta)
        + r_j(theta+phi_(j,s))[f(1-y,theta)-f(y,theta)],

    r_j(theta)=c_j+d_j cos(theta),  c_j>|d_j|>0,
    D_serv>0.                                                (6)

Each sector is a reversible elliptic switching diffusion with common uniform
law on (y,theta); an arbitrary law on s is invariant. Global hidden mixing is
absent. The actual phase shift and held-label diffusion used in A_M are extra
controls; the source does not magically supply them.

For each j and s, rotating theta by phi_(j,s) conjugates the native service
semigroup to the same sector-independent operator. Haar integration therefore
proves (1). Different operations can have different spectator-dependent phase
offsets. Before scrambling, those offsets and the retained phase affect
transient observed responses; they are not dynamically irrelevant in the raw
device.

If p_j is the effective flip probability, conditioning on the angle path gives

    (1-exp[-2t_j(c_j-|d_j|)])/2 <= p_j
       <= (1-exp[-2t_j(c_j+|d_j|)])/2 < 1/2.                 (7)

The finite positive Markov controller remains nontrivial: different j can
produce different flip probabilities, and a conventional dynamic program can
choose them from current y and the recorded task history. The same informed
conventional controller is the correct comparator; there is no new solver
advantage in this construction.

The topology in (6) has two observed components. It does not contradict the
earlier connected-space injective smoothing obstruction. More generally a
true label-preserving fiber reset is noninjective; composing it changes the
physical operation whose finite closure is at issue.

## 6. Acquisition on one nonstationary device

Under exact R, all completed trials of a chosen row (j,y) have conditional
next-label law p_j(y,.) even if their start times are selected from the past and
their hidden spectator is never reset. The observer can use the first N visits
to each requested row, choosing the operation before its fresh randomness.
Conditional Hoeffding gives, simultaneously over s_ops*k*k entries,

    |p_hat_j(y,a)-p_j(y,a)| <= sqrt(log(2 s_ops k^2/beta)/(2N))

with probability at least 1-beta. With A_M the right side gains delta_M as
bounded conditional bias. The empirical row is already a positive probability
vector. Entry errors convert to row-TV by k/2. This is a martingale confidence
argument, not an assertion that unconditioned successive hidden states are iid.

All visits and intervening calls are charged. If some row is never reached,
that row is not acquired. The explicit symmetric binary family (7) supplies
nonzero flip probabilities and hence geometric visit-time bounds; a general
source requires its own reachability/time contract or actual visible-state
preparation. A finite stopping-rule confidence statement must either use fixed
N visits per row, as above, or a valid confidence sequence.

The inherited adjoint-word acquisition can still apply to warranted reversible
factors, but it is unnecessary for the directly sampled positive row model at
this changed interface. An unknown heat coefficient or an uncalibrated phase
actuator is not certified by a short apparent Markov fit.

## 7. Useful failure boundaries

1. Retaining the random phase key can recover hidden dependence. A one-time
   mask is not erased conditional on its key.
2. A frozen spectator that changes the Haar-averaged row survives every phase
   reset and remains visible. Condition (1) cannot be replaced by equal visible
   equilibrium probabilities.
3. Finite deterministic phase grids without smoothing are microscopically
   singular, even though they can approximate specific smooth effects.
4. A reset only before the whole program does not imply (2): native calls can
   regenerate correlations between the visible state and phase. The phase
   operation is paid before EVERY admitted stage.
5. Group averaging, lumpability, local equilibration and controlled Markov
   dynamic programming are established. This construction is not evidence of
   a civilisation-scale discovery, practical speedup or laboratory realization.

The accompanying exact finite checker verifies the full adaptive-record claim
on two operations, four retained initial hidden histories, all 128 depth-three
binary action trees, and a frozen spectator that is visible without scrambling.
It also checks the approximate-scrambling record bound and reports a finite-bit
heat-kernel resource table. The rational check is population algebra; it is
not a physical or finite-sample acquisition experiment.
