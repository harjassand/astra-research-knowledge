# Complete cubic ratio correction: exact construction and two real obstructions

**Author component; independently unreviewed.** All earlier freezes are untouched.
This is the complete residual construction, not a correction of only the literal
-RA term. The broad-domain inward claim is false for the canonical construction.
A separately stated adaptive/count-gated repair is in
`ADAPTIVE_CONDITIONAL_DRIFT_AND_BRACKET.md`.

## 1. Actual task and algebraic reference

Let S=A+B+C+D+E be the actual total; N is a fixed reference and T=N^(1/5).
Put L=A+(C+D)/2, Z=C-D and

    R=E²/(NL),
    F1=R-RAE/(NL),
    D0=(EL/N)(4-3R)-R/L.

Every actual channel is retained. The complete residual

    P(A;L,E,Z,S,N)=G F1-D0

is a polynomial in A of degree at most three when the other arguments are held
as algebraic parameters. Actual C,D,B are expressed as

    C=L-A+Z/2, D=L-A-Z/2, B=S-2L+A-E.

The cubic is generally nonzero. We acquire all its coefficients; none of its
O(A), O(A²), or O(A³) terms is silently dropped.

Define the coupling-adapted algebraic operator

    λ0=1+3L²-3Z²/4, k=S+2L-E-2, β=E,
    Qc f=(λ0+βA)[f(A+1)-f(A)]
         +(k+β)A[f(A-1)-f(A)].

Require k>0. No stationary/conditional Poisson or negative-binomial law is
assumed. With (A)_j=A(A-1)…(A-j+1), direct finite differences give

    Qc(A)_j=-jk(A)_j+j[λ0+(j-1)β](A)_(j-1), j=1,2,3.

Expand the exact residual in this basis,

    P=c0+c1(A)_1+c2(A)_2+c3(A)_3.

If P=p0+p1A+p2A²+p3A³ then
c0=p0, c1=p1+p2+p3, c2=p2+3p3, c3=p3. Equivalently the c_j are the exact
forward differences of P at A=0, divided by j!.

Set

    M0=1,
    M1=λ0/k,
    M2=λ0(λ0+β)/k²,
    M3=λ0(λ0+β)(λ0+2β)/k³,
    Pbar=c0+c1M1+c2M2+c3M3,

    d3=c3/(3k),
    d2=[c2+3(λ0+2β)d3]/(2k),
    d1=[c1+2(λ0+β)d2]/k,
    χ=d1(A)_1+d2(A)_2+d3(A)_3,
    F2=F1+χ.                                             (1)

Then Qcχ=-(P-Pbar) exactly. The zero-at-A=0 convention fixes the parameter-
dependent additive gauge. The M_j are algebraic centering constants, not moments
asserted for the actual chain.

## 2. Exact full residual after the complete correction

The actual/reference A-rate discrepancies are

    δ_+=A²-4AL, δ_-=4A²-4AL.

Let p=(L,E,Z,S), and let a_r=ΔA and Δp_r denote each full actual reaction jump.
Then

    G F2=D0+Pbar+E_fast+E_param,
    E_fast=Σ_(j=1)^3 j d_j
              [δ_+(A)_(j-1)-δ_-(A-1)_(j-1)],
    E_param=Σ_r λ_r Σ_(j=1)^3 (A+a_r)_j Δ_r d_j.          (2)

The actual-minus-reference term has degree up to four. The parameter term is
not frozen. In particular AB↔CD have Δp=0 and contribute nothing to E_param,
but retain their actual jumps and bracket. Equation (2), not its algebraic mean
alone, is the actual drift to test.

## 3. A compact exact rational acquisition formula

For reproducible arithmetic define

    r=R, u=E/N, t=1/L, a=A/L, z=Z/L, s=S/N.

Then N=r/(u²t), E=r/(ut), A=a/t and F1=r(1-au). Every channel has rate
λ_r=t^-2 q_r(a). The table supplies all q_r and physical jumps
(ΔA,ΔL,ΔE,ΔZ,ΔS):

