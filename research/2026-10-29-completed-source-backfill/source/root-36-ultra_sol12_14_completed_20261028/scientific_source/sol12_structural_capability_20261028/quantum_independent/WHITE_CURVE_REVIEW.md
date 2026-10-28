# Independent review: condition-number-free entire white curve

Status: **ACCEPTED at the stated finite-dimensional scope.** I whole-read
`../parent/full_white_ray/KAPPA_FREE.md`, its original `PROOF.md`, its actual
compiler, and the inherited sol11 general-positive-ray and common-bath
statements. The local general-ray theorem, scalar baseline bound and
positive common-bath identity are explicit inherited premises. This review
does not relabel those premises as newly proved here.

## Noncommuting finite increments

For positive definite X, the correct scalar trace derivative is
`d Tr f(X+tY)/dt=Tr[Y(log(X+tY)+I)]` for f(x)=x log x. No operator identity
`Df(X)[Y]=Y(logX+I)` is asserted. Convex tangent bounds give the input and
conditional-expectation increments from below. Since H is a density
matrix, `0<=NH<=I`; integrate the N increment and use operator monotonicity
of log against the positive NH. This gives the claimed upper increment at
`NA0+(a+eps)I`, without commuting H with A0. Trace preservation cancels
the three constant derivative terms. E and N are self-adjoint here, so
the displayed L_eps expression is correct.

`N*R=(I+3P)/4` and `N*S=3Q/4` use the normalized P and antisymmetric R,
with ranks r and3r, respectively. After diagonalizing C only (not H), the
P coefficient at eps0 is nonnegative because its numerator minus
denominator is `(4/3)ac`. The Q coefficient is negative precisely when
`0<c<3a`: squaring its positive ratio reduces the sign to
`c(c-3a)/9`. Its lower bound `-c/(6a)` follows by differentiation, with
derivative `x(x+7)/[6(x+3)(x+1)]` for the corrected function.

The leakage weights `w_j=Tr[Q(I tensor |j><j|)H]` satisfy
`0<=w_j<=1`, sum ell, and need not diagonalize H. Replacing
`c_j w_j` by `c_j^2/m` is conservative and valid. On the negative sector
`c<3a`, the scalar baseline contribution is at least `3c^2/(280a)`.
Hence the first-order charge is at most
`(140/9)(eps/m)h0(a)`. This argument keeps the actual c_j weights and
does not silently introduce a maximum eigenvalue of C.

At finite eps the extra P and Q charges are each bounded by `2eps/a`.
Multiplication by eps and use of **TrH=1**, rather than the dimension,
therefore costs `2eps^2/a`. This checks the claimed trace factors.

## All-r and endpoint qualification

In the small-a interval the normalized density is
`K/(eps+9ra)`, with leakage `(eps ell+8ra)/(eps+9ra)>=ell0`.
For `a<=a0` its actual mass satisfies the inherited local theorem's
bound. For `a>=a0`, `c/(a+c)` increases with c, yielding the uniform
baseline `h0>=(6/35)ra m^2/(a+m)^2`. Since `a0<=m` and
`eps<=a0/16`, the remaining relative charges satisfy

    (140/9)(eps/m)+[2eps^2/a]/baseline
       <=140/(9*2^22)+35/(192r)<1/2

for every integer r>=1. The two ranges both include a0. At a=0 only the
inherited small-a theorem is used, so no logarithm of a singular matrix
is taken. The condition ell>0 and the lower bound C>=mI>0 remain real
admission conditions; zero leakage is not proved by continuity of a
strict bound. No condition-number input is required, although normalized
gap sizes can still depend on TrC.

## Literal bath receiver

`replay_reviews.py` reconstructs the actual r1 source directly from
`H=[I+(E01+E10) tensor diag(1,-1,0)/4]/9`, rather than importing either
producer functions or its saved Z. Exact rational LDL verifies H>I/13
and Z>0. The independent quantities agree with the root compiler:

    ell=8/9, eps=1/5308416, a0=1/331776,
    TrZ=12+eps,
    Delta(Z)>=1327279/4180377600,
    CMI-log3>=2654558/100329063975 > 0.00002645.

U=|+><+| and V=|0><0| are singular noncommuting bath projectors. The
physical marginal is `(TrZ/3)I3`, the bath-|1> compression is X/2, and
the declared physical off-block square is nonzero. The source singlet
fidelity exceeds2/3 and its condition lower bound exceeds24. These
checks exclude only the named old admission premises, not every
previously positive source family. The inherited spectral-mixture
identity uses `q'(0+)=1/2` and `q''>=1/30` on[1,2], explaining both
the eps ell/4 atom and the1/3150 continuous term.

The independent source/39-cell replay took about0.19s together. It is a
mathematical construction, not an experimental or practical quantum
implementation. Historical priority of the strengthened radius remains
unestablished by this review.
