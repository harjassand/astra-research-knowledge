# One-sided relative peak region, including singular sources

27 October 2026. Exact extension of the received relative-marginal BKM theorem. No external priority claim.

Let N=W3⊗id_R, E(X)=I3/3⊗Tr_A X=τ, for any positive X on C3⊗C^d, finite d. Remove only the unused marginal kernel, so τ is faithful. Relative entropy uses the original source and actual marginal. Write D_in=D(X||τ), D_out=D(NX||τ), Δ=D_in−2D_out and H=Tr[(X−τ)Dlog_τ(X−τ)].

## General upper-peak bound

If 0≤mτ≤X≤Mτ with 0≤m≤1≤M, set q=max{m,3−2M,0}. With I(z)=(z log z−z+1)/(z−1)^2, I(0)=1 and I(1)=1/2,

D_in≥I(M)H,  D_out≤I(q)H/4,
D_out≤I(q)/(4I(M)) D_in,
Δ≥[I(M)−I(q)/2]H.

These are sufficient source-specific estimates, not an unrestricted two-source contraction result.

The additional mechanism is the completely positive complement 3E−N. Its physical map is A↦(Tr A I+A^T)/2, whose Choi matrix is the symmetric projection. Applying it to Mτ−X gives

0≤(3E−N)(Mτ−X)=(2M−3)τ+NX,

hence NX≥(3−2M)τ. Positivity and N(X)≥mτ give the stated q. Along the original input and output entropy paths, respectively,

τ+s(X−τ)≤[1+s(M−1)]τ,
τ+s(NX−τ)≥[1+s(q−1)]τ.

The received BKM order argument and exact H_τ(N(X−τ))=H/4 now integrate to the bounds. This retains every changing-base cost and does not whiten entropy.

If X or NX is singular, use X_ε=(1−ε)X+ετ. Its marginal is still τ, upper peak is still at most M, output lower bound is at least qτ, and tangent metric equals (1−ε)^2 H. The faithful proof passes to the finite-dimensional entropy-continuous limit. For q=0, the scalar integral remains finite because (1−s)/(1−s)=1; equivalently use monotone convergence of I(q_ε) to I(0).

## Clean one-sided theorem

If X≤(4/3)E(X), with no positive lower bound required, then q=1/3 and

I(4/3)=12log(4/3)−3,
I(1/3)=3(2−log3)/4.

Exact rational logarithm certificates establish

I(4/3)−I(1/3)/2>1/9,
I(1/3)<(3/2)I(4/3).

Consequently

D(NX||τ)≤(3/8)D(X||τ),
Δ(X)≥D(X||τ)/4,
Δ(X)≥H/9.

Equality in Δ=0 forces X=τ. Arbitrarily ill-conditioned reference marginals and singular input sources are permitted. The sharper unsimplified contraction coefficient is approximately 0.3737634921.

## Sharpness of the CP output-floor mechanism

On C3⊗C3 let F be swap and P_±=(I±F)/2. For 1≤M≤3/2 set

X_M=M P_+ +(3−2M)P_−.

Since Tr_A P_+=2I and Tr_A P_−=I, EX_M=I9. Moreover 0≤X_M≤M I9 and

N(X_M)=((3+M)/4)I9−(9(M−1)/4)P_Φ,

where Φ is normalized maximally entangled. Its minimum eigenvalue is exactly 3−2M. Thus this output floor cannot be universally increased using only the one-sided input peak assumption. At M=3/2 both the input and output have zero eigenvalues. This is a limitation of the separate-floor method, not a VALUE counterexample; the affine-projector source itself was already paid.

Certificate: one_sided_relative_peak_entropy_certificate.py and .json.
