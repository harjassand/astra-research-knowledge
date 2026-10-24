# Acquiring hidden hubs before routing two low-impedance driver channels

2026-10-24. New internal theorem candidate for an explicitly stipulated
instrument. Not physically acquired, independently reviewed, or established
novel. This changes and fully specifies the fixed-port model; it does not
silently treat that model's obstruction as absent. Older frozen sources remain
unchanged.

## 1. Actual interface, target, and paid resources

There are n=2d+2 labelled nodes. The unknown positive forest consists of two
unknown hubs with d leaves each, weights in [a,3a], and an optional hub edge
of known weight a. The task is connectivity only. Hubs, memberships and weights
are not supplied to the positive algorithm.

At an action choose an external voltage command x and a diagonal matrix of
series port resistances R. The actual internal potentials v and port currents
i obey the exact settled equations

    i=L v=R^-1(x-v),
    i=M_R(L)x,
    M_R(L)=R^-1-R^-1(L+R^-1)^-1R^-1.                  (1)

Acquire **all n currents** with independent N(0,sigma^2) scalar readout noise,
independent between actions. Noise is stipulated unchanged when driver routing
changes; no physical amplifier is asserted to achieve this. There are n
ordinary ports, each with fixed resistance

    r0=1/(128a).

At most k=2 ports per action can instead be connected to the two routable
low-impedance channels. Their selected resistance can be

    r1=1/[128a(d+1)].                                 (2)

The positive protocol uses only external commands 0 or A=1/2, from two common
voltage rails. Their actual contrast is supplied/calibrated; independent
unknown per-terminal command offsets are not included. Series switch/lead/
source resistance must all fit the stated R bounds. A common shift of both
rails is immaterial. This is a concrete control requirement, not achieved
calibration. Resistance routing and future commands may use acquired data.

Charge every actual repeated action and all n scalar readouts. The external
command budget is pathwise sum_t x_ti^2<=B for each i. The two selected
channels require impedance O(1/(an)), current capacity O(an), routing to any
label, and O(n) available physical terminal connections. Those resources are
not constant in n merely because their channel count is two. Full settling,
readout duration, rail stability, switch resistance, sensor independence and
calibration are instrument premises. No device, hardware cost, or energy in
Joules has been acquired or inferred.

## 2. Positive acquisition protocol, with finite response encodings

Let delta in (0,1/2), and suppose

    d>=131,   d>=8 ln(16/delta).

Set

    K=max{1,ceil[8(sigma^2/a^2) ln(16n/delta)]},
    T=max{1,ceil[128(sigma^2/a^2) ln(4/delta)]},
    q=K+T.                                           (3)

**Phase I.** Use only ordinary r0 ports. Draw n independent fair bits b_i,
prepare the same command x_i=A b_i for K actual actions, acquire all n currents
each time, and average each vertex's acquired current. Choose the two largest
absolute averages as the hubs; order them deterministically by label.

**Phase II.** Route the two low-impedance channels to the acquired hubs U,V.
Set x_U=A and every other command to zero for T actual actions. Average the
acquired V-current and declare connected if it is below -aA/2=-a/4.

Finite encodings may be included as follows. Round each scalar current
readout to a grid of step a/8, with error at most a/16 absent clipping. Take
an encoding range at least

    H=A(3ad+a)+sigma sqrt[2 ln(4nq/delta)],             (4)

rounded outward to that grid. Encode the signed grid index. This uses

    ceil log2[2 ceil(8H/a)+1]

bits per scalar. Current means in either phase have magnitude at most
A(3ad+a), because actual potentials lie between the two command rails and
weighted node degrees are at most 3ad+a. A Gaussian union bound makes any
clipping probability at most delta/2 over all nq readouts. The margins below
already allow the rounding error.

## 3. Proof that Phase I actually acquires the hubs through finite ports

For common r0, write g=1/r0, beta=r0a=1/128, and
F=(I+r0L)^-1. The inverse is entrywise nonnegative: if a column had a negative
minimum entry, its equation (I+r0L)z=e_j would have a negative left side at
that minimum, a contradiction. Also F1=1 and F is symmetric. Hence

    M=(1/r0)(I-F)

