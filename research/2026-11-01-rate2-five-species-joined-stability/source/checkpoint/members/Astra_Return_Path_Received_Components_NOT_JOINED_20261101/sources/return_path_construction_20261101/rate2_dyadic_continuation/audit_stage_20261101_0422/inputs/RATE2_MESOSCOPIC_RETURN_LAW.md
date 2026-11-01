# Rate-2 tree: a paid mesoscopic return law, not yet a recurrence theorem

**Author component theorem, pending independent review.** The original count
model has CD->AE rate 2 and every other channel of the root five-species tree
rate 1. The starting states are x_N=(A0,B=N,C1,D1,E0). On arbitrary full-chain states
define L_full=A+(C+D)/2; it coincides with L below before a remaining bad event. No product-Poisson law
for this count chain is assumed. This result retains the delayed AE loop and
constructs its time-resolved mesoscopic amplification. It does NOT yet prove
macroscopic A occupation, positive recurrence, or stationary tail bounds.

## 1. Actual retained process and scale

Retain 0->A, AB->CD, CD->AB, CD->AE (rate 2), AE->CD, AE->2A.
Let I count immigration, R count AE->2A, and J count CD->AE. Until the first
remaining channel (an A death, a 2A-source jump, AC->2A, or AD->2A), exact identities
are

  L=A+C=A+D=1+I+R,
  B=N-I-2R+A-E,
  E=J-R-S,

where S counts AE->CD. In particular C=D=L-A and E<=J. Construct the retained
process with its own clocks and couple the full process to it until a remaining
channel occurs. All retained reactions except immigration conserve total count,
so this comparison process too is nonexplosive.

Put T=N^(1/5). For fixed positive K,M,S0, stop the retained process at

  tau_N=min(S0*T, first L>=K*T, first E>=M*T^3).

The thresholds may be replaced by their ceilings. All asymptotic statements below
are unchanged. Before tau_N, A<=L<=K*T, E<=M*T^3 and
B>=N-2K*T-M*T^3>=N/2 for sufficiently large N.
The retained A drift and remaining-channel intensity are

  Lret A=1+3C^2-AB,
  q_rem=A+3A(A-1)+A(C+D)<=(1+5K*T)A.

Stopped Dynkin therefore gives, with constants depending only on K,M,S0,

  E integral_0^tau_N A ds <= C T^3/N,
  P(full and retained processes differ before tau_N)
    <= E integral_0^tau_N q_rem ds <= C T^4/N=C/T.          (1)

This is a STOPPED occupation estimate. It does not imply convergence of the
unrestricted absolute expected occupation. It does charge the probability of
all omitted competing channels on the actual mesoscopic window.

## 2. Fast A elimination is proved by a weighted martingale

The point of the calculation is to avoid assuming that A has a stationary fiber
law. The retained generator acts on AE exactly as

  Lret(AE)=E+3EC^2-ABE+2AC^2-2A^2E+2C^2.                  (2)

The covariance terms from AE->2A and AE->CD cancel, while CD->AE contributes
2C^2. Write the stopped Dynkin martingale for (2), rearrange, and divide by N*T.
Using (1), B/N=1+O(T^3/N), A<=K*T and E<=M*T^3 gives, uniformly for 0<=s<=S0
up to tau_N/T,

  (1/T) integral_0^(sT) AE dt
   = (3/(N*T)) integral_0^(sT) E L^2 dt + o_P(1).           (3)

Here is explicit accounting of the remainders, with fixed K,M,S0:

* terminal AE/(NT) and the integrated E/(NT) term are O(T^3/N)=O(T^-2);
* integrated AC^2/(NT) has expectation O(T^4/N^2)=O(T^-6);
* integrated A^2E/(NT), and replacement of C^2=(L-A)^2 by L^2 in the
  leading term, have expectation O(T^6/N^2)=O(T^-4);
* integrated C^2/(NT) is O(T^2/N)=O(T^-3);
* the B/N replacement contributes o_P(1), since E integral AE dt=O(T^6/N)=O(T)
  and sup|B/N-1|=O(T^3/N);
