# A connected thermal operation that cancels the pressure precision debt

The actual Hamiltonian is the uniform periodic spin-two Heisenberg chain

    H_n = sum_i S_i . S_(i+1),  Z_n(b) = Tr exp(-b H_n).

No Hamiltonian, noise, boundary condition, physical sector, or energy reference
is changed. The target acquired here is the connected scalar

    C_n(b) = log T_(2n)(b) - 2 log T_n(b),
    T_n(b) = Z_n(2b) / Z_n(b)^2.

For n=256,b=3/4 the exact rational replay proves

    -3e-11 < C_256(3/4) < 1e-24,
    S(256,3/2) > 1 - 3e-11.

The tighter outward interval consumer gives

    -8.384640063512e-12 < C_256(3/4) < 2.233265565728e-29.

The weaker rational result is independently sufficient for the first connected
dyadic input. None of the individual fine cold log-purities, the remaining
six connected increments, final T_512(96), or the spin-two gap is asserted.

## 1. Why the extensive log-purities need not be acquired separately

Write s_n(b)=log S(n,b)=log Z_(2n)(b)-2 log Z_n(b). Exact algebra gives

    C_n(b) = s_n(2b) - 2 s_n(b).                         (1)

If an actual transfer eigenvalue is lambda_b and

    Z_n(b)/5^n = lambda_b^n (1+u_n(b)),

then

    s_n(b) = log(1+u_(2n)(b)) - 2 log(1+u_n(b)).          (2)

The pressure n log(lambda_b) cancels exactly. Neither a small pressure
interval nor an accurate extensive partition function is an input to (2).
This is the source's existing dyadic identity with a more economical acquired
input; no priority claim is made for the algebra or normalized squaring.

## 2. Accepted source transfer and complete rotation sectors

The source continuous-history construction supplies a compact self-adjoint
K_b with Z_n(b)=Tr K_b^n for even n>=4. Put J_b=K_b/5. The source A4 rotation
decomposition has lists I,O,N whose even moments obey

    Tr J_b^p = I_p + 2 O_p + 3 N_p.

For the physical closing-bond rotations P (angle pi) and C (angle 2pi/3),

    I_p = [Z_p(I)+3 Z_p(P)+8 Z_p(C)]/(12*5^p),
    O_p = [Z_p(I)+3 Z_p(P)-4 Z_p(C)]/(12*5^p),
    N_p = [Z_p(I)-Z_p(P)]/(4*5^p).                       (3)

These are source group projections, not newly proposed positive frames.
All three lists and their exact multiplicities are retained. In particular,
an aggregate estimate (Tr J^4-I_4)/3 is unnecessary. At b=3/2 it overestimates
the relevant radius enough to lose the previous separation test.

The empty-history atom v has norm one. The actual scalar trial vector

    w = c0 v + c1 J_b v + c2 J_b^2 v

is rotation invariant and belongs to I. Its Gram and Rayleigh forms are
computed from the accepted exact open-chain identities

    m_r = <v,J_b^r v> = Z_open,r(b)/5^r,  r=1,...,6;
    m_0=1;
    G(c)=sum c_i c_j m_(i+j),
    H(c)=sum c_i c_j m_(i+j+1).

If G(c)>0 and H(c)/G(c)>theta>0, an actual positive eigenvalue lambda in I
is greater than theta. No uniqueness, pressure accuracy, physical ground-state
gap, finite-rank premise, or multiplicative amplitude residual is needed.

## 3. Count every periodic-loop mode at the precision actually needed

Select one such lambda. Every other I eigenvalue has modulus at most

    r_I = (I_4-theta^4)^(1/4).

Every O eigenvalue has modulus at most r_O=O_4^(1/4). The new actual six-cycle
acquisition gives the complete N_6 and hence r_N=N_6^(1/6). For even n>=6,

    0 <= u_n <= tau_n,
    tau_n = (I_4-theta^4) r_I^(n-4)/theta^n
            + 2 O_4 r_O^(n-4)/theta^n
            + 3 N_6 r_N^(n-6)/theta^n.                  (4)

For example, after removing lambda from I_4, each remaining |lambda_j|^n
is at most r_I^(n-4)|lambda_j|^4. The even-power sums are nonnegative. The
same argument applies to all O and N modes. Thus (4) includes the complete
infinite source spectrum and the actual periodic closing seam. It is not a
leading-mode approximation with an uncharged omitted tail.

The spatial-purity identity is a purity of the probabilities proportional
to |lambda_j|^n. Consequently S(n,b)<=1. Equations (2),(4) imply

    -2 log(1+tau_n) <= s_n(b) <= 0.                     (5)

This remains valid when a count is poor. It does not require r_I<theta or
r_N<theta; failure to obtain a small tau is reported honestly.

Combining (1),(5) gives the directly acquired connected interval

    -2 log(1+tau_n(2b)) <= C_n(b)
        <= 4 log(1+tau_n(b)).                           (6)

Thus the needed precision is a loop-tail precision. The large global collar
residual and extensive pressure uncertainty do not occur in this interface.

## 4. Complete exact acquisition of N_6

