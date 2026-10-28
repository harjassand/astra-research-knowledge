# Local-variance maximum principle at index27/4 and the full condition-number24 region
27 October 2026. Root analytical extension; independent receiving requested. It extends the separately constructed index-six local-variance proof, not any global effect bound beyond its valid scope.

## Abstract maximum principle
Let U be a finite-dimensional positive effect, U psi=psi, ||psi||1, and V>=0. Assume ONLY the local second-moment inequality <psi,V²psi><=<psi,Vpsi>=y. Then0<=y<=1 and, putting
 B=(4U+23V)/27,
 C=(U+3B)/4=(13U+23V)/36,
we have
 <psi,(logB-2logC)psi> >= c(1-y),
 c=23/54+(529/5832)log[2^8*3^9*23/13^9] >253/29160>0.
GlobalV<=I is not required. Supported logarithms are interpreted on their actual supports.

Use the previously received SAME-PENCIL identities q(z)=<psi,Pi_+(zV-U)psi>, h(s)=<psi,log(U+sV)psi>,
 h(s)=integral s q(z)/[z(z+s)] dz,
 integral q(z)/z² dz=y.
These require positivity, Upsi=psi and the received renormalized hinge derivation; none requires globalV<=I. Initially take both matrices faithful. Seta=23/4,b=23/13,rho=23/54. Then contrast is
 j=log[16n/(n+3)^2]-integral w(z)q(z)dz,
 n=27/4, w=2b/[z(z+b)]-a/[z(z+a)].
Letq0=1_(z>1). Exact integrals give integralwq0=log[16n/(n+3)^2] and integralq0/z²=1.

Definek=w-rho/z². It factors as the specialization atn27/4 of
 -(n-1)^2(z-1)[(2n-3)z-3n+3]
 /[2n z²(n+z-1)((n+3)z+3n-3)].
Thus k is positive only on(1,z0), z0=23/14. Contributions tointegralk(q-q0) fromz<1 and1<z<z0 are nonpositive. Forz>z0, the actual spectral tail bound is
 1-q(z)<=z² <(I-V)²>/(z-1)²<=z²(1-y)/(z-1)².
The second inequality is precisely the local variance premise. Its rightside may exceed1; this does not invalidate it.

Therefore integralwq-integralwq0 <=-(1-y)[rho+integral_z0^infty k(z)z²/(z-1)² dz].
The integrand partialfractions are exactly
 -6877/[648(13z+23)]+2116/[729(4z+23)]+529/[5832(z-1)].
The bracket equals the displayedc. Positivity is rationally received: the degree-eight Taylor polynomial ofexp(23/5) exceeds13^9/(2^8 3^9 23), so its logarithm is<23/5 andc>23/54-(529/5832)(23/5)=253/29160.

RegularizeU_e=(1-e)U+eI andV_e=(1-e)V+eI. U_epsi=psi and
 y_e-<V_e²>=(1-e)²(y-<V²>)+e(1-e)(1-y)>=0.
Thus faithful approximation preserves all premises. Supported logarithmic receiving follows as in the earlier index-six proof; B>=U/n andC>=(n+3)U/(4n) keep thepsi-compressions finite. No arbitrary changeofsource is used in the physical application below.

## Physical consequence: EVERY finite-reference state with condition number<=24
Let E(X)=I3/3 tensorTr_A X andN=W3 tensorid. Suppose0<mI<=X<=MI ontheactualC3 tensorC^d productspace, finite d, withM/m<=24. Then
 Delta(X)>= (11/(2160 M)) ||X-E(X)||_HS² >=0.
In particular equality occurs exactly forX=E(X) inthisregion. This doesnotresolveunrestrictedentropy or singular/large-condition sources.

Normalize anactual top-level source toU<=I withUpsi=psi andU>=I/24. SetV=(nE(U)-U)/(n-1), n27/4. The universal effect inequality nE(A)-A>=-(1-n/9)I for0<=A<=I follows bydualizing thepure-state rankoneSchur test sum r_i/[(n/3)r_i+1-n/9]<=1 (scalarconcavity atthree equalweights). WritingU=m0I+(1-m0)A withm0>=1/24 provesV>=0.

PutZ=I-U, soZpsi0 and||Z||<=23/24. E is the exact average ofnine physicalqutrit Weyl conjugations. Theidentity termannihilatespsi; Cauchy-Schwarz ontheother8 terms gives
 ||E(Z)psi||² <=(8/9)<psi,E(Z²)psi>
 <=(8/9)(23/24)<psi,E(Z)psi>=(23/27)<E(Z)>.
AsVpsi=psi-(27/23)E(Z)psi, this is exactly<V²><=V>. Thelocalmaximumprinciple therefore applies to theSAME source, withB=E(U),C=N²(U). OperatorlogJensen for unitalCP/self-adjointN gives actualtopscore>=c(1-y)=(27c/23)[1-<E(U)>].

ForquantitativewholeVALUE, writeX_t=mI+min(X-mI,t),0<=t<=M-m, withtopprojectionP_t. Everypointretainscondition<=24 andactualtopnormm+t. LetQ(t)=||X_t-E(X_t)||_HS². Awayfinitelymanyspectralknots,
 Q'(t)=2(m+t)[TrP_t-Tr(P_t E(X_t))/(m+t)]>=0,
 Delta'(t)>=(27c/23)[TrP_t-Tr(P_t E(X_t))/(m+t)].
Integratingandusingm+t<=M givesDelta(X)>=27c Q(M-m)/(46M)>=(11/(2160M))Q(M-m), since27(253/29160)/46=11/2160. Initialwhite sourcehasDelta0,Q0. Degeneracies arehandledbythewhole top projectionandfinitelymanycontinuousknots. Literal fullproductidentity isessential; no dimension-independent normalized noise fraction is claimed.
