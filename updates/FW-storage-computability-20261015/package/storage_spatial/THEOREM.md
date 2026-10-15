# Buffered global-heat finite-dimensionalization of storage

Internal deduction, 15 October 2026. Conditional on the exact G global periodic anisotropic heat monotonicity and coercivity stated in SOURCE_QC_REPORT.md. No attainment or interior gradient-tail budget is used. A separate same-team challenge checked the estimates and interval directions; this is not external review.

## Main operation

For an explicitly given finite Fourier endpoint U and constant matrix B (with computable coefficients and certified numerical enclosures), a supplied finite-horizon value gap plus endpoint-dependent L4 gradient bound yields an effective compact finite-dimensional approximation to unrestricted adjusted storage p_B(U), with any prescribed absolute error. The construction adds spatial padding and then cuts inside it. It does NOT assert energy decrease for heat with fixed nonconstant Dirichlet data.

Take a near-minimizer Phi on [0,N] with Phi(0)=0, Phi(N)=U and ||D Phi||_4<=R. All measures below are dx times normalized dy. The existing horizon theorem supplies N and a uniform R, e.g. R^4=(2M+1)/gamma for near-minimizers of finite-horizon value with error below 1, when p_N<=M. Here M may be chosen from the full-endpoint unit entry E(x,y)=x U(y), M=120[|B|^2||DE||_2^2+||DE||_4^4]. Its reflection returns U to zero with the same norm budget; this proves p_N<=M for N>=1 and the displayed R bound for near-minimizers with error <=1. This full-endpoint choice also handles nonzero means.

## Geometry and fixed reference

Choose 0<delta<=1. On the x-circle represented by [-2delta,N+2delta+1], period P=N+4delta+1, define V by:
- 0 on [-2delta,0];
- Phi on [0,N];
- U on [N,N+2delta];
- r(x-N-2delta)U on [N+2delta,N+2delta+1], where r is a fixed polynomial decreasing from 1 to 0 with its first three derivatives zero at both ends.

Define the known C3 periodic W identically outside [0,N], and by a polynomial increasing cutoff times U inside [0,N], flat through order 3 at both ends. Then w=V-W and Dw are supported in [0,N], with zero traces there. Explicitly h(t)=35t^4-84t^5+70t^6-20t^7, with h'(t)=140t^3(1-t)^3, supplies the increasing cutoff h(x/N), and r=1-h. Its first three derivatives vanish at the appropriate endpoint joins. Set

Rtot^4=R^4+2delta||U_y||_4^4+||D(rU)||_4^4,
Rw=R+||DW||_(L4([0,N]xT)),
Lw=N^(3/4)Rw.

Then ||DV||_4<=Rtot, ||Dw||_1<=Lw and ||w||_1<=N Lw. No concentration estimate is involved.

Let I=[-delta,N+delta], length L=N+2delta, and C be its complement in the circle, length 1+2delta. Every point of C has circular x-distance at least delta from the support of w.

## Explicit heat leakage

Let H_s be periodic heat with d1=4897/5000 and d2=5103/5000. Put

q(s,delta,P)=(4 pi d1 s)^(-1/2) [ exp(-delta^2/(4d1s)) + 2 sum_(k>=1) exp(-max(delta,(k-1/2)P)^2/(4d1s)) ] [1+sqrt(pi/(d2s))].

This is an explicit upper bound for the product heat kernel whenever circular x-distance >=delta. The y kernel is with respect to normalized dy. The sum has elementary Gaussian integral tail bounds. q tends to zero as s decreases to zero for fixed delta,P.

Let A0=|| (d1 W_xx+d2 W_yy) ||_infinity and A1=||D(d1 W_xx+d2 W_yy)||_infinity. These are computably bounded from the known polynomial/Fourier W. On C,

|H_s V-W|<=e0:=s A0+q N Lw,
|D H_s V-DW|<=e1:=s A1+q Lw.

This follows by semigroup contraction on the smooth reference and off-diagonal convolution on w,Dw. It also holds at both boundary circles of I.

## Exterior subtraction: the decisive inequality

Global Heat18 gives J_circle(H_s V)<=J_circle(V). Since V=W on C, subtracting the exterior action gives

J_I(H_s V)<=J_[0,N](Phi)+delta jU+Eext,

where jU=E_y f_B((0|U_y)) and

Cpad=120[|B|^2||U_y||_2^2+||U_y||_4^4],
Eext=(1+2delta) 180 e1 [|B|^2(K+e1)+|B|(K+e1)^2+(K+e1)^3],
K=||DW||_(L-infinity(C)).

