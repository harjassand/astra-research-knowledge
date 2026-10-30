# Boundary telescoping and local-leg transfer for the compressed spectral basin
2026-10-30. Root derivation completing the abstract comparison mechanism, under the structural premises of COMPRESSED_CIRCUIT_SPECTRAL_BASIN_CANDIDATE.md. Independent review pending; actual native-interface verification remains separate.

Use P=P0, Q=I-P, and R=R0 from that note. The boundary premise is needed for every fixed-support physical leg and Xi: all P-to-Q matrix elements have both endpoints in R, with R<=1_(E>=bN-O(1)). If the required common boundary strip does not exist, this proof does not apply.

## 1. A uniform tail bound for all partial words
For any fixed integer k, the earlier exact higher-moment bound gives, uniformly for unit vectors psi in P1,

 ||V^k psi||<=exp([ka+k c_t t+C_k delta]N).

Let B be any partial product of original or P-compressed proof gates, possibly with a fixed number of bounded local insertions. Each satisfies a weighted norm bound

 ||V^k B V^-k||<=C exp(C_k delta N).

Projections P,Q,R commute V and do not increase this bound. Consequently

 ||R B psi||<=C exp([ka-k sb+k c_t t+C_k delta]N+O(1)). (1)

Inserting A^(1/2) on the right costs one extra half-power of V. Bound it using the next integer moment. Additional coarse operator norms from other factors cost exp(CN), where C is fixed independently of k. The same statements hold with reference/bath identity factors because these are operator-norm bounds on the system.

Choose a<sb and a fixed k so k(sb-a) dominates all such fixed C by a desired margin, then choose t,delta sufficiently small. We may thus make every displayed boundary error exp(-cN) with c as large as the subsequent finite calculation requires. This is a hierarchy of fixed constants, not an N-dependent parameter choice.

## 2. One compressed gate versus the actual local proof gate
Put Xi_diag=P Xi P+Q Xi Q. Its block-diagonal exponential restricts to exp(epsilon P Xi P) on P. Since

 Xi-Xi_diag=P Xi Q+Q Xi P=R(Xi-Xi_diag)R,

Duhamel's exact formula for the two exponentials contains one R-supported crossing. For a partial-word input B psi, (1) bounds the right side of that crossing. Left exponential norms are bounded by exp(C epsilon). Weighted norms of all intermediate exponentials are also bounded, because conjugation by V^k of Xi_diag is bounded by the corresponding compressed local Xi norm. Integration therefore gives an exponentially small difference on every such input, with a factor C epsilon.

Telescope the O(N) gates. Coarse norms of left partial products are at most exp(C delta N), already paid in(1). Thus the original Y and the block-diagonal comparison circuit Y_diag differ exponentially on P1-supported vectors, also after A^(1/2) and any fixed number of local insertions. The restriction of Y_diag to P is exactly Y0. No assertion of geometric locality of Y_diag is made.

## 3. Bilinear comparison of observables
Let W=A^(1/2)Y†Y A^(1/2), W_diag=A^(1/2)Y_diag†Y_diag A^(1/2). For any fixed-support operators U,Vloc of uniformly bounded norm, the preceding argument and Cauchy-Schwarz give

 ||P1 U†(W-W_diag)Vloc P1||<=exp(-cN).                (2)

For clarity, write the matrix element as the difference of inner products of YA^(1/2)U psi and YA^(1/2)Vloc phi versus their block-diagonal counterparts. One factor difference is exponentially small by section2; the other factor may be bounded by exp(CN), which was already included in the choice of k. This holds uniformly in psi,phi, hence in operator norm, not merely for a particular state.

W_diag equals W0 on P. The extension F=W0+Q differs from W_diag only in its Q block. When U,Vloc act on P1-supported inputs, any Q component is a boundary crossing of a fixed-support local operator. Equation(1) again pays its norm, even with the coarse norm of W_diag. Therefore

 ||P1 U†(F-W)Vloc P1||<=exp(-cN).                    (3)

