# Reversal information: an exact ambiguity and an additional-operation certificate

29 October 2026, Brisbane. Root construction after the parity failure of
the acquired entropy assay. This note pursues the information question:
which extra physical fact or operation makes a thermodynamic consequence
identifiable? It does not infer physical parity from a fitted generator.

The positive result is a theorem for a declared intervention interface.
No physical parity operation was acquired or executed in this tranche.
The earlier native entropy assay remains an acquired ALL-EVEN result.

## 1. Definitions and the changed scientific question

Let Q be a finite irreducible row CTMC generator with positive stationary
law pi. Write Pi=diag(pi) and Q*=Pi^{-1}Q^T Pi. An involution Theta is
represented by its permutation matrix. Assume pi Theta=pi. The physical
reversal of a microscopic path is time reversal followed by Theta.
The physically reversed stationary generator is

    R = Theta Q* Theta.

Generalized detailed balance is Q=R. It is distinct from ordinary
detailed balance Q=Q* unless Theta is the identity or additional
commutation holds. The stationary path entropy rate is

    sigma_Theta = sum_x pi_x sum_{y!=x}
        [q_xy log(q_xy/R_xy) - q_xy + R_xy].                 (1)

Use the extended-value conventions at zero rates. Since pi and the
Theta permutation preserve the stationary average escape rate, the last
two terms sum to zero, but keeping them makes the path-divergence
interpretation explicit. A faithful thermodynamic interpretation still
needs the physical reversal and local detailed-balance model. No abstract
involution by itself constructs an equilibrium laboratory system.

An observed label kernel E is nonnegative with row sums one and
Theta E=E. Endpoint emissions are independent conditional on the
microscopic path, or deterministic. The statement below concerns even
observations. An odd observation can be transformed with a known label
reversal, which must be made explicit before applying the formulas.

The new target is stronger than a mean record: distinguish irreversibility
from hidden reversible transport, and specify an actual extra operation
that resolves this ambiguity when it is available.

## 2. A classical doubled lift and its observation consequence

On states (x,+),(x,-), take generators Q and Q* respectively and add
sign flips of rate epsilon at fixed x. The stationary law is pi_x/2,
and parity swaps the signs. The full generator is

    L_epsilon = [[Q-epsilon I, epsilon I],
                 [epsilon I, Q*-epsilon I]].              (2)

Its adjoint equals Theta L_epsilon Theta. Thus its generalized path
entropy is zero. The adjoint-pair/sign lifting mechanism is established
skew-detailed-balance/Yaglom-reversible machinery; see Andrieu and
Livingstone (2021), Section 3.3 and Section 4.1. It is not claimed here
as a new Markov construction.

At epsilon=0, the stationary visible law, with signs unobserved, is
one half the Q law plus one half its reversed law. If the original
visible process is reversal invariant, it is reproduced exactly.
This epsilon=0 completion is generally not irreducible. For epsilon>0,
the completion is irreducible, and coupling up to its first sign flip
gives, on every passive observation horizon T,

    TV(P_visible, P_visible,epsilon) <= 1-exp(-epsilon T).  (3)

For independent stationary runs of total deterministic duration T_total,
the same coupling gives a bound 1-exp(-epsilon T_total). This is a
finite-horizon closure statement, not exact infinite-time equality or a
uniform finite mixing-time guarantee. It does not automatically preserve
specified reset maps, resolved singleton ports, or control operations.

There is a sharp metric consequence. On a fixed horizon let E_Theta be
the class of stationary visible laws of finite irreducible generalized-
equilibrium CTMCs, with hidden parity unrestricted and even observations.
For every visible law P supplied by the finite irreducible source,

    inf_{R in closure(E_Theta)} TV(P,R)
       = (1/2) TV(P,P^rev).                               (3a)

Every law in the closure is reversal invariant, so the triangle inequality
gives the lower bound. The symmetrized mixture (P+P^rev)/2 attains it and
(2) puts that mixture in the closure. Hence a uniformly size-alpha test
against this unrestricted equilibrium class has power at most alpha at
every reversal-invariant finite-source law, for any fixed finite passive
data horizon. This is an observation-class statement, not an assertion
that every such abstract model is a native physical mechanism.

