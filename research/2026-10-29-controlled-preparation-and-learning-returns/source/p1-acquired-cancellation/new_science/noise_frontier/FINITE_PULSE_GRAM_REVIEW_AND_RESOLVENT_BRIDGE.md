# Finite pulse certification: independent proof and robustness

29 October 2026. Independent causal-noise review/construction of the root's
reversible predictive-space idea. Root and this frontier independently reached
the finite-amplitude, finite-duration refinement. Root then introduced the
exponential-clock resolvent improvement, independently verified here. No
unchanged predecessor is re-audited. No historical priority is asserted.

## 1. Source and physical interface

Q is a conservative CTMC generator on a finite or countable space, reversible
for probability pi, with outgoing rates at most Lambda. Thus Q is bounded and
self-adjoint on L2(pi), with spectrum in [-2Lambda,0]. Visible label a(x) has
k values; P_b multiplies by 1_{a=b}. The stipulated physical control is

    q^h_xy=q_xy h(a(y))/h(a(x)), x!=y, h_b>0,                  (1)

with the diagonal changed to minus the outgoing sum. It changes energy by
-2 tau log h(a), keeping the symmetric kinetic prefactor fixed. Local detailed
balance alone does NOT supply this particular rate law: it must be physically
warranted or acquired. Lambda bounds hidden rates, not only visible jumps.

Let V be finite dimensional, contain 1, and be invariant under Q and every
P_b. Its orthogonal projection P commutes with these self-adjoint operators.
No hidden-state-count bound is assumed. Basis f_1,...,f_r must be actual
conditional means of implemented bounded baseline future reports, with known
linear-combination coefficients. Stationary reversal gives past reports with
the same conditional mean, including the correct physical parity. This makes
their bilinear Gram moments observable without cloning a hidden state.

## 2. One finite field and an independent clock

Choose h=1+c1_b with c!=0 and c>-1, H_b=I+cP_b, and Q_b=Q_h. The weighted
inner product is <f,g>_b=<f,H_b^2 g>_pi, with no normalization needed. Q_b is
self-adjoint and nonpositive in it, since pi h^2 is reversible. Because P
commutes with H_b and its inverse, P is also the weighted orthogonal projection.

Apply the field for an independent exponential time E of rate alpha>0:

    S_b=E exp(E Q_b)=alpha(alpha I-Q_b)^-1.                    (2)

Two INDEPENDENT clocks in succession give S_b^2. Reusing twice the same
duration instead gives E exp(2E Q_b), which is different. Clocks must be
independent of state and reports, not physical-path stopping times.

S_b is positive, self-adjoint and contractive in the weighted space. If
R=max(h)/min(h), its spectrum lies in [a,1], with

    a=alpha/(alpha+2Lambda R).                               (3)

For c=1 and alpha=4Lambda>0, R=2 and a>=1/2. Mean pulse time is 1/alpha;
two clocks use mean 2/alpha. Lambda=0 means Q=0 and is treated separately.

Acquire the matrices

    G_b(i,j)=<f_i,H_b^2 f_j>_pi,
    K_b(i,j)=<f_i,H_b^2 S_b f_j>_pi,
    D_b(i,j)=<f_i,H_b^2 S_b^2 f_j>_pi.                        (4)

Each trial uses a baseline past report, the visible CENTER weight h(a(X_0))^2,
one or two physical random-clock pulses, and a baseline future report after
the field stops. No midpoint sensor is needed. Weighting is postprocessing of
a baseline-prepared trial, not physical preparation of pi_h. No microscopic
reset occurs between pulse durations. The report functions must actually be
paired to the same center state in the stated trial, not substituted marginals.

## 3. Exact Gram identity and closure

The residual

    R_b=D_b-K_b G_b^-1 K_b                                   (5)

satisfies

    R_b(i,j)=<(I-P)S_b f_i,(I-P)S_b f_j>_b.                   (6)

Indeed D_b=<S_b f_i,S_b f_j>_b. The projected coefficient matrix is
G_b^-1 K_b, whose Gram matrix is K_b^T G_b^-1 K_b; symmetry of K_b and
orthogonal Pythagoras prove (6). Therefore R_b is PSD and

    R_b=0 iff S_b V subset V iff Q_b V subset V.              (7)

The last equivalence uses bounded invertibility and

    Q_b=alpha(I-S_b^-1).                                     (8)

