# Control families and hidden-parity equilibrium completions

29 October 2026. Independent construction by the thermodynamic-alternative
branch. This note distinguishes mathematical rate updates, physically
warranted conservative controls, and information actually present in a
native port record. It does not assert a native physical implementation.

## 1. Main results

There are two different answers to the proposed control attack.

1. Departure-only port clock control does not break the passive equivalence.
   The exact port-preserving parity completion survives every deterministic
   or observed-history-adaptive time-varying clock protocol. It also remains
   generalized equilibrium under every frozen control value.
2. A symmetric rate tilt need not preserve generalized equilibrium. The
   missing condition is equality of escape rates at parity partners. For a
   broad class of rate splits, robustness of equilibrium under independently
   addressed port fields forces ordinary detailed balance on every
   port-hidden edge, regardless of the hidden parity or state count.
3. That condition forces the baseline instantaneous hidden-excursion
   matrix K(0) to be completely positive. Thus a non-CP K(0) rules out a
   common equilibrium completion under the stated robust-control contract,
   even though the passive record alone admits an odd completion.
4. One static field in a four-state example makes the native waiting laws
   visibly irreversible. However, the same example also violates the
   simpler equilibrium Gibbs occupancy ratio. No advantage over that
   conventional comparison is claimed.

The phrase "symmetric energy tilt" by itself supplies no physically valid
conservative-control warranty for odd variables. Assuming that warranty
without checking its kinetic content would build the conclusion into the
model class.

## 2. Setup and fixed-control theorem

Use a finite irreducible row generator Q with positive stationary weights
w. Let Theta be an involution, w_Theta(x)=w_x, satisfying full generalized
detailed balance, including diagonals:

    w_x q_xy = w_Theta(y) q_Theta(y),Theta(x),
    lambda_x=lambda_Theta(x).

Ports B are fixed individually by Theta. Hidden states I may be exchanged.
Let u be an even field, u_Theta(x)=u_x, supported on B. Consider the common
rate-update rule

    q^u_xy=q_xy exp[alpha u_y-(1-alpha)u_x],  x != y,

with diagonals reset to make row sums zero. Alpha=1/2 is the symmetric
tilt. Alpha=0 is departure-only clock scaling. The reference Gibbs weights
are

    w^u_x=w_x exp(u_x).

**Theorem 1.** The tilted generator is generalized equilibrium under the
same Theta if and only if

    lambda^u_x=lambda^u_Theta(x)  for every x.

In that case its stationary weights are proportional to w^u. For alpha=0
this holds automatically. For alpha!=0, generalized equilibrium for every
port field in an open neighborhood holds if and only if

    q_xb=q_Theta(x),b,  every hidden x and port b.              (1)

Equivalently, baseline stationary flows obey

    w_x q_xb = w_b q_bx                                      (2)

on all port-hidden edges. No ordinary reversibility inside I is required.

### Proof

The tilted off-diagonal Gibbs flux is

    w^u_x q^u_xy = w_x q_xy exp[alpha(u_x+u_y)].

This satisfies the parity-reversed edge-flux equality automatically. But
its incoming total at x equals w^u_x lambda^u_Theta(x), whereas its outgoing
total is w^u_x lambda^u_x. Hence stationarity, and full generalized detailed
balance, require the displayed escape-rate equality. This is precisely
the condition omitted by an off-diagonal-only argument.

Nor can a different parity-symmetric stationary density repair the issue
while keeping the same Theta. If rho gives generalized detailed balance
for Q^u, divide its edge relation by the baseline relation. The ratios
rho_x/[w_x exp(u_x)] must agree along every directed edge; irreducibility
makes the ratio constant.

Since u is even,

    lambda^u_x-lambda^u_Theta(x)
      = exp[-(1-alpha)u_x]
        sum_y (q_xy-q_Theta(x),y) exp(alpha u_y).

At u=0 the sum vanishes. For hidden x, the only variable terms are

    sum_b (q_xb-q_Theta(x),b)[exp(alpha u_b)-1].                (3)

For alpha!=0, independent variation of the port fields forces each
coefficient to vanish. Conversely, (1) makes (3) zero, and the port
escape-rate equalities are automatic because Theta fixes ports. Finally,
baseline generalized detailed balance gives

    w_x q_Theta(x),b = w_b q_bx,

which makes (1) and (2) equivalent. For alpha=0, Q^u is simply a row-wise
time change and paired escape rates are scaled by the same factor.

### Finite control families

An open continuum of field values is unnecessary for this algebraic
implication. Baseline plus one nonzero independently addressed field at
each port gives m independent equations for the m coefficients in (3).
More generally, m control vectors whose rows

    [exp(alpha u_b)-1]_(b in B)

