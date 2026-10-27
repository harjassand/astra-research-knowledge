# Independent audit: joint-convex shared-pair balancing

2026-10-25. Verdict: PASS for `one_column_shared_pair_balancing_theorem.md`, after correcting the c=0 endpoint description to the physical2+1 block theorem rather than classical/CQ. The result is a global balancing reduction, NOT a proof of the remaining balanced deficit's sign.

## 1. Hessian representation, including nonlinear off-diagonal dependence

For fixed h,d,c with |c|²≤hd, the matrix L(x,b) is positive for x,b>0 and h>0. Its trace is affine in x,b, though its off-diagonal entry is not. The entropy logdet integral may be differentiated twice because the second trace derivatives vanish; it gives Hess TrLlogL=−integral Hess logdet(L+tI)dt. Adding the scalar terms gives the stated Hessian representation. The scalar terms are h²/(xh+t)² and1/(b+t)², since their integrals are h/x and1/b. Thus no derivative of sqrt(x) has been omitted; it is encoded in the exact determinant.

Writing r=|c|², the shifted determinant D=(d+b+t)(xh+t)−xr has derivatives D_x=A=h(d+b+t)−r, D_b=B=xh+t, and D_xb=h. Therefore its mixed log derivative is (hD−AB)/D²=tr/D², exactly the off-diagonal Hessian entry. The diagonal entries are exactly those in the note. The integrals converge at infinity by cancellation of leading terms and are finite at zero in the faithful interior.

## 2. Pointwise PSD certificate

The source condition gives A≥h(b+t)=he and

D−Be=dB−xr=x(dh−r)+dt≥dt≥0.

It follows that M22≥0. Also hD−AB=tr≥0 with A≥0, giving M11≥0. The exact product of the diagonal Hessian entries is

tr(hD+AB)(dB−xr)(D+Be)/(B²e²D^4).

The three factors are bounded below by2hBe, dt, and2Be, respectively. Their product is at least4hdt B²e², which is at least tr B²e² because r≤hd. This proves M11M22≥M12² with the correct determinant factors and substantial slack. The t=0 endpoint has M11=M12=0 and is harmless. Degenerate h,d,c and x,b boundary values extend by entropy continuity; no singular Hessian at the boundary is needed.

As an independent diagnostic only, at h=1,d=2,c=.7,x=.3,b=.4, integrated Hessian eigenvalues are approximately .4819480707 and2.0573075642. Central finite differences agree with the integrated Hessian to about7.2e−8. The proof is the exact pointwise PSD calculation above, not this numerical check.

## 3. Actual entropy receiver

Taking the active population column k and light coordinates i,j, the actual two populated WH output pairs have unscaled matrices L(x,b) and L(1−x,a), up to harmless sign/unitary conjugation. The remaining pair is rank one with spectrum {h,0}. The only nonzero output singleton has unscaled value s=a+b. The input correlated block has spectrum T, with separate population eigenvalues a,b. The reference marginal is (xh,(1−x)h,d+s). These facts give exactly F(x,b)+F(1−x,a) as all variable-allocation dependence at fixed h,d,c,s.

Joint convexity therefore yields F(x,b)+F(1−x,a)≥2F(1/2,s/2). The trace h+d+s is fixed, so neither the homogeneous nor normalized deficit acquires an omitted normalization term. This proves a true global minimization over x and population allocation, not merely a symmetric stationary point or a numerical symmetry guess.

## 4. Balanced remainder and scope

At q=s/2, exact assembly gives

Delta_bal=TrTlogT−2TrLlogL+(d+2q)log(d+2q)
 +(h+d+2q)log(2/3)+d log2.

The d log2 term is necessary: the h and2q scalar contributions cancel against the output scaling with the indicated trace weights. All coefficients agree with the actual channel normalization by1/2.

At c=0 the source generally still contains the entangled vector sqrt(x)|ii>+sqrt(1−x)|jj>, so it need not be classical or CQ. It does, however, lie in a physical2+1 block cone and is safe by that independently audited theorem. The author corrected this wording during the audit. The q=0 endpoint is maximally correlated; the rank-one determinant endpoint reduces to the separately established rank-one-correlated-plus-population class.

The faithful coherent balanced interior still requires a value proof. Joint convexity of F in x,b does not imply concavity or convexity of the full remaining function in d,h,q,|c|², and this audit makes no such inference.
