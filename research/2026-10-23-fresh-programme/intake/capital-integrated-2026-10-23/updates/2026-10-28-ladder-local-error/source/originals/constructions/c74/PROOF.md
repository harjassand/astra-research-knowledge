# Local continuation of the detuned hard-core pair

## Statement and scope

All operators below are the exact semi-infinite ladder in the supplied
packet, in its two-excitation sector, at the fixed coupling (g=1/5).
Write (H_eta=H_g+eta V), (V=n_L-n_R), and let (E,psi) be the
normalized even hard-core pair in the supplied construction. Put

\[
 s(z)=\langle V\psi,(H_{g,\mathrm{odd}}-z)^{-1}V\psi\rangle,
 \qquad \operatorname{Im}z>0.
\]

The following is a local mathematical resonance theorem for this actual
perturbation. It does not require (V) to have finite rank on the
two-particle space.

**Theorem.** There are (r>0), (epsilon>0), and a continuation from the
upper half-plane of both

\[
 G_p(\eta,z)=\langle LR,(H_\eta-z)^{-1}LR\rangle,
 \qquad
 G_\psi(\eta,z)=\langle\psi,(H_\eta-z)^{-1}\psi\rangle
\]

to meromorphic functions on (D(E,r)), for real (|\eta|<\epsilon).
They have the same unique simple pole (lambda(\eta)) there, and their
residues in the convention (a(\eta)/(\lambda(\eta)-z)) are nonzero.
The pole and its projection are holomorphic in complex (eta) near zero,
and the pole is even:

\[
 \boxed{\lambda(\eta)=E-s(E+i0)\eta^2+O(\eta^4).} \tag{1}
\]

In particular, for real (eta), the density proved in the supplied
`S62/PROOF.md` gives

\[
 \boxed{\operatorname{Im}\lambda(\eta)
       =-\pi\rho_g(E)\eta^2+O(\eta^4),\qquad \rho_g(E)>0.} \tag{2}
\]

Thus the pole is strictly in the lower half-plane for all sufficiently
small nonzero real detunings. The constants (r,epsilon) are specified
constructively by resolvent conditions in §7; no useful numerical lower
bound for (epsilon) is asserted. The displayed density decimal remains
uncertified. This theorem is neither an all-times exponential survival law
nor a hardware lifetime or gate-error estimate.

The proof uses explicit bounded operators, contour integration and a
Neumann/Riesz-projection argument. It does not import an unverified
many-body resonance theorem. The spectral-measure/source identities and
strict positivity argument from the named frozen proof are inputs; the
new analytic continuation and perturbation steps are proved below.

## 1. Exact harmonic realization and the hard-core projection

Use the one-particle real Hilbert basis in which the two memory states are

\[
 e_\pm=(L\pm R)/\sqrt2.
\]

The sine transform of each half-line bath identifies its Hilbert space
with (L^2(0,\pi;dk)), the bath Hamiltonian with multiplication by

\[
 \omega_c(k)=c-\cos k,
\]

and its endpoint with (v_0(k)=\sqrt{2/\pi}\sin k). Therefore

\[
 h_0=h_+\oplus h_-,\qquad
 h_\sigma=
 \begin{pmatrix}
 3 & \sqrt{\kappa_\sigma}\langle v_0,\cdot\rangle\\
 \sqrt{\kappa_\sigma}v_0 & M_{\omega_{c_\sigma}}
 \end{pmatrix},
\quad
 (c_+,\kappa_+)=(5,2/25),\quad
 (c_-,\kappa_-)=(1,1/25).
\]

Here and below an integral with real (v_0) has the same value as its
transpose bilinear form. The one-body detuning is

\[
 v=|e_+\rangle\langle e_-|+|e_-\rangle\langle e_+|,
 \qquad h_\eta=h_0+\eta v.
\]

In the harmonic two-boson space (mathscr K=\operatorname{Sym}^2\mathfrak h),
put (A_\eta=d\Gamma(h_\eta)). Let (W:\mathbb C^2\to\mathscr K) have
columns the normalized forbidden states (LL,RR), and set