* the stopped AE martingale has expected quadratic variation at most
  C(T^9+T^12/N). After division by (NT)^2 this is
  O(T^7/N^2+T^10/N^3)=O(T^-3+T^-5). Doob's inequality gives uniform convergence
  of the normalized martingale to zero.

For the quadratic-variation bound, CD exits and AB captures have AE-jump size
O(T^3) and total expected counts O(T^3); the two retained AE channels have that
same jump-size bound and expected count O(T). Immigration is smaller. These
bounds use pre-stopping rates and (1), not an uncharged conditional equilibrium.

## 3. The limiting return law

Define l_N(s)=L(sT)/T and e_N(s)=E(sT)/T^3. Counter martingales give

  I(sT)/T=s+o_P(1),
  R(sT)/T=(1/T) integral_0^(sT) AE dt+o_P(1),
  E(sT)/T^3=(2/T^3) integral_0^(sT) L^2 dt+o_P(1),

uniformly before the stops. Indeed the R and S compensators are O(T), while
J's is O(T^3); their normalized quadratic variations vanish. The two E-death
counters divided by T^3 are O_P(T^-2). The C^2-to-L^2 replacement follows from
(1). Combining these facts with (3) and T^5=N yields the integral equations

  l_N(s)=s+3 integral_0^s l_N(u)^2 e_N(u)du+o_P(1),
  e_N(s)=2 integral_0^s l_N(u)^2 du+o_P(1).                 (4)

On each fixed compact stopped rectangle the vector field is Lipschitz. Elementary
Gronwall estimates therefore prove uniform convergence in probability to the
unique stopped solution

  l'=1+3l^2 e,  e'=2l^2,  l(0)=e(0)=0.                    (5)

By (1) the same stopped limit holds for the FULL rate-2 count chain. Every competing
reaction, waiting phase, unsuccessful AE return, and possible A death has been
charged in this passage to the limit.

The ODE has the exact first integral

  l(s)=s+(3/4)e(s)^2,
  e'=2[s+(3/4)e^2]^2.                                    (6)

It grows by actual retained return events: the term l-s is the scaled accumulated
AE->2A count, not an immigration-only startup.

## 4. Constructive finite-level hitting conclusion

For any fixed K>0, let s_K be the unique time at which l(s_K)=K. It is a well-
defined deterministic number obtained from the scalar ODE (6). l'>=1, so the
crossing is transverse. Choose the outer stopped L level larger than K and an
E level larger than sqrt(4(K+1)/3); (6) ensures E does not hit that outer boundary
first. Uniform convergence and transversality imply

  inf{t:L_full(t)>=K N^(1/5)} / N^(1/5) -> s_K

in probability, with the probability of a remaining bad event before this
crossing tending to zero. This is an actual time-resolved mesoscopic return law.

The solution of (6) blows up in finite scaled time s_*<=2. To see this, l>=s
and hence e(1)>=2/3. Thereafter e'>=(9/8)e^4, whose remaining time to infinity
is at most 1. Therefore s_K increases to a limit s_*<=2 as K increases, and for
EVERY FIXED K and epsilon>0,

  P(L_full reaches K N^(1/5) before (2+epsilon)N^(1/5)) ->1.

The order of quantifiers is essential: K is fixed before N tends to infinity.
No statement with K=K(N), no macroscopic A-occupation lower bound, and no recurrence
conclusion follows merely from this finite-level convergence.

## 5. Remaining hard operation

The new representation tracks activation debt in L and sterile E, with a proved
weighted-martingale correction for the fast A phase. It is not a bounded face
multiplier or a fixed favorable complex path. What remains is a uniformly charged
continuation from arbitrarily large mesoscopic levels through the near-blowup
region to macroscopic A service, followed by a return/occupation estimate that
can be renewed from arbitrary states. The deterministic complex-balanced
realization in the companion note supplies a possible interior Lyapunov tool,
but is not a stochastic shortcut for this missing continuation.
