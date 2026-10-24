# Acoustic transport under a counted equilibrium deformation range

This extends the transport/range construction beyond the scalar rank-one Bloch pencil. Several intercell springs, cross-node links, overlapping bands and nonmonotone branches are admitted. The conclusion concerns intrinsic harmonic ballistic transport and a Gibbs reference-state range bound. It does not optimize a finite specimen's scattering matrix.

The nearest-cell argument was independently derived first. Root then proposed using the average of the intercell phase factors to allow arbitrary finite integer link lengths; that extension is independently verified in Sections2-4. The earlier proofs, first construction and corrections remain unchanged.

## 1. Model, observable and statement

A one-dimensional periodic cell contains any finite number n of positive scalar point masses m_j, with total mass M. Any positive pairwise internal springs are allowed. Each intercell spring e has stiffness kappa_e>0, joins coordinate j_e in cell l to coordinate k_e in cell l+nu_e, and has a nonzero integer shift nu_e. Count every physical spring once per cell. There are finitely many intercell edges, and their maximum shift L=max_e|nu_e| is finite for each network. The infinite periodic graph is connected. No pinning to an external frame is included.

The Bloch elastic energy of a physical displacement x is

E_q(x)=sum_internal kappa_jk |x_j-x_k|^2
      +sum_intercell kappa_e |x_(j_e)-exp(i nu_e q)x_(k_e)|^2.

Mass normalization defines a continuous Hermitian positive matrix D(q), with the uniform translation nullmode at q=0. Put

K_aff=sum_intercell kappa_e>0,
Omega_aff=2sqrt(K_aff/M),
a=max_(q in[-pi,pi]) sqrt(lambda_min(D(q))).

The actual intrinsic channel count N_ch(omega) counts ALL right-moving propagating Bloch modes, including multiplicities from overlapping and nonmonotone bands. It is not replaced by a band-union indicator. Define

J=integral_0^infinity g_theta(omega)N_ch(omega)domega,
g_theta(omega)=[omega/(2theta)/sinh(omega/(2theta))]^2,
theta=k_B T/hbar,
J_Q=pi^2theta/3.

Let x_j(l) be the equilibrium physical displacement of node j in one cell, and fix any one cell coordinate b as reference. Assume in the translation-quotiented harmonic Gibbs state that

Var[x_j(l)-x_b(l)]<=d^2 for every j,

with d>0. These are local relative variances in the thermodynamic Bloch limit. The number of nodes, graph and spring values may vary separately at each T. Define

b_T=min{Omega_aff/4, sqrt[k_B T/(432M d^2)]}.

Then the entire class obeys

a>=b_T,
J>=integral_0^(b_T) g_theta(omega)domega.

Equivalently, writing

Tail(z)=(6/pi^2)integral_z^infinity (u/sinh u)^2du,

we have

(J_Q-J)/J_Q<=Tail[b_T/(2theta)].

For nearest-cell edges only, the constants improve to

b_T=min{Omega_aff/(2sqrt(2)), sqrt[k_B T/(192M d^2)]}.

For same-coordinate nearest-cell rails only, the earlier direct K-weighted argument improves192 to32. Those better constants are not needed for the main structural consequence.

At fixed positive K_aff,M,d, the right-hand side decays as a polynomial times exp[-c/sqrt(T)]. Thus a fixed fractional reduction below one intrinsic acoustic thermal quantum is impossible under this range condition, uniformly over the admitted finite topologies and their retuning. The theorem gives a lower bound: extra channels may make J exceed J_Q.

## 2. A frequency interval must carry at least one channel

The lowest ordered frequency is continuous, equals0 at q=0 and attains a. Therefore its image includes the full interval[0,a]. For almost every omega in(0,a), a Bloch eigenvalue branch crosses omega with nonzero group velocity. Time reversal, D(-q)=D(q)^*, supplies a crossing with opposite velocity; at least one is right-moving.

This statement does not require monotonicity or a rank-one interlacing theorem. A finite Hermitian analytic Bloch matrix has local analytic eigenvalue branches; the exceptional critical/flat-band values have measure zero and do not change the frequency integral. Consequently

N_ch(omega)>=1 for almost every0<omega<a,
J>=integral_0^a g_theta(omega)domega.

All other branches add nonnegative conductance. In particular a small maximum frequency or a narrow union of bands is not by itself a small conductance when many branches cross the same frequency.

## 3. A uniformly soft acoustic branch requires internal deformation

For each q choose a lowest-mode physical eigenvector x(q), normalized by

sum_j m_j |x_j|^2=1.

Its frequency is at most a. Let

X=sum_j m_j x_j/M,
y_j=x_j-X,
W(y)=(1/K_aff)sum_e kappa_e(|y_(j_e)|^2+|y_(k_e)|^2),
F(x)=sum_j m_j|y_j|^2+M W(y).

