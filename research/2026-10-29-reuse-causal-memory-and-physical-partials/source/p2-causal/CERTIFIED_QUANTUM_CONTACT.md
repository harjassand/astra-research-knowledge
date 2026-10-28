# A fully enclosed prediction for the concurrent quantum contact

29 October 2026, Australia/Brisbane. Author: fault_locality. This is a
validated numerical action construction. Independent review is separate;
the word certified refers to the analytic enclosures described here.

## 1. Completed result

For the exact infinite-dimensional Hamiltonian

    H=(pi/2) i(b^dagger a-a^dagger b)
        +(1/8) sigma_x sin[(a+a^dagger)/2]
        +(1/8) sigma_y sin[i(a^dagger-a)/2],              (1)

acting for time one, with source I/2 and both oscillators in vacuum, the
executed calculation encloses the exact source expectation in

    0.009748778824845387583321769614292341
       <= <sigma_z> <=
    0.009748846972041638565154374216800806.              (2)

The two full sine terms are on throughout the passive contact. This is an
infinite-model prediction, not a floating-point cutoff comparison. The
finite numerical contribution to the Z allowance is below 6.32e-34; the
roughly 3.41e-8 half-width is dominated by the explicit infinite-to-finite
Galerkin bound. No statistical samples or measured parameters are used.

Equation (2) certifies the nonunital source operation: a classical mixture
of initially independent Hamiltonian trajectories would preserve I/2.
It gives no hardware performance or logical computing advantage claim.
The input, controls and Hamiltonian in (1) are stipulated mathematical
resources. Physical calibration, delivery, losses and readout uncertainty
remain separate ledgers.

## 2. Finite restriction with an infinite-model allowance

Let P project onto total oscillator number N_a+N_b<M, with M=24. The
source tensor this space has dimension

    D=2*M*(M+1)/2=600.

The matrix H_M is the EXACT restriction P H P, not a matrix sine of a
truncated quadrature. The passive term commutes with total number.

The bounded interaction has total Weyl variation action A=1/4 and each
Weyl displacement has one-particle norm kappa=1/2. Initial total number is
zero. Each order-k Dyson word is a displacement of norm at most k*kappa,
times source contractions and a scalar phase. A displaced vacuum has a
Poisson number generating function. Thus, for every z>1,

    ||1_(N>=M) D(beta)|0>||
      <=min(1,z^(-M/2) exp[|beta|^2(z-1)/2]).            (3)

For each k with (k*kappa)^2<M the code chooses the rational Chernoff point
z=M/(k*kappa)^2; otherwise it uses the unit bound. All exponentials are
enclosed from above by exact rational positive series and an explicit
geometric remainder. Summing through K=14 gives

    T=sum_(k=1)^K A^k/k! t_k
      + A^(K+1)/(K+1)!/[1-A/(K+2)].                    (4)

The k=0 term is exactly zero. Formula (4) bounds the full exact evolution's
high-number vector component uniformly throughout the contact. The
projected equation of motion has leakage force P V Q U. The finite
propagator is unitary on P, so variation of constants gives

    ||(U(1)-U_M(1))psi|| <=(1+A)T=:epsilon_cut.          (5)

This is the m=0 case of `..producer-workspace/FINITE_CONTACT_COMPILER.md`, also derived
directly above for this witness. Because both exact outputs in (5) are
normalized, their sigma_z expectations differ by at most 2 epsilon_cut.
It applies to each of the two source basis inputs and hence their equal
mixture. No occupation truncation of the physical initial vacuum is needed.

## 3. Enclosing every matrix entry

Use the basis |s,a,b> with source s outermost, b next, and a=0,...,M-b-1.
Put ell=min(m,n), r=max(m,n), delta=r-ell. Normal ordering of the Weyl
operator gives

    <m|D(beta)|n>=exp(-|beta|^2/2) sqrt(ell!/r!)
        L_ell^delta(|beta|^2)
        * beta^(m-n)              if m>=n,
        * (-conjugate(beta))^(n-m) if m<n.             (6)

The finite polynomial is computed exactly as

    L_ell^delta(x)=sum_(j=0)^ell
                    (-1)^j binom(ell+delta,ell-j) x^j/j!.

Equation (6) follows by expanding the normal-ordered annihilation and
creation exponentials and extracting the finite matrix coefficient. It
does not approximate the full nonpolynomial interaction.

For odd delta define

    base=exp(-kappa^2/2) sqrt(ell!/r!)
                         kappa^delta L_ell^delta(kappa^2).

Then sin(kappa X)_(m,n)=(-1)^((delta-1)/2)*base is real, whereas
sin(kappa P)_(m,n)=i*sign(m-n)*base. Even delta gives zero. The upper
source-off-diagonal block therefore has exact real entries

    H_(0,m;1,n)=(1/8)*base*
                      [(-1)^((delta-1)/2)+sign(m-n)].  (7)

The lower block is its transpose. The passive edges have imaginary
coefficient i*(pi/2)*sqrt[a*(b+1)] and their conjugate reverses.

The code encloses exp(-1/8) by 100 terms of its alternating rational
series. It encloses pi using Machin's identity and 100-term alternating
arctangent series at 1/5 and 1/239. Every square root is enclosed on a
2^-192 grid using integer square roots and exact squared comparisons.
Laguerre coefficients and products are rational intervals.

