# P1 completed return — 28da6f9d

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2
Prompt: P1_FULL_ORIGINAL_QUARTIC_AFTER_NONLINEAR_PROJECTION_PRO_20261111.txt (source SHA-256 07b643dbc399549024ad3dcfde570ae1a1a22028019aacfba7fa6882c3437261); user turn 953cb3b9-ae2b-4608-8031-7f3a4742751c. Model shown: Pro. Assistant final 28da6f9d-cf6b-50d3-8589-12eaf7d347d2, native read without truncation, observed 2026-11-11 UTC. Current activity and helper details not captured: chat UI loaded older history rather than the current activity. A ZIP was visible in the output panel but its identity was not established; the final links the existing held library packet, which was not collected. No individual files downloaded.

## Complete available final

**I have not resolved the full unrestricted inequality.** I have neither a proof for every \(k>1/3\) nor an actual compatible field with a negative original gap.

The continuation did establish an exact compatibility identity and a theorem about the **actual conditional minima at the lower endpoint**. It also produced an explicit example showing that those conditional minima can decrease along part of the radial path while their **total original energy gap remains strictly positive**. Thus a proof based on universal nonnegative conditional radial flux is now ruled out.

The complete derivations, independent audits, and finite arithmetic receipt are in :chatgpt-content-reference{index="0"}[POTENTIAL_LAW_AND_RADIAL_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/POTENTIAL_LAW_AND_RADIAL_CONTINUATION_RESULTS.txt). The [complete research packet](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal) has been updated to version 13, retaining the earlier capital and the accepted large-\(k\) proof.

## 1. An exact compatibility constraint on Jacobian variance

This result applies to actual \(W^{1,4}\) gradients and accommodates folds and atoms in the distribution of a scalar potential.

For an invertible affine mean, a constant **left** \(SO(2)\) rotation puts its first row into the form \((s,0)\), \(s\ne0\). This preserves \(J_k\), compatibility, and the original source torus. Write the two output potentials as
\[
u=sU,\qquad U(x)=x_1+\frac{f(x)}s,
\]
\[
v=b_1x_1+b_2x_2+g(x),
\qquad d=sb_2=\det A,
\]
where \(f,g\) are periodic. Regard \(U\bmod1\) as a map into the unit circle, and let
\[
\nu=U_\#dx
\]
be its probability law.

For every smooth periodic scalar function \(\Lambda\), actual gradient compatibility gives
\[
\int_{\mathbb T^2}\Lambda(U)\,\partial_1U\,dx
=\int_{\mathbb T}\Lambda(\theta)\,d\theta,
\tag{1}
\]
and
\[
\int_{\mathbb T^2}\Lambda(U)\,j\,dx
=d\int_{\mathbb T}\Lambda(\theta)\,d\theta,
\qquad j=\det D(u,v).
\tag{2}
\]

To verify these identities, choose a periodic primitive \(P\) satisfying
\[
P'=\Lambda-\overline\Lambda.
\]
Then
\[
D\bigl(\overline\Lambda U+P(U)\bigr)=\Lambda(U)DU.
\]
The expression inside the derivative is an actual affine-periodic scalar potential with affine gradient \(\overline\Lambda e_1\). Integrating its derivative proves (1); pairing its gradient with \(Dv\) through the determinant proves (2). The Sobolev chain rule and strong \(W^{1,4}\) approximation justify the same calculation for the stated rough fields.

Equation (1) implies that Haar measure \(d\theta\) is absolutely continuous with respect to \(\nu\). Define
\[
w=\frac{d\theta}{d\nu}.
\]
The two weighted identities say precisely
\[
w(U)=\mathbb E[\partial_1U\mid U],
\qquad
\mathbb E[j\mid U]=d\,w(U).
\tag{3}
\]
In particular,
\[
w\ge0,\qquad \int w\,d\nu=1,\qquad
\|w\|_{L^4(\nu)}\le \|\partial_1U\|_4.
\]

The resulting orthogonal decomposition is
\[
\boxed{
\int_{\mathbb T^2}(j-d)^2\,dx
=
\int_{\mathbb T^2}\bigl(j-dw(U)\bigr)^2\,dx
+
d^2\left(\int_{\mathbb T}w^2\,d\nu-1\right).
}
\tag{4}
\]

Both terms are parts of the **same** original Jacobian variance. They are not additional reserves.

