# Complete inverse realization of strict phonon passbands

## Statement and conventions

Let the desired passband endpoints be specified as **squared frequencies**
\[
0=x_0<y_0<x_1<y_1<\cdots<x_{n-1}<y_{n-1},
\]
so band \(j\) is \([\sqrt{x_j},\sqrt{y_j}]\). Fix any intercell spring constant \(K>0\), and set \(S=4K\). There is an actual passive scalar unit cell consisting of a backbone mass \(m\) and \(n-1\) pendant side masses, each attached to the backbone by one positive spring, whose full passband list is exactly the prescribed list.

The construction is minimal among star cells with every mode visible at the backbone: it uses \(n\) masses total and has no dark modes. The endpoint data determine its backbone mass and total mass as
\[
\Delta=\sum_{j=0}^{n-1}(y_j-x_j),\qquad
P=\frac{\prod_{j=0}^{n-1}y_j}{\prod_{j=1}^{n-1}x_j},\qquad
m=\frac{S}{\Delta},\qquad M=\frac{S}{P}.
\]
The empty product for \(n=1\) is one. If both \(m\) and \(M\) are prescribed independently, these two endpoint moment equations are necessary and sufficient, together with strict interlacing.

## Positive Stieltjes function from the endpoints

Define
\[
f(t)=\frac{\prod_{j=0}^{n-1}(t+y_j)}{\prod_{j=0}^{n-1}(t+x_j)},\qquad
q(t)=\frac{f(t)-1}{S}.
\]
There is a simple pole at each \(t=-x_j\). Its residue is
\[
r_j=\frac{1}{S}\,
\frac{\prod_{\ell=0}^{n-1}(y_\ell-x_j)}
     {\prod_{\substack{\ell=0\\\ell\ne j}}^{n-1}(x_\ell-x_j)}.
\]
For \(\ell<j\), both numerator and denominator contain one negative factor per such index; for \(\ell\ge j\), their factors are positive. Hence every \(r_j>0\). Since \(q(t)=O(t^{-1})\) at infinity and has only these simple poles,
\[
q(t)=\sum_{j=0}^{n-1}\frac{r_j}{t+x_j},\qquad t>0.
\]
Thus \(q\) is a rational Stieltjes function. In particular, it is positive for \(t>0\), has zero-mode residue \(r_0>0\), and is strictly decreasing on every real interval between its poles because
\[
q'(t)=-\sum_j\frac{r_j}{(t+x_j)^2}<0.
\]

The large- and small-\(t\) coefficients are fixed directly by the endpoints:
\[
q(t)=\frac{\Delta}{S}\frac1t+O(t^{-2})\quad(t\to\infty),
\qquad
q(t)=\frac{\prod_j y_j}{S\prod_{j\ge1}x_j}\frac1t+O(1)
      =\frac{1}{M t}+O(1)\quad(t\downarrow0).
\]
The second expansion uses \(x_0=0\). Therefore the translational residue is \(r_0=1/M\), exactly the residue expected for a mass-normalized backbone coordinate in a connected cell of total mass \(M\).

## Foster expansion and positive star parameters

