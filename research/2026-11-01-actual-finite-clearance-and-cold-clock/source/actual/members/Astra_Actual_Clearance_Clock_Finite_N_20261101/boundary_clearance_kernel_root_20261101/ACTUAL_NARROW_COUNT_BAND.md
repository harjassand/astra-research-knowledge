# A received narrow total-count band from the original source ledgers

Status: root stopped-domain construction, pending independent review. This replaces an unnecessarily broad supplied +/-1% total-count premise by an actual event for the fixed corner preparation. It does not prove ratio-cone or imbalance admission.

Initial state is (A,B,C,D,E)=(0,N,1,1,0), integer N>=10^5, and T=N^(1/5)>=10. Let S=A+B+C+D+E and L=A+(C+D)/2. Set

 Emax=ceil(N/100),
 tau_cap=first {E>=Emax OR L>=N/5000}, d=4T.

The two cap exits are declared outputs, not renamed clearance. Use the ORIGINAL actual immigration and death counters I,D from time zero:

 S(t)=N+2+I(t)-D(t).

I has unit-rate Poisson law. The true-death compensator is integral A dt; it is not independent of I or the other history.

## Source storage and its deterministic ceiling

Temporarily stop also at the first B<.9N and at the budget described below. Before the cap, E<N/100 and L<N/5000. Thus A<=L<B and

 C+D+4E<(.0004+.04)N=.0404N<B/2

whenever B>=.9N. The accepted root storage W=A+2(Emax+1-E) is therefore applicable without a separate A or imbalance premise. Its initial value is W0=2(Emax+1).

Put S0=W0+4T and Qbar=2S0. The actual source budget Q=integral[(AB/2)+CD]dt reaches Qbar before the other stops with probability at most

 exp(-S0/124)<=exp(-N/6200),

because S0>=N/50. On paths below this budget,

 integral A dt<=4S0/(.9N)<=1<=T.

For the explicit upper bound, W0<=N/50+4 and N=T^5,T>=10 give
4S0/(.9N)<=(.08N+16+16T)/(.9N)<=1. The original source's actual initial charge is used; no restarted remaining-storage assumption appears.

## Actual count tails, without independent attempts

Chernoff with theta=log2 gives

 P(I(4T)>=10T)<=exp(4T-10T log2)<=exp(-T),

using log2>=1/2. On its complement, 2+I(t)<=12T for every t<=4T.

For the STOPPED death counter, the exponential counting-process martingale and theta=1/2 give

 P(D reaches12T before the source budget/domain stops)
 <=exp(integral A ceiling-6T)<=exp(-5T),

using exp(1/2)-1<1 and the same-stop occupation ceiling<=T. This is not replacement of the actual count by an independent conditional Poisson variable.

On the complements of these three charged failures,

 |S(t)-N|<=12T

through the actual cap or d, subject only to showing the temporary B floor cannot be the first exit.

## The B floor is now received, not assumed

If B were the first floor exit before cap/d, then the exact identity B=S+A-2L-E and the count bounds would give

 B>=N-12T-N/2500-N/100
   >=.9884N>.9N,

because12T/N<=.0012 at T>=10. This contradicts that exit. Including a cap's one-step overshoot subtracts at most3, still safely above .9N for N>=10^5. Thus the auxiliary floor is eliminated by the same actual count event.

Consequently, with probability at least

 1-exp(-N/6200)-exp(-T)-exp(-5T),

both |S(t)-N|<=12T and B(t)>=.9N hold throughout t<=tau_cap wedge4T, including its actual terminal jump. The source budget and its associated occupation ceiling hold on the same event. A zero or negative displayed lower probability is never interpreted as nonvacuous admission.

This event may be used by a later corrected-ratio proof only with its full probability charge and actual cap/clock. It does not license a broad robustness claim for arbitrary initial compositions with S=.99N or1.01N. Those broad-band counterexamples remain valid. No physical reset, rate change or new source preparation is supplied.
