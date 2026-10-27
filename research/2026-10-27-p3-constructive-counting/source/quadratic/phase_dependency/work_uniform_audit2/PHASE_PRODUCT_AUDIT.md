# Independent audit: sparse phase products with many factors

27 October 2026. This audits the new candidate supplied by the parent and dense-algebra agent against Proposition 3.4, Definition 3.1, Lemma 4.7 and the explicit arithmetic estimates in the governing source. The result is conditional on that source. It is not a practical-speed or historical-priority claim.

## 1. Signed Boolean phase: the algebraic reduction is valid

Let P(x)=XOR_{S in M} product_{v in S} x_v be an explicitly listed polynomial over F_2, of degree at most a fixed k, on n original Boolean inputs. Repeated monomials may be cancelled modulo two and repeated powers within a monomial reduced to first powers. Put ell=n+2 and use the commutative Q-algebra

    A=Q[V]/(V^ell).

Give every monomial occurrence its own factor and its own incidence variables:

    Phi_S(Y_S)=1-2V product_{v in S} Y_(S,v).

The factor scope has size at most k. A retained product term selecting j factors has V-degree j<ell and incidence degree at most kj. Therefore the product in A has incidence degree at most

    d=k(ell-1)=k(n+1),

independently of the number m of factors. This is precisely hypothesis (3.2), including its requirement that different factor incidences be considered independent before substitutions. No global multilinearization or common replacement for all occurrences is being assumed.

At T=0 all replacement rows restore the original inputs. For Boolean x, the untruncated product evaluated at V=1 equals (-1)^P(x). Each omitted j-term is divisible by 2^j and j>=ell. Consequently, if Z_trunc is the coefficient sum of the truncated product summed over x, then

    Z_trunc = sum_x (-1)^P(x)  (mod 2^(n+2)).

The true signed sum Z lies in [-2^n,2^n]. Its residue modulo 2^(n+2) uniquely determines it, using a centered representative, and

    # {x:P(x)=0}=(2^n+Z)/2.

The n+2 precision is sufficient and avoids an actual ambiguity: modulo 2^(n+1), the two endpoint sums +2^n and -2^n coincide. Constant monomials are harmless degree-zero factors or may be extracted as a known global sign.

Evaluation at V=1 is not a well-defined algebra homomorphism on Q[V]/(V^ell). It is the specified linear coefficient-sum map on the unique degree-below-ell representative, used only after exact reconstruction at T=0. The divisibility argument above is what justifies that final map. Treating V=1 as a homomorphism during intermediate truncated arithmetic would be an error.

## 2. Manufactured scopes, incidence bounds and design

The original monomial incidence is at most km. Fix every variable occurring in more than

    b0=max(1,ceil(km/n)) ceil(sqrt(lambda)), lambda=ceil(log_2 n),

monomial scopes. There are at most n/sqrt(lambda) such variables. Their assignments give disjoint branches, leaving N>=n/2 free inputs for sufficiently large n. Substitute the fixed bits, cancel duplicate monomials modulo two, and add a neutral factor with scope {v} for every free variable. The new maximum factor incidence is at most b0+1; scope is at most max(k,1). Monomial descriptions never grow.

The truncation precision remains ell=n+2, even when N<n. Thus d=k(n+1)=O_k(N); no original-input precision is lost after branching.

