# Receiving the cavity noise law in established scheduled fault tolerance
30 October 2026. New receiving derivation, pending independent review. The CP-cavity bridge and disjoint gadget lemma have their separate scoped receipt; this note does not extend that receipt automatically.

## 1. Actual established consumer and the precise import
Use the measurement-free computation-code procedures of Aharonov–Ben-Or (ABO), quant-ph/9906129, §§4–7 and Theorem 11. They supply fixed-size universal gate, correction, encoding and decoding circuits, a disjoint recursive rectangle hierarchy, and sparse-fault correctness. Their §2.8 explicitly admits the diamond norm, but its basic noise factorizes locations; our shared-bath law is NOT a verbatim special case. Their input is redundantly supplied classical data, and output is protected repetition, not a qualified single physical detector.

AGP quant-ph/0504218 §11 uses an inclusive fault-set norm and overlapping-exRec truncation. Its stated norm is an operator-amplitude norm, so its numerical thresholds and pure-state normalization argument cannot be imported unchanged. We choose ABO's disjoint hierarchy and replace the noise counting below; therefore no overlapping exRec is used or double-counted.

Primary sources: https://arxiv.org/html/quant-ph/9906129 (particularly §§2.8, 3.2, 7.1–7.5, 8); https://arxiv.org/html/quant-ph/0504218 (§§11.1–11.4). This paragraph identifies imported foundations, not a claim that the standard constructions are new.

## 2. Resource and gadget contract
Fix one of those finite computation-code constructions, including all coherent syndrome/check computation, ancilla gates, conditional correction, identity locations, and routing required by the chosen connectivity. Let m be its block length, d_c its correctable error count, and ell its actual combined correction-plus-gate spread. Choose k>=1 with k ell<=d_c. Put s=k+1>=2. Let A be the maximum number of lower-level locations in a complete rectangle, and D_g its maximum depth. These are finite constants of the chosen actual construction, not the old apparatus's clock constants.

The imported deterministic statement is: if each recursively defined rectangle has at most k bad children, every working-period output lies in the intended recursively correctable module. The correction also receives arbitrary damaged words into a code module, which is essential in the inductive proof. The syndrome computations are physical reversible gates in the same fixed schedule, not calls to perfect classical software. The universal polynomial-code alternative in ABO Theorem 5 is an explicit available family; one must keep its actual code/spread parameters rather than borrow a threshold number optimized for another scheme.

For the unconditional existence consequence stated here, furnish fresh known ancillas at their declared insertion locations, or a preparation interface already satisfying the SAME joint fault law. Every later gate/wait is subject to the cavity noise contract. Arbitrarily dirty finite-time resets are NOT automatically equivalent to ideal fresh insertion plus local post-preparation noise. That receiving problem is separate. Likewise furnish redundant classical input as in the cited construction, or an externally encoded quantum input with its declared initial error contract. The single exposed input-latch problem has not disappeared.

## 3. Recursive counting requires only the inclusive diamond law
Write the exact physical expansion as Phi=sum_F E_F and suppose

 ||sum_(F contains S)E_F||_diamond <= x_0^|S|

for every set S of physical locations. The cavity theorem supplies x_0=[2*3^(q-1)g eta tau]^(1/q), where g,tau refer to the ACTUAL elementary scheduled implementation.

At level j, label a rectangle bad when at least s of its children are bad. Rectangles at one level partition the locations under this selected architecture. The exact binomial sieve from FAULT_CLASS_AND_GADGET_RECEIVING.md therefore proves, jointly for every selected set of level-j rectangles,

 ||sum_(paths making every selected rectangle bad)E_F||_diamond
 <= x_j^(number selected),

 x_(j+1) <= binom(A,s) x_j^s (1+x_j)^(A-s).             (1)

No tensor-product independence, positive paths or fresh bath is used. The recursion operates on exact sets of physical paths; all bath coefficients remain in their original signed maps. It is unnecessary to prove that a single bad simulated map is a physical channel.

Choose x_*>0 with

 (A-s)x_*<=1,
 e binom(A,s) x_*^(s-1)<=1.

If x_0<x_*, then inductively

 x_j <= x_* (x_0/x_*)^(s^j).                            (2)

For an ideal circuit containing L rectangles at the top level, another exact inclusion-exclusion sum gives its bad map B_j:

 ||B_j||_diamond <= (1+x_j)^L-1 <= L x_j exp(Lx_j).       (3)

This is a bound on the complete sum of bad paths, not a union bound on invented probabilities.

## 4. Good linear fault classes: the necessary two-sided argument
A good E_F is not necessarily CP. Expanding it only into physical trace-preserving faults is not justified: a general linear bath coefficient need not have constant trace. Instead retain a coherent ideal decoder as an ANALYSIS isometry and use the common correctable operator span.

