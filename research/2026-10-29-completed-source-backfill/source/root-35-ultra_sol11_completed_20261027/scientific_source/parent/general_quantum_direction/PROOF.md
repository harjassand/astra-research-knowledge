# Independent derivation of the general positive-direction receiver

The first dyadic receiver below is now superseded in strength by the
condition-number-free reviewer construction. Both derivations remain valid.
The stronger result and root's independent derivation appear at the end.

This is root's independent derivation of the producer's new finite-radius
boundary result. It uses the conventions in capability_backchain and the
independent quantum_boundary_review. The unrestricted entropy inequality,
global squashed-entanglement value and historical novelty are NOT_ESTABLISHED.

Let A,B be qutrits, L finite of dimension r, p=P_Omega/3 and
A0=3p tensor C with mI<=C<=MI, m>0, κ=M/m. Let H be ANY positive
matrix on ABL with TrH=1 and leakage ell=Tr[(I-p)H]>0. Write

    X=A0+epsilon H,
    Delta(X)=f(X)+f(EX)-2f(NX), f(Z)=Tr Z log Z,
    N=W3 tensor id, E=I3/3 tensor Tr_A.

Use the exact identity N*(p_sym)=(3/4)(I-p), so the kernel leakage
at NA0 is3ell/4. The E source has no kernel. Fix epsilon/m=x<=1.
All following bounds are on the actual finite matrices, not an asymptotic
expansion or a numerical entropy diagnostic.

## Explicit finite inequality

Scale by m first, using Delta(mZ)=m Delta(Z); thus the base C has
minimum eigenvalue1 and maximum κ, and the perturbation is xH.
Pinch X into the p and(I-p) blocks. Its coherence contribution is
nonnegative, the support increment is bounded below by its tangent at3C,
and the kernel entropy satisfies

    f((I-p)H(I-p))>=ell log[ell/(8r)].

This last bound is ordinary entropy maximization at fixed trace in a space
of dimension8r. It remains true for a rank-deficient kernel block.
Consequently the X increment is at least

    x[(1-ell)(1+log3)+ell log x+ell log(ell/(8r))].

The E increment is at least x(1-log3). For N, the supported increment
is at most x(1-3ell/4)[1+log(κ+x)]. Its kernel entropy is at most
x(3ell/4)log x, because NH is a density matrix and every compression
has eigenvalues at most1. Pinching coherence is at most x log2:
joint convexity charges only NH, not the main source.

Subtracting twice this N bound, simplifying and restoring m proves

    Delta(A0+epsilon H)>=epsilon[
      (ell/2)log(m/epsilon)-ell log(24r/ell)+ell/2
      -2(1-3ell/4)log(κ+epsilon/m)-2log2].               (1)

Since κ>=1 and epsilon/m<=1, weakening the coefficient of the nonnegative
logarithm yields the simpler lower bound

    epsilon[(ell/2)log(m/epsilon)-ell log(24r/ell)
             +ell/2-2log(κ+epsilon/m)-2log2].            (2)

This derivation does not assume H=I_A tensor Y, any input marginal, reset
rank, commutation, reference eigenbasis or a dimension cutoff.

## An exact rational receiver requiring no matrix logarithms

Let L be the smallest integer with2^L>=24r/ell, and K the smallest integer
with2^K>=4κ. Define

    k=2L+ceil(4K/ell)+1.

If0<epsilon<=m2^(-k), then
log(24r/ell)<=Llog2 and
2log(κ+epsilon/m)+2log2<=2Klog2. Equation(2) is therefore at least

    epsilon ell(1+log2)/2 > epsilon ell/2.

In particular the producer's conservative epsilon ell/3 output is proved.
All admission calculations use rational comparisons and integer ceilings;
matrix logarithms are unnecessary once the finite input hypotheses are
certified. The bit length of2^(-k) is O(k), and k can be enormous when
ell is tiny. This is NOT a polynomial-cost assertion in the input bit length.
Positive order certificates, m,M,TrH and leakage are required inputs.

If ell=0, positivity forces H to be supported on p tensor L. Then it
changes only C and Delta=0; the displayed division by ell is not used.
If C is singular with new leakage outside its support, this theorem does
not apply without a new kernel analysis.

