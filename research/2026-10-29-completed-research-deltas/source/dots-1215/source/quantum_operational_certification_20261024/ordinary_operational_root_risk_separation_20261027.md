# Polynomial decoder separation for two ordinary quadratic loss models

27 October 2026. Constructive positive subroutine for the generic unflagged opening. This is NOT an adaptive acquisition theorem: it assumes two CLASSICALLY GIVEN physical model families and supplies a polynomial-size operational separation computation and an actual ordinary distinguishing experiment. It avoids an exponential decoder-policy menu without claiming that the unknown models have already been acquired.

## 1. What matrix information is supplied to this subroutine

Both families live in the SAME known k-dimensional output frame and use the supplied real quaternion encoder x in S3. For the literal polynomial-bit version, their physical quadratic coefficients are supplied as exact rational complex matrices of finite bit length. More general computable descriptions require explicitly certified coefficient/probability errors; they are not an exact-real oracle. Write the physically preparable six-state loss density as

`T(x)=(1/6)sum_l E_x(P_l) tensor (I-P_l)^T`,

and analogously T'(x). The coefficient matrices of these real quadratics are classical inputs to the subroutine. Both model families are physically valid/reset encoded channels, not unconstrained signed estimates silently declared physical.

For an UNNORMALIZED decoder Choi matrix C in physical-input-first/logical-output-second order,

`C>=0`, `Tr_output C=I_k`, `Tr C=k`,

`a_C(x)=(3/2)Tr[C^T T(x)]`, `b_C(x)=(3/2)Tr[C^T T'(x)]`.

These are actual Bell losses, in [0,1]. For each fixed C, they are quadratics x^T B_C x and x^T B'_C x with 0<=B_C,B'_C<=I_4. Define the operational root-risk disagreement

`d_rec(T,T')=sup_(x,C) |sqrt(a_C(x))-sqrt(b_C(x))|`.            (1)

The decoder class in (1) is ALL CPTP maps, not a finite dictionary. The operator bound ||C||<=2 follows from its partial-trace constraint and logical output dimension two. Ordinary Bures confidence for T(x) would suffice for (1), but is stronger than needed.

## 2. One-dimensional variational representation removes decoder enumeration

For any a,b>=0,

`(sqrt(a)-sqrt(b))^2
   =sup_(z>0) [(1-z)a+(1-1/z)b]`.                            (2)

For a,b>0 this follows by minimizing za+b/z, attained at z=sqrt(b/a); the zero endpoints are limits. At fixed x,z the right side is LINEAR in C. Therefore its decoder maximum is the standard full-CPTP SDP

`max_C Tr[H_(x,z) C]`,

`H_(x,z)=(3/2)[(1-z)T(x)^T+(1-1/z)T'(x)^T]`,

with constraints C>=0 and Tr_output C=I_k. Its dual is

`min_Y Tr Y`, `Y tensor I_2 >= H_(x,z)`.

H may be indefinite; both programs remain bounded and have readily constructed strict feasible points. The received finite decoder-SDP machinery applies after a known scalar shift if desired. A feasible decoder and certified primal/dual gap produce an actual executable policy. No unknown-source inverse or unknown coefficient oracle appears.

## 3. Explicit finite polynomial grid and error guarantee

Fix rational 0<eta<=1; an arbitrary requested tolerance may first be rounded DOWN to a dyadic value within a factor two. Put kappa=(eta/16)^2 and replace a,b in (2) by a+kappa,b+kappa. This changes an absolute root difference by at most 2sqrt(kappa)=eta/8; adding the same kappa can only DECREASE that difference.

Use the supplied eight-face sphere grid with chord radius h<=eta/16. For each fixed C,

`|sqrt(a_C(x)+kappa)-sqrt(a_C(y)+kappa)|<=||x-y||`,

because the root is the norm of `(B_C^(1/2)x,sqrt(kappa))`. The same holds for b. Thus taking the best encoder grid point loses at most 2h<=eta/8 in root disagreement. This is a CLASSICAL O(eta^-3) list.

The optimal regularized z lies between sqrt(kappa/(1+kappa)) and its reciprocal, hence inside [kappa,1/kappa]. Make a RATIONAL geometric grid on that interval with ratio `1+eta/64`, including the final endpoint. Its size is O(eta^-1 log(2/eta)); all numbers have polynomial bit length. Every optimal log z lies within eta/64 of a grid log z.

For A=a+kappa,B=b+kappa and e=log(z/z_opt), the loss in (2) is exactly

`2sqrt(AB)(cosh(e)-1)`.

Since A,B<=1+kappa and |e|<=eta/64, this is at most eta^2/256 (a deliberately loose bound). At EVERY grid pair solve the decoder SDP to certified objective error at most eta^2/256, including coefficient arithmetic. In particular Tr C=k makes the objective coefficient debit at most k||Delta H||; allocate matrix precision accordingly, rather than omitting this dimension factor. Add the known constant kappa(2-z-1/z) to the objective. Keep a feasible C and a certified LOWER achieved value, with total certified gap from the true SDP maximum at most eta^2/256; choose the grid pair with the largest such lower value.