At a code correction step, let V be the encoding isometry and {A_a} the admitted error-operator family. The error-correction conditions give

 V^dagger A_a^dagger A_b V=c_ab I_logical.

A coherent recovery can therefore be chosen so that, for every a,

 R A_a V = I_logical tensor |s_a>,

with the Gram matrix of the syndrome vectors equal to c_ab. Tensoring arbitrary bath coefficient operators and taking linear combinations then gives, for EVERY two-sided map supported in this family,

 recovery [sum_(a,b) A_a (·) A_b^dagger tensor M_ab]
   = Id_logical tensor K,

where K is a linear bath/garbage map and need not be positive or trace preserving. No norm is taken on the matrix-unit expansion; it establishes only exact logical factorization.

Apply this same identity at each received correction module and move the coherent logical decoders through the fixed good circuit. The imported sparse-fault propagation ensures that the ket and bra error operators remain in the SAME correctable family at every step. Their individual supports may differ; the error-correction condition already covers their cross terms. The union fault set used to declare E_F good bounds both sides. Thus, on the prescribed encoded input module and before the final physical classical de-encoding,

 Dec composed with G_j composed with Enc = U_logical tensor K_j,   (4)

where G_j=Phi-B_j and U_logical is the intended logical circuit. For logical channels with discarded work, include those work systems in the garbage and trace them only afterward. Input/reference/bath entanglement is allowed.

This is the exact receiving content needed from the code/gadgets. It is stronger than merely saying that each isolated positive output has approximately correct measurement statistics. It follows from coherent code recovery and the actual sparse-fault module invariant, not from positivity of G_j. The physical final de-encoding in ABO is used for CLASSICAL answers; it must not be relabeled an arbitrary quantum-output decoder.

## 5. Replace the amplitude-normalization argument by trace defect
Let b_j=||B_j||_diamond. The actual decoded map T_j=Dec composed with Phi composed with Enc is CPTP. Its good part is U_logical tensor K_j by (4). The bad decoded part has complete trace norm at most b_j, because Enc and Dec are channels.

Trace preservation implies, on the encoded logical/bath input,

 I_logical tensor (K_j^*(I)-I) = -(decoded B_j)^*(I).

Hence ||K_j^*(I)-I||_infinity<=b_j. For any joint logical/bath/reference input rho, the reduced good contribution differs from U_logical(rho_logical,reference) only by applying the bath effect K_j^*(I)-I before tracing bath. Its trace norm is at most b_j. The reduced bad contribution also has trace norm at most b_j. Consequently

 ||actual decoded logical output - ideal output||_1 <=2 b_j,       (5)

uniformly with a reference. This argument does not normalize a signed good state or take its square root. For a deterministic classical-answer projector annihilating the entire good output span, actual wrong-answer probability is directly at most b_j.

If a particular consumer has only a classical correctness statement, use that narrower conclusion; do not announce the complete logical-channel version without the common-span condition in (4).

## 6. Scheduled computation consequence and cost
Under the preceding actual gadget/input/ancilla resource contract and the cavity model, choose j such that 2L x_j exp(Lx_j)<=delta. Equation (2) gives

 j=O(log log(L/delta))

for fixed x_0<x_*. Replacing each rectangle recursively costs at most L A^j elementary locations and ideal-depth times D_g^j. Thus the overhead is polynomial in log(L/delta), with constants inherited from the chosen unoptimized procedures. All gates composing coherent classical control are included in A, and every idle interval is a location.

The weak-noise condition is explicitly

 eta tau < x_*^q/[2*3^(q-1)g].                           (6)

This is an existence tolerance, not a competitive numerical threshold. Arbitrary shared-bath memory and the non-CP nature of individual HP perturbation summands cause no additional volume penalty after the cavity bridge. The schedule, fixed gate strengths/durations, preparation interface and connectivity remain real resources.

## 7. What follows, and what does not
The broad continuous-noise model can enter an actual conventional fault-tolerant architecture by this receiving proof, rather than only a new custom memory. With the declared standard preparation and input resources it gives ordinary SCHEDULED reliable logical computation and protected classical output. That operational capability was already known for other noise models; the tested contribution is the new noise-model interface and its norm receiving, not the invention of universal fault tolerance.

It does not prove that Astra's native apparatus supplies the conventional fresh-ancilla resource, an arbitrary dirty-target reset's joint fault law, raw unknown-state encoding, noiseless external measurement, or an autonomous scheduler. It does not import AGP's distance-3 numerical threshold or its overlap-dependent classification into the disjoint proof. An overlapping exRec implementation would require its own exact path-dependent truncation receiving; it is unnecessary for this existence route and is not silently accepted.

No practical advantage, hardware experiment or historical novelty is established. Independent review is required for the new receiving derivation, especially the complete good-module factorization and the stated preparation boundary.
