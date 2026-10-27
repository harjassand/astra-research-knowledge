# A regular source-supported trap and an explicit positive AC bad label

This is a counterexample to universal posterior viability, NOT a counterexample for the original cosine source or Morrey's conjecture. The original source may admit a policy that avoids this bad posterior.

## 1. Corrected exact atomic trap

Put A=(sqrt6+sqrt2)/4, B=(sqrt6-sqrt2)/4. Use atoms

 (1/2,A,B), (1/2,-A,-B), each weight1/3;
 (-1,1/sqrt2,-1/sqrt2), (-1,-1/sqrt2,1/sqrt2), each weight1/6.

They are actual source phase points, respectively at (x/pi,y/pi)=(1/3,1/12),(1/3,13/12),(1,1/4),(1,5/4). All are regular points of the determinant boundary: its u derivative is -1/2 on the first pair and1 on the second pair.

**Coordinate correction:** in the source coordinates q=uv+uw+vw, the valid relation is q=(u+v+w)/2, NOT q=u. The latter assertion resulted from mixing Lorentz and correlation coordinates and is not a certificate.

The measure has mean0, q moment0 and covariance

 diag(1/2,(3+sqrt3)/6,(3-sqrt3)/6).

Its regression vector is a=e/2, which is timelike, and delta=0. Every posterior on the same support has E q=E S/2. A D0 descendant mean reached by a null step from0 must therefore satisfy q(m)=0 and S(m)=0. Since q(m)=(S(m)²-|m|²)/2, this forces m=0. Repeating the argument rules out every mean-displacing descendant. In fact the four points are affinely independent, so even a label preserving mean0 has the same weights.

## 2. Existing explicit global matrix separator applies

Use the already received global bump with

 L=[[1/2,-1/4],[-1/4,1/2]], lambda=1/4, R=1/16,
 b=lambda^4/768=1/196608,
 P(A)=(det A-L:A)^2+det(L)(A12-A21)^2
      +b(1-|A|_F²/R²)_+³.

It is globally C2 rank-one convex by the prior physical proof. P(0)=b. On the entire source boundary, the bump vanishes, not merely at these atoms. Indeed F(z)=0 implies |z|²>=3/4: for t=|z|²<3/4, F>=1-t-2(t/3)^(3/2)>0. Also |z|²<=(5/2)|Bz|_F², so |Bz|_F²>=3/10>R². Thus on Sigma,

 P(Bz)=(q(z)-S(z)/2)^2=:e(z)^2.

It vanishes on all four atoms, giving the strict atomic Jensen gap b.

## 3. An explicitly defined bounded positive AC posterior

Let K_N be the normalized one-dimensional Fejer kernel

 K_N(t)=(1/N)|sum_{j=0}^{N-1} exp(i j t)|²,

with Fourier multiplier (1-|k|/N)_+ and Haar mean1. Take N=2^28. Around each of the four declared phase atoms, use the tensor product K_N in both phase coordinates, average with its simultaneous phase inversion, and combine with the exact atomic weights. The resulting inversion-even density g_N on the torus is nonnegative, has mean1 and is bounded by N². It defines a physical density with respect to mu because the two generic source fibers are simultaneous inversions; exceptional fibers are mu-null. Alternatively its conditional fiber average gives the same bounds and all expectations.

For any finite Fourier polynomial p with maximal |k1|+|k2|<=d, smoothing changes its atomic expectation by at most d times its Fourier coefficient L1 norm divided by N. Hence, writing d_vec=E_{g_N mu}(1,Z,q)-E_mu(1,Z,q),

 d_0=0, |d_i|<=2/N for the three coordinates, |d_q|<=9/N,
 E_{g_N mu} e²<=243/(2N).

The last bound uses Fourier L1(e)<=9/2 and maximal frequency norm of e² at most6. The unsmoothed atomic expectation is exactly0.

Let Y=(1,u,v,w,q), G=E_mu YY^T, eta=1/786432, and

 k(z)=(1-eta) Y(z)^T G^{-1}d_vec,
 f(z)=(1-eta)g_N(z)+eta-k(z),  sigma=f mu.

This is an exact definition; no array of size N is expanded. The required moments of g_N involve only finitely many low Fourier modes and algebraic phase values, so all coefficients of k are explicitly computable algebraic numbers.

The exact source Gram has coordinate block I/2, coordinate-q cross vector e/4, and q² entry3/4. Its inverse has coordinate block2I+(2/3)ee^T, cross entries-4/3, and q-q entry8/3. Therefore each coordinate coefficient of k has magnitude at most20/N and its q coefficient at most32/N. Since |q|<=3,

 ||k||_infinity<=156/N<eta/2.

Consequently f is a probability density, its mean and q moment are EXACTLY0, and

 139/201326592 <= f <= N²+1.

The moment correction is not a normalization shortcut: E_mu[Y k]=(1-eta)d_vec, including the constant feature.

Since E_mu e²=3/8, the exact residual bound is

 E_sigma e² <=243/(2N)+(9/16)eta
             =627/536870912 <=b/4.

Thus

 P(0)-E_sigma P(BZ)>=3b/4=1/262144.

This is a STRICTLY POSITIVE, BOUNDED, ACTUAL mu-AC D0 posterior that is not a laminate from its mean0. It can be continued for any finite number of sufficiently small source-aware mean steps by the AC compiler, but cannot be exhausted by such a laminate construction. Finite continuability and actual viability are decisively different.

## 4. It can occur in an actual source label

Set p=1/[2(N²+1)]. Since pf<=1/2,

 mu=p sigma+(1-p)tau,   d tau/d mu=(1-pf)/(1-p)>=0.

Both probabilities have mean0 and q moment0. This is a legitimate zero-displacement source label with a positive bad-branch probability. It is NOT asserted that every policy must choose it, and it does not imply mu itself is nonlaminate.

## 5. It also disproves a universal residual-floor preservation rule

Let rho=139/201326592. Domination sigma>=rho mu gives

 delta(sigma)>=rho inf_{a,b} E_mu(q-a.Z-b)²=3rho/8.

Its mean is0, V<=3 and C>=rho I/2. Thus it begins with delta/V²>=rho/24 and C>=(rho/6)V I. In particular it strictly satisfies a residual floor s=rho/48. Yet no policy that both preserves such a fixed floor on every descendant AND guarantees the positive variance-band progress of the conditional compactness theorem can exhaust it, because the explicit global rank-one-convex gap forbids that conclusion.

This pinpoints the limitation: the residual floor is a useful sufficient condition IF maintainable, not a universal maintainable invariant of all AC D0 posteriors. A successful source policy must preserve stronger source-specific viability information or work law-first rather than allow arbitrary posterior disintegrations.