is itself a positive weighted Laplacian. At a row driven by a binary command,
all its nonzero current terms have the same sign. Moreover M<=L in positive
semidefinite order, so every leaf's diagonal is at most 3a and its absolute
current at most 3aA.

Let h be a true hub and l one of its own leaves of weight w_l. Its leaf
equation gives

    F_lh=[r0 w_l/(1+r0w_l)]F_hh,
    -M_hl=[w_l/(1+r0w_l)]F_hh.

Eliminate the leaves in L+gI. The diagonal inverse at h is bounded below by
the reciprocal of its diagonal before eliminating the other hub. Thus, with
theta in {0,1},

    F_hh >= g/[g+sum_l w_l/(1+r0w_l)+theta a]
          >= g/[g+3ad/(1+3beta)+a].

Since d>=131 implies g+a<=da/(1+beta), it follows that for every own leaf

    -M_hl >= g/(4d).                                 (5)

Conditional on the hub's bit, the number of its d own leaves with opposite
bit is Binomial(d,1/2). Except with probability exp(-d/8) it is at least d/4.
On this event the hub's absolute current is at least

    A(d/4)[g/(4d)]=A/(16r0)=8aA.                     (6)

The other hub and every additional effective edge can only add a term of
the same sign. The two binomial failures together cost at most delta/8 by
the d condition. The K-averaged independent sensor errors all have magnitude
at most aA except with probability delta/8, by (3). Quantization contributes
at most aA/8=a/16 to an average. Thus acquired hub averages have magnitude
at least (8-1-1/8)aA, while every leaf's at most (3+1+1/8)aA. The true hubs
are strictly the two largest. This uses actual finite-port data; no topology,
degree, weight-fit, or ideal Laplacian-action oracle has been used.

## 4. Proof of the final acquired core test

Condition on a correct hub pair. Give each hub conductance g_h=1/r1, and keep
ordinary ports at the leaves. Put

    S_h=sum_{l at h} w_l/(1+r0w_l) <=3ad,
    G_h=g_h+S_h.

With the hub edge present, the exact 2-by-2 circuit Schur system gives

    i_V=-aA g_U g_V/[G_U G_V+a(G_U+G_V)].              (7)

With it absent i_V=0. Since g_U,g_V>=128a(d+1), the denominator in (7) is at
most g_Ug_V(1+3/128)^2. Therefore

    |i_V| >= aA(128/131)^2 >=7aA/8.                  (8)

At threshold -aA/2, after the aA/8 quantization allowance, either hypothesis
has a noise margin at least aA/4=a/8. The T-averaged fresh Gaussian noise
therefore errs with probability at most exp[-T a^2/(128sigma^2)]<=delta/4.
It is independent of Phase I hub selection. Combining Phase I failure
delta/4, final-test failure delta/4, and all clipping delta/2 proves total
worst-case error <=delta for **every fixed promised input**.

The actual action count is q=K+T=O((1+sigma^2/a^2)log(n/delta)); the external
row budget is at most B=(K+T)/4. Every repeated sample is charged. There are
nq acquired scalars, O(nq) processing and O(n) working memory. No weight
estimates or subtracted fitted currents enter the controls. The largest
current/source capacity remains O(an) in Phase II; exact preparation via
the selected impedance (2) is an unacquired hardware requirement.

## 5. All-nonadaptive-routing obstruction on the same interface

We now allow a stronger nonadaptive competitor: any real commands satisfying
the same row budget B, arbitrary computation, and selected ports of ANY
positive resistance <=r0, rather than requiring equality to r1. At most k
ports are selected per action; every unselected port has r0. All commands
and all resistance choices are committed before data. Randomization is
independent of the unknown input. After commitment, freely reveal both hubs,
the full leaf partition and every leaf weight, strengthening the decoder.

