# Effective finite-horizon required-supply storage

15 October 2026. New local deduction from SOURCE_QC_REPORT.md. Conditional on the source's quasiconvexity, coercivity and polynomial growth proofs; no independent external review or historical novelty claim.

## Result

The moving-mean issue does not prevent effective horizon truncation. It costs an explicit extra constant ramp. This closes the duration-truncation gate, not the separate finite-dimensional/global-optimization gate.

Write normalized circle integration as E_y, set gamma=1/2500000, b=|B|, and use the source adjusted density

f_B(A)=G(B+A)-G(B)-DG(B):A.

For U in W^(3/4,4)(T;R²), let m=E_y U and V_U=U-m. Choose any certified unit entry E_U from zero to V_U, and put

M=120[b² ||D E_U||_2² + ||D E_U||_4⁴],     E_*=2M/gamma.

Reflection supplies a return with the same upper action bound M. Define p_B^N(U) as the infimum over incoming paths of duration at most N. Equivalently one can demand duration exactly N, by prepending the zero profile; never hold a nonzero profile stationary for free.

For every H,L>0 with H+1+L<=N,

0 <= p_B^N(U)-p_B(U)
 <= 240[5 b² sqrt(E_*/H)+25 E_*/H]
    +120[b² C²/L+C⁴/L³],                              (A)

where C=|m|+H^(3/4) E_*^(1/4).

All constants in the horizon conversion are numerical. The endpoint extension budget M is an input; the source gives M<=120[b² C_E² R²+C_E⁴ R⁴] on a strong critical ball of radius R. A spectral extension budget, when available, can substitute without a generic trace-extension constant.

In particular, for mean-zero U, n=N-1>=4, take H=sqrt(n), L=n/2. Then

0 <= p_B^N(U)-p_B(U)
 <= 1440 b² sqrt(E_*) n^(-1/4)+6240 E_* n^(-1/2).       (B)

At B=0 the better choice H=n^(3/4), L=n/2, valid for n>=16, yields

0 <= p_0^N(U)-p_0(U) <=6960 E_* n^(-3/4).              (C)

These are uniform quantitative convergence rates when M is uniformly bounded. They are sufficient bounds, with no optimality claim.

For target error epsilon>0, a mean-zero all-background sufficient bound is

N >= 1+max{4,(2880 b² sqrt(E_*)/epsilon)^4,
                  (12480 E_*/epsilon)^2}.

At B=0 it suffices that

N >= 1+max{16,(6960 E_*/epsilon)^(4/3)}.

Rounding N upward is harmless. For unadjusted storage the affine term DG(B):(m|0) is identical at every horizon, so these error estimates apply unchanged.

## Proof

### 1. Coercivity and means

For any incoming path Phi ending at U, append the reflected extension from U=m+V_U to m, then a constant ramp m to zero over duration Q. The resulting path has zero outer profiles. The source coercivity gives

gamma ||D Phi||_4⁴ <= J_B(Phi)+M+J_B(mean reset).

The reset gradient is (-m/Q|0), and the source growth estimate gives

|J_B(mean reset)| <=120[b²|m|²/Q+|m|⁴/Q³] ->0.

Thus J_B(Phi)>=gamma ||D Phi||_4⁴-M, also for nonzero endpoint mean. Source mean invariance p_B(U)=p_B(V_U) and its upper witness give p_B(U)<=M. Consequently every eta-minimizer has gradient fourth-power energy at most E_eta=(2M+eta)/gamma. No bound on its original duration or intermediate mean is assumed.

### 2. Find a cheap oscillatory slice without a trace theorem

Let Phi have duration T>H and total fourth-power gradient energy at most E. Fubini on (T-H,T) gives an a.e. cut t in this interval such that

q:=E_y |Phi_y(t,y)|⁴ <=E/H.

One can choose a slice with the usual W^(1,4)(T) representative, so the restriction/gluing traces agree. Set c=E_y Phi(t), V=Phi(t)-c, r=T-t<=H.

For a mean-zero periodic W^(1,4) function, Minkowski and the shortest translated arcs give

||V||_4 <= (1/(2pi)) integral_[-pi,pi] |h| dh ||V'||_4
          =(pi/2)||V'||_4 <2||V'||_4.

