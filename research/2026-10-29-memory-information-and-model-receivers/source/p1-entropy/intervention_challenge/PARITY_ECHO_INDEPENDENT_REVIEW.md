# Independent review: microscopic parity pulse and its precision contract

29 October 2026. This review addresses sections 4--5 of root's
`REVERSAL_INFORMATION_AND_INTERVENTION.md`, using its section 1 definitions.
The frozen source and hash are recorded separately. It does not re-audit
the earlier passive entropy, mean, clock, or reciprocal-completion theorems.

## Verdict

The exact midpoint-operation theorem is valid. The physical reversal of the
whole marked-pulse protocol is represented by the same pulse and generator
R=Theta Q* Theta on both halves. The averaged holding diagonal in the
geometric generator is essential. The total path KL is sigma_Theta*t, and
the coefficient 4 follows with the previously proved reversal-involution
inequality. The pulse and sensor total-variation correction has the stated
score oscillation factor, not twice that factor.

The theorem needs the actual physical involution, its specified action on
hidden states, exact pi Theta=pi, an appropriate endpoint emission contract,
and equal ideal half durations. Root states these substantive conditions.
The intrinsic entropy of Q does not pay for implementing the pulse.

Root's sufficient timing term 2 Lambda kappa is valid. A sharper term is
available for a fixed or independently scheduled placement error. The
conservative term can also cover an arbitrary causal placement within the
specified window, with the coupling proof given below.

## 1. Marked-path reversal and geometric measure

Use row generators and let Q*=Pi^{-1}Q^T Pi, where pi is positive and
stationary. The permutation Theta is an involution preserving pi. On a
window [0,t], with h=t/2, mark one deterministic pulse x -> Theta x at h.
Between pulses the state follows Q. Each half starts with marginal pi.

Define physical reversal by mapping a trajectory to Theta applied to its
time-reversed state sequence. A forward pulse x -> Theta x then becomes
Theta(Theta x) -> Theta x, again x -> Theta x. Thus the pulse schedule is
mapped into itself. The reversed continuous parts have generator

    R = Theta Q* Theta.

The pulse is a prescribed operation; its marked transition contributes a
unit kernel weight, not a native q_{x,Theta x} jump factor. A jump of the
native CTMC at the fixed midpoint has probability zero. These conventions
also handle states fixed by Theta.

Let P be the full protocol law and P^R its physically reversed image. Their
initial laws agree. The density ratio contains native jump-rate ratios and
the holding term

    integral_0^t [R_out(X_s)-Q_out(X_s)] ds.

The expectation of that holding term vanishes because both stochastic
halves have stationary marginal pi and the pi-weighted escape rates of Q
and R coincide. It must nevertheless be retained at path level. The chain
rule for path relative entropy gives exactly

    KL(P||P^R) = t sum_x pi_x sum_{y!=x}
       [q_xy log(q_xy/R_xy)-q_xy+R_xy] = sigma_Theta*t.

No entropy factor is assigned to the deterministic pulse in this comparison.
A physical implementation with additional microscopic degrees of freedom
can have costs not represented by this interface.

The geometric submeasure sqrt(dP dP^R) uses the same pulse and generator

    S_xy=sqrt(q_xy R_xy),             x!=y,
    S_xx=(q_xx+R_xx)/2.

Rowwise Cauchy--Schwarz followed by arithmetic-geometric mean proves S1<=0.
Unlike the all-even case, q_xx need not equal R_xx; replacing the displayed
diagonal by q_xx would generally invalidate the comparison.

Because Theta commutes with Pi and R*=Theta Q Theta, the generator obeys
S*=Theta S Theta. This identity includes the diagonal: its two terms are
exchanged by Theta. It persists under exponentiation.

## 2. Nonnegative factorization and entropy coefficient

Let E be the same nonnegative row-stochastic endpoint emission kernel at
both ends, with Theta E=E. Endpoint emissions are independent conditional
on the hidden path, or deterministic. Write P_S=exp(hS). Then

    (P_S E)^T Pi(P_S E)
      = E^T Pi P_S* P_S E
      = E^T Pi Theta P_S Theta P_S E
      = E^T Pi P_S Theta P_S E.

