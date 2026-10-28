# Complete white-noise curves for arbitrary coherent weak-reset seeds

This complements `WEAK_RESET_PROOF.md`. It is a new mathematical derivation
in this work, pending independent review. The positive operator-bath lift
used below is an existing current Astra theorem, not new here.

Use all notation and hypotheses of the weak-reset theorem. In particular
X=A0+I_A tensor Y, A0=P_Omega tensor C, mI<=C<=MI, kappa=M/m and Y<=bI.
The stronger, conservative assumption

    b<=m/(2^29 kappa^7)                                  (1)

pays the ENTIRE scalar white-noise curve

    h(a)=Delta(X+aI_(9r))>=0 for every a>=0.             (2)

This is not a physical tolerance claim. The small sufficient radius buys
an all-a theorem, rather than positivity on a grid or merely at a=0.

## 1. A quantitative scalar baseline

Set f(x)=xlogx and

    g(s)=f(s+3)+9f(s+1/3)-6f(s+1)-4f(s).

The eigenvalues of A0+aI and its N/E images give exactly

    Delta(A0+aI)=sum_j c_j g(a/c_j),                    (3)

where c_j are the eigenvalues of C. The coefficient of log c_j cancels.
The following scalar lower bound is useful at every positive s:

    g(s)>=(6/35) s/(1+s)^2.                             (4)

Direct differentiation gives

    g''(s)=12(s-1)/[s(s+3)(3s+1)(s+1)].

For 0<=s<=1, g is concave, g(0)=0 and
g(1)=4log(32/27)>=5/8, using log(1+x)>=x/(1+x).
Hence g(s)>=5s/8. For s>=1, g(s),g'(s) tend to zero at infinity, so

    g(s)=integral_s^infinity (t-s)g''(t)dt.

On t>=2s>=2, t-1>=t/2, t+3<=5t/2, 3t+1<=7t/2 and t+1<=3t/2.
Thus g''(t)>=16/(35t^3), and integrating only t>=2s gives
g(s)>=6/(35s). These two bounds imply (4). Consequently

    Delta(A0+aI)>=(6/35) a*r*m²/(a+M)².                (5)

The logarithm and reference-dimension cancellations in (3) are essential;
ordinary entropy continuity alone would not supply this positive sign.

## 2. Charge an arbitrary noncommuting reset

For a>0 integrate the derivative along
A0+aI+t(I_A tensor Y), t from zero to one. The two positive entropy
derivatives have matrix logarithms at least log a. The negative N-image
logarithm is at most log(a+M+b). All constant derivative terms cancel.
No commutation is used. Therefore

    h(a)>=Delta(A0+aI)-6TrY log(1+(M+b)/a)
        >=(6/35) a*r*m²/(a+M)²-18r*b*(M+b)/a.          (6)

The last step uses TrY<=3rb and log(1+x)<=x.

## 3. Cover every a with two actual estimates

Let a0=m/(1024 kappa²). For 0<=a<=a0, assumption (1) gives

    ||Y+aI||<=b+a0<=m/(512 kappa²).

The original weak-reset receiver applies to the ACTUAL combined reset:

    h(a)>=(TrY+3ra)/3.                                 (7)

For a>=a0, a/(a+M)>=1/(1025 kappa³). Moreover
b(M+b)<=m²/(2^28 kappa^6), while the exact integer comparison is

    2^28=268435456>210*1025²=220631250.

Thus the second term in (6) is at most half its first term, giving

    h(a)>=(3/35) a*r*m²/(a+M)², a>=a0.                 (8)

Equations (7),(8) prove (2) on the entire half-line. If Y!=0, h(0)>0.
Regardless of Y, h(a)>0 at every finite a>0. There is no white-noise grid,
reference-dimension cutoff or limiting assumption on bath eigenvectors.

The independent reviewer has derived a stronger relative-order receiver
without kappa in its base condition. That strengthening is not used above
and remains attributed to that review.

## 4. Feed an established noncommuting operator-bath operation

The current8d51 N1096 source
`white_noise_stability_operator_bath_lifting_theorem.md` proves the exact
positive-mixture identity: for positive U,V on any finite extra bath,

    Z=X tensor U+I_(9r) tensor V,
    q(t)=Tr(tU-V)_+,
    Delta(Z)=q'(0+)h(0)+integral_(0,infinity)h(t)dq'(t).  (9)

The measure is positive, total mass TrU. The proof uses spectral counting
in a COMMON resolvent, not measurement or pinching of an inaccessible bath.
It is an inherited operation whose premises include the WHOLE curve.
Sections1–3 acquire that missing premise for arbitrary weak Y and nonflat C.

Therefore (1) supplies Delta(Z)>=0 for arbitrary noncommuting/singular U,V.
This extends the admitted seed class beyond a single coherent reset
eigenvector. It does not cover arbitrary large base Y, arbitrary C,Y pairs,
or unrestricted qutrit-reference states.

## 5. A literal rational noncommuting-bath certificate

Take the two-dimensional bath

    U=(1/2)[[1,1],[1,1]], V=[[1,0],[0,0]].

They are positive rank-one projectors and UV!=VU. Direct eigenvalues give

    q(t)=(t-1+sqrt(t²+1))/2,
    q'(0+)=1/2, q''(t)=1/[2(1+t²)^(3/2)].

The atom alone gives Delta(Z)>=TrY/6. A nonzero, Y-independent margin can
also be acquired. In the m=1 examples, a0<=1, so (8) applies on [1,2].
There q''>=1/30 and h(t)>=(3/35)r/(M+2)², whence

    Delta(Z)>=TrY/6+r/[350(M+2)²].                      (10)

Divide by TrZ=3(TrC+TrY)+9r to get the normalized CMI excess above log3.
The source's logical main C tensor U is now singular and generally nonflat;
its reset has genuine bath noncommutation. The certificate uses the known
positive-mixture theorem and explicit bounds, rather than a numerical
entropy value at a few bath spectra. No physical bath is acquired.

## Root/reviewer improvement of the all-white condition

Root observes that the independently accepted relative-order1/192 reset
receiver replaces (1) by b<=m/(2^26 kappa³). Set a0=m/384. Then
b+a0<=m/192, so the small-a region is paid by that stronger receiver.
For a>=a0, a/(a+M)>=1/(385kappa), b(M+b)<=m²/(2^25kappa²), and
2^25=33554432>210*385²=31127250. The same half-baseline proof gives (8),
hence the entire curve and bath corollary. This strengthening belongs to
root plus the independent reviewer; the original kappa^7 proof remains
above with its actual provenance. It is not required by the general-ray
operation. This file's explicit bath is an analytic construction; no
separate numerical bath-matrix acquisition is claimed in the current record.
