# A relative endpoint certificate uses a success-conditioned clock

13 October 2026. Internal restricted deduction and exact finite diagnostics.
The underlying committor, Doob transform and Feynman–Kac machinery are standard.
This applies them to the intake's rare-yield transfer failure. It does not prove
a new physical capture interface, inexpensive acquisition, or historical novelty.

The matter report correctly proves an adaptive absolute-error identity. The
following narrower, homogeneous finite-generator statement makes precise which
extra object can control relative rare yield. It must not be represented as an
already proved adaptive relative-error theorem.

Let E be finite transient states, T a target and B a bad absorber. An acquired
baseline committor q is strictly positive on E, q(T)=1 and q(B)=0. Let L be a
candidate time-homogeneous generator under which absorption occurs almost surely
and every transient state can reach T. Write h_L for its eventual target
probability. Define a target-only auxiliary generator G by

    G_xy=L_xy q(y)/q(x),   x in E, y in E union {T}, y!=x,
    G_xx=-sum_(y!=x) G_xy,
    v(x)=(Lq)(x)/q(x).

All transitions to B vanish in G. The positivity/path assumptions make its
target-hitting time tau_T finite almost surely. There is an exact identity

    h_L(x)/q(x)=E_x^G exp(integral_0^tau_T v(Y_s) ds).       (R1)

Proof. Let D_q=diag(q|E), L_E be the transient block and b=L_ET. Then

    G_E+diag(v)=D_q^-1 L_E D_q,
    G_ET=D_q^-1 b.

The original finite absorbing-chain hypothesis makes L_E stable. The positive
weighted arrival density integrates to

    integral_0^infinity exp[(G_E+diag(v))t] G_ET dt
      =-(G_E+diag(v))^-1 G_ET
      =D_q^-1[-L_E^-1 b].

The first expression is the finite-state Feynman–Kac expectation in (R1), and
the last is h_L/q. This supplies the needed convergence instead of silently
dropping an exponentially weighted unfinished term. QED.

If a certified pointwise relative generator residual obeys |v|<=delta, then

    E_x^G exp(-delta tau_T)
       <=h_L(x)/q(x)<=E_x^G exp(delta tau_T).              (R2)

The right exponential moment, rather than the ordinary L-absorption time,
is a sufficient relative-error acquisition target. For example, an acquired
nonnegative w with w>=1, w(T)=1 and

    G w+delta w<=0 in E

gives E_x^G exp(delta tau_T)<=w(x) by stopped supermartingale reasoning and
Fatou's lemma. If also E_x^G tau_T<=b(x), Jensen gives the lower bound
exp[-delta b(x)]. These are sufficient checks, not free oracles; q, the tilted
rates, residuals and moment certificates must be acquired and verified. A small
absolute residual or a bounded unconditioned duration alone does not supply them.

## Exact explanation of the rare-branch counterexample

Use the matter report's unit-rate line x0,...,x_(n-1),T, with a unit failure edge
from every transient state to B. Let q=h_1 be its baseline committor and multiply
all failure rates by c in (0,1). Since only transitions to q(B)=0 change,

    L_c q=(1-c)q,       v=1-c.

The auxiliary G is independent of c: it is the unit-failure baseline chain
conditioned on eventual success. Thus

    h_c(x)/h_1(x)=E_x^G exp[(1-c)tau_T].                  (R3)

With the report's recurrence u_0=1,u_1=1+c,
u_(j+1)=(2+c)u_j-u_(j-1), h_c(x0)=1/u_n(c). Differentiating (R3) at c=1 gives

    E_x0^G tau_T=[d/dc log u_n(c)]_(c=1)
                =n/sqrt5+O(1).

The last asymptotic follows from u_n=A_c lambda_+(c)^n+B_c lambda_-(c)^n and
d log(lambda_+)/dc=1/sqrt(c^2+4c). On the physical unconditioned chain the
constant failure hazard instead gives E_Lc tau<=1/c, independent of n.

Consequently a globally small relative residual v=1-c still accumulates along
long, exponentially rare successful paths. This explains how the source's
well-conditioned kinetic operators can fail a dimension-independent relative
capture guarantee. A successful relative certificate needs a controlled
success-conditioned clock or an equivalent endpoint-specific object; the
ordinary fast failure/absorption clock cannot replace it.