Put lambda'=ceil(log_2 N), nu'=ceil(log_2 lambda'). A sufficient logarithmic scale h is

    h = ceil(log_2(2+km/N)) + 4nu' + C_k,

where a fixed constant C_k covers rounding and neutral factors. Set a=h/lambda'. In the intended range m=n exp(o(log n)), a tends to zero. Use

    r=floor(sqrt(lambda'/h)),
    t=ceil(log_2 r), Q=floor(lambda'/(128t)),
    tau=1/(r lambda'), D=r^(2Q),
    A0=ceil(log_2(2(b0+1)r^2 lambda')),
    R=ceil(sqrt(8Q A0))+32.

Here A0=O_k(h), D<=2^(lambda'/64), and

    R/Q=O_k(sqrt(a log(2/a))) + O(log(2/a)/lambda').

For a tending to zero, the exact scope-balance, interval, and tail guards of Lemma 4.7 eventually pass. The binomial tail is certified by the source's Hoeffding estimate; no factor decomposition is supplied by the input. The actual replacement rows and integer summaries are constructed by Lemma 4.7 in polynomial time in their explicit parameters, all bounded by a universal polynomial in L+n in this range.

Guard caution: one must not claim that 6R<=Q eventually holds uniformly at every fixed positive a<=1/16. The ratio R/Q need not tend to zero there. A uniform quantitative implementation can use exhaustive search when the guards fail. For a above a sufficiently small fixed threshold, its cost 2^N is absorbed in the claimed exponential bound by increasing the constant. For a below that threshold, all sufficiently large instances pass uniformly; bounded small cases are again absorbed. This repair does not change the subexponential conclusion when a tends to zero.

## 3. Bit complexity is polynomial; a sharper denominator bound is available

Let delta=(R-1)!Q! be the replacement-row denominator. At a fixed Taylor node, each substituted variable is a rational z-polynomial with denominator dividing delta. Its coefficient norm after clearing delta is at most B0, where

    log B0=O(Q log(Q+2)+log(nD+2)).

The V^j coefficient of any partial or full product of the phase factors has denominator dividing delta^(kj). This follows by induction: selecting j phase terms uses at most kj substituted variables; multiplying V-degrees j_1 and j_2 adds both exponent budgets. The rational denominator need not grow as delta^(km), although that looser bound would also be polynomial in the input length.

After denominator clearing, the coefficient norm of a product of at most m factors is bounded by a sum of at most ell terms of the form

    binom(m,j) (2 max(delta,B0)^k)^j,   0<=j<ell.

Hence its logarithm is

    O(ell(log(m+2)+k log(max(delta,B0)+2))+log ell).

Group assignment sums add at most n bits. The correction-pair and measurement enumeration adds only its logarithm, bounded by O(n+n tau log(D+2)). Thus all rational numerator and denominator lengths are polynomial in L+n and the explicit design parameters. Storing one element of A[z]/(z^J) takes ell J rationals. Factor evaluation, truncated products, group summation and the source's rational Hermite reconstruction have polynomial bit cost and polynomial workspace.

This establishes the arithmetic requirement left abstract by Proposition 3.4; it is not necessary to invoke Proposition 5.3's particular equation lift.

With q=floor(dR/Q), the correction enumeration contributes

    log C_q=O_k(n sqrt(a) [log(2/a)]^(3/2)).

The entropy logarithm is necessary. Group and measurement enumeration contribute O(n/r)=O(n sqrt(a)), and high-incidence branching contributes O(n/sqrt(log n)). Therefore the proposed time bound, with the fallback qualification above, is valid:

    poly(L+n) 2^[O_k(n sqrt(a) [log(2/a)]^(3/2))].

It is subexponential in the ORIGINAL n when m=n exp(o(log n)), for fixed k. All factors and the useful design are manufactured from the explicit monomial list. This by itself is not a theorem about arbitrary circuits that might have a small but undiscovered monomial representation.

## 4. Fixed 2^b-th root phases

Let q0=2^b, with fixed b>=1; d0=2^(b-1); and let zeta be a primitive q0-th root of unity. Work in

    A=Q(zeta)[V]/(V^ell), ell=d0(n+2).

For an explicitly listed polynomial P(x)=sum_S c_S product_{v in S}x_v modulo q0, the monomial factor is

    Phi_S=1+(zeta^(c_S)-1)V product_{v in S}Y_(S,v).

At Boolean inputs and V=1 the untruncated product is zeta^P(x). Every nonzero coefficient zeta^c-1 is divisible in Z[zeta] by pi=zeta-1. Also pi^d0 belongs to 2 Z[zeta]. An elementary proof suffices: for d0>=2, expand (zeta-1)^d0, use zeta^d0=-1, and note that all intermediate binomial coefficients of the power of two d0 are even. For d0=1, pi=-2 directly. Thus every omitted term of V-degree at least d0(n+2) lies in 2^(n+2)Z[zeta]. The argument needs only this divisibility, not an unproved assertion that a ramification unit is freely available.

Use the integral basis 1,zeta,...,zeta^(d0-1), reducing zeta^d0=-1. The true phase sum sum_x zeta^P(x) has each basis coefficient in [-2^n,2^n], since each summand is plus or minus one basis vector. Therefore reduction modulo 2^(n+2) in each integral coordinate and centered reconstruction recovers the phase sum exactly.

The retained incidence degree is k(ell-1)=O_(k,b)(n). The algebra has O_b(n) rational coordinates, and its multiplication uses the fixed relation zeta^d0=-1. Coefficient norms are submultiplicative, and zeta^c-1 has norm at most two. The rational arithmetic and manufactured-design proof therefore extend with constants depending only on k,b.

One phase sum does NOT determine the complete q0-value output histogram when b>1. Compute all q0 characters

    Z_j=sum_x zeta^(j P(x)), j=0,...,q0-1.

Each uses the same construction. Reconstruct every Z_j exactly in the integral basis first; then obtain the residue counts by the exact finite Fourier formula

    N_t=(1/q0) sum_j zeta^(-jt) Z_j.

The numerator is exactly q0 N_t, so the division is exact. Because the phase sums have already been reconstructed exactly, no additional modular precision is lost in this division. There are only fixed-many characters and basis coordinates. This distinction matters: directly dividing a residue modulo 2^(n+2) by 2^b would otherwise lose b bits.

## Audit conclusion

The phase-product candidate passes the source-level algebra, incidence, arithmetic, precision and reconstruction audit, with the explicit guard and Fourier-reconstruction qualifications above. It removes the global polynomial-scope obstruction for a single explicitly sparse phase polynomial: the factors have the monomials' scopes while a shared divisibility budget keeps total incidence degree linear in n even when m is superlinear. That is a different construction from applying Section 5 to one large-scope equation.
