# Port of the established fixed-rank conditional-sample learner

30 October 2026. This ADOPTS Mausberg8October2026, not a claim of a new learning
theorem. It resolves the fixed-rank mathematical access contract below, while
retaining the source's large rank-dependent exponents and implementation scope.
See PRIOR_CORRECTION.md before interpreting any independently reconstructed
ROOT26/27 result as new. No full GLS/LM learning run is claimed.

## 1. Original contract and the exact closure

The original source P is full support on [O]^T, O>=2. At every chronological
cut its ENTIRE full-future NEXT-TOKEN centered-logit matrix has exact rank<=d.
GIVEN alpha>=1 bounds the norm of both factors, so |ell_h(y)|<=alpha^2 for every
prefix/outcome. Only chosen-prefix conditional NEXT-TOKEN samples are supplied.
No original probability/logit VALUE, high temperature, outcome bias, hidden
factor/state, K variation bound or conditional probability floor is supplied.
Every prefix preparation/reset, submitted token and returned symbol is charged.

For each FIXED d, the existing theorem yields a source-free TV-epsilon sampler
with confidence>=1-delta and costs polynomial in T,O,alpha,1/epsilon,1/delta
and the ordinary encoded input lengths. Its degree depends on d. It is NOT
polynomial jointly in d and those parameters; the growing-rank PRF obstruction
is compatible. It is polynomial in alpha, not a proved polynomial in log alpha.

The controlling primary is Mausberg, Theorems1/22, Sections2--4, AppendicesA.1,
A.4--A.5/C/D/E, at commit78fa048d082b465f0925299958dfb1063f38668a:
https://github.com/SamMausberg/low-logit-rank-distillation
The pinned LaTeX is cached in source_cache/mausberg_low_logit_rank_distillation.tex.
The binary theorem and finite-alphabet extension use different rank-lift routes;
they must not be silently identified.

## 2. Pad the norm bound, without new native contexts or new rank

Put

    H=max(32,T,ceil(alpha^2)).

Define Ppad on length-H words by drawing P's first T symbols and then LOCAL
independent uniform symbols from [O]. At cuts t<T, the old future-logit columns
remain unchanged and all columns whose next emission is after T are zero.
At cuts t>=T all future centered logits are zero. Therefore exact cut rank
remains<=d and every centered logit is bounded in magnitude by H. Full support
is preserved. This is not a mixed-length-rank inference or log of a whole
suffix probability.

The adapter, when asked for a next symbol after h, calls P only if |h|<T,
passing EXACTLY h. If |h|>=T it produces a uniform local symbol, with no call
at an undefined original prefix. A conditional padded future iterates these
rules. Its native queries are only at valid original prefixes; its newly
generated padding and all random bits are counted separately. Uniform-prefix
preparation is not granted for an original source with zeros; full support is
the actual load-bearing promise.

Apply the primary length-H theorem and retain only its first T output symbols.
Data processing of TV gives the original requested accuracy. The output is
source-free because the consumed theorem's generator is source-free, not
because we continue to use the adapter during inference. Its computation and
description costs are bounded by

    [H+O+d+log(1/min(epsilon,delta))]^{O(d+1)}
       *poly(1/min(epsilon,delta))+poly(L_in).         (1)

Since H=O(T+alpha^2+1), this is the claimed fixed-d closure. If alpha is
exponential in T, (1) can still be exponential in T; that debt is explicit.
For d=0 the rank promise makes every next-token logit zero, so the original
uniform law can be returned directly without training.

## 3. Binary smoothing is an exact native operation

In this section O=2 and use the primary theorem's scalar convention
u_h=(1/2)log[p_h/(1-p_h)]. Choose its dyadic

    tau=2^-ceil(log2(8H/epsilon)),
    epsilon/(16H)<=tau<=epsilon/(8H).

Define ONE consistent sequential source Ptau by

    Ptau(b|h)=(1-tau)Ppad(b|h)+tau/2.                (2)

At a generated CURRENT prefix h, with probability tau output a fresh fair bit;
otherwise make one original padded next-token call at h. This is not a noisy
channel applied afterwards to a complete original trajectory: the next native
query uses the actual already smoothed prefix. Full support makes it legal.
On padding positions the source is already fair; the implementation may output
one local fair bit directly. Every extra local bit and actual native reply is
counted. Dyadic mixing has a finite exact random-bit implementation.

Equation(2) has a known floor gamma=tau/2. Pointwise next-token TV error<=tau/2
gives the full law bound

    TV(Ppad,Ptau)<=H tau/2<=epsilon/16.               (3)

Its transformed scalar logits are

    psi_tau(u)=1/2 log[((2-tau)e^(2u)+tau)
                       /(tau e^(2u)+2-tau)],
    |psi_tau(u)|<=M_tau=1/2 log((2-tau)/tau).           (4)

Smoothing generally DESTROYS the exact original logit rank. The operation
does not assume otherwise. The next two steps are essential.

