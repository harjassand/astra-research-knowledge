# Local duality transfer of thermal decoder stability

Date: 2026-11-02. Status: a proved conditional transfer lemma, with an explicit local construction of its algebraic maps. Not a claim that the explicit ell=8 family already satisfies its premises.

## Source boundary

Reference [34] of arXiv:2605.10943v1 is Yiming Li, Zimu Li, Zi-Wen Liu, Quynh T. Nguyen, **Poincare Duality and Multiplicative Structures on Quantum Codes**, arXiv:2512.21922v1. Its equations (3.3)–(3.8) specify the double complex used below; Proposition 3.16 supplies its locally exact vertical augmentation. Theorem 3.17 proves code-parameter and decoder duality, not thermal lifetime duality. The newer paper §2.4 explicitly leaves the latter as an expectation and proposes a local HPL approach in footnote 6.

Sources:
- https://arxiv.org/html/2512.21922v1#S3.SS1
- https://arxiv.org/html/2512.21922v1#S3.SS3
- https://arxiv.org/html/2605.10943v1#S2.SS4

All transfer formulas, probability arguments, and conditional conclusions below are derived here, rather than asserted to be source theorems.

## 1. Exact geometric and algebraic hypotheses

Work over F_2, with fixed dimension t (ultimately t=2). Fix coordinate bases of all stalks. Require, uniformly over the family:

1. Every closed cell has at most D faces and every cell has at most D cofaces. Every stalk has dimension at most b. The physical coordinate/check bases are these bounded-size stalk bases, or bounded-local changes thereof.
2. The cellular differential squares to zero. Each closed cell has ordinary cohomology F_2 in degree zero and zero in positive degrees; connectedness is part of this requirement.
3. For every cell sigma, the local transposed cochain complex on its costar has homology only at its top end. Its top kernel is identified with Fperp_sigma through the actual top-cell restriction embedding. Equivalently, the augmented vertical sequences of Proposition 3.16 are exact. Check this by finite-field ranks and the actual augmentation matrices, not by just counting global logicals.
4. The horizontal and vertical differentials below commute. This follows from compatible restrictions, but should also be matrix-verified for an atlas.

These are intentionally explicit premises. Global homology equivalence, global distance, bounded check weights alone, or a visually plausible cell atlas do not substitute for them. In the strong-sheaf framework with top stalk F_2, appropriate local acyclicity gives premise 3; an implementation should still verify the matrices.

Set A^i=C_{t-i}(X,F), with differential d_A=boundary, and B^i=C^i(X,Fperp), with differential d_B=coboundary. For t=2 both have physical errors at degree 1, syndromes at degree 2, and stabilizers at degree 0.

## 2. The actual bounded-local construction

Use the triangular double complex

K^{p,q}= direct_sum_{sigma in X(p)} direct_sum_{tau >= sigma, dim(tau)=t-q} F_tau,

for p,q>=0 and p+q<=t. Label a coordinate by (sigma,tau,a). Its total degree is p+q. Define

(d_h x)(sigma',tau)=sum_{sigma lessdot sigma' <= tau} x(sigma,tau),

(d_v x)(sigma,pi)=sum_{sigma <= pi lessdot tau} res(pi,tau)^T x(sigma,tau).

Then D_T=d_h+d_v and D_T^2=0. These are explicit sparse binary matrices, not inferred maps on homology.

### Horizontal contraction

Regroup coordinates by tau. Each horizontal block is the ordinary cochain complex of the closed cell X_{<=tau}, tensored with F_tau. Contract it onto its degree-zero constant functions, identified with the corresponding summand of A. The inclusion i_A repeats a stalk vector at all vertices below tau. Choose a normalized contraction (i_A,p_A,h_A) by Gaussian elimination separately within this block, with

p_A i_A=I,  I+i_A p_A=d_h h_A+h_A d_h,

h_A^2=0, h_A i_A=0, p_A h_A=0.

Here h_A has bidegree (-1,0). No elimination involving distinct tau blocks is permitted.

### Vertical contraction

Regroup by sigma. Each vertical block is the costar local boundary complex, indexed by q. Its degree-q=0 kernel is the prescribed copy of Fperp_sigma. Contract onto that prescribed kernel using Gaussian elimination within this block, giving (i_B,p_B,h_B), with analogous identities for d_v. Here i_B is the top-cell restriction embedding and h_B has bidegree (0,-1).

### Explicit Gaussian elimination convention

For a finite cochain complex (V,d) with prescribed cohomology representatives H, choose B^j=im d^{j-1}, then representatives H^j, then a complement L^j so V^j=B^j direct_sum H^j direct_sum L^j. The restriction d:L^j -> B^{j+1} is invertible. Define p as projection onto H, i as its prescribed inclusion, and h on B^{j+1} as this inverse and zero on H and L. This gives all normalized contraction identities. Each block has bounded dimension, so even dense local elimination remains uniformly local.

