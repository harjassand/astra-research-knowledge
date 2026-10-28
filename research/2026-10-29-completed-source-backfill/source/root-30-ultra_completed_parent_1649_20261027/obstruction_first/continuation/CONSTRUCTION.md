# Actual history-kernel compression for long spin-two rings

The uniform spin-two gap is **not proved**. This continuation acquires rigorous
long-ring thermal inputs from a three-vector compression of the actual source
kernel, then proves why its present low-moment tail certificate cannot reach
the cold destination. It does not replace the kernel by a supplied finite-rank
model, count only favourable physical states, or assume a ground-state gap.

## Source and target

Let H_n=sum S_j·S_(j+1), n even, local spin2, and Z_n(b)=Tr exp(−bH_n).
The pinned spin-one paper and Tasaki's October19 arbitrary-spin extension are
prior. Tasaki CT Theorem6.2 needs S(L,b)=Z_(2L)(b)/Z_L(b)^2>=7/8 and
T(2L,b)=Z_(2L)(2b)/Z_(2L)(b)^2>=7/8. The temporal purity is on the double
ring. No such cold pair has been acquired here.

In the source's real integer-spin representation, G_alpha=iS_alpha are real
antisymmetric5x5 matrices. The merged-history kernel k_b(x,y) is the real
trace of the chronologically merged G-word. It defines a compact self-adjoint
operator K_b on the source history space, with an empty-history atom v of
mass1. The source trace identity is Z_n(b)=Tr K_b^n for even n>=4. The following
additional contraction identities follow by fixing both endpoint histories
empty or by closing the two/four-site tensor network:

    <v,K_b^r v> = Z_open,r(b),              r>=1,
    Tr K_b^2 = Tr exp(−2b h_pair),
    Tr K_b^4 = Z_periodic,4(b).                       (1)

The r-site open chain has r−1 bonds. The p2 expression has two parallel bonds;
it is not an assertion about an alternatively defined ordinary two-site ring.
Equation(1) uses the actual local quantum model and its history measure. It is
not inferred from a short moment fit. Parent read the source kernel and
arbitrary-spin extension and independently checked the endpoint interpretation.

## Acquire the open traces exactly

In the unnormalized polynomial spin basis, S+|m>=(2−m)|m+1> and
S−|m>=(2+m)|m−1>. These matrices are diagonally similar to the physical
orthonormal spin representation. Consequently B_r=2H_open,r has integer
entries and real physical eigenvalues. Every magnetization sector is included.
For each k the producer calculates Tr B_r^k modulo several approximately
49-bit primes. Each multiplication is a fixed small-integer sparse B times
a dense matrix with entries in[0,p). Its checked row-sum bound is below2^62;
the trace bound is likewise below2^62. Thus the int64 arithmetic does not
overflow. CRT reconstruction is unique once its modulus exceeds

    2*5^r*[12(r−1)]^degree.

The bound comes from the physical Hermitian spectrum, not the nonorthogonal
matrix norm. Exact traces through degree24,96 and192 were acquired on all
open chains r1–6. All97 shared coefficients of the96/192 runs agree. Exact
spin addition independently gives every coefficient on r1,2,3. These traces
are not variational energies or a sampled low spectrum.

For rational b the complete thermal trace is enclosed by

    sum_(k=0)^d Tr B_r^k*(−b/2)^k/k! ± e_r,
    e_r=5^r exp[x] x^(d+1)/(d+1)!, x=6(r−1)b.         (2)

The bound pays every omitted Taylor coefficient and every physical state.
No fitted tail is used. It becomes useless at sufficiently large b; the code
does not silently extrapolate it. Degree192 refines precision on the same
six-site input, rather than enlarging an exponential physical fixture.

## A counted infinite-dimensional compression