For this lower use the subclass with all leaf weights exactly a and random
ordered hub labels/leaf partition, chosen independently of the design and
core bit. Let S be the union of all selected labels in the committed design.
Then |S|<=kq, and the probability that at least one hub ever belongs to S is
at most 2kq/n.

Condition on a fixed design and metadata for which neither hub is ever
selected. At one action let G=R^-1, K0=L0+G, b=e_U-e_V. Direct inversion gives

    M_R(L1)-M_R(L0)=c_R u_Ru_R^T,
    u_R=G K0^-1 b,
    c_R=a/[1+a b^T K0^-1b] <=a.                       (9)

This identity retains every leaf output. At a hub with ordinary conductance
g0=1/r0, each leaf's effective conductance is

    alpha_l=a/(1+r_l a) in [a/(1+beta),a].

The U-star part of u_R has hub entry g0/(g0+sum_l alpha_l) and leaf entries
alpha_l/(g0+sum_l alpha_l); the V-star has their negatives. Each star part
has l1 norm one. Uniformly over all selected leaf resistances,

    ||u_R||_1=2,
    ||u_R||_infinity <= C/d,   C=(1+beta)/beta=129,
    ||u_R||_2^2 <=2C/d.                               (10)

Consequently for any action's command,

    (u_R^T x)^2 <= ||u_R||_1 sum_i |u_Ri|x_i^2
                  <=(2C/d) sum_i x_i^2.

The complete conditional Gaussian transcript KL, on this metadata, is at most

    sum_t [c_R^2||u_R||_2^2/(2sigma^2)](u_R^T x_t)^2
       <=[2a^2C^2/(sigma^2 d^2)] sum_{t,i} x_ti^2
       <=2a^2 C^2 nB/(sigma^2 d^2).                   (11)

Use Pinsker on the metadata where no hub is selected, and the trivial TV
bound one elsewhere. Metadata and the committed seed have common laws under
both hypotheses. Averaging their conditional TVs gives

    TV(P1,P0) <= 2kq/n+(aC/sigma) sqrt(nB)/d.           (12)

The graph/labels are not chosen after the design. A uniform error <=delta
on the promised input family therefore requires

    2kq/n+(aC/sigma) sqrt(nB)/d >=1-2delta.             (13)

At fixed sigma/a, delta and k, with the positive protocol's allowed
B=O(log n), this implies q=Omega(n/k), while the adaptive protocol uses
O(log n) actual finite-port actions with k=2. This is an asymptotic matched
action separation **within the stipulated reconfigurable instrument**.
Its constants, particularly C=129, are conservative; no finite practical
advantage is thereby established. The lower grants arbitrary readout
precision and even post-design full metadata; the upper acquires its hubs.

## 6. Physical-resource questions that remain open

The gain/current-capacity scaling, two-channel routing network, all n current
sensors, shared rail accuracy, burden/switch resistances and stable settling
are part of the required interface. In ordinary conductance/voltage units,
the settled source power is x^T i=v^TLv+i^TRi. For binary external commands,
M_R<=L gives power at most A^2 sum_edges w=O(an) per action; a real duration
must multiply it to obtain energy. No duration or source efficiency has been
measured. A faster action is not automatically a reduction in physical Joules.

Unknown independent terminal voltage offsets can spoil inactive-current
nulling. The shared-rail architecture is precisely the proposed control
capability; it has not been replaced by independently noisy voltage-clamp
offsets without paying their effect. Current noise sigma is assumed stable
through the routing/gain change, including at O(an) dynamic range. A proposed
device must establish that observation law and its sampling/ADC costs, not
just its DC rank. Low-impedance feedback and burden compensation are ordinary
instrument techniques; no invention of those techniques is claimed.

No instrument test, procurement, external communication, or hardware
operation occurred. The result is a producer mathematical candidate with a
concrete acquisition and resource contract, awaiting independent proof and
instrument review. Priority: UNKNOWN. Physical: NOT_ACQUIRED. Practical:
UNKNOWN. Broad mission: NOT_ACHIEVED.
