# Bounded-oscillation logarithmic Lyapunov function gives uniform killed-fiber survival
2026-10-30. Root conditional mathematical lemma for a finite conservative composition process. Application to a particular chemical family still requires its actual uniform boundary drift certificate. No general recurrence or novelty claim.

Let X_N={x in N^d: sum x_i=N}, with actual conservative generator Q_N. A fixed interior set C_N has x_i>=epsilon N. Assume, for all sufficiently large N:

1. A positive V_N has osc(log V_N)<=C_0 N.
2. Outside C_N, Q_N V_N / V_N <= -c_0 N^m.
3. Inside C_N, Q_N log V_N <= C_1 N^m.
4. A real absorbing/clearing transition has rate k_N(x)>=c_1 N^m on C_N and nonnegative rate elsewhere.

These are explicit structural hypotheses, not a mixing or stationarity assumption. Set

 W_N=log V_N-min_{X_N}log V_N,
 f_N=1+W_N/N.

Then 1<=f_N<=1+C_0. Concavity of log gives Q_N log V_N<=Q_N V_N/V_N pointwise. Outside C_N:

 (Q_N-k_N)f_N <= -c_0 N^(m-1).

Inside C_N:

 (Q_N-k_N)f_N <= C_1 N^(m-1)-c_1 N^m.

For N>=2C_1/c_1 this is at most -(c_1/2)N^m, hence at most -c_2 N^(m-1) f_N globally after reducing c_2 using the bounded range of f_N. Positivity of the actual killed semigroup yields

 P_x(tau_clear>t) <= (1+C_0) exp[-c_2 N^(m-1)t].

Consequently E_x tau_clear <= (1+C_0)/(c_2 N^(m-1)), uniformly in composition and without irreducibility of the conservative chain. If all conservative and clearing rates have a common fixed positive catalyst factor a_B, multiply the exponential rate by a_B. For a_B=0 the survival estimate is vacuous and no finite clearing-time conclusion follows. Low finite N must be analyzed separately and can contain closed nonclearing classes.

## Exact factorial oscillation bound
For V_N=exp(sum b_i x_i) product_i (x_i!)^alpha, alpha>0, fixed b_i,

 osc(log V_N)<=N[alpha log d+max_i b_i-min_i b_i].

Indeed N!/product_i x_i! is a multinomial coefficient between1 and d^N. This avoids a spurious log N loss obtained by bounding absolute log V rather than its oscillation on a conserved fiber.

## How the interior upper bound can be checked
For fixed reaction order m and bounded stoichiometric increments, all coordinates on C_N are order N. Each log factorial jump is a bounded sum of logs of coordinate ratios; the common log N cancels because total population is conserved. Its magnitude is bounded independently of N for sufficiently large N. Actual total reaction rate O(N^m) gives assumption3. Enlarging a fixed threshold covers finite-N factorial edge conventions.

## What this does not provide
No uniform negative boundary drift is inferred merely from weak reversibility. The actual fast graph's certificate must prove assumption2 uniformly near every simplex face, including supported subgraphs. This lemma freezes N and the common catalyst factor; immigration, activation or any reaction changing them is NOT included in Q_N. Those must be controlled through an actual stopped-process/competition construction. The survival statement is a killed physical chain estimate, not a claim of fast equilibrium mixing, nor a global Foster function for the full unbounded process.

## Scope clarification from independent review
Exponentialization of a uniform hitting-time mean is standard (Aldous–Fill, Reversible Markov Chains and Random Walks on Graphs, section2.4.3); the possible new application here is the actual uniform boundary/access estimate, not the semigroup implication. A finite shell containing an active state can also contain inactive states: for 2A↔2C at N=2, (1,1) cannot clear under (A)_2. Finite-N extensions must specify source-enabled states/classes, not call the entire shell active. The large-N application with every pure degree-m complex avoids this once N>d(m−1).