The last equality uses E^T Pi Theta=E^T Pi. Hence the geometric endpoint
matrix B is CP, with the claimed factor. The same calculation with S=Q
establishes the equilibrium echo Gram matrix.

Even observations make physical path reversal transpose the endpoint
joint matrix C. Pointwise arithmetic-geometric mean gives C_sym-B>=0.
Normalization of the emission kernels gives

    sum(C_sym-B)=1-affinity(P,P^R)=D.

Physical reversal is an involution of this complete protocol. Therefore
KL(P||P^R)=KL(P^R||P), and the scalar Jeffreys/Hellinger inequality gives
sigma_Theta*t>=4D. For symmetric copositive H,

    gamma=-<H,C_sym> <= h_minus D,
    sigma_Theta >= 4[gamma]_+/(t h_minus).

The CP deficit and nonlinear relaxation inherit exactly the same proof.
The argument handles infinite relative entropy by the usual extended-value
convention. It imposes no microscopic state-count or escape-rate bound in
the exact-operation theorem. It is not a certificate that the accessible
permutation is the *physical* reversal; that remains supplied information.

## 3. One imperfect pulse

Let A be the actual stochastic pulse, with

    sup_x TV(A(x,.),delta_{Theta x}) <= eta.

Only one kernel in the endpoint experiment is replaced. Coupling that
kernel and then using the same subsequent trajectory and readouts gives

    TV(C_A,C_Theta) <= sum_x pi_x TV(A(x,.),delta_{Theta x}) <= eta.

The intermediate state before the pulse has marginal pi, even when its
correlations with the first observed label are retained. The stronger
stationary-average bound is therefore valid if its acquisition is warranted.
A need not preserve pi, satisfy a reversal relation, or have finite entropy
relative to its own reverse. No reverse-protocol theorem is applied to A;
its endpoint law is compared to the ideal Theta protocol.

For L=max H-min H, the standard bounded-score inequality is

    |<H,C_A-C_Theta>| <= L*TV(C_A,C_Theta).

Since H is symmetric, symmetrizing the matrices changes no pairing. Thus
the observed population gamma_A yields

    sigma_Theta >= 4[gamma_A-L*eta]_+/(t h_minus).

The coefficient is L eta, with total variation defined as one half the
entrywise l1 distance. There is no additional factor 2.

## 4. Sensors, preparation, and timing

If independent endpoint instruments F0,F1 have uniform row TV errors
epsilon0,epsilon1 relative to the same even E, their joint readout error is
at most epsilon0+epsilon1. A declared bound on the *joint* endpoint sensor
kernel suffices without independence. Bounds on its two marginals alone do
not suffice: correlated readout noise can violate the factorization while
preserving both marginals.

A useful additional calibration fact is available if the same actual
instrument F is used at both ends. If its parity defect satisfies

    sup_x TV(F(x,.),F(Theta x,.)) <= zeta,

then E=(F+Theta F)/2 is an even reference kernel and each endpoint is within
zeta/2 of E. Independent endpoint readouts therefore cost at most zeta in
the joint-TV budget. This constructs the mathematical reference instrument;
it does not acquire the full hidden-state parity calibration for free.

Initial preparation error nu_prep propagates by Markov contraction. It is
an error relative to the source's genuinely stationary pi. It does not
replace the separate hypothesis that this pi is Theta invariant.

### Timing

Suppose all native escape rates are at most Lambda and the actual pulse is
at h+d with |d|<=kappa<=h. Root's two-semigroup-replacement argument gives
the safe correction 2 Lambda kappa.

For a fixed d>=0, factor the two protocol products as

    P_h (P_d Theta) P_{h-d},
    P_h (Theta P_d) P_{h-d}.

The two middle kernels compare Q with Theta Q Theta over duration d after
a common relabelling. Uniformize both at rate Lambda using one Poisson
candidate-event clock. If no candidate occurs, their states agree. Thus

    sup_x TV((P_d Theta)(x,.),(Theta P_d)(x,.))
       <=1-exp(-Lambda d).

The analogous factorization covers d<0. Therefore a fixed or independently
scheduled displacement gives endpoint TV at most 1-exp(-Lambda|d|), or
its expectation for independent jitter.

