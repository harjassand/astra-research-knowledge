# The full acoustic-contact face: two LMIs, sharp generators, and quasiconvex completion

Date: 15 October 2026. Authoring lane: moving_kernel_genesis.

**Status.** The rank-one-convexity theorem below has a self-contained analytic
proof and an exact symbolic checker. The inherited N850 and moving-family
certificates were reconstructed against their actual inputs and pass exact
checks. The explicit quasiconvex consequences in Sections 6–7 use the supplied
moving-family analytic theorem. External mathematical review, formal proof
verification, and historical priority remain unresolved. No repository files
were edited. The late sharp-QC certificate and the resulting internally
verified interval theorem are handled separately in Sections 9–9.1.

## 1. Result and exact scope

For a real matrix A=[[a,b],[c,d]], put

\[
 u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad j=ad-bc,
 \qquad H=(u+v-2j)^2.
\]

Consider the four-dimensional vector space

\[
 F_{\alpha,\beta,\gamma,\delta}=\alpha H+\beta u^2+\gamma j^2+\delta uj.
\]

**Theorem A (complete rank-one-convex cone in this space).** With no sign or
interval assumptions on the four real coefficients, F is rank-one convex if
and only if both matrices are positive semidefinite:

\[
 \boxed{P(F)=\begin{pmatrix}6\beta+\delta&\delta\\\delta&\gamma\end{pmatrix}\succeq0,
 \qquad
 Q(F)=\begin{pmatrix}8\alpha&\delta\\\delta&2\beta+\delta\end{pmatrix}\succeq0.}
 \tag{1}
\]

Thus this entire rank-one-convex cone is spectrahedral. In particular, the
optimal alpha threshold on the source acoustic boundary is

\[
 \boxed{\alpha_*(r)=\frac{3r}{8(r+2)}}\qquad(r<-2\ \hbox{or}\ r>0).
 \tag{2}
\]

At r=0 the family is alpha H+j² and the threshold is zero. On -2<=r<0
there is no finite alpha giving rank-one convexity. The sharp uniform alpha
floor over the supplied interval I=[-21/8,-5/2] is 15/8; the pointwise floor
ranges from 63/40 to 15/8.

The four-dimensional space is not an arbitrary convenient subspace: it is
exactly the exposed acoustic-contact face through G in the nine-dimensional
left-SO(2)-invariant rank-one-convex cone. Its extreme rays are completely
classified in Section 5. No claim about the unrestricted quartic cone or
quasiconvexity for all generators follows from Theorem A alone.

## 2. Reconstruction of the inherited decisive certificate

The worktree was read at the required pin
`33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`. The current N850 and N860 dossiers,
the incoming report, and the load-bearing reconstruction and moving-certificate
verifiers were read. Input files were treated as mathematical data.

`verify_inherited.py` parses the actual pinned N850 JSON and checks equality
with every transcribed matrix in incoming `reconstruct.py`: C, S, Q=CSCᵀ,
the 60 two-form coefficients, and the two diffusion coefficients. It then
verifies the full polynomial identity, closedness, primitive, rank 18, all
18 positive LDL pivots, and the scalar rank-two subtraction. Consequently the
incoming reconstruction's former uncertainty about equality with the actual
source matrices is removed for this local pin; this is an algebraic comparison,
not an external correctness endorsement.

The same runner invokes the portable moving-family verifier as a function.
Its universal rational identity, closed form, primitive, subtraction identity,
four Bernstein matrices, 72 positive rational pivots, acoustic identities,
and lifted-minor witness all pass. Receipts are written here, not beside the
source. The two certificate files were hashed before and after and remain
unchanged. The exact input hashes and full returned receipts are in
`INHERITED_EXACT_RECEIPT.json`.

## 3. Two direct necessary tests

Because F is invariant under target rotations, it suffices to test rank-one
directions R=e1 tensor (n,m). Write its acoustic form as

\[
 \mathfrak a_F(A;n,m)=D^2F(A)[R,R].
\]

Introduce defect and conformal coordinates

\[
 p=a-d,\ q=b+c,\ h=a+d,\ k=c-b,
\]

so a=(h+p)/2, d=(h-p)/2, b=(q-k)/2, c=(q+k)/2 and H=(p²+q²)².

For the conformal background p=q=0, choose
h=eta, k=t(eta+zeta), n=t, m=1. Exact differentiation gives

