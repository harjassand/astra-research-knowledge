# A polynomial physical first-abnormal operation from every actual state

Author strengthening of GLOBAL_NORMAL_EPISODE_THEOREM.md. Its exact
unbounded normal reference is retained. The previous reciprocal-input-
weight bound is valid but far too loose for synthesis. Here finite
protected heads and the REAL adjoint policy remove that exponential
cost. This earns a global actual-time/output operation, NOT inwardness.

For arbitrary positive raw rates and every physical input x, let sigma
be the first abnormal reaction under the global policy of that theorem.
For every integer r,p>=0 there are acquired raw constants with

    E_x integral_0^sigma (1+M_t)^r dt
          <= C_r*(1+M(x))^(r+2),
    E_x(1+M(X_sigma))^p <= D_p*(1+M(x))^p.            (1)

All actual outputs and normal histories are included. In particular
E sigma<=C_0(1+M)^2 and E J_full(sigma)<=C(1+M)^9. No exponential
return time, stationary full process or uniform normal mixing gap is
assumed. The source list and rate convention are unchanged.

## 1. Protected forward physical clock

Stop at sigma OR the first NORMAL exit from {M<=L}. Let b=min(alpha0,beta0),
B=alpha0+beta0, c1=max(alpha1,beta1), c2=max(alpha2,beta2),
t0=24 min(alpha3,beta3).

Whenever at least one anchor has residue1 or2, the actual abnormal
source0 hazard is >=b. Thus any off-00 interval, stopped at absorption
or return to both residues0, has mean <=1/b. At residue00 the two normal
source0 hazards have aggregate B; all other normal events retain00.
The mean time to off-00 entry or absorption is <=1/B.

An entry by normal source0 puts its chosen port at residue1. Until that
port's next normal step, its normal hazard is <=c1 L^2, while its own
abnormal source0 remains >=b. Peer/core motion does not change this
port's residue. Integrated hazards therefore give probability of kill
OR head exit before this next own normal step at least

    b/(b+c1 L^2).

Returning to00 and restarting the genuine trials proves

    max_D_L E tau <= C_F L^2,
    C_F=1/b+(1/B+1/b)*(1+c1/b), L>=1.               (2)

The constant head exit is included as absorption, never omitted.

## 2. The actual adjoint has a polynomial clock too

The reference mu gives the following EXACT normal reverse generator:

* at residue1, reverse growth0 at the actual source1 hazard;
* at residue2, reverse growth1 at the actual source2 hazard;
* at residue0, reverse growth2 at the actual terminal hazard, and
  reverse terminal (+3A,+2B,+2C) at constant source0 rate;
* both core directions are unchanged.

This follows by the same equal cycle-flux cancellation as the normal
reference. It is a proved mathematical adjoint, not a proposed physical
reaction network. Its killing hazard is the SAME h.

Off-00 time is again <=1/b. At00, within mean1/B a constant reverse
terminal creates a pair at a positive anchor>=3 (unless absorption
already occurs). Thereafter some eligible pair remains until off-00
entry: core cannot move a pair to a zero anchor, and at positive00
anchors every pair is terminal-capable. The total reverse-to-residue2
hazard is therefore >=t0. Thus reverse00 time is <=1/B+1/t0.

The entered residue2 port's next reverse step has hazard <=c2 L^4,
whereas abnormal source0 is >=b. The same actual renewal gives

    max_D_L E tau_reverse <= C_R L^4,
    C_R=1/b+(1/B+1/t0+1/b)*(1+c2/b).                (3)

An initial off-00 segment is included. Reverse head exits, including a
constant reverse packet jump, also count as absorption.

## 3. Pay the REAL probability of leaving the protected head

Let G_L be the genuine normal Green kernel killed at h and normal head
exit. Exact finite adjointness and (3) imply

    G_L(x,y)<= C_R L^4*mu(y)/mu(x).                  (4)

Only normal growths can raise physical mass; their total rate is <=
G0(1+L)^4, G0=alpha0+alpha1+alpha2+beta0+beta1+beta2. A forward head
exit can start only at mass>=L-3. The actual channel compensator yields

    P_x(normal head exit before sigma)
       <=16 C_R G0 L^8/mu(x) *sum_(M>=L-3)mu.       (5)

This charges the entire protected-region failure, with all competing
core and block paths. It is not a prescribed favorable receiving law.