## 4. Unknown polynomial lift, global comparison law, and no hidden factors

The primary Lemma7 proves psi_tau analytic for |Im u|<1/2 with modulus
<=M_tau+2 there. On the Bernstein ellipse of parameter rho=1+1/(2H), a
Chebyshev degree-k truncation r has error

    sup_(|u|<=H)|r(u)-psi_tau(u)|
       <=4H(M_tau+2)rho^-k.                          (5)

In particular k=O[H log(H(M_tau+2)/zeta)] suffices for error zeta.
This is a uniform analytic approximation, including rare and adversarial
native prefixes. It is not learned by fitting logits from those rare tokens.

Define ONE mathematical comparison law Pcirc by next-token logits

    u_circ(h)=r(u_Ppad(h)).                           (6)

The same polynomial r is used at ALL times and cuts. Thus Pcirc is a normalized,
full-support sequential law, not unrelated independent low-rank matrices.
The sigma(2u) derivative bound gives, conservatively,

    sup_h TV(Ptau(.|h),Pcirc(.|h))<=zeta,
    TV(Ptau,Pcirc)<=H zeta.                          (7)

At a cut write u_hf=<x_h,a_f> using the ORIGINAL rank-d row space. Expanding
r(<x_h,a_f>) in monomials in the d coordinates x_h gives exact rank

    D=choose(d+k,d)                                  (8)

for the comparison-law logit matrix. Its entries are bounded by M_tau+zeta.
Max-volume refactorization supplies the primary's known polynomial factor
bound from D and that entry bound, without computing the unavailable factors
or the polynomial coefficients. No minimum singular value is supplied.

The algorithm NEVER computes r, Pcirc, x_h or a_f. They prove why its observable
Ptau interface is sufficient. Calling them a hidden VALUE oracle would be
incorrect: the only implemented queries are (2) and the finite sampling
estimate in Section6.

## 5. The noncircular approximation budget and complete transfer

The source makes all constants explicit. With Cq=52 set

    L=ceil(log2(4/tau))+3,
    J=ceil(log2[2H Cq(d+1)L/(epsilon delta)])+10,
    N=100 Cq(d+1)J, zeta=2^-N,
    k=8H N, D=choose(d+k,d),
    V=2H D L/(epsilon delta).                         (9)

Algorithm3/Lemma19 is the primary's corrected finite exact-rank GLS receiver.
Its numerical-logit and full-sample caps Rell,Rs, logit tolerance xi and total
training token bound W obey

    Rell+Rs<=V^22, xi^-1<=V^11, W<=V^52.              (10)

The primary AppendixA.5 verifies the noncircular inequalities

    zeta<=xi/2, Rs H zeta<=delta/4, H zeta<=epsilon/8. (11)

D grows as a polynomial in H and log(1/zeta) when d is fixed. Consequently
exponentially small zeta can pay every polynomially many approximate-source
request; no equation like 'choose error small compared with its own power-law
inverse sample count' is being assumed. A direct degree bound is

    D <=[801 Cq(d+1)H J]^d.                          (12)

The actual run feeds Algorithm3 independent complete samples from Ptau, plus
cached numerical estimates of Ptau's scalar logits. The ideal comparison run
uses Pcirc samples and a fixed accurate numerical table for Pcirc. Conceptually
assign independent estimation tapes to ALL prefixes, independently of complete
samples and learner coins. Repair an inaccurate table entry in the ideal run
to a canonical accurate dyadic value. These are proof objects, not available
data. On every first actually exposed prefix the tape failure is budgeted;
repeated requests use the same cached value. Values accurate for Ptau within
xi/2 are accurate for Pcirc within xi by (5),(11).

Complete-sample replies can be coupled with discrepancy at most H zeta EACH,
uniformly in a submitted prefix. Until a first discrepancy, the adaptive query
contexts agree. The primary bounds all such source/table transcript errors
by delta/2. The ideal full GLS receiver learns Pcirc to epsilon/2 with its
separately reserved failure and finite generation tolerances. Thus the actual
learner succeeds with probability>=1-3delta/4 and

    TV(Ppad,Q)<=epsilon/16+epsilon/8+epsilon/2<epsilon.(13)

The original target promise was never changed. Only an internally simulated
law and an uncomputed globally consistent comparison law are different.
Truncating the returned word to T preserves (13).

## 6. Implementable probability-floor estimator and exact token charges

At a previously unqueried prefix h draw m independent conditional bits from
the ACTUAL adapter Ptau. The primary Lemma6, with floor gamma, tolerance xi0
and failure beta, uses

    m=ceil[48/(gamma xi0^2) *ceil(log2(4/beta))].       (14)

