# Predictive records, clock budgets and thermodynamic reversibility

29 October 2026, Brisbane. Complementary construction by the thermodynamic
alternative agent. All statements below concern finite stationary CTMCs,
positive stationary weights, and the ordinary time reversal in which every
state is even. Applying their entropy to a native physical system additionally
requires a correct physical reversal and the usual local detailed-balance
interpretation. No physical implementation is claimed.

## 1. Question and standing notation

The prior positive-completion theorem asks whether an oriented mean record
can be executed by a finite positive CTMC under clock ceilings. Here we ask
what stationary entropy production that execution necessarily entails.
This is a property of compatible implementations, not an estimate of the
unknown source's total dissipation from a mean prediction.

Let L=-diag(w)Q, total stationary weight W=sum(w), boundary B of size m,
interior I of weight V>0, and G=L_II. Keep the preceding record
(S,w_B,b_R,b_L,c), with c=w_I^T G^-1 w_I. Define

    d=b_R-b_L,
    F_ij=-S_ij  (i!=j),
    d_i,trace=sum_{j!=i}F_ij,
    a_i=w_i ell_i-d_i,trace,
    A=sum_i a_i.

Here ell_i caps the native port departure rate. A negative a_i is already
infeasible. Hidden departure rates are at most Lambda. These are fixed
calibrated clocks, not a freedom to rescale physical time.

The unnormalized stationary entropy production is

    E=sum_{x!=y} phi_xy log(phi_xy/phi_yx),
    phi_xy=w_x q_xy.

Terms with phi_xy>0=phi_yx make E infinite. The normalized dimensionless
rate is sigma=E/W; multiply by k_B for thermodynamic entropy units.

## 2. A mean record already witnesses some hidden irreversibility

**Proposition 1.** Every compatible stationary realization obeys

    E >= ||b_R-b_L||_1^2/(4c).                         (1)

This can be positive even when S is symmetric and all trace currents vanish.
It is an elementary specialization of time-reversal information inequalities,
not a new general thermodynamic uncertainty relation.

### Proof using native excursion path flux

Split a stationary path into its native port-to-port excursions, excluding
the hold at the initial port but retaining every interior hold and jump.
Direct port jumps have interior duration zero. Let nu be the finite intensity
measure of complete microscopic excursions and Rnu its path reversal.
For an excursion i,x1,...,xk,j with specified hidden holding times, the ratio
of its forward and reversed flux densities is

    w_i product(q_forward) / [w_j product(q_backward)].

The hidden survival factors cancel, and stationary weights telescope to the
product of edge-flow ratios phi_forward/phi_backward. Integrating the log
ratio over nu counts every stationary edge flux exactly once. Thus

    D(nu || Rnu) = E.

The measures have equal finite mass. The identity remains valid with infinity
when reciprocal support fails. Boundary holds must not be attached to the
wrong reversed excursion; doing so can generate spurious irreversibility.

For any port function f, let Z=(f(i)-f(j))*sigma, where sigma is the interior
duration. It is odd under reversal. Write p,q for densities of nu,Rnu.
The elementary inequality (p-q)log(p/q)>=2(p-q)^2/(p+q) gives

    E >= integral (p-q)^2/(p+q)
      >= 2 [integral Z dnu]^2 / integral Z^2 dnu.

The second step is Cauchy-Schwarz, using reversal oddness. By the prior
excursion identities, integral Z dnu=f^T d and
integral sigma^2 dnu=2c. Hence

    E >= (f^T d)^2/[c osc(f)^2].

The entries of d sum to zero. Optimizing over 0<=f<=1 gives (1).
This proof uses the exact supplied record; it does not acquire it statistically.

### Finite-entropy support constraint

Finite E requires reciprocal microscopic support. Every positive-duration
excursion i to j then has a reverse excursion j to i with positive density.
Consequently its residence matrix must satisfy

    M_ij>0 iff M_ji>0.

In particular supp(v_R)=supp(v_L). The previous sharp two-port record
v_R=(1,0), v_L=(0,1) cannot have a finite-entropy exact realization under
this reversal, regardless of its state count or clock allowance. Its positive
CTMC realizations remain mathematically valid; finite entropy was not a prior
hypothesis. A physical irreversible-transition idealization has an additional
thermodynamic limit.

With unrestricted clocks, a zero-entropy realization exists exactly when S is
symmetric and b_R=b_L (besides the prior nonnegativity and mass conditions).
Necessity follows from detailed balance. Sufficiency follows by the existing
reversible leaf construction: a leaf of mass v_i and conductance (V/c)v_i
at each active port gives sum_i v_i^2/[(V/c)v_i]=c.
This zero-entropy characterization does not impose the clock ceilings below.

## 3. A dissipation lower bound from small native return budgets

**Proposition 2.** Set H=V^2/(2c). If sqrt(m Lambda V A)<H, every compatible
finite-entropy realization satisfies

    E >= 4H log[H/sqrt(m Lambda V A)].                 (2)

If A=0 and V>0, every compatible realization has infinite E. In particular,
at a fixed nonzero predictive record and hidden clock ceiling, allowing the
total native return budget to tend to zero forces entropy production to
diverge. State expansion does not remove this lower bound.

### Proof

Let a_ix=phi_ix and b_ix=phi_xi for i in B,x in I, and let h be total
boundary-to-interior flux. Stationarity at hidden nodes implies total
interior-to-boundary flux is also h. The positive-duration excursion measure
has mass h, first duration moment V, and second duration moment 2c. Thus

    h >= H=V^2/(2c).                                  (3)

Let r_i be the total stationary flux of excursions returning to the same
port. The exact trace identity gives

    r_i=w_i lambda_i-d_i,trace <= a_i.

