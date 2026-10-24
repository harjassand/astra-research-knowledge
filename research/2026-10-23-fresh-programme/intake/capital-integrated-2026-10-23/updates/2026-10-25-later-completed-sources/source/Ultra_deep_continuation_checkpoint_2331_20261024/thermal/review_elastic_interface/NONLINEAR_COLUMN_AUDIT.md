# Independent audit: elastic interface E9 and finite-amplitude column result

## E9: signs, constitutive derivatives, and energy

Let \(s\) be conserved solid volume per projected area, \(d\) the current
confined-layer thickness, and \(d_{\rm ref}\) the pillar reference length.
For liquid-filled straight pores, \(\epsilon=1-s/d\), so the through-column
resistance is
\[
R(d)=\frac{d}{k_l\epsilon}=\frac{d^2}{k_l(d-s)}.
\]
If upward top displacement \(v\) compresses the layer, \(d=d_0-v\). Therefore
\[
R_v=\frac{dR}{dv}=-\frac{dR}{dd}
 =\frac{s^2/(d-s)^2-1}{k_l}.
\]
It is positive on \(s<d<2s\), zero at \(d=2s\), and negative for \(d>2s\).
The sign in E9 is correct for the stated compression convention. Its units are
\(\Omega\,\mathrm m\), since \(1/k_l\) has those units.

For an incompressible neo-Hookean pillar with axial stretch
\(\lambda=d/d_{\rm ref}\), the energy per projected area is
\[
E_s=\frac{s\mu}{2}(\lambda^2+2/\lambda-3).
\]
Differentiating with respect to compression \(v\),
\[
p_s=\frac{\partial E_s}{\partial v}
 =-\frac{\partial E_s}{\partial d}
 =\frac{s\mu}{d_{\rm ref}}(\lambda^{-2}-\lambda),\qquad
K_w=\frac{\partial p_s}{\partial v}
 =\frac{s\mu}{d_{\rm ref}^2}(2\lambda^{-3}+1)>0.
\]
Thus pressure work is paid by this stored elastic energy: for a quasistatic
increment, \(dE_s=p_s\,dv\) per projected area. The reported fixture values
also agree with these expressions: \(\lambda=5/9\) gives
\(R=2.2222\times10^{-4}\,\Omega\,\mathrm m^2\),
\(R_v=80\,\Omega\,\mathrm m\), \(p_s\approx1.3422\,\mathrm{MPa}\), and
\(K_w\approx1.5830\times10^{11}\,\mathrm{Pa/m}\).
These are conditional pillar-law values, not acquired separator properties.

## E10-E11: centered-coordinate and galvanostatic derivation

Write \(\mathbf 1^T h=0\), \(\dot h=\nu_m(j-j_0\mathbf 1)\), and let
\(Y=gI+L_{\rm graph}\) with \(g>0\), \(L_{\rm graph}=L_{\rm graph}^T\ge0\).
The column law is \(u_i=f(j_i,h_i)\), with a positive current secant
\[
D_i=\frac{f(j_i,h_i)-f(j_0,h_i)}{j_i-j_0}>0
\]
(using \(\partial_j f\) when the two currents coincide). Let
\(Z=Y^{-1}\), \(K=Z+\operatorname{diag}(D_i)\), \(M=K^{-1}\), and
\(v=M\mathbf 1\). Linear differences here are exact secant identities, not
small-signal expansions. With
\(Q_i(h)=f(j_0,h_i)-f(j_0,0)\), the network equations imply
\[
\delta j=M(\delta V\mathbf 1-Q),\qquad
\mathbf 1^T\delta j=0,
\]
and hence
\[
\delta V=\frac{\mathbf 1^TMQ}{\mathbf 1^TM\mathbf 1},\qquad
\delta j=-A Q,\quad
A=M-\frac{vv^T}{\mathbf 1^Tv}.
\]
This is the galvanostatic rank-one projection; it is essential to the result.
The matrix \(A\) is symmetric positive semidefinite, annihilates
\(\mathbf 1\), and is positive definite on \(\mathbf 1^\perp\). In fact,
\[
A|_{\mathbf 1^\perp}=(P K P|_{\mathbf 1^\perp})^{-1},\qquad
P=I-\mathbf 1\mathbf 1^T/N.
\]

