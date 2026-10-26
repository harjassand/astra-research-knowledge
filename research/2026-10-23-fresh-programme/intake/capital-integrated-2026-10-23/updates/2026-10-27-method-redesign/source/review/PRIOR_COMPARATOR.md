# Prior method and post-output reviewer instantiation

The strongest verified historical method is substantially stronger than the
supplied baseline's scalar/matrix/Doeblin/reset bounds. Published free convex
Positivstellensätze turn the all-dimension positivity problem into a finite SDP.
This is a method-level antecedent; it must be distinguished from an already
packaged channel evaluator with matched timing and exact arithmetic.

## Primary sources and exact scope

1. J. W. Helton, I. Klep, S. McCullough, *The convex Positivstellensatz in a free
   algebra*, Advances in Mathematics 231 (2012), 516–534, Theorem 1.1(2):
   https://arxiv.org/html/1102.4859 ; https://doi.org/10.1016/j.aim.2012.04.028 .
   For a monic linear pencil L and symmetric matrix polynomial p of degree at
   most 2d+1, positivity on all matrix levels of D_L is equivalent to
   p in M_(d,d)(L): sums of squares and L-weighted squares with degree at most
   d. This is an exact finite-size certificate, including non-strict positivity.
   The theorem is stated for real symmetric matrices; realification supplies
   complex Hermitian coverage. No channel-specific statement is asserted there.

2. J. Volčič, *Hilbert's 17th problem in free skew fields*, Forum of Mathematics,
   Sigma 9 (2021), e61, Theorem 5.2 and Section 5.5:
   https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1 ;
   https://arxiv.org/abs/2101.02314 .
   The rational convex Positivstellensatz applies on a free spectrahedron
   intersected with the Hermitian domain. Section 5.5 explicitly gives a single
   SDP for rational eigenvalue optimization with a finite subexpression basis.
   It therefore supplies an alternative prior route before polynomialization.
   General matrix-valued positivity can also be scalarized with auxiliary test
   variables; this need not preserve a small implementation size.

3. I. Klep, J. E. Pascoe, J. Volčič, *Regular and positive noncommutative rational
   functions*, J. London Math. Soc. 95 (2017), 613–632, Section 5.2.1:
   https://igorklep.codeberg.page/files/regular_fun_23dec16.pdf ;
   https://doi.org/10.1112/jlms.12030 . This is a relevant earlier rational-SOS
   algorithm, but its global regularity assumption does **not** directly hold
   for the channel row inverses away from the effect simplex. The 2021 theorem
   avoids silently making that invalid substitution. The 2012 polynomial route
   below already suffices for the present instance class.

I inspected these specific primary passages. The search was targeted, not an
exhaustive priority search. No absence or novelty conclusion follows from
unfound sources. Firecrawl guidance was read but its credit-billed operations
were not used under the no-paid-service instruction; public primary sources
were retrieved through the web tool.

## An actual coefficient-matching SDP

Use the denominator-only 2x2 Schur polynomial P_c derived in DERIVATION.md:

 P_c(Q)=c[diag(w_1,w_2)-w w^*]
         -D[sum_i M_i tensor Q_i-q q^*]D^T,
 w=P K Q, D=P KB, q=[Q_1;Q_2].

All coefficients are rational and affine in c, including singular K. Translate
Q_1=I/3+X_1, Q_2=I/3+X_2, Q_3=I/3-X_1-X_2. The effect domain is precisely

 L(X)=diag(I+3X_1,I+3X_2,I-3X_1-3X_2)>=0.

This is a monic linear pencil with a nonempty interior. P_c is a symmetric
2x2 matrix polynomial of degree two, so the 2012 theorem applies with d=1.
Put W=[I_2;X_1 I_2;X_2 I_2]. Minimize c>=0 subject to four PSD matrices
A,B_1,B_2,B_3 of size 6 and the polynomial identity

 P_c=W^* A W+sum_i W^* B_i [Q_i] W.

