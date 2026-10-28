# The acquired positive transfer and the limits of the attempted compression

This is a construction for the actual spin-two Heisenberg gate, followed by
two different applicability tests. It does not prove a uniform Heisenberg
gap or acquire the cold long-ring partition functions. The local tensor test
does not imply a lower bound on every closed-network trace algorithm.

**1. The source model and the basis change are exact.** In the usual spin
basis, let the magnetic labels be a=-2,-1,0,1,2, Z=diag(a),
P_(a+1,a)=sqrt(6-a(a+1)), and M=P^T. The antiferromagnetic bond is

    h = Z tensor Z + (P tensor M + M tensor P)/2.

Its eigenvalues are -6,-5,-3,0,4. The alternating pi rotation
D=diag(1,-1,1,-1,1) gives

    h_M = Z tensor Z - (P tensor M + M tensor P)/2.

The peer's source uses real antisymmetric generators g_i on the five
traceless symmetric Cartesian tensors and h_source=-sum_i g_i tensor g_i.
`source_gauge_check.py` constructs an exact unitary U by diagonalizing i*g_z
and applying i*g_x-g_y as a raising operator. It checks, entry by entry,

    (U D tensor U)^dagger h_source (U D tensor U) = h_M.

The explicit U and the source SHA256 are in `results/SOURCE_GAUGE_CHECK.json`.
Every even periodic ring admits this alternating unitary. Both polynomial
and exponential gate traces therefore concern the acquired source model.

**2. The quadratic gate has an exact nine-term nonnegative factor.** Put

    G_2(delta) = I-delta h_M + delta^2 h_M^2/2.

For 0<=delta<=1/2 the code constructs G_2=sum_r L_r tensor R_r with every
entry of every L_r and R_r nonnegative. The proof is given here because
floating positivity at one delta would not establish the interval.

For zero magnetization transfer, let x=(a+2)/4 and use the three nonnegative
quadratic Bernstein functions ((1-x)^2,2x(1-x),x^2). For the right magnetic
label b define

    P0=1+9 delta^2-(3/2)delta^2 b^2,
    P1=-(delta+delta^2/4)b,
    P2=(3/4)delta^2(b^2-2).

The corresponding right diagonal entries are
(P0-2P1+4P2, P0-4P2, P0+2P1+4P2). The first and last are the a=-2 and a=2
diagonal entries of G_2. Each is at least 1/2: a diagonal entry is at least
1-t+t^2/2 for t=delta*ab. The middle is
1+15delta^2-(9/2)delta^2b^2 >= 1-3delta^2 >= 1/4.

For magnetization transfer q=1 or -1 set X=a+q/2, Y=b-q/2, so |X|,|Y|<=3/2.
The gate entry, with the ladder factors removed, is

    (delta/2) [1+delta/4-delta X Y].

It is the sum over s=1,-1 of

    (1+s X/(3/2)) * (delta/4)(1+delta/4-s delta(3/2)Y).

Both factors are nonnegative for 0<=delta<=1/2 because the last bracket is
at least 1-2delta. Restoring the nonnegative ladder coefficients gives two
product terms for each sign of q. Transfer q=2 or -2 contributes one term:
L=P^2, R=delta^2 M^2/8, or the reversed pair. Thus the total is 3+2+2+1+1=9.
`positive_gate.py` checks the entire reconstruction symbolically in delta.

For delta>0 the source realignment Gram matrix has independent basis
I, three g_i, and five rank-two tensors, with strictly positive weights
1+6delta^2, delta+delta^2/4, delta^2/2. Its operator Schmidt rank is nine;
local unitary conjugation preserves that rank. Nine nonnegative product
terms are consequently minimal. At delta=0 the rank drops to one.

A positive diagonal similarity removes the remaining square roots:
S=diag(1,2,2sqrt(6),12,24), with all factors replaced by S^-1 L S and
S^-1 R S. At rational delta all entries are rational. This preserves support,
nonnegativity, and all closed traces.

**3. The positive transfer has the correct periodic readout.** For time
histories x,y of length N over the r local factors define

    K_L(x,y)=Tr product_t [L_(y_t) L_(x_t)],
    K_R(x,y)=Tr product_t [R_(y_t) R_(x_t)],
    T_N=K_L K_R^T.

