# Alternative opening: calibrated classical noise against quantum memory

29 October 2026. Complementary construction for Astra P1. This is a scoped
research note, not a new physical acquisition or an externally validated
priority claim.

## 1. Consequential question and opportunity comparison

The materially different destination is to determine when a classically
calibrated randomization has exactly the same information-erasure guarantee
in the presence of an arbitrary quantum memory. A positive general theorem
would make classical noise certificates composable with unknown finite quantum
references without reconstructing their dimension or state. A counterexample
would identify a specifically quantum information resource invisible to the
ordinary scalar contraction coefficient.

For a finite classical channel T with full-support prior pi, define

    eta(T,pi) = sup_{p != pi} D(Tp || Tpi) / D(p || pi).

For positive operators A_x on an arbitrary finite reference, put K=sum_x A_x
and Y_y=sum_x T(y|x) A_x. The candidate general principle is

    sum_y D(Y_y || (Tpi)_y K)
        <= eta(T,pi) sum_x D(A_x || pi_x K).                 (G)

Homogeneity permits tr K=1. Umegaki D is used on positive unnormalized
operators, with the support convention. Zero output-prior rows are omitted.

Astra N994 proves (G) for TWO input symbols, any finite output alphabet,
and any finite quantum reference. Its source-count restriction is material.
N995 gives a three-source balanced-entropy failure but does NOT give a
compatible channel/prior counterexample to (G). Current Wang--Gohari primary
research explicitly leaves dimension separation open for matrix entropy
functions in the complete subadditivity class, which includes t log t.
Thus (G) is a live broader direction, not an already solved binary restatement.

Compared with the root's physical-information programme, this direction has
a clearly consequential mathematical endpoint but currently less construction
leverage. Nothing below turns a visible noisy record into a hidden-system
contraction bound. A complete classical carrier, independent noise mechanism
and untouched reference are substantive physical inputs.

## 2. Completed construction: exact tensorization of complete fixed-prior contraction

For a cq state rho_XR with a finite classical X and arbitrary finite R define

    D_pi(X:R) := D(rho_XR || pi_X tensor rho_R)
               = D(p_X || pi_X) + I(X:R).

Let T_j be finite classical channels with priors pi_j, and let c_j be their
optimal constants in (G), allowing arbitrary finite references.

### Theorem

For the product channel and product prior,

    c(T_1 tensor ... tensor T_n, pi_1 tensor ... tensor pi_n)
        = max_j c_j.                                       (1)

Consequently, if every input register is binary, Astra N994 gives exactly

    c(T_1 tensor ... tensor T_n, product pi_j)
        = max_j eta(T_j,pi_j).                             (2)

There is no factor depending on n or on the dimension of the quantum reference.

### Proof for two registers

It is enough to prove the upper bound with c=max(c_1,c_2); lower bounds follow
by varying one input while taking the other input at its prior and independent
of everything else.

Write D=D(rho_X1X2R || pi_1 pi_2 rho_R), and

    D_1 = D(rho_X1R || pi_1 rho_R),
    D_2 = D(rho_X2R || pi_2 rho_R).

After applying T_1 let D' be the corresponding divergence on Y_1 X_2 R,
and let D'_1 be its Y_1 R marginal divergence.

The cq relative-entropy chain rule, using X_2 R as the untouched reference,
and the definition of c_1 give

    D' <= D_2 + c(D-D_2).                                  (3)

Using R as the reference also gives

    D'_1 <= c D_1.                                        (4)

Next apply T_2, using Y_1 R as the reference. The final divergence obeys

    D_out <= D'_1 + c(D'-D'_1)
          = c D' + (1-c) D'_1
          <= c^2 D + c(1-c)(D_1+D_2).                     (5)

Strong subadditivity gives the exact identity

    D-D_1-D_2 = I(X_1:X_2 | R) >= 0.                       (6)

Hence D_out<=cD. This permits arbitrary initial correlations between the
classical registers and the quantum reference. Induction proves (1).

The proof uses established chain rules, strong subadditivity and complete
contraction. Product-reference tensorization is explicitly Theorem 4 of
Hirche--George--Nuradha--Wilde, arXiv:2608.27171v1, with earlier antecedents
credited there. It is a direct compatible composition, not a new scalar-to-matrix
transfer or a claim to historical priority. The distinction between a product
PRIOR and a product INPUT is essential: the input may be arbitrarily correlated.

### Sharp fair-bit continuous-time consequence

Let each bit independently flip at rate gamma_j>0. Its time-t channel is a
binary symmetric channel with bias r_j(t)=exp(-2 gamma_j t), and stationary
prior (1/2,1/2). Its scalar fixed-prior coefficient is r_j(t)^2.

For completeness, write a binary input distribution as ((1+u)/2,(1-u)/2).
Its divergence to the fair prior is

    F(u) = [(1+u)log(1+u)+(1-u)log(1-u)]/2
         = sum_{k>=1} u^(2k)/[(2k)(2k-1)].

For |r|<=1, positive coefficients imply F(ru)<=r^2 F(u). As u tends to
zero the ratio tends to r^2, proving sharpness.

Therefore

    D(rho_XR(t) || uniform_X tensor rho_R)
      <= exp(-4 min_j gamma_j t)
                    D(rho_XR(0) || uniform_X tensor rho_R). (7)

This holds for every finite quantum reference and all initial cq states.
The reference is untouched by the noise interval. The constant is sharp
already with a scalar reference and a small bias in a slowest bit.

