# Exact cubic counts over characteristic-two chain rings

## Scope and prior work

Let `R_e = F_q[t]/(t^e)`, `q=2^d`, be presented by an irreducible binary
polynomial for the coefficient field, and let

\[
\psi_e(x)=(-1)^{\operatorname{Tr}_{F_q/F_2}(x_{e-1})}.
\]

The pairing `(x,y) -> Tr([t^(e-1)]xy)` is nondegenerate. Ring coordinates are
inputs to this note; acquiring them from a raw Boolean polynomial is a separate
compiler stage. This backend never enumerates the `q` field elements or the
`q^e` ring elements.

The stationary-phase method is established prior work. A particularly close
primary reference is Will Sawin, *The size of wild Kloosterman sums in number
fields and function fields*, arXiv:2209.02170v2 (2023-05-31), Sections 2–3,
https://arxiv.org/pdf/2209.02170. Its local-ring setting includes the rings here.
We give an elementary exact coefficient algorithm and a complete proof because
the extracted magnitude bound in its characteristic-two boundary case is
incompatible with an eight-term example below. No bound from that source is
used in this construction. The arXiv abstract page checked on 2026-10-27 lists
v2 as the latest revision; a targeted erratum search found none. Absence of a
search result is not proof that no correction exists.

At chain length one the backend calls the earlier implemented finite-field
Dwork Kloosterman counter. That dependency is established machinery, not a new
point-counting algorithm.

## The exact counter

**Theorem.** For arbitrary coefficients `A,B,C,D,E,F,G in R_e` and a unit
`lambda in R_e`, the integer

\[
 Z=\sum_{x,y,z\in R_e}
 \psi_e(\lambda xyz+Axy+Bxz+Cyz+Dx+Ey+Fz+G)
\]

is computable deterministically in time polynomial in `e,d`, with polynomial
space. The input is eight coefficient lists of `e` field elements and a field
modulus; its length is `O(ed)` bits. The number of original independent Boolean
inputs is `n=3ed`, and the exact zero count is `(2^n+Z)/2`. Intermediate integer
answers have `O(ed)` bits. There is no enumeration of internal program states.

With schoolbook field arithmetic, an explicit conservative bound for this
implementation, using the prior `O(d^8)` bit Dwork backend, is

\[
 O(e^4d^2+ed^8)+\operatorname{poly}(ed)
\]

bit operations. This is a structural algorithm bound, not a claim of practical
advantage against an equally informed ring-aware implementation.

### 1. Normalize the polynomial

Scale `z'=lambda z`. Replace `B,C,F` by `B/lambda,C/lambda,F/lambda`. Now
translate `x=X+C`, `y=Y+B`, `z'=Z+A`. Characteristic two gives

\[
 XYZ+aX+bY+cZ+g,
\]

where

\[
 a=D+AB,\quad b=E+AC,\quad c=F+BC,
 \quad g=G+DC+EB+FA.
\]

Summing over `Z` uses nondegeneracy of the character:

\[
 Z=|R_e|\psi_e(g)S_e(a,b;c),\qquad
 S_e(a,b;c)=\sum_{xy=c}\psi_e(ax+by).
\]

The change of coordinates is bijective, so it preserves the original count.

### 2. Include every nonunit fiber

Write `v(0)=e` and define

\[
 K_e(A,D)=\sum_{x\in R_e^\times}\psi_e(Ax+D/x).
\]

For `k<e`, set `x=t^ku` with `u` a unit of `R_(e-k)`. Such an `x` can satisfy
`xy=c` only when `v(c)>=k`. When this holds, all solutions are

\[
 y=(c/t^k)u^{-1}+t^{e-k}w,\quad w\in R_k.
\]

The sum over `w` vanishes unless `v(b)>=k`; otherwise it contributes `q^k`.
Consequently

\[
 S_e(a,b;c)=q^e\,1_{b=c=0}+
 \sum_{0\le k\le\min\{v(b),v(c),e-1\}}
 q^k K_{e-k}\left(a\bmod t^{e-k},
       (b/t^k)(c/t^k)\bmod t^{e-k}\right).
\tag{1}
\]

This formula handles `c=0`, including the `x=0` fiber. In particular it returns
`q^e+e(q-1)q^(e-1)` for the number of pairs with `xy=0`.