These are entrywise nonnegative matrices. Expanding Tr(T_N^m) and summing
each local factor index reconstructs the checkerboard product of G on the
2m-site periodic ring, with N time slices. A factor index on one checkerboard
bond reconstructs sum_r L_r tensor R_r=G; the other orientation gives its
site swap, which equals G for this bond. Therefore, exactly,

    Tr(T_N^m)=Z_(2m),N(beta),   beta=N delta.

This is a closed tensor contraction identity, not a projection through an
overcomplete frame. In the quadratic case, T_N and the source Q_N both have
dimension 9^N, and all their positive power traces agree. Newton identities
then give the same characteristic polynomial, including zero eigenvalues.
No extra hidden-state eigenmodes are counted.

The local MPO matrices are the actual nonnegative 25-by-25 matrices

    C_(x,z)=G (L_x tensor R_z).

Their virtual dimension is 25. The identity does not remove the 9^N history
dimension or the 25^m virtual dimension of a spatially powered MPO.
`positive_transfer.py` compares source Q_N power traces for N=1,2,3 and
physical rings through 128 sites, and independently applies the physical
four-site gates. These finite orientation checks have beta<=0.003 and are
not cold bootstrap inputs. All scalar weights are retained.

In particular, temporal doubling requires Z_(2L)(2beta), represented by
2N time slices at fixed delta; it cannot be obtained by calling an additional
spatial power of T_N a temporal purity. The intended criterion needs
S(L,beta)=Z_(2L)(beta)/Z_L(beta)^2 and
T(2L,beta)=Z_(2L)(2beta)/Z_(2L)(beta)^2 at the specified common L,beta.

**4. The exact exponential is a different, 25-term local factor.** For
G_exp=exp(-delta h_M), the matrix A=4I-h_M is entrywise nonnegative. Hence

    G_exp=exp(-4delta) exp(delta A)

is entrywise nonnegative for every delta>=0. Let L_(a',a)=E_(a',a) be a
matrix unit and R_(a',a)[b',b]=G_exp[a'b',ab]. These 25 nonnegative pairs
reconstruct G_exp exactly. The same periodic contraction proof applies,
with 25^N histories, physical alphabet 25, and virtual dimension 25.

For completeness, this local rank cannot be reduced exactly below 25 for
delta>0. In the original real basis, G_exp is the matrix of the CP map
exp(delta L), L(X)=sum_i g_i X g_i^T. Its Kraus expansion assigns a strictly
positive coefficient delta^k/k! to every generator word of length k. The
exact source check finds cumulative word-span ranks 1,4,9,16,25 through
degree four. Thus its Choi Gram matrix is positive definite for delta>0;
realignment gives operator Schmidt rank 25. The unitary gauge preserves it.

`exponential_positive_gate.py` retains exp(-4delta), checks the 25-term
factor, and replays physical four-site closed traces. The peer's newer
589043-slice representative error count uses this exact exponential gate.
It must not be combined with the nine-factor quadratic representation.
That count is recorded as a peer-supplied interface, not rederived here.

**5. The attempted uniform local compression fails at an exact interface.**
Reshape the quadratic C into the cut

    M_((x,a),(z,b))=C_(x,z)[a,b],

where a,b run over the 25 virtual coordinates. The other tested cut exchanges
a,b. `exact_cut_certificate.py` uses the rational similarity above and checks
all 50625 support entries of each cut at delta=1/1000 and
delta=64/2387589. These are actual gates, not arbitrary witnesses.

For the first cut it constructs a 25-by-25 minor B, verifies its inverse
exactly, and obtains

    || |B^-1| |B| ||_infinity <= 2.

If an approximant satisfies |Btilde-B|<=epsilon |B| entrywise, then
||B^-1(Btilde-B)||_infinity <= 2epsilon. In particular epsilon<1/4 leaves
the minor invertible. Every approximant to the whole cut with that relative
entrywise error has rank at least 25. This excludes the attempted truncation
below 25 at the much smaller relative accuracy required by the naive uniform
tensor enclosure. The second cut has weaker but explicit exact rational
thresholds, all preserved in the result file. No floating SVD tail is used as
a proof.

The exact support also contains fooling sets of sizes 24 and 21. Each selected
entry is positive, while for every pair at least one cross entry is zero.
A nonnegative rank-one rectangle covers at most one selected entry. An
entrywise relative approximation with epsilon<1 keeps the same support, so
its nonnegative rank is at least the fooling-set size. For m independent
copies before contraction, the product fooling set has size 24^m (or 21^m).
This is a boundary-uniform obstruction for that uncontracted product matrix.
It is explicitly not a bound on a closed periodic trace computation, nor on
an approximation that exploits its actual environment or permits absolute
error on rare entries.

