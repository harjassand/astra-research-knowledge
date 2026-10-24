# Case D: exact primary-source pin

**Source checked:** Fiorillo & Raffelt, *Flavor solitons in dense neutrino gases*, corrected arXiv v2 (16 Oct 2025), Appendix D.3; [full text](https://arxiv.org/html/2303.12143v2), [PRD 107, 123024 (2023)](https://doi.org/10.1103/PhysRevD.107.123024). Scope limited to this paper, as requested.

## Spectrum and instability

Appendix D.3 Eq. (116) gives the Case-D angular spectrum on $v\in[-1,1]$:

\[
G(v)=D_v^z=0.11-0.5\exp[-12.5(1-v)^2].
\]

Its sole zero is $v_c=1-\sqrt{\log(0.5/0.11)/12.5}=0.6519623316214435\ldots$, reported in the paper as $v_c=0.652$. Thus $G>0$ for $-1\le v<v_c$, and $G<0$ for $v_c<v\le1$. Appendix D.3 says both sufficient homogeneous-instability conditions (its Eq. (10)) hold and gives the normalized unstable root
\[
\bar u=\Omega/M_1^z=-0.203994-0.211175i
\]
(Eq. (117)). For a single crossing, Appendix A shows there is at most one unstable frequency; the D.3 conditions establish its existence. This is the collisionless, homogeneous, axisymmetric fast-limit problem. The EOM absorbs the neutrino interaction scale $\mu$ into dimensionless time (Sec. II.1, Eq. (6)); an exactly aligned state is the unstable fixed point, so the physical pendulum excursion requires a perturbing seed.

The paper's main-text Case-D check reports $G_0=4.7334$, $G_1=-5.2665$, $\Omega=1.0743\pm1.1121i$, $\lambda=|\Omega|=1.5462$, and $\sigma=\mathrm{Re}\,\Omega/|\Omega|=0.6948$ (Sec. II.5 / Fig. 8 discussion). The growth rate is $\Gamma=1.1121$, with $\lambda^2=\omega_P^2+\Gamma^2$ and $\omega_P=\sigma\lambda$ (Appendix B, Eqs. (70)–(71)). Keep $\bar u$ distinct from the absolute frequency: the former is invariant to a common rescaling of the spectrum, while $\Omega,\lambda,\Gamma$ scale with the moment/time convention.

For the displayed function integrated literally against Lebesgue $dv$,
\[
q=\int_{-1}^1G\,dv\simeq0.0946686,\qquad
G_1=\int_{-1}^1vG\,dv\simeq-0.1053314.
\]
Both sign sectors have positive mass (approximately $A_+=0.1714605$, $A_-=0.0767919$); the absolute fixed-charge budget is therefore $B=2A_-\simeq0.1535838$ in this Lebesgue normalization. These moments are 50 times smaller than the paper's stated 100-mode values, consistent with the paper's separate 100-angular-mode discretization. For raw-Lebesgue evolution, do not import its absolute $\lambda=1.5462$; use $\bar u$ and raw $G_1$ consistently. This gives $\lambda_{dv}=|G_1||\bar u|\simeq0.0309266$ and $\sigma_{dv}=-\operatorname{Re}(\bar u)/|\bar u|\simeq0.6947723$.

## Peak-conversion comparator

Yes. The paper provides an exact spectrum-wide soliton solution, not only a qualitative curve. Appendix C, Eqs. (82)–(84), gives $D_v^z(t)$ and its largest excursion at the pulse center $t=0$. Here $C=\int_{-1}^{1}[|G(v)|-\operatorname{sgn}(G(v))D_v^z]/2\,dv$ is the ELN-weighted conversion functional; it is not a fraction of all neutrinos, whose total flavor-resolved occupations are not specified by this spectrum. Substituting Eq. (84) into this functional yields
\[
c(v,0)=|G(v)|\frac{(1-\sigma^2)(vG_1)^2}
 {\lambda^2+2\lambda\sigma vG_1+(vG_1)^2}.
\]
Using the raw-Lebesgue $G_1$ and normalized root above gives $C_{\rm peak}\simeq0.1228212$. Using the paper's rounded $\sigma=0.6948$ and rescaled reported values gives the earlier estimate $0.1228173$; the difference is parameter-rounding scale. Thus the current all-time certificate $C\le0.141$ lies about $0.01818$ above the first-soliton peak, while its gap to the absolute budget is about $B-0.141=0.01258$. These integrated numbers are calculations from the published exact profile, not source-reported budget gaps. The source comparator is one soliton pulse and implies no later-time bound.
