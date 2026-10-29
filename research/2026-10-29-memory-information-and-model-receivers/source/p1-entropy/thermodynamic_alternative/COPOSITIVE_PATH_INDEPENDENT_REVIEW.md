# Independent review of root's copositive path certificates

29 October 2026, Brisbane. Reviewed Sections 3-6 of the branch-root
COPOSITIVE_PATH_CERTIFICATES.md. The quantitative constants and the
geometric killed-process argument are valid under the stated finite,
stationary, even-state CTMC and resolved-native-excursion hypotheses.
This is an ordinary internal reconstruction, not external acceptance.

## 1. Full fixed-duration paths

Let q*_xy=pi_y q_yx/pi_x. Stationarity gives lambda*_x=lambda_x. Define
Q_geo with off-diagonal sqrt(q_xy q*_xy) and original diagonal -lambda_x.
Cauchy-Schwarz gives row sums <=0, and pi_x Q_geo,xy is symmetric.
Thus this is a reversible sub-Markov generator with additional killing.

A full path with fixed jump states and waiting durations has geometric
weight exactly sqrt(p q), where p is its stationary forward path density
and q the stationary time-reversed density. All holding exponentials
coincide. The path endpoint factor is correct because both forward and
time-reversed processes start at pi. There is no missing escape-rate or
normalization correction.

Under a normalized emission kernel, summing the observed endpoint-pair
matrix gives total mass 1 for the original law and Hellinger affinity
for Q_geo. Entrywise arithmetic-geometric mean gives

    Delta=C_sym-C_geo >=0,
    D=sum Delta=1-affinity.

The microscopic reversal is an involution. Therefore the two directed
relative entropies agree, and

    sigma t = (1/2) integral (p-q)log(p/q)
             >=2 integral(sqrt(p)-sqrt(q))^2=4D.

The scalar inequality has the correct factor four:
(a-b)log(a/b)>=4(sqrt(a)-sqrt(b))^2. It approaches equality when a/b tends
to one. The resulting lag certificate sigma>=4gamma/(t h_minus) is valid.

The emission channel must be normalized and time-reversal compatible as
stated. For stochastic emissions the displayed two-time formula corresponds
to independent emissions conditional on the two microscopic endpoint
states. Unnormalized features need their own mass bound. Independent
stationary preparation or a valid dependence-aware acquisition proof is
still needed for statistical confidence from lag samples.

## 2. Native flux measures: no missing factor of total departure rate

Use unnormalized weights w and microscopic edge flux f_xy=w_xq_xy.
For a path beginning at port i, crossing hidden states and next arriving
at port j, the excursion intensity density starts with w_i q_ix rather
than with a normalized initial-state probability. Its reverse has the
corresponding w_j factor. Their ratio telescopes into stationary edge-flow
ratios. Every stationary microscopic edge traversal belongs to exactly one
native excursion, and finite-state hidden transience makes the expected
occupation/jump totals finite. Hence

    integral log(dmu/dmu^rev) dmu = E=W sigma.

The total flux mass is R=sum_i w_i lambda_i for both measures. Equal mass
means the optional -mu+mu^rev terms in generalized KL cancel. This is an
unnormalized identity. Dividing by R yields entropy per native departure;
it does NOT yet yield entropy per physical time.

Direct port-to-port jumps are included in this full measure, with duration
zero. Self returns are valid only through positive-duration hidden paths.
These conventions agree with the existing clock-completion interface.

## 3. Geometric excursion kernel and complete positivity

Let f_geo,xy=sqrt(f_xy f_yx). Its associated q_geo=f_geo/w has original
escape diagonals. In the hidden block, write D=diag(w_I),

    H_geo=D^1/2(-Q_geo,II)D^-1/2,
    A_geo=(f_geo,ix)_{i in B,x in I}.

H_geo is symmetric and -H_geo is Metzler. Therefore at every t>=0,

    K_geo(t)=A_geo D^-1/2 exp(-H_geo t) D^-1/2 A_geo^T
            =B_t B_t^T,
    B_t=A_geo D^-1/2 exp(-H_geo t/2)>=0.

This is the geometric mean of FULL microscopic excursion intensities,
summed over unobserved paths, not the geometric mean of their already
coarsened endpoint densities. That distinction is load-bearing: summation
and geometric mean do not commute. The proof uses the former correctly.