## A rational Choi source outside the old closure

For r=1,C=1 let D0=diag(1,-1,0) and

    H=[I9+(1/4)(E01+E10) tensor D0]/9.

It is a positive density, H>=I/12, and Tr_B H=I3/3. Also ell=8/9,
L=5,K=2,k=20. The rational source X=P_Omega+2^(-20)H, normalized by
3+2^(-20), has maximally mixed A marginal and is a valid qutrit channel
Choi state. Its associated antisymmetric-isometry extension obeys

    CMI>=log3+8/84934683.

This uses the conservative ell/3 theorem, not a matrix-entropy computation.

For every earlier reset seed, its physical off-diagonal reference block is
E01 tensor C, up to the admitted physical covariance and reference isometry;
its square is zero. Positive scaling, white addition, flagged direct sums,
reference isometries and the proved noncommuting bath lift preserve this
property. Unflagged arbitrary convex mixtures or arbitrary reference channels
are NOT among these proved closure operations.

For the new X, its01 block is E01+(2^(-20)/36)D0. Its square is exactly
(2^(-40)/1296)diag(1,1,0), since the mixed anticommutator vanishes.
It is nonzero. Thus this actual finite source escapes that specified closure.
This does not exclude a different as-yet-unproved closure or solve the
global entropy inequality. The source, channel and order information are
synthetic exact mathematical inputs, not a measured or constructed device.

fixture.py independently verifies trace, partial trace, leakage, strict
positivity, exact k and the nonzero block square using Fraction arithmetic.

## Stronger receiver: independent root derivation

The reviewer retains log C. Normalize its minimum eigenvalue to1, set
t=epsilon/m and s=3ell/4. The support log C terms combine to

    Tr[pH log C]+Tr[H log C]-2Tr[p_- NH log C]
       =(1/2)Tr[(I-p)H log C]>=0,

since N*(p_-)=(I+3p)/4. The N support obeys
A_N+t p_-NH p_-<=(1+t)A_N, because NH is a density and C>=I.
Its upper log increment is at most log C+log(1+t), eliminating max C.
Retain f(p_sym NH p_sym)<=s log s and pinching loss h2(s): their sum
-2s log s-2h2(s)=2(1-s)log(1-s)>=-2s. The input-kernel lower bound
ell log[ell/(8r)] and E tangent then give the finite inequality

    Delta(A0+epsilon H)/epsilon
      >=(ell/2)log(1/t)-ell log(24r/ell)-ell-2t.

If t<=ell²/(2^14 r²), this is at least
ell[4log2-log3-1]-2t >=(5/9)ell-2t>ell/2,
using log2>=2/3 and log3<=10/9. Consequently

    epsilon<=m ell²/(2^14 r²)
      implies Delta(A0+epsilon H)>=epsilon ell/2.

This removes the κ-dependent dyadic input radius above. For rational
m,ell, the scalar radius has bit length linear in their input bit lengths
and log r. Reading matrices, proving PSD, acquiring m and certifying ell
remain separate costs. No physical acquisition or best entropy-algorithm
advantage follows. At ell=0 use the supported equality case rather than
inferring a positive-radius claim from this formula.

## Ordinary positive seed defeats an overbroad anisotropy interpretation

The lead's signal-Gram invariant is valid for its specified seed/closure
package. It is not a scientific obstruction to producing anisotropy.
Take rho_cc=(1/3)sum_i Eii tensor Eii, a classical TP Choi density.
Its three source eigenvalues are1/3, its nine E-image eigenvalues1/9,
and its six nonzero N-image eigenvalues1/6. Hence exactly

    Delta(rho_cc)=-log3-2log3+2log6=log(4/3)>0.

Its traceless physical signal has coefficient matrix
(1/3)I3-(1/9)J3 on the diagonal physical/reference bases. This has two
singular values1/3 and all others zero: the signal rank is2, not8.
It therefore violates the near-isotropic8-signal closure condition while
being certified by elementary ordinary entropy arithmetic. Adding this
already-qualified seed breaks that restricted invariant. A meaningful new
coverage claim must compare against such positive families too; anisotropy
by itself is not a newly missing scientific operation.