### Finite perturbation formulas

Perturb the horizontal contraction by d_v and the vertical contraction by d_h:

P_A = p_A sum_{r=0}^t (d_v h_A)^r,
J_A = sum_{r=0}^t (h_A d_v)^r i_A = i_A,
H_A = h_A sum_{r=0}^t (d_v h_A)^r;

P_B = p_B sum_{r=0}^t (d_h h_B)^r,
J_B = sum_{r=0}^t (h_B d_h)^r i_B = i_B,
H_B = h_B sum_{r=0}^t (d_h h_B)^r.

The sums terminate because each repeated factor strictly lowers p or q. The unperturbed inclusions already commute with the complementary differential: d_v i_A=i_A d_A and d_h i_B=i_B d_B. Thus the induced differentials are exactly d_A and d_B, not unidentified effective differentials.

The resulting contractions obey

P_A J_A=I_A, I_T+J_A P_A=D_T H_A+H_A D_T,

and the analogous identities for B.

Define

F=P_B J_A:A->B,   G=P_A J_B:B->A,

H=P_A H_B J_A:A^j->A^{j-1},
K=P_B H_A J_B:B^j->B^{j-1}.

Then

F d_A=d_B F, G d_B=d_A G,
I_A+GF=d_A H+H d_A,
I_B+FG=d_B K+K d_B.

These identities follow by substituting the contraction identities. They hold on every cochain, not only cycles.

### Uniform locality and constants

If every elementary map above has row and column weight at most M>=1, a product of j maps has row/column weight at most M^j; a sum has at most the sum of these bounds. Both properties are essential: column sparsity controls physical error spreading, while row AND column sparsity control stochastic syndrome spreading.

For t=2, P_A,P_B,H_A,H_B have row/column weights <=3M^5, so F,G have weights <=3M^6 and H,K <=9M^11. These are deliberately crude. All are finite-range maps in the cell incidence graph. The constants are independent of the number of recursive levels only when D,b and the local basis conventions are uniformly bounded. Do not compose a level-dependent number of coarse-graining maps and call that uniformly local.

## 3. Local-stochastic syndrome pushforward

A random binary syndrome S is LS(q) if for every coordinate set T,

Pr[T subset supp(S)] <= q^{|T|}.

Let F^2 have row weight <=r and column weight <=c, with r,c>=1. Then F^2 S is LS(p), with

p=min(1,r q^{1/c}).

Proof: for every output coordinate in T that is nonzero, select one occupied input in its row. There are at most r^{|T|} selections. Any selection uses at least |T|/c distinct inputs, because one input reaches at most c outputs. Union bound and LS(q) give (r q^{1/c})^{|T|}. Cancellations cannot invalidate this upper bound.

For a commuting stabilizer Hamiltonian with equal-dimensional syndrome sectors, allowed syndromes form a binary linear space C and their Gibbs law is proportional to product_i q_i^{s_i}, q_i<=1. The supplied Walsh/coset-positivity lemma implies LS(q) with q=max_i q_i. This statement does not require independent checks. A projection onto one CSS sector preserves LS(q).

The pushforward F^2 S need NOT be a Gibbs syndrome law of B. No equality of Hamiltonians or Gibbs channels is assumed or concluded.

## 4. Decoder and exact logical-jump identity

Let R_B:im d_B^1 -> B^1 satisfy d_B R_B(s)=s. Define, for valid A syndromes,

R_A(s)=G^1 R_B(F^2 s)+H^2 s.

Because d_A s=0 and I+GF=d_AH+Hd_A, this is syndrome-correct:

d_A R_A(s)=G^2 F^2 s+d_A H^2 s=s.

For e in A^1 define the decoder jump

J_A(s,e)=R_A(s)+e+R_A(s+d_Ae).

It is a cycle. Expanding the formula and using the homotopy identity gives

J_A(s,e)=G^1 J_B(F^2s,F^1e)+d_A^0 H^1 e.

Therefore its logical class is exactly G_*[J_B(F^2s,F^1e)]. Since G_* is an isomorphism, the A jump is logically nontrivial if and only if the displayed B jump is. The H^2 s term is indispensable; omitting it generally yields a decoder with the wrong syndrome.

## 5. From single-step ANY-LS stability to bounded steps

Assume a genuinely distribution-uniform theorem for B: for every valid-syndrome law nu that is LS(p), and every single-coordinate physical error b,

Pr_nu([J_B(S,b)] !=0) <= epsilon_N(p).

An assertion only for B's Gibbs measure is insufficient.

Let a valid syndrome translation t have support size <=k. The translated law nu_t need not be LS(p). However, for 0<p<1,

