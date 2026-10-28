# Direct matrix heatflow transport from complete MLSI

2026-10-27. Optional alternative lemma, not a dependency of the frozen conservative adaptive-rank proof.

Let a compact diffusion act entrywise on finite-dimensional matrix densities, with normalized trace/integration tau. Let E be averaging on the classical parameter while preserving the matrix algebra. Assume

 Ent(rho)=D(rho||E rho),  Fisher(rho)>=alpha Ent(rho),

at every matrix level, with alpha>0. For a self-adjoint matrix-valued observable f let L²=||Gamma(f,f)||, with Gamma=sum_j(partial_j f)² in an orthonormal diffusion frame. Then

 |tau[(rho-E rho)f]|<=2 L sqrt(Ent(rho)/alpha).

## Proof for faithful smooth densities

Set rho_t=P_t rho, E_t=Ent(rho_t), and I_t=Fisher(rho_t). Entropy dissipation and MLSI give E'_t=-I_t and E_t<=e^(-alpha t)E_0.

The matrix derivative chain rule is

 partial_j rho_t=Omega_(rho_t)(partial_j log rho_t),
 Omega_rho(Y)=integral_0^1 rho^s Y rho^(1-s) ds.

Cauchy-Schwarz for this positive logarithmic-mean quadratic form, summed over the frame and integrated over the parameter, gives

 |tau[(A rho_t)f]|<=sqrt(I_t) sqrt(tau sum_j (partial_j f) Omega_(rho_t)(partial_j f)).

For Hermitian Y, the logarithmic mean is bounded above by the arithmetic mean in this quadratic form:

 Tr[Y Omega_rho(Y)]<=Tr[rho Y²].

This follows entrywise in an eigenbasis of rho from L(x,y)<= (x+y)/2. Consequently the second square root above is at most L, because tau rho_t=1.

Integrating the heatflow derivative gives

 |tau[(rho-E rho)f]|<=L integral_0^infinity sqrt(I_t) dt.

For0<beta<alpha, integration by parts and entropy decay yield

 integral_0^infinity e^(beta t) I_t dt
 =E_0+beta integral_0^infinity e^(beta t) E_t dt
 <=alpha E_0/(alpha-beta).

Weighted Cauchy-Schwarz now bounds the square of the previous integral by alpha E_0/[beta(alpha-beta)]. Set beta=alpha/2 to get4E_0/alpha, proving the claim.

Faithful mixing and heat regularization extend the bound to finite-entropy matrix densities. The use of normalized versus ordinary matrix trace is immaterial after scaling the density accordingly. For self-adjoint f the row and column gradient seminorms coincide.

## Relation to the mixed-flag application

The separately verified SU(3r) complete MLSI has alpha=3r in the entropy-decay convention above, and the exact test gradient obeys L²<=3/r. Thus this lemma would give the stronger correlation estimate2 sqrt(I(U:P))/r after independent receiving. The already frozen root proof deliberately uses the more conservative imported estimate8 sqrt(I(U:P))/r, and its receipt must not be silently replaced by this alternative derivation.