\[
 P=1-WW^*,\quad \mathscr H=P\mathscr K,\quad
 H_\eta=PA_\eta P|_{\mathscr H}.
\]

This is exactly the physical hard-core Hamiltonian. The subspace

\[
 \operatorname{ran}W=\operatorname{span}\{LL,RR\}
\]

is invariant under (d\Gamma(v)=n_L-n_R), so (P) commutes with that
operator. Consequently (H_\eta=H_0+\eta V) exactly, and

\[
 \|V\|_{\mathscr H}=1.
\]

This bounded operator still has infinite rank: it acts when one excitation
is in a memory and the other is arbitrarily far along a bath.

For complex operators use the continuous bilinear form

\[
 B(f,g)=\sum f_jg_j+\sum_{\sigma=\pm}\int_0^\pi f_\sigma(k)g_\sigma(k)\,dk
\]

and its two-particle counterpart. All transposes below refer to this form.
For real physical test vectors it equals the usual bra applied to a
complex resolvent vector. It is essential to use a transpose, rather than
a complex conjugation depending antiholomorphically on the deformation.

## 2. A bounded analytic bath deformation

For (|t|<1), set

\[
 \phi_t(k)=k+t\sin k,\qquad
 \omega_{c,t}(k)=c-\cos\phi_t(k),\qquad
 v_t(k)=\sqrt{2/\pi}\sin\phi_t(k)\sqrt{1+t\cos k}. \tag{3}
\]

The square root in (3) is the branch equal to one at (t=0).
It is single valued for (|t|<1). Replace (M_{\omega_c},v_0) in the
one-body matrices by (M_{\omega_{c,t}},v_t), placing (v_t^T) in the
upper-right entry. Keep the memory block (3I+\eta v) unchanged. This
defines (h_{\eta,t}), and then

\[
 A_{\eta,t}=d\Gamma(h_{\eta,t}),\qquad
 H_{\eta,t}=PA_{\eta,t}P|_{\mathscr H}. \tag{4}
\]

These are bounded holomorphic operator families on a common Hilbert space
for (|t|<1), with

\[
 H_{\eta,t}=H_{0,t}+\eta V. \tag{5}
\]

Indeed (omega_{c,t}) is holomorphic in (L^\infty), (v_t) is
holomorphic in (L^2), and the off-diagonal operators are finite rank.
No complex composition operator on arbitrary (L^2) vectors is assumed.

For **real** (|t|<1), (phi_t) is an increasing diffeomorphism of

\[
 [0,\pi]\longrightarrow[0,\pi],
\]

and