For the stated \(F\) in E10,
\[
\nabla F=j_0[R_{\rm tot}(h_i)-R_{\rm tot}(0)]_i
                 +\nu_m\nabla E_{\rm mech}(h).
\]
This equals \(Q\) up to a constant vector, which \(A\) removes, provided
\(P\nabla E_{\rm mech}(0)=0\). That is the flat-base force-balance
condition: the reference mechanical force must be spatially uniform on the
patches. It is automatic for the displayed translation-invariant quadratic
energy, but should be stated for a general allowed \(E_{\rm mech}\). If it
fails, \(h=0\) is not the stationary uniform-current reference and the
centered \(F\)/claim needs a compensating reference profile or affine force
term.

Under that condition, \(\dot h=-\nu_m A\nabla F\), giving exactly
\[
\dot F=-\nu_m(\nabla F)^TA\nabla F\le0.
\]
No commutation between \(A(h)\) and the mechanical Hessian is needed.

## E12 and the finite-amplitude invariant set

Suppose \(F(0)=0\), \(P\nabla F(0)=0\), the height domain is convex, and the
restricted Hessian satisfies
\(\nabla^2_{\mathbf 1^\perp}F\succeq\alpha I\) throughout it, with
\(\alpha>0\). If \(D_i+\|Y^{-1}\|\le K_{\max}\), then
\[
\lambda_{\min}(A|_{\mathbf 1^\perp})
 \ge \frac1{K_{\max}},\qquad
\|P\nabla F\|^2\ge2\alpha F.
\]
The first inequality follows from the projected-inverse formula and
\(\lambda_{\max}(PKP)\le D_{\max}+\|Z\|\). The second is the strong-convexity
gradient inequality with the centered minimizer at zero. Combining them yields
\[
\dot F\le-\frac{2\nu_m\alpha}{K_{\max}}F,
\]
which is E12. On the domain \(|h_i|<a\), every boundary point has
\(\|h\|\ge a\), so strong convexity gives \(F\ge\alpha a^2/2\) there.
Consequently the sublevel \(F(h(0))<\alpha a^2/2\) cannot reach that boundary.
This is a valid finite-amplitude invariant-sublevel argument under the stated
uniform secant and convexity assumptions.

For the displayed quadratic mechanics,
\[
\nabla^2F=j_0\operatorname{diag}(R'_{\rm tot})
                  +A_0L_{\rm space}+\nu_m B L_{\rm space}^2.
\]
On a graph-Laplacian eigenmode of eigenvalue \(\lambda\ge0\), the last two
terms are \(A_0\lambda+\nu_mB\lambda^2\), bounded below by
\(-\max(-A_0,0)^2/(4\nu_mB)\). Thus the stated sufficient alpha is correct
for \(j_0\ge0\). If \(j_0<0\), the correct general lower bound is
\(\inf_h j_0R'_{\rm tot}(h)\), not \(j_0\inf_hR'_{\rm tot}(h)\); the
written expression implicitly selects the positive-plating regime.

## Scope check

The proof is for a finite set of local, normal-conduction columns connected by
a fixed reciprocal bulk network, with local scalar resistance \(R_{\rm tot}(h_i)\),
monotone local polarization, a conservative mechanical energy, and prescribed
mean current. It does not prove E10-E12 for the spatially conducting deforming
skin. In E4 the skin has in-plane ionic conduction, two distinct moving faces,
and a nonlocal Fourier transfer relation; E4 is explicitly a linearized
free-boundary calculation. Deriving a nonlinear energy/current-gradient law
for that moving distributed conductor would be additional work. The draft's
scope caveat is therefore correct and important.
