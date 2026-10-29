# Why reversibility can change the cost of a positive realization

29 October 2026, Brisbane. Root's further attack after the positive 2m-state
construction. The ordinary algebraic record stays finite without
reversibility, but a positive continuous-time Markov realization need not
have a state bound depending only on the number of retained ports.

## 1. A directed source needs two population loads

Let a finite irreducible CTMC have positive stationary weights w and
L=-diag(w)Q. This is an Eulerian directed Laplacian: L1=0 and 1^T L=0,
but it need not be symmetric. For ports B and interior I let G=L_II and

    S=L_BB-L_BI G^{-1}L_IB,
    b_R=w_B-L_BI G^{-1}w_I,
    b_L=w_B-L_IB^T G^{-T}w_I,
    c=w_I^T G^{-1}w_I.

Both b_R,b_L are positive, and sum(b_R)=sum(b_L)=sum(w). With a passive
grounded exterior R and any added boundary load z>=0, elimination gives

    T=[c+(b_L+z)^T(S+R)^{-1}(b_R+z)]/[sum(w)+sum(z)],       (1)

apart from the separately known residence contribution of external hidden
nodes. The right load controls the boundary Poisson field. The left load
controls how equilibrium population weights that field. Reversibility
makes them equal; equality must not be assumed in a directed source.

This is the nonsymmetric block inverse identity. It is not a new inverse
formula and it does not acquire a stationary law or a source interface.

## 2. Fixed two-port family

For any n>=1, consider the directed cycle

    port 0 -> hidden 1 -> ... -> hidden n -> port 1 -> port 0.

Give both ports mass 1, every hidden state mass 1/n, and every directed
edge stationary flow 1. A state's departure rate is flow divided by mass.
The process is irreducible, the total mass is 3, and every hidden phase
has rate n. Direct calculation gives

    S=[[1,-1],[-1,1]],
    w_B=(1,1), b_R=(2,1), b_L=(1,2),
    c_n=(1+1/n)/2.                                      (2)

Thus the number of scalar coefficients in the exact record is constant.
The excursion from port 0 to port 1 has an Erlang(n,n) duration of mean
1 and variance 1/n. This is a supplied mathematical family, not an acquired
unknown source or a physical clock construction.

## 3. Every positive CTMC with the same record needs at least n hidden states

Consider any finite positive CTMC realization of (2) with k hidden states.
Write v_R=b_R-w_B=(1,0), v_L=b_L-w_B=(0,1). Positivity of G^{-1}w_I
and G^{-T}w_I shows that v_R,1=0 forbids jumps from port 1 into I, while
v_L,0=0 forbids jumps from I into port 0. All stationary hidden population
therefore belongs to excursions entering from port 0 and leaving at port 1.

Let f be the total stationary entry flow into I. Then 0<f<=1, since the
Schur flow from port 0 to port 1 is 1 and any direct contribution is
nonnegative. Let tau be the hidden excursion duration from its true entry
distribution. Stationary occupation and the second-hit-time Poisson
identity give

    f E tau = sum_I w_i = 1,
    (f/2) E tau^2 = c_n.                               (3)

The first follows by multiplying the stationary interior balance equation
by the killed fundamental matrix. For the second, if A=-Q_II then
f alpha^T A^{-1}=w_I^T and
f E tau^2=2f alpha^T A^{-2}1=2w_I^T G^{-1}w_I.

The classical least-variable phase-type inequality states

    Var(tau) >= (E tau)^2/k.                           (4)

Combining (3)-(4) yields

    c_n >= (1+1/k)/(2f) >= (1+1/k)/2,

and therefore k>=n. The directed cycle attains k=n. Exact positive
realization complexity is unbounded at two ports in this nonreversible
class, in contrast with the reversible 2m theorem.

### Self-contained proof of the imported variance inequality

The inequality is Aldous--Shepp's classical phase-type result, not a new
variance theorem. The following martingale proof supplies the precise
version needed here, including an arbitrary initial distribution.

For absorption time tau and a fixed transient starting state i, let
h(x)=E_x tau, with h=0 at absorption. The stopped process
h(X_{t wedge tau})+(t wedge tau) is a square-integrable martingale.
Its terminal value is tau and its jumps are changes in h. Consequently

    Var_i(tau)=E_i sum_jumps [h(after)-h(before)]^2.

Sort the k transient values as 0=a_0<=a_1<=...<=a_k (ties are harmless).
Every absorbing path beginning at h(i)=a_r crosses every level gap
a_j-a_{j-1}, j<=r, at least once. For a jump crossing several such gaps,
its squared size is at least the sum of their squares. Hence pathwise
the total squared jumps are at least

    sum_{j<=r}(a_j-a_{j-1})^2 >= a_r^2/r >= h(i)^2/k.

Taking expectations proves the fixed-start case. For a random initial
state, the variance decomposition adds Var(h(initial)) and Jensen gives
Var(tau)>=E[h(initial)^2]/k>=(E tau)^2/k. Finite proper phase-type laws
have finite moments, so stopped martingale limits are justified.

Primary source: Aldous and Shepp (1987), *The least variable phase type
distribution is Erlang*, DOI 10.1080/15326348708807067,
https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf .

## 4. Relation to observable mean contexts

The record-preserving lower bound above is already precise. It also applies
to a sufficiently rich declared mean interface, rather than requiring that
the record itself be presented to the observer.

At fixed port masses and total mass 3, allow passive external pendant
loads z>=0, grounding each port by the same conductance t>0, and
boundary-started mean queries. Every two-port Eulerian Schur matrix is
symmetric and has one nonnegative edge conductance. After subtracting the
known external residence term, the quadratic coefficient in z in (1)
identifies (S+tI)^{-1}, hence S. The linear coefficient identifies b_R+b_L.
The two boundary-started means identify b_R, since each one-point killed
problem is scalar. Therefore b_L and then the constant c are identified.
Any realization preserving this whole mean family has the same (2), so
the state lower bound applies. These are information-equivalence probes,
not a low-cost experimental acquisition claim.

Even if boundary-started means are omitted, the special two-port family
can be separated up to time reversal using two different t values.
The linear coefficient fixes b_R+b_L=(3,3), and sum(b_R)=sum(b_L)=3.
Thus write b_R=(1+a,2-a), b_L=(2-a,1+a), 0<=a<=1. The constant term is

    c + (9/2)/t - 2(a-1/2)^2/(t+2).

Agreement with (2) at all t forces c=c_n and a=0 or 1. The reverse
orientation obeys the same hidden-state lower bound. Retained calibration
and mass premises remain necessary in this argument.

## 5. Exactness and the resource being bounded

This is an exact positive-realization state bound, not a computational
lower bound. The constant-size algebraic record still evaluates mean
queries through a two-port solve; its c_n coefficient requires O(log n)
bits. A semi-Markov, signed, or direct formula representation is not bound
by the number of CTMC phases. The clocks n in the witness also grow.

The exact obstruction must not be promoted to arbitrary fixed accuracy.
If all other coefficients remain exact and c is allowed error delta>0,
the same argument only forces

    k >= 1/(1/n+2 delta)

for a proposed c no larger than c_n+delta. At fixed delta this saturates.
No general lower bound with simultaneous errors in every record entry is
claimed. Likewise, the theorem gives no native acquisition advantage and
does not justify ignoring the observation-depth or tail costs established
elsewhere in this branch.