\[
 \mathfrak a_F
 =\frac{t^2}{2}\big[(6\beta+\delta)\eta^2-2\delta\eta\zeta+\gamma\zeta^2\big]
  +\frac{t^4}{2}(2\beta+\delta)(\eta+\zeta)^2.
 \tag{3}
\]

Divide by t² and let t tend to zero. Nonnegativity for every eta,zeta forces
P(F)>=0, after changing the sign of the second coordinate.

For R=e11 and A=[[0,2x-y],[y,0]], the exact finite test is

\[
 \mathfrak a_F=2\big[8\alpha x^2-2\delta xy+(2\beta+\delta)y^2\big].
 \tag{4}
\]

Thus Q(F)>=0 is also necessary. In particular, if 2beta+delta>0,

\[
 \alpha\ge\frac{\delta^2}{8(2\beta+\delta)}.
 \tag{5}
\]

This lower bound is attained by the explicit acoustic test background
A=[[0,4beta+delta],[delta,0]]:

\[
 \mathfrak a_F(A;1,0)
 =2(2\beta+\delta)\big[8\alpha(2\beta+\delta)-\delta^2\big].
 \tag{6}
\]

It supplies a genuine rank-one-convexity obstruction below the alpha floor.
It does not rely on failure of a particular Gram representation.

## 4. Sharp boundary generators and sufficiency

Define

\[
 J_r=\frac{3r}{8(r+2)}H+\frac{r(r-1)}6u^2+j^2+r uj,
 \qquad r<-2\ \hbox{or}\ r>0.
 \tag{7}
\]

First prove that J_r is rank-one convex. For the family with arbitrary alpha
and beta=r(r-1)/6, gamma=1, delta=r, write the acoustic quadratic matrix in
the coordinate order (p,q,h,k) in block form. Its conformal (h,k) block is

\[
 L=\begin{pmatrix}
 n^2(r+1)^2/2&-mn(r+1)/2\\
 -mn(r+1)/2&[3m^2+n^2r(r+2)]/6
 \end{pmatrix},
 \qquad \det L=\frac{n^4r(r+1)^2(r+2)}{12}.
 \tag{8}
\]

For n!=0 and the indicated r branches, L is positive definite. Eliminating
h,k by an exact square completion leaves the Schur complement

\[
 \begin{aligned}
 S_{11}&=12\alpha n^2+4\alpha m^2
 -\frac{r[(5r^2+14r+8)n^2+3m^2]}{2(r+1)^2(r+2)},\\
 S_{22}&=4\alpha n^2+12\alpha m^2-\frac{3rn^2}{2(r+2)},\\
 S_{12}&=8\alpha mn-\frac{3rmn}{2(r+1)(r+2)}.
 \end{aligned}\tag{9}
\]

At alpha=alpha*(r), its quadratic form is the transparent two-square identity

\[
 \boxed{
 (p,q)S(p,q)^T
 =\frac{r}{2(r+2)}
   \left[\frac{2r+1}{r+1}np+3mq\right]^2
 +\frac{3r^2}{2(r+1)^2}m^2p^2.}
 \tag{10}
\]

Both coefficients are positive on both branches. Completing the conformal
square with L proves acoustic nonnegativity for n!=0. Continuity of the
original acoustic polynomial covers n=0. Target rotation invariance then
covers every rank-one direction. The C² Legendre–Hadamard criterion proves
rank-one convexity of J_r.

Now suppose (1) holds. If delta=0, it says alpha,beta,gamma>=0, and F is a
nonnegative combination of the convex H,u² and the polyconvex j².

If delta!=0, both 6beta+delta and 2beta+delta are strictly positive. Set

\[
 \rho=\frac{6\beta+\delta}{\delta},\qquad
 \lambda=\frac{\delta^2}{6\beta+\delta},\qquad
 a_0=\frac{\delta^2}{8(2\beta+\delta)}.
 \tag{11}
\]

For delta<0 one has rho<-2, because rho+2=3(2beta+delta)/delta<0. For
delta>0 one has rho>0. The PSD conditions give lambda>0, gamma-lambda>=0,
alpha-a0>=0, and the universal exact identity is

\[
 \boxed{F=\lambda J_\rho+(\gamma-\lambda)j^2+(\alpha-a_0)H.}
 \tag{12}
\]

All three summands are rank-one convex. This proves sufficiency in Theorem A
for every coefficient case, including all singular PSD cases. Applying (1)
to beta=r(r-1)/6,gamma=1,delta=r proves (2) and the impossible interval:
Q has lower-right entry r(r+2)/3, which is negative for -2<r<0; at r=-2
its nonzero off-diagonal entry prevents positivity.