The explicit unit entry Q(s,y)=s V(y), 0<=s<=1, satisfies

||D Q||_4² <= ||V||_4²+(integral_0^1 s⁴ ds)^(1/2)||V'||_4²
            <=5||V'||_4²,

hence ||D Q||_4⁴<=25q and ||D Q||_2²<=||D Q||_4²<=5sqrt(q). Reflection gives a return with these same bounds. Therefore each absolute action is at most

M_cut=120[5b² sqrt(E/H)+25E/H].

This is stronger and simpler than selecting a slab and applying a critical trace theorem: the slice is actually W^(1,4), with an explicit linear extension.

### 3. The dropped prefix has a controlled lower bound

Append to Phi restricted to (0,t) the reflected unit extension V to zero, shifted by c. It ends at constant c. Append a constant reset c to zero over duration Q. Quasiconvexity of the resulting zero-endpoint path gives

J_B(prefix)>=-M_cut-J_B(reset).

Let Q tend to infinity in this inequality, using the displayed reset growth estimate. Thus J_B(prefix)>=-M_cut. This is an inequality proof; the infinite limit is not used as a finite-horizon competitor.

### 4. Bound the actual cut mean by the retained suffix

The average a(x)=E_y Phi(x,y) is absolutely continuous and satisfies a'(x)=E_y Phi_x(x,y). Holder on the retained suffix gives

|c-m| <=integral_t^T |a'(x)| dx <=r^(3/4) E^(1/4)
        <=H^(3/4) E^(1/4).

Hence |c|<=C. A long prefix cannot produce an uncontrolled cut mean when the cut lies within the last H units of a path with a fixed final mean.

### 5. The finite replacement

Use three pieces:

1. Constant ramp 0 to c, duration L, action at most 120[b² C²/L+C⁴/L³].
2. Unit entry c+sV, ending at the actual cut profile c+V, action at most M_cut.
3. The unchanged suffix Phi restricted to (t,T), duration r<=H.

The total duration is at most L+1+H and the endpoint is exactly U, including its mean. The total action exceeds the original action by at most the ramp cost plus 2M_cut, by the prefix lower bound. If T<=H, retain Phi itself and prepend zero padding if an exact horizon is desired.

Apply this to eta-minimizers with E=E_eta and let eta decrease to zero. No original minimizer, compactness assertion, or attainment is used. Continuity of the explicit bound in E gives (A), including E_*=0. Substitution gives (B) and (C). For (B), the quartic term is 120E_*[50n^(-1/2)+8n^(-3/2)]<=6240E_*n^(-1/2) when n>=4.

## Mean-fixed subclass

If all paths are required to have zero transverse mean at every x, then c=0 and no mean ramp is needed. With N=H+1 the same proof for the correspondingly restricted storage gives

0 <= p_(B,mf)^N(U)-p_(B,mf)(U)
 <=1200b²sqrt(E_*) (N-1)^(-1/2)+6000E_* (N-1)^(-1).

The extension must preserve zero mean, as the source mollifier extension does. This statement concerns the restricted infimum: it does not identify it with the unrestricted value.

## Exact scope

- The naive O(E/H) argument is valid at B=0 for oscillatory closure costs, but not generally at nonzero B, where the source growth bound supplies a b² sqrt(E/H) term.
- Ignoring the mean would give the wrong endpoint. A slow finite mean ramp repairs it, with explicit horizon inflation.
- No nonzero profile is assumed to have zero stationary cost.
- The theorem supplies a computable horizon from a certified endpoint extension budget and tolerance, and therefore removes one previously stated obstruction to value evaluation.
- It does not certify global optimization over W^(1,4) at that horizon, give an effective spatial discretization error on the whole critical ball, or defeat the finite-Fourier observation counterexamples.

## Numerical scale: effectiveness is not practicality

With B=0 and a supplied endpoint extension budget ||D E_U||_4=1,
M=120 and E_*=600,000,000. The sufficient B=0 horizon formula gives:

- epsilon=0.01: threshold approximately 3.1213848633×10^19; N=3.13×10^19 is a safe rounded-up choice.
- epsilon=0.001: threshold approximately 6.7248198304×10^20; N=6.73×10^20 is a safe rounded-up choice.

