# Separate compatible-gradient audit: sharp covariance flattening

This supplement is separate from the bounded **noncompatible law** in `../DELTA_REPORT.md`. It independently checks the periodic-gradient realization proposed by the parent task. It uses the same fixed integrand \(G\) from FI Section 5. Its conclusion is a covariance-coercivity obstruction, not a negative Jensen gap or a solution of the positive-definite QC problem.

## Periodic construction

For an integer \(m\ge6\), put \(e=1/(2m)\),
\[
k_+=(1,m),\qquad k_-=(-1,m),\qquad
a_+=(1,3e),\qquad a_-=(1,-3e),
\]
\[
D=1+13e^2+36e^4,
\qquad
\varphi_m(x)=\frac{a_+\sin(2\pi k_+\cdot x)+a_-\sin(2\pi k_-\cdot x)}{2\pi m\sqrt D}
\quad(x\in\mathbb T^2).
\]
Differentiation gives
\[
D\varphi_m(x)=\frac{R_+}{\sqrt D}\cos(2\pi k_+\cdot x)
              +\frac{R_-}{\sqrt D}\cos(2\pi k_-\cdot x),
\qquad R_\pm=B_e\pm eT.
\]
Each \(R_\pm\) has rank one and Frobenius norm \(\sqrt D\). Thus \(|D\varphi_m|\le2\) pointwise. The phase map \(x\mapsto(k_+\cdot x,k_-\cdot x)\) is a finite torus covering of degree \(|\det[k_+;k_-]|=2m\); its pushforward of Haar measure is Haar measure on \(\mathbb T^2\). The two cosine variables are consequently independent, mean zero, and have second moment \(1/2\). The fields are smooth periodic gradients with zero mean and with frequency growing as \(m\to\infty\).

## Covariance and averaged Hessian

Write \(\widehat R_\pm=R_\pm/\sqrt D\) and \(P_\pm=\mathrm{vec}(\widehat R_\pm)\mathrm{vec}(\widehat R_\pm)^T\). Product-phase averaging gives
\[
C_m=\mathbb E[\mathrm{vec}(D\varphi_m)\mathrm{vec}(D\varphi_m)^T]
=\tfrac12(P_++P_-),\qquad \operatorname{tr}C_m=1,
\qquad \operatorname{rank}C_m=2.
\]
The contact angle has
\[
\widehat R_+:\widehat R_-=
\frac{1-13e^2+36e^4}{D}=
\frac{(1-4e^2)(1-9e^2)}{(1+4e^2)(1+9e^2)}>0
\quad(m\ge6).
\]
The two nonzero eigenvalues of \(C_m\) are \((1\pm\widehat R_+:\widehat R_-)/2\); with \(M_2=\operatorname{tr}C_m=1\),
\[
\tau_m=1-\lambda_{\max}(C_m)/M_2
=\frac{13e^2}{D}\sim13e^2.
\]

Because \(D^2G\) is quadratic in its evaluation point and the phases are independent,
\[
H_m=\mathbb E D^2G(D\varphi_m)
=\tfrac12\{D^2G(\widehat R_+)+D^2G(\widehat R_-)\}.
\]
The independently reconstructed leading principal minors are
\[
\begin{aligned}
&\frac{2(321e^4+104e^2+6)}D,\\
&\frac{24(6e^2+1)(19e^2+3)(321e^4+104e^2+6)}{D^2},\\
&\frac{24(321e^4+104e^2+6)(15201e^8+9752e^6+2129e^4+192e^2+6)}{D^3},\\
&\frac{240e^4(243e^4+192e^2+13)(15201e^8+9752e^6+2129e^4+192e^2+6)}{D^4}.
\end{aligned}
\]
They are positive for every \(e>0\), so each \(H_m\succ0\). The cubic vector is zero by product-phase symmetry. The exact mean energy is
\[
\mathbb E G(D\varphi_m)=
\frac{3(17334e^8+9428e^6+2079e^4+218e^2+9)}{4D^2}>0.
\]
Thus this construction is not a compatible negative-gap example.

## Smallest-eigenvalue asymptotic

At \(e=0\),
\[
H_0=\begin{pmatrix}
12&0&0&-12\\0&36&36&0\\0&36&38&0\\-12&0&0&12
\end{pmatrix},
\qquad \ker H_0=\mathbb R(1,0,0,1).
\]
Its eigenvalues are \(0,24,37-\sqrt{1297},37+\sqrt{1297}\); the product of the three nonzero eigenvalues is \(24\cdot72=1728\). The exact determinant is
\[
\det H_m=
\frac{240e^4(243e^4+192e^2+13)(15201e^8+9752e^6+2129e^4+192e^2+6)}{D^4},
\]
so \(\det H_m/e^4\to18720\). The zero eigenvalue of \(H_0\) is simple and the other three eigenvalues converge to positive limits; therefore
\[
\frac{\lambda_{\min}(H_m)}{e^4}\longrightarrow
\frac{18720}{1728}=\frac{65}{6}.
\]
As \(\tau_m^2/e^4\to169\),
\[
\boxed{\frac{\lambda_{\min}(H_m)}{M_2\tau_m^2}\longrightarrow\frac{5}{78}.}
\]
For any exponent \(\alpha<2\), \(\lambda_{\min}(H_m)/(M_2\tau_m^\alpha)\to0\). Thus no positive uniform constant in a bound \(\lambda_{\min}H\ge c_F M_2\tau^\alpha\) with \(\alpha<2\) can hold even on smooth periodic compatible gradients with uniformly bounded gradients, for this fixed \(G\). The construction has increasing frequency, so it does not contradict any fixed-bandwidth assertion. It also leaves the source's lower bound involving the exact acoustic modulus \(\mu_G\) intact.

The checker `compatible_acoustic_realization.py` reconstructs the wave matrices, torus degree, covariance spectrum and \(\tau\), product-phase moments, Hessian minors/determinant, and eigenvalue limit from the displayed \(G\). It imports SymPy only and does not inspect another verifier or sibling artifact.