Use J=K_b/5 and the three actual vectors v,Jv,J^2v. Their Gram matrix and
compressed J matrix use only m_r=Z_open,r(b)/5^r, r0–5. The squared residual
also uses m6. A numerical generalized Ritz computation only proposes three
rational decimal coefficients c. They are directly checked using(2):

    d=c* G c>0,
    theta=(c* H c)/d,
    V=(c* H2 c)/d−theta^2.

Thus theta is a Rayleigh quotient of an actual normalized history-space vector
and V is its actual residual variance, each enclosed with intervals.

Let M_p=Tr J^p, p even, be a complete moment from(1). At least one positive
eigenvalue lambda>=theta_lower exists. All other eigenvalues then obey

    |lambda_i| <= r=(M_p−theta_lower^p)^(1/p).        (3)

Only if r<theta_lower is the trial mode certified to be the unique largest
modulus. Every missing mode has been counted **before** a residual theorem is
used. With this separation, the ordinary Temple inequality gives

    theta_lower <= lambda_1
       <=theta_upper+V_upper/(theta_lower−r).         (4)

For every even n>=p the complete tail satisfies

    Z_n(b)/5^n in [lambda_lower^n,
       lambda_upper^n+(M_p−lambda_lower^p)r^(n−p)].    (5)

It follows directly that S(n,b)>=1/(1+t_n)^2, with
t_n=(M_p−lambda_lower^p)r^(n−p)/lambda_lower^n.
This latter bound cancels the common leading normalization exactly; it does
not raise a rounded Ritz value to a large power as if it were an exact answer.
Thermal purities use interval log Z_n(2b)−2log Z_n(b), paying both errors.

The unprojected degree96 certificate acquires actual ring128/256/512 data.
Examples for ring256: log(Z/5^n) widths are below2.678e−11 at b1/8,
5.197e−8 at b1/4, and2.159e−4 at b1/2. At b1/8,

    log T(256,1/8) in
       [−369.061984128482, −369.0619840764639].

The first five dyadic temperature pairs in the original input table are now
acquired to its required precision. The scalar float endpoints are wider
than the high-precision intervals. The rank3 count passes through b.625 and
fails at b.75 without the following ordinary sector repair. This failure is
retained, not interpreted as a physical failure of the model.

## Execute the source's rotation-sector repair

The vacuum and its Krylov vectors are SO(3)-scalar. Use the source's A4
projection, whose complete fourth moment is

    M_A=(Z4(I)+3Z4(P)+8Z4(C))/(12*5^4),              (6)

where P has angle pi and C angle2pi/3. This projection and the group character
method are prior, not new machinery claimed here. The present P/C traces
are actually acquired. In the same polynomial basis, 2H_P is integer and
2H_C is over Z[zeta], zeta^2+zeta+1=0. The CRT producer propagates both integer
components. The zeta trace component is checked zero modulo every prime;
the full physical trace is real and Galois invariant. All magnetizations and
all Taylor remainders are included.

On an integer-spin SO(3) irrep j, the A4-invariant multiplicity is
(2j+1+3(−1)^j+8chi_j(2pi/3))/12. For j>=1 the complement has dimension at
least3. This follows directly for j1 and from |chi_C|<=1 for j>=2. Therefore
all other scalar/invariant modes and all nontrivial SO(3) modes obey

    r_A=(M_A−theta_lower^4)^(1/4),
    r_non=((M4−M_A)/3)^(1/4),
    r=max(r_A,r_non).                                (7)

The chosen mode is known scalar, so subtracting its mass in M_A is justified.
If r<theta_lower, equations(4)/(5) apply with the full fourth-moment remainder,
not only the projected trace. This counts all representation multiplicities.

Degree192 plus(7) extends the count through b1.25; b1.5 fails. Useful actual
spatial bounds include

    1−S(256,3/4) <1.851e−24,
    1−S(256,1)   <7.586e−13.

At b1, however, the log-Perron interval is about4.62e−4 wide. A good spatial
tail is not automatically a precise thermal trace. No unverified Ritz value
or rank assumption is used to remove that pressure uncertainty.