These conservative bounds are astronomically large. They establish quantitative termination of duration truncation in principle; they are not a recommendation to simulate such horizons. The numerical thresholds were evaluated locally with 50-digit decimal arithmetic; the theorem and the safe rounded choices rely on the displayed exact formula.

## Stronger computational representation: free terminal mean

The following is a different finite problem, stated and checked here. It gives a substantially better horizon approximation to the same infinite-horizon value.

Let U be a centered representative and define

q_B^N([U]) = inf{J_B(Phi): 0<T<=N, Phi(0)=0,
                              Phi(T)=U+d for some d in R²}.

The terminal constant d is an explicit optimization variable. Equivalently the endpoint's oscillatory profile, not its full value, is prescribed. This is NOT p_B^N(U) with a fixed full endpoint. The definition is independent of which representative of [U] is used. Exact duration N is again equivalent by initial zero padding.

For N>1 and E_*=2M/gamma as above,

0 <=q_B^N([U])-p_B(U)
 <=1200 b² sqrt(E_*/(N-1))+6000 E_*/(N-1).             (Q)

Proof of the lower bound: every competitor ends at some U+d, hence its action is at least p_B(U+d)=p_B(U). This uses the source's infinite-horizon mean invariance only. It does not assume finite-horizon changes of mean have zero cost.

For the upper bound take an eta-minimizer of the original fixed-endpoint arbitrary-duration problem from zero to U, with energy E_eta. If its duration is at most H=N-1, it already qualifies. Otherwise apply the cheap-slice argument above in the last H units. At the cut the profile is c+V. Use the unit entry sV from zero to V and retain the original suffix translated by the constant -c. The suffix starts at V and ends at U-c, so its terminal constant is the allowed variable d=-c. The gradient and action of the retained suffix are unchanged exactly. The discarded prefix action is at least -M_cut, while the new entry action is at most M_cut. Thus the action error is at most 2M_cut. The duration is at most H+1=N. Let eta decrease to zero to obtain (Q).

In particular, sufficient horizons are

- General B: N>=1+max{(2400 b² sqrt(E_*)/epsilon)²,
                                  12000 E_*/epsilon}.
- B=0: N>=1+6000 E_*/epsilon.

For E_*>0 these choices have N>1. If U=0 and M=0, q_B^N=p_B(0)=0 for every N>0 by the zero competitor and quasiconvexity/mean invariance; no division edge case is needed.

With B=0, e4=1, M=120, E_*=600,000,000, the sufficient horizons become exactly 1+3.6×10^14 for epsilon=.01 and 1+3.6×10^15 for epsilon=.001. These are still astronomically conservative.

### The additional optimization variable can be bounded

The free terminal mean does not need an unbounded search in near-optimal sublevel sets. For any competitor ending at U+d, the coercivity proof in Section 1 applies with the same oscillatory extension budget M, independently of d:

J_B(Phi)>=gamma ||D Phi||_4⁴-M.

If J_B(Phi)<=M+eta and T<=N, then

||D Phi||_4⁴ <=(2M+eta)/gamma,
|d| <=N^(3/4)[(2M+eta)/gamma]^(1/4),

where the second estimate integrates the mean derivative from the initial zero profile. Thus for any fixed eta0>0, sufficiently near-minimizing sequences for q_B^N lie in the explicit closed ball |d|<=N^(3/4)[(2M+eta0)/gamma]^(1/4), provided N>=1 so the unit endpoint extension supplies q_B^N<=M. Restricting the infimum to this ball leaves its value unchanged. This bounds the extra two real variables but does not resolve the remaining infinite-dimensional optimization.

### Physical and unadjusted-action interpretation

This construction prescribes the final displacement/profile modulo a rigid translation. It does not claim that returning that translation to a prescribed value has zero work in finite time. That restoration is precisely what costs the finite ramp in (A). Accordingly q_B^N is a quotient-state computational surrogate, while p_B^N(U) represents the fully fixed endpoint problem.

For the original unadjusted required supply at an actual known endpoint U_actual with mean m_actual, approximate it by

DG(B):(m_actual|0)+q_B^N([U_actual]).

The affine term is evaluated at the specified physical mean. It must NOT be optimized over the free d in q_B^N, because that would define a different quantity and can destroy the lower bound. The finite surrogate uses the adjusted density f_B throughout.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
