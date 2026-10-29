# Predictive equivalence under finite clocks can force dissipation

29 October 2026, Brisbane. Root construction. Previous sufficient mean
records, positive completion and clock criteria remain unchanged.

## Scientific choice

A complete family of frozen controlled event laws can fail under temporal
composition; the independent controlled_frontier construction establishes
this with finite CTMCs and an additional switched assay. Controlled PSR
closure and likelihood reweighting have strong classical precedents.

The stronger opening concerns realization: a record can admit equilibrium
dynamics yet force positive, even divergent, Markov entropy production
under finite execution clocks. The exact bound ranges over EVERY finite
hidden dimension. Adding states cannot evade it. An entropic representation
and robust inequality make this an instance of a larger principle.

The result concerns implementing declared mean consequences. It does not
identify the original source, infer unknown actuator responses, or improve
mean evaluation over an ordinary reduced linear solve.

## 1. Definitions and physical scope

Let Q be a finite irreducible row CTMC generator, w>0 a calibrated
stationary measure, W=sum w and f_xy=w_x q_xy for x!=y. All states are
even under time reversal. Define unnormalized Markov entropy

    E=sum_{x<y}(f_xy-f_yx)log(f_xy/f_yx).                       (1)

Two zero flows contribute zero; exactly one positive flow gives infinity.
The stationary rate is E/W in nats/time. Multiplication by Boltzmann's
constant is thermodynamic only when states and reversed channels form a
faithful local-detailed-balance description. Unresolved parallel physical
channels or odd variables require separate treatment.

Partition into ports B and hidden I. Put L=-diag(w)Q, G=L_II and

    S=L_BB-L_BI G^{-1}L_IB,
    b_R=w_B-L_BI G^{-1}w_I,
    b_L=w_B-L_IB^T G^{-T}w_I,
    c=w_I^T G^{-1}w_I.

Let v_R=b_R-w_B, v_L=b_L-w_B and V=sum v_R=sum v_L=sum w_I.
Write F_ij=-S_ij off diagonal. Hidden rates are <=Lambda and port rates
<=ell_i. Spare native self-return budgets are

    a_i=w_i ell_i-sum_{j!=i}F_ij,   A=sum_i a_i.              (2)

Nonnegative a_i is necessary. All quantities have common fixed units.

## 2. Clock-boundary rigidity

Uniformize hidden excursions at rate Lambda. Let N count hidden ticks,
including virtual ticks; direct port jumps have N=0. For the stationary
excursion flux measure mu,

    Lambda V=integral N dmu,
    2 Lambda^2 c=integral N(N+1) dmu.                        (3)

Thus c>=V/Lambda, with equality iff N belongs to {0,1} almost surely.
An accessible hidden state with departure rate below Lambda admits a
virtual tick followed by another tick. A hidden-hidden edge also admits
N>=2. Irreducibility makes all hidden states accessible from some port
before the next port. Consequently equality forces every hidden rate
to equal Lambda and forbids every hidden-hidden edge. Hidden stars plus
direct port edges are therefore a forced architecture, not an assumption.

## 3. Entropic completion at the boundary

For star x with weight w_x, its normalized entrance and exit flow laws
alpha_x,beta_x satisfy

    f_ix=Lambda w_x alpha_x(i), f_xj=Lambda w_x beta_x(j).
    T_ij=Lambda sum_x w_x alpha_x(i)beta_x(j).               (4)

The record and budgets are equivalent to

    sum_x w_x=V,
    sum_x w_x alpha_x=v_R, sum_x w_x beta_x=v_L,
    T_ij<=F_ij (i!=j), T_ii<=a_i.                          (5)

Sufficiency is explicit: add direct flows D_ij=F_ij-T_ij. The port rate
is (sumoff F_ij+T_ii)/w_i. Eulerian F ensures balance even for unequal
loads. Define J(alpha,beta)=sum_i(alpha_i-beta_i)log(alpha_i/beta_i).
Then the full entropy is

    E=sum_{i<j}(D_ij-D_ji)log(D_ij/D_ji)
       +Lambda sum_x w_x J(alpha_x,beta_x).                 (6)

The factorization matters: averaged margins can have zero Jeffreys
divergence while every feasible factorization has positive cost.

Any finite finite-entropy realization compresses to <=m^2+1 hidden stars
without changing T or E, m=|B|. Apply Caratheodory to
(vec(alpha beta^T),J(alpha,beta)); the first block sums to one, so affine
dimension is <=m^2. This is an existence reduction, not an algorithmic
or coefficient-precision guarantee.

## 4. Binary inequality

For alpha=(p,1-p), beta=(q,1-q), put r=pq+(1-p)(1-q). Define

    g(r)=4 sqrt(1-2r) atanh(sqrt(1-2r)) for 0<r<1/2,
    g(r)=0 for r>=1/2, and g(0)=infinity.

Then J(alpha,beta)>=g(r). For d=|p-q|, u=(p+q)/2 and r<1/2,

    d^2=1-2r+4(u-1/2)^2,
    J=d log[(1-r+d)/(1-r-d)].