span R^m suffice. One scalar control with distinct fixed port amplitudes
can generate such a family. These are conditions on a common microscopic
control law, not microscopic rates acquired merely by observing m runs.

For a general finite control feature map phi(x), even under Theta, the
same argument says that outgoing rates from x and Theta(x) must have the
same total into every class of states with the same feature vector.
Distinct exponentials separate the feature classes. Thus the equilibrium
condition concerns the classes the control can distinguish.

## 3. A parity-independent CP consequence at the controlled boundary

Let A_bx=w_b q_bx be baseline port-entry flux and D=diag(w_I). The hidden
excursion density at zero duration is

    K(0)=F_BI Q_IB.

If the family in Theorem 1 remains generalized equilibrium under its
nonzero-alpha port controls, (2) implies Q_IB=D^-1 A^T. Therefore

    K(0)=A D^-1 A^T,

which is completely positive. This conclusion allows arbitrary hidden
dimension and arbitrary hidden parity. It does not require a rate ceiling.

Consequently, the previously acquired non-CP baseline kernel is
incompatible with a common equilibrium explanation satisfying this
particular robust-control contract. The additional premise is substantive:
it specifies which microscopic rates change and requires genuine frozen
equilibrium after a conservative field change. The passive record has not
acquired that premise.

Only K(0) is asserted CP here. Ordinary reversibility of the hidden
generator does not follow from (2); an odd internal dynamics can retain
nontrivial time-dependent structure. The old all-even CP theorem for every
time bin cannot simply be imported into this enlarged model class.

### Exact sharpness: robust conservative controls still permit non-CP late kernels

There is a nine-state counterexample to any stronger all-time CP claim.
Start with three ports b_i and three hidden states x_i, i modulo 3, all
weights one. Give b_i <-> x_i symmetric flow epsilon>0. Give the hidden
cycle x_i -> x_(i+1) rate r>0 and no reverse hidden edges. These flows are
stationary. Apply the exact port-preserving parity construction, producing
three ports and six hidden states. Boundary edges are now ordinarily
balanced, so Theorem 1 makes every frozen symmetric port tilt generalized
equilibrium. Let C be the cyclic permutation matrix. The native kernel is

    K(t)=epsilon^2 exp(-epsilon t)
         [exp(r(C-I)t)+exp(r(C^T-I)t)]/2.

It is reciprocal and has K(0)=epsilon^2 I. On the two-dimensional
subspace orthogonal to (1,1,1), its eigenvalue is

    epsilon^2 exp[-(3r/2+epsilon)t] cos(sqrt(3)rt/2).

At t=2pi/(sqrt(3)r), this is strictly negative. A sufficiently small
positive-duration bin around that time is also non-PSD, hence non-CP.
Thus robust, independently addressed conservative port tilts do not
restore the all-even bin certificate when odd interior dynamics remain
admissible. The instantaneous matrix conclusion is sharp in time.

## 4. Exact control equivalence for departure-only modulation

Consider any bounded, predictable positive port multipliers c_b(t), allowed
to depend on the previously observed native record. Multiply all outgoing
rates from port b by c_b(t), and leave all hidden rates unchanged. Compare
two models that have the same native baseline law and the same singleton
port escape rates lambda_b. Relative to baseline, a microscopic path has
likelihood ratio

    R_c = product_(port departures k) c_bk(t_k)
          times exp{sum_b integral 1_(X_t=b) lambda_b[1-c_b(t)] dt}.

Every factor is measurable from the native port record. The same
likelihood ratio therefore tilts both observed baseline laws. They remain
identical under every such protocol, including feedback and adaptive
port resets. Standard nonexplosion/integrability conditions apply; bounded
controls on finite horizons suffice.

Apply this to the exact port-preserving parity completion. Its baseline
native law, lambda_b, port singleton states, and total stationary mass
agree. Thus no native clock experiment in this class can distinguish the
two explanations. For every frozen field c_b=exp(-u_b), its equilibrium
weights are w_x exp(u_x), with unchanged hidden weights. No additional
slow hidden switch is needed.

This is an instance of a general statistical principle: observational
equivalence survives interventions whose change-of-measure density is
the same measurable function of the acquired record. Girsanov's formula
provides the mechanism here; it is not a new likelihood-ratio theorem.
The substantive application is the closure of the exact odd completion
under an entire native control interface.

## 5. What symmetric tilts additionally need to predict

For alpha=1/2, the jump part of the microscopic likelihood ratio is

    exp{(1/2) sum_jumps [u_destination(t)-u_source(t)]}.

When u is supported on resolved ports, this factor is native-record
measurable. The port holding correction is also determined by port clocks
and observed direct-port rates. The hidden holding correction contains

    exp{-sum_b integral_(X_t in I)
                  q_Xt,b [exp(u_b(t)/2)-1] dt}.               (4)

