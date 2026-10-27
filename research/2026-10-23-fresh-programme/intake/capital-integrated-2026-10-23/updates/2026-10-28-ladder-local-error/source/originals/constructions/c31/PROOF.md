# Resonance of the locally detuned hard-core pair

## Theorem and convention

Consider exactly the infinite ladder in the supplied packet, at \(g=1/5\),
in the physical two-excitation Hilbert space. Put

\[
H_\eta=H_g+\eta V,\qquad V=n_L-n_R,
\]

and let \(E=E_p(1/5)\) and \(\psi\) be the normalized unperturbed even pair.
The resolvent convention throughout is \((H-z)^{-1}\), initially for
\(\operatorname{Im}z>0\).

There are \(r>0,a>0\) such that the full physical bare-pair response

\[
r_\eta(z)=\langle p,(H_\eta-z)^{-1}p\rangle,
\qquad p=|LR\rangle,
\]

has an outgoing meromorphic continuation to \(|z-E|<r\), for all real
\(|\eta|<a\). It has precisely one pole there, a simple pole
\(\mathcal E(\eta)\), with a nonzero bare-pair residue. This pole is analytic
in complex \(\eta\) near zero and even in \(\eta\). Its expansion is

\[
\boxed{\mathcal E(\eta)
=E-\eta^2\,B_{\rm out}(E)+O(\eta^4),}
\tag{1}
\]

where

\[
B_{\rm out}(E)=
\lim_{\epsilon\downarrow0}
\langle V\psi,(H_{g,\rm odd}-E-i\epsilon)^{-1}V\psi\rangle.
\tag{2}
\]

Consequently the first nonzero imaginary term is

\[
\boxed{\operatorname{Im}\mathcal E(\eta)
=-\pi\rho_g(E)\eta^2+O(\eta^4),\qquad \rho_g(E)>0.}
\tag{3}
\]

In particular \(\operatorname{Im}\mathcal E(\eta)<0\) for all sufficiently
small nonzero real \(\eta\). The numerical value
\(\pi\rho_g(E)\simeq6.68375948395\times10^{-8}\) uses the supplied,
uncertified numerical evaluation of the exact positive integral. The theorem
uses analytic positivity, not the decimal's sign.

This is a resonance theorem for a specified matrix element of the full
infinite two-particle hard-core operator. It is not an all-times exponential
survival theorem, a device lifetime, or a hardware claim.

## One-body realization and analytic deformation

Use the sine transform on each semi-infinite bath. The one-body Hilbert space
is

\[
\mathcal K=\mathbb C e_+\oplus\mathbb C e_-
 \oplus L^2(0,\pi)_+\oplus L^2(0,\pi)_-.
\]

The bath multipliers and memory-bath coupling functions are

\[
\varepsilon_\sigma(k)=c_\sigma-\cos k,\quad
b_\sigma(k)=\sqrt{k_\sigma}\sqrt{2/\pi}\sin k,
\quad(c_+,c_-)=(5,1),\quad(k_+,k_-)=(2/25,1/25).
\]

Both memory diagonals are 3. The one-body perturbation is
\(\eta t\), where
\(t=|e_+\rangle\langle e_-|+|e_-\rangle\langle e_+|\).
It is the same physical local detuning as in the question.

For real \(|\theta|<1\), define

\[
\phi_\theta(k)=k+\theta\sin k,
\qquad (U_\theta f)(k)=\sqrt{1+\theta\cos k}\,f(\phi_\theta(k)).
\]

This is unitary on each bath \(L^2\) space because \(\phi_\theta\) is an
increasing diffeomorphism fixing 0 and \(\pi\). It acts as the identity on
the two memories. Define \(h_\eta(\theta)\) for complex \(|\theta|<1\) by
its coefficients:

\[
\varepsilon_{\sigma,\theta}(k)=c_\sigma-\cos\phi_\theta(k),\qquad
b_{\sigma,\theta}(k)
=\sqrt{k_\sigma}\sqrt{2/\pi}
\sin\phi_\theta(k)\sqrt{1+\theta\cos k}.
\tag{4}
\]