nu_tilde=(1-p^k) delta_0+p^k nu_t

IS LS(p), since for nonempty T,

Pr_nu_tilde(T occupied) <= p^k p^{|T minus supp(t)|} <= p^{|T|}.

Both mixture components are valid syndromes. Hence any single-step instability event at S+t has probability at most p^{-k} epsilon_N(p).

Now decompose a bounded error v=b_1+...+b_L. Telescope its decoder jump through the prefix syndromes d_B(b_1+...+b_j). If every one-step jump is a boundary, so is their sum. If each physical coordinate creates at most w syndrome bits, every prefix translation has support <=wL, and

Pr_nu([J_B(S,v)] !=0) <= L p^{-wL} epsilon_N(p).

This proof avoids unjustified conditioning or an assumption that shifted local-stochastic laws remain local-stochastic.

## 6. Conditional thermal conclusion

Suppose an A bath jump has physical support <=a. With column weight of F^1 at most C, its image has weight L<=Ca. If A Gibbs syndromes are LS(q), the previous sections give

Pr_A-Gibbs([J_A(S,e)] !=0)
 <= L p^{-wL} epsilon_N(p),
 p=r q^{1/c}<1.

At any fixed sufficiently low positive temperature, r,c,C,w,a and p^{-wL} are constants independent of system size. Consequently, an exp(-Omega(N^eta)) uniform LS bound for B transfers with the same stretched-exponential exponent, up to constant factors and comparable-size conversion between A and B.

For a two-sector quantum lifetime result, apply the same argument separately to the physical X and Z decoder sectors, use a union bound (no independence required), and then invoke the relevant thermal-encoding/Davies or other explicitly assumed bath theorem converting Gibbs-weighted unstable jumps to a trace-norm/lifetime bound. Total bath rates and number of jump terms must be controlled, e.g. polynomially in N. This note does not prove that dynamical theorem or claim a ground-state initialization theorem.

## 7. What remains for the explicit ell=8 family

1. Supply the actual recursively compatible cell/sheaf atlas, including boundary and junction identifications, with uniform D,b.
2. Assemble both local augmented complexes for every atlas type; verify ranks, prescribed kernel embeddings, and all contraction identities.
3. Evaluate the finite formulas above; verify cochain-map and homotopy identities in coordinate matrices and record actual row/column bounds. Merely checking induced logical dimensions is inadequate.
4. Prove the desired decoder's instability witness bound for EVERY valid LS(p) syndrome law. A removable-witness Gibbs argument alone is insufficient; a witness union bound relying solely on occupied-set probabilities is sufficient.
5. Verify both sectors, size comparability, and bath-rate hypotheses; only then state the two-sector lifetime conclusion.

Thus the missing algebraic operation has a constructive resolution under local exactness and bounded atlas size. The outstanding scientific boundary is the explicit-family atlas certificate plus the genuinely distribution-uniform decoder-stability estimate, not an assumed universal lifetime duality.

## 8. Additional source check: the ANY-LS extension is immediate once witnesses are certified

In https://arxiv.org/html/2605.10943v1#S5.SS4, equations (218)–(220) are the Gibbs-specific step. Replace that step by Pr(T occupied)<=p^{|T|}; retain the deterministic witness enumeration and size estimates. Writing Delta for decoding-graph degree, D_level for its within-level degree, M for maximal local-complex size, set

A(p)=2(Delta+1)^2 [(1+p^{1/4})^M-1]^{1/(1+D_level^4)}.

The same counting yields

Pr(nonempty coarse syndrome) <= |V_2| sum_{m>=2^{k-1}} A(p)^m
 = |V_2| A(p)^{2^{k-1}}/(1-A(p)),

when A(p)<1. In particular A(p)<=1/2 gives <=2|V_2| 2^{-2^{k-1}}. Keep the constant seed prefactor |V_2| from Lemma 5.9 even though it disappears in the displayed equation (233). Do not rely on the further printed simplification (235); the unsimplified threshold is sufficient. This extension does not need witness removability, but DOES need the actual deterministic witness lemmas and the instability implication for the specific construction. It does not certify the ell=8 atlas by analogy.

## 9. Executable sanity check

Run `python verify_torus.py`. This independently assembles the square 3x3 torus double complex, obtains contractions by local Gaussian elimination, and verifies every perturbed contraction, cochain map, and both homotopy identities over F_2. Output on 2026-11-02:

```
F shape (36, 36) max row 4 max column 4
G shape (36, 36) max row 4 max column 4
H shape (36, 36) max row 2 max column 2
K shape (36, 36) max row 3 max column 3
PASS: all local contractions, perturbed contractions, cochain maps and two homotopies verified over F_2.
```

This is a nontrivial implementation sanity check, NOT a substitute for checking the requested family's junctions/boundaries.