The submitted spectral law realizes c=4100/4181 in the report's stated finite
kinetic graph. This result concerns that graph's first-hit functional. It does
not create an irreversible quantum absorber, retained material endpoint, or a
uniform finite-epsilon/large-system theorem.

## A finite phase-flip construction for the selected endpoint

The same graph also supplies a positive, task-specific response to the false
rate-to-yield transfer. This is a construction in the submitted finite kinetic
and phase-actuation model, not an engineered retained endpoint.

Use the bounded-degree leaf realization in the matter report: path vertices and
T have D=0; each bad leaf B_i has D=2; eta=1; squared hopping amplitudes are1/2
on path/target edges and2 on failure edges. Keep the coherent D fixed. Let gamma
be the total linewidth at gap2, while gap0 retains linewidth1. The slow-time
rates are then

    q_path=1,   q_failure=c_gamma=4gamma/(gamma^2+4).

Instead of maximizing the failure rate, suppress it by increasing gamma.
An exactly finite-rate common phase controller uses kicks u=+/-pi/2, each sign
with probability1/2, at total native Poisson rate r. Its characteristic exponent
is `phi(w)=r[1-cos(pi w/2)]`, so phi(0)=0 and phi(2)=2r. Choose

    r=(gamma-1)/2,   gamma>=1.

This is an allowed symmetric compound-Poisson phase semigroup acting through
the same actual D. The ideal kicks are instantaneous; no finite-duration
implementation theorem is thereby obtained.

Remove the failure edges temporarily. The unit-rate reflecting path from x0 to
T has mean first-hit time `mu_n=n(n+1)/2`. Reintroducing a constant failure
hazard c_gamma gives

    h_gamma(x0)=E exp[-c_gamma tau_T^path]
               >=1-c_gamma mu_n,
    E tau_absorb<=mu_n.

Since c_gamma<=4/gamma, choosing a target error zeta in (0,1) and

    gamma>=4mu_n/zeta=2n(n+1)/zeta

ensures h_gamma(x0)>=1-zeta. The target and bad vertices still need a separate
physical absorbing/readout/retention interface. The result describes only the
finite kinetic first-hit functional and does not close that missing interface.

### Time, pulse and comparator accounting

Here mu_n is in slow time `tau=epsilon_hop^2 t`, not native laboratory time.
Conditional on realizing the ideal reduced stopping operation, the native
duration ledger is at most `mu_n/epsilon_hop^2` per trial. Keeping the Poisson
controller on for that duration charges expected pulse count at most

    r mu_n/epsilon_hop^2 = O(n^4/[zeta epsilon_hop^2]),

and absolute phase action `(pi/2)` times that count. If independent fresh trials,
failure detection and resets are separately acquired, repetition until success
adds a factor at most1/(1-zeta), plus all preparation/readout/reset costs.
These are conditional model ledgers, not measured completion times or a proof
that a quantum first-hit instrument preserves the reduced rates. Compiling D
into individual site operations can add O(n) spatial operations per kick; native
common modulation is an input promise.

With a bounded native multiplier |a(t)|<=a_max, a kick of action pi/2 needs
duration at least pi/(2a_max). Growing r therefore cannot be called free
bandwidth. Pulse overlap, scheduling, hopping during the pulse, calibration,
switching work, heating and the actual sink dynamics require a new error and
cost account. A small r times pulse-duration is not itself a sufficient proof.
For every fixed n and selected finite gamma the source weak-hopping limit may
be taken first. No joint n, gamma, pulse-duration and epsilon_hop scaling limit
has been established.

A stronger native comparator is essential. If the same actual D actuator may
also statically rescale the coherent Hamiltonian to aD without violating the
scientific task, baseline dephasing alone gives

    q_failure,static=4/(1+4a^2),   q_path,static=1.

The same elementary yield bound reaches1-zeta when
`a^2>=mu_n/zeta-1/4`, with amplitude O(n/sqrt(zeta)) and no repeated-kick
overhead. Its holding/control energy, amplitude limit and changed coherent
Hamiltonian must be charged. The phase-flip construction is therefore a useful
fixed-coherent-D capability statement, not a demonstrated operational advantage
over the full actuator set. A physical reason to forbid static rescaling cannot
be invented merely to rescue the noise proposal.

The supplied energy separation of desired and failed branches is also essential.
It was constructed in this graph, not discovered or acquired in a material.
The new mathematical target is selective suppression of low-committor channels,
which differs from simultaneous maximization of every conductance.