If d=d_rec(T,T'), the resulting ACTUAL decoder and encoder obey

`|sqrt(a_C(x))-sqrt(b_C(x))| >= d-eta`.                       (3)

Indeed regularization and the encoder grid lose at most eta/4 in root distance. The z grid and SDP lose at most eta^2/128 in its square. The elementary bound sqrt(max(0,r^2-s))>=r-sqrt(s) then gives total loss at most eta/4+eta/sqrt(128)<eta/2; (3) leaves ample finite-synthesis slack.

The computation uses

`O(eta^-4 log(2/eta))`

known-coefficient SDPs of size 2k. This is polynomial in k,1/eta and the coefficient bit length, not exponential in k^2. It may be a very high-cost polynomial. Encoder controls, certified decoder synthesis, rational coefficients, and matrix precision must be paid. The theorem does not assume the classically supplied coefficients are themselves cheaply learned.

## 4. The witness is an ordinary source experiment

Execute the chosen x,C using an ordinary uniformly random Pauli eigenstate and its final projector test. The mismatch probability is p=a/(3/2) under the first model and q=b/(3/2) under the second. The source is queried ONCE per independent record; no acceptance normalization or coherent encoder/reference is introduced.

Take 0<beta<1. If the witness root gap is at least eta, the Bernoulli Bhattacharyya coefficient obeys

`BC=sqrt(pq)+sqrt((1-p)(1-q)) <=1-eta^2/3`.

A known-model likelihood-ratio test on

`n_test=ceil[3 log(1/beta)/eta^2]`

records has EACH error probability at most beta: the sum of its two errors is at most BC^n. This is a deterministic all-query cap. In particular if the two given model families have d_rec>=2eta, (3) supplies such an ordinary witness. This is the IDEAL statistical cap. For final failure beta under finite physical operations, run the likelihood test at beta/2, use `n_test=ceil[3 log(2/beta)/eta^2]`, and require the WHOLE record experiment discrepancy to be at most beta in unhalved diamond norm, hence beta/2 in total variation. Its failure is then at most beta. The discrepancy includes finite synthesis of the selected ordinary encoder, decoder and final tests at all n_test uses, not merely a single-use error; it also covers any known receiver-frame implementation used by this experiment. Alternatively an ideal-beta test with record discrepancy nu_record has failure at most beta+nu_record/2. These budgets are separate from the classical model-coefficient and SDP objective debits above. With rational model coefficients, rational x_i x_j and a certified rational feasible C, the two ideal Bernoulli probabilities are exact rationals: compute likelihood comparisons by integer/rational products of powers, with zero probabilities handled explicitly. Their bit cost is polynomial in n_test and the supplied coefficient bits, so no exact comparison of unknown transcendental logs is assumed. Any approximate probability evaluation, likelihood decision or bounded sampler instead contributes its certified discrepancy to nu_record; an unbudgeted coarse probability fit is not sufficient. The stronger proved computational witness gap d-eta/2 leaves eta-scale synthesis slack if a separate witness-quality claim is desired.

This is pairwise MODEL discrimination with models and their probabilities given. It does not identify which model in a huge class is correct at this cost, does not guarantee balanced version-space elimination, and does not bound the number of adaptive witness rounds.

## 5. Why this is the right sufficient matrix target, and what is still missing

Suppose an ACTUALLY ACQUIRED physical model T_hat satisfies d_rec(T,T_hat)<=eta. Optimize its global encoder/decoder risk to additive nu<=eta^2 (an encoder grid plus one feasible decoder SDP at each point suffices). If ell_* is the true global optimum, the deployed true loss obeys

`sqrt(ell_selected) <=sqrt(ell_*)+2eta+sqrt(nu)`

`ell_selected <=(1+gamma)ell_*+18eta^2/gamma`, for 0<gamma<=1.

The first inequality uses the root-risk confidence once at the chosen policy and once at a true optimal comparator; the second is Young's inequality and nu<=eta^2. Thus eta^2<=gamma epsilon/64 leaves more than half the epsilon budget for finite processing/deployment errors. This transfer neither learns a generic coherent Choi matrix nor chooses the baseline-optimal decoder.

A boundary-safe ordinary learner achieving this confidence at n=O_tilde(k^2/(gamma epsilon)), with polynomially represented uncertainty and polynomial processing, WOULD close the requested generic acquisition bridge when k<=8R. This note does not supply that learner. In particular:

* The positive baseline E_x<=4E_bar does not imply such root-risk confidence or optimum transfer; the separate unique-optimum physical counterexample rules that out.
* A PSD completion of observable real-control coefficients is not automatically an acquired Bures-close completion, even if one exists.
* Pairwise SDP separation does not provide a cheap global version-space maximum over UNKNOWN coefficient models. Searching exponentially many model hypotheses, assuming an optimistically selected model, or presuming a quantum Fisher-information estimator reaches its local limit would leave the main gap unpaid.

The additional information that suffices is task-sensitive confidence on the acquired encoder-dependent matrix family, not only its dominating baseline density or a single baseline decoder. This note makes the policy-separation and final-decision parts polynomial once that information is available.

## Check scope

The companion code checks the scalar variational and finite-grid bounds, physical Pauli-model separation with exact full-CPTP optimization, and several noncommuting general-Hermitian decoder SDPs, including indefinite cases using the received small-instance primal/dual method. These are finite mathematical/circuit-interface checks, not a full acquisition execution or proof of the missing adaptive regression theorem.