Indeed J_I(V)=J(Phi)+delta jU and |jU|<=Cpad. The *entire* return energy cancels algebraically; it is not assumed small or positive. Only its smoothing perturbation on the separated exterior is bounded.

## Exact endpoint repair without a trace constant

Write a(y)=H_s V(-delta,y), b(y)=H_s V(N+delta,y), and theta=(x+delta)/L. Define

Psi=H_s V -(1-theta)a + theta(U-b) on I.

It has exact traces 0,U. Both endpoint value errors are <=e0 and y-derivative errors <=e1, so the correction h obeys

||Dh||_4<=h0:=L^(1/4)(2e0/L+e1).

For a domain of measure L define

DIF_L(A,h)=180h[ |B|^2 L^(1/2)(A+h)+|B| L^(1/4)(A+h)^2+(A+h)^3 ].

The source polynomial derivative bound and Holder imply action difference <=DIF_L(A,h) when original gradient L4 norm <=A and perturbation norm <=h. Consequently

J(Psi)<=J(Phi)+delta Cpad+Eext+DIF_L(Rtot,h0).

Choose delta first to control padding, then s sufficiently small to control the last two terms. All choices terminate using known inputs.

## Fourier truncation and finite parameter box

On the full P by 2pi torus, write xi_kn=(2pi k/P,n), lambda_kn=d1(2pi k/P)^2+d2 n^2. Since V has the zero trace on a whole left padding strip, elementary x-Poincare gives

|Vhat_kn| <= (1/P)||V||_1 <= P^(3/4)Rtot=:C0.

The vector coefficient norm bound suffices; a componentwise real/imaginary box of any computed rational radius Cbar>=C0 contains it (impose conjugate symmetry so the map is real). Set Q_K to the Fourier sum of H_s V over |k|,|n|<=K. Define

T0=C0 sum_outside exp(-s lambda_kn),
T1=C0 sum_outside (|2pi k/P|+|n|) exp(-s lambda_kn).

These are computable Gaussian series tails tending to zero. Then ||Q_K-H_s V||_infinity<=T0 and ||D Q_K-D H_s V||_infinity<=T1. Apply the same endpoint repair operator to Q_K. The repaired profiles differ in gradient L4 norm by at most

t0=L^(1/4)(2T1+2T0/L).

Hence the final repaired Fourier profile has action <=J(Phi)+

spatial_error:=delta Cpad+Eext+DIF_L(Rtot,h0)+DIF_L(Rtot+h0,t0).

Choose K to make the final term small. This uniform error does not require Fourier decay of the unknown competitor before heat.

Let F_K be ALL real two-vector Fourier polynomials with these frequencies and real/imaginary coefficients in [-Cbar,Cbar], repaired by the displayed affine endpoint operator with fixed U. It is a finite-dimensional compact family of actual W1,4 paths with exact endpoints. Its minimum m_K satisfies

p_B(U) <= m_K <= p_B^N(U)+spatial_error.

The right inequality follows by applying the uniform construction to arbitrary near-minimizers and taking their approximation errors to zero; the left follows simply from admissibility at duration L. The use of a slightly longer duration is deliberate and harmless for unrestricted storage. This is NOT necessarily an error theorem for p_B^N at the unchanged exact horizon.

Explicit basis convention: choose one representative of each nonzero conjugate pair (k,n),(-k,-n), and use 2cos(xi_kn dot (x,y)) and -2sin(xi_kn dot (x,y)) in each output coordinate. Their coefficients are respectively Re(Vhat_kn) and Im(Vhat_kn), each bounded by Cbar. Use the constant basis separately. If ordinary unscaled cos/sin is used instead, the radius must be 2Cbar. The objective on this real coefficient box is a quartic polynomial, with computable coefficients obtained by integrating products of known trigonometric and affine functions. A rational finite grid and an explicit polynomial gradient bound give certified global lower and upper bounds to m_K to any requested accuracy; finite-dimensional existence here is just compactness of a box, not an assumed PDE minimizer. With horizon gap hN and grid error hG, the resulting interval for p is [grid_lower-hN-spatial_error, grid_upper], of width at most hN+spatial_error+hG.

## Explicit global-grid certificate

