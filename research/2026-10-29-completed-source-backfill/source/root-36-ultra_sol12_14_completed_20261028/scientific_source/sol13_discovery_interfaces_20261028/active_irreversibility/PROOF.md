# An active interface that separates stationary spectroscopy from ordered response

Status: a constructive continuous-family separation and an exact fixed-time
CTMC receiver are acquired. A new fluctuation theorem, controlled-HMM
learner, physical measurement or practical advantage is **NOT_ACHIEVED**.
The generic successful receiver is ordinary Crooks reciprocity. Priority
of the particular family and sharp one-pulse/two-pulse separation is UNKNOWN.

The operation investigated is a preprogrammed, cyclic change of one visible
energy level, followed by comparison with the reversed control schedule.
It requires no hidden point preparation and assumes no parity assignment
to the hidden coordinates. It does require a physically qualified energy
coupling and reverse protocol. Merely naming an input a potential is
insufficient; Section 8 gives an exact countercontrol.

## 1. What must actually be acquired

The mathematical equilibrium null has one fixed hidden state space, an
unknown fixed involution J, a visible emission h with h(Jx)=h(x), and a
dimensionless visible field u. Write g=1_{h=1}. Its equilibrium laws are

    pi_u(x)=pi_0(x) exp(u g(x))/Z_u,

and its constant-field kernels obey full generalized detailed balance

    pi_u(x) K_u(t;x,y)=pi_u(Jy) K_u(t;Jy,Jx).                    (1)

The displayed same-kernel equations assume a time-even background. If an
odd external parameter is present, its actual reversal requires a paired
reverse kernel and Gibbs law; (1) must not be imposed on the unchanged
kernel. No such odd external parameter is present in the numerical model.

The physical interface needed to use this null consists of:

- A known time-even readout h and an energy change
  E_u(x)-E_0(x)=-kBT u g(h(x)), including field scale and detector errors.
- A justified energy-only intervention: if the baseline is equilibrium,
  applying this control preserves microscopic equilibrium at each fixed
  field with the same physical reversal, including waiting-time dynamics.
- Actual reversal of the field schedule and every time-odd external
  parameter, or a justified absence of such unreversed parameters.
- Actual reversal-compatible baseline equilibrium preparation pi_0, or a
  quantified bound on its error obtained by justified relaxation. An
  arbitrary stationary law is insufficient, as Section 9 proves. Hidden
  point preparation is not an input.
- Observations at the switching times. Other trajectories must be charged,
  even when the receiver's selected event does not occur.

These are qualifications to acquire from device physics/calibration, not
facts inferred from passive reversal symmetry. In the supplied mathematical
family we compute the rates and preparation bounds. No physical apparatus,
label parity, energetic calibration or samples were acquired. Without the
energy-only qualification, a violation diagnoses the controlled family's
microreversibility failure; it cannot uniquely attribute that failure to
baseline physical dissipation. No entropy-production rate is inferred.

## 2. Ordinary reciprocity receiver, with arbitrary hidden parity

For fields u_1,...,u_m, durations t_1,...,t_m and hidden boundary states
x_0,...,x_m, compare

    p_F=pi_(u1)(x0) prod_l K_(ul)(tl;x_(l-1),x_l)

with the process starting from pi_(um), using reversed field/duration order
and the reversed hidden states Jx_m,...,Jx_0. Multiplying (1) gives

    p_F/p_R=prod_(l=1)^(m-1) pi_(ul)(x_l)/pi_(u(l+1))(x_l)
           =(Z_(um)/Z_(u1)) exp[-sum_l (u_(l+1)-u_l)g(x_l)].      (2)

This is the ordinary cyclic-work/Crooks argument, not a new theorem. In
a closed protocol u_1=u_m, and on an observed event with g=0 at every
switch, (2) is exactly one. Summing over every compatible hidden trajectory
therefore gives

    P_F(observed event)=P_R(reversed observed event).             (3)