The notation for each localizer means sum_(a,b) (B_i)_(a,b) times
word_a^* Q_i word_b, with 2x2 coefficient blocks; it does not commute Q_i past
the words. Matching all fifteen words through degree three gives linear
coefficient constraints. Scaling Q_i by three absorbs the monic L weights.
Each L-weighted square splits by its three diagonal rows, so these four Gram
matrices represent exactly the theorem's degree-one quadratic module.
Thus the exact SDP optimum is the required channel coefficient. This is an
explicit old-theorem instantiation, rather than an appeal to quantifier
elimination or an unexecuted asymptotic hierarchy.

For rational validation, round and strictly shift every Gram matrix, checking
all LDL pivots exactly. The resulting represented polynomial h is globally
positive on the simplex. If E_w are the rational coefficients of P_c-h, then

 epsilon=sum_w sum_ab |(E_w)_ab| (2/3)^|w|

bounds its operator norm, because ||X_j||<=2/3 at every matrix level. Further,
N_K^-1>=kappa I, with
kappa=[max(1/min K_row1,1/min K_row2)+2/min K_row3]^-1>0.
Consequently P_(c+epsilon/kappa)>=0. All residual and rounding costs are
charged in the upper bound. This residual certificate covers complex effects
and relies on the strict channel positivity already required by the task.

## What was actually constructed and what it proves

`old_sos_comparator.py` is **post-output reviewer work** written after both
candidate proofs were read. It uses their audited covariance linearization;
it is not evidence that this precise efficient implementation had been frozen
before the trial, nor a repair or increment credited to either candidate.
It deliberately uses generic coefficient matching, not the candidates' small
common-center certificate. It currently acquires only certified upper bounds;
it has no independent lower-witness collector.

On the public quantum-reference control the generic SDP objective was
0.33840084343960647. Exact rational validation gave upper 0.3384008593572023,
against the independently checked delivered lower 0.3384008430069494. A fresh
process including imports took 1.0474 seconds; input-dependent construction,
solve, rounding and exact verification took 0.0305 seconds. Two fresh reviewer
contraction inputs, including singular K, also gave checked uppers within
1.2e-8 of independently checked delivered lower witnesses in 0.02–0.03 seconds
each. See checks/OLD_SOS_QUANTUM_CONTROL.json and checks/OLD_SOS_FRESH.json.

After the official release, the same generic upper constructor ran all thirteen
development/control/holdout inputs in 1.2043 seconds including 0.8955 seconds of
imports. Maximum input-dependent work was 0.0439 seconds. Every upper was
rationally checked and was within the target width of the independently checked
X13 lower witness; maximum gap was 1.724e-7. The lower acquisition was reused,
so this is an executed competing upper mechanism, not a separately completed
autonomous interval evaluator. See checks/OLD_SOS_FINAL_UPPERS.json and
checks/OLD_SOS_FINAL_COMPARISON.json. The retained solver warning on a finite
case does not supply or invalidate a rational certificate.

The reviewer isolated CVXPY installation was not timed and its provisioning
cost is UNKNOWN. An initial CVXPY 1.9.3 import failed against inherited NumPy
1.26.4; CVXPY 1.7.3 was installed in this reviewer folder and succeeded, with
Clarabel 0.11.1. This setup cannot be silently omitted from a one-shot deployment
comparison. Candidate selected paths need none of these new packages.

The experiment can credit completed, measured constructions and the smaller
three-LMI/covariance specialization relative to its displayed priors. A claim
that historical mathematics lacked a finite global SDP method is excluded by
the primary sources. Equal or superior full-evaluator performance against the
best historical implementation is not established by one post-output upper
constructor and candidate-acquired lower witnesses.

## Older supplied Astra source

`sources/N405_adaptive_RESULTS.md` is dated 9 October 2026 and explicitly calls
its universal Choi-SDP result an unreviewed theorem candidate (lines 3–4).
Its Sections 4–5 contain relevant centered Gram/minimax geometry, but its
coefficient compares one quantum channel with the identity. This audit did
not establish its universal theorem or a valid transfer to arbitrary K,L.
In particular K L^-1 is generally not a stochastic postprocessor and the
image of L is restricted even when that product happens to be stochastic.
N405 is therefore an antecedent requiring its actual status and scope, not
an accepted solution to the present two-channel comparison.