F is a nonnegative quadratic form in translation-free within-cell coordinates, independent of q. Write E_q^inter for the intercell incidence map with edge norm weighted by kappa_e, and put

f(q)=sum_e kappa_e sin^2(nu_e q/2).

Since the internal energy is nonnegative,

||E_q^inter x||_kappa<=a.

The uniform part X1 has intercell edge norm2sqrt(f(q))|X|. The triangle inequality and the elementary two-endpoint bound give

2sqrt(f(q))|X|
 <=a+||E_q^inter y||_kappa,
||E_q^inter y||_kappa^2
 <=2sum_e kappa_e(|y_(j_e)|^2+|y_(k_e)|^2)
 =2K_aff W(y).

Every nu_e is a nonzero integer, so the normalized Brillouin average of f is K_aff/2, while0<=f<=K_aff. Hence the set A={q:f(q)>=K_aff/4} has normalized measure at least1/3. On that set,

sqrt(M)|X|<=2a/Omega_aff+sqrt(2M W(y)).

Combining this with1=||x||_Mass<=sqrt(M)|X|+||y||_Mass and Cauchy-Schwarz yields

1<=2a/Omega_aff+sqrt[3F(x)].

If a<=Omega_aff/4, it follows that

F(x(q))>=1/12 for q in A.

This is the physical step: a mode whose frequency is small everywhere cannot move all masses nearly together, because the counted intercell springs would then charge a finite uniform-displacement energy on a set of wave numbers with finite measure. It must carry internal relative deformation.

## 4. Gibbs covariance supplies the frequency floor

In a positive mass-normalized mode of frequency omega, the quantum Gibbs position covariance coefficient is

c_T(omega)=hbar/(2omega)coth[hbar omega/(2k_B T)]
         >=k_B T/omega^2.

Let V_F be the local equilibrium expectation of the quadratic form F after subtracting the mean. In each q sector all mode contributions to V_F are nonnegative. Retaining only its lowest mode on A, and using omega_min(q)<=a, gives

V_F>= (1/3)(k_B T/a^2)(1/12)
    =k_B T/(36a^2),

provided a<=Omega_aff/4.

The asserted local range cap gives an independent upper bound. Put r_j=x_j-x_b and r_CM=sum_j(m_j/M)r_j. The L2 triangle inequality gives rms(r_CM)<=d and therefore rms(y_j)=rms(r_j-r_CM)<=2d for every j. Thus

V_F
 <=sum_j m_j(4d^2)
   +(M/K_aff)sum_e kappa_e(4d^2+4d^2)
 =12M d^2.

Combining the two estimates proves a^2>=k_B T/(432M d^2) whenever a<=Omega_aff/4. In the other case the first threshold already bounds a below. This proves Section1.

The argument uses the thermodynamic Brillouin average. A finite periodic ring has a discrete wave-number set whose fraction in A need not equal1/3; the displayed constants are not asserted for every finite ring. One can obtain the Gibbs relative observables as limits of translation-quotiented finite rings. If the relative variance diverges, the finite range cap already fails. No absolute one-dimensional acoustic position variance is assumed finite.

## 5. Better constants for nearest-cell links

When every |nu_e|=1, f(q)=K_aff sin^2(q/2). On the half-zone |q|>=pi/2, f>=K_aff/2. The same triangle argument gives

sqrt(M)|X|<=sqrt(2)a/Omega_aff+sqrt[M W(y)],
1<=sqrt(2)a/Omega_aff+sqrt[2F(x)].

If a<=Omega_aff/(2sqrt(2)), then F>=1/8 there. Its half-zone measure gives

V_F>=k_B T/(16a^2).

Together with V_F<=12M d^2, this gives the stated192 constant. No semidefinite derivative in q is used, so arbitrary cross-node nearest-cell links are included.

For the special self-coordinate rails, D(q)=D0+4sin^2(q/2)B with B positive diagonal in physical coordinates. The lowest branch is monotone on[0,pi], so a=sqrt(lambda_min D(pi)). Using the K-weighted mean X_K=sum_jK_jx_j/K_aff directly gives ||x-X_K1||_Mass>=1/2 on the same half-zone when a<=Omega_aff/(2sqrt(2)). Its Gibbs quadratic expectation is then>=k_B T/(8a^2), while the all-relative cap bounds it by4M d^2. This gives32, consistent with the larger cross-node class.

## 6. Explicit tail and the priced resource order

For z>0,

Tail(z)<= (6/pi^2)
 exp(-2z)(2z^2+2z+1)/(1-exp(-2z))^2.