The operation in (12) is also useful beyond verification: every nonzero
delta case reduces to one sharp boundary generator, rather than an arbitrary
mixture. It exposes exactly which new QC theorem would close a coefficient
sector.

## 5. The exposed face and all its extreme rays

Every left-SO(2)-invariant homogeneous quartic has the independent nine-term
representation

\[
 f_0u^2+f_1v^2+f_2uv+f_3w^2+f_4uw+f_5vw+f_6uj+f_7vj+f_8wj,
\]

using uv=w²+j². On the rank-one-convex cone, the linear functional
ell(F)=D²F(I)[e12,e12] is nonnegative. Its zero set is therefore an exposed
face. At a zero of a nonnegative acoustic form, all first derivatives vanish.
Differentiating in the matrix and rank-one variables gives the exact five
independent linear conditions

\[
 f_1=-f_7/4,\quad f_2+f_3=-f_7/2,\quad f_4=f_5=f_8=0.
 \tag{13}
\]

The resulting four-dimensional nullspace is exactly span{H,u²,j²,uj}.
The checker independently regenerates this rank-five system and proves that
the four displayed generators span its nullspace. Conversely, all members of
this four-dimensional space have ell=0. Theorem A thus describes the whole
exposed face, with no omitted rank-one-convex quartics in that face.

**Theorem B (complete extreme-ray classification in the invariant cone).**
The extreme rays of this face are precisely H, u², j², and J_r for r<-2 or
r>0. They are also extreme rays of the full nine-dimensional left-invariant
rank-one-convex cone.

For J_r, P=[[r²,r],[r,1]] is nonzero of rank one, as is Q. In a PSD
decomposition, every summand of a rank-one PSD matrix is proportional to it.
Hence if J_r=F1+F2 with F_i in the face, P(F_i)=t_iP(J_r) and
Q(F_i)=s_iQ(J_r). Their shared nonzero off-diagonal delta forces s_i=t_i.
Together the two matrix images determine all four coefficients, so
F_i=t_iJ_r. This proves extremality. The same argument using zero and
rank-one images proves extremality of H,u²,j². Identity (12), and the
nonnegative three-ray decomposition at delta=0, exclude all other extreme
rays. An extreme ray of a face is extreme in the containing cone.

This final containing cone is the **nine-dimensional invariant cone**.
Extremality in the unrestricted cone of all quartic polynomials is not proved.

A particularly simple new sharp ray under the source normalization is

\[
 E=45H+35u^2+24j^2-60uj=24J_{-5/2}.
 \tag{14}
\]

The source functional Lambda=64alpha+16beta+4gamma gives Lambda(E)=3536,
so E/3536 is normalized. E(I)=-1, which supplies non-polyconvexity by the
standard lifted-minor witness; rank-one convexity is established above.
The source G is J_{-5/2}+(9/8)H, so its alpha=3 is far above this sharp
rank-one-convex boundary.

## 6. Exact conic completion of the inherited QC interval

This section requires only the already supplied theorem

\[
 F_r^{\rm source}=3H+\frac{r(r-1)}6u^2+j^2+r uj,
 \qquad F_r^{\rm source}-\kappa H\text{ is QC on }I,
 \quad\kappa=3/16000.
\]

Let a=3-kappa. Define C_old to be the conic hull of these certified
F_r^{source}-kappa H, r in I, together with H,u²,j². This is a QC cone by
convexity of H,u² and polyconvexity of j². It is a specified generated QC
cone, not the entire local compatible-heat Gram cone.

For delta=-d<0, set

\[
 m_* =\max\left\{\frac{8d}{21},\frac{d^2}{6\beta-d}\right\}.
 \tag{15}
\]

Then membership in C_old is exactly

\[
 \boxed{\beta\ge\frac{7d}{12},\qquad
 \gamma\ge m_*,\qquad \alpha\ge a m_*.}
 \tag{16}
\]

For delta=0 it is exactly alpha,beta,gamma>=0, and no delta>0 is generated.
In particular, the smallest alpha in this specified cone is the explicit
value a m*. This is an analytic optimum, not an SDP or finite parameter test.

To prove it, let M be the total mass of certified interval generators in any
finite positive mixture. The weighted mean of their r parameters is delta/M.
By the variance inequality,

\[
 \beta\ge\frac{M}{6}\left[(\delta/M)^2-\delta/M\right]
 =\frac{\delta^2}{6M}-\frac\delta6.
\]

