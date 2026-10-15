# Independent audit: generic binary acquisition and shifted-margin certificate

Audit date: 2026-10-15.

## Disposition

The main generic binary acquisition theorem, its finite-extension degree bound, and its query-count argument are valid. No counterexample to the main theorem was found. The shifted-margin certificate is also valid with the norm definitions stated below. The original anchor-context paragraph should use N854 section 3, rather than directly applying section 4's singular-gauge cycle example to the normalized parameter family.

## 1. Explicit proof of the finite-extension degree lemma

Let k be an infinite characteristic-zero field and let L=k(h_1,...,h_N) be a subfield of k(x_1,...,x_n), where each h_i has numerator and denominator degree at most d. Suppose h_1,...,h_r are a transcendence basis of L/k, and put F=k(h_1,...,h_r).

### A coordinate slice suffices

By the characteristic-zero Jacobian criterion, the Jacobian of h_1,...,h_r has a nonzero r-by-r minor. Relabel variables so its columns are x_1,...,x_r. Specialize x_(r+1),...,x_n to constants in k while preserving the nonzero numerator of this minor and every original h_i denominator as nonzero polynomials in the retained variables.

Such constants exist. The product of the finitely many relevant nonzero polynomials is nonzero. At least one coefficient of this product as a polynomial in the retained variables is a nonzero polynomial in the variables being specialized. Over an infinite field it is nonzero at some constant specialization.

The resulting coordinate slice E is affine r-space. The restricted h_1,...,h_r remain algebraically independent.

### Restriction embeds the entire response field

Set A=k[h_1,...,h_N], an affine domain of dimension r. Restriction defines a homomorphism A -> k(E). Its image has transcendence degree r. Its kernel is zero, because quotienting an affine domain by a nonzero prime strictly lowers dimension. Thus restriction extends to an embedding L -> k(E).

This step is important: one should not simply presume every denominator of every element of L survives a restriction. Dominance/injectivity proves it.

### Bezout gives the bound

The extension k(E)/F is finite. For independent generic target values y_j, its generic fiber, away from denominator zeros, is cut out by

    N_j(z) - y_j D_j(z) = 0,  j=1,...,r.

All these equations have degree at most d. Characteristic zero makes the generic finite extension separable, so the geometric generic fiber has [k(E):F] distinct points. Each is an isolated solution of the cleared equations: in its neighborhood the denominators are invertible and the fiber is zero-dimensional.

Bezout bounds this number by d^r, even when the cleared equations also have components supported on denominator-zero sets. Hence

    [L:F] <= [k(E):F] <= d^r.

For r=0, the only elements of k(x_1,...,x_n) algebraic over k are in k, so L=k.

The document's generic affine-hyperplane argument has the same valid conclusion. The coordinate-slice proof makes the existence and field-embedding steps more explicit.

### Sharpness of the abstract lemma

Take h_1=x_1^d,...,h_r=x_r^d and additionally include x_1,...,x_r. Then L=k(x_1,...,x_r) and [L:F]=d^r. Improvement of this bound requires additional structure beyond general degree-d rational functions.

## 2. Application and constructive query count

For the normalized binary map, each g_S has denominator degree at most |S| and numerator degree at most |S|-1 in B, hence the uniform bound d=m is valid.

Every genuine field enlargement E -> E(g_S) has degree at least two. After t such steps, 2^t <= D=[L:F], so t <= floor(log_2 D). Once every original generator has been scanned, the final field is L. This proves rational reconstruction of every output, not merely finitely many candidate tables.

The resulting bound is

    Q <= 1 + m + r + floor(log_2 D)
      <= 1 + m + n + floor(n log_2 m), n=m(m-1).

Duplicates only reduce the distinct query count, and querying all 2^m settings supplies the stated minimum bound when preferable.

The exact symbolic computations are legitimate over Q(a_1,...,a_m). Algebraic independence, graph elimination, and finite-extension degree computations are decidable. Once field equality is established, enumeration of rational-expression candidates and exact identity testing is a terminating reconstruction procedure. None of this supplies an efficient algorithm.

Treating a as indeterminates does not make selection depend on plant measurements. The symbolic procedure is fixed by m and its chosen scan order. Coefficient denominators involving a, target reconstruction denominators, and physical singularities exclude only finitely many proper algebraic sets. Their product is nonzero, so a nonempty simultaneous generic domain remains, including real points.

## 3. Exact small examples

For m=2,

    g12 = (a1+a2-a1*b12-a2*b21)/(1-b12*b21).

It is nonconstant, so r=1, L=k(g12), and D=1. This construction uses all four settings.

For m=3, specialize a=(1,2,3), b12=t, and every other B entry to zero. The Jacobian of (g12,g13,g23,g123), with columns (b12,b13,b23,b31), is

    [-1  0    0      0   ]
    [ 0 -1    0     -3   ]
    [ 0  0   -2      0   ]
    [-1 -1   t-2   3t-3  ].

Its determinant is -6t. All binary inverses exist at this specialization. Thus all four nonsingleton responses are algebraically independent, r=4 and D=1; the construction uses all eight settings.

## 4. Anchor-context paragraph: normalization caveat and corrected example