| channel | q_r | jump |
|---|---|---|
| 0→A | t² | (1,1,0,0,1) |
| A→0 | at | (-1,-1,0,0,-1) |
| 2A→AC | a(a-t) | (-1,-1/2,0,1,0) |
| AC→2A | a(1-a+z/2) | (1,1/2,0,-1,0) |
| 2A→AD | a(a-t) | (-1,-1/2,0,-1,0) |
| AD→2A | a(1-a-z/2) | (1,1/2,0,1,0) |
| 2A→AE | a(a-t) | (-1,-1,1,0,0) |
| AE→2A | ar/u | (1,1,-1,0,0) |
| AE→CD | ar/u | (-1,0,-1,0,0) |
| CD→AE | 2[(1-a)²-z²/4] | (1,0,1,0,0) |
| CD→AB | (1-a)²-z²/4 | (1,0,0,0,0) |
| AB→CD | a(sr/u²-2+a-r/u) | (-1,0,0,0,0) |

For a row with increments (b,v,w,*,*) put c=1+wut/r and h=1+vt. Its exact
F1 jump is affine in a:

    ΔF1=J0+J1 a,
    J0=r(c²/h-1)-rut b c³/h²,
    J1=-ru(c³/h²-1).

If q_r=q_(r,0)+q_(r,1)a+q_(r,2)a², the coefficients p_j of the normalized
complete residual [GF1-D0]/(EL/N) are the explicit rational sums

    p_j=(1/(ut))Σ_r[q_(r,j)J0+q_(r,j-1)J1]
          -1_(j=0)[4-3r-rt²/u],                          (3)

with absent q coefficients zero. This is a finite twelve-row computation, not
an oracle for the residual.

For the normalized falling basis P_j(a)=a(a-t)…(a-(j-1)t), set

    K=s-u+2u²(1-t)/r, Λ=3-3z²/4+t²,
    μ=u²Λ/(rK), η=tu/K, bscale=u³/(rK),
    c0=p0, c1=p1+t p2+t²p3, c2=p2+3t p3, c3=p3,
    D3=bscale c3/3,
    D2=bscale c2/2+(3/2)(μ+2η)D3,
    D1=bscale c1+2(μ+η)D2.

The same χ is

    χ=D1P1(a)+D2P2(a)+D3P3(a)=h1 a+h2 a²+h3 a³,
    h1=D1-tD2+2t²D3, h2=D2-3tD3, h3=D3.                 (4)

The normalized algebraic drift is

    Dbar=4-3r-rt²/u
       +c0+c1μ+c2μ(μ+η)+c3μ(μ+η)(μ+2η).                 (5)

`derive_complete.py` acquires these exact expressions. Literal expanded rational
formulas are saved in `exact_formulas.txt`; the pure-Fraction evaluator is
`exact_fraction_coefficients.py`. The small formulas (3)-(5) are preferable for
understanding and independently rebuilding the object.

## 4. Actual shifts and costs are not hidden inside a mean

For an actual row (b,v,w,q,d), let c=1+wut/r, h=1+vt. The transformed endpoint is

    r'=rc²/h, u'=uc, t'=t/h,
    a'=(a+bt)/h, z'=(z+qt)/h, s'=s+du²t/r.               (6)