This follows by bounding1/sinh^2(u)<=4exp(-2u)/(1-exp(-2z))^2 for u>=z and integrating u^2exp(-2u) exactly. Thus at fixed M,d,K_aff the cutoff divided by theta grows at least as T^(-1/2), and the largest permitted deficit below J_Q is superalgebraically small. This is an upper bound on a possible deficit, not its sharp attainable asymptotic.

More generally, in a family for which Omega_aff/theta tends to infinity, a nonzero limiting deficit requires M T d^2 to remain bounded away from zero. QUANTUM_COST_ATTAINABILITY.md supplies an actual one-pendant family with M proportional to1/T, fixed range, all positive finite resources at each T, and nonzero limiting deficit. Therefore the mass/range/temperature RESOURCE ORDER survives in this much larger graph class. The constants and full Pareto frontier are not claimed sharp.

## 7. Static stiffness and interaction length must be distinguished

K_aff counts the sum of physical cross-cell spring stiffnesses. It is the elastic cost of a rigid cell displacement under the phase factors, not in general the relaxed long-wavelength stiffness. For a scalar affine displacement n+xi_j, the relaxed stiffness per cell is

K_eff=min_xi [sum_internal kappa_jk(xi_j-xi_k)^2
             +sum_intercell kappa_e(nu_e+xi_(k_e)-xi_(j_e))^2].

The trial xi=0 gives

K_eff<=sum_e nu_e^2 kappa_e<=L^2 K_aff.

Consequently a fixed positive K_eff and a uniform finite shift bound L0 give the weaker but meaningful threshold Omega_aff>=2sqrt(K_eff/M)/L0. The theorem then applies uniformly with that replacement. Pricing a fixed physical cell length makes L0 a bound on the reach of an interaction; it is not an uncounted operation.

Without a uniform length bound one cannot replace K_aff by K_eff in this proof. An exact connected positive counterexample to that cutoff replacement is one mass M per cell with nearest spring kappa_1=K/L^4 and skip spring kappa_L=(K-kappa_1)/L^2. Then

K_eff=kappa_1+L^2 kappa_L=K,
K_aff=kappa_1+kappa_L tends to0,
omega(q)^2=(4/M)[kappa_1 sin^2(q/2)+kappa_L sin^2(Lq/2)],
max_q omega(q)<=2sqrt(K_aff/M) tends to0.

There is no internal relative coordinate to constrain. Yet this is NOT a thermal-insulation counterexample: it has many right-moving crossings. On each of the L skip-link lobes, the peak is at least2sqrt(kappa_L/M) and the adjacent minima are at most2sqrt(kappa_1/M). Hence the complete classical channel bandwidth is at least

integral N_ch(omega)domega
 >=2L[sqrt(kappa_L)-sqrt(kappa_1)]/sqrt(M)
 ->2sqrt(K/M).

If L theta tends to infinity, the entire narrow frequency range is classical and the same lower bound asymptotically applies to J. Counting its band union only once would falsely turn this conventional long weak skip-link chain into a low-conductance construction. The full channel count prevents that error. This exposes a genuine role of the rank-one monotone hypothesis in the older spectral-indicator optimum, while the range theorem above keeps all crossings.

## 8. Established explanation and scope

The full primary [Rego-Kirczenow 1998 paper](https://arxiv.org/html/cond-mat/9801238), equations1-5 and its contact discussion, was read: velocity and density of states cancel for each transmitted mode, and each gapless ideal acoustic branch gives the familiar low-temperature quantum. This is the strongest conventional explanation, not an excluded competitor. The present bound adds a uniform quantitative statement over networks and tunings that may change with T, using a counted equilibrium deformation range and interaction stiffness/length. The existence or priority of a matching earlier uniform bound remains UNKNOWN.

[Dhar-Roy](https://arxiv.org/html/cond-mat/0606465), equations3.5,3.7 and4.2-4.4, keeps reservoir fluctuation, contact-dressed transport and coordinate covariance as distinct objects. Those exact primary equations were checked. Our Gibbs reference-state range condition is not asserted to describe a finite device carrying heat between different-temperature reservoirs. It must not be inferred merely from an S21 transmission reduction.

The scalar one-link moment theorem needs only a CM-relative variance cap for its earlier O(T) deficit bound. The stronger present conclusion uses ALL-node relative range, so the statements do not have identical hypotheses. Multiple positive links invalidate the scalar indicator synthesis argument but do not, by themselves, remove the equilibrium deformation cost proved here.

External pinning, active or negative stiffness, nonharmonic dynamics, extra physical polarizations, contact reflection and other reservoirs change the contract. No fabricated network, measured thermal effect, material-specific stiffness or device advantage has been acquired. An equally informed conventional passive design receives all the same counted resources and obeys the same theorem.