The next construction closes that reset loophole for the complete native
return interface used by this project.

## 3. Exact reciprocal return completion with the same resolved ports

Use unnormalized stationary weights w and a nonempty resolved port set B;
let I be the hidden interior. The original Q is irreducible. Form a new
state space B disjoint-union I_+ disjoint-union I_-. Preserve each port
as ONE state. Assign weights w_b to ports and w_i/2 to either hidden copy.
The new rates are:

* Within I_+, use Q_II; within I_-, use Q*_II, including their diagonals.
* From port b to i_+, use q_bi/2; to i_-, use q*_bi/2.
* From i_+ to port b, use q_ib; from i_- to port b, use q*_ib.
* For distinct ports b,c, use (q_bc+q*_bc)/2.
* Keep the original port diagonal q_bb. There are no inter-copy jumps.

The stationary reversed chain has the same escape rate at every state:
q*_xx=q_xx. Hence every row sums to zero, each native port holding rate
is unchanged, every hidden escape-rate ceiling is preserved, and the
total stationary weight W is unchanged. Define Theta to fix B and swap
I_+ with I_-. Edgewise fluxes obey generalized detailed balance. This
also proves stationarity of the stated weights.

The chain is irreducible. Every hidden copy can reach B and is reachable
from B by an original or reversed directed path; the plus layer and the
unchanged port set retain paths between every pair of ports. The factor
one half on entries does not remove any positive edge. If I is empty,
the construction reduces to the symmetrized port chain.

Let the original positive-duration excursion flux density be

    K(t) = diag(w_B) Q_BI exp(t Q_II) Q_IB.

Then the new density is exactly

    K_new(t) = [K(t)+K(t)^T]/2,      t>0.                  (4)

The second term follows from Q*_{II}=diag(w_I)^{-1}Q_II^T
diag(w_I). Direct-port fluxes are likewise symmetrized. Port departure
fluxes rho_b=w_b(-q_bb) and their preparation probabilities rho_b/R
are unchanged.

**Exact information consequence.** If the complete original hidden-return
kernel K(t), including the separately handled zero-duration direct flux,
is reciprocal, the new finite irreducible generalized-equilibrium model
reproduces every native excursion law exactly. Because a resolved port
is an actual microscopic renewal state, it also reproduces arbitrary
concatenations of these excursions and native port holds, including
adaptive choices of which resolved port to reset to. All mean, lifetime,
bounded-bin and paired residence consequences of that interface agree.
Known native holding rates and escape-rate ceilings do not distinguish
the two models. The completion uses at most 2|I|+|B| states.

No separately stipulated control action or preparation inside I has been
preserved by this theorem. A known all-even microscopic state class
excludes the completion. So can an independently calibrated operation
whose action on physical parity is specified. More samples of the same
complete reciprocal native law cannot do so.

The merged-port idea was supplied by the controlled-frontier collaborator;
the root derivation above and the independent thermodynamic review retain
its actual scope. PARITY_DOUBLING_INDEPENDENT_REVIEW.md and its exact
rational controls verify three port sets of a nonuniform directed chain,
the 25-state glued version of the 15-state source, and 20 Laplace-kernel
identities. No source observations were added. This extends the explicit
15-state parity counterexample without changing the earlier all-even theorem.

## 4. A midpoint parity operation restores a nonnegative Gram constraint

Assume the following ADDITIONAL access: a calibrated instrument can apply
the true microscopic involution Theta instantaneously at the midpoint of
a fixed observation horizon t. The pulse is deterministic and its action
is known on every physically relevant microscopic state. The source is
stationary with pi Theta=pi. This is stronger access than knowing a
generator family or printing an involution. Its physical preparation,
control precision and energetic costs are not acquired for free.

Writing h=t/2, retain the two endpoint labels. Their joint matrix is

    C_echo(t) = E^T Pi exp(hQ) Theta exp(hQ) E.              (5)

If Q*=Theta Q Theta, let V=exp(hQ)E. Since Theta E=E,

    C_echo(t) = V^T Pi V.                                 (6)