Multiplicative Chernoff for both outcomes bounds their relative errors. Clip
the empirical fraction only on bad transcripts to [gamma/2,1-gamma/2], compute
the centered log ratio to the supplied finite tolerance, and dyadically round.
This yields a total finite routine, not logs of zero. For the full algorithm
take xi0 and rounding grid from the primary's xi/2 cached wrapper and budget
beta across Rell; no original rare-event floor is measured. The same prefix
is cached once, with new independent tapes for new prefixes. A conditional
suffix is generated by successively updating its actual current prefix.

For binary sources, the primary's sharpened request accounting yields

    tilde O(H^14 D^6/epsilon^5) generated training bits,
    tilde O(H^15 D^6/epsilon^5) submitted+generated tokens. (15)

For fixed epsilon,delta,d this is tilde O_d(H^{6d+15}) tokens; constants and
logarithmic powers depend on fixed d. Every prefix length and local noise bit
is included. In our padding adapter, ORIGINAL native queries occur only before
T and can be fewer than these conservative H-based bounds. The H-T padding
and smoothing bits are local computation, not hidden native teacher access.
If the only native service returns a whole ORIGINAL suffix, keeping its first
symbol costs that full suffix, at most T original symbols per elementary
next-token request; multiply the native-symbol portion of (15) by at most T.
No probability VALUE is created or assumed.

The source supplies deterministic caps on training, arithmetic, data size and
each future generation, with a fair-bit fallback on failures. Its proof is
stronger than an unspecified real-arithmetic implementation. The GitHub
repository contains the manuscript, Lean lemmas and a finite structural audit,
not an installed end-to-end learner. Our implemented adapter is therefore not
reported as an executed full Algorithm3 run. The actual theorem and its full
finite program are the consumed working predecessor.

## 7. More than two outcomes: use the actual finite-vocabulary theorem

AppendixE/Theorem22 proves (1) for every finite O. It does NOT simply apply
the scalar map(4) independently to categorical probabilities, which would
break normalization and rank control. Its construction is as follows.

At each time choose max-volume original logit rows, giving a reachable native
coordinate x in[-1,1]^d with exact linear token updates. Each readout vector
w_(t,y) has entries bounded by H. The ordinary softmax probabilities

    F_(t,y)(x)=exp(<x,w_(t,y)>)/sum_z exp(<x,w_(t,z)>)

are analytic on a product of Bernstein ellipses of width O(1/(dH)); all logit
imaginary parts are <1/4, so the denominator's real part is positive and the
functions are uniformly bounded there. Tensor Chebyshev polynomials g_(t,y)
approximate them on the FULL cube to error beta with degree K per coordinate,
K=O[dH log(2d(9dH)^d/beta)]. Correct both normalization and positivity:

    r_y=g_y+(1-sum_z g_z)/O,
    q_y=(r_y+3beta)/(1+3O beta).                      (16)

These q_y are strictly positive polynomials summing identically to1, with
next-token TV discrepancy<=4O beta. Define ONE global surrogate by
Ptilde(y|h)=q_(t,y)(x_t(h)). From any cut, each later factor is a polynomial
of degree<=dK in the SAME original state coordinates; a suffix product has
degree<=H dK, so the exact probability rank is at most

    R=choose(d+H dK,d).                              (17)

This is a statement about the CONSISTENT SURROGATE, not a false identification
of original logit rank and original probability rank. Neither its latent
states nor coefficients are supplied to the learner.

Run the actual Liu--Moitra same-target conditional-sampling rank-R learner
with ORIGINAL Ppad replies. The ideal run would receive Ptilde replies. The
primary explicitly inlines every statistical call, supplies a deterministic
polynomial request cap q, and chooses exponentially small uniform next-token
error eta with (q+1)H eta<=a, a=min(epsilon,delta)/4. Because R grows only
polynomially in log(1/eta) for fixed d, this is again noncircular. Uniform
conditional coupling transfers the full adaptive training transcript and final
law. AppendixD pays the finite rational caches, KL projection arithmetic and
standalone generator caps; Theorem22's (1) includes finite alphabet encoding.

Thus the finite-O alpha port is also closed mathematically at the published
source's exact scope. A new runtime benchmark of our own weak-Holder compiler
would be an inferior comparison; the full strong ordinary LM/GLS operations
and their acquisition contracts are retained instead.

## 8. Actual code/experiment boundary and strategic conclusion

The private native adapter implements padding, exact dyadic smoothing and a
cached sampling logit estimator. It does not implement or execute the huge
GLS/LM learner. Any finite primitive control is labeled separately with its
actual tolerance; it cannot be claimed to run the full theorem's much smaller
xi. No source factors, surrogate coefficients, original logit value or extra
outcome-bias control enters that code.

The correct frontier is now established prior rather than a fresh open positive
problem: exact fixed rank permits native conditional learning; growing rank
does not admit a general joint-polynomial classical learner under the stated
PRF premise. Approximate-average-rank robustness, fixed-parameter rather than
H^{O(d)} complexity, practical exponents and scientific source/control admission
remain separate. This port changes no prior frozen proof and claims no new
historical contribution, practical advantage or acquired physical apparatus.
