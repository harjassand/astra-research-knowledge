# A charged permutation counterpart of the precise Reed–Muller unitary stability theorem

2026-10-09. Proof candidate deduced here using the mixed-copy transfer and existing finite-dimensional unitary stability. The finite-group application uses the stated finite-group Becker–Chapman theorem, so it does not depend on the compact/Borel adaptation. Historical priority is not asserted. The source's additive error floor is retained throughout.

## 1. General code-presentation transfer

Let C be a binary linear code of length L, dimension k, and relative minimum distance Delta>0. Let

 G=F_2^L / C^perp = F_2^k,

with the L coordinate generators s_i and uniform generator measure. Suppose some finite presentation of this G on those generators, with relation distribution mu_R, has the following unitary stability modulus f:

For input d-by-d unitaries with average squared normalized HS relation defect at most epsilon, there are an exact representation rho:G->U(D), a rank-r partial isometry w:C^d->C^D, and eta=f(epsilon), such that

 average_i ||U_i-w^*rho(s_i)w||_F^2/d <= eta,
 (d-r)/d <= eta,   (D-r)/D <= eta.                  (A)

For relation errors epsilon<=1/2, the same presentation and distributions are flexibly stable in permutations, with a valid coarse modulus

 F(epsilon)=min{1, 2,000,000 f(2epsilon)/Delta}.     (B)

More explicitly, if the second entry is below one, input permutations on d labels with average relation Hamming defect epsilon admit an exact action on N>=d labels such that

 N <= (1+2,000,000 f(2epsilon)/Delta)d,
 average_i d_h(P_i,h(s_i)) <=2,000,000 f(2epsilon)/Delta.

For the other regime use the trivial action on d labels. For epsilon>1/2 define F(epsilon)=1 and also use that action; no value of f outside its stated domain is required. The metric d_h counts every additional label as an error.

### Why the exact tensor gap is uniform

The characters of G are naturally the codewords c in C, with chi_c(s_i)=(-1)^(c_i). Every unitary representation of this finite abelian group decomposes into characters. For each nontrivial character,

 average_i |chi_c(s_i)-1|^2 =4 wt(c)/L >=4Delta.

The same holds for the mixed tensor representation of any rho, since its constituents are again characters of G. Therefore the energy-gap parameter kappa in FINITE_SOURCE_UNITARY_ROUNDING.md can always be taken to be 4Delta. No infinite property-(T) hypothesis is used.

### Partial-isometry bookkeeping: a common coordinate space

Assume eta<=1/2. Write a=d-r, b=D-r. From (A), D<=d/(1-eta), so b<=2eta d. Work on H=C^d direct-sum C^b, of dimension ell=d+b. Embed C^D isometrically as w(C^d) identified with the rank-r initial subspace A=w^*w in C^d, plus the new C^b coordinates. On its orthogonal complement B=I-A, extend rho by the trivial representation. This yields an exact representation sigma on H. Extend each P_i by the identity on the b new coordinate labels, giving a permutation P_i'.

Let A_i=w^*rho(s_i)w. The C^d diagonal block of sigma(s_i) is A_i+B. Consequently

 ||A_i+B-P_i||_F^2 <= ||A_i-P_i||_F^2+3a.

Each off-diagonal block between C^d and C^b has squared Frobenius norm at most b; the difference of the C^b block from the identity has squared norm at most 4b. Hence

 ||sigma(s_i)-P_i'||_F^2 <= ||A_i-P_i||_F^2+3a+6b.

Averaging, dividing by ell>=d, and using eta<=1/2 gives

 delta_new^2 <=16eta,
 ell <=(1+2eta)d.                                 (C)

This explicit construction does not discard coordinates in a basis incompatible with the original permutation labels.

Apply the mixed-copy transfer with kappa=4Delta. It gives an action on N>=ell labels with

 N/ell-1 <=789264 eta/Delta,
 average_i d_h(P_i',h(s_i)) <=16eta+1321416 eta/Delta.

The original-to-padded comparison costs b/ell<=2eta. Also

 N/d-1 <=2eta+1578528 eta/Delta <=1578530 eta/Delta,

and

 average_i d_h(P_i,h(s_i)) <=18eta+1321416 eta/Delta <=1321434 eta/Delta.

Both are bounded by the constant in (B). If eta>1/2, the trivial action already obeys the coarse bound. This proves the general transfer. The initial conversion epsilon_HS=2epsilon_Hamming explains f(2epsilon).

## 2. Exact CVY input, with its limitations preserved

Chapman–Vidick–Yuen, arXiv:2311.04681v2 (19 July 2026), Definition 2.2 gives exactly (A), including both rank deficiencies. For an input matrix algebra M_d, a finite-trace corner of M_d tensor B(ell_2) has finite rank D, so this really yields a finite-dimensional exact representation, not an uncharged infinite-dimensional dilation.

Their Theorem 4.1 applies to the binary Reed–Muller/Hadamard code with parameters

 q=2^t,  number of variables m,  individual polynomial degree r<q,
 L=q^(m+1),   k=t(r+1)^m.

The q-ary Reed–Muller code has relative distance at least 1-mr/q; Hadamard concatenation gives

 Delta >=(1-mr/q)/2.

The source's precise unitary modulus is

 f(epsilon)=min{ C(mrt)^a (epsilon^b+q^(-c)), C'_(m,r,t) epsilon },

where C,a,b,c are positive universal constants and C' may depend on the presentation. Thus (B) gives a permutation modulus with the SAME parameter dependence, up to a universal factor divided by Delta. When mr/q<=1/2, Delta>=1/4 and this factor is universal.

The number of generators is L, the number of relators is O(L^2), and their maximum length is max(r+2,4), with precisely the source's generator and relation sampling distributions. No new relations or stronger input test are smuggled into the transfer.

## 3. What capability follows, and what does not

This provides a permutation analogue of the **formal** CVY Theorem 4.1, with charged flexible sheet count. In its efficient parameter/error regime, unitary soundness from quantum code testing can therefore be transferred to a genuine finite action in the Hamming metric.

For a concrete infinite parameter sequence, take m=r=s and t=s^2. Then q=2^(s^2), k=s^2(s+1)^s, presentation size is 2^(O((log k)^3)), relation length is O(log k), and Delta is bounded below. The transferred modulus has a poly(log k) prefactor times epsilon^b+2^(-c s^2), together with the separate presentation-dependent linear bound. For epsilon>=2^(-c s^2/b), the additive floor is absorbed into epsilon^b.

It is NOT legitimate to erase the additive q^(-c) term and assert a uniform poly(log k)epsilon^b modulus for all positive epsilon. The fallback constant C' can be large. Nor does this prove the polynomial-in-k presentation size demanded by the sharper form of Chapman–Lubotzky Problem 6.9, arbitrary-code permutation testability, or a non-sofic group. The random-complex first-stage unitary repair remains a different unresolved gate.

## Sources

- Exact unitary statement and partial-isometry metric: https://arxiv.org/html/2311.04681v2 , Definitions 2.1–2.3, Theorem 4.1, Sections 3.2–3.3.
- Finite-group uniform charged completion: Becker–Chapman, Theorem 1.2, https://arxiv.org/pdf/2005.06652 . Only the finite-domain case is needed in this application.
- Motivating quotient-Poincare and permutation presentation questions: https://arxiv.org/html/2311.06706v3#S6 . The source's broader motivations are not automatic consequences of this note.