The h=1 version certifies baseline Q invariance. A label projector has residual
J_b-J_b G^-1 J_b, where J_b=<f_i,P_b f_j>_pi. These criteria require actual
paired report moments. Exact zero is a population statement: finite confidence
intervals certify small leakage, not an exact equality.

## 4. Coverage of every energy amplitude

For arbitrary positive visible h, set H=sum_b h_b P_b. Direct rate algebra gives

    Q_h=H^-1 Q H-H^-1 M_(Qh),                                (9)

where M_g is multiplication by g. For the field h=1+c1_b,

    H_b Q_b=Q H_b-c M_(Q1_b).                               (10)

If (7) holds, this identifies invariance of the missing multiplication
M_(Q1_b). Testing k-1 labels is enough because sum_b Q1_b=0. Formula (9) then
gives invariance for ALL positive fields, including untested amplitudes.

In coefficient coordinates C_b=G_b^-1 K_b and

    L_b=alpha(I-C_b^-1),
    M_(b,V)=(Q_V H_(b,V)-H_(b,V)L_b)/c.                       (11)

These determine (9) on V. No derivative, matrix logarithm, vanishing pulse
duration or hidden-state-count bound is used. The source supplies a positive
realization of the visible laws in the exact case. The r predictive coordinates
need not be probabilities of r classical states.

## 5. Quantitative inverse bridge

In the weighted space let C=P S_b|V, B=(I-P)S_b|V. The acquired Gram residual
gives

    epsilon^2=||B||_b^2=lambda_max(G_b^-1/2 R_b G_b^-1/2),
    c_min=lambda_min(G_b^-1/2 K_b G_b^-1/2)>=a.                (12)

Then the exact bounds are

    ||(I-P)Q_bP||_b <= alpha epsilon/(a c_min)
                                      <=alpha epsilon/a^2,  (13)

and, with Lhat_b=alpha(I-C^-1),

    0 <= Lhat_b-PQ_bP,
    ||Lhat_b-PQ_bP||_b <= alpha epsilon^2/(a c_min^2)
                                      <=alpha epsilon^2/a^3.(14)

Proof. Write S=[[C,B*],[B,D]] and
E=(D-BC^-1 B*)^-1=(I-P)S^-1(I-P). Positivity gives ||E||<=1/a. The block
inverse identities are

    (I-P)S^-1P=-E B C^-1,
    P S^-1P-C^-1=C^-1 B* E B C^-1.

Insert (8). This proves (13), (14), and the positive sign of the bias. The
acquired c_min can improve the bound, but cannot replace a: unseen modes may
have smaller spectrum than the compressed matrix. A true Lambda or another
FULL-operator bound is still needed.

By (10), in baseline norm,

    ||(I-P)M_(Q1_b)P||_pi
        <=max(h) alpha epsilon/(|c|a c_min),                 (15)

and the error in the compressed multiplication matrix from (11) is at most

    max(h) alpha epsilon^2/(|c|a c_min^2).                    (16)

Multiplication by H_b converts output weighted norm into baseline norm, and
||f||_b<=max(h)||f||_pi; this avoids an unnecessary squared condition factor.
Finite sample confidence intervals, Gram conditioning and arithmetic errors
must be added. An empirical negative eigenvalue is not negative physical
leakage: one needs an upper confidence bound on the true PSD residual.

## 6. Deterministic-duration alternative

If S=exp(delta Q_b), the same weighted Gram residual holds, with
a=exp(-2Lambda R delta). The exact reduced generator is delta^-1 log C, using
the real principal logarithm of a matrix similar to symmetric positive definite.
Independent ordinary proofs give

    ||(I-P)Q_bP||_b <=epsilon/(delta a),                      (17)
    0<=log C-P(log S)P,
    ||delta^-1 log C-PQ_bP||_b<=epsilon^2/(2delta a^2).        (18)

For (17), [log S,P] is the integral of
(S+t)^-1[S,P](S+t)^-1. Its norm is <=||[S,P]||/a; for self-adjoint S the
commutator norm equals the omitted-block norm. For (18), the Schur identity
shows

    P(S+t)^-1P-(C+t)^-1
     =(C+t)^-1 B*[(I-P)(S+t)^-1(I-P)]B(C+t)^-1.

It is positive, with norm <=epsilon^2/(a+t)^3. Integrate to get 1/(2a^2).
The exponential-clock variant avoids the logarithm and its exponential spectral
conditioning. A deterministic clock may nevertheless be physically simpler.