Write the repaired family as Psi_theta=theta_x U+sum_j theta_j beta_tilde_j, where theta_x=(x+delta)/L, beta_tilde_j is the endpoint-repaired Fourier basis, and |theta_j|<=Cbar under the chosen coefficient normalization. Bound B_j>=||D beta_tilde_j||_4 directly from elementary trigonometric derivatives; let S=sum_j B_j and A_box=||D(theta_x U)||_4+Cbar S. Then every partial derivative of the action is at most

180 B_j[|B|^2 L^(1/2)A_box+|B| L^(1/4)A_box^2+A_box^3].

A finite grid covering the box within coefficientwise distance rho therefore has grid gap at most

gerr=180 rho S[|B|^2 L^(1/2)A_box+|B| L^(1/4)A_box^2+A_box^3].

If every grid objective is interval-evaluated and gminus=min lower endpoints, gplus=min upper endpoints, then m_K lies in [gminus-gerr,gplus]. Consequently p lies in [gminus-gerr-hN-spatial_error,gplus]. The finite grid may be enormous, but termination and both interval directions are explicit. Uniform interval precision makes gplus-gminus as small as requested.

## Scope and remaining checks

The result is effective, not computationally practical: P, 1/s, K, and the grid can be enormous. Endpoint critical tails can be handled separately by the established bounded-ball Lipschitz storage theorem. Without a supplied effective critical-tail approximation of U, this does not contradict the finite-observation obstruction.

Mean-zero U is not necessary for this fixed-endpoint proof. No quotient endpoint or quasi-periodic heat argument is needed. The stronger horizon bound for free endpoint means could be added separately, but is not presently a premise.

The local analytic Heat18 proof was read at ../critical_storage_construction/G_QUASICONVEXITY_PROOF.md, especially §§3–4. It explicitly covers G itself and torus heat, though its header has an older repository pin. The independent same-team Fraction-only reconstruction in ../heat_monotonicity_verification/PROOFCHECK.md verifies all 210 identity coefficients, Q=C S C^T, rank 18, closedness, primitive, and all 18 positive LDL pivots. The byte-hash difference is a terminal-newline difference, as reconciled there. The present spatial deduction does not execute downloaded code, and external review remains unknown. The certified exact diffusion ratio is used throughout; arbitrary separately chosen diffusivities are not asserted.


The separate same-team audit is ../storage_spatial_audit/INDEPENDENT_HEAT_AUDIT.md. It checks the kernel normalization, all displayed error bounds, exterior cancellation, coefficient radius, and the directions of the final two-sided interval. It identifies no substantive obstruction.

## Terminating selection procedure

Given target interval width epsilon>0:
1. Obtain a certified horizon gap hN<epsilon/4 using FINITE_HORIZON_STORAGE.md and take N>=1. Use an independently known full-endpoint entry budget to set R for finite-horizon near-minimizers.
2. Choose rational delta in (0,1] with delta Cpad<epsilon/16 (if Cpad=0 any sufficiently small rational delta works). Construct W and all displayed budgets.
3. Search dyadic s decreasing to zero until Eext+DIF_L(Rtot,h0)<epsilon/8, using outward numerical enclosures of the Gaussian sums. Termination follows from q(s,delta,P)->0 and e0,e1->0.
4. Search integer K increasing until DIF_L(Rtot+h0,t0)<epsilon/16. Gaussian tails give a terminating certified test. Then spatial_error<epsilon/4.
5. Form the finite repaired coefficient box with outward rational radius. Select mesh rho making gerr<epsilon/4 and evaluate every grid objective with interval width <epsilon/4. Return [gminus-gerr-hN-spatial_error,gplus]. Its width is <epsilon.

All strict tests can use harmless slack and monotonically tightened certified upper bounds. No minimizer identification, tail measurement, convexity assumption, or variational solver oracle occurs. A search so large that it is infeasible in practice still satisfies the finite termination theorem; no practical runtime estimate is claimed.

## Concrete cost instantiation

`RESOURCE_RECEIPT.md` instantiates the construction at U=(cos y,sin y), B=0, target enclosure width 0.01. Its newly written Fraction-only checker passes 33 inequalities. A sufficient selection uses N=10^22, delta=10^-6, s=10^-40, K=10^44 and coefficient-grid spacing 10^-640. The real dimension is approximately 8×10^88, with sufficient grid cardinality having base-10 logarithm less than approximately 5.296×10^91 (the exact bound is in the receipt). No grid objectives or storage values were computed. This explicit exhaustive construction is overwhelmingly impractical; its cost is not a lower bound on other algorithms.