An immediate i->x->i return has flux a_ix*b_ix/(w_x lambda_x). Since
lambda_x<=Lambda,

    sum_{i,x} a_ix*b_ix/w_x <= Lambda sum_i r_i
                                 <= Lambda A.         (4)

Write B_overlap=sum_{i,x}sqrt(a_ix*b_ix). Cauchy-Schwarz first over ports
at a fixed hidden state, then over hidden states, yields

    B_overlap^2 <= m V sum_{i,x} a_ix*b_ix/w_x
                   <= m Lambda V A.                  (5)

For h>0, the arrays P_ix=a_ix/h and Q_ix=b_ix/h are probabilities. Boundary
edge entropy is h[D(P||Q)+D(Q||P)]. Jensen's inequality gives
D(P||Q)>=-2log(sum sqrt(PQ)), and the reverse gives the same bound. Other
unordered edges have nonnegative entropy contributions. Therefore

    E >= 4h log(h/B_overlap).

When B_overlap<=sqrt(m Lambda V A)<H<=h, the last expression is increasing
in h and decreasing in B_overlap. Substituting (3) and (5) proves (2).
For A=0, positive h is incompatible with positive reciprocal boundary flows,
so finite E is impossible. This also proves the infinite statement directly,
without assigning a logarithm to zero as a limiting argument.

The bound is sufficient as a lower certificate, not claimed to equal the
minimum entropy over all compatible completions. It uses m rather than a
possibly sharper incidence-dependent factor. The two elementary information
inequalities and moment argument are conventional ingredients.

## 4. A fixed record whose finite-rate thermodynamic cost diverges

Take ports 0,1 and hidden states a,b, all with stationary weight 1. Around
the four-cycle 0->a->1->b->0 put clockwise flow alpha=1-beta and reverse
flow beta, where 0<beta<=1/2. Add a symmetric direct 0<->1 edge with flow
2 alpha beta in each direction. Exact elimination gives, for EVERY beta,

    S=[[1,-1],[-1,1]], w_B=(1,1),
    v_R=v_L=(1,1), c=2.

Every hidden departure rate is exactly 1. Every port departure rate is
1+2 beta(1-beta), so its spare flux is 2 beta(1-beta). Total mass is W=4.
The unnormalized entropy is

    E_beta=4(1-2beta) log[(1-beta)/beta].               (6)

It vanishes at beta=1/2. It diverges logarithmically as the port ceiling
decreases to 1. Proposition 2 gives

    E >= 2 log[1/(16 beta(1-beta))]

whenever beta(1-beta)<1/16, so it proves the same logarithmic order for
EVERY realization with this record and those clock ceilings. The displayed
four-state construction is within a factor two in the leading logarithmic
coefficient of this lower bound. No claim of an exact optimal curve is made.

Thus the thermodynamic burden here is neither a large mean nor a growing
state count: the same four-state mean record remains fixed. It is the lack
of native return flux compatible with a fixed hidden speed. At the limiting
port ceiling 1 a positive directed realization exists, but every exact
realization has infinite entropy under the stated reversal.

## 5. Opposite direction: identical complete boundary laws do not upper-bound EP

Use ports 0,1 of weight 1 with a symmetric direct flow 1/2. Attach three
hidden states of weight 1/3 each to port 0, each with incoming flux 1/3
and exit rate 1 to port 0. Among the three hidden states add clockwise
rate p=1/2 and counterclockwise rate q in (0,1/2].

The internal cyclic motion is balanced. Since the exit hazard is exactly
1 at every hidden state, the entire interior duration is exponential(1)
independently of p,q and always exits at port 0. The native port clocks
are (3/2,1/2). Hence the FULL native port event/holding/excursion-time law
is identical for every q, not merely the mean record. It has

    S=[[1/2,-1/2],[-1/2,1/2]], v_R=v_L=(1,0), c=1.

There are always five states, and every departure rate is at most 2.
Nevertheless

    E=(1/2-q)log[(1/2)/q]

ranges from zero to arbitrarily large values as q decreases to zero. The
missing resource is the hidden affinity / reverse-rate precision; a clock
ceiling controls neither. This demonstrates why a positive mean representative
cannot be interpreted as reconstructing the original source's dissipation.
It also shows that even complete baseline boundary laws cannot answer every
thermodynamic or control query. Native hidden observations or additional
intervention-coupled records must supply the missing information.

## 6. Opportunity judgement and prior art

This alternative has a concrete explanatory payoff: the class of compatible
positive implementations has a thermodynamic boundary not visible in state
count, clock ceilings separately, or trace currents. Equations (1)-(2) and
the fixed-record family are self-contained constructions, but their basic
information inequalities have established antecedents. Skinner and Dunkel
(2021) already optimize entropy over hidden models consistent with waiting
time moments. Van der Meer, Ertel and Seifert (2022) already establish waiting-
time entropy estimators and emphasize correct time reversal. Neither broad
waiting-time dissipation inference nor constrained hidden-model optimization
is a new program here.

The possible addition is a direct resource inequality in the previously
constructed calibrated mean record and native return budgets, including a
matching logarithmic-order fixed-record example. Full thermodynamic optimal
completion, finite physical affinities, robust acquisition of its inputs and
causal predictions under interventions remain open. Relative to the central
intervention-information attack, this is promising reusable capital but not
yet a larger universal learning or control capability.

See THERMODYNAMIC_SOURCES.md for exact reading scope, the existing Astra
N185 acquisition obstruction, and the distinction between acquired data and
these exact supplied-generator controls. No data were acquired in this branch.