This conclusion holds for every hidden dimension and unknown J satisfying
the qualified null. The selected event has zero control work; the protocol
does work on other trajectories. There is no feedback or uncharged
postselection. Known cyclic endpoints avoid a free-energy measurement.

Primary prior: [Crooks 1999, Sections II–III](https://threeplusone.com/pubs/Crooks1999a.pdf)
explicitly uses physical reversal, including momenta and magnetic fields.
Nonlinear response and kinetic/escape-rate contributions are also prior:
[Basu, Kruger, Lazarescu and Maes](https://arxiv.org/abs/1410.7450).

## 3. A positive-rate six-state family

There are four internal states with visible label 0, and two uniquely
labeled markers 1 and 2. Define internal vectors

    x=(-3,-1,1,3),  u=(1,-1,-1,1),  v=(1,-3,3,-1).

They satisfy u,v perpendicular to both 1 and x, u dot v=0,
||u||^2=4 and ||v||^2=20. For parameters

    a>3|b|>0,       c>6|gamma|>0,

let the symmetric generator S have internal off-diagonal rates c, marker
rates S_(i,4)=S_(4,i)=a+b x_i and S_(i,5)=S_(5,i)=a-b x_i, and no direct
marker-marker edge. Its diagonal is minus its exit rate. Add the internal
circulation

    K=gamma(uv^T-vu^T),          Q=S+K.                          (4)

K is skew, has zero row/column sums, and all resulting off-diagonal
internal rates are positive because max_ij |u_i v_j-v_i u_j|=6. The ports
are positive too. Q is irreducible with uniform stationary pi=1/6.

Let V be the span of 1_internal, x, marker1 and marker2. S preserves V,
K annihilates V, and emissions preserve V. Consequently Q and Q*=Q^T
coincide with S on V, while V also reduces Q. Every stationary observed
finite-dimensional distribution, at arbitrary continuous observation
times, is exactly the same for Q and the ordinary reversible S. This is
an all-time/all-word statement from invariant-subspace algebra, not a
finite-window fit.

## 4. Static energy control and complete linear FDT

Put d=exp(u/2)>0 and D=diag(1,1,1,1,d,1). The specified rate-response law is

    q_ij(d)=q_ij D_j/D_i   (i!=j),       q_ii(d)=-sum_(j!=i)q_ij(d).
                                                                    (5)

This law is supplied to the model compiler; its physical realization is
unacquired. The stationary law is exactly

    pi_d=(1,1,1,1,d^2,1)/(5+d^2).                               (6)

Indeed K annihilates every emission function, including D1, so the Gibbs
stationarity condition derived in Section 8 holds. The same argument
works for any potential constant within emission classes.

Differentiate pi_(u+epsilon) Q_(u+epsilon)=0. With B the rate derivative,

    pi_u B=-pi_u diag(g) Q_u.                                  (7)

For any visible output f this gives the impulse response

    R_gf(t)=pi_u B exp(tQ_u) f
           =-d/dt E_(pi_u)[g(X0) f(Xt)].                       (8)

Thus every accessible linear FDT test passes, at every static field, for
all times/frequencies, not just a finite grid. With additional visible
potential channels, the same identity holds for each such channel.
At the baseline, all correlation and response curves equal those of S.
General response formulas are ordinary prior; see
[Baiesi, Maes and Wynants](https://arxiv.org/abs/0909.5306).

## 5. All static laws and every isolated constant pulse remain ambiguous

Use the basis H=(1_internal,x,u,v,marker1,marker2). Its physical stationary
Gram at field d, apart from the scalar 1/(5+d^2), is

    M0_d=diag(4,20,4,20,d^2,1).

Writing L_d=H^(-1)Q_d H, direct algebra gives

    M_d L_d=L_d^T M_d,
    M_d=diag(4,20,4,rho_d,d^2,1),
    rho_d=20[3b(d-1)+20gamma]/[3b(d-1)-20gamma].                 (9)

One way to check the only changed edge is to use

    x^2=5*1+4u,    x*u=(4/5)x-(3/5)v,    x*v=-3u,
    K*u=-4gamma*v,       K*v=20gamma*u.

The internal block is the baseline internal operator minus
(d-1)diag(a+b x). Its u,v coordinate entries are
3b(d-1)+20gamma and 3b(d-1)/5-4gamma. Equation (9) symmetrizes this pair;
all other coordinate pairs retain their physical weights.

M_d need not be positive. It is a bilinear algebraic device, not a physical
parity or a positive hidden realization. It commutes with emissions and
agrees with M0_d on V, including the constant function. Taking adjoints in
this bilinear form proves reversal symmetry of every stationary observed
word of Q_d, at arbitrary observation times. The exceptional denominator
in (9) causes no gap: each fixed word identity follows for generic d and
extends by continuity of the actual finite-state semigroup.

There is an equally informed parity comparator at every field:

    R_d=diag(Q_d,Q_d*),     pi_hat_d=(pi_d/2,pi_d/2),
    J swaps the two copies.                                   (10)

Here * uses pi_d. It is also the ordinary potential tilt of the single
baseline block generator diag(Q,Q*), because pi_d is stationary and K
annihilates emission functions. It has one fixed parity J, preserves
labels and satisfies full generalized detailed balance for every field.
At any fixed field the two observed laws in its blocks are identical by
static reversal symmetry. Hence (10) matches every static observed law of
Q_d, and (7)–(8) make all their linear response spectra identical too.

The twelve-state comparator is **reducible**, with canonical sector weights
1/2. Those weights are supplied; they cannot be obtained by relaxation
across disconnected sectors. No physical parity, ergodic device or sector
preparation is acquired. The irreducible six-state S remains the ordinary
baseline comparator, and its energy-tilted family satisfies (3) exactly.
Replica lifting is prior, not a new algorithm here.

The ambiguity is stronger than linear FDT. A single quench from any
stationary field e to a constant field d is obtained by multiplying the
stationary d path law by pi_e(X0)/pi_d(X0), a known emission function.
Therefore all such quench trajectories, at any amplitude, match (10).

**Isolated-pulse theorem.** Starting at the stationary baseline, an arbitrary
record containing one contiguous interval at one constant nonbaseline level
d, with arbitrary baseline observations before and after, is identical
between Q and (10). Thus one rectangular pulse, at any amplitude/duration,
cannot distinguish them. This does not cover a shaped pulse with multiple
levels or arbitrary nonstationary preparation.

Proof: In H coordinates put C_d=M0_d^(-1) M_d. Generically it is invertible,
commutes with emissions, fixes V, and

    L_d*=C_d L_d C_d^(-1).                                    (11)

The baseline past/future boundary vectors lie in V: V reduces both Q and
Q* and is emission invariant. Reweighting the left boundary from pi_1 to
pi_d also preserves V, because the ratio is an emission function. In any
within-pulse word, substituting (11) telescopes C_d through all emissions
and interval kernels. It disappears at both V boundaries. This proves
the identity for Q_d and Q_d* and hence their mixture. Exceptional d
follow by continuity. QED.

Consequently the whole stationary/single-quench/isolated-rectangular-pulse
interface is nonidentifying for this family, even with exact data. This is
not a claim about all possible active experiments or a physical equilibrium
realization of (10).

## 6. Two separated pulses: a continuous-family exact discriminator

For a uniformized discrete-tick implementation let P_d=I+tau Q_d, with tau
small enough that every used kernel is stochastic. Start from pi_1 and use

    fields=(1,d,1,d,d,1),    word=(1,0,0,0,0,0,2).

The reverse experiment reverses the fields and the word. All switches in
this event occur at label 0, so (3) requires equality under the qualified
null. Exact polynomial multiplication gives

    p_F-p_R=-256 gamma b^5(d-1)^3 tau^6.                       (12)

`derive_family.py` proves (12) with symbolic a,b,c,gamma,d,tau; the result
is not a fit. Positivity conditions in Section 3 leave an open parameter
family with nonzero signal whenever b*gamma*(d-1)!=0. This proves that two
separated rectangular pulses suffice, while Section 5 excludes one.
The signal is cubic in this field contrast for this receiver; no universal
claim about all lower-order response tensors is made.

The first exact example used a=c=1,b=1/4,gamma=1/12,d=2,tau=1/16:

    p_F=33057373/28991029248,
    p_R=33057409/28991029248,
    p_F-p_R=-1/805306368.

The ordinary reversible S control gives exactly zero. The twelve-state
parity comparator gives (p_F+p_R)/2 in both directions, by (2).
Equation (12) concerns actual discrete ticks, not fixed-time CTMC samples.
Section 7 separately acquires the latter.

For perspective, optimizing only this discrete receiver over nonnegative
rates, d>=1 and stochastic tau gives a sharp supremum |p_F-p_R|=1/236196.
To see this, increase |gamma| to c/6 and |b| to a/3; the latter increases
b^5/[3c+2a+(d-1)(a+3b)]^6 throughout that interval. Put r=c/a and use
tau<=1/(3c+2ad) at that boundary. The upper bound becomes

    (128/729) r(d-1)^3/(3r+2d)^6.

It is maximized at r=2d/15 and then d=5/2, giving r=1/3,tau=1/(6a).
The other exit-rate constraint 4a is smaller there. Strict positive
parameters approach the boundary maximum. This is a receiver-specific
signal optimization, not an information lower bound or a statement about
optimal control, all records or all active assays.

## 7. Actual fixed-time continuous dynamics, independently enclosed

The strict positive instance is

    a=1, b=33/100, c=1/3, gamma=11/200, d=5/2.

Use genuine kernels exp(t Q_d), not P_d ticks. The forward experiment has

    fields   =(1,d,1,d,1),
    durations=(1/4,1/4,1/4,1/2,1/4),
    word     =(1,0,0,0,0,2).

The reverse experiment uses reversed field/duration order and reversed
word. Both start from pi_1. The total duration is 3/2 model time units.
All four switches of the selected event occur at g=0; it has zero work.
Exact enclosures prove

    -700390315/10^16 < p_F-p_R < -700390314/10^16,               (13)

or -7.00390315e-8 < difference < -7.00390314e-8. The displayed individual
probabilities are approximately 0.00184854243482336 and
0.00184861247385481. They are not rare events silently conditioned to
probability one. The reversible S family gives exactly zero; the
canonical twelve-state comparator gives their average in either direction.

`certify_continuous.py` builds stochastic rational approximants to all six
required kernels (three for Q, three for S). With rate lambda=6,
P=I+Q_d/lambda is stochastic and

    exp(tQ_d)=exp(-z) sum_(k>=0) z^k P^k/k!,       z=lambda t.

Take degree 48. If E is the scalar partial sum and U the rational tail bound

    U=[z^49/49!]/[1-z/50],

the normalized rational matrix sum_(k=0)^48 z^k P^k/(k! E) is stochastic.
The true kernel is a convex mixture containing it with weight at least
E/(E+U); its row-TV error is therefore at most U/(E+U). A five-kernel event
probability has error at most the sum of these row bounds. Twice that sum
encloses the forward-minus-reverse difference. All intervals and rational
kernel matrices are saved in `CONTINUOUS_CERTIFICATE.json`.

`independent_taylor_replay.py` imports no producer module. It reconstructs
the literal six-state rates and encloses each exponential with the signed
Taylor series in Q_d, degree 80, using induced infinity-norm remainder

    U_T=[eta^81/81!]/[1-eta/82],       eta=t ||Q_d||_infinity.

It independently recovers (13), proves overlap with the producer intervals,
and builds the twelve-state adjoint comparator directly from the saved
rational kernels. Its forward/reverse probabilities are exactly the
target average. This is independent code by the same worker, not a separate
peer review or physical validation. The computational method is ordinary
uniformization/Taylor enclosure, not a new integration algorithm.

## 8. The escape-rate qualification cannot be omitted

Let a baseline generator Q obey generalized detailed balance with J and
pi, with pi J=pi, g J=g. Put D=diag(exp(u g/2)). The off-diagonal tilt (5)
can be written exactly as

    Q_u=D^(-1) Q D-diag(r),       r=D^(-1) Q D1.                (14)

Off-diagonal flux pairing with the candidate Gibbs law pi_u proportional
to pi D^2 is automatic. The **full** condition, including its diagonal,
is not. Direct multiplication gives

    (pi_u Q_u)_i = pi_i D_i [(Q*-Q)D1]_i /Z.                   (15)

Moreover, baseline generalized detailed balance and D J=J D imply
r_(Ji)=(Q*D1)_i/D_i. Thus the following are equivalent:

    pi_u stationary;
    (Q-Q*)D1=0;
    r_i=r_(Ji) for every i;
    full generalized detailed balance of Q_u with this J,pi_u.  (16)

Matching off-diagonal entropy-looking ratios does not acquire (16).
Holding times are part of the active physical interface.

An exact four-state countercontrol is the unit-rate directed cycle
0->1->2->3->0, parity J=(0 3)(1 2), labels (0,1,1,0), and uniform baseline
law. The baseline satisfies full parity detailed balance. At d=2 the
tilted exit rates are (2,1,1/2,1). Off-diagonal Gibbs pairing still holds,
but the Gibbs candidate (1/10,2/5,2/5,1/10) has stationarity defect

    (-1/10,-1/5,1/5,1/10).

The actual stationary law is (1/9,2/9,4/9,2/9). Even its observed label-1
mass is 2/3, rather than the candidate Gibbs 4/5.
`calibration_countercontrol.py` reconstructs these facts exactly. It is a
kinematic countercontrol, not a physically realized equilibrium device.

Our six-state family avoids this algebraic defect because its K annihilates
all emission functions. But that is supplied model information. An
experimenter observing only labels cannot assume it as a free calibration.
Physical energy-only control must independently justify the equilibrium-
preserving implication before a failure of (3) is attributed to baseline
dissipation rather than to the intervention itself.

## 9. Stationary does not mean reversal-compatible preparation

There is a second obstruction. In (10), the initial law (pi_1,0) is
stationary but not J-invariant. It reproduces Q's observations under
**every future control protocol**, at all orders, exactly. The canonical
half/half law used in (2) cannot be obtained by relaxation between the
disconnected sectors. Consequently active data alone cannot distinguish
baseline generator irreversibility from a parity-reversible generator
prepared in an unresolved odd sector. Stationarity of visible statistics
does not acquire the missing preparation condition.

This remains a finite-acquisition obstruction if irreducibility is required.
Add constant symmetric copy flips eta>0:

    R_(d,eta)=[ Q_d-eta I       eta I
                eta I          Q_d*-eta I ].                  (17)

It is irreducible, has canonical stationary law (pi_d/2,pi_d/2), full common-
parity detailed balance, and the same energetic tilt interface. Start it
in the + sector. Couple it to Q until its first copy flip. Over any total
elapsed duration H, even with bounded admissible adaptive visible control,
path-law TV is at
most 1-exp(-eta H)<=eta H. For any finite observation budget H and error
tolerance epsilon, rational eta<=epsilon/H gives such a countercontrol.
The + preparation is not globally stationary for eta>0; a finite waiting
time cannot certify that an unbounded slow hidden sector has mixed.
At baseline all visible observations still exactly match the source for
any sector weights with within-sector law pi_1, because V reduces both
copies. This holds even while those weights slowly change.

This is not a new lifting trick or an asymptotic nonidentifiability claim
at fixed eta. It identifies the particular missing acquisition: an actual
reversal-compatible equilibrium preparation or a justified uniform mixing
contract. Hidden point preparation was never granted. With both the
qualified control and preparation contracts, ordinary Crooks supplies a
useful active falsification without assuming every hidden coordinate even.
Without either contract, the broader baseline physical conclusion remains
UNKNOWN.