### 3. Reduce arbitrary Kloosterman coefficients

If `s=min(v(A),v(D))<e`, then

\[
 K_e(A,D)=q^s K_{e-s}(A/t^s,D/t^s).
\tag{2}
\]

If both coefficients are zero, `K_e=(q-1)q^(e-1)`. After (2), at least one
coefficient is a unit. For reduced length one, a single nonzero coefficient
has sum `-1`. For reduced length at least two, exactly one unit coefficient
forces zero: translation of the unit variable by `t^(e-1)h` leaves only the
nonzero derivative `A_0+D_0/x_0^2` in the top trace, whose sum over `h` vanishes.
If both are units, scale `v=Ax` and obtain

\[
 K_e(A,D)=K_e(1,AD).
\tag{3}
\]

We therefore need only the unit-parameter sum `K_e(1,u)`.

## Polynomial acquisition of the stationary center

Assume `e>=2` and `u` a unit. Set

\[
 c=\lceil e/3\rceil,\qquad z=\lceil(e-1)/3\rceil,
 \qquad f(x)=x+u/x.
\]

For any unit `a` and any `y in t^c R_e`, all powers `y^j`, `j>=3`, vanish,
so

\[
 f(a+y)-f(a)=U(a)y+V(a)y^2,
 \quad U(a)=1+u/a^2,\quad V(a)=u/a^3.
\tag{4}
\]

This is an additive polynomial in the binary vector `y`. Its character is
identically one precisely when, for every `0<=i<=e-1-c`,

\[
 U(a)_i+
 \begin{cases}
 \sqrt{V(a)_{2i-e+1}},&2i-e+1\ge0,\\
 0,&2i-e+1<0
 \end{cases}=0.
\tag{5}
\]

To prove (5), put `y=sum_(j>=c) y_jt^j`. In the top coefficient, the variable
`y_j` contributes
`U_(e-1-j)y_j+V_(e-1-2j)y_j^2`. The field identity
`Tr(v y^2)=Tr(sqrt(v)y)` gives the stated condition. The square root is the
unique field square root, computable by `d-1` squarings.

### Why only one short center is possible

Condition (5) depends only on `a mod t^z`. Indeed the mixed second difference
of `f` for shifts `y in t^c` and `h in t^z` begins with `y^2h+yh^2`;
`2c+z>=e` and `c+2z>=e` in all three residue classes of `e mod 3`. Higher
terms vanish too. Equivalently the coefficients in (5) are unchanged.

The coefficient `a_0` must satisfy `a_0^2=u_0`, fixing its nonzero value.
Suppose `a_0,...,a_(j-1)` are fixed and temporarily set `a_j=0`. Use the
condition (5) at `i=2j`. The coefficient of `V` involved is `4j-e+1<j`
for `j<z`, so it is already determined. Replacing `a_j` by `alpha` changes
`U_(2j)` by `alpha^2/a_0^2` and changes no earlier condition. Therefore

\[
 a_j=a_0\sqrt{U(a)_{2j}+
              1_{4j-e+1\ge0}\sqrt{V(a)_{4j-e+1}}}.
\tag{6}
\]

The index `2j` is always in the range of (5) for `j<z`. Thus (6) manufactures
the only possible center, using polynomially many field operations. After
constructing all its `z` coefficients, test every equation (5), including
all odd-indexed equations. If any fails, `K_e(1,u)=0`. This is a complete
acquisition algorithm, not an assumption that a critical center is supplied.

## Reconstruct the exact sum

Every coset modulo `t^c` has either zero sum or a constant character times
`q^(e-c)`. Only cosets whose center reduces to the acquired `a mod t^z` can
survive.

If `c=z`, exactly one coset survives and

\[
 K_e(1,u)=q^{e-c}\psi_e(f(a)).
\tag{7}
\]

Otherwise `e=3z+1`, `c=z+1`, and the surviving cosets have representatives
`a+t^z w`, `w in F_q`. The expansion now keeps precisely the cubic term:

\[
 f(a+t^zw)=f(a)+U(a)t^zw+V(a)t^{2z}w^2+
                         (u/a^4)t^{3z}w^3.
\]

Only the constant coefficient of `u/a^4` contributes to the cubic term.
Define