If
\[
\nu=\rho\,d\theta+\nu_s,
\]
then
\[
\int w^2\,d\nu=\int_0^1\frac{d\theta}{\rho(\theta)}.
\tag{5}
\]
Its finiteness follows from (3); it is not an extra regularity assumption on \(\rho\). If the singular part has mass \(p\), then
\[
\int w^2\,d\nu\ge\frac1{1-p},
\]
and hence
\[
\int(j-d)^2\ge \frac{d^2p}{1-p}.
\tag{6}
\]

A useful consequence is that **constant total determinant \(j=d\ne0\) forces the first-coordinate law to be uniform**.

### A direct consequence for the original density

Write, as in the supplied endpoint representation,
\[
J_k(F)=j(F)^2+\ell Q_k(F),\qquad \ell=3k-1,
\]
where \(Q_k\ge0\). For the fixed first potential above, every compatible second row satisfies
\[
\boxed{
\int J_k(F)-J_k(A)
\ge
d^2\left(\int w^2\,d\nu-1\right)-\ell Q_k(A).
}
\tag{7}
\]

This is an original-energy certificate with no restriction on the completing second row’s amplitude, frequency, concentration, or determinant sign. A positive first-coordinate contribution therefore excludes that fixed first row from being a negative test sufficiently near \(k=1/3\).

The limitation is exact: when \(\nu\) is uniform, this contribution vanishes. In particular, it does not resolve the anisotropic energy on arbitrary constant-total-Jacobian maps.

### Attainment in the smooth monotone case

Suppose \(U\) is smooth and \(\partial_1U\ge c>0\). Let \(X(\theta,y)\) invert \(x_1\mapsto U(x_1,y)\), and set
\[
q(\theta,y)=X_\theta(\theta,y),\qquad
\rho(\theta)=\int_0^1q(\theta,y)\,dy,
\]
\[
C(\theta,y)=\int_0^y\frac{q(\theta,z)}{\rho(\theta)}\,dz.
\]
Then
\[
v_0=b_1U+b_2C(U,x_2)
\]
has the correct affine increments and
\[
\det D(sU,v_0)=\frac d{\rho(U)}.
\]
Consequently,
\[
\boxed{
\min_{g\in W^{1,4}_{\rm per}}
\int \det D(sU,b\cdot x+g)^2
=
d^2\int_0^1\rho^{-1}.
}
\tag{8}
\]

This is an explicit compatible completion attaining the determinant-energy minimum. It does not assert that the same completion minimizes \(J_k\).

## 2. The actual conditional minima have a precise lower-endpoint limit

This theorem fixes an arbitrary actual first row and minimizes over **every** compatible second row.

Let
\[
x=a+Df,\qquad
\mathcal Y_b=\{b+Dg:g\in W^{1,4}_{\rm per}\}.
\]
Define
\[
Z(y)=\int \det(x;y)^2,\qquad
m_0=\inf_{y\in\mathcal Y_b}Z(y),
\]
and, with \(k=(1+\ell)/3\),
\[
m_\ell=\min_{y\in\mathcal Y_b}
\int J_{(1+\ell)/3}(x;y).
\]

The original conditional minimum \(m_\ell\) is attained. Let
\[
\mathcal M_0=\{y\in\mathcal Y_b:Z(y)=m_0\}.
\]
If this set is nonempty, put
\[
m_1=\min_{y\in\mathcal M_0}\int Q_0(x;y).
\]
If it is empty, define \(m_1=+\infty\).

The proved value limit is
\[
\boxed{
m_\ell\longrightarrow m_0,\qquad
\frac{m_\ell-m_0}{\ell}\longrightarrow m_1
\quad\text{as }\ell\downarrow0.
}
\tag{9}
\]

When \(m_1<\infty\), its constrained minimizing row \(\bar y\) is unique, and the actual original minimizing rows satisfy
\[
\boxed{y_\ell\longrightarrow\bar y\quad\text{strongly in }L^4.}
\tag{10}
\]

This is stronger than a candidate upper bound or a formal expansion around a selected completion.

### What pays the limit

First, the correction itself has uniform coercivity:
\[
\boxed{
\frac1{336}|F|^4\le Q_k(F)\le\frac7{16}|F|^4,
\qquad \frac13\le k\le1.
}
\tag{11}
\]
This estimate is for \(Q_k\) itself. It is not obtained by dividing a bound for \(J_k\) and overlooking the remaining \(j^2/\ell\).