The other conditions are M<=gamma, aM<=alpha, and delta/M in I. Conversely,
one generator at the mean delta/M meets the lower beta bound, and the three
basic nonnegative remainders supply every excess. Consequently mixtures
offer no improvement over one interval generator. Eliminating M gives

\[
 \max\{8d/21,d^2/(6\beta-d)\}
 \le\min\{2d/5,\gamma,\alpha/a\},
\]

equivalent to (16). At beta=145/96, gamma=1, delta=-5/2, the optimal mass
is 20/21 and the smallest alpha is 15999/5600, approximately 2.8570.

## 7. A strict-QC, non-polyconvex consequence below the source alpha sector

An explicit simple example, with a positive inherited Jensen constant, is

\[
 F_{\rm new}=\frac{120}{41}H+\frac{95}{64}u^2+j^2-\frac52uj
 =\frac{40}{41}F^{\rm source}_{-41/16}+\frac1{41}j^2.
 \tag{17}
\]

Here alpha=120/41 is strictly below 3-kappa. The determinant-square affine
Jensen gap is nonnegative, so the supplied source theorem yields

\[
 \int[F_{\rm new}(B+D\phi)-F_{\rm new}(B)]
 \ge\frac1{2562500}\int|D\phi|^4
 \tag{18}
\]

with precisely the source's bounded Lipschitz zero-trace, periodic rectangle,
and zero-end-profile strip contracts. Its non-polyconvexity is explicit:
F_new(I)=-1/64 and F_new(diag(1,-1))=135959/2624. Give each of +/-64I
mass 1/[2(1+64²)] and each of +/-diag(1,-1) mass 64²/[2(1+64²)]. Mean A
and mean determinant are zero, whereas the bracket in the lifted Jensen test
is exactly -31977/2624. Hence the lifted mean energy is negative.

This four-atom law is not a compatible gradient law. It establishes
non-polyconvexity and does not contradict (18).

## 8. Primary-source comparison, reproducibility, and open obligations

The bounded comparison is recorded in `PRIMARY_COMPARISON.md`, with direct
primary links and exact reading scope. Bruno–Pasqualotto's double-rotation
theorem does not apply directly: for beta!=0, F(e11)=alpha+beta differs
from F(e12)=alpha, although those matrices differ by a right rotation. Their
boundary-plus-determinant-square strategy is an inherited analogue of (12),
not a new general method claimed here. Calderón's biquadratic SOS theorem
also means that an acoustic SOS is not itself evidence of a new principle.
Neither comparison establishes historical priority for this exact face or
its spectrahedral formulas.

Run from any directory:

```sh
python3 /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-moving-heat-observable-power-v1/workers/moving_kernel_genesis/verify_inherited.py
python3 /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-moving-heat-observable-power-v1/workers/moving_kernel_genesis/verify_face.py
```

The inherited runner checks actual source matrices and all stated portable
certificate identities. The face checker records 33 exact groups,
including both necessary tests, the full contact nullspace, universal Schur
identity, sharp SOS, global decomposition, rank-one boundary images, and
the explicit strict-QC example. No floating-point eigensolver, parameter
sampling, numerical optimizer, or pickle is used. The analytic proof is not
replaced by these checks.

Open obligations after this lane's own results are: review the analytic face
and extremality arguments independently; acquire historical priority beyond
the bounded comparison; determine QC of sharp J_r outside any independently
audited QC interval; determine the feasible local compatible-heat cone when
the source's arbitrary free coefficients are unfrozen. No physical capability
or practical numerical advantage is claimed.

## 9. Late conditional sharp-QC interface (append-only update)

After the preceding independent derivation and exact checks, root reported
that `sharp_boundary_qc` exported an exact sharp-boundary certificate over
I=[-21/8,-5/2], with a 12-dimensional support and six Bernstein matrices.
Root also reported that an independent exact audit was running. This lane
has not yet independently validated that new certificate or its analytic
proof. The following consequence is therefore **conditional on that audit
and the required heat-to-QC implication**; it is not inferred from the report
of a successful run.

If J_r is quasiconvex for every r in I, identity (12) immediately proves:
for delta<0 and rho=(6beta+delta)/delta in I,

\[
 F\text{ is rank-one convex}\quad\Longleftrightarrow\quad
 F\text{ is quasiconvex}\quad\Longleftrightarrow\quad P(F),Q(F)\succeq0.
 \tag{19}
\]

