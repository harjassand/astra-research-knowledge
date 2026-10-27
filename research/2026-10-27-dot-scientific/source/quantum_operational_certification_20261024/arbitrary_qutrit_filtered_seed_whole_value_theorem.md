# Whole value for an arbitrary qutrit pure main plus physically isotropic reset

26 October 2026. Consolidated source theorem. The complete theorem has independent PASS in `arbitrary_qutrit_filtered_seed_whole_value_independent_audit.md`. The final conditional-curvature step also has independent algebra/source receiving in `clean_core_full_curvature_schur_independent_audit.md`. No unrestricted WH3 or anchored-filter claim.

## Statement

Let psi belong to C3 tensor C3, and let A>=0 be any qutrit reference matrix. Set

 X=|psi><psi|+I3 tensor A,
 R=Tr_physical X, N=W3 tensor id,
 W3(B)=(Tr(B)I3-B^T)/2.

Then

 Delta(X)=f(X)+f(R)-2f(NX)-Tr(X)log3 >=0,
 f(B)=Tr B logB,

with 0 log 0=0. Equivalently Delta=f(X)+f(R)-f(2NX)+log(4/3)TrX.

No commutation, Schmidt-weight equality, or TP condition is assumed. Reference dimension at most 3 is load-bearing in this proof. Padding a smaller reference is harmless; arbitrary larger reset support is not covered.

By a physical unitary, which leaves I3 tensor A unchanged, put psi=(I tensor sqrt(H))Omega3 for H>=0. It suffices to prove the theorem for the pair(H,A). The feasible trace-normalized domain TrH+3TrA=1 is compact, and Delta is continuous.

## 1. A hypothetical negative minimum has faithful H and rank-two A

Singular H means the main has physical Schmidt rank at most2. The already-received physical2+1 block theorem pays this boundary. The explicit companion bound is

 Delta(X)>=f(A)+3f(A+H/3)-4f(A+H/4)>=0.

Rank A<=1 is the entire coherent-star theorem (arbitrary pure main plus physical noise on one reference line), also previously received.

For faithful A, write A=A0+bI with b=lambda_min(A)>0. The exact determinant kernel is

 Delta(H,A)=integral_0^infinity F(K(t))dt,
 K(t)=sqrt(H)(A+tI)^(-1)sqrt(H),
 F(K)=2logdet[I+(TrK I-K)/2]-3logdet(I+K/3)-log(1+TrK).

Its previously received zero-surface theorem says every coordinate gradient is negative on F=0, so an actual Loewner-decreasing path cannot cross zero downward. Translation gives

 Delta(H,A)=integral_b^infinity F(sqrt(H)(A0+sI)^(-1)sqrt(H))ds.

If this value is negative, the kernel at b is negative and stays negative for 0<s<=b. Hence Delta(H,A0)<Delta(H,A)<0. Its source trace also decreases, so renormalization strictly improves the negative value. This rules out a faithful reset at a negative normalized minimum. Therefore H>0 and rankA=2.

## 2. Actual stationary reduction to one common eigenline

The independently received theorem `filtered_seed_faithful_stationary_common_eigenline_theorem.md` applies at fixed A and fixed TrH, including singular A. It proves H,A share a reducing eigenline.

Briefly, in a simple A eigenbasis write the actual invariant derivatives alpha>0, beta>0, c and j real, and n<0 as in that theorem. Orientation and direct off-diagonal H stationarity give

 c(adjH)_ij=(alpha a_k+beta)H_ij,
 n(adjH)_ij=(c a_k+j)H_ij.

Two nonzero off-diagonal pairs would force n alpha=c^2, impossible. Repeated-reset eigenspaces are received by diagonalizing their H block; direct off-diagonal stationarity then forces one cross entry to vanish. This is a source stationarity theorem, not an assumed entropy pinching.

If H and A commute, the already-received aligned filtered-seed CQ-dilation theorem pays the value. Otherwise write H=H2 direct-sum h and A=A2 direct-sum a, with a noncommuting faithful active H2.

## 3. Only a clean spectator can remain

The received transverse H Hessian excludes a strictly middle reset eigenvalue as spectator: its determinant is (c^2-n alpha)(a1-a)(a2-a), negative for a middle a.

A maximum-reset spectator is also excluded. Its local-minimum transverse Hessian gives the actual order H2>=hI. As A2<=aI,

 sqrt(H2)(A2+tI)^(-1)sqrt(H2)>=h/(a+t)I.

Thus active resolvent product p is at least spectator k squared. The received scalar active-trace derivative F_s is strictly positive under this condition. Its integral cannot vanish at a genuinely noncommuting stationary orientation. The full maximum-spectator argument and its direct ordered whole-value corollary have independent PASS in `filtered_seed_maximum_spectator_independent_audit.md`.

Since rankA=2, the remaining spectator is its zero eigenvalue. Thus A=0 direct-sum A2 with A2>0. This is the clean-spectator core; no normal/boundary reset variation is needed below.

## 4. The final clean-core negative curvature

Diagonalize A2=diag(a,b), a!=b, and gauge H2=[[x,z],[z,y]], z>0. Put

 D(t)=det(A2+tI), u=Tr(H2 adjA2), v=detH2,
 s(t)=[Tr(H2)t+u]/D(t), p(t)=v/D(t), k(t)=h/t.

