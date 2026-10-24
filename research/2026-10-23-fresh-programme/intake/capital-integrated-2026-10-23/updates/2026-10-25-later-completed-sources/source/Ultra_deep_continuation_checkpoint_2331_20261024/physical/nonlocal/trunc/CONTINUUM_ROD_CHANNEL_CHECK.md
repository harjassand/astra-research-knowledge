# Continuum-rod realization of the positive finite-range kernel

## Scope and model

This is an ideal metric-graph model, not a routed three-dimensional device. There is one point mass \(M\) at each lattice vertex \(j\in\mathbb Z\), and for each \(n=1,\ldots,N-1\) one independent uniform axial rod edge from \(j\) to \(j+n\) in every cell. Edge length is \(L_n=na\). All edges have the same Young modulus \(E\) and mass density \(\rho\), with \(c=\sqrt{E/\rho}\), and cross-section
\[
 A_n=\frac{\kappa_n L_n}{E}.
\]
Edges interact only through their endpoint vertices. The result below counts every continuum rod mode; it does not discard internal modes.

## Counted rod mass and acoustic limit

Each length-\(L_n\) rod has mass
\[
 m_n^{\rm rod}=\rho A_nL_n
 =\frac{\rho}{E}\kappa_nL_n^2
 =\frac{\kappa_n n^2a^2}{c^2}.
\]
There is one outgoing edge of each length per cell (equivalently, half of the incoming plus half of the outgoing edge mass belongs to a cell), so
\[
 M_{\rm rod/cell}=\sum_{n=1}^{N-1}m_n^{\rm rod}
 =\frac{a^2}{c^2}\sum_n n^2\kappa_n
 =\frac{K_{\rm eff}a^2}{c^2}.
\]
For the specified kernel \(\kappa_n=c_N(N-n)\), \(c_N=12K/[N^2(N^2-1)]\), the finite sum is \(\sum_n n^2\kappa_n=K\); hence the rod mass per cell is exactly \(Ka^2/c^2\), independent of \(N\).

For harmonic frequency \(\omega\), put \(\theta_n=\omega L_n/c=\omega na/c\). Away from rod Dirichlet poles, the field on edge \((j,j+n)\), with endpoint displacements \(X_j,X_{j+n}\), is
\[
 U_{j,n}(s)=
 X_j\frac{\sin[\theta_n(1-s/L_n)]}{\sin\theta_n}
 +X_{j+n}\frac{\sin(\theta_n s/L_n)}{\sin\theta_n}.
\]
Since \(EA_n(\omega/c)=\kappa_n\theta_n\), the forces from the outgoing and incoming rods at vertex \(j\) sum to
\[
 F_j=\sum_n\frac{\kappa_n\theta_n}{\sin\theta_n}
 [X_{j+n}+X_{j-n}-2X_j\cos\theta_n].
\]
With \(X_j=Xe^{iqj}\), Newton's equation \(-M\omega^2X=F_j\) is exactly
\[
 D(q,\omega):=-M\omega^2+
 2\sum_{n=1}^{N-1}\kappa_n\theta_n
 \frac{\cos\theta_n-\cos(nq)}{\sin\theta_n}=0.
\]
Here \(q\) is the dimensionless phase per cell.

For \(q\to0\) on the acoustic branch, \(\omega=O(q)\), and
\[
 2\kappa_n\theta_n
 \frac{\cos\theta_n-\cos(nq)}{\sin\theta_n}
 =\kappa_n n^2q^2-
   \kappa_n\frac{n^2a^2}{c^2}\omega^2+O(q^4).
\]
Thus
\[
 D(q,\omega)=K_{\rm eff}q^2-
 \left(M+M_{\rm rod/cell}\right)\omega^2+O(q^4),
 \qquad
 \omega^2=\frac{K_{\rm eff}}{M+M_{\rm rod/cell}}q^2+O(q^4).
\]
The static long-wave stiffness is the original \(K_{\rm eff}=\sum n^2\kappa_n=K\); the acoustic inertia is the point mass plus the fully counted rod mass. In physical wave number \(k=q/a\), the sound speed is \(a\sqrt{K/(M+Ka^2/c^2)}\).

## What happens at \(\sin\theta_n=0\)