For the lower bound, put \(r=ku-v+2j\). Then
\[
(ku+v)^2
=(ku-v)^2+4kuv
\le2r^2+(8+4k)uv
\le16(k+2)Q_k(F).
\]
Since \(ku+v\ge k|F|^2\) for \(k\le1\),
\[
Q_k(F)\ge\frac{k^2}{16(k+2)}|F|^4\ge\frac1{336}|F|^4.
\]

The exact division formula also yields
\[
|\widehat Q_\ell(F)-\widehat Q_\varepsilon(F)|
\le\frac{13}{96}|\ell-\varepsilon|\,|F|^4,
\qquad
\widehat Q_\ell=Q_{(1+\ell)/3}.
\tag{12}
\]

If \(m_0\) is attained, all its minimizers have the same determinant field \(j_*\). The quadratic Euler identity gives
\[
Z(y)-m_0=\|j_y-j_*\|_2^2
\tag{13}
\]
for every compatible second row.

On the affine constraint \(j_y=j_*\), the determinant square is constant along row segments. Original row convexity therefore makes \(Q_0\) convex on that constraint. Dividing the accepted original row reserve by \(\ell\) gives
\[
Q_0(x,y_1)-Q_0(x,y_0)
-D_yQ_0(x,y_0)\cdot(y_1-y_0)
\ge\frac1{288}|y_1-y_0|^4
\tag{14}
\]
whenever the two determinant fields agree. This proves existence and uniqueness of the constrained minimizer.

The essential lower-limit argument avoids assuming that \(Q_0\) is convex away from this constraint. Set
\[
R_\ell(y)
=\frac{\int J_{(1+\ell)/3}(x;y)-m_0}{\ell}.
\]
For fixed \(\varepsilon\ge\ell>0\),
\[
R_\ell(y)\ge R_\varepsilon(y)
-\frac{13\varepsilon}{96}\int|(x;y)|^4.
\tag{15}
\]
The functional \(R_\varepsilon\) is a positive multiple of the **original convex row functional**, plus a constant. It is weakly lower semicontinuous. Coercivity supplies the uniform \(L^4\) bound, so one first takes the weak lower limit in (15), then lets \(\varepsilon\downarrow0\). A fixed constrained minimizer provides the matching upper bound.

Finally, applying the original row reserve at the actual minimizer \(y_\ell\) gives
\[
\int\widehat Q_\ell(x;\bar y)
-\frac{m_\ell-m_0}{\ell}
\ge\frac1{288}\|\bar y-y_\ell\|_4^4.
\]
The left side tends to zero, proving (10).

If \(m_0\) is unattained, boundedness of \((m_\ell-m_0)/\ell\) along a sequence would give an \(L^4\)-bounded sequence of original minimizers. Its weak limit would attain \(m_0\), a contradiction. Thus the scaled excess tends to \(+\infty\). In that case the fixed first row has a strictly positive original conditional gap sufficiently near the endpoint.

### The remaining sign is now explicit

Writing \(d=\det A\), the attained case gives
\[
\boxed{
m_\ell-J_{(1+\ell)/3}(A)
=
(m_0-d^2)
+\ell\bigl[m_1-Q_0(A)\bigr]
+o(\ell).
}
\tag{16}
\]

In the smooth monotone case of (8), **every** determinant-minimizing second potential is
\[
v=v_0+p(U),
\qquad p\in W^{1,4}_{\rm per}(\mathbb T),
\tag{17}
\]
up to an additive constant. In inverse coordinates, the difference between any two minimizers has zero derivative in the fiber direction, which proves this classification.

Therefore \(m_1\) becomes an exact scalar-profile problem
\[
m_1=
\min_{\substack{z\in L^4(\mathbb T)\\ \int z=0}}
\int_0^1\mathcal Q(\theta,z(\theta))\,d\theta,
\tag{18}
\]
where \(\mathcal Q\) is a convex quartic obtained by integrating the original \(Q_0\) over the fiber with its actual source weight \(q=X_\theta\).

The unresolved comparison is
\[
\boxed{m_1\ge Q_0(A)}
\tag{19}
\]
when \(m_0=d^2\). The coefficients of \(\mathcal Q\) retain the two-variable geometry of \(U\), so convexity in \(z\) does not establish (19).

No actual field violating (19) was obtained. Equality leaves higher orders open. The entire limit theorem fixes the first row; it does not supply uniform control over first rows changing with \(k\).

## 3. Conditional radial work can be negative while the total original gap is positive