At fixed reset and fixed main trace, u,v are independent actual local coordinates. Stationarity implies

 Ip=integral F_p/D dt=0,
 Is=integral F_s/D dt=0.

The full operator/transport theorem `clean_core_conditional_curvature_operator_proof.md` proves Ip=0 implies

 Q0=integral {[(1+k)D+N]^(-2)-2[2D+N]^(-2)}dt<0,
 N=Tr(H2)t+u.

Its proof uses the actual qubit Haar determinant identity, a sharp scalar quadratic-resolvent lower bound, a positive 2x2 matrix mean and integral determinant Minkowski. Specifically, the unique Ip-zero h_star satisfies h_star>4(2-sqrt3)h_cert>h_cert, where h_cert is an explicit sufficient transport threshold for Q0<0. No commutation or sampled sign is used.

For completeness, the negative invariant direction is an EXACT source curve. Set

 x_epsilon=x+epsilon/(b-a), y_epsilon=y-epsilon/(b-a),
 z_epsilon=sqrt(x_epsilon y_epsilon-v+3epsilon).

For small two-sided epsilon it preserves main trace and faithfulness and gives u_epsilon=u+epsilon,v_epsilon=v-3epsilon. Therefore its actual entropy second derivative is

 integral { (s+k+1)^(-2)-2(s+2)^(-2)
            -2(k-1)^2/[p+(k+2)(s+k+2)]^2 }/D(t)^2 dt
 <=Q0<0.

This contradicts local minimality. If a=b, the active reset is scalar and commutes with H2, already paid. Hence no negative minimum exists, proving the theorem.

## Dependency and scope controls

The boundary physical2+1, coherent-star, aligned CQ-dilation, zero-surface and common-line results precede the final clean curvature argument and do not use this whole theorem. The realification and cyclic-phase comparisons are useful but NOT needed in this proof. The exact fixed-spectrum interior orientation minimum and joint-balancing obstructions remain valid: the proof uses actual stationary directions rather than those false universal reductions.

An arbitrary invertible reference filter of a qutrit-reset seed has this form, so its VALUE is nonnegative. This does not prove

 Delta(filtered)>=lambda_min(Z*Z)Delta(unfiltered),

which is the stronger noncommuting anchored comparison. Nor does it pay an arbitrary larger-reference coherent-reset bath, general accepted-only GLS monotonicity, or the unrestricted WH3 inequality. The separate equality addendum below is not used by the value proof and has independent PASS in `qutrit_filtered_seed_equality_and_curvature_independent_audit.md`.

## Equality addendum (independently received PASS)

The received value theorem also implies the following exact zero set:

 Delta(P_psi+I3 tensor A)=0
 iff psi=0, or A=0 and psi is maximally entangled up to scale.

The zero source is included. This addendum is not used in the value proof.

If H=0 the source is a physical-identity product state and its deficit is
zero for every A. If A=0, the ordinary pure qutrit equality theorem says
that the deficit vanishes precisely when H is a scalar multiple of I3.

Suppose H is nonzero but singular. The boundary bound in Section 1 is
strict: trace x log x is strictly convex, so

 f(A)+3f(A+H/3)-4f(A+H/4)>0

for every nonzero H. Thus every other equality candidate has H>0.

If rank A=1, identify its reference line with the coherent-star center.
Its physical noise is D=aI3, a>0; the pure main splits as c on that line
and chi_B on its two-dimensional orthogonal complement. Full Schmidt rank
of the main forces c!=0 and rank B=2, hence B!=0. The received strict
coherent-star equality classification excludes this case.

For a commuting pair with H>0 and A!=0, use the already-received
COMMUTING anchored-filter theorem, not an unproved strictness claim for a
limit. Put A0=H^(-1/2) A H^(-1/2), which commutes with H. Then

 Delta(P_psi+I tensor A)
 >=lambda_min(H) Delta(P_Omega+I tensor A0)>0.

The first inequality is `mean_dominant_reference_score_and_commuting_filter_order.md`
(independent PASS). The second is the strict nontrivial-mixture assertion
of `arbitrary_qutrit_mixed_reset_value_theorem.md` (independent PASS).
Neither dependency uses this new whole-value theorem.

If rank A=2 and equality held, the source would be a global minimum,
since the whole value theorem is now known. Every fixed-A, fixed-main-trace
variation used in Sections 2--4 is still feasible. The common-line theorem
reduces to commuting or noncommuting two-core form. The commuting case is
strict by the preceding paragraph. Middle and maximum reset spectators
are excluded by their Hessian/stationarity arguments, while the remaining
clean noncommuting core has the same strictly negative actual H curvature.
None of those arguments requires a negative value once local minimality
is known. Thus rank-two reset cannot attain equality with H>0.

Finally let A=A0+bI be faithful, b>0. The asymptotic exact log kernel is

 F(sqrt(H)(A0+tI)^(-1)sqrt(H))
 =[3(TrH)^2-Tr(H^2)]/(12t^2)+O(t^(-3)),

whose leading coefficient is strictly positive for H!=0. If the integral
from b to infinity were zero, the no-downward-zero property and this
strict positive tail would force F at b to be strictly negative. It is
then negative throughout 0<t<=b. Removing the floor would give a strictly
negative deficit, contrary to the received value theorem. Faithful reset
therefore cannot attain equality either. This completes the zero-set proof.
