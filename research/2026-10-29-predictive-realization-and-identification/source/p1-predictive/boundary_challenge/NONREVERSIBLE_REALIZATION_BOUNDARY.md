# Two retained ports can require arbitrarily many Markov states

29 October 2026, Brisbane. Root's directed-cycle construction, independently
challenged and proved here. This extends the realization review beyond
reversibility. It uses the classical least-variance phase-type theorem;
a self-contained finite proof of the needed inequality is included.

## 1. General stationary, nonreversible record

Let Q be an irreducible finite continuous-time generator, with nonnegative
off-diagonal rates and positive stationary weights w. We do not require
detailed balance. The directed conductance matrix `L=-diag(w)Q` is Eulerian:
its row and column sums vanish. Partition into labelled boundary B and
interior I, and assume every interior state can reach B, so G=L_II is an
invertible M-matrix. Write

```
S  = L_BB-L_BI G^-1 L_IB,
bR = w_B-L_BI G^-1 w_I,
bL = w_B-L_IB^T G^-T w_I,
c  = w_I^T G^-1 w_I.
```

All components of `vR=bR-w_B` and `vL=bL-w_B` are nonnegative, and both
sum to the interior mass V. S is again Eulerian with nonpositive
off-diagonal entries. For any grounded exterior the exact source energy
has the ordinary nonsymmetric Schur form

```
c+bL^T (S+R)^-1 bR.                                  (N1)
```

The source and its normalization remain specified stationary weights.
The finite-state positive realization class in this note does not include
deterministic delays, age variables, signed kernels or general semi-Markov
holding laws.

## 2. A fixed-size record with an unbounded realization requirement

Take two retained ports 0,1, each of mass 1, and n hidden states, each of
mass 1/n. Give the directed cycle

```
0 -> hidden_1 -> ... -> hidden_n -> 1 -> 0
```

stationary flow 1 on every edge. Native exit rates are 1 at the two
ports and n at the hidden states. The chain is irreducible, total mass
is 3, and the hidden duration from leaving 0 until reaching 1 is Erlang
with n phases and rate n. Its mean is 1 and its second moment is 1+1/n.
Direct triangular elimination gives

```
S=[[1,-1],[-1,1]],
w_B=(1,1),
bR=(2,1), bL=(1,2),
c_n=(1+1/n)/2.                                       (N2)
```

**Theorem.** Every finite stationary CTMC realizing the same calibrated
record (N2), with these two retained ports, has at least n hidden states.
The original directed cycle attains this bound. Consequently no bound on
the number of positive Markov states depending only on the port count
can realize all such nonreversible records exactly.

### Reduction to one hidden phase-type channel

Consider a competing realization with k hidden states and positive
weights. The vector `G^-1 w_I` is strictly positive, since G^-1 is
nonnegative with positive diagonal. Therefore `vR_1=0` forces every
flow from port 1 to the interior to vanish. Similarly `G^-T w_I>0` and
`vL_0=0` force every flow from the interior to port 0 to vanish.

Thus all hidden flow enters from port 0 and exits at port 1. Define
the incoming flow row `a^T=-L_0I` and total f=sum(a)>0. The initial
hidden state after such entry has probability row alpha=a^T/f. Its
absorption time tau at port 1 is a phase-type distribution with at most
k transient states; arbitrary branching, feedback and entry mixtures
are allowed.

Let D_I=diag(w_I). The hidden fundamental time matrix is
`N=G^-1 D_I`. Column balance gives `a^T=1^T G`, so

```
f E_alpha tau = a^T G^-1 w_I = V = 1,
f E_alpha tau^2
 = 2 a^T G^-1 D_I G^-1 w_I = 2c_n.                   (N3)
```

Every hidden excursion exits at port 1. Consequently the trace
conductance from port 0 to port 1 is f plus its nonnegative direct
conductance. Equation (N2) therefore forces `0<f<=1`.

The phase-type inequality proved below is

```
E tau^2 >= (1+1/k)(E tau)^2.
```

Combining with (N3) gives

```
c_n >= (1+1/k)/(2f) >= (1+1/k)/2.
```

Since c_n=(1+1/n)/2, k>=n. No global spectral-gap, rarity, or mixing
assumption enters this proof. Unreachable hidden states cannot weaken
it: the phase-type order is at most the total hidden state count.

## 3. A self-contained proof of the phase-type inequality

This is the classical Aldous--Shepp least-variance principle, not a new
information inequality. The following finite flow proof is supplied to
make its new use auditable.

Let tau be absorption at state 0 from deterministic transient state s
of a finite CTMC with k transient states. Let h_i=E_i tau, h_0=0,
and let nu_i be the expected occupation time of transient state i before
absorption. Every moment is finite: the finite transient generator is
invertible and absorption is almost sure. The mean equations are
`Q h=-1`, and `nu^T Q=-e_s^T` on the transient block.

Put `f_ij=nu_i q_ij` for each actual directed jump i->j, including j=0.
These nonnegative expected jump counts have divergence +1 at s, -1 at
the absorber, and zero elsewhere. An elementary expansion gives

```
sum_ij f_ij (h_i-h_j)^2
 = nu^T Q(h^2)-2 sum_i nu_i h_i (Qh)_i
 = -h_s^2+2 nu^T h
 = E_s tau^2-(E_s tau)^2.                             (N4)
```

Equivalently (N4) is the quadratic-variation identity for the stopped
martingale `h(X_t)+t`. It is valid for arbitrary finite branching and
cycles, not only sequential phases.

Decompose the nonnegative flow f into unit-total-weight simple paths
from s to 0 and nonnegative cycles. One finite construction repeatedly
finds an s-to-0 path and subtracts its smallest edge flow; each subtraction
removes an edge, and flow conservation ensures the total extracted path
weight is 1. Remaining flow consists of cycles. Every simple path has
r<=k edges, telescoping potential change h_s, and therefore

