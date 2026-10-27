# Independent quadratic mixed-flag Choi-program lower bound

PASS, 27 October 2026. Scope is IID full normalized Choi programs plus an independent noisy datum, one fixed unknown U, arbitrary collective processor. No quadratic adaptive physical-query lower bound is received.

The actual program is P_U/r with rank-r P_U and Tr_A P_U=I_(3r)/3. The one-copy Haar average is I/(9r). Relative Haar invariance gives exactly (9r)^m Tr R_m²=E g^m, g=(9/r)Tr(P_I P_U), with0<=g<=9 and E g=1. Renyi2<=von Neumann entropy and log g<=g-1 imply F_m<=log E exp[m(g-1)], including g=0 without a support inverse.

Independently verified the concentration normalization in the primary [Meckes–Meckes paper, Appendix Eq(6) and proof of Theorem15](https://arxiv.org/pdf/1210.2681): their convention Ent(f²)<=2C E|grad f|² and SU(d) constant C=2/d give the required4/d coefficient. The metric is the Hilbert–Schmidt Riemannian metric. Phase invariance makes SU and U averages identical; no unsupported U(d) Ricci estimate is used.

For any unit-HS Hermitian tangent generator, differentiating the overlap gives two conjugate terms. Hilbert–Schmidt Cauchy-Schwarz and Tr_A P_U=I/3 bound its derivative by2sqrt(r/3), hence ||grad g||<=6sqrt(3/r). Applying the verified LSI to exp(tg/2) gives t psi'-psi<=t² L²/d, and integrating gives centered log MGF<=36t²/r². Boundedness on the compact group justifies every derivative. Thus F_m<=36m²/r² for all m, not just a small-m representation-theory regime.

Consistency and permutation symmetry give nondecreasing entropy increments a_m by SSA/data processing. For n>=1 all n increments from n+1 through2n dominate a_(n+1), so a_(n+1)<=(F_(2n)-F_n)/n<=144n/r². Nonnegativity F_n is relative entropy to the maximally mixed state.

The logical-label information step is exact: Tr_A R_(n+1)=R_n tensor I_d/d because the individual program output marginal is U-independent. Therefore I(A:programs B)=a_(n+1), not the much larger total program entropy deficit. Measuring A gives a uniform three-valued label and precisely the desired ensemble E[J_U^n tensor E_U(|a><a|)]. Data processing bounds its Holevo information by the increment.

Uniform unhalved complete inverse error zeta gives basis decoding error<=zeta/2 for each U, since the output differences have trace zero. Fano then gives log3-h(zeta/2)-(zeta/2)log2, positive throughout0<zeta<1. Combining yields the stated r²/144 bound. The n=0 case cannot meet the guarantee because the averaged datum is label-independent. This proof is for mixed program access, not purified programs or an inverse oracle. The separate collision bound still supplies the accuracy-dependent r log(1/zeta) requirement and the independently received linear-r adaptive-query bound.