All local Hamiltonian, jump gain, and complete loss contributions are bilinear forms of this kind. Summing O(N) terms preserves an exponential bound. Thus

 ||P1[L^*(F)-L^*(W)]P1||<=exp(-cN).                 (4)

For the broad joint HP perturbation model, one must use the existing finite SYSTEM-leg expansion with bounds from the joint cb norm. The system operator bound(3) remains uniform under reference amplification; bath-only terms commute all system observables. No nominal record lift or chosen physical jump decomposition for the perturbation is assumed.

The same telescoping yields

 ||S rho S†-S0 rho S0†||_1<=exp(-cN)                (5)

for positive trace<=1 states supported in P1. Because the coverage observable D and E have O(N) norm, their expectation differences are also exponentially small. S0 rho S0† lies exactly in P, so the earned basin-local D>=cE inequality may now be used. This completes the comparison step proposed as equation9 in the companion note, under its stated boundary/locality premises.

## 4. Local-leg weighted norm and escape
For the original local circuit, a fixed-support system operator J obeys

 ||S J S^-1||<=C_J,

because A^(1/2) conjugation uses only its bounded raw-energy/discount neighborhood and Y is fixed-depth. Hence J†WJ<=C_J² W. Applying(3) first with U=Vloc=J and then with U=Vloc=I gives, on P1,

 P1 J†FJ P1<=C_J² P1 F P1+exp(-cN)P1.              (6)

Inside P, the spectral complement P-P1 is at most exp(-aN)W0. Outside P, a local J can act only on the raw boundary strip, whose amplitude is already exponentially small by(1). Thus, for a positive P1-supported state rho with x=Tr(F rho),

 Tr[(I-P1)J rho J†]
   <=C_J² exp(-aN)x+exp(-cN).                       (7)

The same estimate applies to local Hamiltonian and loss legs as bounded operators. Standard trace-norm Cauchy-Schwarz then bounds full-minus-P1-compressed generator action by

 C N exp(-aN/2)sqrt(x)+exp(-cN),                    (8)

up to the existing fixed-support joint cb constants. Actual interval-CPTP propagation contracts the Duhamel integral. With the companion killed moment x<=exp(nu N), nu<a, full-versus-killed error is polynomial(N) times physical time times exp[-(a-nu)N/2], plus the initial projection discrepancy if any.

## 5. Why the spectral projection does not assume a physical operation
P1 is an analysis projector only. The real apparatus never measures it. The actual comparison is to its positive CP/TNI compressed process, using(8). Under the companion's canonical-edge premise, every P Xi P, raw-energy/discount term, and P local physical leg P is identity on the logical factor. Functional calculus then makes P1 logical identity as well. The compressed process therefore retains the required common correctable logical span. A real fixed decoder is still supplied by the existing code-distance argument.

## Remaining actual checks
The abstract comparison requires: (a) a common high-energy boundary strip for every actual proof/physical support; (b) [P,A]=[P,E]=0; (c) finite local norm/energy-width bounds uniform in the chosen fixed proof parameters; (d) the canonical logical-edge property for all compressed proof operators; (e) a well-defined joint CP/TNI compression and actual interval-CPTP propagator. It does not grant any of these for a new apparatus automatically. The full native LOCC first-order service proof also remains under independent review, including a separately identified classical-contention correction.

## Native LOCC scope correction
The abstract logical-factor premise is stronger than is needed for the present Bell-resource application. Its accepted target is the COMMON BELL-TARGET/SHARED-GAUGE module, not arbitrary identity on the entire bilateral logical space. For that application it suffices to verify coefficientwise preservation of the admitted common module by every P0-compressed proof/physical leg. Self-adjoint proof generators then reduce that module, and their exponentials and the spectral projector preserve it by functional calculus. This transfers only the accepted Bell-target/gauge conclusion. No stronger arbitrary-joint-logical-identity result is inferred from the earlier stochastic source receipt.
