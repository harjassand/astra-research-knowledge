# Independent joint flag-rank/signal Choi lower bound

PASS, 27 October 2026, on the explicit integer-grid family1<=r<=D, p=r/D, IID normalized Choi-copy access. This does not receive a quadratic adaptive-query bound or an all-real-p interpolation.

The active flags contribute Phi/D and inactive flags I9/(9D), giving exactly J=I/(9D)+[(Phi-I9/9) tensor P_r]/D before the unknown output unitary. Each flag block has zero homogeneous deficit and orthogonal reset/success support, hence the original source has Delta0 and success p. Its physical program marginal is I_(3D)/(3D), independently of U.

Direct expansion (Phi-I9/9)^2=(7/9)Phi+I9/81 gives Tr A0²=8r/(9D²) and Tr_A A_U²=(8/(27D²)) U(I3 tensor P_r)U^*<=8I/(27D²). The commutator derivative and Hilbert–Schmidt Cauchy-Schwarz then yield ||grad g||<=16sqrt(r)/(sqrt3 D). The independently verified phase-invariant SU(3D) LSI/Herbst normalization gives centered log MGF<=256r t²/(9D³). The prior primary-source check is recorded in mixed_flag_quadratic_choi_independent_audit.md, citing the Meckes–Meckes Appendix.

Pair purity and Renyi entropy give F_m<=256r m²/(9D³); consistent exchangeable program marginals give nondecreasing entropy increments and a_(n+1)<=F_(2n)/n<=1024rn/(9D³). The U-independent physical marginal makes I(A_last:programs B_last) equal this increment exactly. Measuring A_last produces precisely the uniform logical-label/data ensemble. No independent-program Haar average or purified program is substituted.

For complete unhalved error delta<=p/4, event probabilities differ by at most delta/2: total acceptance z>=7p/8, wrong accepted probability<=p/8, and each input's acceptance<=9p/8. Thus conditional error<=1/7 and each accepted input posterior probability<=3/7. The latter correctly handles input-dependent acceptance; accepted labels are not assumed uniform. Min-entropy lower-bounds H(A|accept) by ln(7/3), while conditional Fano upper-bounds H(A|B,accept) by h(1/7)+ln2/7. Multiplying by acceptance and retaining nonnegative flag information gives an exact coefficient:

(7/8)[ln(7/3)-h(1/7)-ln2/7]=(1/8)ln(32/3)>1/4.

The final strict inequality is elementary: e<3 by its series, so e²<9<32/3. Thus the decimal in the source is not needed for certification. Combining label information>p/4 with the entropy-increment upper and p=r/D gives n>=9D²/4096=(9/4096)r²/p². A zero-program scheme has no Haar-averaged label information, so the n>=1 increment step loses no case.

The result is simultaneous signal/rank scaling for this exactly specified model. At p=1 the earlier stronger numerical rank constant remains valid separately; no inconsistency or optimal constant is claimed. Conditional IID means one fixed U throughout programs and independent datum. No physical adaptive-query reduction is inferred.
