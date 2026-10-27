# Independent permanent trap and explicit positive AC bad label — PASS

26 October 2026. Reviewed `REGULAR_TIMELIKE_TRAP_AND_EXPLICIT_AC_BAD_LABEL.md`, its exact receiver, and the earlier full-matrix global bump proof. Frozen receipt reproduced byte-for-byte; no large Fejer array or sampled inference used.

## Correct atomic geometry and permanent obstruction

All four declared phase pairs produce the stated atoms. The first pair has F_u=−1/2, the second F_u=1, so all are regular source boundary points. The correct support identity is q=(u+v+w)/2, NOT q=u. The exact positive weights give mean0, Eq0 and the stated positive diagonal covariance; a=e/2 and delta0. Any admissible first null-displacing descendant from mean0 would have q(m)=0 and sum(m)=0, hence |m|²=0. The same argument repeats after every zero-displacement label. Affine independence further fixes the mean-zero atomic weights. This obstructs all mean-displacing posterior continuation on this support, not just a bounded feature module.

## Full physical separator, not coefficient-only extension

L has eigenvalues1/4 and3/4. The already-received determinant/skew-square identity gives global C2 rank-one convexity for the stated R=1/16 and b=1/196608. On symmetric Bz, the skew term vanishes and det(Bz)−L:Bz=q−S/2. The bump is zero on ALL source boundary points: F=0 implies |z|²>=3/4, and |z|²<=(5/2)|Bz|². Independently checked the latter matrix inequality is strictly positive definite. Thus |Bz|²>=3/10>R². No atom-only bump test or unproved cutoff extension is used.

## Explicit Fejer and exact moment correction

Normalized tensor Fejer kernels have mean1, nonnegative density bounded by N², and Fourier multiplier (1−|k1|/N)_+(1−|k2|/N)_+. For the finitely supported Fourier polynomials here, their multiplier error is at most(|k1|+|k2|)/N. With inversion averaging, the physical pushforward density retains these bounds and all expectations; exceptional fibers are source-null, or conditional averaging gives the same construction.

Coordinate errors<=2/N, q error<=9/N follow from Fourier degree/L1 bounds. For e=q−S/2, L1<=9/2 and e² has frequency norm<=6, so smoothing the zero atomic e² expectation costs at most243/(2N). The source five-feature Gram inverse has the displayed blocks. Its correction coefficients are bounded by20/N per coordinate and32/N for q, giving sup correction<=156/N. The constant coefficient is zero. The minus correction sign restores mass, mean and q exactly, rather than merely normalizing.

At N=2^28 and eta=1/786432, 156/N<eta/2. Therefore f>=139/201326592>0 and f<=N²+1. Since E_mu e²=3/8, adding the eta source and subtracting the correction costs at most(eta+eta/2)*(3/8)=9eta/16. This receives E_sigma e²<=627/536870912<=b/4 and hence **P(0)−E_sigma P(BZ)>=1/262144**. The resulting bounded strictly positive source-AC probability is nonlaminate from mean0.

## Actual label and scope

With p=1/[2(N²+1)]=1/144115188075855874, pf<=1/2. The complement density(1−pf)/(1−p) is strictly positive and normalized; both branches have mean0 and Eq0. This is an admissible zero-displacement source label retaining the bad branch with positive probability.

Domination sigma>=rho mu gives C>=rho I/2 and delta>=rho inf_(a,b) E_mu(q−a·Z−b)²=3rho/8. Since V<=3, it starts with covariance ratio at least rho/6 and residual ratio at least rho/24, strictly above the proposed rho/48 floor. No universal policy guaranteeing both fixed-floor preservation on all descendants and exhausting variance-band progress can hold for every such posterior: that would contradict the explicit rank-one-convex Jensen gap.

This does NOT make the original cosine source nonlaminate, produce a Morrey counterexample, or show that every policy must choose a bad branch. Finite AC continuability and viable infinite exhaustion are different. The original source may admit a policy avoiding this label. No invariant-preservation theorem is inferred.