## 7. Conservative finite-snapshot guarantee

Here baseline invariance is EXACT and initialization is common pi. Approximate
baseline closure is not silently assumed exact. Let allowed fields have ratio
at most R_*. Suppose finite reduced matrices Lhat_h satisfy uniformly

    ||Q_h I_V-I_V Lhat_h||_(V->L2(pi))<=eta,
    ||Q_h||,||Lhat_h||<=M.                                  (19)

I_V is inclusion. Equations (9), (13)--(16), plus matrix errors can supply eta.
The native bound ||Q_h||<=Lambda(3R_*-1) follows from
||H^-1QH||<=2Lambda R_* and ||(Qh)/h||_infinity<=Lambda(R_*-1).
The estimated matrices need their own norm bound. Duhamel gives

    ||exp(tQ_h)I_V-I_V exp(t Lhat_h)||<=t eta exp(Mt).          (20)

This also holds for measurable time-varying fields under the same uniform
bounds and physical well-posedness. Label measurement P_a has norm <=1 and
preserves V. For at most m label snapshots in total time T, each specified
label word probability is a product of propagators and projectors between
initial and terminal 1. Telescoping (20) bounds each word error by
T eta exp(MT), including history-selected fields. There are at most k^m words:

    L1(complete signed record error)<=k^m T eta exp(MT).       (21)

Next snapshot times can depend on charged reports, with at most m snapshots
and total T. Common standard-Borel sensor reports from the current visible
LABEL and earlier history can be added. For each fixed label word, integrate
the common normalized report kernels; uniform (20) retains (21), without
counting the report alphabet. Hidden-state sensors and uncharged continuous
event-triggered timestamps are excluded.

If the reduced record is positive and normalized, half (21) is TV error.
Without positive realization, (21) is an L1 bound for a SIGNED prediction and
controls bounded consequences by their sup norm times (21). Per-query clipping
does not create one consistent physical model for all policies. Exact closure
has the positive source realization from Section 4.

The k^m dependence is explicitly conservative. No efficient snapshot-count
scaling is proved. A stronger instrument norm or positive completion could
improve it; a hidden-dimension-free population theorem is not a free finite
precision algorithm. This limitation is consequential for large control trees.

## 8. Original weak-pulse check and novelty scope

For A_b=[Q,P_b]-M_(Q1_b), A_b*=A_b-2[Q,P_b]. The commutator preserves V, so
the omitted block has the needed adjoint symmetry. Therefore the root's original
sequential weak-pulse Gram residual is correct. Finite weighted pulses improve
the acquisition contract, and root's independent exponential clock gives the
stronger rational recovery above. Neither needs a third independent microscopic
future or state cloning.

Strong conventional comparators include spectral predictive-state/observable
operator methods, coarse-grained nonlinear response, matrix inverses and Schur
complements. The proposed addition is the physical generator identity together
with finite reversible-pulse Gram certification of an entire continuous energy
family, without a hidden-state-count bound. Matrix algebra and ordinary
likelihood reweighting are not claimed inventions.

## 9. Controlled future words and constructive exact label closure

The root's new controlled-test acquisition is correct. If O_i is a finite word
of physical pulse resolvents and visible projectors, f_i=O_i1 lies in [0,1].
Detailed balance gives S_h^*=H^2 S_h H^-2 in baseline L2(pi). Thus

    <f_i,T f_j>_pi=<1,O_i^* T O_j1>_pi

is a single chronological forward experiment: reverse the word O_i, replace
each adjoint pulse by the SAME physical pulse with visible endpoint weights
h(start)^2/h(end)^2, then apply T and O_j. No hidden reversal or clone is used.
Each endpoint ratio is at most R^2, so a word of ell adjoint pulses has weight
at most R^(2ell). Statistical range, dynamic range and implementation cost pay
this factor. All pulse clocks are independent fresh apparatus clocks. Appending
S_h f_i is an implementable new test if its residual proves it lies outside V.
Finite controlled predictive dimension guarantees eventual exact rank saturation
under exhaustive expansion; there is no promise that this dimension is small
or finite for every source.

Exact label closure can be BUILT instead of inferred. Replace any finite test
family g_i including1 by all P_a g_i. Their span contains1, is exactly invariant
under every P_a, and its functions are implemented with a current-label prefix.
This costs at most a factor k in dictionary size. Choosing a well-conditioned
basis still uses acquired Gram information and finite-rank uncertainty.

