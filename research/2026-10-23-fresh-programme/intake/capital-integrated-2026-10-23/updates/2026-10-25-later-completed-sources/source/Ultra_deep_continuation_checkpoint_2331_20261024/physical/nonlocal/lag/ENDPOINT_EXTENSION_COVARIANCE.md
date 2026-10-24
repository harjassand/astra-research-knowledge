# Endpoint-extension covariance check

This is a bounded quantum-equilibrium calculation for the distributed-rod Fejer N=4 cell and the specified local counted-pendant comparator. It uses hbar=k_B=theta=1, so Matsubara frequencies are nu_l=2*pi*l. The calculation is an ideal harmonic metric-graph result, not a material or device claim.

For the Fejer cell, K=Mtot=1, tau=a/c=1/sqrt(101), m=100/101, and (kappa_1,kappa_2,kappa_3)=(0.15,0.10,0.05). The endpoint coordinate for an n-cell rod is delta_n=x_(j+n)-x_j. Eliminating the rod interiors at Euclidean frequency gives

    D_E(q,nu)=m*nu^2+2*sum_(n=1)^3 kappa_n*sigma_n*(coth(sigma_n)-cos(nq)*csch(sigma_n)),
    sigma_n=n*nu*tau,

and

    Var(delta_n)=theta*sum_(l in Z) average_q [2*(1-cos(nq))/D_E(q,nu_l)].

The l=0 term is evaluated after quotienting the common translation; the difference-coordinate integrand has a finite q->0 limit.

For the pendant cell, m_b=0.001, ell/a=0.4, k=0.4, the backbone-rod mass is 1/101, the pendant-rod mass is k*(0.4*tau)^2=0.064/101, and m_s=0.9884653465346535. The total-mass check is exactly 1 in the displayed parameters. For eta=nu*tau, zeta=0.4*nu*tau, set

    P=k*zeta*coth(zeta), C=k*zeta*csch(zeta), D=m_s*nu^2+P,
    A=m_b*nu^2+2*K*eta*coth(eta)+P-C^2/D,
    B=2*K*eta*csch(eta), S=sqrt(A^2-B^2).

A Schur complement followed by exact reciprocal-q averages gives, for l>0,

    average_q [(-1,1) D_E^(-1) (-1,1)^T] = 1/D + (1-C/D)^2/S,
    average_q [2*(1-cos q)*(D_E^(-1))_bb] = (2/S)*(1-B/(A+S)).

At l=0, the relative pendant coordinate contributes exactly theta/k=2.5, and the nearest-neighbor backbone difference contributes exactly theta/K=1. Direct 256-node Gauss-Legendre q integration of terms l=1,2,10,100 agrees with these closed forms to at most 5.6e-16.

The omitted Matsubara tail is positive. Since the Euclidean rod contributions are positive semidefinite, D_E >= M*nu_l^2 pointwise in q. Therefore, after the positive sum through l=L, the residual upper bounds are

    Fejer delta_n:       1/(m*pi^2*theta*L)
    pendant x_s-x_b:     (1/m_b+1/m_s)/(2*pi^2*theta*L)
    backbone neighbor:   1/(pi^2*theta*m_b*L).

These bound only the Matsubara tail; they do not certify the Fejer q-quadrature.

At L=500,000, the finite partial sums and Matsubara-tail bounds are:

| Cell coordinate | Partial sum | Tail upper bound | Status of q average |
|---|---:|---:|---|
| Fejer delta_1 | 3.0098135898 | 2.05e-7 | Gauss-Legendre; Q=64,128,256,512 varied by <5e-12 at L=20,000 |
| Fejer delta_2 | 3.6814394196 | 2.05e-7 | same |
| Fejer delta_3 | 4.6012728354 | 2.05e-7 | same |
| Pendant relative x_s-x_b | 8.1555548119 | 1.02e-4 | exact reciprocal-q average |
| Pendant-cell backbone neighbor | 10.8832934680 | 2.03e-4 | exact reciprocal-q average |

The local pendant choice has substantially larger endpoint-extension variances than the three Fejer rod endpoint coordinates at this parameter point, especially because its backbone point mass is only 0.001. These are coordinate-specific equilibrium variances, not a matched range-cap proof: geometry, supports, fabrication constraints, and other modes are outside the fixture.

Replay: endpoint_extension_covariance.py; full refinement data and tail bounds: endpoint_extension_covariance_results.json.
