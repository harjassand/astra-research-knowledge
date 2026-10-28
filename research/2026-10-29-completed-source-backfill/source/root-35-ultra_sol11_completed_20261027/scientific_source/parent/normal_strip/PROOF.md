# An exact, useful normal strip for the calibrated convex operation

This is a root construction and independent consumer of the delivered exact
G26/G35 inputs. It is not an independent peer audit of its own code. The global
calibrated-operation theorem is developed separately in smooth_conic_interface
and independently challenged in calibrated_sos_review. No physical capability,
world novelty, or smoothness everywhere in R5 is claimed.

Use the old accepted quartic F and degree-six polynomial p from
support_gram_compiler/COMPILER_PROOF.md, literally rebuilt in certify.py.
Write T=|A|², q=det A and set

    κ=1/20000000, ε=1/100−κ, σ=1/34,
    H=F−κq², pH=p−2κqT², D=(T+σ)², E=H+εT.

The calibrated affine function is

    ell_A(B,s)=E(A)+(DE(A)−[pH(A)/D(A)]cof A):(B−A)
                         +[pH(A)/D(A)](s−q(A)).

Let V(B,s) be the infimum of t for which D(A)[t−ell_A(B,s)] is SOS
in the four variables A, degree at most8. The final compensated operation is
G(B,s)=V(B,s)+κ(|B|²+s²). Its graph energy is F(B)+(1/100)|B|².

## Exact result

    G(0,s)=κs² whenever |s|≤24999875/63245787552.

The halfwidth is approximately0.0003952812664313. A rational69 by69 Gram
on all nonconstant degree≤4 monomials is uniformly STRICTLY above
I/250000 on this entire strip. The omitted constant feature has a zero
row/column in the corresponding70-feature feasible Gram at t=0.

This gives more than a symbolic limit or Hessian-grid check. At s=1/10000,
the exact value is1/2000000000000000=5e−16, with a delivered rational
Gram and a matching point-evaluation dual lower bound.

## Homogeneous-block proof

Euler's identity gives

    D(A)[−ell_A(0,s)]
      = [3T²H−pH q]
        +[6σTH+εT³−s pH]
        +[3σ²H+2εσT²]+εσ²T.                         (1)

The four brackets have degrees8,6,4,2. They have block-diagonal Grams
in the ordinary degree4,3,2,1 monomial bases of sizes35,20,10,4.

The bottom10 principal block GF of the supplied G26 represents F exactly
and is strictly above I/25000. Thus GFH=GF−κ vvᵀ, v the coefficients
of q, represents H and is strictly above(1/25000−2κ)I because |v|²=2.
Multiplication by T is the sum of four explicit monomial congruences and
therefore preserves the SOS property.

The supplied G35 represents3T²F−pq and is strictly above I/200000.
Subtracting κ wwᵀ, with w the quartic coefficient vector of Tq and
|w|²=8, gives a Gram G8 for3T²H−pHq strictly above

    (1/200000−8κ)I=(23/5000000)I.

The literal coefficient l1 norm of p is P=1976430361/156250000.
The coefficient l1 norm of qT² is32. Hence ||pH||coeff,1≤Pbar=P+64κ.
A canonical cubic-monomial Gram Gp for pH assigns each degree6 monomial
to one pair of cubic features. Its maximum absolute row sum is at most
||pH||coeff,1, so ||Gp||2≤Pbar. The degree6 block is

    G6(s)=6σ G_TH+ε G_T³−s Gp ≥(ε−|s|Pbar)I,

since G_TH is PSD and the multinomial diagonal Gram G_T³ is at least I.
Thus G6(s)≥(ε/2)I for |s|≤ε/(2Pbar), the stated rational strip.
The degree4 block is at least2εσI, and the degree2 block is εσ²I.
All four lower bounds exceed1/250000. This proves the uniform69 margin.

The explicit block Gram proves V(0,s)≤0. Evaluation at A=0 gives
ell_0(0,s)=0 and D(0)=σ²>0, so every SOS-feasible t satisfies t≥0.
The matching bound is attained by the delivered Gram: V(0,s)=0.

## Matched ordinary finite-operation control

Apply the earlier15-moment all-support operation to the SAME compensated
energy E, then add the SAME κ(|B|²+s²). At B=0 its constraints give
E q=s. Positivity of the quadratic moment matrix gives E T≥2|s|.
Since H is SOS, its value is therefore at least

    2ε|s|+κs².                                        (2)

An explicit feasible two-atom measure uses A=±sqrt(|s|)diag(1,sign s),
with equal weights. All degree≤4 moments are rational when s is rational;
its mean is0, determinant expectation s, and moment matrix is PSD by its
actual two-atom representation. This yields the upper bound

    2ε|s|+[2p0+p2−κ]s²+κs².                          (3)

At nonzero s in the strip, (2) is strictly greater than the calibrated value.
The two operations agree on the minors graph but extend it differently.
This proves a useful smooth-versus-corner distinction. It does not establish
a speed advantage over a best ordinary SOS solver or a new general SOS method.

## Evidence and costs

certify.py imports only the standard library. It rebuilds F,p,H,pH and (1)
with Fraction arithmetic; checks the literal GF and G35 input identities;
proves the compensated GF/G35 margins by exact LDL; checks the cubic-Gram
row bound; and verifies every coefficient of (1) at both strip ends and at
s=0,±1/10000. Separate exact LDL checks also prove both endpoint degree6
blocks above I/250000. The uniform interval proof is the analytic row-bound
argument above, rather than interpolation from finitely many points.

EXACT69_QUERY_BLOCKS.json contains all rational blocks and ordered features
for s=1/10000. RESULT.json records exact values, matched ordinary bounds,
input hashes, certificate hash and a measured0.071s consumer run including
source loads and exact LDL. Interpreter startup and historical acquisition
of the supplied G26/G35/R180 inputs are separate costs. No70-SDP solve was
needed for these normal-strip evaluations.