With this construction, the weighted pulse formulas remain valid even if Q
invariance is approximate: only label invariance was needed for P to be weighted
orthogonal. Let ell_0,d_0 bound baseline generator leakage and inverse-compression
error; let ell_b,d_b be the corresponding weighted pulse bounds. Equation (10)
then yields

    ||(I-P)M_(Q1_b)P||_pi <=max(h^b)/|c_b| (ell_0+ell_b),

and Mhat_b=(Lhat_0 H_b-H_b Lhat_b)/c_b has compressed multiplication error
at most max(h^b)/|c_b|(d_0+d_b). This uses H_b to convert output weighted
norm directly, avoiding an unnecessary extra condition factor.

For h^b=1+1_b the leakage bound is 2ell_0+2ell_b. Acquire k-1 fields and set
Mhat_k=-sum_(b<k)Mhat_b. For target min h=1,max h<=R, the uniform generator
leakage is at most R ell_0+(R-1)sum_(b<k)(2ell_0+2ell_b); the analogous
compressed matrix error replaces ell by d. Their sum supplies Section7's eta
without assuming exact baseline dynamics. True Gram leakage upper bounds and
finite estimator errors must be accounted separately.

## 10. Independent check of root's stronger full visible-path bound

Root's new killed-block construction removes the snapshot-count limitation of
Section7. Here is its ordinary verification. Let P be exactly label-closed,
d0=||(I-P)QP||_pi, and let Dkill bound the omitted block of each controlled
within-label killed generator. The root's proposed conservative value

    Dkill=R d0+(R-1)sum_(b<k)(2d0+4D_b)

is valid if D_b is pulse leakage in its weighted norm. Section9 gives the slightly
stronger 2d0+2D_b with the same definition. These bounds concern compression of
the TRUE operators; numerical acquisition errors are added afterwards.

Within a visible label a, Q_h,aa has unchanged off-diagonal rates q_xy and a
diagonal killed escape term. It is self-adjoint and nonpositive in baseline
L2(pi): its quadratic form is a within-label Dirichlet form minus the nonnegative
controlled exit rate. Its propagator is therefore contractive. This remains
true for time-dependent fields chosen from the already observed visible history,
because along one fixed label segment that history fixes a deterministic
measurable field and the energy estimate holds at each time.

The block-diagonal compression onto V plus V-perp preserves self-adjoint
negativity. The difference between the true and block-diagonal killed operators
has norm equal to their off-diagonal leakage, at most Dkill. Duhamel bounds a
killed segment discrepancy by its duration times Dkill, with no exponential
growth factor for these segments.

A jump a->b has operator J_ab^h=(h_b/h_a)E_a Q E_b. Its norm is at most
J=Lambda R: the baseline off-diagonal rate kernel has L2(pi) norm at most
Lambda by the reversible row/column Schur bound. The difference from its
V/V-perp block-diagonal compression has norm at most R d0. Its two omitted
blocks are bounded by d0 because Q is self-adjoint and P commutes with labels.
The norm of that off-diagonal 2-by-2 block is the maximum, not the sum.

For a specified visible path with m jumps and total duration T, telescope its
chronological killed-propagator/jump product. Initial and terminal label
indicators have norm at most1. The resulting density error is at most

    T Dkill J^m + m R d0 J^(m-1).

At m=0 the second term is absent. History-dependent control causes no extra
derivative term: conditional on the recorded prefix it selects the same physical
field on both sides of each product. Bounded ratios and rates ensure nonexplosion.
There are k(k-1)^m label words and the ordered jump-time simplex has volume
T^m/m!. Summing gives the COMPLETE SIGNED PATH L1 bound

    k T [Dkill+(k-1)R d0] exp((k-1)Lambda R T).               (24)

The series is absolutely convergent. All bounded measurable visible-path payoffs
inherit their sup norm times (24), uniformly over the stated visible-history
feedback. This includes event-triggered visible decisions whose information is
the charged complete label path. It does not include hidden-state access or
an uncalibrated control law. The compressed object is a signed prediction unless
a positive realization is separately supplied; (24) does not change that caveat.

If numerical killed-block errors are at most zK and jump-block errors at most
zJ, a safe extension replaces Dkill by Dkill+zK, R d0 by R d0+zJ, J by J+zJ,
and multiplies by exp(zK T). The acquired matrices need consistent label blocks.
This is one explicit way to justify root's stated extra-error exponent. A claim
using a single Z must specify which block errors it bounds.