The chosen error contract explains why this obstruction matters. If M_v is
replaced by a nonnegative Mtilde_v satisfying
(1-epsilon)M_v<=Mtilde_v<=(1+epsilon)M_v for every local entry, monotonicity
of the full closed nonnegative contraction bounds Ztilde/Z between
(1-epsilon)^V and (1+epsilon)^V. For n sites, N slices there are V=nN/2
local folded cells. Taking epsilon=0.001/(nN) safely budgets logZ error
below 0.001. At the representative quadratic input n=128,beta=64,
N=2387589 this is approximately 3.27213e-12. That representative cost is
the earlier peer-supplied quadratic count, not rederived here, and is not a
complete budget for all three distinct bootstrap trace inputs.

**6. A physical one-spin PSD product frame cannot represent the cold state.**
This is a separate obstruction to transplanting the preceding corpus-first
EA/physical-frame construction. It is not an obstruction to the nonphysical
matrix-unit worldline factors in sections 2--4.

Use the ordinary spin-two AKLT tensor A_m obtained by coupling two virtual
spin-one labels to physical spin two and contracting one virtual leg with
the spin-one singlet matrix. `physical_frame_barrier.py` gives all five
3-by-3 matrices explicitly. Define E=sum_m A_m tensor A_m and the bond
insertion F=sum_(st,uv) h_(st,uv) (A_s A_t) tensor (A_u A_v), using the
original antiferromagnetic h, not h_M. Both E and F are rational 9-by-9
matrices. Their exact spectral projector data are

| eigenvalue of E | multiplicity | Tr(P F) |
| --- | ---: | ---: |
| 5/3 | 1 | -25/2 |
| -5/6 | 3 | -15 |
| 1/6 | 5 | -5/2 |

The projectors, commutation, normalization, and a fully independent four-site
physical-vector expectation are checked exactly. For every even n>=4 the
finite periodic state has positive squared norm

    Tr(E^n)=(5/3)^n [1+3*2^(-n)+5*10^(-n)] > 0

and energy per bond

    e_n=-(9/2) [1+(24/5)*2^(-n)+20*10^(-n)]
                 /[1+3*2^(-n)+5*10^(-n)] < -9/2.

The inequality is immediate: subtracting denominator from numerator leaves
(9/5)*2^(-n)+15*10^(-n)>0. This is an exact finite-ring trial family; no
thermodynamic-limit energy density or Heisenberg ground-state approximation
is assumed. The code also preserves the weaker legitimate 16-site block
tiling construction used before the direct formula was obtained.

Let rho_beta=exp(-beta H_n)/Z_n(beta), U_beta=Tr(H_n rho_beta). The Gibbs
variational principle and entropy S(rho_beta)<=n log 5 give

    U_beta/n <= n^-1 <H_n>_trial + log(5)/beta
              < -9/2 + log(5)/beta.

For any fully separable state sigma, every one-spin mean vector has length
at most two; hence <S_i dot S_j> >= -4 and Tr(H_n sigma)>=-4n. A finite
positive Taylor sum with 13 terms proves exp(161/100)>5, so log 5<161/100
with no floating logarithm premise.

Every bond has spectrum in [-6,4]. Consequently
||H_n+nI||<=5n. For D(rho,sigma)=||rho-sigma||_1/2,

    D(rho_beta,sigma) > [1/2-(161/100)/beta]/10.

This is positive whenever beta>161/50. At beta=64 it is 3039/64000,
or 0.047484375, on every even ring n>=4; at beta=96 it is 4639/96000.
Any nonnegative mixture of normalized one-spin PSD product-frame vertices
is fully separable and is therefore excluded at smaller trace distance.
The result does not automatically constrain an arbitrary history-space
cone, an entangled block frame, or a representation asked to return only
scalar partition functions. Entangled finite-temperature states can be
gapped or gapless; this witness proves neither alternative.

**7. The unresolved acquisition is global and task-specific.** Positivity
and periodic trace closure are acquired. The tested uniform local truncation
and one-spin physical-frame transplant do not supply an efficient cold
compression. A method that retains entangled boundary information and
certifies the actual omitted contribution to the three bootstrap traces
could escape both tests. Its cold trace/tail acquisition is not present in
this folder. Existing sign-free SSE and thermal MPO methods remain the
proper ordinary comparators; the exact local construction alone establishes
no speedup or new tractability class.