The secular equation above is an elimination formula and is not valid at its poles. Let
\[
 R(\omega)=\{n:\theta_n=m_n\pi\text{ for some integer }m_n\ge1\}.
\]
This is a discrete, locally finite set of frequencies for fixed finite \(N\). On a resonant rod, the endpoint-value problem is solvable only if
\[
 X_{j+n}=(-1)^{m_n}X_j.
\]
If the common Bloch vertex amplitude \(X\ne0\), this means \(e^{inq}=(-1)^{m_n}\) for every \(n\in R\). A compatible resonant-rod field has the form
\[
 U_{j,n}(s)=Xe^{iqj}\cos(m_n\pi s/L_n)
             +A_ne^{iqj}\sin(m_n\pi s/L_n).
\]
The cosine component has zero endpoint derivatives. The sine component's net force at each vertex is proportional to
\(\kappa_n\theta_n[1-(-1)^{m_n}e^{-inq}]A_n\), which also vanishes under the compatibility condition. Therefore a node-bearing mode exists only if the nonresonant rods and point mass separately obey
\[
 D_{\rm nr}(q,\omega):=-M\omega^2+
 2\sum_{n\notin R}\kappa_n\theta_n
 \frac{\cos\theta_n-\cos(nq)}{\sin\theta_n}=0.
\]
Such a mode is an exceptional compatible crossing. The free sine coefficient does not enter vertex force balance, but it can interfere with the cosine component and make a resonant rod carry power. For the harmonic power convention \(J=(\omega EA_n/2)\operatorname{Im}(U^*U')\), this field gives the constant rod flux \(J_n=(\omega EA_n\theta_n/(2L_n))\operatorname{Im}(X^*A_n)\), equivalently \(J_n=(\omega EA_n(\omega/c)/2)\operatorname{Im}(X^*A_n)\). It vanishes for a pure cosine or pure sine, but not for a quadrature mixture (a traveling-wave component). Thus a node-bearing compatible crossing can carry flux in resonant rods as well as in nonresonant rods, if it also satisfies \(D_{\rm nr}=0\). Such crossings occur only at the discrete resonant frequencies and do not affect frequency integrals.

There are also node-zero Dirichlet modes. Set \(X_j=0\). Nonresonant rods must then vanish, while each resonant rod can have
\(U_{j,n}(s)=A_ne^{iqj}\sin(m_n\pi s/L_n)\). Vertex force balance is the single equation
\[
 \sum_{n\in R}\kappa_n\theta_n
  [1-(-1)^{m_n}e^{-inq}]A_n=0.
\]
If \(|R|\ge2\), this has a nonzero solution for every \(q\), producing one or more genuinely flat bands at that commensurate frequency (at least \(|R|-1\) independent modes generically). If \(|R|=1\), it has a solution only at the finitely many phases satisfying \(e^{inq}=(-1)^{m_n}\); these are isolated Bloch eigenmodes, not a flat band. Every *node-zero* Dirichlet mode is a pure sine on each resonant rod, so its time-averaged axial power is zero; a flat band also has zero group velocity. These dark modes are not flux-carrying channels. At a compatible phase, however, a node-bearing mode satisfying \(D_{\rm nr}=0\) can be superposed with the dark sine modes and may carry flux, including along resonant rods through cosine–sine interference. This is an exceptional crossing at a pole, not part of the flat Dirichlet sector.

## Channel-count lemma away from the poles

Put \(d=N-1\). At a fixed \(\omega>0\) with \(\sin\theta_n\ne0\) for every \(n\), \(D(q,\omega)\) is an even trigonometric polynomial
\[
 D(q,\omega)=c_0(\omega)+\sum_{n=1}^{d}c_n(\omega)\cos(nq),
 \qquad
 c_n(\omega)=-\frac{2\kappa_n\theta_n}{\sin\theta_n}\ne0.
\]
Writing \(z=e^{iq}\) and multiplying by \(z^d\) gives a nonzero polynomial of degree \(2d\) (the leading coefficient is \(c_d/2\)). Hence there are at most \(2d\) Bloch phases solving the secular equation, counting distinct roots. Away from band edges, every propagating root is regular and gives one mode: for nonpole frequencies the edge profiles are uniquely fixed by the single vertex amplitude, so there is no hidden internal eigenvector multiplicity. Time reversal pairs \(q\) with \(-q\) and reverses the group velocity. A flux-carrying root has nonzero group velocity, so it is not at the self-paired phases \(q=0,\pi\); the pair contributes exactly one right-moving channel. Therefore
\[
 N_{\rm ch}(\omega)\le d=N-1
\]
at every regular nonpole frequency. To justify the almost-everywhere qualification, between adjacent rod poles the nonpole dispersion branches are real analytic; in any compact frequency subinterval there are finitely many branches. None can be identically flat, since that would require \(D(q,\omega_0)\equiv0\) for all \(q\), contradicting its nonzero highest-harmonic coefficient. Thus each branch has only a discrete set of stationary points, and the band-edge/degeneracy frequencies form a measure-zero (locally countable) set. The excluded rod-pole set is countable as well. At poles, do not apply the eliminated secular equation: count only flux-carrying modes of the full vertex-plus-edge problem, not the flat Dirichlet modes.

Consequently, for every nonnegative integrable weight \(g\) and every measurable tail set \(I\subset(0,\infty)\),
\[
 \int_I g(\omega)N_{\rm ch}(\omega)\,d\omega
 \le (N-1)\int_I g(\omega)\,d\omega.
\]
The inequality is an almost-everywhere channel-count statement; countably many rod-pole frequencies do not affect the integral. It does not by itself imply a small tail as \(N\) grows, since the prefactor is \(N-1\).