The needed extra record is therefore the hidden return-hazard exposure
measure, jointly distributed with the native record:

    R_b(dt)=1_(X_t in I) q_Xt,b dt.

Baseline entrance, exit and duration data do not automatically reveal
this path-dependent measure. If its joint law were independently acquired,
(4) and the observable factors would predict the complete controlled law
without identifying every hidden state. Acquisition of that joint law is
an additional information interface, not supplied by writing the formula.

For piecewise-constant fields, the corresponding unobserved insertions are

    A exp(Q_II t0) D_b1 exp(Q_II t1) ... D_bk exp(Q_II tk) Q_IB,
    D_b=diag(q_xb : x in I).

The baseline kernel gives only the k=0 family. Time-varying controls probe
ordered multi-time insertions, which can distinguish dynamics with the
same passive kernel. This is conventional Feynman-Kac machinery applied
to an explicit missing record. No low-variance reuse, sampling speedup,
or free acquisition is claimed.

The particular odd completion may still reproduce a target's controlled
law while ceasing to be equilibrium under the control. These questions
must be separated. The example below has exactly that property.

### An exact intervention-complete record at this interface

There is a precise sufficiency-and-necessity statement. Fix a finite
horizon, a known initial port, the complete native record Y, and common
port clocks/direct-port rates. Let two finite CTMC models have the same
baseline law of Y and obey the same symmetric-tilt rate rule. Then the
following are equivalent:

1. Their observed laws agree under every bounded deterministic
   piecewise-constant port field u(t).
2. Their conditional laws of the vector measure (R_b)_b, given Y, agree
   almost surely under the common baseline law.

Either condition also implies equality under bounded controls adapted to
the observed history. This does not assert that R has been acquired.

**Proof.** Write the observed density under u relative to the common
baseline law as

    dP^u_Y/dP^0_Y = G_u(Y)
        E[exp{-sum_b integral phi_b(t) R_b(dt)} | Y],
    phi_b(t)=exp(u_b(t)/2)-1,

where G_u is the common, strictly positive native-record-measurable jump
and port-hold factor derived above. Equality of the conditional measure
laws makes every displayed density equal, also when the field is an
observed-history-dependent functional.

Conversely, equality of all controlled densities gives equality of these
conditional Laplace functionals after division by G_u. Nonnegative bounded
piecewise-constant phi are allowed, using u=2 log(1+phi). They determine the
law of the positive finite vector measure R. More formally, a countable
class of rational time intervals and rational nonnegative amplitudes
fixes a common full-measure set on which all finite-dimensional Laplace
transforms agree; uniqueness gives the conditional measure law. Finite
state spaces make the exposures finite on finite horizons. This proves
the equivalence without requiring hidden state labels to match.

Thus the additional information is an explicit path measure, rather than
an unspecified demand for the whole hidden generator. It can nevertheless
be infinite-dimensional and expensive to acquire. No finite-rank closure
or universal acquisition advantage follows from the theorem. The proof
combines established change-of-measure and Laplace-uniqueness machinery;
the new object here is its exact specialization to the declared native
control interface.

### A passive-equivalent pair separated by one static symmetric tilt

Take the earlier nonuniform three-state generator

    Q=[[-3,2,1],[1/2,-3/2,1],[2/3,1/3,-1]],
    w=(1,2,3),  B={0}.

Q and its stationary reverse Q* have identical full one-port native laws.
Their baseline hidden-duration transform is

    Phi(s)=[(5/9)s+7/6]/[s^2+(5/2)s+7/6],

and both port holds are Exp(3). Apply the same symmetric tilt with
exp(u_0/2)=2. Their hidden-duration transforms become respectively

    Phi_+(s)=[(10/9)s+3]/[s^2+(11/3)s+3],
    Phi_-(s)=[(10/9)s+3]/[s^2+(23/6)s+3].

At s=1 these are 37/69 and 74/141, differing by 37/3243. The port-preserving
parity completion has their average transform under this common tilt,
and therefore does not reproduce the original controlled law. The extra
hazard-exposure record is genuinely additional information. Because this
interface has only one port, each individual frozen event-time law remains
reversal symmetric; the failure is controlled prediction, rather than an
observable arrow of time at one frozen parameter.

## 6. One static control exposes a four-state example

Take ports 0,1 and hidden states +,-, all baseline weights one. Set p=3/4,
q=1/4. The nonzero rates are

    0 -> + : p,     0 -> - : q,
    1 -> + : q,     1 -> - : p,
    + -> 0 : q,     + -> 1 : p,
    - -> 0 : p,     - -> 1 : q.

All baseline escape rates equal one. Theta fixes 0,1 and exchanges +,-,
so the source itself is generalized equilibrium under that abstract
parity. Its native kernel is

    K(t)=exp(-t) [[2pq,p^2+q^2],[p^2+q^2,2pq]],

