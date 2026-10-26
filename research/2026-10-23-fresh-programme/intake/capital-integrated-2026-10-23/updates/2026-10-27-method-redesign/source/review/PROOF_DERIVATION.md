# Independent global-proof derivation

26 October 2026. Scope: frozen X13/X68 phase-one scientific sources only. This
derivation was written after reading those sources; it is an audit, not an
independent pre-exposure construction or a repair credited to either candidate.
The accepted free Umegaki representation and its metric/witness lift are premises.

## Domain, closure, and denominator

Write B=[(1,0),(0,1),(-1,-1)]^T, u=Bz and
A_C(Q)=sum_y (CB)_y^T(CB)_y tensor W_y(C)^(-1).
For Q_i>=0, sum Q_i=I, strict channel positivity gives
min_i C_yi I <= W_y(C) <= max_i C_yi I. Therefore the boundary introduces no
singular output inverse. With
V=B^T L^T diag(1/max_i L_yi) LB, injectivity of L on zero-sum inputs gives V>0
and A_L(Q)>=V tensor I. In particular det(V)/Tr(V)>0 is a rational coercivity
bound. Normalize the two input vectors, and use the supplied dimension cutoff:
the quotient is continuous on a compact domain with denominator bounded away
from zero. Replacing Q_i by (1-epsilon)Q_i+epsilon I/3 identifies the open and
closed suprema. All uses of this boundary require the stated strict channel
positivity and informative L; none extends to singular output mixtures.

The supplied Umegaki bridge can also be checked locally: BKM is the integral of
the inverse left/right arithmetic superoperators. Normalizing their common
reference superoperator gives effects Q_i. The common gauge
u_i=a_i-Q_i sum_j a_j has zero sum and removes the reference Hessian for both
channels. Thus an all-effect free upper inequality integrates to the conditional
Umegaki inequality. Conversely the active/vacuum off-diagonal construction has
equal reference marginals and logarithmic BKM leading term F_C. The ordered
limits (first tangent size, then vacuum weight) give every free quotient as a
supremum lower bound. A free boundary witness is consequently a legitimate
lower bound; it need not itself be a finite pair attaining the coefficient.

## X13 Gram SDP: why it is exact

Let r contain z_1,z_2 and the six actual inverse-action vectors x_Cy. Define
M_i=r^*Q_i r. Let D_i have column C_yi e_xCy-a_Cy, where a_Cy occupies the
first two coordinates. Then sum_i M_i D_i=0, and the F_C are diagonal traces
against the corresponding output labels. This gives the primal SDP after
normalizing F_L=1.

Conversely put M0=sum_i M_i and R=M0^(1/2), on its support. Since 0<=M_i<=M0,
ker M0 is in ker M_i. The effects Q_i=R^+ M_i R^+ sum to identity on the
support, and the labelled vectors are r_a=R e_a. Left multiplication of the
Gram equation by R^+ gives the genuine vector equation W_Cy x_Cy=v_Cy.
There is no untested component outside the Gram span: each term lies in that
support. Strict positivity of W makes x_Cy its unique inverse action. This
proves both directions, including rank-deficient Gram data. Taking real parts
of Hermitian M_i preserves the real linear equations and diagonal objectives;
their real PSD property suffices for a real realization. Thus the real SDP
has the full complex value, without a commuting restriction.

