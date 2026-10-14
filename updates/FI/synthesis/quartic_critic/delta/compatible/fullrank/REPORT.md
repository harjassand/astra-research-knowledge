# Full-rank covariance extension: independent audit

This is a further compatible-gradient supplement. It is separate from the
bounded noncompatible Section 8 law and from the rank-two periodic realization
in `../REPORT.md`. It tests the optional addition of two small modes against
the same fixed quartic $G$ from FI Section 5. The result is a full-rank
covariance sequence with a sharp order-$\tau^2$ averaged-Hessian eigenvalue;
it is not a negative Jensen-gap example or a quasiconvexity result.

## Field and compatibility

For integers $m\ge3$, set $e=1/(2m)$, $k_+=(1,m)$, $k_-=(-1,m)$,
$a_+=(1,3e)$, $a_-=(1,-3e)$, and
$$
D=1+13e^2+36e^4.
$$
Use the periodic vector potential

$$
\phi_m(x_1,x_2)=
\frac{a_+\sin(2\pi k_+\cdot x)+a_-\sin(2\pi k_-\cdot x)}
     {2\pi m\sqrt D}
+e^3\begin{pmatrix}
\sin(6\pi x_1)/(6\pi)\\
\sin(8\pi x_1)/(8\pi)
\end{pmatrix}.
$$

Write $B=\begin{psmallmatrix}0&1\\6e^2&0\end{psmallmatrix}$,
$T=\operatorname{diag}(2,3)$, and $R_\pm=B\pm eT$. Differentiating gives
$$
D\phi_m=\widehat R_+\cos(2\pi k_+\cdot x)
+\widehat R_-\cos(2\pi k_-\cdot x)
+e^3 E_{11}\cos(6\pi x_1)+e^3 E_{21}\cos(8\pi x_1),
\qquad \widehat R_\pm=R_\pm/\sqrt D.
$$
The matrices $R_\pm$ are rank one and have squared Frobenius norm $D$.
This is a smooth periodic gradient with mean zero. The main two modes have
pointwise Frobenius norm at most 2; the added modes contribute at most
$2e^3$, so $\|D\phi_m\|_{L^\infty}\le2+2e^3$.

## Full-rank covariance and anisotropy

The four frequency vectors are $(1,m),(-1,m),(3,0),(4,0)$; none are equal
or opposite. Haar integration therefore removes all distinct-mode second
moments and gives
$$
C_m=\tfrac12(\hat r_+\hat r_+^T+\hat r_-\hat r_-^T)
+\tfrac{e^6}{2}(e_{11}e_{11}^T+e_{21}e_{21}^T),
\qquad M_2=\operatorname{tr}C_m=1+e^6.
$$
The four vectors $r_+,r_-,e_{11},e_{21}$ have determinant $6e$ in
row-major matrix coordinates. Consequently
$$
\det C_m=\frac{9e^{14}}{4D^2}>0,
$$
so $C_m$ has rank four for every $m\ge3$.

For the rank-two main covariance, the normalized contact inner product is
$$
\hat r_+:\hat r_- = \frac{1-13e^2+36e^4}{D},
$$
and its anisotropy parameter is $\tau_e=13e^2/D$. The added covariance has
operator norm $e^6/2$. Weyl's inequality and $M_2=1+e^6$ give
$$
\tau_m=1-\lambda_{\max}(C_m)/M_2=\tau_e+O(e^6),
\qquad \tau_m/e^2\longrightarrow13.
$$

## Positive averaged Hessian and sharp scaling

Let $H_e$ be the averaged Hessian from the main two modes. Pairwise Fourier
orthogonality removes cross terms, while each added cosine has mean square
one half. Since $D^2G$ is quadratic in its evaluation point,
$$
H_m=H_e+\frac{e^6}{2}\{D^2G(E_{11})+D^2G(E_{21})\}.
$$
The four leading principal minors of $H_e$, independently recomputed by the
checker, are
$$
\frac{2A}{D},\quad
\frac{24(6e^2+1)(19e^2+3)A}{D^2},\quad
\frac{24A B}{D^3},\quad
\frac{240e^4(243e^4+192e^2+13)B}{D^4},
$$
where $A=321e^4+104e^2+6$ and
$B=15201e^8+9752e^6+2129e^4+192e^2+6$. These are positive for every
$e>0$, so $H_e\succ0$.
In row-major coordinates $(a,b,c,d)$, direct differentiation of the
displayed $G$ gives
$$
D^2G(E_{11})=
\begin{pmatrix}
107/2&0&0&-87/2\\0&12&29/2&0\\0&29/2&107/6&0\\-87/2&0&0&38
\end{pmatrix},\quad
D^2G(E_{21})=
\begin{pmatrix}
107/6&0&0&-29/2\\0&38&87/2&0\\0&87/2&107/2&0\\-29/2&0&0&12
\end{pmatrix}.
$$
Their leading principal minors are respectively
$$
(107/2,642,1605/8,8445/16),\qquad
(107/6,2033/3,60241/24,8445/16),
$$
so both additions are positive definite. The main Hessian has a simple zero
eigenvalue at $e=0$, with the product of its three positive limiting
eigenvalues equal to 1728; its determinant satisfies
$\det H_e/e^4\to18720$. Thus
$$
\lambda_{\min}(H_e)/e^4\to65/6.
$$
The added positive matrix has norm $O(e^6)$. Weyl's inequality sandwiches
the smallest eigenvalue of $H_m$ between that of $H_e$ and that value plus
an $O(e^6)$ term, hence
$$
\boxed{\frac{\lambda_{\min}(H_m)}{M_2\tau_m^2}\longrightarrow\frac5{78}.}
$$
Also $H_m\succ0$ for every $e>0$. For every exponent $\alpha<2$,
$\lambda_{\min}(H_m)/(M_2\tau_m^\alpha)\to0$. This rules out a uniform
positive lower bound of that power form even when the covariance is full rank
and the matrices come from smooth periodic gradients with a uniform gradient
bound. The frequency grows with $m$, so this gives no fixed-bandwidth
conclusion and does not challenge a bound formulated using the exact acoustic
modulus.

## Cubic term and gap scope

There is no signed triple of the four frequency types summing to zero. This
was checked by exact enumeration of all $4^3\cdot2^3=512$ choices of three
mode types, with repetition, and signs: the vertical component is an integer
multiple of $m$, and whenever that coefficient vanishes the horizontal
component is nonzero. Since $DG$ is cubic, the averaged cubic vector is
therefore $b=\mathbb E DG(D\phi_m)=0$. Mean determinant is also zero: the
individual modes are rank one, and all distinct-mode quadratic cross terms
have zero average. The mean energy converges to the main-field limit
$27/4>0$, because the added gradient is uniformly $O(e^3)$ and $G$ is
smooth on the uniformly bounded range. Thus this full-rank extension does not
produce a negative compatible Jensen gap.

The self-contained checker
`fullrank_acoustic_realization.py` reconstructs $G$, verifies the added
Hessian matrices and Sylvester minors, checks covariance rank/determinant,
enumerates all signed cubic frequency combinations, and reproduces the
small-eigenvalue ratio. It uses SymPy only; it imports no other verifier.