and is reciprocal. Its ordinary all-even entropy is positive. This is
not a newly identified physical equilibrium system; it is an exact CTMC.

Apply the symmetric tilt with exp(u_0/2)=a=2 and exp(u_1/2)=b=1. Then

    lambda_0=1/2,  lambda_1=1,
    lambda_+=a q+b p=5/4,
    lambda_-=a p+b q=7/4.

The source's parity partners now have unequal escape rates. Its stationary
distribution is (52,17,19,11)/99, so it is not parity symmetric either.
The long-time relative-entropy rate against this parity reversal is 4/99;
the stationary mean jump log-ratio vanishes, and the escape-rate term
supplies the positive result. This is a concrete failure of the claim
that the tilted off-diagonal ratios alone establish equilibrium.

The port-reset excursion transforms are

    L_01(s)=b[p^2/(s+lambda_+) + q^2/(s+lambda_-)],
    L_10(s)=a[q^2/(s+lambda_+) + p^2/(s+lambda_-)].

Their exact values are

    L_01(0)=17/35,   L_10(0)=26/35,
    L_01(1)=3/11,    L_10(1)=46/99.

In any equilibrium explanation with these ports fixed by physical
reversal, stationary departure fluxes rho_i would make
rho_0 L_01(s)=rho_1 L_10(s) for every s. But

    L_01(0)L_10(1)-L_01(1)L_10(0)=16/693 != 0.

Thus no generalized-equilibrium completion of the controlled native law
exists under any hidden parity fixing the two ports. One static control
already suffices; a sophisticated time-dependent protocol is unnecessary
for this example. The four expectations are bounded reset statistics:
E_i[1_(next port=j) exp(-s tau)], with tau the hidden duration. Their
acquisition requires genuine controlled port trials, timing and resets.

### Strong conventional comparison

If the control is independently known to change only state energies by
-u, the equilibrium Gibbs occupancy ratio would be pi_0/pi_1=4. The
actual ratio is 52/17. Hence ordinary equilibrium susceptibility or Gibbs
occupancy checks also reject the model's proposed thermodynamic contract.
The waiting-law determinant is not claimed to beat this simpler method.
It does avoid assuming a supplied stationary preparation when known port
resets are available, but the fixture has no difficult mixing regime that
would establish an acquisition advantage.

Crucially, this experiment does not prove that the baseline source was
dissipative under its native physical reversal. It proves incompatibility
of the observed control response with the joint claim of equilibrium,
even fixed ports, and the stated conservative-control interpretation.
The field implementation may itself be injecting a kinetic drive.

## 7. Primary-literature scope

Baiesi, Maes and Wynants, "Nonequilibrium linear response for Markov
dynamics, I: jump processes and overdamped diffusions" (2009), Section
2.1 and the response derivation, explicitly use symmetric potential-rate
tilts and separate entropic from dynamical-activity response. Their stated
scope excludes inertial degrees of freedom. The rate formula and the
importance of escape-rate response are established machinery.
https://www2.pd.infn.it/~baiesi/papers/FDR_I.pdf

Lee, Kwon and Park, "Fluctuation Theorems and Entropy Production with
Odd-Parity Variables," PRL 110, 050602 (2013), emphasize that equilibrium
also requires stationary parity symmetry. The preprint and published
abstract were consulted. No novelty is claimed for that requirement.
https://doi.org/10.1103/PhysRevLett.110.050602
https://arxiv.org/pdf/1209.0543

Kolchinsky, Dechant, Yoshimura and Ito, "Generalized free energy and
excess/housekeeping decomposition in nonequilibrium systems: From large
deviations to thermodynamic speed limits," PR Research 8, 023025 (2026),
Appendix B, explicitly retains the escape-rate contribution for odd
variables and explains why conservative jump forces alone need not give
equilibrium. This directly blocks any broad novelty or physical-validity
claim based only on noticing the missing diagonal condition.
https://doi.org/10.1103/r48t-dghl

The constructed addition is narrower: an exact control-class criterion,
its parity-independent CP consequence at a resolved boundary, and the
closure of the port-preserving completion under all native departure-clock
protocols. A comprehensive priority search for those combined statements
has not been completed.

## 8. Executable scope

`check_control_completion.py` passes 13 exact frozen-control checks,
12 exact departure-control transform comparisons, and 30 exact passive
and controlled transform checks for the one-port prediction pair. The
nine-state late-time negative eigenvalue also has a floating SciPy control;
its sign is proved analytically above. `CONTROL_COMPLETION_CHECKS.json`
contains the outputs and checker SHA-256. No native source was sampled,
redrawn, or operated, and no resource or hardware interface was acquired.
