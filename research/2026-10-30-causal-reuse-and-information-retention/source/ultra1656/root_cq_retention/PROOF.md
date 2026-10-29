# Exact label-information retention of arbitrary quantum preparations

30 October 2026, Brisbane. Root's central construction, developed with C's
pure-frame extraction and B's independent modular reconstruction. Independent
whole-file challenge is pending. This is a supplied finite-channel theorem,
not physical channel acquisition or historical-priority clearance.

## 1. Operation and exact statement

Let n>=2 and let tau_1,...,tau_n be finite-dimensional density matrices.
The input label X is EXPLICITLY classical. The preparation channel sends
i to tau_i. For arbitrary finite quantum reference R and classical-quantum
hypotheses rho_XR,sigma_XR, define

 J_X=D(rho_XR||sigma_XR)-D(rho_R||sigma_R),
 J_tau=D((tau tensor id)rho||(tau tensor id)sigma)-D(rho_R||sigma_R).

Only defined finite differences are admitted. Let S be the support of
sum_j tau_j and let Pi_i project, WITHIN S, onto the kernel of
sum_(j!=i)tau_j. Set r_i=Tr(tau_i Pi_i), r=min_i r_i.

**Theorem.** For every admitted pair and every finite R,

    J_tau >= r J_X.                                      (1)

The constant r is SHARP, even restricting R to dimension1 and using
equal-reference hypotheses. Thus the sharp reverse factor is1/r if r>0,
and infinite if r=0. Equivalently,

 D_out >= r D_in+(1-r)D_reference.                        (2)

This does NOT follow merely from D_out>=rD_in. No classical-output
equal-reference/conditional equivalence is imported for these quantum
outputs. The changing-reference term is proved below.

For rational density matrices, kernel projectors, r_i and the sharp factor
are acquired by polynomial exact rational linear algebra. No optimization
over reference states, matrix logarithm or eigenvalue precision oracle is
needed for this operation. Exact supports are substantive input information.

## 2. The algebraic extraction identity

Assume first every r_i>0, and put E_i=Pi_i/r_i. On output Hilbert--Schmidt
space define T(Y)_i=Tr(E_iY), with adjoint T*e_i=E_i. This linear extraction
is NOT claimed to be a jointly normalized POVM.

Positivity implies Pi_i tau_j=tau_j Pi_i=0 for j!=i. Therefore

 T|tau_j>=e_j,
 T L_tau_j T*=T R_tau_j T*=(1/r_j)|j><j|.                 (3)

For example the (i,k) entry of the first identity of operators is
Tr(E_i tau_j E_k): it vanishes unless i=k=j, when it equals
Tr(tau_j Pi_j)/r_j^2=1/r_j. The right-multiplication case follows by
cyclicity of trace with the SAME complex cross terms. The Pi_i need not
be mutually orthogonal. This is precisely why replacing T by an unambiguous
measurement's simultaneous normalization would lose the sharp constant.

For ANY two positive operator families X_i^L,X_i^R on an auxiliary space,
let Q_i=X_i^L+X_i^R and

 W=sum_i L_tau_i tensor X_i^L+R_tau_i tensor X_i^R,
 v=sum_i |tau_i> tensor u_i.

Equation(3) gives

 (T tensor I)W(T* tensor I)=diag(Q_i/r_i),
 (T tensor I)v=col(u_i).

The inverse-form Cauchy inequality, or the variational formula for
v*W^-1v, consequently proves

    <v,W^-1v> >= sum_i r_i<u_i,Q_i^-1u_i>.               (4)

Use faithful weights/restrict to S where necessary; actual modular weights
below are positive. No unsupported one-family CQ Fisher equality is used.

## 3. A direct unequal-reference modular gauge

Take faithful input blocks A_i>0 and Hermitian tangent blocks H_i. Write
M=sum_i A_i, H=sum_i H_i. For s in(0,1), on reference Hilbert--Schmidt
space put

 Q_i=s L_Ai+(1-s)R_Ai, Z=sum_i Q_i,
 z=Z^-1 H, u_i=H_i-Q_i z.

Then sum_i u_i=0 and square completion gives the input conditional
modular Hessian

 sum_i <H_i,Q_i^-1 H_i>-<H,Z^-1H>
      =sum_i <u_i,Q_i^-1u_i>.                           (5)

The output modular operator on HS(S) tensor HS(R) is

 W=s sum_i L_tau_i tensor L_Ai
           +(1-s)sum_i R_tau_i tensor R_Ai.

Its tangent is v_H=sum_i|tau_i> tensor H_i. Because Tr(tau_i)=1,

 W(|I_S> tensor z)=sum_i|tau_i> tensor Q_i z,
 <I_S tensor z,W(I_S tensor z)>=<z,Zz>.

The cross term of v_u=sum_i|tau_i> tensor u_i with I_S tensor z
vanishes by sum_i u_i=0. Thus the output conditional modular Hessian is
EXACTLY

    <v_H,W^-1v_H>-<H,Z^-1H>=<v_u,W^-1v_u>.              (6)

