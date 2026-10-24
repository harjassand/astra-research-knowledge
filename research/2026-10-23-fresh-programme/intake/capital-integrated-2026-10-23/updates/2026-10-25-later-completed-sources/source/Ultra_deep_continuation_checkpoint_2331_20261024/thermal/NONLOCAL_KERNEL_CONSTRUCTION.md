# Positive nonlocal kernels can flatten the full ballistic spectrum

This is a new owned construction prompted by checking the interaction-length boundary in ACOUSTIC_RANGE_THEOREM.md. It uses positive springs and retains EVERY propagating crossing. Unlike the single skip-link counterexample there, a distributed positive interaction kernel really does send total intrinsic conductance to zero in the ideal point-mass model at fixed total point mass and fixed long-wavelength stiffness. Its interaction reach grows without bound; connector dynamics and extension range are not granted as physical operations.

## 1. Exact positive network

Put one scalar point mass M>0 in every cell. For an integer N>=2, connect each mass to its n-th neighbour with spring

kappa_n=c_N(N-n), n=1,...,N-1,
c_N=12K/[N^2(N^2-1)],
K>0.

All couplings are positive. The nearest coupling is positive, so the periodic graph is connected. The relaxed long-wavelength stiffness is exactly

K_eff=sum_(n=1)^(N-1) n^2 kappa_n=K,

because sum n^2(N-n)=N^2(N^2-1)/12. The total cross-spring stiffness is

K_aff=sum kappa_n=6K/[N(N+1)].

There are no within-cell internal coordinates. Thus any range condition only on internal coordinates relative to one cell's reference is vacuous here. Interaction shift N-1 and the motion across intercell connectors must be counted separately.

The exact Bloch dispersion is

omega_N(q)^2=(2/M)sum_n kappa_n[1-cos(nq)]
 =(c_N/M)[N^2-D_N(q)^2],
D_N(q)=sin(Nq/2)/sin(q/2).

The identity follows from the positive triangular Fourier/Fejer kernel. At q=0 interpret D_N=N by continuity. The acoustic slope remains sqrt(K/M), whereas the exact maximum frequency is

Omega_N=N sqrt(c_N/M)
       =sqrt[12K/(M(N^2-1))].

Thus the linear acoustic cone occupies a shrinking wave-number interval; almost all the Brillouin zone becomes a nearly flat low-frequency plateau. A band-union argument alone would be insufficient, because the plateau has many small oscillations and hence multiple propagating crossings. Section2 bounds their COMPLETE contribution.

## 2. A rigorous total-variation bound counts all crossings

For an even scalar dispersion, the complete classical intrinsic channel bandwidth is

W_N=integral N_ch(omega)domega
   =(1/2)integral_(-pi)^pi |omega_N'(q)|dq
   =TV_(0,pi)(omega_N).

The full Bose conductance obeys0<J_N<=W_N since0<g_theta<=1. Write

u_N(q)=D_N(q)/N,
omega_N=Omega_N sqrt(1-u_N^2).

On the first interval0<q<q0=2pi/N, u_N decreases from1 to0. To verify monotonicity, its logarithmic derivative has the sign of x cot x-(x/N)cot(x/N), where x=Nq/2 in(0,pi); the function x cot x is strictly decreasing there. Hence the first interval contributes exactly Omega_N to the total variation.

For q0<=q<=pi, sin(q/2)>=sin(pi/N) and N sin(pi/N)>=2, giving |u_N|<=1/2. Therefore

|omega_N'|<=2Omega_N |u_N u_N'|,
|u_N u_N'|
 <=1/[2N sin^2(q/2)]+1/[2N^2 sin^3(q/2)].

The two integrals satisfy

integral_(q0)^pi dq/[2N sin^2(q/2)]
 =cot(pi/N)/N<=1/pi,

integral_(q0)^pi dq/[2N^2 sin^3(q/2)]
 <=pi/16.

For the second estimate use sin(q/2)>=q/pi and integrate q^(-3). For N=2 the remaining interval is empty, so the bounds still hold. Consequently

Omega_N<=W_N
 <=[1+2/pi+pi/8]Omega_N.

This is a bound on all propagating-channel variation, not on a band union counted only once. In particular

J_N(theta)<= [1+2/pi+pi/8] sqrt[12K/(M(N^2-1))]
 ->0 at EVERY fixed positive theta.

If theta also tends to0, taking N theta tending to infinity gives J_N/J_Q tending to0 by the same upper bound, while the rigid chain with mass M and spring K still has J_rigid/J_Q tending to1. Every finite N network is connected, positive and has exact K_eff=K; there is no hidden negative spring or spectral truncation in the construction.

## 3. The physical operations that are not free

This does not contradict ACOUSTIC_RANGE_THEOREM.md or its quantum corollary. K_aff tends to0 and interaction reach tends to infinity, so their fixed-K_aff or bounded-reach/fixed-K_eff hypotheses do not apply. It is a genuine mathematical counterexample to imposing only K_eff,M and within-cell relative range while allowing unpriced positive interactions of unbounded length.

An actual connector range is expensive even before fabrication. For the nearest-neighbour relative observable Y=x_(l+1)-x_l, the total quantum equilibrium variance obeys

Var(Y)>= (1/(2pi))integral_(-pi)^pi
  [4sin^2(q/2)/M] [hbar/(2omega_N(q))]dq
 >=hbar/(M Omega_N),

since the average of4sin^2(q/2) is2 and omega_N<=Omega_N. At positive T the classical floor similarly gives

Var(Y)>=2k_B T/(M Omega_N^2).

Thus the seemingly empty internal range budget hides intercell relative motion growing at least linearly in N from zero-point motion, and quadratically in N at fixed classical temperature. The ideal construction is not a bounded-extension material. A strain cap relative to a connector's increasing length is a different resource and needs its own physical contract.

Nor can long springs be treated as massless finite-band actuators without acquisition. A uniform axial connector with stiffness kappa_n, length n a and material specific modulus E/rho has mass kappa_n(n a)^2/(E/rho), and its internal mode frequencies scale as the inverse length. The sum of that simple axial mass estimate is K a^2/(E/rho), which stays finite here; one must therefore calculate its distributed modes rather than declare either free physical realization or automatic failure from total connector mass alone. Those extra propagating modes, routing and interfaces are unacquired. They may change the winning design.

The positive point-mass construction is a load-bearing boundary result. A conventional nonlocal lattice receives the same kernel and obtains the same spectrum. No novelty, finite-material advantage or device operation is inferred.
