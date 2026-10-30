# A constructive coherent Peierls sieve for occupied connected components

2026-10-29. This proves a nontrivial special case of a coherent witness sieve. It is NOT yet a sieve for the sparse/dense connected-animal certificates produced by asynchronous SSF.

## 1. Binary-location theorem

Let G have n fault locations, bounded degree, and at most n A^l connected vertex sets of size l, with A>=2 fixed. Suppose exact path sums A_T and inclusive sums F(S)=sum_{T superset S} A_T satisfy

    ||F(S)||_diamond <= η^|S|.

They may be signed or coherent maps and may act on a retained common bath. No positivity is assumed for A_T. Let b(T)=1 precisely when G[T] has a connected occupied component with at least m vertices. Define B=sum_T b(T)A_T. Then, for 2Aη<1,

    ||B||_diamond <= exp(Z)-1,
    Z = n (2Aη)^m/(1-2Aη).                            (1)

In particular Z<=1 implies ||B||<=2Z. There is no exp(nη) prefactor. If the complementary paths all belong to a common correctable span, their decoded logical channel has error at most 2(exp(Z)-1).

### Proof

Let μ_b(S)=sum_{U subset S}(-1)^(|S|-|U|)b(U). Then B=sum_S μ_b(S)F(S). Fix S and its induced connected components C_1,...,C_k. For U subset S,

    b(U)=1-product_i [1-b(U intersect C_i)].

Taking the full mixed finite difference over S shows

    μ_b(S)=(-1)^(k-1) product_i μ_{b_i}(C_i),

where b_i is the occupied-component event restricted to C_i. If |C_i|<m, then b_i is identically zero, so μ_b(S)=0. Otherwise |μ_{b_i}(C_i)|<=2^|C_i|.

Therefore the weighted absolute Möbius sum is bounded by the sum over collections of mutually disjoint, nonadjacent connected sets C, each of size at least m, with activity (2η)^|C|. Dropping compatibility and applying the exponential generating-function bound gives

    sum_{S nonempty}|μ_b(S)|η^|S|
      <= exp[sum_{C connected, |C|>=m}(2η)^|C|]-1
      <= exp(Z)-1.

This explicitly resums all unmarked locations through F(S); it does not sum their absolute Dyson weights. The proof uses the special componentwise Boolean factorization, not a classical probability inequality.

## 2. Multiplicity version, proved with factorial inclusive bounds

At each graph vertex j let n_j>=0 count insertions. Suppose the inclusive sums for arbitrary selected positive thresholds satisfy

    ||F(k_S)||_diamond <= product_{j in S} ε_j^k_j/k_j!,
    ε_j<=ε.

This is exactly the mixed Taylor-remainder bound in COHERENT_EXTENSION.md. Let b(n)=1 if an occupied connected component has *total insertion multiplicity* at least m. Then for any x>=1 with

    y=2A(exp(xε)-1)<1,

one has

    ||B||_diamond <= exp(Z_x)-1,
    Z_x=n x^(-m) y/(1-y).                             (2)

Choose a constant u>0 so that 2A(e^u-1)<1 and set x=u/ε, for ε<=u. This gives

    ||B||_diamond <= exp[C_A n (ε/u)^m]-1.            (3)

Thus repeated insertions in one cell are included without replacing them by one binary fault.

### Proof

Use Möbius inversion on the product of nonnegative integer chains. The coefficient at a positive multi-index k supported on S is

    μ_b(k)=product_{j in S} Δ_j b(k),
    Δ_j f(k)=f(k)-f(k-e_j).

Coordinates outside S are zero. For the induced components of S, the same OR factorization as above applies to every evaluation k-e. If some component C has sum_{j in C}k_j<m, b restricted to that component is identically zero on this finite-difference cube, so its factor vanishes. Every remaining component coefficient has absolute value at most 2^|C|.

For each connected set C define its majorizing activity

    a(C)=2^|C| sum_{k_j>=1, sum k_j>=m}
                       product_j ε^k_j/k_j!.

Using x>=1,

    a(C)<=x^(-m)[2(e^(xε)-1)]^|C|.

Connected-set counting gives sum_C a(C)<=n x^(-m)y/(1-y). The compatible-polymer sum is again bounded by exp(sum_C a(C))-1. Finite count truncation followed by absolute-convergence passage yields (2).

## 3. Physical scope

The inclusive factorial bound is available for bounded local Hamiltonian commutators and added bounded Lindblad generators if independently scaling each assigned cell by z_j in [0,1] preserves CPTP evolution. All norms must be on the retained system-bath maps; bath dimension and memory are not discarded. Conditioning on an externally independent ideal Poisson evaluation schedule is legitimate: intervening ideal measurement/feedback instruments remain CPTP. Conditioning on unobserved fault labels is not.

Arbitrary signed HP additions are outside this proof unless they satisfy the same independent-switching contract or have another norm-resummation proof. Only the complete perturbed generator being physical is insufficient.

## 4. Why this does not close asynchronous SSF

The actual SSF obstruction is a connected *containing animal* W with a positive density of fault mass. Its occupied fault vertices need not themselves be connected in a fixed bounded-degree graph. Long clean bridges may connect densely seeded islands. Neither a fixed-radius graph power nor arbitrary Pauli-label branching automatically fixes this.

For a general dense-animal selector, the key vanishing assertion used above can fail: b restricted to the disconnected occupied support S can depend jointly on different components through containing animals using unoccupied vertices. Hence the Möbius coefficient need not factor by the components of G[S]. Replacing the actual selector by occupied-cluster badness is unsound unless a new deterministic extraction lemma proves that implication.

Canonical first-witness extraction alone also does not solve this: subtracting all earlier possible witnesses creates a history-defined signed sub-sum, and its norm is not bounded by the original inclusive norm. It needs a further resummation argument. The theorem above supplies that argument for a precisely specified nontrivial family, but not for all dense-animal witnesses.

The independently recorded Poisson CPTP-kick theorem in POISSON_CPTP_ONE_BLOCK.md bypasses this coherent sieve by a legitimate probability union bound on a label-independent envelope event. It does not establish the same result for continuously acting coherent Hamiltonian noise.
