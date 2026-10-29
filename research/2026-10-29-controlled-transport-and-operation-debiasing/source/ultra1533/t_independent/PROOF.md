# Exact harmonic-mixture sampling without a height gap

Status: new private construction; no independent acceptance or historical-priority claim.
The finite mathematical model is supplied, not inferred from a material.

## 1. Consequence and admitted model

The intended operation is a normalized independent equilibrium draw of a non-Gaussian
elastic field, including a nonconvex potential, without first estimating its height
relaxation time. This is a finite-graph result, not an infinite-volume local sampler.

Let G be a finite connected graph, with m>=1 edges and n>=2 vertices, and pin one height.
Write b_e in R^(n-1) for its oriented incidence columns. For x in {0,1}^m put

    k_e=1+(q-1)x_e,    L_x=sum_e k_e b_e b_e^T,    q>=1.

One can also add a fixed PSD grounding matrix to L_x. There are r independent
real field components conditional on x, with common edge conductances. The exact
joint density, with respect to counting measure on x and Lebesgue field measure, is

    prod_e p_e^x_e (1-p_e)^(1-x_e)
        exp[-(1/2) sum_e k_e ||b_e^T phi||^2],       0<p_e<1.

Consequently the field's edge potential is

    V_e(s)=-log[(1-p_e) exp(-||s||^2/2)+p_e exp(-q||s||^2/2)]

and the conductance marginal is

    mu(x) proportional prod_e p_e^x_e(1-p_e)^(1-x_e) det(L_x)^(-r/2).

All Gaussian integrations, the conductance representation, its attractive
single-site conditionals, and the transfer-current mechanism are established prior
(Buchholz, PTRF 2021, DOI 10.1007/s00440-020-01021-5). They are not the claimed new
step. The step below bounds the sum of influences at a common finite configuration
before taking a supremum, rather than exchanging those operations in Dobrushin's
entrywise criterion.

## 2. Conditional and monotonicity

Set rho=q-1. Given all other bits, let L_0 have edge e at its low value and put
R_e=b_e^T L_0^(-1)b_e. The determinant lemma gives

    h_e=P(x_e=1|x_-e)
       =p_e/[p_e+(1-p_e)(1+rho R_e)^(r/2)].                 (1)

Increasing any other conductance decreases R_e, so h_e increases. Thus a common
uniform single-site update preserves the coordinate order. This establishes the
monotone grand coupling required below, including arbitrary nonconstant p_e.

## 3. One-configuration influence sum

Fix a different edge f and allow its conductance to range continuously from 1 to q,
while holding all other current conductances fixed. Let L be this COMMON matrix,
including the current value k_e (which is either 1 or q when e!=f), and let

    R_ef=b_e^T L^(-1)b_f.

Differentiating (1) with respect to k_f gives

    d h_e/d k_f
      =(r rho/2) h_e(1-h_e)
         (b_e^T L_(e=1)^(-1)b_f)^2/(1+rho R_e).

If k_e=1, the fraction on the right is at most R_ef^2.
If k_e=q, Sherman--Morrison gives this fraction exactly

    R_ef^2/(1-rho b_e^T L^(-1)b_e) <= q R_ef^2.            (2)

The last inequality uses the variational effective-resistance bound
b_e^T L^(-1)b_e<=1/q for an edge of conductance q. It remains valid with a fixed
PSD grounding term. Since h_e(1-h_e)<=1/4,

    0<=d h_e/d k_f <= (r rho q/8) R_ef^2.                 (3)

For the entire edge frame B=[b_e], L>=B B^T, hence

    sum_e R_ef^2
      = b_f^T L^(-1) B B^T L^(-1)b_f
      <= b_f^T L^(-1)b_f <=1.                            (4)

Crucially the L in (4) is the SAME for every summand. Integrating over k_f in
[1,q], and omitting e=f, proves for EVERY pair x,y differing only at f

    sum_(e!=f) |h_e(x)-h_e(y)| <= c,
    c= r q(q-1)^2/8.                                    (5)

No pointwise Green-function decay, inverse height gap, dimension, vertex degree,
or summation of separately maximized influences is used. For r=1,q=2, c=1/4.
For r=3,q=2, c=3/4. The sufficient condition is c<1.

## 4. Global contraction and exact CFTP

At each step choose an edge uniformly and use a shared fresh uniform in (1).
For adjacent configurations, the changed edge is erased with probability 1/m;
the expected new disagreements elsewhere sum to at most c/m. Thus the expected
Hamming distance is at most

    gamma=1-(1-c)/m.

For any ordered configurations, telescope along a monotone Hamming path. The
same common-uniform update has expected Hamming distance at most gamma times
the previous distance. In particular, top/bottom chains started T steps ago obey

    P(not coalesced at time 0) <= m gamma^T
                                <= m exp[-(1-c)T/m].      (6)