Use the holomorphic square root equal to 1 at \(\theta=0\). Both off-diagonal
memory-bath entries use \(b_{\sigma,\theta}\), without conjugating it. This
is a bounded operator-valued holomorphic family on every smaller theta disk.
For real theta it equals \(U_\theta h_\eta U_\theta^{-1}\). No complex
composition operator on arbitrary \(L^2\) functions is asserted: (4) itself
is the complex extension.

Let \(\mathcal H_{\rm harm}=\operatorname{Sym}^2\mathcal K\),
\(A_\eta(\theta)=d\Gamma_2(h_\eta(\theta))\), and

\[
P=|LL\rangle\langle LL|+|RR\rangle\langle RR|,
\qquad Q=1-P.
\]

The exact deformed physical operator is

\[
\boxed{H_\eta(\theta)=QA_\eta(\theta)Q\big|_{Q\mathcal H_{\rm harm}}.}
\tag{5}
\]

For real theta, \(U_\theta^{\otimes2}\) fixes the forbidden double-memory
vectors, hence commutes with \(Q\). Therefore (5) is unitarily equivalent
to the full physical \(H_\eta\), with its hard-core constraint intact.
Also \(V\) commutes with this real deformation and does not depend on theta.
On the physical space \(\|V\|=1\): the allowed memory occupations give
\(n_L-n_R\in\{-1,0,1\}\). This construction does not treat \(V\) as rank one.

Fix, for example,

\[
\theta_0=-i/10.
\]

The deformed bath spectra are the compact arcs

\[
\Gamma_\sigma=
\{c_\sigma-\cos(k-i\sin k/10):0\le k\le\pi\}.
\tag{6}
\]

Their imaginary part is

\[
-\sin k\sinh(\sin k/10)<0\quad(0<k<\pi),
\]

and it vanishes only at the two bath edges. The real part is strictly
increasing in the interior: its derivative is

\[
\sin k\cosh(t\sin k)+t\cos^2k\sinh(t\sin k)>0,
\qquad t=1/10.
\]

Thus these are simple arcs below the physical bands.

## The outgoing sheet really continues the physical response

For \(\operatorname{Im}z>0\), the free bath memory self-energy integral

