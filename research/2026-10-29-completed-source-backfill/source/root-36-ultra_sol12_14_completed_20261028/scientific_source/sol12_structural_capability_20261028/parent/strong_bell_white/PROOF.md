# A strong five-Bell source acquires an entire noise curve

Root construction using exact algebra and finite scalar certificates,
independent of the lead's entropy/purity envelope. No physical instrument,
unrestricted W3 or historical priority is claimed.

Let rho mix Weyl-Bell labels(00,01,02,10,11), weights(64,8,4,2,1)/79.
It has trace1 and both marginals I3/3. certify.py independently reconstructs

    N(rho)=I3/3 tensor M,
    M=sum p_ab |s_ab><s_ab|,
    s_ab=(|a+1>-omega^(-b)|a+2>)/sqrt2.

Define h(a)=Delta(rho+aI9), f(t)=tlogt. If lambda_j are M's eigenvalues,

    h(a)=sum_(five)f(a+p_i)+4f(a)+9f(a+1/9)
                         -6sum_(j=1)^3 f(a+lambda_j/3).

It is continuous at0, f0=0, and tends0 at infinity by trace cancellation.

## Exact finite critical points

Direct exact matrix algebra gives

    P(a)=det(aI3+M/3)=a³+a²/3+515a/37446+319/4437351,
    h'(a)=log[a^4 prod(a+p_i)(a+1/9)^9/P(a)^6].

P>0, so all positive critical points are positive roots of the rational
degree16 numerator difference R. The full Sturm chain records exactly2
positive roots, both simple and isolated with rational widths<2^-40:

    a1 approximately.008032290729, a2 approximately.063927431026.

R0 and its leading coefficient are negative. Endpoint signs give the
decrease/increase/decrease pattern. No later critical point is omitted.

Rational eigenvalue brackets and24-term atanh logs with geometric
remainders certify h0>1/5, h(a1)>1/5 and h(a2)>1/5. Lower displays are
.22284441305,.20668964772,.21745288210; rational JSON endpoints govern.
Thus h(a)>0 for EVERY finite a>=0, with h>=1/5 on[0,1/16].
The last segment decreases to0. No white-noise grid or floating entropy
sign receives this half-line.

All matrices are exact Q(omega); the cubic and R are derived from M.
Fraction products handle negative-log signs and f0 exactly. A first
execution hit a SymPy Boolean-sum type error before any certificate;
the implementation was corrected. No conclusion relies on that failed run.

## Inherited common-bath operation, now with a strong coherent seed

The reviewed current corpus identity for ANY base with a paid whole curve is

    Delta(rho tensor U+I9 tensor V)
      =q'(0+)h0+integral h(t)dq'(t), q(t)=Tr(tU-V)_+.

Its measure is positive for arbitrary finite PSD, possibly noncommuting
or singular U,V. Therefore every such bath source has nonnegative deficit;
for U!=0 it is positive because h is positive at every finite t.
The identity is inherited at Git8d51d60762b3ee28c10aaaa56e1b92da119dc1cc,
not rediscovered. All-white positivity does not follow from h0 alone.

For U=P+=(1/2)[[1,1],[1,1]], V=diag(1,0), q'(0+)=1/2. The exact
18-dimensional source Z=rho tensor U+I9 tensor V consequently has
Delta(Z)>=1/10. Its trace is10 and physical marginal(10/3)I3, so its
normalized antisymmetric-isometry extension has

    CMI>=log3+1/100,

with reference dimension6 and extension dimension54. No extra flag is needed.
The lower bound uses the positive atom only; the rest of the measure helps.
No physical state, bath or instrument is acquired.

The source violates reduction positivity by compression to kerV: it gives
rho/2, whose Bell eigenvalue64/79 exceeds1/3. Its Schmidt number is3 since
its Bell fidelity64/79 exceeds2/3; local reference compression cannot raise
Schmidt number. The singular lifted source has rank14, excluding the
faithful condition24 premise. Its physical01 block has nonzero square,
excluding the declared square-zero reset/bath package. Other positive
families or alternative projector factorizations are not classified.

## Reusable operation and costs

For a supplied rational Bell mixture with full-rank SIC output, the same
finite procedure derives a cubic and a degree<=16 derivative polynomial,
isolates ALL positive critical points, and bounds actual entropy there
and at0. Strict positive lower bounds receive the whole white curve.
An unresolved zero/too-small margin returns UNKNOWN at finite precision;
no generic polynomial precision or all-weight coverage is asserted.
The current executable is specialized to the stated strong source.

The actual exact run took about.354s including SymPy import and algebra,
excluding interpreter startup/initial stdlib imports. Inputs and inherited
theorem acquisition are separately charged. This buys a different output
than a single point entropy evaluation, not a speed separation.
The result covers this source and arbitrary common baths, not every
five-Bell white curve, all9 Bell mixtures, arbitrary Choi states, arbitrary
unflagged composition or a civilisation-level technology.