Generate one sequence of independent edge/uniform maps indexed by negative times.
Run top and bottom through a window; if they disagree at zero, DOUBLE the window,
prepend new independent maps, and replay the SAME old maps. Once they agree,
every initial state agrees. The standard coupling-from-the-past theorem gives an
exact mu draw, not an unqualified burn-in approximation. Fresh whole words give
independent draws. Propp--Wilson CFTP and path coupling are ordinary ingredients.

An explicit conservative cost is available. Let

    L=ceil[m(ceil(log2 m)+1)/(1-c)].

Start with L maps and double. At level j>=1 the chance that this level is reached
is at most exp[-2^(j-1)]. Counting both extremal chains and all replays,

    E[number of single-state heat-bath evaluations] <=8 L. (7)

Indeed sum_(j>=1) 2^j exp[-2^(j-1)]<3, using e>2 and
2^(j-1)>=2j-2 for j>=3. This bound is deliberately conservative.

## 5. Access, exact arithmetic, and remaining cost

For a rational finite graph, rational q and p_e, maintain L^(-1) exactly by rank-one
updates. Each update uses O(n^2) rational arithmetic after initial inversion.
All current inverse entries are ratios of determinants of matrices whose entry
sizes are bounded by the supplied graph/input sizes; no uncontrolled accumulation
of precision is required. A fresh exact inverse is a slower equally valid option.

For r=1, deciding u<h_e requires only the RATIONAL comparison

    u^2(1-p_e)^2(1+rho R_e) < p_e^2(1-u)^2.              (8)

For general integer r use (1+rho R_e)^r in (8). A stored lazy fair-bit uniform
interval settles this comparison almost surely. At a fixed replay level each
threshold depends only on earlier maps, not its current uniform. The precision
tail per comparison is geometric. Combining its second-moment bound with (6)
by Cauchy--Schwarz pays a finite expected total number of fair bits, including
adaptive CFTP replays. This is a finite rational discrete-output algorithm;
seeded PRNG execution is only a deterministic diagnostic of that algorithm.

After the exact conductance draw, the conditional field is an ordinary normalized
Gaussian with covariance L_x^(-1), independently for r components. This completes
an ideal-real full-law operation. The later sibling quantized_field.py ACTUALLY
implements the finite-output completion, by exact rational LDL and strict outward
Box--Muller/floor decisions on persistent random-bit intervals; see FIELD_OUTPUT.
Gaussian factorization cost, output precision and large coordinate variances are
real costs. The update-count bound does not imply cheap sparse linear algebra or
volume-independent local output. TOTAL_COST supplies a constructive bit-cost
theorem and separates it from the native library's unproved CPU complexity.

## 6. Nonconvexity and limits of the source class

For r=1, q=2 and p=99/100, at s^2=2 log99 the two mixture terms have equal
posterior weight, so

    V''(s)=3/2-(log99)/2 < -1/2,

where log99>4. Thus the operation is not restricted to uniformly convex physical
potentials. This is softening, Gaussian-scale-mixture non-Gaussianity, NOT arbitrary
quartic hardening, Lennard--Jones interactions, defects, or a fitted real crystal.
Pinning removes the one exact translation zero mode; an arbitrarily small remaining
height spectral gap is admitted. Infinite-volume uniqueness/local sampling is not
inferred from this finite global update bound.

## 7. Strong ordinary comparison

An equally informed approximate conductance sampler can use exactly the same chain
and contraction bound: ceil[m log(m/epsilon)/(1-c)] updates give total-variation
error <=epsilon from any start. It may be cheaper than CFTP at an approximation
target; exactness, not an incumbent speed advantage, is the new consumer target.

Alternating Gaussian field draws with independent conductance draws conditional on
the field is the established powerful data-augmentation baseline. Preconditioned
Langevin/HMC, Gaussian sampling, determinant updates, and perfect sampling must not
be replaced by a deliberately slow unpreconditioned height dynamics comparator.
No claim that the present implementation beats those methods at equal accuracy is
licensed by the theorem. The supplied finite graph/model itself is its acquisition
input. Real-material fitting, quantum nuclei and continuum limits are unacquired.

## 8. Frame form (same proof, no graphical assumption)

Replace the incidence columns by ANY supplied real spanning frame b_e and use
L_x=A+sum_e k_e b_e b_e^T, with a fixed PSD A and SPD baseline. Equations (1)--(7)
are unchanged: L>=sum b_e b_e^T and k_e b_e b_e^T<=L are the only matrix inputs.
For exact code/bit complexity take a rational frame and rational A. This is a
normalized sampler for centered finite Gaussian ridge-mixture models. It does not
admit a linear field, arbitrary shifted mixtures or an unknown frame. The current
implementation/receipts specialize to graph incidences, A=0, and constant p_e.