If timing can depend causally on the trajectory while remaining in
[h-kappa,h+kappa], conditional-on-d semigroup multiplication is not a valid
proof. Instead couple through one rate-Lambda uniformization clock. If no
candidate occurs anywhere in this length-2kappa window, the two processes
reach the same state after their single parity operation irrespective of
its exact placement. This proves the sufficient uniform correction

    1-exp(-2 Lambda kappa) <= 2 Lambda kappa.

Thus root's conservative budget remains available with this broader
placement interpretation. Without a known rate or continuity modulus,
clock precision alone does not give a uniform endpoint-law guarantee.

Adding the independent error sources by a triangle inequality gives the
root budget, capped at one. A bounded-score confidence interval then adds
L nu to its statistical radius. This step requires a supplied confidence
bound on calibration errors if those errors are themselves estimated.

## 5. A certified genuine finite CTMC control

The exact checker uses six states (p,v), where p is a position modulo three
and v is + or -. The parity operation flips v and leaves p fixed. Rates are

    (p,+) -> (p+1,+)  at a=1,
    (p,-) -> (p-1,-)  at b=1/100,
    (p,v) -> (p,-v)   at c=1/100000.

The source is irreducible with uniform stationary distribution. Observe p,
use h=12/5 and t=24/5, and choose the manifestly copositive matrix H=zz^T,
z=(1,-1,0). Here h_minus=1 and L=2. The physical reverse interchanges a
and b, while S has geometric speed 1/10, the same velocity-flip rate, and
constant killing rate 81/200. Escape rates of parity partners differ, so
this control exercises the holding-diagonal issue.

First put c=0. The two visible half-generators commute, giving the exact
nontrivial echo eigenvalue

    lambda=exp(-909/250)*exp(i*(297/250)*sqrt(3)),
    gamma0=-(2/3) Re(lambda).

The angle lies between 2 and 3. The alternating cosine series gives
cos(2)<-131/315. Also e<68/25 implies e^4<55, while 909/250<4. Consequently

    gamma0 > 262/51975.

Restore c>0 and couple until the first internal velocity flip. Its
probability during the entire protocol is at most ct. The bounded-score
loss is at most 2ct. Therefore the irreducible six-state source satisfies

    gamma > 262/51975 - 2ct
          = 321263/64968750 > 0.00494488504.

Its exact generalized entropy rate is

    sigma_Theta=(a-b)log(a/b)/2=(99/200)log(100),

and the full geometric echo affinity is exp[-(81/200)t]. Rational interval
evaluation verifies sigma_Theta*t>=4(1-affinity). The code also checks a
specific marked path and its physical reversal, including exact jump
prefactors and holding exponents, and an equilibrium control with a=b.

An erroneous pulse consisting of the correct parity map mixed with a reset
to one state at weight 1/1000 has that uniform row-TV error and need not
preserve pi. Adding two endpoint errors of 1/10000 gives nu=3/2500.
Even allowing the worst population score loss and then subtracting the
calibration correction leaves the strictly positive score margin

    gamma_lower - 2L nu = 9413/64968750.

This is a population robustness demonstration, not acquired finite-sample
data. A completed floating matrix exponential gives gamma approximately
0.00821771950791518 and minimum symmetric-joint eigenvalue approximately
-0.004108859753957614; those values are corroboration, not the certificate.
The stronger CP-versus-PSD separation is not claimed by this particular
rank-one-witness control.

`check_parity_echo.py` executed successfully and wrote
`PARITY_ECHO_EXACT_CHECKS.json`. No native measurements or parity operations
were made. The originally planned matrix-exponential interval routine was
not executed; the closed-form/coupling certificate above replaces it.

## 6. Literature and claim scope

The Markov factorization, physical path reversal, divergence inequality,
and stochastic echo idea are established ingredients. Targeted primary
leads, their URLs, and actual retrieval scope are saved in
`PARITY_ECHO_PRIMARY_LEADS.md`. They are not an exhaustive priority search.
The independently checked result is the root's specific CP entropy
certificate for the declared midpoint operation, with its acquisition and
precision contract. This review does not claim that the required operation
has been constructed for a native physical source.
