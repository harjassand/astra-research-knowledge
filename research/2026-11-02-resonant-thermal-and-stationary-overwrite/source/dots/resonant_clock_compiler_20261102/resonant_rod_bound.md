# Resonant path-clock: exact resolvents and uniform thermal local potential

2026-11-02. This establishes the analytic replacement for the large-detuning rod bound, conditional only on the exact pair-factor/gas representation already proved in `native_thermal_interactions_20261101/root_rod_audit.md`. No claim about physical implementation or novelty.

## Model and identities

Let K>=3, n=K-1, A=t(2I-T_n), v=e_1+e_n, and g=eta*t/K. Only the two links incident on clock vacuum 0 have strength g; all path-internal links have strength t. Onsite energy is 2t. Define

    mu=2t[1-cos(pi/K)]=4t sin²(pi/(2K)),
    4t/K² <= mu <= pi²t/K².

The absolute ordinary-excursion density and winding subdensity are

    rho(l)=g² v^T exp(-Al)v,
    rho_w(l)=2g² [exp(-Al)]_(1,n).

The inverse is G_ij=min(i,j)[K-max(i,j)]/(tK). In particular A^{-1}v=1/t times the all-ones vector, so EXACTLY

    M0=integral rho=2g²/t,
    M1=integral l*rho=g²(K-1)/t²,
    J0=integral rho_w=2g²/(tK)=2eta²t/K³,
    integral l*rho_w / J0=(K²-1)/(6t).

The last identity follows by summing i(K-i)/(t²K²) for (A^{-2})_(1,n). These are infinite-time integrals, not ground-space projections.

## Tilted bounds

For 0<=b<=mu/2, spectral calculus applied to v gives

    M0(b)=g²v^T(A-bI)^{-1}v <=4g²/t,
    M1(b)=g²v^T(A-bI)^{-2}v <=4g²(K-1)/t².

The off-diagonal inverse entry has constant cofactor t^(n-1). Consequently

    J(b)/J0 = [(A-bI)^{-1}]_(1,n)/G_(1,n)
             = det A / det(A-bI)
             = product_j (1-b/lambda_j)^(-1).

Here Tr A^{-1}=(K²-1)/(6t), whence

    log[J(b)/J0] <= b(K²-1)/[6t(1-b/mu)]
                  <= b(K²-1)/(3t).

No invalid entrywise inference from a PSD inequality is used. The determinant identity is also a direct proof that the marked winding-duration moment generating function has a volume-independent relative bound.

A convenient tail bound uses c=t/K²<=mu/4:

    integral_beta^infty rho_w / J0
       <= exp(2/9-beta*t/K²).

Indeed log[J(c)/J0] <= (1/6)/(1-1/4)=2/9.

## Explicit KP hypotheses

Let D>=1 count the clock itself and every overlapping clock; introduce any desired spatial exponential weight kappa>=0 and Dbar=D exp(kappa). Write x=Dbar eta². Choose

    x<=1/64,
    a0=64 Dbar g²K/t²=64x/K,
    b=32 Dbar g²/t=32x*t/K².

Then a0<=1/3<log 2 and b<=mu/2 (in fact <=mu/8). Charge ordinary rods by a0+b*l and full-circle wraps by a0+b*beta. The exact wrap activity after length tilt is

    W(b)=Tr exp[-beta(A-bI)]
        <=(K-1) exp[-beta(mu-b)].

Require the explicit thermal condition

    (K-1) exp[-beta(mu-b)] <= eta²/K.                 (T)

Pair Mayer functions have modulus <=2 and vanish unless rods overlap in time on equal or interacting clocks. The overlap-start measure of an ordinary rod l with another l' is at most l+l'; wrap overlap is the full circle. Hence the ordinary-root KP integral is at most

    2Dbar exp(a0)[l M0(b)+M1(b)+W(b)]
    <=16 Dbar(g²/t)l+20 Dbar g²K/t²
    <= b*l+a0.

For a wrap root, replace l by beta; the same bound applies (and overestimates its ordinary overlap). Thus the complex/signed soft-interaction KP theorem applies uniformly in volume and all flux assignments. It treats ALL thermal histories, including never-vacuum histories. Condition (T) is not optional and is not a global-vacuum-probability condition.

## Local free-energy remainder

The exact prefix gauge leaves individual winding fluxes s_a and flux-independent pairwise clock-history signs, including shared X/Z clocks. The same marked-winding argument as in the earlier audit therefore gives

    F_beta(s)=c_beta-J0 sum_a s_a + sum_{nonempty B} r_B product_{a in B}s_a,

    sup_a sum_{B contains a} exp[kappa diam(B)] |r_B| / J0
       <= exp(2/9-beta*t/K²) + exp[a0+b(K²-1)/(3t)]-1
       <= exp(2/9-beta*t/K²) + exp(32x)-1.            (R)

