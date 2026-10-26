# Single-port shunt tomography: construction and limits

These are mathematical statements in the declared finite network model. They
are not claims of a new physical instrument or established historical novelty.
All numerical data accompanying this proof are local synthetic calculations.

## Model

Let A be a real symmetric positive definite n by n matrix with nonpositive
offdiagonal entries and a connected offdiagonal graph. Thus A is an irreducible
symmetric nonsingular M-matrix. A physically familiar subclass is

    A = L_w + diag(g),   w_ij >= 0, g_i >= 0,

with a connected conductance graph and at least one positive grounded leak.
A steady unit current or heat input at labeled node 0 gives temperature or
voltage vector A^{-1} e_0. The sole measured scalar is the response at node 0.
The permitted intervention adds a *known, calibrated* shunt at a selected node:

    f_A(d) = e_0^T (A + diag(d))^{-1} e_0,  d_i >= 0.

The construction assumes the number of nodes, their intervention labels and
the shunt amplitudes are known. It does not assume the graph or its weights.
The steady model requires settling after every configuration. Wiring, switches,
calibration and settling are acquisition resources; they are not supplied by
the proof. In a thermal dynamic model A(s)=K+sC, changing a heat capacity has
no steady effect at s=0. That initial idea was therefore replaced by shunts.

## Theorem 1: exact finite tomography

For every A in this class and every fixed t>0, the following d=n(n+1)/2
exact scalar measurements determine every entry of A:

* baseline d=0;
* d=t e_i and d=2t e_i for every i=1,...,n-1;
* d=t e_i+t e_j for every 1<=i<j<=n-1.

No spectral simplicity, controllability, tree topology or generic weights are
needed. No infinitesimal derivative or frequency sweep is used.

### Inverse-M inequalities

Write R=A^{-1}. All entries of R are strictly positive: express A=sI-B with
B>=0 and s>rho(B), and sum the convergent nonnegative Neumann series. Graph
connectivity gives a positive walk between each pair. Principal submatrices
are again nonsingular M-matrices. Block inversion gives, for any k and i,j!=k,

    R_ij - R_ik R_kj/R_kk = (A_{not k,not k}^{-1})_ij >= 0.       (1)

This elementary identity is the sign information needed below. Positivity of
the inverse alone without the M-matrix assumption does not give (1).

### Recover diagonals and the port column

The baseline is r=R_00. For a hidden node i put a=R_0i>0 and p=R_ii>0.
The established rank-one inverse identity gives

    l_1 = r-f_A(t e_i)  = t a^2/(1+t p),
    l_2 = r-f_A(2t e_i) = 2t a^2/(1+2t p).

In particular 0<l_1<l_2<2l_1. With q=l_2/l_1,

    p = (2-q)/(2t(q-1)),   a = sqrt(l_1(1+t p)/t).              (2)

The positive root is selected because R_0i>0. Thus all R_ii and R_0i are known.

### Recover each remaining offdiagonal and select the root globally

Fix i,j!=0. Let a=R_0i, c=R_0j, p=R_ii, q=R_jj, and x=R_ij. Put
U=1+t p, V=1+t q, and y=r-f_A(t e_i+t e_j)>0. Rank-two inversion yields

    y(x) = [t a^2 V + t c^2 U - 2t^2 a c x]/[UV-t^2 x^2].    (3)

Equation (1), conditioning respectively on j and i, implies

    0 < x <= u := min(a q/c, c p/a) <= sqrt(p q).              (4)

On this entire admissible interval the denominator in (3) is positive and

    y'(x) = -2t^2 (aV-tcx)(cU-tax)/(UV-t^2x^2)^2 < 0,         (5)

because its two factors are respectively at least a and c. Thus there is
exactly one admissible x for the observed y. Equivalently let

    Q = (a^2 V+c^2 U)/t - yUV/t^2.

Then x is the smaller root of

    y x^2 - 2ac x + Q = 0,
    x = [ac-sqrt(a^2c^2-yQ)]/y = Q/[ac+sqrt(a^2c^2-yQ)].      (6)

Indeed (5) implies ac-yx>0 at a solution of (3). This proves the root choice,
not merely numerical agreement on examples. Finally invert the assembled R.
The count is 1+2(n-1)+(n-1)(n-2)/2 = n(n+1)/2. Formula evaluation is O(n^2)
after acquisition; a dense final inversion is O(n^3) arithmetic operations.

### What the count does and does not optimize

The strictly diagonally dominant subclass with all offdiagonal entries negative
contains an open set of d=n(n+1)/2 independent real parameters. If m smooth
scalar measurements admit a differentiable local reconstruction G with
G(F(A))=A, the chain rule gives I_d=DG DF, so m>=d. The construction attains
this count. This is dimension optimality for this regular local inverse
criterion. It is not an information-bit, precision, noise, hardware, acquisition
time or energy optimality statement. An arbitrarily precise real number is
not a fixed-cost physical datum.

## Theorem 2: an exact ordinary comparator for a local leak

Fix any A_0 in the above class, v any node, delta>0 and
A_1=A_0+delta e_v e_v^T. Let f_h(d)=f_{A_h}(d) and

    Delta(d)=f_0(d)-f_1(d).

Then for every nonnegative diagonal load d,

    0 < Delta(d) <= Delta(0)
      = delta (A_0^{-1})_0v^2/[1+delta (A_0^{-1})_vv].        (7)

To prove this, the rank-one inverse identity proves positivity and the last
formula. Let R_h(d)=(A_h+diag(d))^{-1}. Inverse monotonicity is entrywise:

    R_0-R_1 = R_0 (delta e_v e_v^T) R_1 >= 0.