The hidden killed block is transient. A closed geometric component with
zero killing would saturate the row Cauchy-Schwarz inequality at each
state, forcing equality between original and reversed outgoing rows;
it would therefore be closed in the irreducible original source. This is
impossible for a component wholly inside I. Alternatively all needed
weighted integrals are dominated by the finite original/reversed path
moments via arithmetic-geometric mean.

For 0<=phi<=1 supported on positive duration, integrating gives CP
C_geo,phi and nonnegative entrywise deficit. Its total is exactly

    D_phi=(1/2) integral phi(tau)(sqrt(dmu)-sqrt(dmu^rev))^2,

which is at most the same expression without phi. Thus E>=4D_phi.
For a copositive H, its negative entries control the deficit:

    gamma=-<H,C_phi,sym>
          <=-<H,Delta><=h_minus D_phi.

Therefore E>=4gamma/h_minus. No assumption of symmetry of the observed
kernel is needed. Symmetric H automatically ignores its antisymmetric
part, so using C_phi or C_phi,sym in the pairing is equivalent.

The positive-duration exclusion is essential. A reversible direct-jump
flow matrix need not be CP; treating that zero-time atom as a hidden
duration bin would invalidate the certificate. A strictly positive lower
bin edge is a practical way to separate the atom if timing resolution
cannot distinguish arbitrarily short excursions from direct jumps.

## 4. First-moment certificate

Let h=sqrt(p)-sqrt(q) on microscopic excursion space. Reversal preserves
duration, and both measures have second duration moment 2c. Then

    D1=(1/2) integral tau h^2,
    D1^2 <=(1/4)(integral tau^2 h^2)(integral h^2)
          <=(1/4)(4c)(E/2)=cE/2.

The inequalities use h^2<=p+q and the symmetric-KL bound E>=2 integral h^2.
Since M_geo is CP and gamma_M<=h_minus D1,

    E>=2 gamma_M^2/(c h_minus^2).

Both the factor 2 and the single power of c are correct. This bound is
valid but no optimality is established. Acquisition of c cannot be supplied
by a bounded finite-window score; the finite-window certificate genuinely
avoids this extra moment obligation.

## 5. A sharpness family for the coefficient four

The fifteen-state five-cycle construction extends continuously. For any
0<d<1, put p=(1+d)/2, q=(1-d)/2. On each cycle edge use two mirror hidden
stars, each of weight 1/(1-d^2), all at rate 1. The residence matrix is

    M(d)=I+[(1+d^2)/(2(1-d^2))] C5.

Its Horn gap is gamma=10d^2/(1-d^2). The full positive-duration kernel
has K(t)=exp(-t)M(d), and its entropy is

    E(d)=20d/(1-d^2) log[(1+d)/(1-d)].

With phi=1 on all positive durations,

    E(d)/gamma = (2/d)log[(1+d)/(1-d)] ->4 as d->0.

For sufficiently small d the matrix remains strictly positive definite,
and the complete observed native event-time law remains time-reversal
symmetric. Thus the universal coefficient four cannot be increased, even
within this symmetric PSD observed-law subclass. This is an asymptotic
sharpness theorem, not a finite-sample claim. If the bin is cut at fixed
finite h, its gap is multiplied by 1-exp(-h), so this same limiting example
does not saturate the constant for that narrower fixed-bin subclass.

## 6. Statistical and physical units

Flux-weighted resets, i sampled with rho_i/R, reproduce the normalized
native excursion measure. The score expectation is <H,C_phi>/R. Hence
E/R>=4[-EY]/h_minus is dimensionless entropy per departure and does not
require a tail envelope. Equal reset probabilities are appropriate only
when equal flux weights are supplied or independently certified.

The renewal-reward identity for the complete cycle, including the initial
port hold, is E[cycle duration]=W/R. Converting the bounded-score certificate
to sigma requires this time normalization or an honest upper bound on it.
It is not acquired by the bounded endpoint/bin score alone. Timing noise
depending on hidden state or endpoint is not automatically compatible with
the same phi(t); its effect must be bounded or modeled.

All thermodynamic interpretations retain the stated even-state reversal
and stationary microscopic Markov hypothesis. The arguments do not exclude
equilibrium models with a different odd-variable reversal or a different
native observation interface.