The forward implication uses lambda J_rho plus the nonnegative
determinant-square and H remainders. The reverse implication QC=>ROC is
standard. This would attain the exact alpha floor throughout that coefficient
sector and would establish QC of the explicit normalized extreme ray E/3536.
There is no assertion here that every sharp generator outside I is QC.

### 9.1. Subsequent frozen-certificate replay and analytic reading: PASS

The author subsequently supplied the actual frozen files, not merely a status
message. This lane read `sharp_boundary_qc/REPORT.txt` and the complete portable
verifier, and replayed a byte-identical verifier copy in its own directory on
the author's certificate. The exact universal heat identity, closedness,
global primitive, moving rank-12 support, two acoustic contacts, positive
diffusion on the entire interval, degree-five Bernstein reconstruction, and
all 72 rational pivots pass. Frozen input hashes are

* certificate: `2adcc075976981aab4533fbaf16830e2fd6a99b86e0aa16b7d0fd65226674863`;
* verifier: `e6cee5ed72f5e2c4e11cf2a9d0338d861d1fdaafca6345910b8b5586f5b030bd`.

`LATE_SHARP_REPLAY_RECEIPT.json` records the hashes, exact replay, source
immutability and analytic reading. `SHARP_VERIFICATION.json` is this lane's
local replay receipt, distinct from the author's original receipt. No file
in the author's directory was modified by this replay.

The analytic implication reconstructs as written. For each fixed r, positive
constant anisotropic diffusion evolves a smooth compactly supported
perturbation. The relative quartic energy is integrable; Gaussian decay and
the quartic Taylor bound give its zero limit at infinity. The homogeneous
quadratic closed form has a global polynomial primitive. Pullback and Stokes
remove its integral, because differentiated heat perturbations decay rapidly
while the background is constant. Integration by parts therefore gives a
nonpositive energy derivative. Strong L²,L³,L⁴ continuity at zero and strong
W^(1,4) approximation give QC at every affine background; periodic heat and
Stokes give the periodic version. No uncorrected pointwise heat positivity
or uniform coercive margin is assumed.

**Theorem C (internally verified sharp-QC coefficient sector).** For real
coefficients with delta<0 and

\[
 \rho=\frac{6\beta+\delta}{\delta}\in[-21/8,-5/2],
\]

F is quasiconvex if and only if it is rank-one convex if and only if both
matrices in (1) are PSD. This is valid at every affine background on bounded
planar Lipschitz domains with W0^(1,4) perturbations, and for periodic
perturbations. The proof is exactly (12) with the now checked sharp interval
certificate. In particular, the normalized extreme ray E/3536 is
quasiconvex and non-polyconvex.

Equivalently, writing d=-delta>0, the parameter-strip premise is
7d/12<=beta<=29d/48. The exact floor within this strip is
alpha>=delta²/[8(2beta+delta)], with the independent gamma bound
gamma>=delta²/(6beta+delta). No arbitrary beta or r extension is inferred.
This lane's new reading and replay are internal mathematical evidence;
external correctness, formal verification and priority remain unresolved.

## 10. Independently checked extension: every sharp generator is non-polyconvex

The following support-gap construction was communicated by
`contact_face_priority_audit` after the face theorem was derived. This lane
reconstructed it directly and added four exact checks to `verify_face.py`.
It is credited as a shared internal extension, not independently invented
again here.

For every r<-2 or r>0, J_r is non-polyconvex, even when J_r(I) is positive.
Suppose it had a convex lift in (A,det A). The convex hull of the graph
{(A,det A)} is all of R⁵: the average of A+B and A-B has matrix mean A and
determinant mean det A+det B, and det B ranges over R. A convex lift finite
on that graph is consequently finite on R⁵ and has a supporting affine
functional at (I,1). After differentiating its contact with the smooth J_r,
the support inequality takes the form

\[
 \mathcal G_\ell(A)=J_r(A)-J_r(I)-DJ_r(I):(A-I)
 -\ell[\det A-1-\operatorname{tr}(A-I)]\ge0.
 \tag{20}
\]

Its Hessian at I must be PSD. The e12 diagonal entry is zero, so its e12 row
must vanish. The e12–e21 cross entry is exactly ell-r-2; hence ell=r+2.
The sole possible gap is therefore

\[
 \mathcal G(A)=J_r(A)-(r+2)j-\frac23r(r+2)a+\frac{(r+2)(r+1)}2.
 \tag{21}
\]

On A=I+t diag(1,-r-1), exact expansion gives