Here is an explicit construction showing why the radial-work formula cannot be closed by proving \(M'(t)\ge0\) everywhere.

Center a disk of radius \(R=1/4\) at \(z_c=(1/2,1/2)\). Define
\[
\Phi(z)=z_c+\mathcal R_{\theta(r)}(z-z_c),
\qquad r=|z-z_c|,
\]
inside the disk, and let \(\Phi(z)=z\) outside, with
\[
\theta(r)=
\begin{cases}
3\pi,&0\le r\le1/8,\\
6\pi(1-4r),&1/8<r<1/4,\\
0,&r\ge1/4.
\end{cases}
\tag{20}
\]
This is a Lipschitz map equal to the identity near the cell boundary. Thus
\[
\Phi=\operatorname{id}+(f,g_1)
\]
is an actual affine-periodic map.

On the annulus,
\[
D\Phi
=\mathcal R_{\theta(r)}
\left(I+\alpha e_\theta\otimes e_r\right),
\qquad \alpha=r\theta'(r).
\]
Because \(e_\theta\cdot e_r=0\),
\[
\det D\Phi=1,\qquad |D\Phi|^2=2+\alpha^2<578.
\tag{21}
\]

Choose the exact rational parameter
\[
\boxed{
k=\frac{16777217}{50331648},\qquad \ell=2^{-24}.
}
\tag{22}
\]
For the actual conditional minimum
\[
M(t)=\min_g\int J_k(e_1+tDf,e_2+Dg),
\tag{23}
\]
the accepted attained-row and radial-work results apply.

At \(t=1/2\), the first potential is constant on the core: the half-turn gives
\[
x_1+\frac12f=\frac12.
\]
Every second-row completion therefore has determinant zero on a set of area \(\pi/64\), while compatibility still requires determinant integral one. Cauchy–Schwarz gives
\[
\boxed{
M(1/2)\ge\frac1{1-\pi/64}>\frac{64}{61}.
}
\tag{24}
\]

At \(t=1\), the explicit second component of \(\Phi\) is an admissible competitor. Using
\[
Q_k(F)\le\frac7{16}|F|^4,\qquad \frac13\le k\le1,
\]
and (21),
\[
\int Q_k(D\Phi)<2^{18}.
\]
Hence
\[
\boxed{M(1)<1+2^{18}2^{-24}=\frac{65}{64}.}
\tag{25}
\]

It follows that
\[
\boxed{
\int_{1/2}^1M'(t)\,dt<-\frac{131}{3904},
}
\tag{26}
\]
and \(M'(t)<-131/1952\) at some point of that interval.

These bounds concern the actual conditional minimum. The midpoint estimate covers every completing second row; the endpoint upper bound uses one compatible competitor. No trial second row has been substituted for the minimizer along the path.

The same example has a rigorously **positive total original gap**. Its first-row fourth moment is exactly
\[
\int|D\Phi_1|^4
=
1+\frac{405\pi^3}{256}+\frac{5103\pi^5}{512}
>2304.
\tag{27}
\]
The elementary estimate
\[
Q_k(F)\ge\frac{|F|^4}{1152}
\]
and determinant Jensen imply, for every completing second row,
\[
\int J_k(D\Phi_1,e_2+Dg)>1+2\ell.
\]
Meanwhile
\[
M(0)=J_k(I)=1+\frac{\ell(k+3)}8<1+\frac\ell2.
\]
Therefore
\[
\boxed{M(1)-M(0)>\frac3{2^{25}}>0.}
\tag{28}
\]

Thus negative conditional radial flux is compatible with a certified positive total original gap. It cannot serve as an original quasiconvexity counterexample.

## 4. A nonlinear compatible class has an all-profile, all-mean theorem

A separate construction gives another actual integral operation, rather than a finite collection of positive samples.

Let \(f,g\) be arbitrary smooth periodic profiles satisfying
\[
a(p,v)=1+f''(p+v)+g''(p-v)>0.
\]
Set
\[
L(p,v)=\frac{p^2+v^2}{2}+f(p+v)+g(p-v),
\qquad u=L_p.
\]
The map \((p,v)\mapsto(u,v)\) is an actual torus diffeomorphism with Jacobian \(a\). Its partial Legendre transform
\[
\Phi(u,v)=up-L(p,v)
\]
has
\[
\Phi(u,v)=\frac{u^2-v^2}{2}+\psi(u,v),
\qquad \det D^2\Phi=-1,
\]
with periodic \(\psi\).

For any constant output matrix \(T\), define the compatible gradient
\[
G=TR\bigl(D^2\Phi-S\bigr),
\qquad S=\operatorname{diag}(1,-1).
\]
Then, for every continuous rank-one-convex integrand \(W\) and every independent affine mean \(A\),
\[
\boxed{\int W(A+G)\ge W(A).}
\tag{29}
\]

The proof retains the actual nonconstant source Jacobian. With
\[
\alpha=f''(p+v),\qquad \beta=g''(p-v),
\]
one has
\[
D^2\Phi=
\frac1{1+\alpha+\beta}
\begin{pmatrix}
1&-(\alpha-\beta)\\
-(\alpha-\beta)&-(1+2\alpha+2\beta+4\alpha\beta)
\end{pmatrix}.
\]
For fixed \(\beta\), the matrix lies on a rank-one line as \(\alpha\) varies, while \(aD^2\Phi\) is affine in \(\alpha\). The weighted energy is consequently convex in that scalar variable. The same holds with the variables reversed.

The integer phase map
\[
(p,v)\mapsto(p+v,p-v)
\]
is a degree-two torus covering that preserves normalized Haar measure. Thus the two profile means are independently zero. Two weighted rank-one Jensen steps prove (29).

For \(J_k\), their two distinct rank-one reserves give
\[
\boxed{
\int J_k(A+G)-J_k(A)
\ge\frac{\mu_k}{24\nu_k}\int J_k(G),
}
\tag{30}
\]
where \(\mu_k|F|^4\le J_k(F)\le\nu_k|F|^4\) are paid positive coercivity and upper constants.

This covers the entire stated smooth global partial-Legendre branch, with arbitrary profiles, amplitudes, frequencies, and independent means. It does not cover arbitrary gradients or justify continuation through folds of the coordinate map.

## 5. One finite certificate was executed exactly

The distributional quantity in (4) has the dual formula
\[
\int w^2\,d\nu-1
=
\sup_{\Lambda}
\left[
2\int_0^1\Lambda(\theta)\,d\theta
-\int_{\mathbb T^2}\Lambda(U)^2\,dx-1
\right],
\tag{31}
\]
where real trigonometric polynomials suffice. Each single test supplies a lower certificate; no optimal-test oracle is required.

For finite rational Fourier data, its moments can be enclosed using a finite Taylor polynomial for \(e^{it}\), whose remainder is at most
\[
\frac{|t|^{M+1}}{(M+1)!},
\]
followed by exact Gaussian-rational Laurent integration.

For the actual first potential
\[
U=x_1+\frac{\sin(2\pi x_1)\cos(2\pi x_2)}{4\pi},
\tag{32}
\]
the contributions through degree five to
\[
c_2=\int\cos(4\pi U)
\]
are exactly
\[
0,\quad0,\quad\frac1{16},\quad0,\quad-\frac1{256},\quad0.
\]
The remainder is at most \(1/720\), giving
\[
c_2\ge\frac{659}{11520}>\frac1{18}.
\]
Taking
\[
\Lambda(\theta)=1-\frac{\cos(4\pi\theta)}{18}
\]
in (31) proves
\[
\int w^2\,d\nu-1\ge\frac1{324}.
\]
At
\[
k=\frac{325}{972},\qquad \ell=\frac1{324},
\]
equation (7) therefore gives the original bound
\[
\boxed{
\int J_k\bigl(D(U,x_2+g)\bigr)-J_k(I)\ge\frac1{648}
}
\tag{33}
\]
for **every** real periodic \(g\in W^{1,4}\).

The exact check ran once, using standard-library rational arithmetic: 220 Laurent coefficient-pair products, 892 instrumented rational additions, and 904 rational multiplications, together with six factorial scalings and finite rational comparisons. The Taylor error is included above. No numerical optimization, sampling, quadrature, or conditional solver was run.

## What is still missing

For every actual compatible \(G\), the unrestricted problem still requires
\[
\boxed{b_G^T H_G^\dagger b_G\le2c_G.}
\]

The new results do not establish that inequality. At the lower endpoint they identify a more precise fixed-first-row obstruction: an approaching negative sequence with one fixed first row must have an attained determinant minimum \(m_0=d^2\), and its constrained correction must satisfy \(m_1\le Q_0(A)\). The strict negative case has not been realized; the universal opposite inequality has not been proved.

The accepted unrestricted large-\(k\) theorem remains intact. Arbitrary determinant fluctuations and the remaining parameter interval are still unresolved in this work.