Each interval is rounded at its midpoint to the nearest multiple of
2^-128. The reverse entry is copied as an exact conjugate, so the resulting
dyadic matrix H_d is EXACTLY Hermitian. Each exact entry's distance from
its dyadic center is bounded by the larger endpoint distance. A maximum
row-sum bound on these errors gives

    ||H_M-H_d|| <= delta_H.                            (8)

All interval endpoint arithmetic is exact Fraction arithmetic. The matrix
and its operator error allowance are saved in
`quantum_contact_dyadic_matrix.json`. Unitary Duhamel over unit time
charges delta_H once, without an exponential of the Hamiltonian norm.

## 4. Scaled Taylor action with all roundoff included

The true target for this stage is exp(-i H_d)|s,0,0>, s=0,1. Let S=2^128.
Every complex vector coordinate is stored as a pair of arbitrary-precision
integers divided by S. Sparse matrix-vector products use EXACT integer
multiplication and addition. The only numerical rounding is an explicitly
implemented nearest-integer division.

Let B be the maximum row sum of |Re H_d|+|Im H_d|. Hermiticity gives
||H_d||<=B. Choose n_steps as the smallest power of two at least B; the
executed value is 64. Thus L=B/n_steps<=1. At each time step the code
evaluates the degree-32 Taylor action using the recurrence

    t_0=v,
    t_k=round_grid[(-i H_d)/(n_steps*k) t_(k-1)],
    v_next=sum_(k=0)^32 t_k.                           (9)

The sums in (9) are exact integer sums on the same grid. Every rounded
complex vector has 2D real coordinates; rounding each by at most 1/(2S)
gives a Euclidean perturbation at most

    r=ceil(sqrt(2D))/(2S).

If e_k is the error in Taylor term k due to previous rounding, then

    e_k <=(L/k)e_(k-1)+r,  e_0=0.

Since L<=1, the elementary factorial majorant yields e_k<=exp(L)r<3r.
The error in the summed degree-32 action is therefore at most 3*32*r.

For a HERMITIAN matrix, the Taylor remainder of its unitary exponential
satisfies

    ||exp(-i H_d/n_steps)-P_32(-i H_d/n_steps)||
       <= L^33/33! = eta.                             (10)

This follows from the integral Taylor remainder, whose exponential factor
is unitary; the usual generic exp(L) norm factor is unnecessary.

At the start of EVERY step, the code checks the current vector norm <=2
by the exact integer inequality sum_i(Re_i^2+Im_i^2)<=4S^2. Thus a step's
total action error is at most 2 eta+3*32*r. Comparing each step against
the exact UNITARY step propagator and telescoping gives

    epsilon_action <= n_steps*(2 eta+3*32*r).           (11)

There is no exp(B) amplification over the full computation. The finite
solver's vector allowance is

    epsilon_solver=delta_H+epsilon_action.             (12)

The two propagated columns, their exact grid numerators, and all step-norm
checks are saved in `quantum_contact_fixedpoint_vectors.json`. No binary64
dynamics, matrix exponential, numerical eigenvalue calculation, or
quadrature is used in this pipeline.

## 5. Turning vectors into an observable interval

The source starts in I/2, so the exact grid prediction is the rational

    Z_grid=(1/2) sum_(s=0,1) sum_i z_i |v_(s,i)|^2,
    z_i=+1 for source 0 and -1 for source 1.            (13)

The approximate vectors need not be normalized. For a normalized exact
vector u and an approximate v within epsilon_solver,

    |<u,Z u>-<v,Z v>| <= epsilon_solver*(2+epsilon_solver),

because ||Z||=1 and ||v||<=1+epsilon_solver. Averaging the two columns
does not enlarge this bound. Add the independent infinite-model allowance
2 epsilon_cut to obtain the total interval half-width

    e_Z=2 epsilon_cut+epsilon_solver*(2+epsilon_solver).

The two endpoints Z_grid +/- e_Z are exact rational numbers in the JSON.
Displayed lower endpoints are rounded downward and upper endpoints upward.
Equation (2) therefore encloses the declared infinite model, including
both truncation and finite numerical errors.

## 6. Execution and limits

The completed run used dimension 600, two propagated columns, 64 time
steps, degree 32 and 4096 sparse matrix-vector actions. Exact matrix
nonzero counts, artifact hashes and wall time are in the result ledger.
Runtime is informational and is not used by any mathematical certificate.
The code uses only the Python standard library and arbitrary-precision
integers/Fractions; no package installation was required.

The output is one complete source-observable prediction for one contact,
not a fully enclosed numerical transfer matrix for every input, a
100-contact certified solver, an estimated device noise rate, or a proof
of computational advantage. The finite matrix H_d defines a unitary in
exact mathematics; rounded action columns themselves are not asserted to
be an exact CPTP channel. The observable error bound avoids needing that
assertion. The previous binary64 transfer diagnostic remains useful at
its explicitly different numerical scope.

The useful new bridge is constructive: the full infinite sine/contact
model now produces an actual, finite, auditable numerical prediction with
separate representation and solver enclosures. Ordinary cutoff convergence
alone was not used as a certificate. Existing source-only abelian machinery
is retained where its stronger conventional reduction applies.
