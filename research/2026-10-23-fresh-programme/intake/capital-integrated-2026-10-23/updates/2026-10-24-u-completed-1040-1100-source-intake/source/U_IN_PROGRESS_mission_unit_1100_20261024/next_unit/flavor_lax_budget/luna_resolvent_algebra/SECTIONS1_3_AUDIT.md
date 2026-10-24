# Sections 1–3 algebra audit

Bounded check of `ALL_TIME_LAX_BUDGET_GATE.md`; central and frozen files were left unchanged. The corrected primary fast-system Lax definition and bilinear square are consistent with [Fiorillo–Raffelt, arXiv:2301.09650v3, Sec. III](https://arxiv.org/html/2301.09650v3). This note audits the stated homogeneous continuum equations and does not assess Sections 4–5's compactness argument.

## EOM, Lax square, and conversion equality

For $u\in\mathbb C\setminus[-1,1]$, differentiation under the integral gives

\[
\dot L_D(u)=D_0\times L_D(u)-D_1\times\int_{-1}^1\frac{v^2D(v)}{u-v}\,dv.
\]

Using $v^2/(u-v)=uv/(u-v)-v$, the last integral is $uL_D(u)-D_1$, so

\[
\dot L_D=(D_0-uD_1)\times L_D,\qquad
\frac{d}{dt}(L_D\cdot L_D)=0.
\]

The dot and cross products here are complex bilinear extensions, not Hermitian ones; the scalar triple product vanishes algebraically. The sign and moment order in the gate's Eq. (5) are correct. Also $\dot D_0=D_0\times D_0-D_1\times D_1=0$, and $d|D(v)|^2/dt=0$ a.e.; the vector field is locally Lipschitz on real $L^\infty$, so the pointwise bound prevents finite-time norm blowup.

For the fixed ideal charge $\int D_z=q=A_+-A_-$, split $C=C_++C_-$ over $G>0$ and $G<0$. The pointwise ball implies $C_+\le A_+$ and $C_-\le A_-$. Charge conservation gives

\[
2(C_+-C_-)=q-\int D_z=0,
\]

so $C_+=C_-=C/2$ and $C\le2\min(A_+,A_-)=B$. If, for example, $A_+<A_-$, equality forces $C_+=A_+$, hence $c(v;D)=G(v)$ a.e. on the positive minority sector. There $D_z=-G$ and $|D|\le|G|$ force $D=-G\hat z$. The negative-minority case is symmetric. If $A_+=A_-$, equality forces this full reversal on both sectors (the tied case should be made explicit wherever “the minority sector” is used).

## Plemelj sign and local-flip continuation

For the kernel $1/(u-v)$, the upper boundary is $\operatorname{PV}\int f(v)/(x-v)\,dv-i\pi f(x)$ and the lower boundary has $+i\pi f(x)$. Thus the gate's sign is right:

\[
L_+-L_-=-2\pi i\,xD(x),\qquad \ell_+-\ell_-=-2\pi i\,xG(x).
\]

A shorter equivalent route avoids a sign-sensitive factorization. Set $M=L_z+\ell$. The invariant is exactly

\[
L_x^2+L_y^2+M^2-2M\ell=0.
\]

If $D=-G\hat z$ on an open interval $J$, then the Cauchy densities of $L_x,L_y$ vanish on $J$, and the density of $M$ is $v(D_z+G)$, also zero there. Therefore all three functions have matching upper/lower boundary values on $J$. Subtracting the two boundary versions of the invariant leaves $-2M(x)(\ell_+-\ell_-)=0$. On a subinterval avoiding $x=0$, $xG(x)\ne0$, so $M=0$ a.e. there. The original Eq. (8) follows equivalently from the difference of squares.

Here $vD$ and $vG$ are in $L^2$, so their Cauchy transforms have $L^2$ boundary values and the squared identities have $L^1$ boundary values. Since $M$'s density vanishes on $J$, its remaining support is a positive distance from every compact subinterval of $J$; hence $M$ extends holomorphically across that subinterval. Its zero boundary values make the extension identically zero there. The complement of the remaining support (a subset of the real interval) is connected, so analytic continuation gives $M=0$ off that support. Its jump then gives $v(D_z+G)=0$ a.e.; the single point $v=0$ has zero Lebesgue measure. Thus $D_z=-G$ a.e., and the ball gives $D=-G\hat z$ a.e. Its total charge is $-q$, contradicting the fiber charge $q\hat z$ when $q\ne0$. The continuation proof is valid under the stated open-interval hypothesis; it does not prove a version for arbitrary positive-measure sets.

## Boundaries

- If $q=0$, the full flip $D=-G\hat z$ lies in $K_G$: it has the required charge and $L_D=-\ell\hat z$, so $L_D\cdot L_D=\ell^2$ and $C=B$. Thus the nonzero-$q$ premise is essential to a strict gap over the relaxed fiber.
- The interval/Plemelj argument does not apply to a finite atomic angular measure. The exact capital's three-beam first-pulse example has $(v_i)=(-1,1/3,1)$, $(G_i)=(-4,-4,1)$, $A_+=1$, $A_-=8$, and $C(t_p)=B=2$. This is a first-pulse atomic counterexample to importing the continuous-spectrum local-flip obstruction into the atomic case; it says nothing about the all-time continuum claim.