Set
\[
R(t)=\frac{1}{tq(t)}.
\]
The poles of \(q\) are \(-x_j\), located at distinct nonpositive real points. On each interval \((-x_{j+1},-x_j)\), \(q\) decreases from \(+\infty\) to \(-\infty\). It has exactly one simple zero there. Write that zero as \(-\nu_j^2\), where
\[
x_j<\nu_j^2<x_{j+1},\qquad j=0,\ldots,n-2.
\]
There are no other zeros: \(q\) has numerator degree \(n-1\), and these are already \(n-1\) distinct roots. Thus the poles of \(R\) are precisely \(-\nu_j^2\). At such a pole its residue is
\[
k_j=\operatorname*{Res}_{t=-\nu_j^2}R(t)
    =-\frac{1}{\nu_j^2 q'(-\nu_j^2)}>0.
\]
At infinity \(R(t)\to S/\Delta=m\). Partial fractions therefore give the positive Foster form
\[
R(t)=m+\sum_{j=0}^{n-2}\frac{k_j}{t+\nu_j^2}.
\]
For each term use a side spring of stiffness $k_j$ and define its side mass by
\[
M_j=\frac{k_j}{\nu_j^2}>0.
\]
Then \(k_j/M_j=\nu_j^2\), and
\[
R(0)=m+\sum_j\frac{k_j}{\nu_j^2}=m+\sum_j M_j=M.
\]
For \(n=1\), the sum is empty and \(M=m=S/y_0\): the single backbone mass and intercell spring realize the lone band.

## Why this star realizes the endpoints

Let \(D_0\) be the mass-normalized internal spring matrix of the constructed star, with no intercell spring included, and let \(v=e_b/\sqrt m\) be the mass-normalized backbone coordinate. A Schur complement at the backbone gives
\[
v^T(tI+D_0)^{-1}v
=\frac{1}{t\left(m+\sum_j k_j/(t+\nu_j^2)\right)}
=\frac{1}{tR(t)}=q(t).
\]
The internal matrix is connected and has just one zero mode, the rigid translation. The positive residues of \(q\) show that the backbone sees all \(n\) eigenvalues; its poles are exactly \(-x_j\), so \(\operatorname{spec}(D_0)=\{x_j\}_{j=0}^{n-1}\). The rank-one determinant lemma now yields
\[
\frac{\det(tI+D_0+Svv^T)}{\det(tI+D_0)}
=1+S v^T(tI+D_0)^{-1}v
=1+Sq(t)=f(t).
\]
Consequently \(D_0+Svv^T\) has eigenvalues \(y_j\), since its characteristic-polynomial ratio is exactly the specified endpoint ratio. For Bloch phase \(q_{\rm B}\), the intercell update is \(s(q_{\rm B})vv^T\) with \(s=4K\sin^2(q_{\rm B}/2)\in[0,S]\). Each ordered eigenvalue increases monotonically between its values at \(s=0\) and \(s=S\); hence the passbands are exactly \([\sqrt{x_j},\sqrt{y_j}]\). This is a passive finite object, not only a feasible indicator function.

## Endpoint trace and logarithmic moments

The first spectral moment is
\[
\int_0^\infty 2\omega\chi(\omega)\,d\omega
=\sum_j(y_j-x_j)=\Delta=\frac{S}{m},
\qquad
\chi(\omega)=\sum_j\mathbf1_{[\sqrt{x_j},\sqrt{y_j}]}(\omega).
\]
The endpoint product is
\[
\frac{\prod_j y_j}{\prod_{j\ge1}x_j}
=\frac{S}{M}=\Omega_r^2,
\qquad \Omega_r=\sqrt{S/M}.
\]
Equivalently, the frequency-endpoint product is \(\prod_j\sqrt{y_j}/\prod_{j\ge1}\sqrt{x_j}=\Omega_r\). With a common lower cutoff at zero, this gives the exact logarithmic moment
\[
\int_0^\infty\frac{\chi(\omega)-\mathbf1_{[0,\Omega_r]}(\omega)}{\omega}\,d\omega=0.
\]
These are also immediate from the \(t\to\infty\) and \(t\downarrow0\) coefficients of \(f(t)=1+Sq(t)\). They are necessary endpoint identities, and the Foster construction shows they are part of a complete realization for strict interlacing in this one-backbone, one-intercell-spring class.

## Dark modes, degeneracies, and cost

Strict interlacing makes all residues \(r_j\), zeros \(\nu_j^2\), spring constants \(k_j\), and side masses \(M_j\) strictly positive. No side mode is dark: each pole of the backbone resolvent has nonzero residue. Endpoint equalities cause cancellations in \(f\) and lower the active rational order. A zero-width band or touching adjacent bands is then represented by the reduced minimal star; an additional mode hidden by the canceled factor is not identifiable from the passband data and would be a dark internal degree of freedom. Coincident side-resonance limits can likewise create dark linear combinations. The strict theorem does not assign masses or springs to such invisible modes.

For input endpoints represented exactly, the residues follow by products and the \(n-1\) resonances are roots of a known rational function, each uniquely bracketed in \((x_j,x_{j+1})\). A straightforward implementation evaluates \(q\) in \(O(n)\) work per point and uses safeguarded bisection/Newton on each interval; this is \(O(n^2 p)\) arithmetic for \(p\) root iterations, with \(O(n)\) storage. Product residues can be formed in \(O(n^2)\) straightforwardly. This is a finite constructive algorithm, not a claim of a special fast synthesis method. Near endpoint collisions, residues or gaps become small and the inverse map becomes ill-conditioned; the required dynamic range and output precision can grow sharply. Therefore exact strict realizability does not imply robust fabrication under finite tolerances.

This is the classical finite Stieltjes/Foster synthesis pattern in an explicit mechanical realization. No novelty or priority claim is made for the synthesis principle.

## Exact two-band sanity check

For squared endpoints $(x_0,y_0,x_1,y_1)=(0,1,4,9)$ and $S=4$, the construction gives
\[
q(t)=\frac{6t+9}{4t(t+4)}=\frac{9/16}{t}+\frac{15/16}{t+4},
\quad \nu_0^2=\frac32,
\quad R(t)=\frac23+\frac{5/3}{t+3/2}.
\]
Thus the backbone mass is $m=2/3$, the side spring is $k_0=5/3$, and the side mass is $M_0=10/9$, giving $M=16/9$. The internal squared frequencies are $0,4$; after the $S=4$ rank-one update they are $1,9$. This checks the endpoint and mass formulas in an exact rational fixture.
