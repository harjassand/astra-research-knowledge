# FI quartic packet audit and integration note

**Scope:** internal mathematical audit for Astra research-capital synthesis. **Status:** source-derived, independently replayed finite algebra, and an exact acoustic/covariance asymptotic. External correctness and novelty remain **UNKNOWN**. No negative compatible quasiconvexity gap, full rank-one-convexity-to-quasiconvexity theorem, physical result, or civilisation-scale breakthrough is established.

## Strongest result

For the packet's fixed non-polyconvex quartic $G$, an explicit pair of independent normalized rank-one contacts approaches a common line with separation $s_e\asymp e$, while the smallest acoustic eigenvalue is asymptotic to $(65/3)e^4$. Consequently, the packet's fixed-integrand acoustic modulus obeys
\[
\limsup_{e\downarrow0}\frac{\mu_G(s_e)}{s_e^4}\le \frac5{624}.
\]
The associated balanced rank-one covariance has anisotropy $\tau_e=13e^2/(1+13e^2+36e^4)$ and
\[
\frac{\lambda_{\min}H_G(C_e)}{\tau_e^2}\longrightarrow\frac5{78}.
\]
For $e=1/(2m)$, two Fourier modes realize this covariance by smooth periodic gradients. Adding two nonresonant modes of amplitude $e^3$ gives a full-rank balanced covariance and Hessian, still with zero cubic vector and $|D\varphi_m|_F\le2+2e^3$. The enlarged fields satisfy $M_2=\mathbb E|D\varphi_m|_F^2=1+e^6$ and
\[
\frac{\lambda_{\min}H_G(C_e^{\rm full})}{M_2\tau_e^2}\longrightarrow\frac5{78},
\qquad \tau_e:=1-\lambda_{\max}(C_e^{\rm full}/M_2).
\]
Thus no lower bound $\lambda_{\min}H_G(C)\ge c M_2\tau^\alpha$ can hold along this full-rank compatible family for $\alpha<2$. The acoustic modulus bound remains a pair-test upper bound; there is no matching lower bound, no universal exponent, and no Schur-loss discontinuity or negative Jensen gap in these periodic constructions. Their gradients are uniformly bounded, hence their fourth powers are uniformly integrable; their growing Fourier bandwidth does not give strong-$L^4$ convergence to a fixed one-line field. The exact construction and frequency argument are in [DERIVATION.md](DERIVATION.md).

## Mathematical audit

The packet's two-contact theorem is scoped to rank-one-convex homogeneous quartics in the complete nine-coefficient left-SO(2)-invariant cone. It states that a balanced covariance of rank at least two has singular averaged Hessian exactly in the displayed polyconvex class $\mathcal P_2$, equivalently when there are two independent rank-one Hessian contacts. The accompanying all-35-coefficient one-quadric closure is broader, but the exceptional-class classification is not. The proof uses indefinite Finsler decomposition, cubic closure on the Finsler kernel, rank-one/invertible distinguished-background cases, and explicit acoustic tests in singular top-block cases. The source contains the analytic details; independent replay does not replace external proof review or proof-assistant formalization.

The packet's compatible concentrating sequence has $H_\rho\succ0$ and covariance $C_\rho\succ0$ for every $\rho>0$, converges to a nonzero singular $H_0$, and has Schur-loss limit $80089/21313530>0$ although the limiting loss is zero. Its actual optimized gaps are positive. Fourth-moment mass concentrates on shrinking supports, so this sequence is not equiintegrable in $L^4$ and does not settle strong-$L^4$ continuity. The separate bounded law is not compatible. Strong $L^4$ convergence gives convergence of $b,H,c$, but not by itself the relative control $r_n^TS_n^{-1}r_n\to0$ required at a singular Hessian. For $G$ and a fixed perturbation of a one-line base $\zeta e_{12}$, the effective null cubic has no first-order term; this conditional calculation does not control higher-order Schur degeneracy or arbitrary sequences. Compatible equiintegrable/strong-$L^4$ loss continuity remains **OPEN** here.

A restricted contact-shear transfer is proved in [DERIVATION.md](DERIVATION.md): after volume-preserving straightening, Jensen applies to residual profiles separated in two unimodular torus coordinates. It does not cover arbitrary coupled profiles. An exact nonconstant $G$ example in that class has positive gap $4699/2592$, not a negative witness.

## Relation to capital

The capital interface was read first. The audited capital checkout is at revision b7f166a4e0495acc01b6657be44a364432475df4, with clean status at audit end. The task-provided main revision ace0cfc4437fe91c20ccd24d69e0ee4bb335e871 and PR83/base metadata were treated as routing context, not revalidated against a remote service.

N800 is the closest predecessor. It already has (i) all-35 one-quadric nullspace closure, (ii) the full-nine exceptional-class singular-face Jensen theorem, and (iii) an integration-derived near-singular $F=(\det A)^2$ fixed-bandwidth compatible family whose optimized gap tends to zero while the limiting gap is $1/4$ and the minimizing background escapes. The current packet's continuity obstruction is complementary: fixed non-$\mathcal P_2$ $G$, a nonzero singular Hessian limit, and an actual concentrating compatible family give a positive limiting Schur loss while the endpoint loss is zero. Neither construction is a negative compatible gap. N800's positive-definite Schur remainder and external review gates remain open.

N797's closed-heat results are scoped to $F_\star$ and the adjacent $H_L$ family, not the full quartic cone. N740's pointwise compatible two-form completion does not supply a smooth/global closed selection. Their universal Q4/Morrey gates remain open. No Astra capital file was edited or promoted by this audit.

## Verification and provenance

- Replayed the supplied verifier from the owned copy. All 12 grouped checks passed; generated verification JSON matched the supplied JSON byte-for-byte.
- Ran [results/check_fi_quartic.py](results/check_fi_quartic.py), which independently rebuilds the contact identity, rank-six acoustic Gram, concentration moments/Schur limit, shear chain rule, separated shear witness, acoustic/covariance asymptotics, compatible covariance realizations, full-rank determinant, contact-Hessian positivity, and cubic nonresonance. Nine groups pass under SymPy 1.14.0.
- Read-only inputs from work/FI-sources are byte-identical to the owned source snapshot listed in [OWNED_MANIFEST.json](OWNED_MANIFEST.json). The capital checkout remained clean.
- Primary literature and exact access depth are logged in [PRIMARY_READ_LEDGER.md](PRIMARY_READ_LEDGER.md). No full third-party paper, environment, or cache is included.

The complete optimized inequality over compatible positive-definite instances, strong-$L^4$ compatible loss continuity, external correctness, priority, and novelty remain **UNKNOWN/OPEN**. Checks establish integrity and finite identities only.