It is therefore completely positive (CP): a Gram matrix of nonnegative
vectors. The midpoint operation cancels the involution that otherwise
sits between the two reflected hidden predictions. The conditional
interpretation is two equal nonnegative half-path factors. This is an
ordinary positive Markov factorization; the object to test is now an
intervention law rather than the passive law.

For a nonequilibrium Q, let R=Theta Q* Theta and define the killed
geometric generator S by

    S_xy=sqrt(q_xy R_xy) for x!=y,
    S_xx=(q_xx+R_xx)/2.                                  (7)

Cauchy-Schwarz and the arithmetic-geometric inequality give S1<=0.
Its adjoint obeys S*=Theta S Theta, including the diagonal. The path
submeasure generated by S on each half, with the same exact midpoint
pulse, is the geometric mean of the forward and physically reversed
echoed path measures. The geometric endpoint matrix consequently is

    B_echo = E^T Pi exp(hS) Theta exp(hS)E
           = [exp(hS)E]^T Pi [exp(hS)E],                  (8)

which is CP. Conditional emissions do not change this conclusion when
they satisfy the declared independence/reversal contract.

The physical reversal maps the deterministic midpoint pulse into itself:
a transition x -> Theta x becomes x -> Theta x after reversing time and
applying Theta. Both stochastic halves have stationary marginal pi,
since the pulse preserves pi. Therefore their full path KL is

    KL(P_echo || P_echo^rev,Theta) = sigma_Theta t.         (9)

This equality does not count laboratory work required to implement the
pulse. It is the passive generator's generalized stationary path entropy
integrated over the two stochastic halves. A dissipative implementation
of the instrument is an additional system and must be costed separately.

Entrywise path AM-GM gives C_echo,sym-B_echo>=0 with total mass
1-affinity(P_echo,P_echo^rev,Theta). The involutive path-reversal inequality
KL>=4(1-affinity), used in COPOSITIVE_PATH_CERTIFICATES.md, now proves:

**Midpoint-operation theorem.** For every supplied copositive H, with
h_minus=max(0,-min_ij H_ij)>0,

    sigma_Theta >= 4[-<H,C_echo,sym(t)>]_+/(t h_minus).    (10)

Equivalently, using the CP deficit already defined in
POSITIVE_FRAGMENTS_AND_HISTORY.md,

    sigma_Theta >= 4 d_CP(C_echo,sym(t))/t.                (11)

The nonlinear CP relaxation from that note also applies to sigma_Theta t.
No microscopic state-count bound or clock ceiling is required in the
EXACT-operation theorem. At Theta=identity it reduces to the passive lag
theorem. Thus the same information geometry can be accessed by two
different physical routes: a justified all-even source class, or a known
microscopic parity operation. Neither route is inferred merely from a
good fit to passive means or waiting times.

## 5. The finite-information and finite-precision acquisition bridge

Choose H and t before using the certification data, or pay the appropriate
selection/uniform-confidence cost. With N independent stationary
preparations, execute the pulse once per trial and measure the endpoints.
For Y=H_{Y_0,Y_t}, let L=max H-min H and let bar_Y be the sample average.
A one-sided Hoeffding bound gives, with failure at most delta,

    -E Y >= -bar_Y - L sqrt(log(1/delta)/(2N)).             (12)

This is a bounded fixed-horizon score, so no unobserved lifetime tail
assumption is required. Independence or a supplied mixing/renewal
replacement is still required; a long trajectory does not automatically
provide independent trials.

Suppose the ACTUAL experiment differs from the ideal endpoint law by
total variation at most nu. The score correction is at most L nu. Thus
the implementable certificate is

    sigma_Theta >= (4/(t h_minus))
      [-bar_Y-L sqrt(log(1/delta)/(2N))-L nu]_+.            (13)

An explicit sufficient bound is

    nu <= min(1, nu_prep + eta_pulse + 2 Lambda kappa
                    + eta_readout),                     (14)