Use the explicit envelope from the preceding theorem. Choose its base
z0=z(x), write n=M(x), and put

    Kc=max(1,R,R^-1), Kp=max(1,alpha0/alpha3,beta0/beta3),
    K=Kc Kp, t=6K,
    rmin=min(1,alpha0/alpha3,beta0/beta3), Cx=Kc/rmin,
    D0=32 C_R G0 Kc^2*alpha_max*beta_max/(alpha_min*beta_min).

The input has core exponent0, so

    C_envelope/mu(x)
        <= Kc^2*alpha_max*beta_max/(alpha_min*beta_min)
                                *Cx^n*n!.

If L-3>=2t, the factorial-series tail has bound
2 t^(L-3)/(L-3)!. Therefore (5) is at most

    D0 L^8 Cx^n*n!*t^(L-3)/(L-3)!.                  (6)

## 4. Acquire a uniform rare-head threshold with raw scalar tests

Fix any delta>0. Set L=2(n+N). A FINITE raw N can be acquired as follows:

    N>=3, N>=t+2, N+1>=2 Cx t^2, N+1>=2^9 t^2,
    D0*2^17*8!*N^8*t^(2N)/N! <= delta.              (7)

Test the last inequality in logarithms, increasing N by doubling if
needed. It eventually holds: beyond the displayed threshold its left
side decreases at least geometrically with N.

For completeness, (7) is uniform in ALL n, not a head-by-head oracle.
Writing m=L-3, N>=3 gives m>=2n+N and thus
n!/m!<=1/(n+N)!<=1/[N!(N+1)^n]. Since t>=1, (6) is at most

    D0*2^8*N^8*t^(2N)/N! *(n+1)^8*2^-n.

The final factor is <=8!*2^9 by its convergent binomial-series bound.
This proves the desired probability <=delta from every physical input.

## 5. Continue every genuine head output; sum the actual rewards

At a normal head exit the actual mass is <=L+3. Keep that output, reset
the head from its ACTUAL mass, and repeat until an abnormal reaction
occurs. This continuation is exactly the original first-abnormal stop,
not a restart of the physical state. Put Z=M+2N+3. A genuine failed
head obeys Z_next<=2Z, with conditional probability <=delta.

Within a block, (2) gives mean time <=4 C_F Z^2 and weighted occupation
at most4 C_F 2^r Z^(r+2). Choose delta=2^(-r-3). Strong Markov summation
over every actual failed head proves

    E integral_0^sigma(1+M_t)^r dt
       <=8 C_F 2^r*(M_in+2N+3)^(r+2).               (8)

For output moments choose delta<=2^(-p-1). Every terminating abnormal
output has 1+M_out<=2Z at its current block, hence

    E(1+M_out)^p <=2^(p+1)*(M_in+2N+3)^p.           (9)

The actual first-abnormal stop is independent of these proof cutoffs;
N may be selected separately for each moment. Since Z is bounded by a
raw multiple of1+M, (8),(9) prove (1). Infinite failed heads have zero
probability; normal nonexplosion was already proved. The full genuine
jump count follows from its actual polynomial rate compensator.

## 6. Meaning and remaining scientific work

This is a genuine population-controlled operation from EVERY region:
unbounded cold inventories, arbitrary signed residuals, zero anchors,
high anchors and all source/peer landings. The raw translated-cycle
reference and its reversed constant packet activation pay the head
failure and physical clock. No stationary actual input or mixing gap
was inserted.

The common output INTEGRABILITY contract is now polynomial. The actual
inward SIGN remains unproved. The signed factorial energy probes and
source-conditioned debt rules have not yet been reconciled into one
global negative return law. In particular polynomial exit mass moments
alone do not bound a signed energy decrement or its repayment. This
theorem supplies neither full six-species recurrence nor arbitrary-WR
recurrence. Its constants are deliberately conservative; no practical
advantage is claimed.

Ordinary ingredients are finite adjoint Green comparison, channel
compensators and renewal summation. The existing finite normal-cell
theorem and P3 nonexplosion method retain their accepted scopes. The
new raw operation is the all-anchor normal reference, its derived
adjoint packet dynamics and global polynomial actual first-abnormal
contract. global_polynomial_episode_bounds.py acquires the scalar N
and constants; check_global_normal_reverse.py checks the exact reverse
identities, separately from the proof's all-state quantifiers.