At fixed r the last expression increases with d; its minimum is u=1/2.
The function g is convex nonincreasing. With x=sqrt(1-2r),

    g'=-4[atanh(x)/x+1/(1-x^2)],
    g''=4[(x/(1-x^2)-atanh(x))/x^3+2/(1-x^2)^2]>=0.

Left derivative at 1/2 is -8, right derivative zero. Endpoint cases
follow by limits.

## 5. Exact frontier over all finite hidden dimensions

Fix

    S=[[1,-1],[-1,1]], w_B=(1,1),
    v_R=v_L=(1,1), c=2, Lambda=1.

Give both ports ceiling ell>=1 and set A=2(ell-1).
For ell=1, positive realizations exist but all have infinite E.
For 1<ell<3/2 the exact minimum is

    E_min=4d log[(1+d)/(1-d)], d=sqrt(3-2ell)=sqrt(1-A).      (7)

For ell>=3/2 the minimum is zero. Divide by W=4 for stationary rate.

Proof: clock rigidity applies since V=2. Each star has return fraction
r_x with sum w_x r_x<=A. Equations (6), the binary inequality and Jensen
give E>=sum w_x g(r_x)>=2g(A/2), which is (7).

Attainment: two ports and two hidden states each have weight one.
Around the alternating four-cycle use clockwise rate p=(1+d)/2 and
counterclockwise rate q=(1-d)/2. Add symmetric direct port flow
2pq=A/2. Hidden rates are 1; port rates are 1+2pq=ell. The record is
exactly the one above. Four cycle edges each contribute
(p-q)log(p/q). Rational p gives a rational generator.

At ell=3/2 merge the identical stars into one hidden state of weight
two, alpha=beta=(1/2,1/2), plus symmetric direct flow 1/2. It has E=0.

As A->0, E_min-4log(4/A)->0. Near A=1,
E_min=8(1-A)+O((1-A)^2). Every member has mean 2 to either individual
port from stationary law conditioned outside that target, and the same
previously declared passive-composition mean consequences.

## 6. Robust inequality with positive clock slack

Let delta=Lambda c-V>=0 and h_1=mu{N=1}. Set

    h_0=Lambda max(V-2delta,0)=max(3Lambda V-2Lambda^2 c,0).

Since N<=N(N-1) for N>=2, (3) gives

    h_1=Lambda V-integral_{N>=2}N dmu>=h_0.                 (8)

One-tick excursions i->x->j have flux f_ix f_xj/(Lambda w_x).
If a_x=sum_i f_ix, b_x=sum_i f_xi, their total flux is
h_x=a_x b_x/(Lambda w_x), with entrance alpha_x(i)=f_ix/a_x and
exit beta_x(i)=f_xi/b_x. Omit h_x=0.

The KL divergence of the stationary excursion flux measure from its
reversal is E: path-density ratios telescope stationary weights, and
stationary expected jump counts give every edge contribution in (1).
Direct port edges are zero-duration excursions. Uniformization adds
self ticks with likelihood ratio one. One-tick paths through a specified
x form a reversal-invariant subset contributing h_x J(alpha_x,beta_x).
Other reversal-invariant subsets have nonnegative relative entropy.

Hence E>=sum h_x J(alpha_x,beta_x). For two ports the one-tick return
flux is <=A. Jensen and monotonicity imply, for h_0>0,

    E>=h_1 g(A/h_1)>=h_0 g(A/h_0).                         (9)

The last step uses that h*g(A/h) is nondecreasing. The right side is
zero if A/h_0>=1/2. At delta=0 it is exact for the stated two-port
record; at positive slack it is a bound, not an asserted optimum.
The new path-measure use was independently reviewed in
controlled_frontier/ROBUST_ENTROPY_REVIEW.md. Its120 exact finite-generator
controls include positive clock slack from hidden transitions and slower
clocks. Define the bound as zero when h_0=0; do not form0*g(0/0).

## 7. A multiport cut witness

For any nontrivial partition B=C union C^c, aggregate each one-tick
entrance/exit law to two groups. Jeffreys divergence decreases under
aggregation. Same-group one-tick flux is bounded by

    B_C=A+sum_{i!=j; i,j in the same group}F_ij.

Thus E>=h_0 g(B_C/h_0), h_0>0. Maximize over cuts by ordinary methods.
No new combinatorial optimization algorithm is claimed.

The independent thermodynamic branch gives a complementary logarithmic
bound using a hidden-entry-flux floor from the uniformized moment
envelope and a boundary-edge Hellinger inequality. Use the stronger
applicable bound.

## 8. Acquisition and contribution boundary

Theorems take calibrated records and rate ceilings as exact mathematical
input. Samples do not certify exact equalities, exact zeros or unknown
physical clocks. For interval records minimize a valid lower bound over
all compatible parameters; (9) and the cut version supply a route, not
an executed acquisition.

Entropy production, Jeffreys divergence, path contraction, uniformization
and Caratheodory are classical. The proposed addition is the exact
constraint from a consequence-sufficient record and port/hidden clock
budgets over all finite hidden dimensions. Priority is unsettled.
A conventional reduced solve remains preferable for mean evaluation.