For the dual, sum Tr(sym(D_i X^T) M_i)=0. Exact rational positivity of
c C_Li-C_Ki/g+sym(D_i' X^T)+eta I therefore yields
F_K <= g(c+eta T'), provided the scaled trace bound T' is correct. It is:
the input labels contribute <=max s_u^2/beta, K inverse labels contribute
<=max s_K^2 c0/min K, and L labels contribute <=max s_L^2/min L.
Here c0=Tr(V^-1 U), U=B^T K^T diag(1/min K_yi) KB. This remains valid for
singular K. An exactly checked rounded Gram witness need not satisfy the
primal inverse equations: using its actual effects gives the rational formula
sum_y (G0 a'_Cy)^T (sum_i C_yi G_i)^(-1)(G0 a'_Cy), which is a genuine free
witness regardless of the floating primal residual. The lead alternative is
therefore sound at its stated scope, including its residual charge and fallback.

## Common covariance identity and the selected small certificate

For any positive W_1,W_2,W_3 summing to I define
N=diag(W_1^-1,W_2^-1)+[I;I]W_3^-1[I,I]. Block multiplication, preserving
all operator product orders, gives
N^-1=diag(W_1,W_2)-[W_1;W_2][W_1,W_2].

Put P=[I_2,0], R=P L^-1, q=[Q_1;Q_2],
M_i=R diag(L[:,i])R^T, and e_1=(1,0), e_2=(0,1), e_3=0. Applying the preceding
identity in L output coordinates yields
A_L(Q)^-1=sum_i M_i tensor Q_i-q q^*.
For a direct verification, if D_L=P LB and b=P L[:,3], then
R=D_L^-1(P-b 1^T). The output covariance diag(W)-WW^* kills 1, so the constant
shift cancels. Its coordinate change is exactly the displayed inverse.

For K put D=P KB, x_i=P K[:,i], T_i=diag(x_i)-x_i x_i^T,
H_i=M_i-e_i e_i^T and S_i=D H_i D^T. Each T_i is positive definite because
the three entries of K[:,i] are positive. Each H_i is the positive definite
scalar vertex A_L(e_i)^-1. Let N_K be N for the K output weights, and
X=sum_i x_i tensor Q_i. Then A_K=D^T N_K D. For c>=0,

 A_K<=c A_L iff D A_L^-1 D^T <= c N_K^-1.

Indeed T=N_K^(1/2)D A_L^(-1/2) has T^*T<=cI iff TT^*<=cI. This uses no
inverse of D or K, and therefore covers singular K. Expanding the right-hand
inequality produces exactly

 P_c(Q)=c N_K^-1-D A_L^-1 D^T
       =sum_i(cT_i-S_i) tensor Q_i+(c-1)V(Q),
 V(Q)=sum_i x_i x_i^T tensor Q_i-X X^* >=0.

The covariance is the compression of a projection (equivalently operator
Schwarz). Hence for c>=1 the three vertex tests cT_i-S_i>=0 are sufficient
and necessary. Their maximum generalized eigenvalue is the exact coefficient
whenever it is at least one, including singular K.

For c<1 put t=1-c. For any real center z,

 P_c(Q)=t(X-zI)(X-zI)^*+
         sum_i[cT_i-S_i-t(z-x_i)(z-x_i)^T] tensor Q_i.

This is an identity for arbitrary complex noncommuting Q_i. The three
rational 2x2 residuals therefore certify the global bound. The affine 3x3
Schur LMIs in X13 worker1/PROOF.md are exactly the substitution a=t z.
X68's inverse-K center certificate is a congruent coordinate version when
K is invertible; X68's general 9x9 version removes that assumption directly.

To establish center completeness, for a test-vector pair with columns U put
E_i=U^*Q_i U, G=sum E_i and d=sum E_i x_i. Normalize Tr G=1. Projection onto
ran U gives ||X^*w||^2>=d^*G^+d, with the range condition included. Every
E_i>=0 is realized with equality on supp G by U=G^(1/2) and
Q_i=G^(-1/2) E_i G^(-1/2). Thus the exact minimum is the finite SDP in
E_i and s>=d^*G^+d. Slater holds at E_i=I/6 and large s. A finite objective
and primal strict feasibility give an attained dual; its lower-right scalar
is t and its upper block can be decreased to bb^*/t. Writing b=t z leaves
precisely the three residual conditions. Conjugation averaging gives real
data and a real center. The converse and the all-complex domain therefore
hold; no favorable optimizer was assumed.

This also gives a genuine refinement at this interface: if the coefficient
is below one, every strict violation is realized in real active dimension
at most two. Above one, scalar vertices suffice. It improves the supplied
active dimension three bound, but historical priority of this specialized
refinement is not established by this audit.

## X68 general moment cone and complete SDP

For p test columns put X_i=V^*Q_iV, D0=diag(X_i), Y_ij=V^*Q_iQ_jV and H=D0-Y.
Then Y,H>=0 and HE=0 for E=[I_p;I_p;I_p]. These necessary conditions are
also sufficient. Factor D0=A0^*A0 block diagonally, with A0 surjective onto
the direct sum of supports. There is a contraction R0 with A0^*R0 A0=Y.
Set V0=A0 E. The row-sum constraint implies R0 V0=V0. Dilate R0 to the
projection [[R0,sqrt(R0(1-R0))],[sqrt(R0(1-R0)),1-R0]]. It fixes (V0,0).
Compress a partition of coordinate projections by this projection. Its first
moments are exactly X_i and its second moments exactly Y_ij. Zero supports
cause no exception because A0 is taken onto its support, not inverted on a
kernel. This verifies the nontrivial converse in X68's completeness claim.

For arbitrary K, M=KB and D_K=diag(W_y^K), the singular-value equivalence
A_K<=c A_L iff c D_K-M A_L^-1 M^T>=0 holds even if M is singular. Inserting
the L covariance identity gives exactly X68's linear objective in X_i,H.
With alpha=sum Tr(diag(K[:,i])X_i)=1, strict K positivity bounds the total
trace and makes the feasible set compact. The parameterization H=TJT^T has
strict points X_i=aI, J=bI for small b/a. The dual is precisely A>=0,
A_ii=c diag(K[:,i])-M A_L(e_i)^-1 M^T, T^T(A-ss^T)T>=0. The exact rational
PSD checks certify every returned upper independently of solver flags.

## Status and execution evidence

No blocking mathematical gap was found in the frozen constructions examined.
The completeness statements are proved by the displayed converses/duality,
not by the finite checks. Lower-witness rationalization, strict output support,
singular K, and the complex domain are all covered. General numerical
acquisition may still fail or return wider valid bounds; this is an operational
limitation, not a defect in the global proof. After the final sources and six
official holdouts were explicitly released, the same scientific implementations
were replayed on all thirteen inputs. Both candidates' ten asymmetric intervals
and three controls passed exact independent checks. The selected X13 scientific
code matched phase one byte for byte; its final wrapper only made optional
nonfinite display diagnostics strict-JSON safe. X68's selected scientific source
was unchanged. Final X13 proof wording clarified the Schur argument and a dual
sign convention; neither changed an audited identity or rational certificate.