where the initial law is within nu_prep of pi, the actual pulse A has
uniform row TV distance at most eta_pulse from Theta, its midpoint
placement error is at most 0<=kappa<=t/2, all native escape rates are at most
Lambda, and the joint endpoint readout error has TV at most eta_readout.
For timing error, compare the two products with a pulse shifted by d:
Markov contraction and TV(exp(|d|Q)(x,.),delta_x)<=Lambda|d|
give the two Lambda|d| terms. The pulse term follows from one stochastic
kernel replacement and data processing. This is a sufficient calibration
bound, not claimed tight. Without a rate/continuity control, a small
clock error alone has no uniform state-law guarantee.

For causal placement inside [h-kappa,h+kappa], conditioning on a realized
offset does not by itself justify that semigroup argument. A common
uniformization clock repairs it: if no candidate event occurs in the
whole window, the coupled endpoint states agree after both pulses.
The error is at most 1-exp(-2 Lambda kappa)<=2 Lambda kappa. With a fixed
or independently scheduled offset d, the shorter interval gives
1-exp(-Lambda|d|). The actual imperfect pulse need not preserve pi:
the certificate compares its endpoint law with the ideal law rather
than asserting stationary path KL for the imperfect experiment.

Full essential resources are N independent preparations, N microscopic
parity operations, Nt units of native evolution, 2N label readouts, the
declared timing and pulse calibration, and a proved copositive witness.
Evaluating an already supplied witness is linear in the number of trials;
finding a useful witness or validating a physical parity primitive may
be difficult. No experiment executing this new interface has been done.

The strongest equally informed baseline is hidden-model entropy
minimization using the same controlled endpoint table and confidence
region. It can adopt (10) as a valid analytic constraint. No statistical
or computational advantage over that full task has been demonstrated.
The prospective addition is an explicit dimension-independent consequence
and its intervention/precision contract.

The independent review in intervention_challenge/
PARITY_ECHO_INDEPENDENT_REVIEW.md validates Sections 4-5 at these
conditions. Its exact six-state odd-velocity CTMC control, at t=24/5,
has a supplied PSD/copositive witness H=zz^T, z=(1,-1,0), with rigorously
bounded gap gamma>321263/64968750. A closed-form zero-flip comparison
and first-flip coupling certify the result, without an interval matrix
exponential. It also checks unequal parity-partner escape rates and
the averaged S diagonal. No native measurements, parity operations or
finite-sample assay were executed for this new example.

The robust certificate itself makes one score correction L nu. A
worst-case positive-certificate demonstration may pay two L nu terms:
the actual score can move by L nu and the consumer then subtracts its
own calibration allowance. The review keeps these distinct. At its
declared endpoint error nu=3/2500, the guaranteed corrected population
margin remains positive. This is a theoretical feasibility control,
not an operational advantage over observed-pair KL or full hidden-model
optimization.

## 6. Relation to the preserved results and primary machinery

The actual 262,144-excursion certificate remains conditional on all-even
physical reversal; it is not retrospectively upgraded to a parity-pulse
experiment. The exact clock/mean completion frontier remains useful and
unchanged. Its positive representatives solve a realization problem,
not a new mean-evaluation algorithm.

Established ingredients include hidden-network thermodynamic minimization
(Skinner-Dunkel), positive Markov and reflected-history factorizations,
the entropy half-tilted generator (Lebowitz-Spohn), and involution-reversible
lifting (Andrieu-Livingstone and earlier work). The new claims should be
assessed as the explicit CP entropy certificates, their exact native-law
scope boundary, and the additional-operation restoration theorem. A
targeted literature search is not a priority proof.

Primary source anchors:

* Skinner and Dunkel (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC8106300/.
* Lebowitz and Spohn (1999), https://arxiv.org/pdf/cond-mat/9811220.
* Andrieu and Livingstone (2021), https://discovery.ucl.ac.uk/10108137/1/Livingstone_20-AOS2008.pdf.
* Jorgensen, Neeb and Olafsson (2016), https://arxiv.org/html/1510.07445v3.

The independently preserved controls distinguish exact rational algebra,
numerical matrix checks, ordinary proofs, supplied contracts and actual
native records. Physical energy, instrument calibration and scientific
priority are not established by the same kind of evidence.