N854 section 4 explicitly uses w=v=e1. Its diagonal gauge W=diag(w) is singular. Therefore that example cannot simply be asserted to belong to the normalized family g_S=a_S^T(I+B_SS)^(-1)1 through the stated gauge construction. It remains a valid example for the broader original physical family; the issue is the scope of its use here.

N854 section 3 gives a direct replacement inside the normalized family. Take

    H  = [[10, 1/5, 1/2], [3/10, 10, 11/10], [7/10, 13/10, 10]],
    H' = [[10, 1/5, 21/10], [3/10, 10, 11/10], [1/6, 13/10, 10]],
    a_original=(1,2,3), w=(1,1,1), t=1.

Only edge {1,3} is switched. Its product and weighted sum are unchanged:

    H13*H31 = H'13*H'31 = 7/20,
    a1*H13+a3*H31 = a1*H'13+a3*H'31 = 13/5.

Consequently all singleton and pair responses agree. Both matrices are strictly accretive: their symmetric parts have leading principal minors respectively

    (10, 1599/16, 196347/200),
    (10, 1599/16, 1751059/1800).

Normalize by a=a_original/11, B=(H-10I)/11 and B'=(H'-10I)/11. These have zero diagonal and give exactly the same t=1 binary responses as the original models. All binary inverses exist.

The full three-node response reductions are exactly

    g123  = 623490/1311109,
    g'123 = 1875110/3934847,
    g123-g'123 = -5135840960/5159013315323 != 0.

The rational values and symmetric leading minors were independently recomputed with exact arithmetic during this audit.

Place this three-node block outside the anchor set and disconnect it from the anchors. Every anchor-context query containing at most two non-anchor controls sees identical responses in the two models, while the full three-node block separates them. Thus universal anchor-context identification fails within the normalized family. This nongeneric counterexample does not refute generic identification or the acquisition theorem.

## 5. Shifted-margin extension

Audited file: ../binary_prediction_certificate/SHIFTED_MARGIN.md.

Use ||x||_Lambda=(x^T Lambda x)^(1/2), the corresponding induced operator norm, and the dual vector norm ||a||_(Lambda^-1). Interpret sym_Lambda(M) as sym(Lambda^(1/2) M Lambda^(-1/2)). Lambda must be positive diagonal.

### Control-cube resolvent estimate

For positive diagonal D<=UI,

    D(I+HD)^(-1) = (D^(-1)+H)^(-1).

Since D and Lambda commute, weighted similarity leaves D^(-1) unchanged. If sym_Lambda(H)>=hI, then the symmetric part of the transformed D^(-1)+H is at least (1/U+h)I. For positive shifted margin mu=1/U+h, the inverse norm is at most 1/mu. No condition h>=0 is required.

When D has zero coordinates, reordering into active/inactive coordinates shows D(I+HD)^(-1) equals the active inverse block, zero padded. Principal compression preserves the accretivity bound, so the same estimate holds. The zero-coordinate treatment is valid specifically because the metric is diagonal.

### Binary prediction bound

State the error definitions explicitly:

    e0 >= |f0-fhat0|,
    ea >= ||a-ahat||_(Lambda^-1),
    eB >= ||B-Bhat||_Lambda,
    kappa_hat > eB,
    kappa=kappa_hat-eB.

If sym_Lambda(I+Bhat)>=kappa_hat I, then sym_Lambda(I+B)>=kappa I by the induced-norm perturbation bound. Every principal block inherits these bounds. Thus the zero-padded active inverses T_B and T_Bhat satisfy

    ||T_B||_Lambda <= 1/kappa,
    ||T_Bhat||_Lambda <= 1/kappa_hat,
    ||T_B-T_Bhat||_Lambda <= eB/(kappa*kappa_hat).

The last bound follows from the resolvent identity on each active block. Decompose

    a^T T_B 1 - ahat^T T_Bhat 1
      = (a-ahat)^T T_B 1 + ahat^T(T_B-T_Bhat)1.

Weighted Cauchy-Schwarz gives exactly the stated prediction certificate. The all-ones norm can be replaced by the active indicator norm for a subset-specific sharper bound.

### Physical existence and the diagonal metric

Let M=t^(-1)I+H0 and L=diag(M_ii). Since sym(A)>0,

    sym(A^(-1)) = A^(-T) sym(A) A^(-1)>0.

Thus sym(H0)>=0 for arbitrary P, and sym(M)>0 because t>0. In particular L>0. With I+B0=M L^(-1) and Lambda0=L^(-1),

    Lambda0^(1/2)(I+B0)Lambda0^(-1/2)
      = L^(-1/2) M L^(-1/2),

whose symmetric part is positive definite.

For nonsingular real diagonal W, set B=W^(-1)B0 W and Lambda=W^2 L^(-1). Write J=diag(sign(W_ii)), so Lambda^(1/2)=|W|L^(-1/2). Direct multiplication gives

    Lambda^(1/2)(I+B)Lambda^(-1/2)
      = J L^(-1/2) M L^(-1/2) J.

This is orthogonal sign-diagonal similarity of the positive-accretive matrix above. The proposed metric Lambda=W^2 L^(-1) is therefore correct, including negative entries of W.

The witness depends on unknown physical quantities and is not supplied by binary observations. The certificate requires an independently verified common metric and parameter enclosure. It does not establish acquisition, noise-robust identifiability, efficient optimization, or any new physical capability.
