# A finite-prefix gap from crossing and interpolation

**Scope.** This proves a positive gap for every finite prefix and the explicit lower bound `exp[-4 n log n - O_theta(n)]`. Joined to the separately established general prefix-compression theorem, it gives a growing-memory lower bound. It does not give a sublinear decoder or a matching linear-memory converse.

## 1. Definitions and orientation

Site 0 is the source and sites 1,...,n are bath qubits. Let `u=cot(theta)` be real and nonzero. Write `P_0j` for SWAP, and define

    L_j(z) = z I + i P_0j,
    T_n(z) = L_n(z)...L_1(z),
    W_n = T_n(u)/(u^2+1)^(n/2),
    Lambda_n(X) = (1/2) Tr_0[W_n(I_0 tensor X)W_n^dagger].

The chronological physical unitary equals W_n up to a scalar phase. All Hilbert-Schmidt norms use normalized trace. Set `Xbar=I_0 tensor X`, and similarly for Y. Define `gamma_n` as the minimum of `1-||Lambda_n(X)||_2^2` over traceless bath operators of norm one. The proof shows that this number is positive. It is the smallest nonzero eigenvalue of both `I-Lambda_n^dagger Lambda_n` and `I-Lambda_n Lambda_n^dagger`, since they have the same singular-value defects.

## 2. Crossing and alternating intertwiners

Let `C(A)=sigma_y^(0) A^(t_0) sigma_y^(0)`, with transpose only on site 0. This is a linear Hilbert-Schmidt isometry. Directly,

    C(L_j(z-i)) = z I - i P_0j.

The entries of factors at distinct bath sites commute, so source transposition reverses their order. Consequently,

    C(T_n(z-i)) = (z^2+1)^n T_n(z)^(-1).                 (1)

For `D(z;X,Y)=T_n(z)Xbar-Ybar T_n(z)`, multiplication by bath operators commutes with C. Equation (1) implies

    D(z-i;Y,X)
      = -(z^2+1)^n C[T_n(z)^(-1) D(z;X,Y) T_n(z)^(-1)]. (2)

X and Y alternate at each shift. Neither C nor the inverse is used as a physical operation; they occur only in a mathematical converse.

If `D(u;X,Y)=0`, all `T_n(u-ki)` are invertible, and (2) gives `D(u-2ki;X,Y)=0` for every k>=0. Since D is a polynomial of degree at most n, n+1 even-shift zeros make it identically zero. Its leading coefficient gives X=Y. At z=0,

    T_n(0) = i^n C_n,  C_n=P_0n...P_01,

where C_n cyclically permutes all n+1 sites. Hence Xbar commutes with the cycle. It is identity on site 0; cyclic invariance makes it identity on every site. Thus X is scalar. In particular, if `||Lambda_n(X)||_2=||X||_2`, the conditional expectation has lost no norm, so with `Y=Lambda_n(X)` one has `W_n Xbar W_n^dagger=Ybar`. The preceding argument proves that identity is the only singular-value-one direction.

## 3. Quantitative propagation and interpolation

Put `delta=||W_n Xbar-Ybar W_n||_2`, so `||D(u;X,Y)||_2=(u^2+1)^(n/2) delta`. At `z=u-ki`, the singular values of each local L_j are `|z+i|` and `|z-i|`. Therefore the norm multiplier in (2) is at most

    [(u^2+(k+1)^2)/(u^2+(k-1)^2)]^(n/2).

These factors telescope. For m>=1,

    ||D(u-mi; alternating X,Y)||_2
      <= [((u^2+(m-1)^2)(u^2+m^2))/u^2]^(n/2) delta.  (3)

Define `B_n=(u^2+4n^2)/|u|`. At the n+1 nodes `z_k=u-2ki`, k=0,...,n, equation (3) gives `||D(z_k;X,Y)||_2 <= B_n^n delta`. The k=0 case also holds because `B_n>=sqrt(u^2+1)`.

The reciprocal product of node differences at node k has magnitude `1/[2^n k!(n-k)!]`; summing these magnitudes gives `1/n!`. Lagrange interpolation of the leading coefficient and evaluation at zero therefore yield

    ||X-Y||_2 <= B_n^n delta/n!,
    ||D(0;X,Y)||_2 <= (|u|+2n)^n B_n^n delta/n!.

Set

    K_n = B_n^n [(|u|+2n)^n+1]/n!.                    (4)

Since `C_n Xbar-Xbar C_n=(C_n Xbar-Ybar C_n)+(Ybar-Xbar)C_n`, these bounds give

    ||[C_n,Xbar]||_2 <= K_n delta.                    (5)

## 4. Cycle estimate and gap

Let E_j be the conditional expectation replacing site j by identity. E_0 fixes Xbar. Its jth cyclic rotation lies in the range of E_j and is within `j||[C_n,Xbar]||_2` of Xbar. By orthogonal projection, `||Xbar-E_j(Xbar)||_2 <= j||[C_n,Xbar]||_2`. The commuting site expectations obey variance tensorization:

    ||Xbar-tr(X)I||_2^2
      <= sum_(j=0)^n ||Xbar-E_j(Xbar)||_2^2
      <= n(n+1)(2n+1)/6 * ||[C_n,Xbar]||_2^2.          (6)

For traceless X of norm one and `Y=Lambda_n(X)`, orthogonal projection gives `delta^2=1-||Lambda_n(X)||_2^2`. Equations (5)-(6) prove

    gamma_n >= 6/[n(n+1)(2n+1) K_n^2] > 0.            (7)

An optional sharper cycle estimate is `||[C_n,Xbar]||_2^2 >= alpha_n ||X-tr(X)I||_2^2`, where `alpha_n=4 sin^2(pi/[2(n+1)])`. To prove it, expand in Pauli strings and partition the strings into cyclic orbits. Every nonidentity orbit has a string with a nonidentity source Pauli; its coefficient is forced to zero. The allowed coefficients form discrete Dirichlet paths of length at most n. Their minimum Laplacian eigenvalue is `2-2cos(pi/(n+1))=alpha_n`. The trace removes the identity orbit. This yields the stronger valid bound

    gamma_n >= alpha_n/K_n^2.                        (8)

## 5. Asymptotics and operational consequence

At fixed nonzero finite u, Stirling's formula in (4) gives `log K_n=2n log n+O_u(n)`. Hence (7) or (8) implies

    gamma_n >= exp[-4n log n-O_u(n)].                 (9)

The next step imports the general prefix-compression theorem established separately. For q retained qubits, choose prefix n=q+1, provided n<=N. The compression Choi state's spectral cap is `2^q/2^n=1/2`. Since the kernel is rank one, its gap energy is at least `gamma_n/2`; the prefix theorem bounds that energy by a constant times final half-diamond error epsilon. Thus

    log(1/epsilon) <= 4(q+1)log(q+1)+O_theta(q+log q),
    liminf_(epsilon->0) q_peak loglog(1/epsilon)/log(1/epsilon) >= 1/4.

If q>=N there is already full linear storage. At the benchmark `N=Theta_theta(log(1/epsilon))`, the result is `q=Omega_theta(N/log N)`. It still permits q=o(N), so the requested endpoint remains unresolved. A gap bound exponential in n, or a strong enough low-spectrum profile, would be needed to obtain a matching linear-memory converse at fixed theta.