```
sum_path (h_i-h_j)^2 >= h_s^2/r >= h_s^2/k.
```

Cycles have nonnegative cost. Inserting the path decomposition into
(N4) proves `Var_s(tau)>=h_s^2/k`, hence
`E_s tau^2 >= (1+1/k) h_s^2`.

For an arbitrary initial probability alpha, apply this bound for each
starting state, then Jensen:

```
E_alpha tau^2 >= (1+1/k) sum_i alpha_i h_i^2
                  >= (1+1/k)(sum_i alpha_i h_i)^2.
```

An Erlang chain of k equal-rate sequential phases attains the bound.

## 4. The obstruction also concerns an actual scalar-mean context family

In general a nonreversible pair `(bL,bR)` need not be identifiable from
scalar equilibrium means: time reversal exchanges the pair while
preserving many such means. The theorem above is stated for a retained
record, but the two-port example can be strengthened beyond that statement.

Allow the same calibrated passive probes used in the previous note:
ground both ports with conductance t>0 and attach known pendant masses
z_i by known conductances g_i. Every probe has source mass 3+sum(z).
After subtracting the known pendant residual, the scalar mean gives

```
F(t,z)=(3+sum z)T(t,z)-sum_i z_i^2/g_i
      =c+(bL+z)^T (S+tI)^-1 (bR+z).                  (N5)
```

Suppose a competing stationary two-port module has the same w_B=(1,1),
total mass 3, and agrees with (N2) for EVERY such mean probe. Any two-by-two
Eulerian Schur Laplacian is symmetric. The quadratic coefficients in z
of (N5) identify `(S+tI)^-1`, so S must equal (N2). The linear coefficients
identify `bL+bR=(3,3)`. Since both vectors sum to 3 and exceed w_B,

```
bR=(3/2+d,3/2-d), bL=(3/2-d,3/2+d), |d|<=1/2.
```

The constant term is then

```
F(t,0)=c+9/(2t)-2d^2/(t+2).
```

Agreement at two distinct values of t forces `c=c_n` and `d^2=1/4`.
Thus the record equals (N2) or its time reversal. Either orientation
has the same phase-type lower bound after exchanging port labels.

Therefore the unbounded state requirement holds even when asking only
for agreement with this explicit FAMILY OF SCALAR EQUILIBRIUM MEANS,
not for a gratuitously overcomplete oriented record. Six nonnegative
mass probes at one t plus the zero-mass probe at another t suffice for
the exact coefficient argument. These are exact consequential outputs,
not a claim of seven cheap or arbitrarily precise physical measurements.

## 5. Scope: exact complexity is not a fixed-error impossibility

The target means need not grow with n. For instance the mean to port 1
from equilibrium conditioned outside it is

```
T_1=(2+c_n)/2=5/4+1/(4n),
```

which stays between 5/4 and 3/2. The obstruction comes from the information
encoded by the equilibrium residual, not a large printed timescale.

Conversely, its exactness matters. If S,bR,bL,w_B remain exact and c is
allowed absolute error epsilon, the preceding argument only forces

```
k >= 1/(1/n+2 epsilon).
```

For n>=k, using the k-phase Erlang record instead has
`|c_k-c_n|<=1/(2k)`. Thus a fixed absolute c accuracy admits a phase count
independent of n on this family. The required mean accuracy follows by
the explicit normalization in the query formula. Allowing errors in
the other record components is a different stability problem and is not
settled by this corollary.

Increasing source observations does not make the small residual difference
1/(2n) a free precision resource. The bounded-mean normalization has
hidden exit rate n. The exact state obstruction also has a uniformly
bounded-clock variant: divide ALL cycle flows by n. Then every native
exit rate is at most 1, S becomes S/n, c becomes `(n+1)/2`, and bR,bL,w_B
are unchanged. The possible competing throughflux now obeys f<=1/n, so
the same proof still gives k>=n. Its means are n times the bounded-mean
values; no uniform-time execution advantage follows from either version.
No fixed microscopic geometry is acquired here. There is no lower bound
against semi-Markov delays,
signed linear realizations, explicit non-Markovian memory, or direct
evaluation of the small mean record itself.

The contrast with the reversible theorem is therefore precise: every
feasible reversible mean record has the positive at-most-2m-state
realization, whereas two stationary nonreversible ports can require an
arbitrarily large exact positive Markov realization. The same finite
mean record remains cheap to evaluate algebraically once actually known.

## 6. Primary source and execution

David Aldous and Larry Shepp, *The least variable phase type distribution
is Erlang*, Communications in Statistics--Stochastic Models 3(3),
467--473 (1987), DOI 10.1080/15326348708807067.
Primary repository: https://escholarship.org/uc/item/7w51x4rb
PDF: https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf

The primary scanned theorem and proof on journal pages 470--472 were
read by local OCR after the web text view exposed only the cover. The
PDF SHA256 is
`fb24e61b3b9ead859bd73a5baf90a13f3886085b677a9bc688da0db8772e504a`.
The research copy is under `sources/primary`, outside the generated
deliverable; the citation and proof-use scope are preserved here.
The source theorem states deterministic initial state; the initial-mixture
extension needed above is proved explicitly by Jensen, not assumed.

`check_nonreversible_boundary.py` checks exact cycle records, phase
moments, the hidden-flux identities for cyclic mixed-entry phase systems,
the scalar passive-probe reconstruction and finite-error corollary.
All controls use supplied rational generators and exact arithmetic.
There are no physical observations, acquired clocks, or general performance
claims. The state lower bound follows from the ordinary proof, not a
search over finitely many candidate realizations.