\[
 \boxed{\mathcal G(A)=\frac{t^3(r+2)}{24}
 [(9r^3+36r^2+40r+12)t-8r].}
 \tag{22}
\]

The cubic coefficient is -r(r+2)/3, nonzero on both sharp branches. One sign
of sufficiently small t makes this gap negative, contradicting a supporting
inequality. Thus every J_r is non-polyconvex. This does not settle its QC
status outside the interval currently audited in Section 9.1.

## 11. A no-loss natural diffusion for the sharp negative branch

An additional exact symmetry, independently checked here, is

\[
 B_r=\begin{pmatrix}0&2r+1\\3&0\end{pmatrix},\qquad
 J_r(AB_r)=9(2r+1)^2J_r(A),\qquad B_r^2=3(2r+1)I.
 \tag{23}
\]

For r<-2 put q=-(2r+1)>0 and T=B_r/sqrt(3q). Then T²=-I, det T=1 and
J_r(AT)=J_r(A). This is a discrete elliptic quarter-turn symmetry. It is
not continuous right-rotation invariance.

For the standard compatible-heat/closed-local-two-form/PSD-Gram class,
an invertible spatial coordinate change x=Ty transports any certificate
with input diffusion D to one with diffusion T^(-1) D T^(-T). The polynomial
Gram transforms by an invertible linear congruence, so PSD is preserved;
the correcting form transforms by pullback and a determinant factor, so
closedness is preserved. Here T^(-1)=-T and det T=1. Averaging the original
and transported certificates therefore replaces D=[[a,b],[b,c]] by

\[
 D+TDT^T=\operatorname{diag}\big(a+(q/3)c,\ c+(3/q)a\big).
 \tag{24}
\]

Its ratio is d2/d1=3/q. After positive scalar normalization, the natural
diffusion diag(q,3) is consequently **no loss for existence** of a certificate
in that class. The trace-two normalization is

\[
 d_1=\frac{2r+1}{r-1},\qquad d_2=-\frac3{r-1}.
 \tag{25}
\]

This eliminates diffusion search on each sharp negative ray. It does not
by itself construct a positive Gram certificate, settle a non-SOS mechanism,
or establish QC outside the audited interval. A later author message reports
a candidate universal-negative-branch certificate; it is not incorporated
into Theorem C before its frozen algebra and analytic implication are read.

## 12. Exposure caveat: extreme in the full invariant cone, but not exposed there

The word "exposed" in Sections 1 and 5 refers to the four-dimensional
acoustic-contact face. Each sharp ray is exposed relative to that face.
It is **not exposed in the full nine-dimensional invariant ROC cone**.
The following proof was communicated by `contact_face_priority_audit` and
reconstructed here; the determinant, kernel, and second-zero identities were
added to the exact checker.

Let K denote the full nine-dimensional invariant ROC cone. Normalize the
rank-one acoustic evaluation functionals by |A|=|target|=|input|=1. Their set
T is compact. Every one evaluates the convex quartic |A|⁴ to at least 4,
so the conic hull of T is closed: a convergent conic combination has bounded
total mass when evaluated at that quartic, and the convex hull of T is
compact. The bipolar theorem gives K*=cone(T). Carathéodory's theorem allows
finite positive combinations of acoustic evaluations for every support.

After rotating the target direction to e1, the sharp acoustic determinant
in the original (a,b,c,d) coordinates is 9r⁴n⁴m⁴. For n,m both nonzero it
has no nonzero background zero. At n=0 its kernel is span{I}; at m=0 it is
span{A_r}, where A_r=[[0,(2r+1)/3],[1,0]]. The positivity and kernel
statements follow also from the Schur square completion. The determinant
square's acoustic value is 2(dn-cm)², zero at both families. Consequently,
every acoustic evaluation vanishing on J_r also vanishes on j². Every
supporting functional of K vanishing on J_r therefore vanishes on j², so
it cannot expose J_r alone.

In fact its minimal exposed face in K is exactly cone{J_r,j²}. The sum of
the two nonnegative acoustic evaluations at (I,e12) and (A_r,e11) exposes
that face. The first zero forces membership in the four-dimensional contact
space. The second is (2/9)zᵀQ(F)z=0 for z=(r+2,-3). PSD forces Q(F)z=0,
which gives alpha=3delta/[8(r+2)] and beta=(r-1)delta/6. Then P(F)>=0
is exactly delta=t r, gamma=t+s with t,s>=0, giving F=tJ_r+s j².

Thus extremality proved in Theorem B remains intact, while global exposure
would be an incorrect strengthening.