Apply(4) with X_i^L=s L_Ai and X_i^R=(1-s)R_Ai. Equations(5),(6) give
the conditional modular comparison with factor r for EVERY s. Integrate
over s using the ordinary BKM divided-difference representation
g_A(H)=integral_0^1 <H,[sL_A+(1-s)R_A]^-1H> ds.
Then integrate the Hessian along the affine path from sigma to rho with
Taylor weight1-t. The Bregman differences are exactly J_tau and J_X.
This proves(1),(2) for faithful hypotheses with arbitrary reference change.

Finite-divergence boundary hypotheses follow by mixing BOTH with the SAME
faithful cq state on the common input/reference support and passing to the
common-mixture limit. Output space is restricted to S, on which faithful
input blocks give faithful outputs. Infinite-minus-infinite is never used.
If r=0, inequality(1) is simply conditional DPI/nonnegativity; sharpness
is still established next.

## 4. Sharpness with ordinary classical endpoint priors

Fix i. Choose positive weights w_j for j!=i summing to1 and let
omega=sum_(j!=i)w_j tau_j. Compare input rho=|i><i| with the faithful
prior q_i=epsilon, q_j=(1-epsilon)w_j. Their classical divergence is
log(1/epsilon). The output comparison is tau_i versus

    Omega_epsilon=(1-epsilon)omega+epsilon tau_i.

Inside S, Pi_i is exactly ker omega. The compression Pi_i tau_i Pi_i
is positive definite on this kernel: a vector killed by both omega and
tau_i would lie outside S. Small eigenvalues of Omega_epsilon are therefore
Theta(epsilon), with cluster projector Pi_i+O(epsilon); remaining eigenvalues
are bounded away from0. Equivalently, min-max plus
Omega_epsilon>=epsilon(omega+tau_i) for epsilon<=1/2 and the fixed positive
gap of omega on its range gives

    log Omega_epsilon=(log epsilon)Pi_i+O(1).

The cluster-projector error times log epsilon remains bounded. Hence

 D(tau_i||Omega_epsilon)=r_i log(1/epsilon)+O(1).          (7)

The ratio tends to r_i. If Pi_i=0 the output divergence stays bounded,
so the ratio tends to0. These hypotheses have trivial/equal reference;
if faithful rho is desired, regularize it on a smaller scale and use
continuity at each positive epsilon. Equation(7) proves sharpness and
the zero convention without a quantum-reference search or a claimed
favorable rate uniform over channels.

## 5. An explicit finite Choi certificate

The inequality also has a direct coefficient certificate for the two-family
source pencil diag(X_i^L,X_i^R) direct_sum [[W,V],[V*,I]], where
V=sum_i|tau_i> tensor U_i and sum_i U_i=0. The classical-label target is
[[diag(Q_i),U],[U*,cI]], with c=1/r=max_i1/r_i.

Use the arrow Kraus Z/sqrt(c), where Z's upper block is T* and its bottom
entry is c. Its congruence gives target top diag(Q_i/(c r_i)), exact U
offdiagonal and bottom cI. Fill each diagonal deficit
(1-1/(c r_i))Q_i from BOTH corresponding source effect blocks. All fills
are nonnegative. For rational tau, the Choi matrices are rational outer
products ZZ*/c and scalar diagonal fills; no square root is evaluated.
This is a solver-free CP pencil certificate, not a physical degrader.
C independently executed the SAME binary0,+ case's27-order rank1 Choi
coefficient identity in c_cq_extension/EXACT_TWO_FAMILY.json.

## 6. Acquisition, predecessors and limits

Kernel projectors of rational Hermitian matrices are rational: for any
rational full-column kernel basis V use V(V*V)^-1V*. One may compute the
kernel of sum_(j!=i)tau_j in the full output space; the common kernel of
all tau_j contributes zero to r_i and can be subtracted as a nested
projector. Exact rank/linear algebra and traces have polynomial bit cost.
No arbitrary numerical near-zero eigenvalue is declared an exact support.

For independent pure preparations with Gram G, r_i=1/(G^-1)_ii. The sharp
reverse factor is max_i(G^-1)_ii. For |0>,|+>, r=1/2 and it is2. The
ordinary heralded inverse has uniform success1-1/sqrt2, a different physical
operation with weaker bound2+sqrt2. UDM reciprocal states/support subspaces
are established predecessors (Rudolph--Spekkens--Turner2003; Chefles1998),
not new inventions here. B's general pure-pair resolvent proof independently
earns the equal-reference answer; this proof pays the full conditional and
mixed-output operation. Precise broader-world priority remains UNKNOWN.

The exact coefficient is NOT robust under unrestricted channel uncertainty:
any positive full-rank contamination of every preparation makes r=0 for
n>=2. This is a material access boundary, not a physically stable inverse.
The theorem concerns supplied state matrices and a worst-case information
ratio. It does not acquire a quantum experiment, jointly normalized UDM,
capacity, guessing/privacy order, a correlated-block constant or a
civilisation-level operational technology. Product-source retention is
multiplicative at the full product alphabet, as independently derived by B;
it does not make the same single-use reverse factor unchanged under reuse.