\[
 \beta=U(a)_{2z}+\sqrt{V(a)_z},\qquad
 \gamma=u_0/a_0^4=a_0^{-2}.
\]

Then

\[
 K_e(1,u)=q^{e-c}\psi_e(f(a))
          \sum_{w\in F_q}(-1)^{\operatorname{Tr}(\gamma w^3+\beta w)}.
\tag{8}
\]

The last function is **quadratic over F2**: `w^3=w*w^2`, and squaring is
binary linear. Its constant, `d` unary values, and `d(d-1)/2` pair values
acquire its Boolean quadratic form. Ordinary exact quadratic elimination
computes the integer Gauss sum in polynomial time and space. The code uses
`sum_(x,y) (-1)^(xy+xA+yB)=2(-1)^(AB)` to eliminate one quadratic pair at a
time, preserving signs and zero cases. No `q`-point sum is executed.

### Cost accounting

One ring inverse uses `O(e^2+d)` field operations by coefficient recurrence.
There are `O(e)` center coefficients. Derivatives and tests therefore cost
`O(e^3+ed)` field operations. Acquiring the final Boolean quadratic uses
`O(d^3)` field operations including traces, and its elimination uses
`O(d^4)` elementary bit work with packed masks. Equation (1) makes at most
`e` Kloosterman calls. The finite-field calls use the earlier exact Dwork
backend. These estimates give the theorem's conservative bound. The result
and every partial sum have `O(ed)` bits; all arrays have polynomial size.

## Decisive source-bound limitation

Take `R=F_2[t]/t^4`, `u=1+t^2`, and the primitive character
`psi(x)=(-1)^[t^3]x`. Every unit has a unique expression

\[
 x=1+at+bt^2+ct^3,\quad a,b,c\in F_2,
\]

and

\[
 x^{-1}=1+at+(a^2+b)t^2+(a^3+c)t^3.
\]

Thus the `t^3` coefficient of `x+(1+t^2)/x` is `a^3+a=0`, so all eight
terms are `+1` and `K_4(1,1+t^2)=8` exactly. In the displayed source bound,
`p=k=2`, `n=4`, `c=2`, `c_tilde=1`, `k*=1` give `2^(5/2)`, whose square is
32; the actual squared sum is 64. The eight terms are saved in the executed
JSON. This is a limitation of that displayed bound; no claim is made about
uninspected versions or an author's intended hypothesis.

The mechanism is visible in (8). The polar radical of `Tr(gamma w^3)` is

\[
 \{w:\gamma^2w^4+\gamma w=0\}.
\]

Its binary dimension is one when `d` is odd; when `d` is even it is two if
`gamma` is a cube and zero otherwise. The quadratic Gauss sum is either zero
or has magnitude `2^((d+r_rad)/2)`, so replacing it by `sqrt(q)` can lose a
factor `sqrt(2)` or `2`. Our exact elimination retains the radical and sign.

## Executed evidence

`chain_ring_checks.py` uses independent exhaustive ring enumeration only as
an oracle. The production functions in `chain_ring_kloosterman.py` do not.

- 1,266 complete unit-parameter comparisons: F2 lengths 2–9, F4 lengths 2–4,
  F8 lengths 2–3.
- 350 arbitrary-parameter Kloosterman comparisons, including zero/nonunit
  coefficients and reductions to length one.
- 240 arbitrary product-fiber comparisons, including the zero product.
- 50 complete three-ring-variable cubic counts with arbitrary lower terms
  and unit leading coefficient.
- A second center-acquisition audit reconstructs 74 arbitrary nonconstant
  planted centers from `u` alone; 70 of these also match a complete unit-sum
  oracle. Four runs use `d=32` and lengths 16,31,64,128; the final length-128
  nonconstant-center run took about 5.3 seconds diagnostically.
- Four initial large structured backend runs at `d=32`, chain lengths 16,31,64,128,
  corresponding to 1,536,2,976,6,144,12,288 Boolean input bits. These are
  coefficient-representation backend executions, not raw-ANF acquisition
  demonstrations. Some sums are zero; the length-31 and length-128 sums are
  nonzero and stored exactly. No field/ring points were enumerated.

These checks establish finite agreement and implementation evidence. They
are not comparative performance benchmarks or an empirical proof of the
asymptotic theorem. The theorem follows from (1)–(8).