\[
\int_0^\pi \frac{(2/\pi)\sin^2\phi_\theta(k)\,
                  \phi_\theta'(k)}{c-\cos\phi_\theta(k)-z}\,dk
\]

can be moved from the real momentum interval to its deformed contour.
There is no crossed denominator zero: the intervening contours have bath
energies in the lower half-plane. It therefore equals the original surface
resolvent

\[
r_c(z)=2\{c-z+\sqrt{(z-c)^2-1}\}.
\tag{7}
\]

Equivalently, this follows by the identity theorem from real theta at large
\(|z|\), followed by continuation in the upper half-plane. The square root
in (7) has its cut along the deformed arc and agrees with the physical branch
above the original band and on the real exterior of that band.

For every real eta, the two-memory Schur matrix of \(h_\eta(\theta_0)-z\)
in the upper half-plane is therefore exactly the physical one. Since the
physical one-body operator is self-adjoint, that Schur matrix is invertible
there. The deformed bath multiplication operators are also invertible there.
Hence

\[
\sigma(h_\eta(\theta_0))\subset\{\operatorname{Im}z\le0\}.
\]

For bounded operators \(B,C\),
\(\sigma(B\otimes1+1\otimes C)\subset\sigma(B)+\sigma(C)\).
The needed inclusion follows directly by a Dunford contour separating
\(\sigma(B)\) from \(z-\sigma(C)\); the integrand
\((\zeta-B)^{-1}\otimes(C+\zeta-z)^{-1}\) gives the inverse. The symmetric
restriction obeys the same inclusion. Thus \(A_\eta(\theta_0)-z\) is
invertible throughout the upper half-plane.

Put \(R_\eta^\theta(z)=(A_\eta(\theta)-z)^{-1}\) and define the exact
2-by-2 hard-core Schur matrix

\[
K_\eta^\theta(z)=P R_\eta^\theta(z)P\big|_{P\mathcal H_{\rm harm}}.
\tag{8}
\]

For large \(z\), all matrix elements of (8) equal the physical ones:
real-theta unitarity fixes the two forbidden vectors, and the large-z
Neumann series is holomorphic in theta. Both sides are holomorphic in the
entire upper half-plane, so equality holds there. For real eta the physical
matrix has strictly positive imaginary part:

\[
\operatorname{Im}K_\eta^0(z)
=(\operatorname{Im}z)\,P(A_\eta^0-\bar z)^{-1}
                         (A_\eta^0-z)^{-1}P>0.
\]

It is invertible. Solving the forbidden component of the resolvent equation
gives the exact compression identity

\[
(H_\eta(\theta)-z)^{-1}
=Q R_\eta^\theta(z)Q
-Q R_\eta^\theta(z)P\,[K_\eta^\theta(z)]^{-1}
                         P R_\eta^\theta(z)Q.
\tag{9}
\]

This also proves that the deformed physical operator has no upper-half-plane
spectrum for real eta. Since \(p\) is fixed by the deformation, (9) shows

\[
\langle p,(H_\eta(\theta_0)-z)^{-1}p\rangle=r_\eta(z)
\quad(\operatorname{Im}z>0).
\tag{10}
\]

The outgoing sheet used below is precisely the continuation supplied by
(5), (6), and (10), across a real interval about \(E\). This is continuation
of the full response. It is not an inference from Hölder boundary values.

## Certified separation from thresholds and harmonic point spectrum

The only input pair facts used from the supplied construction are the
complete one-body measures, the unique even pair root between \(2E_+\) and
\(2E_-\), and its normalized vector. They also follow from (9) at
eta zero. A small interval certificate supplies the extra strict
separations needed here.

For \(a_c=3-c\), the physical one-body atom is exactly

\[
E_c=c+
\frac{a_c(1-2k)-\operatorname{sgn}(a_c)\,2k\sqrt{3+4k}}
     {1-4k}.
\tag{11}
\]

The complete memory measure is the atom of mass
\(w_c=[1+k r_c'(E_c)]^{-1}\) plus the density

\[
\varrho_c(x)=
\frac{2k\sqrt{1-(x-c)^2}}
 {\pi\{[3-c-(1-2k)(x-c)]^2+4k^2[1-(x-c)^2]\}}
\quad(c-1<x<c+1).
\tag{12}
\]

Let \(m_c(z)=[3-z-k r_c(z)]^{-1}\) and
\(L_c(e)=\int m_c(e-x)d\mu_c(x)\). The executed
`certify_separation.py` uses exact rational interval operations, rational
integer-square-root enclosures, Machin's alternating-series enclosure for
pi, and 1024 interval cells per band. Its outward rational bounds imply

\[
\begin{array}{c|c}
e&L_+(e)+L_-(e)\\\hline
5.9785&(-0.038633,-0.038463)\\
5.97865&(0.034266,0.034436)
\end{array}
\]

Each band is integrated as \(\int_{-1}^1
\varrho_c(c+u)m_c(e-c-u)du\), with the atom included separately. No
floating-point quadrature is used for these signs. Strict monotonicity of
the root function between its two double-bound poles gives

\[
\boxed{5.9785<E<5.97865<6,}
\qquad
5.97931529997724990766<E_++E_-
<5.97931529997724990767.
\tag{13}
\]

In particular the bound-atom sum is strictly separated from \(E\), by more
than \(0.00066529\). The individual atom enclosures are in
`separation_certificate.json`.

For completeness there are no extra one-body eigenvalues revealed by this
deformation at eta zero. Outside \(\Gamma_c\), the scalar Schur equation
\(3-z-k r_c^\theta(z)=0\), after squaring, has just the two possible values
\(z=c+d\) with

\[
(1-4k)d^2-2a_c(1-2k)d+a_c^2+4k^2=0.
\tag{14}
\]

Both candidates are real and outside the physical bath band for our two
parameters. The branch on that real exterior is unchanged by deformation.
Only (11) obeys the unsquared equation; the other candidate has the wrong
square-root sign. The bath Schur formula thus gives

\[
\sigma(h_\sigma(\theta_0))=\Gamma_\sigma\cup\{E_\sigma\}.
\tag{15}
\]

The free two-body spectrum is contained in the compact sumset

\[
\mathcal S=
(\Gamma_+\cup\Gamma_-\cup\{E_+,E_-\})
+(\Gamma_+\cup\Gamma_-\cup\{E_+,E_-\}).
\tag{16}
\]

A sum of two arc points is real only when both are endpoints; its possible
real values are \(0,2,4,6,8,10,12\). A bound-plus-arc point is real only at
an arc endpoint, giving \(E_\sigma+0, E_\sigma+2,E_\sigma+4,E_\sigma+6\),
all separated from (13). The three bound-bound sums are separated from \(E\)
by (13) and \(2E_+<E<2E_-\). It follows that

\[
d_A:=\operatorname{dist}(E,\mathcal S)>0.
\tag{17}
\]

This supplies an actual local analytic domain for the free deformed
resolvent: any disk \(D(E,r_A)\) with \(0<r_A<d_A\). The fact that the
pair energy is close to 6 does not prevent the argument; the strict
separation (13) is essential.

## Simplicity of the deformed physical eigenvalue

At eta zero use the forbidden parity basis

\[
q_e=(|LL\rangle+|RR\rangle)/\sqrt2
=(q_++q_-)/\sqrt2,
\quad q_o=(|LL\rangle-|RR\rangle)/\sqrt2=|e_+e_-\rangle,
\]

where \(q_\sigma=|e_\sigma e_\sigma\rangle\) has unit norm. Then (8) is
diagonal:

\[
K_0^{\theta_0}(z)=
\begin{pmatrix}(L_+(z)+L_-(z))/2&0\\0&M_{\rm out}(z)\end{pmatrix}.
\tag{18}
\]

The first entry is the unchanged even-sector gap resolvent. At \(E\) it
has a simple zero with derivative \(D/2>0\), where

\[
D=L_+'(E)+L_-'(E).
\]

The second entry continues
\(M(z)=\iint (x+y-z)^{-1}d\mu_+(x)d\mu_-(y)\) from above. At \(E\), only
the opposite-band continuum is on shell, and

\[
\operatorname{Im}M_{\rm out}(E)
=\pi\int_4^E\varrho_+(x)\varrho_-(E-x)dx>0.
\tag{19}
\]

The atom is off shell by (13), so this entry is finite and nonzero. From
(9), (18), and \(E\in\rho(A_0(\theta_0))\), the full deformed physical
operator has a simple, algebraically multiplicity-one eigenvalue at \(E\).
In detail \(w=(A_0(\theta_0)-E)^{-1}q_e\) is physical because
\(Pw=0\), and the only singular term of (9) is

\[
-\frac{w\,w^T}{(D/2)(z-E)}.
\]

Here transpose means the bilinear pairing obtained from the original real
coordinates; complex-conjugating the deformed right vector would be
incorrect. The normalized analytic right vector is

\[
\psi_\theta=\sqrt{2/D}(A_0(\theta)-E)^{-1}q_e,
\qquad \psi_\theta^T\psi_\theta=1.
\tag{20}
\]

Thus the Riesz projection is \(\psi_\theta\psi_\theta^T\). Its bare-pair
matrix element is independent of theta and equals

\[
Z_0=\langle p,P_0p\rangle
=\frac{2L_+(E)^2}{D}>0.
\tag{21}
\]

This proves both simplicity and visibility, without presuming that a
positive golden-rule expression already implies a resonance.

## Local eta domain, perturbation theorem and remainder

Choose \(r<d_A/2\) small enough that the closed circle
\(\mathcal C=\{z:|z-E|=r\}\) surrounds only the simple zero in (18), and
that \(M_{\rm out}\) has no zero on the closed disk. Such an \(r\) exists
by (18), (19), and analyticity. Define the finite constants

\[
M_H=\max_{z\in\mathcal C}
\|(H_0(\theta_0)-z)^{-1}\|,
\quad
M_A=\max_{|z-E|\le r}\|(A_0(\theta_0)-z)^{-1}\|.
\]

For a concrete positive, though not numerically evaluated, choice take

\[
a=\min\left\{\frac1{2M_H},\frac{Z_0}{4rM_H^2},
                    \frac1{4M_A}\right\}.
\tag{22}
\]

The first bound makes the physical resolvent Neumann series converge on
\(\mathcal C\) for \(|\eta|<a\). The third keeps the harmonic resolvent
invertible on the disk, since \(\|d\Gamma_2(t)\|\le2\), so (8), (9) are
also valid there at nonzero eta. The second bound ensures the pole remains
visible in \(p\): the resolvent identity and contour integration give

\[
\|P_\eta-P_0\|
\le \frac{r|\eta|M_H^2}{1-|\eta|M_H}
\le2r|\eta|M_H^2<Z_0/2.
\tag{23}
\]

The only perturbation result used is the following elementary bounded
analytic-family fact. A bounded holomorphic family on a fixed Hilbert
space, with an isolated eigenvalue of finite algebraic multiplicity one at
zero, has a holomorphic rank-one Riesz projection and a holomorphic simple
eigenvalue while its fixed isolating resolvent contour persists. Here it
follows by integrating the uniformly convergent resolvent Neumann series;
the rank is locally constant and remains one throughout the eta disk.
The eigenvalue is \(\operatorname{Tr}(H_\eta(\theta_0)P_\eta)\).
These are all its hypotheses, checked above. No resonance or decay theorem
is imported.

Rail parity satisfies
\(S H_\eta(\theta_0)S=H_{-\eta}(\theta_0)\). Uniqueness of the enclosed
eigenvalue gives \(\mathcal E(-\eta)=\mathcal E(\eta)\).
Its Taylor series is therefore even. As \(|\mathcal E(\eta)-E|<r\) for
\(|\eta|<a\), Cauchy's coefficient bounds give, for \(|\eta|\le a/2\),

\[
\left|\mathcal E(\eta)-E-\mathcal E_2\eta^2\right|
\le\frac{4r}{3a^4}|\eta|^4.
\tag{24}
\]

This is an actual remainder bound with finite, defined constants. It is a
qualitative small-eta theorem: no numerical usable eta radius is claimed.
The continued response has the local form

\[
r_\eta^{\rm out}(z)
=-\frac{Z_\eta}{z-\mathcal E(\eta)}+h_\eta(z),
\qquad Z_\eta=\langle p,P_\eta p\rangle\ne0,
\tag{25}
\]

where \(h_\eta\) is holomorphic in the disk. This specifies the local
analytic domain and the visible pole on the outgoing sheet.

## Identification and sign of the second-order coefficient

Differentiate the eigenvalue equation, using the normalized right vector
(20) and its bilinear left functional. Parity gives
\(\mathcal E_1=0\), and \(V\psi_\theta\) lies in the odd subspace. The odd
operator is invertible at \(E\) by (18), (19). Thus

\[
\mathcal E_2
=-\psi_\theta^T V
 (H_{0,\rm odd}(\theta_0)-E)^{-1}V\psi_\theta.
\tag{26}
\]

The minus sign follows from solving
\((H_0-E)\psi_1=-V\psi_0\); it is specific to the stated resolvent
convention. For real theta (26)'s scalar is the corresponding physical
source response. Its complex-theta expression is holomorphic and continues
the physical upper-half-plane response, by the same contour/identity
argument used in (10). Hence it equals \(B_{\rm out}(E)\) in (2).

To make this identification explicit, retain the complete endpoint
measures, including their atoms, and set

\[
C=\sqrt{2/D},\quad
u(x,y)=m_+(E-x)+m_-(E-y),
\]

\[
M(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
J(z)=\iint\frac{u(x,y)d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
F(z)=\iint\frac{u(x,y)^2d\mu_+(x)d\mu_-(y)}{x+y-z}.
\]

The actual source is \(V\psi=Cu\) in the mixed-parity spectral
representation. This follows by applying the one-body memory exchange to
both particles in \((\phi_++\phi_-)/\sqrt D\); the bosonic factor is
\(\sqrt2\), and its forbidden overlap is
\(C[L_+(E)+L_-(E)]=0\). The complete odd hard-core response is exactly

\[
B(z)=\frac2D\left(F(z)-\frac{J(z)^2}{M(z)}\right).
\tag{27}
\]

All of (27) has a holomorphic continuation near \(E\), supplied by the
bounded deformed odd resolvent. We do not deduce holomorphic continuation
from boundary regularity alone.

Writing \(\alpha=J(E+i0)/M(E+i0)\), the scalar boundary formula gives

\[
\operatorname{Im}B_{\rm out}(E)=\pi\rho_g(E),
\]

\[
\rho_g(E)=\frac2D\int_4^E
\varrho_+(x)\varrho_-(E-x)
\left|m_+(E-x)+m_-(x)-\alpha\right|^2dx.
\tag{28}
\]

This can also be checked before taking a boundary value through the
identity

\[
\operatorname{Im}\left(F-\frac{J^2}{M}\right)
=\iint\frac{\epsilon\,|u-J/M|^2}
                  {(x+y-E)^2+\epsilon^2}d\mu_+(x)d\mu_-(y).
\]

The supplied spectral-response proof establishes finiteness and strict
positivity of (28). Its load-bearing positivity step can be verified
without any decimal: on the open shell the two densities are positive,
and \(U(x)=m_+(E-x)+m_-(x)\) is real analytic on
\(x>\max(E-E_+,E_-)\). It is nonconstant, since at large \(x\)

\[
U(x)=\frac{E-6}{x^2}+O(x^{-3}),
\]

and (13) proves \(E\ne6\). A scalar alpha cannot make its squared
variation vanish on the open shell. Therefore (28) is strictly positive.
The complete measures and smooth off-shell denominators also give the
needed scalar boundary regularity. Substitution into (26) proves (1)--(3).

## Computation, scope and remaining work

`certify_separation.py` and `separation_certificate.json` are part of the
proof: their exact rational enclosures establish the strict separation (13).
The initial run completed its mathematical assertions but failed while
serializing enormous exact fractions under Python's integer-string safety
limit; output is now rounded outward to rational denominators \(10^{20}\),
and the corrected script was rerun successfully. No asserted sign uses a
rounded float.

`contour_poles.py` is an additional, uncertified numerical check of the new
construction. It discretizes the deformed momentum integrals, diagonalizes
the full one-body \(h_\eta(\theta)\), and then imposes both forbidden
memory-double constraints on the harmonic two-body resolvent. The full eta
dependence is retained. At \(N=100,t=0.2\) and \(N=160,t=0.1,0.3\), the
computed pole at \(\eta=0.02\) is approximately

\[
5.97857648336624-2.675\times10^{-11}i.
\]

The ratios \(-\operatorname{Im}\mathcal E/\eta^2\) are close to
\(6.68376\times10^{-8}\), with finite-eta corrections and double-precision
noise visible in the saved output. At eta zero the spurious numerical
imaginary part is around \(10^{-15}\), demonstrating the precision floor.
These outputs neither establish the infinite-system theorem nor certify
particular finite-eta widths; the analytic argument above does that at its
stated qualitative scope.

The primary requested mathematical endpoint is established here. There is
no remaining analytic-continuation, pole-existence, or coefficient-sign
obligation within this proof. A useful next quantitative task is to bound
\(r,M_H,M_A,Z_0\) explicitly, producing a certified numerical eta radius and
an effective fourth-order remainder constant. Auditing this proof is also
separate work; no independent audit is claimed. An all-times survival law,
preparation errors, physical disorder, and hardware realization remain
separate questions.