For every load coordinate j,

    partial Delta/partial d_j = -R_0(0,j)^2+R_1(0,j)^2 <= 0.  (8)

Integrating along a path from zero to d proves (7). This applies to arbitrarily
large positive loads anywhere, including the faulty node and the sensor node.

### Statistical dominance, including adaptive shunt selection

Now specify a measurement instrument: each settled unit-current observation
under configuration d is N(f_h(d),sigma^2), independently, with the SAME known
sigma for every d and h. This is an assumed instrument-noise model, not a
claim about Johnson noise, thermodynamic fluctuations or every real detector.
Both hypotheses A_0,A_1 are known; h is unknown and equally likely.

Set alpha=Delta(d)/Delta(0) in (0,1] and

    beta = (f_0(d)+f_1(d))/2 - alpha(f_0(0)+f_1(0))/2.

From an unloaded observation X, generate

    Y = alpha X + beta + Z,
    Z independent N(0, sigma^2(1-alpha^2)).

Under either h this has exactly the distribution of the loaded observation.
This transformation does not know h. Thus each loaded experiment is a
Blackwell garbling of an unloaded experiment. An entire adaptive policy of T
shunt selections can be simulated recursively from T fresh unloaded samples
and independent random numbers. No policy in this class beats the ordinary
architecture that repeatedly measures with d=0. This comparison covers all
estimators and all adaptive positive shunt designs in the stated model.

The exact optimal equal-prior error with T observations is

    P_error = Phi[-sqrt(T) Delta(0)/(2 sigma)].                (9)

For at least 75% correct discrimination the optimal required integer count is
max(1,ceil[(2 sigma Phi^{-1}(.75)/Delta(0))^2]). It is both achievable and
unimprovable under these hypotheses. This is stronger than the coarser KL and
Pinsker bound included in the original depth table. It does not assert the
same result for configuration-dependent noise, transient observations, added
detectors, negative loads or controls that remove existing leakage.

## Corollary: exact identifiability coexists with exponential acquisition cost

Take a path with nodes 0,...,L, each edge conductance k>0 and each node leak
g>0: A_0=gI+k L_path. The alternative has one additional delta leak at node L.
Let a=g+2k. Then A_0=aI-B, with B nonnegative, row sum 2k (endpoint diagonal
entries compensate the missing path edge). In the series

    A_0^{-1} = (1/a) sum_{m>=0}(B/a)^m,

the (0,L) entry vanishes for m<L and each entry thereafter is at most the row
sum q^m, q=2k/(g+2k)<1. Hence

    (A_0^{-1})_0L <= q^L/g,
    Delta(d) <= Delta(0) <= delta q^(2L)/g^2.                (10)

Equations (9)-(10) give an exponential necessary number of observations at
fixed absolute noise and input amplitude. On g=k=delta=1 the exact rational
signal at L=20 is 1/116139356908771352, about 8.61e-18; at L=30 it is
1/26575719233704840344934802, about 3.76e-26. This is true despite moderate
matrix conditioning and finite exact-data recovery. Double-precision return
values can erase the signal before any inverse code sees it.

## Theorem 3: unknown calibration cannot be self-invented by this experiment

In a dynamic network write the one-port transfer function as

    z(s,u)=e_0^T [K+s C+diag(h_i u_i)]^{-1} e_0,

where C is positive diagonal, h_i>0 are unknown actuator gains and u_i are
known commands. For ANY positive diagonal S with S_00=1 define

    K'=S K S, C'=S C S, h'_i=S_ii^2 h_i.

The primed bracket is S times the original bracket times S. Therefore its
one-port transfer is identical for all commands and all s in the resolvent
domain. If K is a strictly grounded conductance matrix, an open neighborhood
of S=I preserves that physical subclass. There are n-1 independent hidden
scale degrees of freedom. The explicit example in calibration_gauge.json has
two different grounded physical networks, positive capacities and gains, and
the same transfer at every s and command, not only the 140 sampled checks.

This argument also covers time-varying commands in the ideal model with fixed
C: the change of hidden state x'=S^{-1}x carries C xdot+Kx+diag(hu)x=e_0 I(t)
to the primed equations and leaves the port output unchanged. No amount of
one-port data removes this gauge when gains and capacities are unknown.

One can reconstruct a command-normalized representative instead of K, but
that does not identify absolute internal heat flow or temperature semantics.
Independent calibration or known internal material parameters are needed to
make those physical tasks identifiable.

## Stronger route attempted: remove background loss

The nonnegative-load no-go has a precise escape. If the pre-existing internal
leaks can be switched OFF, leaving a known port leak g_0 only, then

    A = L_w+g_0 e_0 e_0^T,  A 1=g_0 e_0,
    A^{-1}e_0=(1/g_0)1.

The sensor-to-node Green entries no longer attenuate with graph distance. On
the unit path, R_0L=1 and R_LL=1+L, so adding a unit leak at L changes the
port response by exactly 1/(L+2). The supplementary script verifies this by
exact rational arithmetic for all depths in its table. The unit-noise sample
cost is now quadratic in L rather than exponential.

This is an actual mathematical bypass, but its new control is the ability to
remove or compensate every hidden background leak. Adding calibrated shunts
does not supply this ability. A prewired resistor chain with switchable
grounding resistors is an ordinary realizable special case. It gives no
same-apparatus advantage over an ordinary experimenter who opens the same
switches. General electronic guarding is already established; that source
does not demonstrate switchable internal thermal isolation in an unknown
specimen. No claim is made that this latter operation has been constructed.