`code/acquire_cycle_moments.py` constructs the actual physical six-site
periodic Hamiltonians H_6(I) and H_6(P), including the closing bond. In the
unnormalized polynomial spin basis, 2H has integer entries and is diagonally
similar to the physical Hermitian Hamiltonian. The pi twist negates only the
closing raising/lowering terms; its Sz Sz term is unchanged.

For each magnetization M=0,...,12 and each selected modulus, the producer
computes all Tr(2H)^k through k=192, counting M>0 twice. This is exact because
spin inversion identifies the +/-M blocks for I and P. The largest sector
has dimension1751. Every sparse multiplication is small signed integers times
entries in[0,p). The code verifies row_abs_sum*p<2^62 and dimension*p<2^62;
both matrix accumulation and trace accumulation therefore fit signed int64.
Modular reconstruction uses pairwise coprime moduli and total modulus above

    2 * 5^6 * 72^192.

Since ||2H||<=72 in the physical norm, this uniquely reconstructs every
integer trace, with every physical state included. Primality is not needed
for the CRT argument; the modular inverses establish required coprimality.

No eigensolver output is a premise. The new physical I/P six-cycle arrays
are `results/cycle6_moments_exact_degree192.json`. A four-cycle replay matches
the previous exact P array and an independent analytic spin-addition spectrum
for I through degree24. That finite control checks source construction; the
all-mode conclusion follows from (3),(4), not extrapolation of a fixture.

## 5. Two independent scalar evaluations

The Fraction replay uses the complete exact power arrays and the elementary
Taylor enclosure

    Z = sum_(k=0)^D Tr(2H)^k (-b/2)^k/k! +/- E,
    E = d exp(x) x^(D+1)/(D+1)!,  x=6 B b,               (7)

where B is the number of physical bonds and d is the full dimension. It
encloses exp(x) itself by positive rational Taylor sums and a geometric tail.
All later computations are stdlib Fraction operations; no producer import,
eigensolver, mpmath, or Chebyshev code is used. Simple rational trial
coefficients are

    b=3/4: c=(16/1250,-91/100,-1), theta=233/25;
    b=3/2: c=(37/100,-1,-17/1000), theta=285.

Exact rational inequalities prove G>0, H-theta G>0 and the following bounds:

| b | theta lower | other I radius upper | O radius upper | N radius upper |
| --- | ---: | ---: | ---: | ---: |
| 3/4 | 9.32 | 3 | 4.2 | 7.36, using N_4 |
| 3/2 | 285 | 141 | 197 | 257, using new N_6 |

The deliberately rounded radii prove

    tau_256 <= (r_I/theta)^256
               +2(r_O/theta)^256+3(r_N/theta)^256.

The replay checks exactly that 2 tau_256(3/2)<3e-11 and
4 tau_256(3/4)<1e-24. Using log(1+x)<=x in (5),(6) proves the displayed
rational result, including S(256,3/2)>1-3e-11.

The separate interval consumer `code/scalar_loop_certificate.py` evaluates
the same exact moments by an improved Chebyshev expansion. For B bonds set

    Y=(2H+2B I)/(10B), spectrum(Y) subset[-1,1], a=5bB;
    exp(-bH)=exp(bB)[I_0(a)+2 sum_(k>=1)(-1)^k I_k(a)T_k(Y)].

It computes Tr T_k(Y) with exact integer polynomial recurrence

    P_0=1, P_1=X+2B,
    P_(k+1)=2(X+2B)P_k-(10B)^2 P_(k-1),
    T_k(Y)=P_k(2H)/(10B)^k.

The positive series I_k(a)=sum_m (a/2)^(2m+k)/(m!(m+k)!) is enclosed by its
paid geometric tail. For any rational r>1 the Laurent/Cauchy bound gives

    I_k(a) <= exp[a(r+1/r)/2] r^(-k),
    uniform omitted tail <=
        2 exp[a(r+1/r)/2] r^(-D-1)/(1-1/r).              (8)

Multiplication by d exp(bB) pays the whole physical trace error. All binary
floating endpoints reported in JSON are rounded further outward. This
consumer retains the explicit mpmath interval-arithmetic assumption. The
Fraction result at the first increment is independent of it.

Chebyshev evaluation makes the same exact moment arrays usable through b=6,
well beyond the earlier raw Taylor evaluation. It does not repair their
mode count: at b=3, the current all-other radius/theta bound is about1.1032,
and the connected b=3/2 input is still far too broad. No useful cold input
is inferred from improved polynomial evaluation alone.

## 6. Remaining contract

The actual first connected increment meets the first 7.44047619e-7 scale
with considerable margin, while neither separate log T_256(3/4) nor separate
log T_512(3/4) is acquired at that precision. This is a constructive reason
to replace that pair by the scalar quantity the dyadic identity actually uses.

Starting instead from the acquired S(256,3/2)>1-3e-11, six doublings reach
b=96. The propagated seed log error is below1.921e-9. Six later connected
increments and final T_512(96) are unacquired. Failed b=3 and b=6 mode counts
are retained in the output; they are not impossibility results for richer
messages, higher moments, MED, BS-CMI, QBP, or thermal MPOs.