Thus the exact actual drift and bracket can be evaluated directly as

    GF2/(EL/N)=Σ_r q_r [F2(x')-F2(x)]/(ut),
    Γ(F2)=Σ_r q_r [F2(x')-F2(x)]²/t².                    (7)

Alternatively use (2). For a stopped coefficient/derivative budget, let

    D_A=Σ_j j|d_j|(A+1)^(j-1),
    H_k=Σ_j(A+1)^j sup_segments|∂_(p_k)d_j|.

Then the honest pointwise charges include

    |E_fast|<=8AL D_A,
    |E_param|<=H_L s_L+H_E q_EE+H_Z q_Z+H_S(1+A),
    Γ(χ)<=2D_A² q_A+8[H_L²q_LL+H_E²q_EE+H_Z²q_Z+H_S²(1+A)].

These are actual generator charges. No parameter-shift term or fast-channel
bracket has been removed. A sharper uniformly paid endpoint/bracket certificate
is supplied in the companion adaptive note; the bracket certificate itself is
valid on the original broad domain.

## 5. The requested broad-domain sign statement is false

Consider the originally proposed full domain

    .99N<=S<=1.01N, E/N<=.01, A<=L/100, |Z|<=L/100,
    R∈[1/2,2], E^5>=32N³, L>=100.

The canonical complete cubic inverse (1) has exact outward witnesses in this
domain. Examples, with every other count recovered from the displayed formulas:

| R | L | u=E/N | S/N | A/L | rigorous GF2/(EL/N) |
|---|---:|---:|---:|---:|---|
| 2 | 10^6 | 10^-6 | .99 | .01 | (6,7) |
| 1/2 | 10^8 | 10^-8 | 1.01 | .01 | (-47,-46) |
| 1.99 | 10^6 | 10^-6 | .9901 | .0099 | (5,7) |
| .51 | 10^8 | 10^-8 | 1.0099 | .0099 | (-49,-46) |

Z=0 in each case. N=rL/u², E=uN, A=aL, C=D=L-A, S=sN, and
B=S-A-C-D-E are all nonnegative integers. The latter two witnesses lie strictly
inside the stated R, A, and total-count bounds. The exact algebraic mean has the
inward sign in all four cases; the actual parameter-motion remainder reverses it.

`verify_exact_witnesses.py` proves these signs by Fraction arithmetic, checks every
domain inequality and exact reference/full-generator decomposition, and stores
`exact_counterexamples.json`. This is an exact negative answer to the broad
uniform statement, not a finite-grid positivity argument.

The same two original face states have inward signs when S is replaced by N or
N±100 floor(N^(1/5)); six exact replays are in
`narrow_count_band_replays.json`. That removes the first counterexample mechanism
but does not yet close the pointwise theorem.

## 6. A second obstruction survives even at S=N

Set R=1/2, L=10^8, u=128/L², A=L/100, Z=0, S=N. Then
N=L^5/32768 and E=L³/256 are integers, and E^5=32N³ exactly. Yet

    -57 < GF2/(EL/N) < -56,
    2 < Dbar < 3,
    |F2-R| <10^-14.

The AE→2A parameter-motion contribution alone is about -58.593509 in these
normalized units. A strict-interior variant R=.51, A=.0099L, the same u and
L, has E^5/N³=33.2928>32 and corrected drift in (-59,-56), again S=N.
`verify_critical_witness.py` proves both signs exactly and saves
`critical_exact_counterexamples.json`.

The mechanism can be seen without treating the reference mean as a chain law.
At S=N, Z=0 and u=K t² with fixed r,a,K, the exact coefficients have

    h1=rK t³+O(t⁴), h2=O(t⁴), h3=O(t⁶).

The AE→2A parameter change therefore creates the leading normalized term

    -3a²r² t/u=-3R²[A²N/(L³E)].                          (8)

A fixed A/L cap does not bound this quantity near the lower mesoscopic scale.
A small endpoint correction is not a guarantee of a useful pointwise drift.

These failures concern the canonical complete correction on the stated broad
region. They do not refute the actual fixed-corner capability, an occupation-
integrated admission argument, another gauge/additional correction, or an
adaptively restricted fast-A region. No failure probability for reaching these
rare spike states has been inferred from their existence.

## 7. What the conditional repair changes

The companion note receives, rather than assumes for free,

    |S-N|<=E/100,
    A²N/(L³E)<=1/100,

in addition to the original geometric domain. It proves a uniform inward drift
for the same complete F2 near both R faces, and pays the endpoint and martingale
costs with actual stopped source/occupation clocks. The root must separately
acquire these count/adaptive-A gates from the original process and its entrance
charge. The outward witness files are preserved and not overwritten by that
conditional repair.