\[
 (U_tf)(k)=\sqrt{\phi_t'(k)}f(\phi_t(k))
\]

is unitary. Extend it by the identity on the memories. Then

\[
 h_{\eta,t}=U_th_\eta U_t^{-1},\qquad
 H_{\eta,t}=U_t^{(2)}H_\eta(U_t^{(2)})^{-1}. \tag{6}
\]

Both (P) and (V) commute with the corresponding real changes of
variables. Also (U_t^{(2)}p=p) for (p=LR). Thus (4) deforms the full
microscopic detuned problem, including both hard-core constraints.

Fix, for example, (t=-i\theta) with (	heta=1/4). Its bath arcs are

\[
 \Gamma_{c,\theta}
 =\{c-\cos(k-i\theta\sin k):0\le k\le\pi\}.
\]

For (0<k<\pi),

\[
 \operatorname{Im}\omega_{c,-i\theta}(k)
 =-\sin k\sinh(\theta\sin k)<0. \tag{7}
\]

The endpoints remain (c-1,c+1). These are simple arcs: writing

\[
 x(k)=c-\cos k\cosh(\theta\sin k),
\]

one has

\[
 x'(k)=\sin k\cosh(\theta\sin k)
       -\theta\cos^2k\sinh(\theta\sin k)>0
\]

for (0<\theta<1), since (	anh a\le a). Hence their real parts
range monotonically over the original bands.

## 3. One-body spectra and the threshold at six

Outside (Gamma_{c,\theta}), the one-body Schur denominator is

\[
 d_{c,\kappa,\theta}(z)=3-z-\kappa r_{c,\theta}(z),
\quad
 r_{c,\theta}(z)=\frac2\pi\int_0^\pi
 \frac{\sin^2\phi_{-i\theta}(k)\phi'_{-i\theta}(k)}
 {c-\cos\phi_{-i\theta}(k)-z}\,dk. \tag{8}
\]

Deforming the (k) contour shows that (r_{c,\theta}(z)=r_c(z)) in
the upper half-plane and on the real line outside the original band,
where

\[
 r_c(z)=2\{c-z+\sqrt{(z-c)^2-1}\}
\]

uses the branch asymptotic to (z-c). The complement of the simple arc
is connected; analytic continuation of the identity from the upper
half-plane gives

\[
 r_{c,\theta}^2+4(z-c)r_{c,\theta}+4=0. \tag{9}
\]

Any zero of (8) must therefore be a root of

\[
 (3-z)^2+4\kappa(z-c)(3-z)+4\kappa^2=0. \tag{10}
\]

For the two specified channels the polynomials, up to positive factors,
are

\[
 425z^2-2150z+2641,\qquad
 525z^2-3350z+5329.
\]

All their roots are real and outside the original bands. Checking the
original branch in (8) discards one root in each case. The surviving
simple eigenvalues are

\[
 E_+=\frac{43}{17}+\frac{4\sqrt{83}}{85},\qquad
 E_-=\frac{67}{21}-\frac{2\sqrt{79}}{105}. \tag{11}
\]

Thus, for every (0\le\theta<1),

\[
 \sigma(h_{\sigma,-i\theta})
 \subseteq\Gamma_{c_\sigma,\theta}\cup\{E_\sigma\}. \tag{12}
\]

Only this inclusion is needed. It follows directly by the one-body Schur
inverse, without an assumption about completeness of nonnormal
eigenfunctions.

There is a nearby mixed-band endpoint sum at (6), so we now exclude

\[
 E=6
\]

analytically. For a generic upper bath (b) with spectrum ([4,6]) and
memory coupling (sqrt\kappa), split the two-boson space into two
memories, one memory plus one bath boson, and two bath bosons. At energy
6 its matrix is

\[
 A_+(\kappa)-6=
 \begin{pmatrix}
 0&\sqrt{2\kappa}\langle0|&0\\
 \sqrt{2\kappa}|0\rangle&T&\sqrt\kappa W_b^*\\
 0&\sqrt\kappa W_b&C
 \end{pmatrix},
\quad T=b-3\ge1,
\quad C=d\Gamma(b)-6\ge2,
\quad\|W_b\|\le\sqrt2. \tag{13}
\]

Consequently (D_b=W_b^*C^{-1}W_b\ge0), (|D_b|\le1), and

\[
 L_+(6;\kappa)
 =-\frac1{2\kappa\,s_b(\kappa)},\qquad
 s_b(\kappa)=\langle0,(T-\kappa D_b)^{-1}0\rangle>0. \tag{14}
\]

For (0<\kappa<1), (s_b) is nondecreasing, so

\[
 \kappa s_b(\kappa)
\]

is strictly increasing and (L_+(6;\kappa)) is strictly increasing.
Spectral reflection of the bath and a real sign change at the memory
give (L_-(6;\kappa)=-L_+(6;\kappa)) when their couplings agree. At
the actual unequal couplings this implies

\[
 L_+(6;2/25)+L_-(6;1/25)
 =L_+(6;2/25)-L_+(6;1/25)>0. \tag{15}
\]

The supplied pair root is the strictly increasing zero of (L_++L_-)
between (2E_+) and (2E_-). Since (2E_+<6<2E_-), (15) proves

\[
 \boxed{2E_+<E<6.} \tag{16}
\]

This excludes every real mixed-band endpoint sum (4,6,8). It also
places (E) away from all atom-plus-band endpoints: those relevant near
this energy lie below (E_-+2<5.1) or above (E_++4>6.8).

## 4. The unperturbed deformed hard-core eigenvalue is isolated

An elementary tensor-sum resolvent contour gives, for bounded (B,C),

\[
 \sigma(B\otimes1+1\otimes C)\subseteq\sigma(B)+\sigma(C).
\]

To see the needed exclusion, if (z\notin\sigma(B)+\sigma(C)), choose
a contour enclosing (sigma(B)) and excluding (z-\sigma(C)), and
integrate the product of the two resolvents. Multiplication by the tensor
sum minus (z) gives the identity by Cauchy's formula. The same
inclusion holds on a symmetric tensor sector because its projection
commutes with this inverse.

At (eta=0) split the harmonic two-particle space into

\[
 A_{e,\theta}=d\Gamma(h_{+,-i\theta})|_{2+}
                  \oplus d\Gamma(h_{-,-i\theta})|_{2-},
 \qquad
 A_{o,\theta}=h_{+,-i\theta}\otimes1+1\otimes h_{-,-i\theta}.
\]

Each spectral sum involving a bath arc lies in the lower half-plane
except when every bath momentum is an endpoint. Equations (11), (16)
and the endpoint bounds therefore exclude (E) from all these sums.
The only possible harmonic spectral points at real (E) are the isolated
atom sums (2E_+,2E_-), and (a=E_++E_-). The first two differ from

\[
 E
\]

strictly. The third is treated without assuming a numerical separation.

The forbidden vectors in the parity sectors are

\[
 q_e=(q_++q_-)/\sqrt2,\quad q_\sigma=|e_\sigma e_\sigma\rangle,
 \qquad q_o=|e_+e_-\rangle.
\]

For a bounded symmetric operator (A), a normalized real forbidden
vector (q), and (Q=1-|q\rangle\langle q|), the exact compression
identity is

\[
 (QAQ-z)^{-1}_{q^\perp}
 =Q\left[R(z)-R(z)q\,m(z)^{-1}q^TR(z)\right]Q,
\quad R(z)=(A-z)^{-1},\quad m(z)=q^TR(z)q, \tag{17}
\]

when (z\in\rho(A)) and (m(z)\ne0). It follows by solving

\[
 (A-z)w=f+\alpha q,\qquad q^Tw=0.
\]

### Even sector

Here (E\in\rho(A_{e,\theta})). Matrix elements at memory vectors are
unchanged by contour deformation at energies in the even gap. Therefore

\[
 m_{e,\theta}(E)=\tfrac12(L_+(E)+L_-(E))=0,
 \qquad m'_{e,\theta}(E)=D/2>0,
 \quad D=L_+'(E)+L_-'(E). \tag{18}
\]

These equalities also follow by analytic continuation in (t) along

\[
 t=-is,\quad 0\le s\le\theta,
\]

because the harmonic even operator has no spectrum at (E) along that
path. Formula (17) then gives a simple rank-one pole, so the deformed
even hard-core eigenvalue (E) is algebraically simple. An eigenvector
with transpose norm one is

\[
 \psi_\theta
 =\frac{(A_{+,\theta}-E)^{-1}q_+
        +(A_{-,\theta}-E)^{-1}q_-}{\sqrt D},
 \qquad B(\psi_\theta,\psi_\theta)=1. \tag{19}
\]

At real deformation parameters it is (U_t^{(2)}\psi); it extends
holomorphically along the stated path.

### Odd sector, including a possible coincident atom sum

First suppose (E\ne a=E_++E_-). Then (E\in\rho(A_{o,\theta})), and

\[
 M_\theta(z)=q_o^T(A_{o,\theta}-z)^{-1}q_o
\]

agrees in the upper half-plane with the physical complete-measure
Stieltjes transform

\[
 M(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z}.
\]

The physical boundary formula at (E), and holomorphy of the deformed
resolvent there, give

\[
 \operatorname{Im}M_\theta(E)
 =\pi\int_4^E\varrho_+(x)\varrho_-(E-x)\,dx>0. \tag{20}
\]

No atom-band term is on shell. The interval has positive length, and
both band densities are strictly positive in its interior. Hence

\[
 M_\theta(E)\ne0,
\]

and (17) shows that (E) is in the odd hard-core resolvent set.

If (E=a), the harmonic odd resolvent has a simple rank-one pole

\[
 R(z)=\frac{\Pi}{a-z}+R_0(z),\qquad
 M_\theta(z)=\frac{b}{a-z}+m_0(z),\qquad
 b=q_o^T\Pi q_o=w_+w_->0. \tag{21}
\]

Since (Pi) has rank one and is symmetric,

\[
 \Pi q_o q_o^T\Pi/b=\Pi.
\]

Substitution in (17) cancels the entire pole. The inverse of

\[
 b+(a-z)m_0(z)
\]

is holomorphic near (a), so the compressed resolvent has a removable
singularity. The continued inverse still satisfies both resolvent
identities at (a), and (a\in\rho(H_{o,\theta})).

We have therefore proved in both cases that (E) is an isolated,
algebraically simple eigenvalue of the **full** (H_{0,-i\theta}), and
its odd block has a bounded inverse at (E).

## 5. What is analytically continued

Let (R_{\eta,\theta}(z)=(H_{\eta,-i\theta}-z)^{-1}). The continued
memory compression is

\[
 G_p^\mathrm{out}(\eta,z)=B(p,R_{\eta,\theta}(z)p). \tag{22}
\]

The continued unperturbed-pair response is

\[
 G_\psi^\mathrm{out}(\eta,z)
   =B(\psi_\theta,R_{\eta,\theta}(z)\psi_\theta). \tag{23}
\]

The superscript means the following sheet, rather than an assumed
scalar-density extension: start with the physical upper-half-plane
resolvent, keep both momentum endpoints fixed, and lower the two
momentum contours by (k\mapsto k-i\theta\sin k). Equations (22) and
(23) then continue that germ locally through the interior energy (E).

Here is an explicit matching argument valid for the actual detuning.
At (eta=0), (H_{0,-is}) has no spectrum in the upper half-plane for
any (0\le s\le\theta). Its harmonic spectrum there is empty, and
each hard-core scalar compression denominator agrees with a physical
Herglotz function there, whose imaginary part is strictly positive.
Choose a point (z_*=E+ir/2), where (r) is as in §7. The compact path

\[
 s\longmapsto H_{0,-is}
\]

has uniformly bounded resolvent at (z_*). For sufficiently small
complex (eta), the Neumann series preserves that resolvent along the
whole path and on an open neighborhood of (z_*). For real (t),
unitary equivalence (6) equates the physical and deformed matrix
elements; the identity theorem in (t), propagated along the path,
equates their holomorphic germs at (t=-i\theta). Thus (22),(23) really
match the actual physical response on a nonempty upper-half-plane open
set. Their meromorphic continuation to (D(E,r)) is established below.

This does **not** assert a bounded continuation of the physical
resolvent on the original unweighted Hilbert space across its continuous
spectrum. It constructs a bounded deformed operator and continuations
of the specified full microscopic matrix elements. No (eta)-dependent
channel or hard-core term has been dropped.

## 6. Exact pole criterion for the actual perturbed compression

For arbitrary (eta) and (z\in\rho(A_{\eta,-i\theta})), define the
two-by-two matrix

\[
 K_\eta(z)=W^T(A_{\eta,-i\theta}-z)^{-1}W. \tag{24}
\]

Then the full allowed-space inverse is exactly

\[
 R_{\eta,\theta}(z)=P\left[R_A(z)
      -R_A(z)W K_\eta(z)^{-1}W^T R_A(z)\right]P. \tag{25}
\]

In the stated harmonic resolvent set,

\[
 \boxed{z\in\sigma(H_{\eta,-i\theta})
 \ \Longleftrightarrow\ \det K_\eta(z)=0.} \tag{26}
\]

For example, if (K_\eta(z)c=0), the nonzero vector

\[
 (A_{\eta,-i\theta}-z)^{-1}Wc
\]

is in the allowed space and is an eigenvector of its compression.
Conversely a compressed eigenvector gives such a kernel vector.
Invertibility equivalence follows from (25), not just this kernel
argument.

One must not use (26) at a pole of the harmonic resolvent. A criterion
without that restriction is invertibility of the bounded augmented
operator

\[
 \boxed{\mathcal B_\eta(z)=
 \begin{pmatrix}
 A_{\eta,-i\theta}-z&W\\
 W^T&0
 \end{pmatrix}.} \tag{27}
\]

It is invertible precisely when (H_{\eta,-i\theta}-z) is invertible.
To verify this directly write (u=v+Wd), (v\in\mathscr H), in the
equations ((A-z)u+Wc=f, W^Tu=d); the first equation projected by

\[
 P
\]

is exactly an equation for (H_{\eta,-i\theta}-z) on (v), and the
remaining equation then determines (c). This also handles the possible
coincident harmonic atom in §4.

For numerical construction, in the forbidden parity basis (q_e,q_o),
whenever (K_{oo}\ne0), (26) is equivalently the exact scalar equation

\[
 K_{ee}(z)-K_{eo}(z)^2/K_{oo}(z)=0. \tag{28}
\]

It is an equation for the **full** one-body detuning followed by the
two-boson hard-core compression. It is not the truncation

\[
 E-z-\eta^2s(z)=0.
\]

The latter supplies only the second-order expansion, whereas (24)–(28)
retain all powers of (eta).

## 7. Local domain and small-detuning existence

Here is a precise, nonnumerical choice of domain. At (	heta=1/4), use
the compact one-body spectral supersets in (12) and their tensor sums.
The even sums avoid (E). The odd sums avoid (E) except possibly for
the isolated atom (a). Work in a disk avoiding all those other sums.
Shrink its radius until

\[
 \left|\frac{m_{e,\theta}(z)}{z-E}-\frac D2\right|<D/4, \tag{29}
\]

and, in the case (a\ne E),

\[
 |M_\theta(z)-M_\theta(E)|<|M_\theta(E)|/2. \tag{30}
\]

If (a=E), replace (30) by

\[
 |(a-z)M_\theta(z)-b|<b/2, \tag{31}
\]

and use the pole-cancelled expression (21). The functions in (29)–(31)
have their removable values inserted at the centers. Existence of a
strictly positive radius follows from (18),(20),(21) and holomorphy.
If necessary shrink once more so these inequalities hold on a closed
disk of radius (2r). It follows that

\[
 \sigma(H_{0,-i\theta})\cap\overline{D(E,2r)}=\{E\},
\]

with algebraic multiplicity one. Set

\[
 M_r=\sup_{|z-E|=r}\|(H_{0,-i\theta}-z)^{-1}\|<\infty.
\]

Since (|V|=1), for

\[
 |\eta|<(2M_r)^{-1} \tag{32}
\]

the contour (|z-E|=r) remains in the resolvent set by a convergent
Neumann series. Its Riesz projection (\Pi_\eta) is holomorphic and
has constant rank one. The operator on that one-dimensional spectral
subspace is multiplication by one holomorphic eigenvalue

\[
 \lambda(\eta)\in D(E,r).
\]

Thus the inverse has exactly one simple pole in the disk. This proves
existence, simplicity and a meromorphic local resolvent without assuming
formal perturbation theory is valid.

To include the matching argument in §5 explicitly, put

\[
 N_* =\sup_{0\le s\le\theta}
 \|(H_{0,-is}-z_*)^{-1}\|<\infty,
 \qquad z_*=E+ir/2,
\]

and also require (|\eta|<(2N_*)^{-1}).

The physical memory overlap is

\[
 Z_p=B(p,\Pi_0p)
 =-\frac{2L_+(E)L_-(E)}{D}>0.
\]

The contour resolvent identity gives

\[
 \|\Pi_\eta-\Pi_0\|\le2r|\eta|M_r^2.
\]

Hence for (|\eta|<Z_p/(4rM_r^2)), the pole coefficient in (22)
satisfies

\[
 |B(p,\Pi_\eta p)-Z_p|<Z_p/2.
\]

It cannot vanish. For (23) the coefficient at zero is one, because

\[
 B(\psi_\theta,\psi_\theta)=1,
\]

and it remains nonzero, for example, if additionally

\[
 |\eta|<\{4rM_r^2\|\psi_\theta\|^2\}^{-1}.
\]

Taking the minimum of these four positive bounds specifies an

\[
 \epsilon>0
\]

for all the asserted domain, pole, matching and visibility properties.
The norm constants are mathematical definitions, not evaluated
experimental tolerances.

## 8. Expansion and the sign of the imaginary coefficient

The rail-exchange involution (S) commutes with the deformation and
hard-core projection, and

\[
 SH_{\eta,-i\theta}S=H_{-\eta,-i\theta}.
\]

Uniqueness of the simple eigenvalue in the fixed disk implies

\[
 \lambda(-\eta)=\lambda(\eta). \tag{33}
\]

Differentiate the eigenvalue equation using the transpose-normalized

\[
 \psi_\theta
\]

from (19). The first derivative vanishes by parity. Because

\[
 f_\theta=V\psi_\theta
\]

is odd, the first eigenvector correction is

\[
 -\,(H_{o,\theta}-E)^{-1}f_\theta.
\]

The coefficient of (eta^2) is therefore exactly

\[
 \lambda_2
 =-B(f_\theta,(H_{o,\theta}-E)^{-1}f_\theta). \tag{34}
\]

The scalar function

\[
 s_\theta(z)=B(f_\theta,(H_{o,\theta}-z)^{-1}f_\theta)
\]

equals the physical (s(z)) for (operatorname{Im}z>0), by the same
real-unitary/analytic-continuation argument as above. Its holomorphy near

\[
 E
\]

was proved in §4, including the possible atom coincidence. Consequently

\[
 s_\theta(E)=\lim_{\delta\downarrow0}s(E+i\delta)=s(E+i0). \tag{35}
\]

The supplied source calculation is for the actual dressed source

\[
 (V\psi)(x,y)=\sqrt{2/D}\,[m_+(E-x)+m_-(E-y)]
\]

in the complete mixed spectral representation. Its exact compression
identity gives

\[
 s(z)=\frac2D\left(F(z)-\frac{J(z)^2}{M(z)}\right), \tag{36}
\]

and its proved positive boundary-density identity is

\[
 \operatorname{Im}s(E+i0)=\pi\rho_g(E)>0. \tag{37}
\]

For clarity, the complete scalar interface in (36) is as follows:

\[
 m_\sigma(z)=(3-z-\kappa_\sigma r_{c_\sigma}(z))^{-1},\qquad
 u(x,y)=m_+(E-x)+m_-(E-y),
\]

\[
 (M,J,F)(z)=\iint\frac{(1,u(x,y),u(x,y)^2)}{x+y-z}
                   \,d\mu_+(x)d\mu_-(y).
\]

All integrals include the single atom and the band in each complete
measure. The band density is

\[
 \varrho_\sigma(x)=\pi^{-1}\operatorname{Im}m_\sigma(x+i0),
\]

strictly positive in its band interior and with square-root vanishing
at its endpoints. With

\[
 \alpha=\lim_{\delta\downarrow0}J(E+i\delta)/M(E+i\delta),
\]

the actual density is

\[
 \rho_g(E)=\frac2D\int_4^E
 \varrho_+(x)\varrho_-(E-x)
 |m_+(E-x)+m_-(x)-\alpha|^2\,dx.
\]

The scalar positivity identity underlying this expression is

\[
 \operatorname{Im}(F-J^2/M)
 =\iint\frac{\delta\,|u-J/M|^2}
 {(x+y-E)^2+\delta^2}\,d\mu_+(x)d\mu_-(y),\qquad z=E+i\delta.
\]

The supplied proof establishes its boundary limit, including the
coincident-atom case. Its strict positivity can also be read particularly
simply after (16): the real function

\[
 U(x)=m_+(E-x)+m_-(x)
\]

is analytic on the connected interval

\[
 x>\max(E-E_+,E_-),
\]

which contains the entire open shell ((4,E)) and extends to infinity.
Its asymptotic expansion is

\[
 U(x)=(E-6)x^{-2}+O(x^{-3}).
\]

Since (E<6), it cannot be constant on the shell: constancy would
extend analytically to infinity and force both that constant and the
nonzero leading coefficient to vanish. No scalar (alpha) can
therefore annul the integrand almost everywhere. This confirms the
strict sign without using its floating-point value.

Equations (34)–(37) prove the sign and coefficient in (1),(2). In
particular the minus sign comes from the eigenvector correction for the
resolvent convention (H-z); it is not inserted by a formal decay
convention.

The remainder is (O(\eta^4)), rather than only (o(\eta^2)), because
the eigenvalue is holomorphic and even. More explicitly, for any

\[
 0<\epsilon_0<\epsilon,
\]

Cauchy's estimate and (|\lambda(\eta)-E|<r) give, for

\[
 |\eta|<\epsilon_0,
\]

\[
 |\lambda(\eta)-E+\eta^2s(E+i0)|
 \le \frac{r(|\eta|/\epsilon_0)^4}
 {1-(|\eta|/\epsilon_0)^2}. \tag{38}
\]

No time-domain conclusion is used in or follows automatically from this
bound.

## 9. Executed contour checks

`contour_check.py` discretizes (3) with Gauss-Legendre quadrature, using
complex symmetric one-body matrices. It computes the exact two-boson
forbidden-state Schur complement **of that quadrature**, including the
one-body memory mixing (eta). It also independently evaluates (36)
on the deformed contour.

At 96–160 nodes per bath and (	heta=0.25,0.4), it obtains

\[
 s_\theta(E)\simeq0.00707837231216
                  +6.6837594\times10^{-8}i,
\]

and (operatorname{Im}s_\theta(E)/\pi\simeq2.1275067\times10^{-8}),
consistent with the frozen response. The actual-detuning Schur roots at

\[
 \eta=.04,.02,.01
\]

have respectively (operatorname{Im}(\lambda-E)/\eta^2) approximately

\[
 -6.6985\times10^{-8},\quad-6.6861\times10^{-8},\quad-6.6844\times10^{-8}.
\]

These finite quadratures are normalization and sign diagnostics, with
floating-point cancellation at the smallest widths. They establish no
interval bounds, existence theorem, or minimum detuning range. The
existence proof is §§1–8.

A separate direct two-boson Fock construction at five quadrature nodes
per bath, (	heta=.25,eta=.07), checks the entire compressed inverse
against (25), with maximum entry discrepancy (5.7\times10^{-12}) at

\[
 z=E+.017i.
\]

It also obtains (|V|=1), exact complex symmetry to the displayed
floating-point precision, and forbidden/allowed overlap below

\[
 2.3\times10^{-17}.
\]

This independently checks the finite-dimensional bosonic factors,
physical detuning, and two-constraint compression used by the contour
implementation.

## 10. What remains

At the mathematical scope asked for, the construction above closes the
local small-(eta) resonance/existence and leading-width target, provided
the supplied exact source-density proof is retained. The main quantities
left unevaluated are a numerical lower bound for the analytic detuning
radius, interval bounds for the density and real shift, and quantitative
control of the transient/nonexponential part of survival. None is a
logical premise of the local theorem.

A useful next construction is a validated estimate of (r,M_r,N_*) from
the explicit arc resolvents and two-by-two Schur matrix, followed by a
controlled time-domain contour deformation if an operational decay law is
desired. That work must retain the endpoint threshold at six and its
nearby branch geometry.