The first term is the omitted tail of the exact single winding rod. The second bounds all connected clusters containing a marked winding rod beyond that singleton, since their rooted absolute activity is bounded by exp(a0+b*l)-1. All backtracking inside a winding excursion is already included in J0, so there is NO additional 'higher internal-path order' error. Wrap-containing clusters are included through KP. Flux-independent clusters are absorbed into c_beta. The flux cube may be formal; restriction to actual allowed syndrome sectors is subsequent.

Thus choose x small for a desired relative margin and beta large enough for (T), the tail, AND the code's independent cold condition beta*J0>=B_c. In particular beta*t/K²=(beta*J0)K/(2eta²), so cold scaling helps, not hurts, the thermal bounds. One must not hold beta*t fixed while taking eta small.

## Baseline operator gap despite overlap

For a single clock a, its g=0 Hamiltonian H_a consists of 2t Q_a and path hops carrying single-site Pauli unitaries. A unitary controlled on its path coordinate gauges its internal chain to A on the nonzero clock subspace (and zero on vacuum); it may act on data but is valid as an operator inequality on the FULL shared Hilbert space. Therefore H_a>=mu Q_a independently of other clocks. Adding these inequalities yields sum_a H_a>=mu sum_a Q_a without requiring [H_a,H_b]=0. Each Q_a commutes with each baseline H_b because internal hops preserve vacuum/nonvacuum occupation. The all-clock-vacuum data space is the baseline kernel, and the gap above it is at least mu. Overlap does not invalidate this argument.

## Corollary: heterogeneous clock lengths without common clock-state padding

Let each clock have K_a=max(3,weight(S_a)) states, with M=max_a K_a. Small checks may use identity factors to reach 3, but are NOT padded with states to M. For a desired common effective coefficient J>0 choose

    t_a=J M² K_a/(2eta²),  g_a=eta*t_a/M.

Then J_a=2g_a²/(t_a K_a)=J exactly. All moments and inverse formulas above apply separately, giving

    M0,a=J K_a<=JM,
    M1,a=eta²(K_a-1)/M²<=eta²/M,
    mu_a>=4t_a/K_a²>=2JM/eta².

Use x=Dbar eta²<=1/64 and the COMMON charges

    a0=64Dbar eta²/M,  b=16Dbar JM.

They satisfy a0<=1/3 and b/mu_a<=8x<=1/8 for every species. Consequently tilted moments obey M0,a(b)<=2JM and M1,a(b)<=4eta²/M. Impose

    (M-1) exp[-beta(2JM/eta²-b)]<=eta²/M.             (T_het)

Every species' tilted wrap activity is then <=eta²/M. Regardless of which lengths occur among a clock's at most D interacting neighbors, its KP integral is bounded by

    8Dbar JM*l+20Dbar eta²/M <= b*l+a0.

This uses species-uniform bounds and therefore does not assume neighbors have equal lengths. For a marked winding rod of species a,

    log[J_a(b)/J] <= b(K_a²-1)/(3t_a)
                    <=(32/3)x K_a/M <=(32/3)x.

Together with a0<=64x/3 this gives the same bound exp(32x)-1. The tail tilt c_a=t_a/K_a² has log moment ratio <=2/9 and c_a>=JM/(2eta²). Hence

    sup_a sum_{B contains a} exp[kappa diam(B)] |r_B| / J
       <=exp[2/9-beta*JM/(2eta²)]+exp(32x)-1.        (R_het)

The exact thermal free energy is c_beta-J sum_a s_a+R on the formal flux cube, then restricted to physical syndromes. This is a new choice of the physical clock Hamiltonian; it does not by itself prove any separate transfer or dynamical certificate.

Resource accounting: clock dimension sum is sum_a K_a, not M times the number of checks. The number of clock edges is likewise sum_a K_a, and the peak internal coefficient is max_a t_a=J M³/(2eta²). Be precise about the word 'strength': sum_a t_a=[JM²/(2eta²)]sum_a K_a, but the actual sum of individual edge coefficients is

    sum_a [(K_a-2)t_a+2g_a]
      = [JM²/(2eta²)] sum_a K_a(K_a-2+2eta/M).

Thus its exact dependence involves sum K_a², although the upper bound (t_max+2g_max)sum K_a is linear in the actual state-count at a fixed maximum-length budget. The onsite projector-coefficient sum is sum_a 2t_a(K_a-1). No generic coherent-simulation-padding claim is made here.