`verify_continuation.py` independently replays the b3/4 A4 certificate with
stdlib Fraction Taylor/exponential enclosures, from the stored integer
moments and rational c. It also checks all analytic r1–3 moments and96/192
consistency. It does not rerun every CRT multiplication on r4–6. Parent's
separate Fraction replay covers the unprojected degree96 b1/8,1/4,1/2
certificate, not the later A4 work.

## A precise cold obstruction, including the projected method

A numerical factorization produced dyadic matrices L,X for the381-dimensional
M=0 block of H_open5+19.604I. Subsequent verification is entirely rational:
LL^T and LX are integer products divided by2^80, and sqrt6 is enclosed by
rational endpoints. The Schur row/column bounds give

    rho>=||I−LX||<1,
    ||L^−1||<=||X||/(1−rho)=B,
    lambda_min(H_open5+19.604I)>=B^−2−error>0.

The final positive margin is stored as an exact fraction. Every integer-spin
SU(2) multiplet includes an M=0 vector, so this proves the full open-chain
lower bound. A failed raw numerical candidate with nonzero unused triangle
was rejected; the accepted L explicitly discards that triangle and passes
the integer/rational residual proof. No numerical eigensolver accuracy is a
premise in this certificate.

Each ring bond occurs four times in the sum of translated open-five-site
Hamiltonians. Thus H_n>=−4.901n for n>=5. Taking even large n in the source
trace identity gives ||K_b||<=5exp(4.901b). The exact two/four-site ground
energies yield Tr K_b^2>=exp(12b), Tr K_b^4>=exp(20b), so

    Tr K_b^4/||K_b||^4 >= exp(.396b)/625.              (8)

The unprojected one-mode count requires this ratio<2; it is impossible for
b>18.00732028 even with an exact leading vector. Because every physical
twisted partition function is positive, M_A>=Tr K_b^4/(12*5^4). The A4
one-mode count is likewise impossible once exp(.396b)/7500>2, at about
b24.28. At b64 its invariant mass/norm^4 is above13.54million.

More generally a rank-k fourth-moment residual-mass proof can remove at most
k||K_b||^4 from that invariant trace. To reduce its residual below one mode
requires k>=exp(.396b)/7500−1. This is a limitation of this moment-tail method,
not a lower bound against all tensor compression, a no-go for larger moments,
or a physical theorem against the Haldane gap. Increasing numerical precision
or keeping a few more Krylov vectors with the same p4 mass cannot reach the
cold destination. Higher moments, structural operator-norm tails, or another
acquired normalized-purity operation are genuinely different repairs.

## Temperature lifting and the remaining actual acquisition

Source CT Eq5.10 already gives the exact identity

    s_L(2b)=2s_L(b)+log T(2L,b)−2log T(L,b),
    s_L=log S(L,b).                                  (9)

The actual S(256,3/4) above supplies a high-temperature initial condition for
seven doublings to b96. Its propagated initial log error is below2.4e−22.
Fourteen normalized thermal purities, on rings256/512 at b=.75,1.5,...,48,
plus final T(512,96), would complete the finite source input at that target.
The first-pair log-purity tolerance can be7.44e−7 and the last4.76e−5 for a
total logS budget.001. These cold/intermediate normalized inputs have not
been acquired. No point cold S or T value is fabricated.

The published2026 local-purity factorization result is a serious ordinary
comparator, but its theorem is stated for intervals with beta-dependent
constants. A periodic ring can be exactly folded into an open two-leg chain
of local dimension25, with endpoint rung interactions. This preserves the
loop, while requiring paired-site marginals, boundary-term control, numerical
decay constants, and their actual acquisition. The source's translation-
invariant interval hypotheses do not supply those facts for free.

The continuation therefore achieves the missing compressed transfer operation
at a real warm scope and identifies a governing cold limitation. It does not
claim a new general Lanczos/Temple/group-projection theorem, a matched speedup
over optimized Araki/MPO/QMC methods, or a uniform spin-two gap.