If one instead parameterizes a fair replacement generator by replacement
rate lambda_j, its flip rate is lambda_j/2 and the exponent is
-2 min_j lambda_j t. These rate conventions must not be conflated.

### Physical and acquisition contract

The complete classical register must be the actual carrier on which the
independent noises act. Characterizing noisy changes of a coarse output is
insufficient. The noise channels, product prior and independence must be
warranted by the physical construction or acquired to the required accuracy.
The theorem supplies neither that acquisition nor a gate cost.

The R reference may have arbitrarily large finite dimension and need not be
known, but it must not backact during the asserted product-noise evolution.
This is an information-theoretic divergence, not automatically heat or work.
Thermodynamic claims additionally need a specified Hamiltonian, reservoir
model, detailed-balance contract and accounting for implementation.

## 3. Exact failure of the apparent hidden-memory bridge

One can perfectly replace the accessible carrier and still retain all memory
that will affect a later observation.

Take classical bits H,E,S. Initially H is fair, E=H and S=H. Apply a genuine
replacement to S with an independent fair bit U. Immediately afterward,

    rho_SR = uniform_S tensor rho_R,

for R=(H,E), so the carrier's divergence in (7) is exactly zero. Now let a
later uncontrolled interaction copy E into S. The accessible output is again
S=H with certainty. The future prediction depends on the old history despite
the perfect accessible reset.

Both stages are valid finite classical channels and therefore valid quantum
channels when embedded diagonally. This does not refute (7): the second stage
couples the carrier to the previously untouched reference and leaves its scope.

More generally, a system-only causal break is a preparation operation on the
system, not a certified regeneration of all environmental degrees of freedom.
Operational quantum process/Markov-order literature already makes instrument
dependence explicit. This small construction is retained to block a tempting
but invalid physical receiving use of (2).

## 4. A second construction: the exact information lost under a common dephasing

Let P be any fixed rank-one pinching on the reference, not necessarily in an
eigenbasis of K. Set A'_x=P(A_x), K'=P(K), and Y'_y=P(Y_y). Define D_in,D_out
as in (G), and let D'_in,D'_out be their pinched versions.

Since all primed matrices commute, the scalar fixed-prior coefficient applies
coordinate by coordinate:

    D'_out <= eta(T,pi) D'_in.                             (8)

Let C(B)=D(B || P(B)), the homogeneous relative entropy of coherence.
The exact Pythagorean identities are

    Delta_in := D_in-D'_in = sum_x C(A_x)-C(K),
    Delta_out := D_out-D'_out = sum_y C(Y_y)-C(K).           (9)

Data processing under pinching gives Delta_in>=0. Joint convexity and
homogeneity of C give sum_y C(Y_y)<=sum_x C(A_x), because T is stochastic.
Consequently

    0 <= Delta_out <= Delta_in,

and

    D_out <= eta D_in + (1-eta) Delta_in.                  (10)

Thus any genuine violation of (G) must use a nonzero information loss under
EVERY common dephasing. For a candidate with D_out/D_in=eta+v,

    Delta_in/D_in >= v/(1-eta)                            (11)

for every pinching, whenever eta<1.

Equation (10) is a diagnostic reduction, not a solution: Delta_in can be a
substantial fraction of D_in, and no dephasing acquiring it was performed.
It uses ordinary relative-entropy and coherence identities. It identifies
precisely the term a scalarization proof must eliminate or control; merely
choosing the eigenbasis of the total K does not eliminate it.

## 5. Serious first attack and its failure

The executable exploration uses 16 three-input/three-output random channels,
with fixed asymmetric priors, and reference dimension 2 (eight cases) or 3
(eight cases). A_i=L_i L_i^T guarantees positivity. The optimization permits
variable traces and noncommuting real matrices. Scalar candidates are obtained
by differential evolution on the simplex plus all point masses; matrix
candidates by six BFGS starts, including a scalar witness.

The largest printed matrix-minus-scalar gap was about 4.38e-11. No meaningful
separation was found. This is neither an upper bound on a matrix optimum nor
a proof of equality. Both optimized values are LOWER bounds, the real-matrix
search omits genuinely complex families, the prior/channel menu is finite,
and singular boundaries can defeat local optimization.

Files:
- explore_matrix_sdpi.py
- MATRIX_SDPI_EXPLORATION.json

The ordinary proofs in Sections 2--4 do not rely on these optimizations.

A general multi-symbol proof cannot simply repeat N994 independently for
pairs: the normalizing reference K couples all sources, and the independent
three-source entropy transfer is false by N995. A useful next serious attack
would isolate the special coefficient geometry of a stochastic channel versus
a replacer, instead of trying to lift every balanced scalar inequality.
A counterexample needs an actual T,pi and a rigorous SCALAR UPPER bound;
a matrix candidate larger than another optimizer's candidate would not suffice.

## 6. Scope and research decision

This branch supplies an exact many-bit positive result, an exact causal-reset
failure, a coherence-defect identity, and a recorded unsuccessful first attack
on a live more general conjecture. These are reusable constructions, not a
claim that quantum hidden memory has been acquired or erased.

Given current evidence I do not recommend replacing the root's productive
physical-information direction solely with this alternative. The generalized
matrix-SDPI question is high consequence, but no newly decisive bridge was
found in this bounded attack. The product-binary class is a useful source class
only when the physical register/noise interface is already justified.

